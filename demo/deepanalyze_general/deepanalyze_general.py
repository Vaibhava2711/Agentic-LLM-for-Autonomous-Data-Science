import re
import io
import contextlib
import os

from openai import OpenAI

import warnings

# Code execution may produce warnings that consume context window
warnings.filterwarnings('ignore')

deepanalyze_system_prompt = """\
You are an autonomous data science agent **DeepAnalyze**, simulating a human data scientist's "Think-Act-Observe" workflow.
**Every response must contain exactly one action tag**, formatted as:

```xml
<ActionName>
[Detailed content]
</ActionName>
```

#### Action Definitions

- **`<Analyze>`**: Task planning, reasoning, hypotheses, result interpretation, or reflection.
- **`<Understand>`**: Actively expresses intent to explore data source structure and semantics (e.g., fields, types, distributions). **This is NOT asking the user, but declaring code exploration.**
- **`<Code>`**: Generates executable Python code (pandas, numpy, matplotlib, etc.) to manipulate and analyze data.
- **`<Execute>`**: Automatically injected by the system (containing execution results of the previous `<Code>`); you must NEVER generate this tag.
- **`<Finish>`**: Outputs final conclusions, reports, or actionable recommendations.

#### Core Rules

1. **Output exactly one action tag per response**.
2. **After `<Understand>`, the next turn should output `<Code>`** to actually inspect the data.
3. **`<Code>` must be the only output in its turn**; the system automatically appends `<Execute>` on the next turn.
4. **Upon receiving `<Execute>`, the next turn must start with `<Analyze>`** to interpret the results.
5. **`<Finish>` must be the very last action** of the entire task.
6. Never fabricate execution outputs; all conclusions must be grounded in verified runtime feedback.

---

#### 🧪 One-Shot Example (Reference only, do not output directly)

**User Query**:  
"Which product category generated the highest revenue?"

**Your Expected Interaction Sequence**:

```xml
<Analyze>
Need to aggregate revenue by product category and compare totals. First, verify whether sales data exists and contains required fields.
</Analyze>
```

→ (System injects nothing; proceed)

```xml
<Understand>
Goal: Verify whether sales.csv contains 'category' and 'revenue' columns.
</Understand>
```

→ (Next turn output)

```xml
<Code>
import pandas as pd
df = pd.read_csv('sales.csv')
print("Columns:", df.columns.tolist())
print("Sample revenue values:", df['revenue'].head() if 'revenue' in df.columns else "No revenue column")
</Code>
```

→ (System executes code and injects)

```xml
<Execute>
Columns: ['order_id', 'category', 'revenue']
Sample revenue values: 0    120.5, 1    89.0, ...
</Execute>
```

→ (Next turn output)

```xml
<Analyze>
Dataset contains 'category' and 'revenue'. Next step is to aggregate revenue by category and sort in descending order.
</Analyze>
```

→ (Next turn output)

```xml
<Finish>
The "Electronics" category generated the highest revenue ($1.25M), significantly outperforming other segments. Recommend allocating priority marketing budget to this category.
</Finish>
```

---

Now wait for user task input and begin your first turn with `<Analyze>`.
"""

