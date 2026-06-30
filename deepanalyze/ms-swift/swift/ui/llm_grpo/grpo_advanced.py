from functools import partial
from typing import Type
import gradio as gr
from swift.llm import BaseArguments, ModelType
from swift.llm.model.register import get_all_models
from swift.ui.base import BaseUI

class GrpoAdvanced(BaseUI):
    group = 'llm_grpo'
    locale_dict = {'grpo_advanced_tab': {'label': {'zh': 'GRPO advanced settings', 'en': 'GRPO advanced settings'}}, 'loss_type': {'label': {'zh': 'Loss normalization type', 'en': 'Loss normalization type'}}, 'epsilon': {'label': {'zh': 'Clip coefficient', 'en': 'Clip coefficient'}}, 'epsilon_high': {'label': {'zh': 'Upper clip coefficient', 'en': 'Upper clip coefficient'}}, 'move_model_batches': {'label': {'zh': 'Batches of model params moving', 'en': 'Batches of model params moving'}, 'info': {'zh': 'How many batches to divide the model into when moving parameters to an inference framework such as vLLM', 'en': 'How many batches to divide the model into when moving parameters to an inference framework such as vLLM'}}, 'multi_turn_scheduler': {'label': {'zh': 'Multi turn Scheduler', 'en': 'Multi turn Scheduler'}, 'info': {'zh': 'Multi turn of GRPO parameters, pass in the corresponding plugin name', 'en': 'Multi turn of GRPO parameters, pass in the corresponding plugin name'}}, 'max_turns': {'label': {'zh': 'Max num of multi turn', 'en': 'Max num of multi turn'}}, 'dynamic_sample': {'label': {'zh': 'Dynamic sampling', 'en': 'Dynamic sampling'}, 'info': {'zh': 'Filter out data with a reward standard deviation of 0 within the group and sample new data', 'en': 'Filter out data with a reward standard deviation of 0 within the group and sample new data'}}, 'max_resample_times': {'label': {'zh': 'Max num of resampling times', 'en': 'Max num of resampling times'}, 'info': {'zh': 'Limit the number of resampling times when dynamic_sample is set', 'en': 'Limit the number of resampling times when dynamic_sample is set'}}, 'overlong_filter': {'label': {'zh': 'Skip overlong samples', 'en': 'Skip overlong samples'}, 'info': {'zh': 'Skip overlong truncated samples and exclude them from loss calculation', 'en': 'Skip overlong truncated samples and exclude them from loss calculation'}}, 'beta': {'label': {'zh': 'KL regularization coefficient', 'en': 'KL regularization coefficient'}}, 'vllm_enable_prefix_caching': {'label': {'zh': 'Enable prefix cache', 'en': 'Enable prefix cache'}, 'info': {'zh': 'vLLM transparent transmission parameters in colocate mode', 'en': 'vLLM transparent transmission parameters in colocate mode'}}, 'log_completions': {'label': {'zh': 'Record generated content', 'en': 'Record generated content'}, 'info': {'zh': 'Whether to record the model generation content during training', 'en': 'Whether to record the model generation content during training'}}, 'num_iterations': {'label': {'zh': 'Num of updates per batch', 'en': 'Num of updates per batch'}}, 'reward_model': {'label': {'zh': 'Reward Model id or path', 'en': 'Reward Model id or path'}, 'info': {'zh': 'The actual model id or model path', 'en': 'The actual model id or model path'}}, 'reward_model_type': {'label': {'zh': 'Select Reward Model Type', 'en': 'Select Reward Model Type'}, 'info': {'zh': 'Base model type supported by SWIFT', 'en': 'Base model type supported by SWIFT'}}, 'reward_model_plugin': {'label': {'zh': 'Reward model logic', 'en': 'Reward model logic'}, 'info': {'zh': 'Use reward_model_plugin to customize the processing logic of the reward model', 'en': 'Use reward_model_plugin to customize the processing logic of the reward model'}}, 'external_plugins': {'label': {'zh': 'External plugin file', 'en': 'External plugin file'}, 'info': {'zh': 'List of external plugin files that will be registered into the plugin module', 'en': 'List of external plugin files that will be registered into the plugin module'}}, 'ref_model_type': {'label': {'zh': 'Ref model type', 'en': 'Ref model type'}, 'info': {'zh': 'Model type supported by SWIFT', 'en': 'Model type supported by SWIFT'}}, 'ref_model': {'label': {'zh': 'Ref model id or path', 'en': 'Ref model id or path'}, 'info': {'zh': 'The actual model id or path', 'en': 'The actual model id or path'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.TabItem(elem_id='grpo_advanced_tab'):
            with gr.Blocks():
                with gr.Row():
                    gr.Dropdown(elem_id='loss_type', choices=['grpo', 'bnpo', 'dr_grpo'], value='grpo', scale=4)
                    gr.Textbox(elem_id='epsilon', value=0.2, lines=1, scale=4)
                    gr.Textbox(elem_id='epsilon_high', value=None, lines=1, scale=4)
                    gr.Textbox(elem_id='beta', value=0.04, lines=1, scale=4)
                    gr.Textbox(elem_id='num_iterations', lines=1, scale=4)
                with gr.Row():
                    gr.Textbox(elem_id='move_model_batches', lines=1, scale=4)
                    gr.Checkbox(elem_id='dynamic_sample', scale=4)
                    gr.Slider(elem_id='max_resample_times', minimum=1, maximum=16, step=1, value=3, scale=4)
                    gr.Checkbox(elem_id='overlong_filter', scale=4)
                    gr.Checkbox(elem_id='vllm_enable_prefix_caching', scale=4)
                with gr.Row():
                    gr.Checkbox(elem_id='log_completions', scale=4)
                    gr.Textbox(elem_id='multi_turn_scheduler', lines=1, scale=4)
                    gr.Textbox(elem_id='max_turns', lines=1, scale=4)
                    gr.Textbox(elem_id='external_plugins', lines=1, scale=8)
            with gr.Row():
                gr.Textbox(elem_id='reward_model_plugin', lines=1, scale=8)
                gr.Dropdown(elem_id='reward_model', multiselect=True, choices=get_all_models(), scale=8)
                gr.Dropdown(elem_id='reward_model_type', multiselect=True, choices=ModelType.get_model_name_list(), allow_custom_value=True, scale=4)
            with gr.Blocks():
                with gr.Row():
                    gr.Dropdown(elem_id='ref_model', scale=12, value=None, choices=get_all_models(), allow_custom_value=True)
                    gr.Dropdown(elem_id='ref_model_type', choices=ModelType.get_model_name_list(), value=None, scale=8)

    @classmethod
    def after_build_ui(cls, base_tab: Type['BaseUI']):
        cls.element('ref_model').change(partial(cls.update_input_model, allow_keys=['ref_model_type'], has_record=False, is_ref_model=True), inputs=[cls.element('ref_model')], outputs=[cls.element('ref_model_type')])
        cls.element('reward_model').change(partial(cls.update_input_models, allow_keys=['reward_model_type'], is_reward_model=True, has_record=False), inputs=[cls.element('reward_model')], outputs=[cls.element('reward_model_type')])

    @classmethod
    def update_input_models(cls, models, allow_keys=None, has_record=False, arg_cls=BaseArguments, is_reward_model=False):
        if models is None:
            return gr.update()
        rm_type_str = ''
        for model in models:
            rm_type_str = ' '.join([rm_type_str, cls.update_input_model(model, allow_keys=allow_keys, has_record=has_record, arg_cls=arg_cls, is_reward_model=is_reward_model)['value']])
        return gr.update(value=rm_type_str.strip())
