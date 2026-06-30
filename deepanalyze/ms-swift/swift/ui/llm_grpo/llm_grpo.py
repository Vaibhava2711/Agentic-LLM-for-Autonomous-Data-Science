from functools import partial
from typing import Dict, Type
import gradio as gr
from packaging import version
from swift.llm.argument.base_args.base_args import get_supported_tuners
from swift.ui.base import BaseUI
from swift.ui.llm_grpo.advanced import GRPOAdvanced
from swift.ui.llm_grpo.dataset import GRPODataset
from swift.ui.llm_grpo.external_rollout import LLMRollout
from swift.ui.llm_grpo.grpo_advanced import GrpoAdvanced
from swift.ui.llm_grpo.hyper import GRPOHyper
from swift.ui.llm_grpo.model import GRPOModel
from swift.ui.llm_grpo.optimizer import GRPOOptimizer
from swift.ui.llm_grpo.quantization import GRPOQuantization
from swift.ui.llm_grpo.report_to import GRPOReportTo
from swift.ui.llm_grpo.reward import Reward
from swift.ui.llm_grpo.rollout import Rollout
from swift.ui.llm_grpo.runtime import GRPORuntime
from swift.ui.llm_grpo.save import GRPOSave
from swift.ui.llm_grpo.tuner import GRPOTuner
from swift.ui.llm_train.llm_train import LLMTrain
from swift.ui.llm_train.runtime import Runtime
from swift.utils import get_device_count, get_logger
logger = get_logger()

