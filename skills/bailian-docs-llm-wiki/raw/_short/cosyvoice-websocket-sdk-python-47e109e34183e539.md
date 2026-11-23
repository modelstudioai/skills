# CosyVoice Python SDK

## 前提条件

-   [安装 Python SDK](raw/model-api-reference/preparations/install-sdk.md)
-   [获取并配置 API Key](raw/model-api-reference/preparations/get-api-key.md)

## 快速开始

示例使用北京。将代码中的 `{WorkspaceId}` 替换为实际的[业务空间 ID](raw/application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。运行后，音频保存到当前目录的 `output.mp3`。

```
# coding=utf-8

import os

import dashscope

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "cosyvoice-v3-plus"
# 音色
voice = "longanyang"

# 发送待合成文本，获取二进制音频
audio = client.audio.tts.synthesize("今天天气怎么样？", model=model, voice=voice)

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

## 更多示例与参考

-   [流式合成示例](https://help.aliyun.com/zh/model-studio/realtime-websocket-python-sdk-qwen-audio-tts-cosyvoice#model-cosyvoice-8e498a23461om)
-   [请求参数](https://help.aliyun.com/zh/model-studio/realtime-websocket-python-sdk-qwen-audio-tts-cosyvoice#model-cosyvoice-h3-cv-params)
-   [接口参考](https://help.aliyun.com/zh/model-studio/realtime-websocket-python-sdk-qwen-audio-tts-cosyvoice#model-cosyvoice-h2-cosyvoice-synth)