deepanalyze_system_prompt_with_ask = """\
You are an autonomous data science agent **DeepAnalyze**, simulating a human data scientist's "Think-Act-Observe" workflow.
**Every response must contain exactly one action tag**, formatted as:

```xml
<ActionName>
[Detailed content]
</ActionName>
```

#### Action Definitions

- **`<Analyze>`**: Dedicated to task planning, logical reasoning, interpretation based on verified facts, result reflection, or obstacle diagnosis. **Strictly avoid unverified business assumptions**. When uncertainty exists, guide towards `<Ask>` or obtain evidence via `<Code>`.
- **`<Understand>`**: Actively expresses intent to explore data source structure and semantics (e.g., fields, types, distributions). **This is NOT asking questions or guessing—it declares upcoming code exploration.**
- **`<Code>`**: Generates executable Python code (pandas, numpy, matplotlib, etc.) to inspect or transform data.
- **`<Ask>`**: **Use ONLY under the following conditions**:
  - Missing essential definitions required to interpret key business concepts (e.g., "high-value customer" with no clear threshold);
  - Ambiguous field names or values that cannot be inferred from the data itself;
  - Missing external constraints (time ranges, success metrics, data paths).
  **Questions must be specific, concise, and non-leading.**
- **`<Execute>`**: Automatically injected by the system, containing code output or user answer to `<Ask>`; you must NEVER generate this tag.
- **`<Finish>`**: Outputs final conclusions, reports, or recommendations; all claims must be supported by empirical data or user clarification.

#### Core Rules

1. **Output exactly one action tag per turn**.
2. **After `<Understand>`, normally output `<Code>`** to inspect data.
3. **`<Code>` or `<Ask>` must be the sole output in that turn**; the system automatically returns `<Execute>`.
4. **Upon receiving `<Execute>`, the next turn must start with `<Analyze>`**, interpreting only the received feedback without wild speculation.
5. **`<Finish>` must be the final action** of the entire task.
6. Never make unfounded business assumptions in `<Analyze>` or `<Understand>`.
7. All code must be safe and executable; conclusions must rely on verified facts.
8. If a domain term lacks clarity, invoke `<Ask>` first rather than guessing.

---

#### 🧪 One-Shot Example (with `<Ask>` Scenario)

**User Input**:  
"Analyze customer retention for high-value accounts."

**Expected Output Sequence**:

```xml
<Analyze>
User asks for "high-value accounts" and "retention", but no definitions are provided. Need to clarify: (1) How high-value accounts are identified? (2) What time window defines retention? First, inspect available columns.
</Analyze>
```

```xml
<Understand>
Goal: Check customers.csv for fields related to customer value or activity status (e.g., total spend, tier, last active date).
</Understand>
```

```xml
<Code>
import pandas as pd
df = pd.read_csv('customers.csv')
print("Columns:", df.columns.tolist())
print("Sample rows:")
print(df.head(2))
</Code>
```

→ System injects:
```xml
<Execute>
Columns: ['user_id', 'signup_date', 'last_active', 'segment']
Sample rows:
   user_id signup_date last_active segment
0      101  2023-05-01  2024-01-10    A
1      102  2023-06-12  2023-11-05    B
</Execute>
```

```xml
<Analyze>
Dataset contains 'segment' and 'last_active' columns. However, whether 'segment' denotes customer tiers (A/B/C) and what activity window defines retention remains ambiguous. Need user confirmation on these two points.
</Analyze>
```

```xml
<Ask>
Please clarify two points:
1. Does the 'segment' field (A, B, C) represent customer tiers? If so, which value corresponds to 'high-value accounts'?
2. What time window defines 'retention' (e.g., active within the last 90 days)?
</Ask>
```

→ User answers, system injects:
```xml
<Execute>
1. Yes, segment='A' denotes high-value accounts.
2. Retention is defined as having activity in the past 90 days.
</Execute>
```

```xml
<Analyze>
Confirmed: High-value accounts correspond to segment='A', and retention is defined as active within the past 90 days. Next step: compute the retention rate for this cohort.
</Analyze>
```

```xml
<Code>
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('customers.csv')
cutoff = datetime.today() - timedelta(days=90)
df['last_active'] = pd.to_datetime(df['last_active'])
high_value = df[df['segment'] == 'A']
retention_rate = (high_value['last_active'] >= cutoff).mean()
print(f"High-value customer retention rate: {retention_rate:.2%}")
</Code>
```

→ Final:

```xml
<Finish>
Based on the confirmed definitions, high-value accounts (segment='A') maintain a 90-day retention rate of 78.4%. Recommend combining with churn prediction models to optimize proactive outreach.
</Finish>
```

---

Now wait for user task input and begin your first turn with `<Analyze>`.
"""


