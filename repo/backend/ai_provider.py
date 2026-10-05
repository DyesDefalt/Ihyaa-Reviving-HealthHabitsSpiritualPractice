"""Configurable OpenAI adapter. The key stays on the server."""
import os

from emergentintegrations.llm.chat import LlmChat, StreamDone, TextDelta, UserMessage


def model_info() -> dict:
    return {"provider": os.environ["COACH_PROVIDER"], "model": os.environ["COACH_MODEL"]}


async def stream_reply(session_id: str, system: str, history: list[dict], text: str):
    config = model_info()
    chat = LlmChat(
        api_key=os.environ["EMERGENT_LLM_KEY"], session_id=session_id,
        system_message=system,
        initial_messages=[{"role": "system", "content": system}, *history],
    ).with_model(config["provider"], config["model"]).with_params(
        max_completion_tokens=1400, timeout=50, num_retries=0,
    )
    completed = False
    async for event in chat.stream_message(UserMessage(text=text)):
        if isinstance(event, TextDelta):
            yield event.content
        elif isinstance(event, StreamDone):
            if event.finish_reason not in ("stop", "end_turn"):
                raise RuntimeError("Incomplete coach response")
            completed = True
    if not completed:
        raise RuntimeError("Missing completion event")