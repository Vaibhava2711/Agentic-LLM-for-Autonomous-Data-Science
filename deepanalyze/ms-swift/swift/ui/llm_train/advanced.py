from typing import Type
import gradio as gr
from swift.ui.base import BaseUI

class Advanced(BaseUI):
    group = 'llm_train'
    locale_dict = {'advanced_tab': {'label': {'zh': 'Advanced settings', 'en': 'Advanced settings'}}, 'tuner_backend': {'label': {'zh': 'Tuner backend', 'en': 'Tuner backend'}, 'info': {'zh': 'The tuner backend', 'en': 'The tuner backend'}}, 'weight_decay': {'label': {'zh': 'Weight decay', 'en': 'Weight decay'}, 'info': {'zh': 'Set the weight decay', 'en': 'Set the weight decay'}}, 'logging_steps': {'label': {'zh': 'Logging steps', 'en': 'Logging steps'}, 'info': {'zh': 'Set the logging interval', 'en': 'Set the logging interval'}}, 'lr_scheduler_type': {'label': {'zh': 'The LrScheduler type', 'en': 'The LrScheduler type'}, 'info': {'zh': 'Set the LrScheduler type', 'en': 'Set the LrScheduler type'}}, 'warmup_ratio': {'label': {'zh': 'Lr warmup ratio', 'en': 'Lr warmup ratio'}, 'info': {'zh': 'Set the warmup ratio in total steps', 'en': 'Set the warmup ratio in total steps'}}, 'truncation_strategy': {'label': {'zh': 'Dataset truncation strategy', 'en': 'Dataset truncation strategy'}, 'info': {'zh': 'How to deal with the rows exceed the max length', 'en': 'How to deal with the rows exceed the max length'}}, 'max_steps': {'label': {'zh': 'Max steps', 'en': 'Max steps'}, 'info': {'zh': 'Set the max steps, if the value > 0 then num_train_epochs has no effects', 'en': 'Set the max steps, if the value > 0 then num_train_epochs has no effects'}}, 'max_grad_norm': {'label': {'zh': 'Max grad norm', 'en': 'Max grad norm'}, 'info': {'zh': 'Set the max grad norm', 'en': 'Set the max grad norm'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.TabItem(elem_id='advanced_tab'):
            with gr.Blocks():
                with gr.Row():
                    gr.Dropdown(elem_id='tuner_backend', scale=20)
                    gr.Textbox(elem_id='weight_decay', lines=1, scale=20)
                    gr.Textbox(elem_id='logging_steps', lines=1, scale=20)
                    gr.Textbox(elem_id='lr_scheduler_type', lines=1, scale=20)
                with gr.Row():
                    gr.Dropdown(elem_id='truncation_strategy', value=None, scale=20)
                    gr.Textbox(elem_id='max_steps', lines=1, scale=20)
                    gr.Textbox(elem_id='max_grad_norm', lines=1, scale=20)
                    gr.Slider(elem_id='warmup_ratio', minimum=0.0, maximum=1.0, step=0.05, scale=20)