class LLMGRPO(LLMTrain):
    group = 'llm_grpo'
    sub_ui = [GRPOModel, GRPODataset, Reward, GRPORuntime, Rollout, GRPOSave, GRPOTuner, GRPOOptimizer, GRPOHyper, GRPOQuantization, GRPOAdvanced, GrpoAdvanced, GRPOReportTo, LLMRollout]
    locale_dict: Dict[str, Dict] = {'llm_grpo': {'label': {'zh': 'LLM GRPO', 'en': 'LLM GRPO'}}, 'external_alert': {'value': {'zh': 'Err: {} \nRollout model deployment is incomplete, please check the logs and start training later!', 'en': 'Err: {} \nRollout model deployment is incomplete, please check the logs and start training later!'}}, 'submit_alert': {'value': {'zh': 'Task started, please check the tensorboard or log file, closing this page does not affect training', 'en': 'Task started, please check the tensorboard or log file, closing this page does not affect training'}}, 'dataset_alert': {'value': {'zh': 'Please input or select a dataset', 'en': 'Please input or select a dataset'}}, 'submit': {'value': {'zh': '🚀 Begin', 'en': '🚀 Begin'}}, 'dry_run': {'label': {'zh': 'Dry-run', 'en': 'Dry-run'}, 'info': {'zh': 'Generate run command only, for manually running', 'en': 'Generate run command only, for manually running'}}, 'gpu_id': {'label': {'zh': 'Choose GPU', 'en': 'Choose GPU'}, 'info': {'zh': 'Select GPU to train', 'en': 'Select GPU to train'}}, 'train_type': {'label': {'zh': 'Train type', 'en': 'Train type'}, 'info': {'zh': 'Select the training type', 'en': 'Select the training type'}}, 'seed': {'label': {'zh': 'Seed', 'en': 'Seed'}, 'info': {'zh': 'Select a random seed', 'en': 'Select a random seed'}}, 'torch_dtype': {'label': {'zh': 'Training Precision', 'en': 'Training Precision'}, 'info': {'zh': 'Select the training precision', 'en': 'Select the training precision'}}, 'envs': {'label': {'zh': 'Extra env vars', 'en': 'Extra env vars'}}, 'use_ddp': {'label': {'zh': 'Use DDP', 'en': 'Use DDP'}, 'info': {'zh': 'Use Distributed Data Parallel to train', 'en': 'Use Distributed Data Parallel to train'}}, 'ddp_num': {'label': {'zh': 'Number of DDP sharding', 'en': 'Number of DDP sharding'}, 'info': {'zh': 'The data parallel size of DDP', 'en': 'The data parallel size of DDP'}}, 'use_liger_kernel': {'label': {'zh': 'Use Liger kernel', 'en': 'Use Liger kernel'}, 'info': {'zh': 'Liger kernel can reduce memory usage', 'en': 'Liger kernel can reduce memory usage'}}, 'sequence_parallel_size': {'label': {'zh': 'Sequence parallel size', 'en': 'Sequence parallel size'}, 'info': {'zh': 'Currently supports CPT/SFT/DPO/GRPO', 'en': 'Currently supports CPT/SFT/DPO/GRPO'}}, 'deepspeed': {'label': {'zh': 'DeepSpeed', 'en': 'DeepSpeed'}, 'info': {'zh': 'Choose from the dropbox or fill in a valid path', 'en': 'Choose from the dropbox or fill in a valid path'}}, 'resume_checkpoint_alert': {'value': {'zh': 'Detected that "args.json" is in {}, will start breakpoint resume training from this checkpoint', 'en': 'Detected that "args.json" is in {}, will start breakpoint resume training from this checkpoint'}}, 'resume_only_model_alert': {'value': {'zh': '"args.json" is detected in {}, but optimizer parameters are not detected. Only model parameters will be loaded to start breakpoint continuation training', 'en': '"args.json" is detected in {}, but optimizer parameters are not detected. Only model parameters will be loaded to start breakpoint continuation training'}}, 'more_params': {'label': {'zh': 'Other params', 'en': 'Other params'}, 'info': {'zh': 'Fill in with json format or --xxx xxx cmd format', 'en': 'Fill in with json format or --xxx xxx cmd format'}}, 'extra_params': {'label': {'zh': 'Extra settings', 'en': 'Extra settings'}}, 'train_param': {'label': {'zh': 'Train settings', 'en': 'Train settings'}}}

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.TabItem(elem_id='llm_grpo', label=''):
            default_device = 'cpu'
            device_count = get_device_count()
            if device_count > 0:
                default_device = '0'
            with gr.Blocks():
                GRPOModel.build_ui(base_tab)
                GRPODataset.build_ui(base_tab)
                Reward.build_ui(base_tab)
                with gr.Accordion(elem_id='train_param', open=True):
                    with gr.Row():
                        gr.Dropdown(elem_id='train_type', scale=4, choices=list(get_supported_tuners()))
                        gr.Textbox(elem_id='seed', scale=4)
                        gr.Dropdown(elem_id='torch_dtype', scale=4)
                        gr.Checkbox(elem_id='use_liger_kernel', scale=4)
                        gr.Textbox(elem_id='sequence_parallel_size', lines=1, scale=4)
                    with gr.Row():
                        gr.Dropdown(elem_id='gpu_id', multiselect=True, choices=[str(i) for i in range(device_count)] + ['cpu'], value=default_device, scale=8)
                        gr.Checkbox(elem_id='use_ddp', value=False, scale=4)
                        gr.Textbox(elem_id='ddp_num', value='1', scale=4)
                        gr.Dropdown(elem_id='deepspeed', scale=4, allow_custom_value=True, value=None, choices=['zero0', 'zero1', 'zero2', 'zero3', 'zero2_offload', 'zero3_offload'])
                GRPOHyper.build_ui(base_tab)
                GRPORuntime.build_ui(base_tab)
                with gr.Row(equal_height=True):
                    gr.Textbox(elem_id='envs', scale=12)
                    gr.Checkbox(elem_id='dry_run', value=False, scale=4)
                    submit = gr.Button(elem_id='submit', scale=4, variant='primary')
                Rollout.build_ui(base_tab)
                LLMRollout.set_lang(cls.lang)
                LLMRollout.build_ui(LLMRollout)
                GRPOTuner.build_ui(base_tab)
                with gr.Accordion(elem_id='extra_params', open=False):
                    with gr.Tabs():
                        GrpoAdvanced.build_ui(base_tab)
                        GRPOAdvanced.build_ui(base_tab)
                        GRPOQuantization.build_ui(base_tab)
                        GRPOSave.build_ui(base_tab)
                        GRPOReportTo.build_ui(base_tab)
                    with gr.Row():
                        gr.Textbox(elem_id='more_params', lines=4, scale=20)
                cls.element('train_type').change(GRPOHyper.update_lr, inputs=[base_tab.element('train_type')], outputs=[cls.element('learning_rate')])
                submit.click(cls.train_local, list(cls.valid_elements().values()), [cls.element('running_cmd'), cls.element('logging_dir'), cls.element('runtime_tab'), cls.element('running_tasks'), cls.element('train_record')], queue=True)
                Rollout.element('vllm_mode').change(LLMRollout.external_rollout_display, Rollout.element('vllm_mode'), LLMRollout.element('llm_rollout'))
                LLMRollout.element('rollout').click(LLMRollout.rollout_model, list(LLMRollout.valid_elements().values()) + [cls.element('model'), cls.element('model_type'), cls.element('template')], [LLMRollout.element('rollout_runtime_tab'), LLMRollout.element('rollout_running_tasks')])
                GRPORuntime.element('kill_task').click(GRPORuntime.kill_task, [GRPORuntime.element('running_tasks')], [GRPORuntime.element('running_tasks')] + [GRPORuntime.element('log')] + GRPORuntime.all_plots).then(GRPORuntime.reset, [], [GRPORuntime.element('logging_dir')] + [GRPOHyper.element('output_dir')])
                base_tab.element('gpu_id').change(cls.update_ddp_num, [base_tab.element('gpu_id'), base_tab.element('use_ddp')], base_tab.element('ddp_num'))
                base_tab.element('use_ddp').change(cls.update_ddp_num, [base_tab.element('gpu_id'), base_tab.element('use_ddp')], base_tab.element('ddp_num'))
                base_tab.element('ddp_num').change(Rollout.update_num_gen, [GRPOHyper.element('per_device_train_batch_size'), GRPOHyper.element('gradient_accumulation_steps'), cls.element('ddp_num')], [Rollout.element('num_generations')])
                GRPOHyper.element('gradient_accumulation_steps').change(Rollout.update_num_gen, [GRPOHyper.element('per_device_train_batch_size'), GRPOHyper.element('gradient_accumulation_steps'), cls.element('ddp_num')], [Rollout.element('num_generations')])
                GRPOHyper.element('per_device_train_batch_size').change(Rollout.update_num_gen, [GRPOHyper.element('per_device_train_batch_size'), GRPOHyper.element('gradient_accumulation_steps'), cls.element('ddp_num')], [Rollout.element('num_generations')])

    @classmethod
    def prepare_sub_to_filter(cls):
        tabs_relation_dict = {key: val for (key, val) in zip(['train_type', 'optimizer', 'vllm_mode'], [GRPOTuner.tabs_to_filter, GRPOOptimizer.tabs_to_filter, Rollout.tabs_to_filter])}
        return tabs_relation_dict
