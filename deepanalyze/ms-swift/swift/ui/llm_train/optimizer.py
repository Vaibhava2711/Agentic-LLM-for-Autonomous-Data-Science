from typing import Type
import gradio as gr
from swift.ui.base import BaseUI

class Optimizer(BaseUI):
    group = 'llm_train'
    locale_dict = {'galore_tab': {'label': {'zh': 'GaLore Settings', 'en': 'GaLore Settings'}}, 'use_galore': {'label': {'zh': 'Use GaLore', 'en': 'Use GaLore'}, 'info': {'zh': 'Use GaLore to reduce GPU memory usage in full parameter training', 'en': 'Use GaLore to reduce GPU memory usage in full parameter training'}}, 'galore_rank': {'label': {'zh': 'The rank of GaLore', 'en': 'The rank of GaLore'}}, 'galore_update_proj_gap': {'label': {'zh': 'Projection matrix update interval', 'en': 'Projection matrix update interval'}, 'info': {'zh': 'Update interval of GaLore decomposition matrix', 'en': 'Update interval of GaLore decomposition matrix'}}, 'galore_with_embedding': {'label': {'zh': 'Use GaLore with embedding', 'en': 'Use GaLore with embedding'}, 'info': {'zh': 'Whether to apply GaLore to embedding', 'en': 'Whether to apply GaLore to embedding'}}, 'lorap_tab': {'label': {'zh': 'LoRA+ settings', 'en': 'LoRA+ settings'}}, 'lorap_lr_ratio': {'label': {'zh': 'LoRA+ lr ratio', 'en': 'LoRA+ lr ratio'}, 'info': {'zh': 'When using LoRA, specify this parameter to use LoRA+, and the recommended value is 10 to 16', 'en': 'When using LoRA, specify this parameter to use LoRA+, and the recommended value is 10 to 16'}}, 'muon_tab': {'label': {'zh': 'Muon Settings', 'en': 'Muon Settings'}}, 'use_muon': {'label': {'zh': 'Use Muon', 'en': 'Use Muon'}, 'info': {'zh': 'Using the Muon optimizer, set `--optimizer muon` in the command line', 'en': 'Using the Muon optimizer, set `--optimizer muon` in the command line'}}, 'multimodal_tab': {'label': {'zh': 'Multimodal Settings', 'en': 'Multimodal Settings'}}, 'vit_lr': {'label': {'zh': 'Learning rate of ViT', 'en': 'Learning rate of ViT'}}, 'aligner_lr': {'label': {'zh': 'Learning rate of aligner', 'en': 'Learning rate of aligner'}}, 'optimizer_params': {'label': {'zh': 'Optimizer params', 'en': 'Optimizer params'}}}
    tabs_to_filter = {'galore': ['use_galore', 'galore_with_embedding', 'galore_rank', 'galore_update_proj_gap'], 'lorap': ['lorap_lr_ratio'], 'multimodal': ['vit_lr', 'aligner_lr'], 'muon': ['use_muon']}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Accordion(elem_id='optimizer_params', open=False):
            with gr.Tabs():
                with gr.TabItem(elem_id='galore_tab'):
                    with gr.Row():
                        gr.Checkbox(elem_id='use_galore', scale=4)
                        gr.Checkbox(elem_id='galore_with_embedding', scale=4)
                        gr.Slider(elem_id='galore_rank', minimum=8, maximum=256, step=8, scale=4)
                        gr.Slider(elem_id='galore_update_proj_gap', minimum=10, maximum=1000, step=50, scale=4)
                with gr.TabItem(elem_id='lorap_tab'):
                    with gr.Row():
                        gr.Textbox(elem_id='lorap_lr_ratio', scale=4)
                with gr.TabItem(elem_id='multimodal_tab'):
                    with gr.Row():
                        gr.Textbox(elem_id='vit_lr', lines=1, scale=20)
                        gr.Textbox(elem_id='aligner_lr', lines=1, scale=20)
                with gr.TabItem(elem_id='muon_tab'):
                    with gr.Row():
                        gr.Checkbox(elem_id='use_muon', scale=4)
