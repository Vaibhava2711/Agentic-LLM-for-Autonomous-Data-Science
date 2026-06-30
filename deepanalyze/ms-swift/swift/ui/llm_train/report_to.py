from typing import Type
import gradio as gr
from swift.ui.base import BaseUI

class ReportTo(BaseUI):
    group = 'llm_train'
    locale_dict = {'reporter_tab': {'label': {'zh': 'Training report', 'en': 'Training report'}}, 'report_to': {'label': {'zh': 'Report to', 'en': 'Report to'}}, 'swanlab_token': {'label': {'zh': 'The login token of SwanLab', 'en': 'The login token of SwanLab'}}, 'swanlab_project': {'label': {'zh': 'Project of SwanLab', 'en': 'Project of SwanLab'}}, 'swanlab_workspace': {'label': {'zh': 'Workspace of SwanLab', 'en': 'Workspace of SwanLab'}}, 'swanlab_exp_name': {'label': {'zh': 'Experiment of SwanLab', 'en': 'Experiment of SwanLab'}}, 'swanlab_lark_webhook_url': {'label': {'zh': 'Webhook URL of SwanLab Lark Callback', 'en': 'Webhook URL of SwanLab Lark Callback'}}, 'swanlab_lark_secret': {'label': {'zh': 'Secret of SwanLab Lark Callback', 'en': 'Secret of SwanLab Lark Callback'}}, 'swanlab_mode': {'label': {'zh': 'Work mode of SwanLab', 'en': 'Work mode of SwanLab'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.TabItem(elem_id='reporter_tab'):
            with gr.Blocks():
                with gr.Row():
                    gr.Dropdown(elem_id='report_to', multiselect=True, is_list=True, choices=['tensorboard', 'wandb', 'swanlab'], allow_custom_value=True, scale=20)
                    gr.Textbox(elem_id='swanlab_token', lines=1, scale=20)
                    gr.Textbox(elem_id='swanlab_project', lines=1, scale=20)
                with gr.Row():
                    gr.Textbox(elem_id='swanlab_lark_webhook_url', lines=1, scale=20)
                    gr.Textbox(elem_id='swanlab_lark_secret', lines=1, scale=20)
                with gr.Row():
                    gr.Textbox(elem_id='swanlab_workspace', lines=1, scale=20)
                    gr.Textbox(elem_id='swanlab_exp_name', lines=1, scale=20)
                    gr.Dropdown(elem_id='swanlab_mode', scale=20)
