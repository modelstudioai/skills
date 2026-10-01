# start using

本文档介绍如何快速开始使用百炼平台的核心能力，包括模型调用、应用构建与基础配置。开发者可基于平台提供的 API 或低代码界面快速集成大模型能力。所有操作均需先完成[百炼控制台注册与项目创建](../../raw/application-user-guide/getting-started.md)。

## 支持的模型/功能

当前平台默认提供 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类推理模型，支持文本生成、知识库问答、[函数调用](../concepts/function-calling.md)（Function Calling）及多轮对话状态管理。知识库问答能力依赖于[0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)中描述的向量化流程；[函数调用](../concepts/function-calling.md)需在请求中显式启用 `enable_function_calling: true` 并传入符合 OpenAI 兼容格式的 `tools` 定义。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-turbo`；必须与[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)中当前可用模型列表一致 |
| `input.messages` | array | 是 | 至少包含一个 `role: user` 的 message 对象，`content` 字段不支持空字符串或纯空白符 |
| `parameters.temperature` | number | 否 | 范围 0.0–2.0，默认 1.0；设为 0 时启用确定性采样 |

> **注意**：`top_p` 与 `temperature` 不应同时设为极端值（如 `temperature=0` 且 `top_p=0.1`），否则可能触发服务端校验拒绝——该行为与[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)中 v2024.06 版本说明存在不一致，以实际 API 响应为准。

## 使用方式

- **API 方式**：调用 `POST /v1/chat/completions`，需携带 `Authorization: Bearer <api_key>` 及 `Content-Type: application/json`。完整请求示例见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 的“API 集成”小节。
- **低代码方式**：在控制台「应用」→「新建应用」中选择「知识库问答」模板，上传文档后自动完成切片、嵌入与检索配置，无需编码。

## 限制和注意事项

- 单次请求 `input.messages` 总长度上限为 32768 token（含 system [prompt](prompt.md)）；
- 知识库问答场景下，上传文件单个大小不得超过 100 MB，且仅支持 PDF、TXT、DOCX、PPTX 格式；
- 所有 API 请求需在 `X-Bailian-Request-ID` 头中传递唯一 trace ID，便于问题定位；缺失该头可能导致日志无法关联。  
- 免费试用额度仅限新注册用户首 30 天内使用，配额详情以[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)最新公告为准。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


