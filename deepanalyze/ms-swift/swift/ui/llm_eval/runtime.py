from typing import Type
import gradio as gr
from packaging import version
from swift.ui.base import BaseUI
from swift.ui.llm_infer.runtime import Runtime
from swift.utils import get_logger
logger = get_logger()

class EvalRuntime(Runtime):
    group = 'llm_eval'
    cmd = 'eval'
    locale_dict = {'runtime_tab': {'label': {'zh': 'Runtime', 'en': 'Runtime'}}, 'running_cmd': {'label': {'zh': 'Command line', 'en': 'Command line'}, 'info': {'zh': 'The actual command', 'en': 'The actual command'}}, 'show_log': {'value': {'zh': 'Show eval status', 'en': 'Show eval status'}}, 'stop_show_log': {'value': {'zh': 'Stop showing running status', 'en': 'Stop showing running status'}}, 'log': {'label': {'zh': 'Logging content', 'en': 'Logging content'}, 'info': {'zh': 'Please press "Show eval status" if the log content is not updating', 'en': 'Please press "Show eval status" if the log content is not updating'}}, 'running_tasks': {'label': {'zh': 'Running evaluation', 'en': 'Running evaluation'}, 'info': {'zh': 'All tasks started by swift eval', 'en': 'All tasks started by swift eval'}}, 'refresh_tasks': {'value': {'zh': 'Find evaluation', 'en': 'Find evaluation'}}, 'kill_task': {'value': {'zh': 'Kill evaluation', 'en': 'Kill evaluation'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Accordion(elem_id='runtime_tab', open=False, visible=True):
            with gr.Blocks():
                with gr.Row(equal_height=True):
                    gr.Dropdown(elem_id='running_tasks', scale=10)
                    gr.Button(elem_id='refresh_tasks', scale=1, variant='primary')
                    gr.Button(elem_id='show_log', scale=1, variant='primary')
                    gr.Button(elem_id='stop_show_log', scale=1)
                    gr.Button(elem_id='kill_task', scale=1, size='lg')
                with gr.Row():
                    gr.Textbox(elem_id='log', lines=6, visible=False)
                concurrency_limit = {}
                if version.parse(gr.__version__) >= version.parse('4.0.0'):
                    concurrency_limit = {'concurrency_limit': 5}
                cls.log_event = base_tab.element('show_log').click(cls.update_log, [], [cls.element('log')]).then(cls.wait, [base_tab.element('running_tasks')], [cls.element('log')], **concurrency_limit)
                base_tab.element('stop_show_log').click(cls.break_log_event, [cls.element('running_tasks')], [])
                base_tab.element('refresh_tasks').click(cls.refresh_tasks, [base_tab.element('running_tasks')], [base_tab.element('running_tasks')])
