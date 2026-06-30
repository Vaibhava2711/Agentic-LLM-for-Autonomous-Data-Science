from typing import Type
import gradio as gr
from swift.llm.dataset.register import get_dataset_list
from swift.ui.base import BaseUI

class Dataset(BaseUI):
    group = 'llm_train'
    locale_dict = {'dataset': {'label': {'zh': 'Dataset Code', 'en': 'Dataset Code'}, 'info': {'zh': 'The dataset(s) to train the models, support multi select and local folder/files', 'en': 'The dataset(s) to train the models, support multi select and local folder/files'}}, 'max_length': {'label': {'zh': 'The max length', 'en': 'The max length'}, 'info': {'zh': 'Set the max length input to the model', 'en': 'Set the max length input to the model'}}, 'split_dataset_ratio': {'label': {'zh': 'Split ratio of eval dataset', 'en': 'Split ratio of eval dataset'}, 'info': {'zh': 'Split the datasets by this ratio for eval', 'en': 'Split the datasets by this ratio for eval'}}, 'padding_free': {'label': {'zh': 'Padding-free batching', 'en': 'Padding-free batching'}, 'info': {'zh': 'Flatten the data in a batch to avoid data padding', 'en': 'Flatten the data in a batch to avoid data padding'}}, 'dataset_param': {'label': {'zh': 'Dataset settings', 'en': 'Dataset settings'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Accordion(elem_id='dataset_param', open=True):
            with gr.Row():
                gr.Dropdown(elem_id='dataset', multiselect=True, choices=get_dataset_list(), scale=20, allow_custom_value=True)
                gr.Slider(elem_id='split_dataset_ratio', minimum=0.0, maximum=1.0, step=0.05, scale=10)
                gr.Slider(elem_id='max_length', minimum=32, maximum=32768, value=1024, step=1, scale=10)
                gr.Checkbox(elem_id='padding_free', scale=10)
