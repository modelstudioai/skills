# getting started

百炼平台提供统一的 API 接口与 CLI 工具，支持快速接入大模型能力。本文档面向开发者，说明基础使用路径、关键参数含义、功能边界及常见约束。所有操作均需完成 [安装与鉴权](getting-started/installation.md) 后方可进行。

## 支持的模型/功能

当前支持调用 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、Yi 系列及部分开源模型（通过 `model` 参数指定）。文本生成、流式响应、[函数调用](../concepts/function-calling.md)（tool calling）和多轮对话上下文管理均已上线。图像理解（qwen-vl）与语音转文本（qwen-audio）功能处于灰度阶段，详见 [概览](getting-started/overview.md)。> **注意**：文档 1 中未列出具体模型列表，实际可用模型以 [快速开始](getting-started/quickstart.md) 示例中 `model` 字段值为准，部分旧文档提及的 `qwen-14b-chat` 已下线。

## 关键参数

必填参数：`model`（模型标识符）、`input.messages`（消息数组，至少含 `role` 和 `content`）。  
常用可选参数：`temperature`（0.0–2.0，默认 1.0）、`top_p`（0.1–1.0）、`max_tokens`（默认 2048，最大 8192）、`stream`（布尔值，启用流式响应）。  
工具调用需额外传入 `tools` 数组与 `tool_choice`。参数语义与行为严格遵循 [快速开始](getting-started/quickstart.md) 中定义的 schema。

## 使用方式

推荐通过 CLI 快速验证：  
```bash
bailian chat --model qwen-turbo --message "你好"
```  
或调用 REST API（POST `/v1/chat/completions`），需在 Header 中携带 `Authorization: Bearer <api_key>`。完整请求结构与示例见 [快速开始](getting-started/quickstart.md)。CLI 安装与密钥配置步骤请参考 [安装与鉴权](getting-started/installation.md)。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为 32768（含 system prompt）；  
- 免费试用额度为 1000 次/日，超出后需绑定计费账户；  
- 流式响应（`stream=true`）下，`max_tokens` 实际生效值可能略低于设定值，因服务端需预留终止标记空间；  
- 非 JSON Schema 格式的 `tools` 定义将被静默忽略——该行为与 [概览](getting-started/overview.md) 描述一致，但与早期内测文档存在差异。

## 来源文档

- [开始使用](../../raw/cli/getting-started.md)