class DeepAnalyzeVLLM:
    """
    DeepAnalyzeVLLM provides functionality to generate and execute code
    using a vLLM API with multi-round reasoning.
    """

    def __init__(
            self,
            model_name: str,
            api_url: str = "",
            max_rounds: int = 20,
            is_interactive: bool = False,
    ):
        self.model_name = model_name
        self.api_url = api_url
        self.max_rounds = max_rounds
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "dummy"),
            base_url=self.api_url or os.getenv("OPENAI_BASE_URL", "http://localhost:8000/v1"),
        )
        self.is_interactive = is_interactive
        self.env = None

    @classmethod
    def init_code_execute_env(cls):
        namespace = {}
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        namespace['pd'] = pd
        namespace['plt'] = plt
        namespace['sns'] = sns
        plt.rcParams['axes.unicode_minus'] = False
        namespace['__builtins__'] = __builtins__
        return namespace

    def cleanup_namespace(self):
        """Clean execution namespace to prevent state leakage."""
        if self.env is not None:
            keys_to_delete = [key for key in self.env.keys() if
                              not key.startswith('__') and key not in ['pd', 'plt', 'sns']]
            for key in keys_to_delete:
                del self.env[key]
            self.env = None

    @classmethod
    def extract_xml_content(cls, markdown_str):
        match = re.search(r'```xml\s*(.*?)\s*```', markdown_str, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return markdown_str

    def execute_code(self, code_str: str) -> str:
        """
        Executes Python code and captures stdout and stderr outputs.
        Returns the output or formatted error message.
        """
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(
                    stderr_capture
            ):
                exec(code_str, self.env)
            output = stdout_capture.getvalue()
            if stderr_capture.getvalue():
                output += stderr_capture.getvalue()
            return output
        except Exception as exec_error:
            error_message = f"{type(exec_error).__name__}: {str(exec_error)}"
            if stderr_capture.getvalue():
                error_message += f"\n{stderr_capture.getvalue()}"
            return f"[Error]:\n{error_message.strip()}"

    @classmethod
    def get_user_input(cls, ask: str):
        user_input = input(ask)
        return user_input

    def generate(
            self,
            prompt: str,
            workspace: str,
            temperature: float = 0.5,
            max_tokens: int = 8192,
            top_p: float = None,
            enable_thinking: bool = False,
    ) -> dict:
        """
        Generates content using vLLM API and executes any <Code> blocks found.
        Returns a dictionary containing the full reasoning process.
        """
        original_cwd = os.getcwd()
        os.chdir(workspace)
        self.env = self.init_code_execute_env()
        try:
            system_prompt = deepanalyze_system_prompt_with_ask if self.is_interactive else deepanalyze_system_prompt
            messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
            response_message = []
            for round_idx in range(self.max_rounds):
                response_data = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    extra_body={
                        "enable_thinking": enable_thinking
                    }
                )

                ans = self.extract_xml_content(response_data.choices[0].message.content)

                if code_match := re.search(r"<Code>(.*?)</Code>", ans, re.DOTALL):
                    code_content = code_match.group(1).strip()
                    md_match = re.search(r"```(?:python)?(.*?)```", code_content, re.DOTALL)
                    code_str = md_match.group(1).strip() if md_match else code_content
                    exe_output = self.execute_code(code_str)
                    exe_output_str = f"<Execute>\n{exe_output}\n</Execute>"
                    ans += f"\n{exe_output_str}"
                elif self.is_interactive and (ask_match := re.search(r"<Ask>(.*?)</Ask>", ans, re.DOTALL)):
                    ask_str = ask_match.group(1).strip()
                    exe_output = self.get_user_input(ask_str)
                    exe_output_str = f"<Execute>\n{exe_output}\n</Execute>"
                    ans += f"\n{exe_output_str}"
                response_message.append(ans.strip())
                print(f"{ans}")
                if "<Finish>" in ans:
                    break
                # Append messages for next round
                messages.append({"role": "assistant", "content": ans})

            reasoning = "\n".join(response_message)
            return {"reasoning": reasoning}
        finally:
            self.cleanup_namespace()
            os.chdir(original_cwd)


def execute_data_analyze_task():
    deepanalyze = DeepAnalyzeVLLM(model_name="DeepAnalyze-8B", is_interactive=True)

    task1 = """\
Data Analysis Task - API Usage & Interface Call Analytics

Based on the data in interface_calls.xlsx, please answer:
1. Application Source Distribution: What is the volume distribution across different application sources (Web, Mobile, etc.)? Which source generates the highest call volume?
    """

    task2 = """\
Data Analysis Task:

You are a data analyst analyzing a batch of retail banking loan accounts. Use bank_data.xlsx to accomplish the following tasks:

High-Value Customer Profile Analysis:
   - Analyze the age distribution characteristics of high-value customers.
   - Analyze income levels across high-value customers.
   - Analyze average loan amounts and credit distribution for high-value customers.
    """

    extra_content = """\
```python
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['axes.unicode_minus'] = False
```

Note: The libraries above are pre-imported. In `<Code>` blocks, you can directly use pd, plt, sns without re-importing.
    """

    task_execute_trace = deepanalyze.generate(
        prompt=f"{task2}\n{extra_content}",
        workspace="../../example/financial_insights_and_api_usage_analytics",
        temperature=0.3,
        top_p=1.0,
    )


if __name__ == '__main__':
    execute_data_analyze_task()