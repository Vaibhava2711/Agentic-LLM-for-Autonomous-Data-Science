import os

import torch

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
os.environ["SWIFT_DEBUG"] = "1"


def _infer_model(pt_engine, system=None, messages=None, images=None, **kwargs):
    seed_everything(42)
    request_config = RequestConfig(max_tokens=128, temperature=0, repetition_penalty=1)
    if messages is None:
        messages = []
        if system is not None:
            messages += [{"role": "system", "content": system}]
        messages += [{"role": "user", "content": "Hello"}]
        resp = pt_engine.infer([{"messages": messages}], request_config=request_config)
        response = resp[0].choices[0].message.content
        messages += [
            {"role": "assistant", "content": response},
            {"role": "user", "content": "<image>What is this?"},
        ]
    else:
        messages = messages.copy()
    if images is None:
        images = ["http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/cat.png"]
    resp = pt_engine.infer(
        [{"messages": messages, "images": images, **kwargs}],
        request_config=request_config,
    )
    response = resp[0].choices[0].message.content
    messages += [{"role": "assistant", "content": response}]
    logger.info(f"model: {pt_engine.model_info.model_name}, messages: {messages}")
    return response


def test_qwen2_vl():
    pt_engine = PtEngine("Qwen/Qwen2-VL-2B-Instruct")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert (
        response
        == response2
        == "This is an image of a kitten with black and white fur, large round eyes, looking very cute."
    )


def test_qwen2_5_vl():
    pt_engine = PtEngine("Qwen/Qwen2.5-VL-7B-Instruct")
    messages = [{"role": "user", "content": "<image>What kind of dog is this?"}]
    images = [
        "https://qianwen-res.oss-accelerate-overseas.aliyuncs.com/Qwen2-VL/demo_small.jpg"
    ]
    response = _infer_model(pt_engine, messages=messages, images=images)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine, messages=messages, images=images)
    assert (
        response
        == response2
        == (
            "The dog in the picture appears to be a Labrador Retriever. Labradors are known for their "
            "friendly and energetic nature, which is evident in the image where the dog seems to be "
            "interacting playfully with the person. The dog's size, coat color, and build are "
            "characteristic of the Labrador Retriever breed."
        )
    )


def test_qwen2_5_omni():
    pt_engine = PtEngine("Qwen/Qwen2.5-Omni-7B")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert response == response2


def test_qvq():
    pt_engine = PtEngine("Qwen/QVQ-72B-Preview")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert response == response2


def test_internvl2():
    pt_engine = PtEngine("OpenGVLab/InternVL2-2B")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert response == response2


def test_internvl2_phi3():
    pt_engine = PtEngine("OpenGVLab/Mini-InternVL-Chat-4B-V1-5")
    _infer_model(pt_engine, system="")
    pt_engine.default_template.template_backend = "jinja"
    _infer_model(pt_engine, system="")


def test_internvl3_8b():
    pt_engine = PtEngine("OpenGVLab/InternVL3-8B")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(
        pt_engine,
        system="You are InternVL, a multimodal large language model.",
    )
    assert response == response2


def test_internvl3_9b():
    pt_engine = PtEngine("OpenGVLab/InternVL3-9B")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(
        pt_engine,
        system="You are InternVL, a multimodal large language model.",
    )
    assert response == response2


def test_llava():
    pt_engine = PtEngine("AI-ModelScope/llava-v1.6-mistral-7b")
    _infer_model(pt_engine)


def test_yi_vl():
    pt_engine = PtEngine("01ai/Yi-VL-6B")
    _infer_model(pt_engine)


def test_glm4v():
    # There will be differences in '\n'. This is normal.
    pt_engine = PtEngine("ZhipuAI/glm-4v-9b")
    messages = [{"role": "user", "content": "Describe this image"}]
    response = _infer_model(pt_engine, messages=messages)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine, messages=messages)
    assert response == (
        "This image is a close-up of a kitten with striking blue eyes and mixed grey, white, and brown fur. Its ears are perked up with distinct whiskers, looking very cute."
    )
    assert response2 == (
        "This is a close-up photograph showing a fluffy kitten with large, round dark blue eyes and bright features. Its nose is small,"
        "pink, with slender whiskers and upright ears with soft, dense fur."
        "The pattern is mainly white and brown, against a softly blurred indoor background."
    )


