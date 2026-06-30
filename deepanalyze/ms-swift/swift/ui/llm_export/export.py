from typing import Type
import gradio as gr
from swift.llm.dataset.register import get_dataset_list
from swift.ui.base import BaseUI

class Export(BaseUI):
    group = 'llm_export'
    locale_dict = {'merge_lora': {'label': {'zh': 'Merge LoRA', 'en': 'Merge LoRA'}, 'info': {'zh': 'The output path is in the sibling directory as the input checkpoint. Please refer to the runtime log for more specific information.', 'en': 'The output path is in the sibling directory as the input checkpoint. Please refer to the runtime log for more specific information.'}}, 'device_map': {'label': {'zh': 'The device_map when merge-lora', 'en': 'The device_map when merge-lora'}, 'info': {'zh': 'If GPU memory is not enough, fill in cpu', 'en': 'If GPU memory is not enough, fill in cpu'}}, 'quant_bits': {'label': {'zh': 'Quantize bits', 'en': 'Quantize bits'}}, 'quant_method': {'label': {'zh': 'Quantize method', 'en': 'Quantize method'}}, 'quant_n_samples': {'label': {'zh': 'Sampled rows from calibration dataset', 'en': 'Sampled rows from calibration dataset'}}, 'max_length': {'label': {'zh': 'The quantize sequence length', 'en': 'The quantize sequence length'}}, 'output_dir': {'label': {'zh': 'Output dir', 'en': 'Output dir'}}, 'dataset': {'label': {'zh': 'Calibration datasets', 'en': 'Calibration datasets'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Row():
            gr.Checkbox(elem_id='merge_lora', scale=10)
            gr.Textbox(elem_id='device_map', scale=20)
        with gr.Row():
            gr.Dropdown(elem_id='quant_bits', scale=20)
            gr.Dropdown(elem_id='quant_method', scale=20)
            gr.Textbox(elem_id='quant_n_samples', scale=20)
            gr.Textbox(elem_id='max_length', scale=20)
        with gr.Row():
            gr.Textbox(elem_id='output_dir', scale=20)
            gr.Dropdown(elem_id='dataset', multiselect=True, allow_custom_value=True, choices=get_dataset_list(), scale=20)
