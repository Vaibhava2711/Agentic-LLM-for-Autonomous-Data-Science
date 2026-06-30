from functools import partial
from typing import Type
import gradio as gr
from swift.llm import BaseArguments, ModelType
from swift.llm.model.register import get_all_models
from swift.ui.base import BaseUI

class Reward(BaseUI):
    group = 'llm_grpo'
    locale_dict = {'reward_funcs': {'label': {'zh': 'Reward functions', 'en': 'Reward functions'}, 'info': {'zh': 'GRPO algorithm reward function', 'en': 'GRPO algorithm reward function'}}, 'reward_weights': {'label': {'zh': 'The weight of each reward function', 'en': 'The weight of each reward function'}, 'info': {'zh': 'The weights of each reward function are separated by spaces', 'en': 'The weights of each reward function are separated by spaces'}}, 'reward_param': {'label': {'zh': 'Reward settings(more params->GRPO advanced settings)', 'en': 'Reward settings(more params->GRPO advanced settings)'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Accordion(elem_id='reward_param', open=True):
            with gr.Row():
                gr.Dropdown(elem_id='reward_funcs', multiselect=True, choices=['accuracy', 'format', 'cosine', 'repetition', 'soft_overlong'], scale=2, allow_custom_value=True)
                gr.Textbox(elem_id='reward_weights', lines=1, scale=2)
