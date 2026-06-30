from functools import partial
from typing import Type
import gradio as gr
from swift.llm import TEMPLATE_MAPPING, EvalArguments, ModelType
from swift.llm.model.register import get_all_models
from swift.ui.base import BaseUI

class Model(BaseUI):
    group = 'llm_eval'
    locale_dict = {'checkpoint': {'value': {'zh': 'Trained model', 'en': 'Trained model'}}, 'model_type': {'label': {'zh': 'Select Model Type', 'en': 'Select Model Type'}, 'info': {'zh': 'Base model type supported by SWIFT', 'en': 'Base model type supported by SWIFT'}}, 'model': {'label': {'zh': 'Model id or path', 'en': 'Model id or path'}, 'info': {'zh': 'The actual model id or path, if is a trained model, please fill in the checkpoint-xxx dir', 'en': 'The actual model id or path, if is a trained model, please fill in the checkpoint-xxx dir'}}, 'reset': {'value': {'zh': 'Reset to default', 'en': 'Reset to default'}}, 'template': {'label': {'zh': 'Prompt template type', 'en': 'Prompt template type'}, 'info': {'zh': 'Choose the template type of the model', 'en': 'Choose the template type of the model'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Row():
            gr.Dropdown(elem_id='model', scale=20, choices=get_all_models(), value='Qwen/Qwen2.5-7B-Instruct', allow_custom_value=True)
            gr.Dropdown(elem_id='model_type', choices=ModelType.get_model_name_list(), scale=20)
            gr.Dropdown(elem_id='template', choices=list(TEMPLATE_MAPPING.keys()), scale=20)

    @classmethod
    def after_build_ui(cls, base_tab: Type['BaseUI']):
        cls.element('model').change(partial(cls.update_input_model, arg_cls=EvalArguments, has_record=False), inputs=[cls.element('model')], outputs=list(cls.valid_elements().values()))
