from typing import Type
import gradio as gr
from swift.ui.base import BaseUI
from swift.utils import get_logger
logger = get_logger()

class Eval(BaseUI):
    group = 'llm_eval'
    locale_dict = {'eval_backend': {'label': {'zh': 'Eval backend', 'en': 'Eval backend'}, 'info': {'zh': 'Select eval backend', 'en': 'Select eval backend'}}, 'eval_dataset': {'label': {'zh': 'Evaluation dataset', 'en': 'Evaluation dataset'}, 'info': {'zh': 'Select eval dataset, multiple datasets supported (select eval backend first)', 'en': 'Select eval dataset, multiple datasets supported (select eval backend first)'}}, 'eval_limit': {'label': {'zh': 'Eval numbers for each dataset', 'en': 'Eval numbers for each dataset'}, 'info': {'zh': 'Number of rows sampled from each dataset', 'en': 'Number of rows sampled from each dataset'}}, 'eval_output_dir': {'label': {'zh': 'Eval output dir', 'en': 'Eval output dir'}, 'info': {'zh': 'The dir to save the eval results', 'en': 'The dir to save the eval results'}}, 'custom_eval_config': {'label': {'zh': 'Custom eval config', 'en': 'Custom eval config'}, 'info': {'zh': 'Use this config to eval your own datasets, check the docs in github for details', 'en': 'Use this config to eval your own datasets, check the docs in github for details'}}, 'eval_url': {'label': {'zh': 'The eval url', 'en': 'The eval url'}, 'info': {'zh': 'The OpenAI style link(like: http://localhost:8080/v1/chat/completions) for evaluation(Input actual model type into model_type)', 'en': 'The OpenAI style link(like: http://localhost:8080/v1/chat/completions) for evaluation(Input actual model type into model_type)'}}, 'api_key': {'label': {'zh': 'The url token', 'en': 'The url token'}, 'info': {'zh': 'The token used with eval_url', 'en': 'The token used with eval_url'}}, 'infer_backend': {'label': {'zh': 'Infer backend', 'en': 'Infer backend'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        try:
            from swift.llm.argument.eval_args import EvalArguments
            eval_dataset_dict = EvalArguments.list_eval_dataset()
            default_backend = EvalArguments.eval_backend
        except Exception as e:
            logger.warn(e)
            eval_dataset_dict = {}
            default_backend = None
        with gr.Row():
            gr.Dropdown(elem_id='eval_backend', choices=list(eval_dataset_dict.keys()), value=default_backend, scale=20)
            gr.Dropdown(elem_id='eval_dataset', is_list=True, choices=eval_dataset_dict.get(default_backend, []), multiselect=True, allow_custom_value=True, scale=20)
            gr.Textbox(elem_id='eval_limit', scale=20)
            gr.Dropdown(elem_id='infer_backend', scale=20)
        with gr.Row():
            gr.Textbox(elem_id='custom_eval_config', scale=20)
            gr.Textbox(elem_id='eval_output_dir', scale=20)
            gr.Textbox(elem_id='eval_url', scale=20)
            gr.Textbox(elem_id='api_key', scale=20)

        def update_eval_dataset(backend):
            return gr.update(choices=eval_dataset_dict[backend])
        cls.element('eval_backend').change(update_eval_dataset, [cls.element('eval_backend')], [cls.element('eval_dataset')])