def test_cogagent():
    pt_engine = PtEngine("ZhipuAI/cogagent-9b-20241220")
    messages = [
        {
            "role": "user",
            "content": """<image>Task: I'm looking for a software to \"edit my photo with grounding\"
History steps:
(Platform: Mac)
(Answer in Action-Operation-Sensitive format.)""",
        }
    ]
    images = ["https://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/agent.png"]
    response = _infer_model(pt_engine, messages=messages, images=images)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine, messages=messages, images=images)
    assert (
        response
        == response2
        == (
            """Action: Click on the 'Adobe Photoshop 2023' icon located in the middle of the screen to open the application.
Grounded Operation: CLICK(box=[[346,574,424,710]], element_type='card', element_info='Adobe Photoshop 2023')
<<General Action>>"""
        )
    )


def test_minicpmv():
    pt_engine = PtEngine("OpenBMB/MiniCPM-V-2_6")
    _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    _infer_model(pt_engine)


def test_minicpmo():
    pt_engine = PtEngine("OpenBMB/MiniCPM-o-2_6")
    messages = [
        {
            "role": "user",
            "content": "<image><image>Compare image 1 and image 2, tell me about the differences between image 1 and image 2.",
        }
    ]
    images = [
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/cat.png",
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/animal.png",
    ]
    response = _infer_model(pt_engine, messages=messages, images=images)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine, messages=messages, images=images)
    assert (
        response
        == response2
        == (
            "The main difference between image 1 and image 2 is the subject matter. "
            "Image 1 features a close-up of a kitten, while image 2 depicts a cartoon illustration of four sheep "
            "standing in a grassy field. The setting, the number of subjects, and the overall style of the images "
            "are distinct from each other."
        )
    )


def test_got_ocr():
    # https://github.com/modelscope/ms-swift/issues/2122
    pt_engine = PtEngine("stepfun-ai/GOT-OCR2_0")
    _infer_model(
        pt_engine,
        messages=[{"role": "user", "content": "OCR: "}],
        images=["https://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/ocr.png"],
    )


def test_got_ocr_hf():
    pt_engine = PtEngine("stepfun-ai/GOT-OCR-2.0-hf")
    response = _infer_model(
        pt_engine,
        messages=[{"role": "user", "content": "OCR: "}],
        images=["https://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/ocr.png"],
    )
    assert response[:200] == (
        "Introduction: Framework supports training, inference, evaluation, and deployment of 250+ LLMs and 35+ MLLMs. Developers can directly integrate"
        "this framework into research and production workflows. Beyond standard PEFT techniques,"
        " it provides a comprehensive adapters library supporting NEFTune, LoRA+, and LLaMA-PRO,"
        "ready for direct usage in custom pipelines."
    )


def test_llama_vision():
    pt_engine = PtEngine("LLM-Research/Llama-3.2-11B-Vision-Instruct")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert response == response2


def test_llava_hf():
    pt_engine = PtEngine("llava-hf/llava-v1.6-mistral-7b-hf")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert response == response2


def test_florence():
    pt_engine = PtEngine("AI-ModelScope/Florence-2-base-ft")
    _infer_model(
        pt_engine, messages=[{"role": "user", "content": "who are you?"}], images=[]
    )

    _infer_model(
        pt_engine,
        messages=[{"role": "user", "content": "<OD>"}],
        images=[
            "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/animal.png"
        ],
    )


def test_phi3_vision():
    # pt_engine = PtEngine('LLM-Research/Phi-3-vision-128k-instruct')
    pt_engine = PtEngine("LLM-Research/Phi-3.5-vision-instruct")
    _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    _infer_model(pt_engine)


def test_qwen_vl():
    pt_engine = PtEngine("Qwen/Qwen-VL-Chat")
    _infer_model(pt_engine)


def test_llava_onevision_hf():
    pt_engine = PtEngine("llava-hf/llava-onevision-qwen2-0.5b-ov-hf")
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert response == response2


def test_xcomposer2_5():
    pt_engine = PtEngine(
        "Shanghai_AI_Laboratory/internlm-xcomposer2d5-ol-7b:base", torch.float16
    )
    # pt_engine = PtEngine('Shanghai_AI_Laboratory/internlm-xcomposer2d5-7b')
    response = _infer_model(pt_engine, system="")
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert response == response2


