# OpenAI 兼容接口

百炼平台提供与 OpenAI 客户端库直接兼容的 API 接口，开发者可复用已有的 OpenAI SDK 代码，仅需更换 API endpoint 和密钥即可完成接入，是迁移成本最低的调用方式。

## 在百炼中的使用场景

### 文本生成模型调用

OpenAI 兼容接口是百炼为文本生成模型提供的四种调用方式之一，适合从 OpenAI 生态迁移现有应用或接入第三方工具。其中：

- **OpenAI 兼容 Chat Completions**：与标准 OpenAI 协议完全兼容，迁移成本最低。
- **OpenAI 兼容 Responses**：在 Chat Completions 基础上扩展，内置联网搜索、代码解释器和网页内容提取等工具能力，可自动管理对话历史，适合需要工具调用的复杂场景。

### 专用模型调用

百炼平台的多个专用模型均可通过 OpenAI 兼容接口调用，包括意图理解（`tongyi-intent-detect-v3`）、机器翻译（`qwen-mt-plus` / `qwen-mt-turbo`）、GUI 界面交互（`gui-plus-2026-02-26`）和 OCR 文字提取（`qwen3.5-ocr`）等。

> **例外**：`qwen-deep-research` 深度研究模型当前仅支持 Python [DashScope SDK](dashscope-sdk.md) 和 curl，暂不支持 OpenAI 兼容接口。

### 第三方工具与客户端接入

终端 AI 编程助手（Codex、Qwen Code、Kilo CLI、Qoder CLI）、IDE 插件（Cursor、Cline、Qoder 等）以及 API 测试工具均可通过 OpenAI 兼容协议接入百炼。配置时在工具的设置中填入对应的 Base URL 和 API Key 即可。

## 关键参数与配置

### Base URL

Base URL 随计费方案和地域不同而变化：

| 计费方案 | 地域 | OpenAI 协议 Base URL |
|---------|------|---------------------|
| Token Plan 团队版 | 北京 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | 北京 | `https://coding.dashscope.aliyuncs.com/v1` |
| 按量计费 | 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 按量计费 | 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 按量计费 | 弗吉尼亚 | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

### 鉴权

所有接口均通过百炼平台统一鉴权，使用百炼 API Key。HTTP 调用时在 Header 中传入 `Authorization: Bearer $DASHSCOPE_API_KEY`，推荐通过环境变量 `DASHSCOPE_API_KEY` 配置以避免硬编码。

> **注意**：三种计费方案的 API Key 互不通用，按量计费的 API Key 还需与所选地域对应。配置时必须确保 API Key 与 Base URL 来自同一方案。

### 请求路径

OpenAI 兼容接口的请求路径通常为 `/compatible-mode/v1/chat/completions`，请求体结构与 OpenAI Chat Completions API 一致，`model` 参数填入百炼模型名称（如 `qwen-plus`、`farui-plus` 等）。

## 接口选择建议

| 场景 | 推荐接口 |
|------|----------|
| 从 OpenAI 迁移现有应用 | OpenAI 兼容 Chat Completions |
| 需要内置工具（搜索、代码执行等） | OpenAI 兼容 Responses |
| 需要百炼平台完整功能集和最大灵活性 | DashScope 原生接口 |

第三方兼容接口便于迁移，但功能覆盖度受限于协议本身；如需使用百炼平台特有的高级参数和全部能力，推荐使用 DashScope 原生接口。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


