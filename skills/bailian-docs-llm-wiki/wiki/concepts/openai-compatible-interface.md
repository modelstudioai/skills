# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套与 OpenAI 官方 API 高度对齐的调用方式：开发者可直接复用官方 OpenAI 客户端库（Python/Node SDK）或 HTTP 请求，仅需替换 `api_key`、`base_url` 与 `model` 三项，即可将现有 OpenAI 应用平滑迁移到百炼，无需改动业务逻辑。

## 在百炼平台的使用场景

OpenAI 兼容接口是百炼最主流的接入入口，覆盖多种典型场景：

- **迁移已有 OpenAI 应用**：追求最低迁移成本时的首选。已基于 OpenAI SDK 构建的应用，改动量极小。
- **调用通义千问及三方模型**：支持 Qwen 商业版/开源版、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及 DeepSeek、Kimi、GLM、MiniMax 等三方模型（三方直供模型仅在中国内地地域可用，需先在控制台开通）。
- **调用专用模型**：意图理解（`tongyi-intent-detect-v3`）、翻译（`qwen-mt-plus`）、OCR（`qwen3.5-ocr`）、界面交互（`gui-plus`）等多数专用模型均可通过 OpenAI 兼容接口调用。
- **接入第三方工具**：Cursor、Cline、Cherry Studio、Chatbox、Dify 等聊天客户端与开发工具，统一以「Base URL + API Key + 模型 ID」的形式通过 OpenAI 兼容协议接入百炼网关。

> 注意：并非所有模型都支持。例如 Qwen-Audio、`qwen-deep-research` 仅支持 DashScope 协议（后者仅 Python SDK、仅北京地域）。使用前请对照具体模型的 API 参考确认。

## 接口家族

OpenAI 兼容体系不止 Chat Completions，还包含多个能力接口：

- **Chat Completions（对话补全）**：最常用的接口，支持非流式、流式（`stream=True`，配合 `stream_options={"include_usage": True}` 返回 Token 统计）与 function call 工具调用。
- **Responses（智能体原生接口）**：Chat Completions 的演进版本，内置联网搜索、网页抓取、代码解释器、文搜图/图搜图等工具；输入更灵活（可直接传字符串），并通过 `previous_response_id` 自动管理多轮上下文，无需手动拼接消息历史。
- **Conversations（会话管理）**：提供会话的创建、查询、更新、删除及消息项管理，配合 Responses 可自动注入历史上下文。
- **Completions（文本补全）**：面向代码补全/内容续写，当前仅支持 `qwen-coder-turbo`，且仅适用于中国内地（北京）地域，使用 `<|fim_prefix|>...<|fim_suffix|>...<|fim_middle|>` 模板。
- **Embedding、文件、Batch** 等能力也提供对应的兼容接口，并可直接接入 LangChain / LangChain4j 等主流框架。

## 关键参数与配置

迁移的核心是配置以下三项：

- **`api_key`**：替换为百炼 API Key。各地域的 API Key 相互独立、不能跨地域混用，切换地域时需同步更换。建议写入环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。
- **`base_url`**：OpenAI SDK 统一使用以 `/compatible-mode/v1`（部分方案为 `/v1`）结尾的路径；HTTP 调用在其后追加资源路径（如 `/chat/completions`、`/responses`、`/embeddings`、`/files`）。
- **`model`**：替换为百炼支持的模型名称。

各地域 SDK `base_url`（`{WorkspaceId}` 为业务空间 ID，可在控制台业务空间详情页查看）：

| 地域 | base_url |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

最小调用示例（北京地域）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

部分模型的专属参数需通过 OpenAI SDK 的 `extra_body` 传入，例如 Qwen-MT 的 `translation_options`（`source_lang` / `target_lang` / `terms` / `tm_list` / `domain_prompt`）、Qwen-OCR 的 `min_pixels` / `max_pixels`、GUI-Plus 的 `vl_high_resolution_images`。

## 注意事项

- **Base URL 与 API Key 必须同地域、同计费方案配套**，否则会报 401 或跨地域错误。
- **推荐使用业务空间专属域名**（`{WorkspaceId}.{region}.maas.aliyuncs.com`）用于生产环境，具备更高并发、更低时延与流量隔离，请求超时 3600 秒；旧版 `dashscope.aliyuncs.com` 等域名仍可用但建议迁移，超时 600 秒。
- **旧版路径将停止维护**：Responses 与 Conversations 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 即将下线，请迁移到新版 `/compatible-mode/v1/...`。
- **依赖内置工具（联网搜索、代码解释器等）时须用 Responses 接口**，而非普通 Chat Completions。
- 跨接口迁移时需核对参数映射：DashScope 原生接口参数最全，OpenAI/Anthropic 兼容接口以各自生态的字段约定为准。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more models](../api/more-models.md)


