from typing import Type
import gradio as gr
from swift.ui.base import BaseUI

class Save(BaseUI):
    group = 'llm_train'
    locale_dict = {'save_tab': {'label': {'zh': 'Saving settings', 'en': 'Saving settings'}}, 'push_to_hub': {'label': {'zh': 'Push to modelscope hub', 'en': 'Push to modelscope hub'}, 'info': {'zh': 'Whether push the output model to modelscope hub', 'en': 'Whether push the output model to modelscope hub'}}, 'hub_model_id': {'label': {'zh': 'The model-id in modelscope', 'en': 'The model-id in modelscope'}, 'info': {'zh': 'Set the model-id of modelscope', 'en': 'Set the model-id of modelscope'}}, 'hub_private_repo': {'label': {'zh': 'Model is private', 'en': 'Model is private'}, 'info': {'zh': 'Set the model as private', 'en': 'Set the model as private'}}, 'hub_strategy': {'label': {'zh': 'Push strategy', 'en': 'Push strategy'}, 'info': {'zh': 'Set the push strategy', 'en': 'Set the push strategy'}}, 'hub_token': {'label': {'zh': 'The hub token', 'en': 'The hub token'}, 'info': {'zh': 'Find the token in www.modelscope.cn', 'en': 'Find the token in www.modelscope.cn'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.TabItem(elem_id='save_tab'):
            with gr.Blocks():
                with gr.Row():
                    gr.Checkbox(elem_id='push_to_hub', scale=20)
                    gr.Textbox(elem_id='hub_model_id', lines=1, scale=20)
                    gr.Checkbox(elem_id='hub_private_repo', scale=20)
                    gr.Dropdown(elem_id='hub_strategy', scale=20, choices=['end', 'every_save', 'checkpoint', 'all_checkpoints'])
                    gr.Textbox(elem_id='hub_token', lines=1, scale=20)
