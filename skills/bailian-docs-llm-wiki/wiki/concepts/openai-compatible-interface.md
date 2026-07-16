# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套遵循 OpenAI API 规范的服务入口，让已有 OpenAI 应用只需替换 `api_key`、`base_url` 和 `model` 三项即可迁移到百炼，无需改动业务逻辑，是接入成本最低的调用方式。

## 在百炼平台的使用场景

OpenAI 兼容接口贯穿百炼的多类使用场景：

- **文本生成模型调用**：作为四类接口（OpenAI 兼容 Chat Completions、OpenAI 兼容 Responses、Anthropic 兼容 Messages、DashScope 原生）中迁移成本最低的一类，适合已基于 OpenAI SDK 构建的应用平滑迁移。其中 Chat Completions 为最常用入口，支持非流式、流式与工具调用（function call）；Responses 为其演进版本，内置联网搜索、代码解释器、网页抓取等工具，并通过 `previous_response_id` 自动管理多轮上下文。
- **接入第三方客户端与开发工具**：Cherry Studio、Chatbox、Cursor、Cline、Dify 等聊天客户端和编程工具，统一通过「Base URL + API Key + 模型 ID」以 OpenAI 兼容协议接入百炼网关。
- **专用模型调用**：`tongyi-intent-detect-v3`（意图理解）、`qwen-mt-plus`（翻译）、`qwen3.5-ocr`（OCR）、`gui-plus`（界面交互）等专用模型多数支持 OpenAI 兼容接口调用（注意 `qwen-deep-research` 仅支持 Python DashScope SDK，Qwen-Audio 仅支持 DashScope 协议）。
- **智能体与工作流应用调用**：应用可通过 OpenAI 兼容的 Responses API 调用，支持同步/异步、多轮对话与[流式输出](streaming-output.md)。

## 关键参数与配置

迁移与调用的核心是配置以下三要素：

- **`api_key`**：使用百炼 API Key。各地域、各计费方案的 API Key **相互独立、不能混用**，建议配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。若 Base URL 与 API Key 不配套会返回 401。
- **`base_url`**：OpenAI SDK 调用统一以 `/compatible-mode/v1`（部分方案为 `/v1`）结尾；HTTP 调用需在其后追加具体资源路径（如 `/chat/completions`、`/responses`、`/embeddings`、`/files`）。各地域 SDK Base URL 示例：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
  - 日本（东京）：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`
  - 德国（法兰克福）：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`
  - 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`

  其中 `{WorkspaceId}` 为业务空间 ID，可在控制台业务空间详情页查看。北京、新加坡地域推荐使用业务空间专属域名以获得更好的性能与稳定性。
- **`model`**：替换为百炼支持的模型名称（如 `qwen-plus`、`qwen3-max` 等）。

常用请求参数：

- `messages`（array，必选）：对话消息列表，每条含 `role`（system/user/assistant）与 `content`。
- `stream`（bool，可选）：是否[流式输出](streaming-output.md)；流式统计 Token 需配合 `stream_options={"include_usage": True}`。
- 部分专用模型的特有参数（如 Qwen-MT 的 `translation_options`、Qwen-OCR 的 `min_pixels`/`max_pixels`）在 OpenAI SDK 中通过 `extra_body` 传入。

## 调用示例

以北京地域业务空间专属域名为例（Python）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
)
print(completion.choices[0].message.content)
```

OpenAI Python SDK 要求 Python ≥ 3.8。

## 注意事项

- **协议路径区分**：OpenAI 协议 Base URL 以 `/compatible-mode/v1`（或 `/v1`）结尾，Anthropic 协议以 `/apps/anthropic` 结尾；部分工具还要求在 Anthropic 端点后追加 `/v1`，以各工具原文为准。
- **接口能力差异**：DashScope 原生接口参数最全；若依赖联网搜索、代码解释器等内置工具，需使用 Responses 而非普通 Chat Completions。跨接口迁移时需核对参数映射。
- **旧路径迁移**：Responses、Conversations 接口的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 即将停止维护，请迁移至新版 `/compatible-mode/v1/...`。
- **地域约束**：Base URL、API Key 和模型列表均不能跨地域混用；限流按主账号维度合并计算。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [get started with models](../guides/get-started-with-models.md)
- [more models](../api/more-models.md)
- [application call](../api/application-call.md)


