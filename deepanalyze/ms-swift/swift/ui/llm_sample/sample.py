from typing import Type
import gradio as gr
from swift.ui.base import BaseUI

class Sample(BaseUI):
    group = 'llm_sample'
    locale_dict = {'sampler_type': {'label': {'zh': 'Sampler type', 'en': 'Sampler type'}}, 'sampler_engine': {'label': {'zh': 'Infer engine', 'en': 'Infer engine'}}, 'num_return_sequences': {'label': {'zh': 'Num of original sequences returned by sampling', 'en': 'Num of original sequences returned by sampling'}}, 'n_best_to_keep': {'label': {'zh': 'Num of best sequences', 'en': 'Num of best sequences'}}, 'max_new_tokens': {'label': {'zh': 'Max new tokens', 'en': 'Max new tokens'}}, 'temperature': {'label': {'zh': 'Temperature', 'en': 'Temperature'}}, 'top_k': {'label': {'zh': 'Top-k', 'en': 'Top-k'}}, 'top_p': {'label': {'zh': 'Top-p', 'en': 'Top-p'}}, 'repetition_penalty': {'label': {'zh': 'Repetition Penalty', 'en': 'Repetition Penalty'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Row():
            gr.Dropdown(elem_id='sampler_type', choices=['sample', 'mcts', 'distill'], value='sample', scale=5)
            gr.Dropdown(elem_id='sampler_engine', choices=['pt', 'lmdeploy', 'vllm', 'no', 'client'], value='pt', scale=5)
            gr.Slider(elem_id='num_return_sequences', minimum=1, maximum=128, step=1, value=64, scale=5)
            gr.Slider(elem_id='n_best_to_keep', minimum=1, maximum=64, step=1, value=5, scale=5)
        with gr.Row():
            gr.Textbox(elem_id='max_new_tokens', lines=1, value='2048')
            gr.Slider(elem_id='temperature', minimum=0.0, maximum=10, step=0.1, value=1.0)
            gr.Slider(elem_id='top_k', minimum=1, maximum=100, step=5, value=20)
            gr.Slider(elem_id='top_p', minimum=0.0, maximum=1.0, step=0.05, value=0.7)
            gr.Slider(elem_id='repetition_penalty', minimum=0.0, maximum=10, step=0.05, value=1.05)
