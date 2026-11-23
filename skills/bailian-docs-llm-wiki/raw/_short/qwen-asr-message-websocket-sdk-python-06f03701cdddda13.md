# Qwen-Audio-ASR-Message Python SDK

## 前提条件

-   已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。请配置API Key到环境变量，而非硬编码在代码中，防范因代码泄露导致的安全风险。
-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 快速开始

将示例中的 `{WorkspaceId}` 换成实际的业务空间 ID，`{YOUR_AUDIO_FILE}` 换成本地 16 kHz WAV 文件路径。运行后，终端输出识别结果。

```
import os
import dashscope

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 识别本地语音文件：recognize_file自动分块发送音频并驱动到任务结束
for event in client.audio.asr.recognize_file(
        '{YOUR_AUDIO_FILE}',
        model='qwen-audio-3.1-asr-flash-message',
        format='wav',
        sample_rate=16000):
    payload = event.get('payload') or {}
    sentence = (payload.get('output') or {}).get('sentence') or {}
    if sentence.get('text') and not sentence.get('heartbeat'):
        print('识别结果：', sentence['text'])
```

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/realtime-websocket-python-sdk-qwen-audio-asr-fun-asr#model-qwen-audio-asr-message)
-   [接口参考](raw/_short/realtime-websocket-python-sdk-qwen-audio-asr-fun-4386efe6c60ac2b2.md)
