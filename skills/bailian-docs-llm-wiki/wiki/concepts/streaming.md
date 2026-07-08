# 流式输出

流式输出（Streaming）是指服务端在生成结果的过程中，将内容以增量片段的方式逐步推送给客户端，而非等待全部生成完毕后一次性返回。在大语言模型场景中，流式输出可以显著降低用户感知的首字延迟，提升交互体验。

## 工作原理

百炼平台的流式输出基于 HTTP Server-Sent Events（SSE）协议实现。开启流式后，服务端会将模型生成的 token 逐步以事件流的形式推送到客户端，每个事件包含一段增量文本。客户端可以在收到第一个片段时就开始渲染，无需等待完整响应。

对于实时[多模态](multimodal.md)场景（如 Qwen-Omni-Realtime API），则采用 WebSocket 长连接实现双向事件流，服务端通过 `response.audio.delta`、`response.text.delta` 等事件逐帧推送音频和文本数据，实现更低延迟的实时交互。

## 适用场景

### 应用调用

通过 Responses API 或 DashScope API 调用智能体应用和工作流应用时，均可开启流式输出。适用于：

- **实时对话**：聊天机器人等交互场景，用户可以边看边等，体验更流畅。
- **长文本生成**：报告、摘要等耗时较长的生成任务，避免用户长时间等待空白响应。

> 注意：[异步调用](async-invocation.md)（`background=true`）模式下暂不支持流式输出。异步任务适合后台批量处理，结果通过轮询获取。

### 文本生成模型调用

通过 OpenAI 兼容 Chat Completions、OpenAI 兼容 Responses、Anthropic 兼容 Messages 或 DashScope 原生接口调用 Qwen 系列模型时，均支持 `stream` 参数开启流式输出。不同接口的流式响应格式遵循各自协议规范：

- [OpenAI 兼容接口](openai-compatible-interface.md)返回 `data: {...}` 格式的 SSE 事件，与 OpenAI 官方格式一致。
- DashScope 原生接口同样支持 SSE 流式，响应结构与同步调用保持一致，增量包含在 `output.text` 中。

### 实时[多模态](multimodal.md)交互

Qwen-Omni-Realtime API 通过 WebSocket 实现天然的流式交互。服务端在生成过程中持续推送音频和文本增量事件，客户端实时播放和渲染，延迟可低至毫秒级。这种模式下无需显式设置 `stream` 参数，流式是默认且唯一的交互方式。

## 关键参数与配置

### stream 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stream` | boolean | `false` | 设为 `true` 开启流式输出 |

在 HTTP API 中，通过请求体中的 `stream` 字段控制：

```json
{
  "input": { "prompt": "请介绍流式输出的原理" },
  "parameters": {},
  "stream": true
}
```

### SDK 使用示例

**Python（OpenAI 兼容）：**

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**Python（[DashScope SDK](dashscope-sdk.md) 应用调用）：**

```python
from dashscope import Application

responses = Application.call(
    app_id="YOUR_APP_ID",
    prompt="你好",
    stream=True
)

for response in responses:
    if response.output and response.output.text:
        print(response.output.text, end="", flush=True)
```

### 增量输出与全量输出

部分接口支持通过 `incremental_output` 参数控制流式响应的内容模式：

- `incremental_output=true`：每次事件只返回新增的增量文本片段。
- `incremental_output=false`（默认）：每次事件返回截至当前的全量文本。

增量模式在网络带宽受限或需要精确控制渲染的场景下更为高效。

## 流式输出与其他调用模式的关系

| 调用模式 | 是否支持流式 | 适用场景 |
|----------|-------------|----------|
| 同步调用 + 流式 | 支持 | 实时对话、交互式生成 |
| 同步调用 + 非流式 | 支持 | 简单请求、后端处理 |
| [异步调用](async-invocation.md) | 不支持 | 耗时任务、批量处理 |
| WebSocket 实时交互 | 天然流式 | 语音对话、[多模态](multimodal.md)实时交互 |

## 注意事项

- 流式模式下，客户端需要正确处理 SSE 连接的建立、数据解析和断连重试。
- 流式输出的最终结果与非流式调用完全一致，仅传输方式不同。
- 在使用代理或网关时，需确保中间层支持 SSE 长连接转发，避免缓冲导致流式效果失效。
- 视频生成等异步任务不使用流式输出，而是采用任务创建加轮询的模式获取结果。

## 关联主题页

- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [video generation api](../api/video-generation-api.md)


