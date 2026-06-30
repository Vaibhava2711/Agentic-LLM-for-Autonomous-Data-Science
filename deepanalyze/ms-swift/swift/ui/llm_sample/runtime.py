from swift.ui.llm_infer.runtime import Runtime
from swift.utils import get_logger
logger = get_logger()

class SampleRuntime(Runtime):
    group = 'llm_sample'
    cmd = 'sample'
    locale_dict = {'runtime_tab': {'label': {'zh': 'Runtime', 'en': 'Runtime'}}, 'running_cmd': {'label': {'zh': 'Command line', 'en': 'Command line'}, 'info': {'zh': 'The actual command', 'en': 'The actual command'}}, 'show_log': {'value': {'zh': 'Show running status', 'en': 'Show running status'}}, 'stop_show_log': {'value': {'zh': 'Stop showing running status', 'en': 'Stop showing running status'}}, 'log': {'label': {'zh': 'Logging content', 'en': 'Logging content'}, 'info': {'zh': 'Please press "Show running status" if the log content is not updating', 'en': 'Please press "Show running status" if the log content is not updating'}}, 'running_tasks': {'label': {'zh': 'Running sampling', 'en': 'Running sampling'}, 'info': {'zh': 'Started by swift sample', 'en': 'Started by swift sample'}}, 'refresh_tasks': {'value': {'zh': 'Find sampling', 'en': 'Find sampling'}}, 'kill_task': {'value': {'zh': 'Kill running task', 'en': 'Kill running task'}}}