def test_deepseek_vl():
    # pt_engine = PtEngine('deepseek-ai/deepseek-vl-1.3b-chat')
    pt_engine = PtEngine("deepseek-ai/Janus-1.3B")
    _infer_model(pt_engine)


def test_deepseek_janus():
    pt_engine = PtEngine("deepseek-ai/Janus-Pro-7B")
    messages = [{"role": "user", "content": "Describe image"}]
    response = _infer_model(pt_engine, messages=messages)
    assert response == (
        "This is a very cute cat photo. The fur is white with grey markings and large, bright blue eyes,"
        "looking playful and inquisitive against a soft bokeh background."
        "The overall image conveys a warm and delightful feeling."
    )


def test_deepseek_vl2():
    pt_engine = PtEngine("deepseek-ai/deepseek-vl2-small")
    response = _infer_model(pt_engine)
    assert response == (
        "This is a cute kitten with big blue eyes and soft fur, with upright ears and alert curiosity."
        "With a pink nose and lively expression, the kitten appears energetic and inquisitive."
    )


def test_mplug_owl2():
    # pt_engine = PtEngine('iic/mPLUG-Owl2')
    pt_engine = PtEngine("iic/mPLUG-Owl2.1")
    _infer_model(pt_engine, messages=[{"role": "user", "content": "<image>What is this?"}])


def test_mplug_owl3():
    # pt_engine = PtEngine('iic/mPLUG-Owl3-7B-240728')
    pt_engine = PtEngine("iic/mPLUG-Owl3-7B-241101")
    response = _infer_model(pt_engine, system="")
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine, system="")
    assert response == response2


def test_ovis1_6():
    pt_engine = PtEngine("AIDC-AI/Ovis1.6-Gemma2-9B")
    # pt_engine = PtEngine('AIDC-AI/Ovis1.6-Gemma2-27B')
    response = _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine)
    assert response == response2


def test_ovis1_6_llama3():
    pt_engine = PtEngine("AIDC-AI/Ovis1.6-Llama3.2-3B")
    messages = [{"role": "user", "content": "What is this?"}]
    # llama3
    response = _infer_model(pt_engine, messages=messages)
    pt_engine.default_template.template_backend = "jinja"
    # llama3_2
    _infer_model(
        pt_engine,
        messages=messages,
        system="You are a helpful and honest multimodal assistant.",
    )
    assert (
        response
        == "This is a kitten, exhibiting juvenile features such as large expressive eyes, fine whiskers, and soft juvenile coat."
    )


def test_ovis2():
    pt_engine = PtEngine("AIDC-AI/Ovis2-2B")  # with flash_attn
    response = _infer_model(
        pt_engine, messages=[{"role": "user", "content": "Describe the image."}]
    )
    assert response[:200] == (
        "The image features a close-up portrait of a young kitten with striking blue eyes. "
        "The kitten has a distinctive coat pattern with a mix of gray, black, and white fur, "
        "typical of a tabby pattern. Its ea"
    )


def test_paligemma():
    pt_engine = PtEngine("AI-ModelScope/paligemma-3b-mix-224")
    response = _infer_model(
        pt_engine, messages=[{"role": "user", "content": "detect cat"}]
    )
    assert response == "<loc0000><loc0000><loc1022><loc1022> cat"


def test_paligemma2():
    pt_engine = PtEngine(
        "AI-ModelScope/paligemma2-3b-ft-docci-448", torch_dtype=torch.bfloat16
    )
    response = _infer_model(
        pt_engine, messages=[{"role": "user", "content": "caption en"}]
    )
    assert response == (
        "A close up view of a white and gray kitten with black stripes on its head and face staring forward with "
        "its light blue eyes. The kitten is sitting on a white surface with a blurry background. "
        "There is a light shining on the top of the kitten's head and the front of its body."
    )


def test_pixtral():
    pt_engine = PtEngine("AI-ModelScope/pixtral-12b")
    _infer_model(pt_engine, messages=[{"role": "user", "content": "<image>What is this?"}])


def test_glm_edge_v():
    pt_engine = PtEngine("ZhipuAI/glm-edge-v-2b")
    _infer_model(pt_engine, messages=[{"role": "user", "content": "<image>What is this?"}])


