from swift.ui.llm_infer.runtime import Runtime
from swift.utils import get_logger
logger = get_logger()

class ExportRuntime(Runtime):
    group = 'llm_export'
    cmd = 'export'
    locale_dict = {'runtime_tab': {'label': {'zh': 'Runtime', 'en': 'Runtime'}}, 'running_cmd': {'label': {'zh': 'Command line', 'en': 'Command line'}, 'info': {'zh': 'The actual command', 'en': 'The actual command'}}, 'show_log': {'value': {'zh': 'Show export status', 'en': 'Show export status'}}, 'stop_show_log': {'value': {'zh': 'Stop showing running status', 'en': 'Stop showing running status'}}, 'log': {'label': {'zh': 'Logging content', 'en': 'Logging content'}, 'info': {'zh': 'Please press "Show export status" if the log content is not updating', 'en': 'Please press "Show export status" if the log content is not updating'}}, 'running_tasks': {'label': {'zh': 'Running export task', 'en': 'Running export task'}, 'info': {'zh': 'All tasks started by swift export', 'en': 'All tasks started by swift export'}}, 'refresh_tasks': {'value': {'zh': 'Find export', 'en': 'Find export'}}, 'kill_task': {'value': {'zh': 'Kill export', 'en': 'Kill export'}}}
