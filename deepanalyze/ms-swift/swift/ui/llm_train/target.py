from typing import Type
import gradio as gr
from swift.ui.base import BaseUI

class Target(BaseUI):
    group = 'llm_train'
    locale_dict = {'target_params': {'label': {'zh': 'Tuner modules params', 'en': 'Tuner modules params'}}, 'freeze_llm': {'label': {'zh': 'Freeze LLM', 'en': 'Freeze LLM'}}, 'freeze_aligner': {'label': {'zh': 'Freeze aligner', 'en': 'Freeze aligner'}}, 'freeze_vit': {'label': {'zh': 'Freeze ViT', 'en': 'Freeze ViT'}}, 'target_modules': {'label': {'zh': 'Specify the tuner module', 'en': 'Specify the tuner module'}}, 'target_regex': {'label': {'zh': 'Tuner module regex expression', 'en': 'Tuner module regex expression'}}, 'modules_to_save': {'label': {'zh': 'Original model modules to train and save', 'en': 'Original model modules to train and save'}}, 'init_weights': {'label': {'zh': 'Init tuner weights', 'en': 'Init tuner weights'}, 'info': {'zh': 'LoRA: gaussian/pissa/pissa_niter_[n]/olora/loftq/lora-ga/true/false,Bone: bat/true/false', 'en': 'LoRA: gaussian/pissa/pissa_niter_[n]/olora/loftq/lora-ga/true/false,Bone: bat/true/false'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Blocks():
            with gr.Row():
                gr.Textbox(elem_id='target_modules', lines=1, value='all-linear', is_list=True, scale=5)
                gr.Checkbox(elem_id='freeze_llm', scale=5)
                gr.Checkbox(elem_id='freeze_aligner', scale=5)
                gr.Checkbox(elem_id='freeze_vit', scale=5)
            with gr.Row():
                gr.Textbox(elem_id='target_regex', scale=5)
                gr.Textbox(elem_id='modules_to_save', scale=5)
                gr.Textbox(elem_id='init_weights', scale=5)