def test_internvl2_5():
    pt_engine = PtEngine("OpenGVLab/InternVL2_5-26B")
    _infer_model(pt_engine)
    pt_engine.default_template.template_backend = "jinja"
    _infer_model(
        pt_engine,
        system="You are InternVL, a multimodal large language model.",
    )


def test_internvl2_5_mpo():
    pt_engine = PtEngine("OpenGVLab/InternVL2_5-1B-MPO", model_type="internvl2_5")
    response = _infer_model(
        pt_engine,
        messages=[{"role": "user", "content": "Hello, who are you?"}],
        images=[],
    )
    assert response == (
        "Hello! I'm an AI assistant whose name is InternVL, developed jointly by Shanghai AI Lab, "
        "Tsinghua University and other partners."
    )
    response2 = _infer_model(
        pt_engine, messages=[{"role": "user", "content": "<image>What is this?"}]
    )
    assert response2 == (
        "This is a close-up photograph of a kitten with blue eyes and fluffy fur, capturing an endearing portrait."
    )


def test_megrez_omni():
    pt_engine = PtEngine("InfiniAI/Megrez-3B-Omni")
    _infer_model(pt_engine)
    response = _infer_model(
        pt_engine,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "audio", "audio": "weather.wav"},
                ],
            }
        ],
    )
    assert response == (
        "From the image, ambient lighting suggests a pleasant day with soft indoor illumination."
        "Diffused lighting without harsh shadows indicates comfortable indoor daylight."
    )


def test_molmo():
    # pt_engine = PtEngine('LLM-Research/Molmo-7B-O-0924')
    pt_engine = PtEngine("LLM-Research/Molmo-7B-D-0924")
    _infer_model(pt_engine)
    response = _infer_model(
        pt_engine, messages=[{"role": "user", "content": "<image>What is this?"}]
    )
    assert response == (
        " This is a close-up photograph of a young kitten. "
        "The kitten has striking blue eyes and a mix of white and black fur, "
        "with distinctive black stripes on its head and face. "
        "It's looking directly at the camera with an alert and curious expression. "
        "The kitten's fur appears soft and fluffy, and its pink nose and white whiskers are clearly visible. "
        "The background is blurred, which emphasizes the kitten as the main subject of the image."
    )


def test_molmoe():
    pt_engine = PtEngine("LLM-Research/MolmoE-1B-0924")
    response = _infer_model(
        pt_engine, messages=[{"role": "user", "content": "<image>What is this?"}]
    )
    assert response == (
        " This is a close-up photograph of a kitten's face. The kitten has striking blue eyes and "
        "a mix of white, black, and brown fur. It's looking directly at the camera with an adorable "
        "expression, its ears perked up and whiskers visible. The image captures the kitten's cute "
        "features in sharp detail, while the background is blurred, creating a soft, out-of-focus "
        "effect that emphasizes the young feline's charm."
    )


def test_doc_owl2():
    pt_engine = PtEngine("iic/DocOwl2", torch_dtype=torch.float16)
    response = _infer_model(
        pt_engine, messages=[{"role": "user", "content": "Who are you?"}], images=[]
    )
    images = [
        "https://modelscope.cn/models/iic/DocOwl2/resolve/master/examples/docowl2_page0.png",
        "https://modelscope.cn/models/iic/DocOwl2/resolve/master/examples/docowl2_page1.png",
        "https://modelscope.cn/models/iic/DocOwl2/resolve/master/examples/docowl2_page2.png",
        "https://modelscope.cn/models/iic/DocOwl2/resolve/master/examples/docowl2_page3.png",
        "https://modelscope.cn/models/iic/DocOwl2/resolve/master/examples/docowl2_page4.png",
        "https://modelscope.cn/models/iic/DocOwl2/resolve/master/examples/docowl2_page5.png",
    ]
    response = _infer_model(
        pt_engine,
        messages=[
            {
                "role": "user",
                "content": "<image>" * len(images)
                + "what is this paper about? provide detailed information.",
            }
        ],
        images=images,
    )
    assert response == (
        "This paper is about multimodal Language Models(MLMs) achieving promising OCR-free "
        "Document Understanding by performing understanding by the cost of generating thorough sands of visual "
        "tokens for a single document image, leading to excessive GPU computation time. The paper also discusses "
        "the challenges and limitations of existing multimodal OCR approaches and proposes a new framework for "
        "more efficient and accurate OCR-free document understanding."
    )


