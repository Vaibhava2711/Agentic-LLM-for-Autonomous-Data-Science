from functools import partial
from typing import Type
import gradio as gr
from swift.llm import TEMPLATE_MAPPING, DeployArguments, ModelType
from swift.llm.model.register import get_all_models
from swift.ui.base import BaseUI
from swift.ui.llm_infer.generate import Generate

class Model(BaseUI):
    llm_train = 'llm_infer'
    sub_ui = [Generate]
    locale_dict = {'model_type': {'label': {'zh': 'Select Model Type', 'en': 'Select Model Type'}, 'info': {'zh': 'Base model type supported by SWIFT', 'en': 'Base model type supported by SWIFT'}}, 'load_checkpoint': {'value': {'zh': 'Deploy model', 'en': 'Deploy model'}}, 'model': {'label': {'zh': 'Model id or path', 'en': 'Model id or path'}, 'info': {'zh': 'The actual model id or path, if is a trained model, please fill in the checkpoint-xxx dir', 'en': 'The actual model id or path, if is a trained model, please fill in the checkpoint-xxx dir'}}, 'template': {'label': {'zh': 'Prompt template type', 'en': 'Prompt template type'}, 'info': {'zh': 'Choose the template type of the model', 'en': 'Choose the template type of the model'}}, 'merge_lora': {'label': {'zh': 'Merge LoRA', 'en': 'Merge LoRA'}, 'info': {'zh': 'Only available when `sft_type=lora`', 'en': 'Only available when `sft_type=lora`'}}, 'lora_modules': {'label': {'zh': 'More LoRA modules', 'en': 'More LoRA modules'}, 'info': {'zh': 'name=/path1/path2 split by blanks', 'en': 'name=/path1/path2 split by blanks'}}, 'more_params': {'label': {'zh': 'More params', 'en': 'More params'}, 'info': {'zh': 'Fill in with json format or --xxx xxx cmd format', 'en': 'Fill in with json format or --xxx xxx cmd format'}}, 'reset': {'value': {'zh': 'Reset to default', 'en': 'Reset to default'}}, 'infer_backend': {'label': {'zh': 'Infer backend', 'en': 'Infer backend'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Row(equal_height=True):
            gr.Dropdown(elem_id='model', scale=20, choices=get_all_models(), value='Qwen/Qwen2.5-7B-Instruct', allow_custom_value=True)
            gr.Dropdown(elem_id='model_type', choices=ModelType.get_model_name_list(), scale=20)
            gr.Dropdown(elem_id='template', choices=list(TEMPLATE_MAPPING.keys()), scale=20)
            gr.Checkbox(elem_id='merge_lora', scale=4)
            gr.Button(elem_id='reset', scale=2)
        with gr.Row():
            gr.Dropdown(elem_id='infer_backend', value='pt', scale=5)
        Generate.set_lang(cls.lang)
        Generate.build_ui(base_tab)
        with gr.Row(equal_height=True):
            gr.Textbox(elem_id='lora_modules', lines=1, is_list=True, scale=40)
            gr.Textbox(elem_id='more_params', lines=1, scale=20)
            gr.Button(elem_id='load_checkpoint', scale=2, variant='primary')

    @classmethod
    def after_build_ui(cls, base_tab: Type['BaseUI']):
        cls.element('model').change(partial(cls.update_input_model, arg_cls=DeployArguments, has_record=False), inputs=[cls.element('model')], outputs=list(cls.valid_elements().values()))
