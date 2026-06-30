import os
import gradio as gr
from swift.ui.llm_train.runtime import Runtime
from swift.utils import get_logger
logger = get_logger()

class GRPORuntime(Runtime):
    group = 'llm_grpo'
    locale_dict = {'runtime_tab': {'label': {'zh': 'Runtime', 'en': 'Runtime'}}, 'tb_not_found': {'value': {'zh': 'tensorboard not found, install it by `pip install tensorboard`', 'en': 'tensorboard not found, install it by `pip install tensorboard`'}}, 'running_cmd': {'label': {'zh': 'Command line', 'en': 'Command line'}, 'info': {'zh': 'The actual command', 'en': 'The actual command'}}, 'show_running_cmd': {'value': {'zh': 'Show running command line', 'en': 'Show running command line'}}, 'show_sh': {'label': {'zh': 'Show sh command line', 'en': 'Show sh command line'}}, 'cmd_sh': {'label': {'zh': 'Training command line', 'en': 'Training command line'}, 'info': {'zh': 'Please press "Show running command line" if the content is none, click the "Save training command" below to save the sh script', 'en': 'Please press "Show running command line" if the content is none, click the "Save training command" below to save the sh script'}}, 'save_cmd_as_sh': {'value': {'zh': 'Save training command', 'en': 'Save training command'}}, 'save_cmd_alert': {'value': {'zh': 'The training command line will be saved in: {}', 'en': 'The training command line will be saved in: {}'}}, 'close_cmd_show': {'value': {'zh': 'Close training command show', 'en': 'Close training command show'}}, 'show_log': {'value': {'zh': 'Show running status', 'en': 'Show running status'}}, 'stop_show_log': {'value': {'zh': 'Stop showing running status', 'en': 'Stop showing running status'}}, 'logging_dir': {'label': {'zh': 'Logging dir', 'en': 'Logging dir'}, 'info': {'zh': 'Support fill custom path in', 'en': 'Support fill custom path in'}}, 'log': {'label': {'zh': 'Logging content', 'en': 'Logging content'}, 'info': {'zh': 'Please press "Show running status" if the log content is not updating', 'en': 'Please press "Show running status" if the log content is not updating'}}, 'running_tasks': {'label': {'zh': 'Running Tasks', 'en': 'Running Tasks'}, 'info': {'zh': 'All running tasks(started by `swift rlhf --rlhf_type grpo`)', 'en': 'All running tasks(started by `swift rlhf --rlhf_type grpo`)'}}, 'refresh_tasks': {'value': {'zh': 'Find running tasks', 'en': 'Find running tasks'}}, 'kill_task': {'value': {'zh': 'Kill running task', 'en': 'Kill running task'}}, 'tb_url': {'label': {'zh': 'Tensorboard URL', 'en': 'Tensorboard URL'}, 'info': {'zh': 'Not editable', 'en': 'Not editable'}}, 'start_tb': {'value': {'zh': 'Start TensorBoard', 'en': 'Start TensorBoard'}}, 'close_tb': {'value': {'zh': 'Close TensorBoard', 'en': 'Close TensorBoard'}}}

    @classmethod
    def save_cmd(cls, cmd):
        if len(cmd) > 0:
            (cmd_sh, output_dir) = cls.cmd_to_sh_format(cmd)
            os.makedirs(output_dir, exist_ok=True)
            sh_file_path = os.path.join(output_dir, 'grpo.sh')
            gr.Info(cls.locale('save_cmd_alert', cls.lang)['value'].format(sh_file_path))
            with open(sh_file_path, 'w', encoding='utf-8') as f:
                f.write(cmd_sh)
