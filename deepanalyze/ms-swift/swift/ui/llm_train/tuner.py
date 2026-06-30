from typing import Type
import gradio as gr
from swift.ui.base import BaseUI
from swift.ui.llm_train.lora import LoRA
from swift.ui.llm_train.target import Target

class Tuner(BaseUI):
    group = 'llm_train'
    sub_ui = [LoRA, Target]
    locale_dict = {'adalora_tab': {'label': {'zh': 'AdaLoRA settings', 'en': 'AdaLoRA settings'}}, 'adalora_target_r': {'label': {'zh': 'Average rank of AdaLoRA', 'en': 'Average rank of AdaLoRA'}}, 'adalora_init_r': {'label': {'zh': 'Initial rank of AdaLoRA', 'en': 'Initial rank of AdaLoRA'}}, 'adalora_tinit': {'label': {'zh': 'Initial fine-tuning warmup steps of AdaLoRA', 'en': 'Initial fine-tuning warmup steps of AdaLoRA'}}, 'adalora_tfinal': {'label': {'zh': 'Final fine-tuning steps of AdaLoRA', 'en': 'Final fine-tuning steps of AdaLoRA'}}, 'adalora_deltaT': {'label': {'zh': 'Internval of AdaLoRA two budget allocations', 'en': 'Internval of AdaLoRA two budget allocations'}}, 'adalora_beta1': {'label': {'zh': 'AdaLoRA EMA parameters', 'en': 'AdaLoRA EMA parameters'}}, 'adalora_beta2': {'label': {'zh': 'AdaLoRA EMA parameters', 'en': 'AdaLoRA EMA parameters'}}, 'adalora_orth_reg_weight': {'label': {'zh': 'Coefficient of AdaLoRA orthogonal regularization', 'en': 'Coefficient of AdaLoRA orthogonal regularization'}}, 'lora_ga_tab': {'label': {'zh': 'LoRA-GA settings', 'en': 'LoRA-GA settings'}}, 'lora_ga_batch_size': {'label': {'zh': 'LoRA-GA initialization batch size', 'en': 'LoRA-GA initialization batch size'}}, 'lora_ga_iters': {'label': {'zh': 'LoRA-GA initialization iters', 'en': 'LoRA-GA initialization iters'}}, 'lora_ga_max_length': {'label': {'zh': 'LoRA-GA initialization max length', 'en': 'LoRA-GA initialization max length'}}, 'lora_ga_direction': {'label': {'zh': 'LoRA-GA initialization direction', 'en': 'LoRA-GA initialization direction'}}, 'lora_ga_scale': {'label': {'zh': 'LoRA-GA initialization scaling method', 'en': 'LoRA-GA initialization scaling method'}}, 'lora_ga_stable_gamma': {'label': {'zh': 'Gamma value', 'en': 'Gamma value'}, 'info': {'zh': 'Select the gamma value for stable scaling', 'en': 'Select the gamma value for stable scaling'}}, 'longlora': {'label': {'zh': 'LongLoRA settings', 'en': 'LongLoRA settings'}}, 'reft_tab': {'label': {'zh': 'ReFT settings', 'en': 'ReFT settings'}}, 'reft_layers': {'label': {'zh': 'ReFT layers', 'en': 'ReFT layers'}}, 'reft_rank': {'label': {'zh': 'Rank of the ReFT matrix', 'en': 'Rank of the ReFT matrix'}}, 'reft_intervention_type': {'label': {'zh': 'ReFT intervention type', 'en': 'ReFT intervention type'}}, 'vera_tab': {'label': {'zh': 'VeRA settings', 'en': 'VeRA settings'}}, 'vera_rank': {'label': {'zh': 'VeRA rank', 'en': 'VeRA rank'}}, 'vera_projection_prng_key': {'label': {'zh': 'VeRA PRNG initialisation key', 'en': 'VeRA PRNG initialisation key'}}, 'vera_dropout': {'label': {'zh': 'VeRA dropout', 'en': 'VeRA dropout'}}, 'vera_d_initial': {'label': {'zh': 'Initial value of d matrix', 'en': 'Initial value of d matrix'}}, 'boft_tab': {'label': {'zh': 'BOFT settings', 'en': 'BOFT settings'}}, 'boft_block_size': {'label': {'zh': 'BOFT block size', 'en': 'BOFT block size'}}, 'boft_block_num': {'label': {'zh': 'Number of BOFT blocks', 'en': 'Number of BOFT blocks'}, 'info': {'zh': 'Cannot be used with boft_block_size', 'en': 'Cannot be used with boft_block_size'}}, 'boft_dropout': {'label': {'zh': 'Dropout value of BOFT', 'en': 'Dropout value of BOFT'}}, 'fourierft_tab': {'label': {'zh': 'FourierFT settings', 'en': 'FourierFT settings'}}, 'fourier_n_frequency': {'label': {'zh': 'Num of FourierFT frequencies', 'en': 'Num of FourierFT frequencies'}}, 'fourier_scaling': {'label': {'zh': 'W matrix scaling value', 'en': 'W matrix scaling value'}}, 'llamapro_tab': {'label': {'zh': 'LLaMA Pro Settings', 'en': 'LLaMA Pro Settings'}}, 'llamapro_num_new_blocks': {'label': {'zh': 'LLaMA Pro new layers', 'en': 'LLaMA Pro new layers'}}, 'llamapro_num_groups': {'label': {'zh': 'LLaMA Pro groups of model', 'en': 'LLaMA Pro groups of model'}}, 'lisa_tab': {'label': {'zh': 'LISA settings', 'en': 'LISA settings'}}, 'lisa_activated_layers': {'label': {'zh': 'Num of LISA activated layers', 'en': 'Num of LISA activated layers'}, 'info': {'zh': 'Num of layers activated each time, a positive value means using LISA', 'en': 'Num of layers activated each time, a positive value means using LISA'}}, 'lisa_step_interval': {'label': {'zh': 'The interval of LISA layers switching', 'en': 'The interval of LISA layers switching'}}, 'tuner_params': {'label': {'zh': 'Tuner params', 'en': 'Tuner params'}}}
    tabs_to_filter = {'lora': ['lora_rank', 'lora_alpha', 'lora_dropout', 'lora_dtype', 'use_rslora', 'use_dora'], 'llamapro': ['llamapro_num_new_blocks', 'llamapro_num_groups'], 'lisa': ['lisa_activated_layers', 'lisa_step_interval'], 'adalora': ['adalora_target_r', 'adalora_init_r', 'adalora_tinit', 'adalora_tfinal', 'adalora_deltaT', 'adalora_beta1', 'adalora_beta2', 'adalora_orth_reg_weight'], 'lora_ga': ['lora_ga_batch_size', 'lora_ga_iters', 'lora_ga_max_length', 'lora_ga_direction', 'lora_ga_scale', 'lora_ga_stable_gamma'], 'reft': ['reft_layers', 'reft_rank', 'reft_intervention_type'], 'vera': ['vera_rank', 'vera_projection_prng_key', 'vera_dropout', 'vera_d_initial'], 'boft': ['boft_block_size', 'boft_block_num', 'boft_dropout'], 'fourierft': ['fourier_n_frequency', 'fourier_scaling']}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Accordion(elem_id='tuner_params', open=False):
            with gr.Tabs():
                LoRA.set_lang(cls.lang)
                LoRA.build_ui(base_tab)
                with gr.TabItem(elem_id='llamapro_tab'):
                    with gr.Blocks():
                        with gr.Row():
                            gr.Textbox(elem_id='llamapro_num_new_blocks', scale=2)
                            gr.Textbox(elem_id='llamapro_num_groups', scale=2)
                with gr.TabItem(elem_id='lisa_tab'):
                    with gr.Blocks():
                        with gr.Row():
                            gr.Textbox(elem_id='lisa_activated_layers', value='0', scale=2)
                            gr.Textbox(elem_id='lisa_step_interval', value='20', scale=2)
                with gr.TabItem(elem_id='adalora_tab'):
                    with gr.Blocks():
                        with gr.Row():
                            gr.Textbox(elem_id='adalora_target_r', value='8', scale=2)
                            gr.Slider(elem_id='adalora_init_r', value=12, minimum=1, maximum=512, step=4, scale=2)
                            gr.Textbox(elem_id='adalora_tinit', value='0', scale=2)
                            gr.Textbox(elem_id='adalora_tfinal', value='0', scale=2)
                        with gr.Row():
                            gr.Textbox(elem_id='adalora_deltaT', value='1', scale=2)
                            gr.Textbox(elem_id='adalora_beta1', value='0.85', scale=2)
                            gr.Textbox(elem_id='adalora_beta2', value='0.85', scale=2)
                            gr.Textbox(elem_id='adalora_orth_reg_weight', value='0.5', scale=2)
                with gr.TabItem(elem_id='lora_ga_tab'):
                    with gr.Blocks():
                        with gr.Row():
                            gr.Slider(elem_id='lora_ga_batch_size', value=2, minimum=1, maximum=256, step=1, scale=20)
                            gr.Textbox(elem_id='lora_ga_iters', value='2', scale=20)
                            gr.Textbox(elem_id='lora_ga_max_length', value='2048', scale=20)
                            gr.Dropdown(elem_id='lora_ga_direction', scale=20, value='ArB2r', choices=['ArBr', 'A2rBr', 'ArB2r', 'random'])
                            gr.Dropdown(elem_id='lora_ga_scale', scale=20, value='stable', choices=['gd', 'unit', 'stable', 'weights'])
                            gr.Textbox(elem_id='lora_ga_stable_gamma', value='16', scale=20)
                with gr.TabItem(elem_id='reft_tab'):
                    with gr.Blocks():
                        with gr.Row():
                            gr.Textbox(elem_id='reft_layers', scale=2)
                            gr.Slider(elem_id='reft_rank', value=4, minimum=1, maximum=512, step=4, scale=2)
                            gr.Dropdown(elem_id='reft_intervention_type', scale=2, value='LoreftIntervention', choices=['NoreftIntervention', 'LoreftIntervention', 'ConsreftIntervention', 'LobireftIntervention', 'DireftIntervention', 'NodireftIntervention'])
                with gr.TabItem(elem_id='vera_tab'):
                    with gr.Blocks():
                        with gr.Row():
                            gr.Slider(elem_id='vera_rank', value=256, minimum=1, maximum=512, step=4, scale=2)
                            gr.Textbox(elem_id='vera_projection_prng_key', value='0', scale=2)
                            gr.Textbox(elem_id='vera_dropout', value='0.0', scale=2)
                            gr.Textbox(elem_id='vera_d_initial', value='0.1', scale=2)
                with gr.TabItem(elem_id='boft_tab'):
                    with gr.Blocks():
                        with gr.Row():
                            gr.Textbox(elem_id='boft_block_size', value='4', scale=2)
                            gr.Textbox(elem_id='boft_block_num', scale=2)
                            gr.Textbox(elem_id='boft_dropout', value='0.0', scale=2)
                with gr.TabItem(elem_id='fourierft_tab'):
                    with gr.Blocks():
                        with gr.Row():
                            gr.Textbox(elem_id='fourier_n_frequency', value='2000', scale=2)
                            gr.Textbox(elem_id='fourier_scaling', value='300.0', scale=2)
            Target.set_lang(cls.lang)
            Target.build_ui(base_tab)