def test_valley():
    pt_engine = PtEngine("bytedance-research/Valley-Eagle-7B")
    _infer_model(pt_engine)


def test_ui_tars():
    os.environ["MAX_PIXELS"] = str(1280 * 28 * 28)
    pt_engine = PtEngine("bytedance-research/UI-TARS-2B-SFT")
    prompt = (
        "You are a GUI agent. You are given a task and your action history, with screenshots. "
        "You need to perform the next action to complete the task."
        + r"""

## Output Format
```\nThought: ...
Action: ...\n```

## Action Space

click(start_box='<|box_start|>(x1,y1)<|box_end|>')
left_double(start_box='<|box_start|>(x1,y1)<|box_end|>')
right_single(start_box='<|box_start|>(x1,y1)<|box_end|>')
drag(start_box='<|box_start|>(x1,y1)<|box_end|>', end_box='<|box_start|>(x3,y3)<|box_end|>')
hotkey(key='')
type(content='') #If you want to submit your input, use \"\
\" at the end of `content`.
scroll(start_box='<|box_start|>(x1,y1)<|box_end|>', direction='down or up or right or left')
wait() #Sleep for 5s and take a screenshot to check for any changes.
finished()
call_user() # Submit the task and call the user when the task is unsolvable, or when you need the user's help.


## Note
- Use Chinese in `Thought` part.
- Summarize your next action (with its target element) in one sentence in `Thought` part.

## User Instruction
"""
    )
    instruction = 'I\'m looking for a software to "edit my photo with grounding"'
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt + instruction},
            ],
        },
    ]
    images = ["https://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/agent.png"]
    response = _infer_model(pt_engine, messages=messages, images=images)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine, messages=messages, images=images)
    assert response == response2


def test_phi4_vision():
    pt_engine = PtEngine("LLM-Research/Phi-4-multimodal-instruct")
    response = _infer_model(
        pt_engine, messages=[{"role": "user", "content": "describe the image."}]
    )
    assert response == (
        "The image features a close-up of a kitten's face. The kitten has large, "
        "round eyes with a bright gaze, and its fur is predominantly white with black stripes. "
        "The kitten's ears are pointed and alert, and its whiskers are visible. The background is blurred, "
        "drawing focus to the kitten's face."
    )
    response = _infer_model(
        pt_engine,
        messages=[{"role": "user", "content": "describe the audio."}],
        images=[],
        audios=[
            "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/weather.wav"
        ],
    )
    assert response == "The weather is really nice today"


def test_gemma3_vision():
    pt_engine = PtEngine("LLM-Research/gemma-3-4b-it")
    response = _infer_model(
        pt_engine,
        messages=[{"role": "user", "content": "<image>Describe this image in detail."}],
    )
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(
        pt_engine,
        messages=[{"role": "user", "content": "<image>Describe this image in detail."}],
    )
    assert (
        response[:80]
        == response2[:80]
        == (
            "Here's a detailed description of the image:\n\n**Overall Impression:**\n\nThe image "
        )
    )


def test_mistral_2503():
    pt_engine = PtEngine("mistralai/Mistral-Small-3.1-24B-Instruct-2503")
    response = _infer_model(
        pt_engine,
        messages=[{"role": "user", "content": "What is shown in this image?"}],
    )
    assert response == (
        "The image shows a close-up of a Siamese kitten. The kitten has distinctive blue almond-shaped eyes, "
        "a pink nose, and a light-colored coat with darker points on the ears, paws, tail, and face, "
        "which are characteristic features of the Siamese breed. "
        "The kitten appears to be looking directly at the viewer with a curious and endearing expression."
    )


def test_llama4():
    pt_engine = PtEngine("LLM-Research/Llama-4-Scout-17B-16E-Instruct")
    messages = [
        {
            "role": "user",
            "content": "<image><image>What is the difference between the two images?",
        }
    ]
    images = [
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/cat.png",
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/animal.png",
    ]
    response = _infer_model(pt_engine, messages=messages, images=images)
    assert (
        response[:128]
        == (
            "The two images are distinct in their subject matter and style. The first image features "
            "a realistic depiction of a kitten, while"
        )
        and len(response) == 654
    )


