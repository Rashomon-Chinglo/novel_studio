import asyncio

from app.core.config import settings
from app.core.llm import get_llm


async def test_simple_llm():
    print(f"Testing with Model: {settings.OPENAI_MODEL}")
    print(f"Base URL: {settings.OPENAI_BASE_URL}")
    # Don't print the whole key for security, just prefix/suffix
    key = settings.OPENAI_API_KEY
    if len(key) > 10:
        print(f"API Key: {key[:5]}...{key[-5:]}")
    else:
        print("API Key is very short or empty!")

    llm = get_llm()
    try:
        res = await llm.ainvoke("hi")
        print(f"Response: {res.content}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_simple_llm())
