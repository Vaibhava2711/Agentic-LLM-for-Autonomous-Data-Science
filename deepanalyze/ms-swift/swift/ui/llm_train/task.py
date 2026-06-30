from typing import Type
import gradio as gr
from swift.ui.base import BaseUI

class Task(BaseUI):
    group = 'llm_train'
    locale_dict = {'embed_tab': {'label': {'zh': 'Embedding', 'en': 'Embedding'}}, 'loss_type': {'label': {'zh': 'Loss type', 'en': 'Loss type'}}, 'seq_cls_tab': {'label': {'zh': 'Sequence Classification', 'en': 'Sequence Classification'}}, 'num_labels': {'label': {'zh': 'Number of labels', 'en': 'Number of labels'}}, 'use_chat_template': {'label': {'zh': 'use chat template', 'en': 'use chat template'}, 'info': {'zh': 'Use the chat template or generation template', 'en': 'Use the chat template or generation template'}}, 'task_type': {'label': {'zh': 'Task type', 'en': 'Task type'}}, 'task_params': {'label': {'zh': 'Task params', 'en': 'Task params'}}}
    tabs_to_filter = {'embedding': ['loss_type'], 'seq_cls': ['num_labels', 'use_chat_template']}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Accordion(elem_id='task_params', open=False):
            gr.Dropdown(elem_id='task_type', choices=['causal_lm', 'seq_cls', 'embedding'])
            with gr.Tabs():
                with gr.TabItem(elem_id='embed_tab'):
                    with gr.Row():
                        gr.Dropdown(elem_id='loss_type', choices=['cosine_similarity', 'contrastive', 'online_contrastive', 'infonce'])
                with gr.TabItem(elem_id='seq_cls_tab'):
                    with gr.Row():
                        gr.Textbox(elem_id='num_labels', scale=4)
                        gr.Checkbox(elem_id='use_chat_template', value=True, scale=4)