def test_kimi_vl():
    pt_engine = PtEngine("moonshotai/Kimi-VL-A3B-Instruct")
    messages = [
        {
            "role": "user",
            "content": "<image><image>What is the difference between the two images?",
        }
    ]
    images = [
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/cat.png",
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/animal.png",
    ]
    response = _infer_model(pt_engine, messages=messages, images=images)
    assert response == (
        "The first image is a close-up of a kitten with a blurred background, "
        "while the second image is a cartoon of four sheep standing in a field."
    )


def test_kimi_vl_thinking():
    pt_engine = PtEngine("moonshotai/Kimi-VL-A3B-Thinking-2506")
    messages = [
        {
            "role": "user",
            "content": "<image><image>What is the difference between the two images?",
        }
    ]
    images = [
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/cat.png",
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/animal.png",
    ]
    response = _infer_model(pt_engine, messages=messages, images=images)
    assert response[:200] == (
        "◁think▷So, let's analyze the two images. The first image is a close - "
        "up of a real kitten with detailed fur, whiskers, and a realistic style. "
        "The second image is an illustration of four sheep in a car"
    )


def test_glm4_1v():
    models = ["ZhipuAI/GLM-4.1V-9B-Thinking"]
    messages = [
        {
            "role": "user",
            "content": "<image><image>What is the difference between the two images?",
        }
    ]
    images = [
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/cat.png",
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/animal.png",
    ]
    for model in models:
        pt_engine = PtEngine(model)
        response = _infer_model(pt_engine, messages=messages, images=images)
        pt_engine.default_template.template_backend = "jinja"
        response2 = _infer_model(pt_engine, messages=messages, images=images)
        assert response == response2


def test_gemma3n():
    pt_engine = PtEngine("google/gemma-3n-E2B-it")
    messages = [
        {
            "role": "user",
            "content": "<image><image>What is the difference between the two images?",
        }
    ]
    images = [
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/cat.png",
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/animal.png",
    ]
    response = _infer_model(pt_engine, messages=messages, images=images)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine, messages=messages, images=images)
    assert response == response2


def test_keye_vl():
    pt_engine = PtEngine("Kwai-Keye/Keye-VL-8B-Preview")
    messages = [
        {
            "role": "user",
            "content": "<image><image>What is the difference between the two images?",
        }
    ]
    images = [
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/cat.png",
        "http://modelscope-open.oss-cn-hangzhou.aliyuncs.com/images/animal.png",
    ]
    response = _infer_model(pt_engine, messages=messages, images=images)
    pt_engine.default_template.template_backend = "jinja"
    response2 = _infer_model(pt_engine, messages=messages, images=images)
    assert response == response2


if __name__ == "__main__":
    from swift.llm import PtEngine, RequestConfig
    from swift.utils import get_logger, seed_everything

    logger = get_logger()
    # test_qwen2_vl()
    # test_qwen2_5_vl()
    # test_qwen2_5_omni()
    # test_internvl2()
    # test_internvl2_phi3()
    # test_llava()
    # test_ovis1_6()
    # test_ovis1_6_llama3()
    # test_ovis2()
    # test_yi_vl()
    # test_deepseek_vl()
    # test_deepseek_janus()
    # test_deepseek_vl2()
    # test_qwen_vl()
    # test_glm4v()
    # test_cogagent()
    # test_llava_onevision_hf()
    # test_minicpmv()
    # test_got_ocr()
    # test_got_ocr_hf()
    # test_paligemma()
    # test_paligemma2()
    # test_pixtral()
    # test_llama_vision()
    # test_llava_hf()
    # test_florence()
    # test_glm_edge_v()
    # test_phi3_vision()
    # test_phi4_vision()
    # test_internvl2_5()
    # test_internvl2_5_mpo()
    # test_mplug_owl3()
    # test_xcomposer2_5()
    # test_megrez_omni()
    # test_qvq()
    # test_mplug_owl2()
    # test_molmo()
    # test_molmoe()
    # test_doc_owl2()
    # test_minicpmo()
    # test_valley()
    # test_ui_tars()
    # test_gemma3_vision()
    # test_mistral_2503()
    # test_llama4()
    # test_internvl3_8b()
    # test_internvl3_9b()
    # test_kimi_vl()
    # test_kimi_vl_thinking()
    # test_glm4_1v()
    # test_gemma3n()
    test_keye_vl()
