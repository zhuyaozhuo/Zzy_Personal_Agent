from langchain_zhipu import ChatZhipuAI
from core.config import settings


def get_llm(temperature: float = 0.7):
    return ChatZhipuAI(
        model=settings.ZHIPU_MODEL,
        temperature=temperature,
        api_key=settings.ZHIPU_API_KEY
    )


llm = get_llm()
