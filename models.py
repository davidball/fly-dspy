import os

import dspy


def venice(model_name):
    key = os.getenv("VENICE_API_KEY")
    if not key:
        return None
    return dspy.LM(
        model=f"openai/{model_name}",
        api_base="https://api.venice.ai/api/v1",
        api_key=key,
    )


def grok(model_name):
    key = os.getenv("XAI_API_KEY")
    if not key:
        return None
    return dspy.LM(
        model=f"openai/{model_name}",
        api_base="https://api.x.ai/v1",
        api_key=key,
    )


def openai(model_name):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    return dspy.LM(
        model=f"openai/{model_name}",
        api_base="https://api.openai.com/v1",
        api_key=key,
    )


def ollama(model_name):
    return dspy.LM(model=f"ollama/{model_name}")


def lms(model_name):
    return dspy.LM(
        model=f"lm_studio/{model_name}",
        api_base="http://localhost:1234/v1",
        api_key="lm-studio",  # Required dummy key
    )


ollama_qwen = ollama("qwen2.5:14b")

lms_qwen32b = lms("qwen2.5-vl-32b-instruct")

lms_qemma_12b = lms("google/gemma-3-12b")

venice_uncensored = venice("venice-uncensored")

grok_code_fast = grok("grok-code-fast")

grok_4_1_fast_reasoning = grok("grok-4-1-fast-reasoning")
