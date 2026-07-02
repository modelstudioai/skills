# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组遵循 OpenAI API 协议规范的 RESTful 接口，开发者可直接使用 OpenAI 官方 SDK 或任何兼容 OpenAI 协议的客户端工具接入百炼模型服务，通常只需替换 `api_key`、`base_url` 和 `model` 三个参数即可完成迁移。

## 接口族与覆盖能力

百炼的 OpenAI 兼容接口不是单一端点，而是一组覆盖多种能力的接口族，调用路径统一位于 `compatible-mode/v1` 下：

| 接口 | HTTP 路径 | 典型场景 |
|------|-----------|----------|
| Chat Completions | `POST /chat/completions` | 多轮对话、function call、流式输出 |
| Responses | `POST /responses` | 智能体原生能力、内置工具（联网搜索、代码解释器、网页抓取）、自动管理对话历史 |
| Completions | `POST /completions` | 代码补全、文本续写（FIM） |
| Embeddings | `POST /embeddings` | 文本向量化 |
| Vision | 走 Chat Completions | 图像/视频理解 |
| File | `POST /files` | 上传/查询/删除文件 |
| Batch | `POST /batches` | 异步批量推理，费用 50% |
| Conversations | `POST /conversations` | 跨设备会话状态管理 |

其中 Chat Completions 是最常用的接口，支持 Qwen 全系列、DeepSeek、Kimi、GLM、MiniMax 等模型；Responses 接口是其演进版本，内置联网搜索、代码解释器和网页内容提取，并通过 `previous_response_id` 自动维护上下文。

## 使用场景

### SDK 与代码迁移

已有 OpenAI SDK 代码只需修改三个参数即可切换到百炼：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
```

### 客户端与开发工具接入

Claude Code、Cursor、Continue、Cline、Cherry Studio 等 AI 编程工具和桌面客户端均通过 OpenAI 兼容协议接入百炼。配置时在各工具的设置文件中将 Base URL 指向百炼的 `compatible-mode/v1` 端点，填入百炼 [API Key](api-key.md) 即可。

### 专用模型调用

除通义千问主对话模型外，翻译模型（qwen-mt-plus）、OCR 模型（qwen3.5-ocr）、意图理解模型（tongyi-intent-detect-v3）、界面交互模型（gui-plus）等专用模型同样支持通过 OpenAI 兼容接口调用。

## 关键参数与配置

### 鉴权三要素

| 参数 | 说明 |
|------|------|
| `api_key` | 百炼 [API Key](api-key.md)，建议通过环境变量 `DASHSCOPE_API_KEY` 注入。各地域的 [API Key](api-key.md) 互不通用 |
| `base_url` | [业务空间](workspace.md)专属域名，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`。`{WorkspaceId}` 在百炼控制台的[业务空间](workspace.md)详情页获取 |
| `model` | 模型名称，如 `qwen3.7-plus`、`qwen3.7-max`、`deepseek-v4-pro` 等 |

### 各地域 Base URL

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

> 弗吉尼亚地域使用固定域名，不带 `{WorkspaceId}`；其余地域均需替换为真实[业务空间](workspace.md) ID。

### [计费](billing.md)方案与域名差异

百炼提供按量[计费](billing.md)、Coding Plan、[Token](token.md) Plan 团队版三种方案，每种方案有独立的 Base URL 和 API Key，不能混用：

- **按量[计费](billing.md)**：使用上述业务空间专属域名
- **Coding Plan**：`https://coding.dashscope.aliyuncs.com/v1`
- **[Token](token.md) Plan 团队版**：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

## 与其他接口的关系

百炼同时提供三种协议风格的接口：

- **OpenAI 兼容接口**：迁移成本最低，生态兼容最广，适合已有 OpenAI 代码的项目
- **Anthropic 兼容接口**：兼容 Anthropic Messages API，Base URL 以 `/apps/anthropic` 结尾，适合使用 Claude Code 等 Anthropic 生态工具
- **DashScope 原生接口**：功能集最完整，参数支持最丰富，适合需要使用百炼全部能力的场景

## 限制与注意事项

- OpenAI 兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数。如需最全的采样参数或插件能力，应使用 DashScope 原生接口。
- 联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力，Chat Completions 接口不内置这些工具。
- 仅 Responses 接口自动维护对话历史，其他接口需由调用方在 `messages` 中手动管理上下文。
- 部分模型（如 Qwen-Audio、qwen-deep-research）不支持 OpenAI 兼容协议，仅支持 DashScope SDK 调用。
- API Key 与 Base URL 必须属于同一地域、同一计费方案，否则会报 `401` 错误。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [more models](../api/more-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [omni realtime api](../api/omni-realtime-api.md)


