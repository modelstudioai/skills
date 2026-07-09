# 流式输出

流式输出（Streaming）是指模型在生成过程中逐步返回部分结果，而非等待全部生成完毕后一次性返回。这种方式显著降低了用户感知的首字延迟，适用于对话交互、长文本生成等需要实时反馈的场景。

## 适用场景

在百炼平台中，流式输出贯穿多个 API 接口和交互模式：

- **Chat Completions 接口**：最常用的文本对话场景，通过设置 `stream=True` 开启流式输出，模型逐 token 返回生成内容。
- **Responses API（OpenAI 兼容）**：智能体应用调用时，在请求参数中设置 `stream=true` 即可获得增量响应。
- **实时多模态接口（Omni Realtime API）**：基于 WebSocket 协议，服务端通过 `response.audio.delta` 和 `response.audio_transcript.delta` 等事件持续推送音频和文本增量数据，实现低延迟的实时语音对话。

## 关键参数与配置

### HTTP 接口（Chat Completions / Responses API）

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | boolean | 是否开启流式输出，默认 `false` |
| `stream_options.include_usage` | boolean | 流式模式下是否在最后一个 chunk 中返回 token 用量统计 |

### WebSocket 接口（Omni Realtime API）

实时接口天然采用流式传输，服务端通过以下事件逐步推送结果：

| 事件 | 含义 |
|------|------|
| `response.audio.delta` | 增量音频数据（Base64 编码的 PCM） |
| `response.audio_transcript.delta` | 增量文本转录 |
| `response.done` | 响应生成完毕 |

## 使用示例

使用 OpenAI Python SDK 开启流式输出：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=True,
    stream_options={"include_usage": True},
)

for chunk in stream:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
```

## 注意事项

- 流式模式下，每个 chunk 仅包含增量内容（delta），客户端需自行拼接完整响应。
- 设置 `stream_options={"include_usage": True}` 可在流结束时获取本次请求的 token 消耗，便于计费统计。
- [异步调用](async-invocation.md)（`background=true`）与流式输出互斥——异步任务通过轮询获取最终结果，不支持流式返回。
- 实时语音场景建议直接使用 WebSocket 接口，HTTP 流式输出不适用于音频数据的实时传输。

## 关联主题页

- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [omni realtime api](../api/omni-realtime-api.md)


