import os

# 提前注入虚拟的环境变量，防止 `app.core.config.Settings` 初始化时报错
os.environ["OPENAI_API_KEY"] = "mock-openai-key"
os.environ["JINA_API_KEY"] = "mock-jina-key"
