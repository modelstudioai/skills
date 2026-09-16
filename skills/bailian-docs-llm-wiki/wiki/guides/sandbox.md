# sandbox

sandbox 是百炼平台提供的隔离式模型实验与调试环境，用于安全地测试提示词、微调效果、多轮对话逻辑及自定义工具集成。它支持快速创建临时实例，无需部署即可验证模型行为，适用于开发迭代与 QA 验证阶段。所有操作均通过 SDK 或 OpenAPI 完成，实例生命周期由用户自主控制。

## 支持的模型与功能

sandbox 当前支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分已发布的微调模型（需模型状态为 `published`）。功能包括：单次/流式推理、系统提示词注入、工具调用模拟、上下文长度动态配置（最大 32768 token），以及基于 JSON Schema 的结构化输出约束。不支持训练、模型上传或持久化存储。详细能力列表见 [Sandbox 概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 关键参数

- `model`: 必填，指定模型 ID（如 `qwen-turbo`），必须在 [Sandbox 快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 中列出的支持列表内；
- `enable_search`: 布尔值，启用后自动调用平台内置搜索插件（仅限 `qwen-max` 和 `qwen-plus`）；
- `response_format`: 可选，设为 `json_object` 时强制模型返回合法 JSON，需配合 `response_schema` 使用；
- `timeout`: 单位秒，默认 60，最大 120，超时后实例自动销毁。

> **注意**：`response_schema` 参数在 [Sandbox SDK 文档](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 中要求为 OpenAPI 3.0 兼容格式，但实际 API 校验仅支持 subset of JSON Schema draft-07（如不支持 `anyOf`/`not`）。请以 [Sandbox 模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) 中的 schema 示例为准。

## 使用方式

1. 调用 `POST /v1/sandbox/instances` 创建实例，传入模型与初始参数；
2. 使用返回的 `instance_id` 调用 `POST /v1/sandbox/instances/{id}/chat/completions` 发起请求；
3. 实例默认 30 分钟无活动自动释放；也可显式调用 `DELETE /v1/sandbox/instances/{id}` 提前销毁。

完整代码示例与错误码说明参见 [Sandbox SDK 文档](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- 单用户并发 sandbox 实例上限为 5 个；
- 每个实例最大上下文长度受所选模型原生限制约束（例如 `qwen-turbo` 实际上限为 8192）；
- 不支持跨实例共享 session state 或缓存；
- 所有日志与 trace 数据仅保留 7 天，不可恢复；
- 实例创建失败时，若错误信息含 `invalid_model`，请确认模型 ID 是否已在 [Sandbox 概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) 的“可用模型”章节中列出。

## 来源文档

- [Sandbox](../../raw/application-user-guide/sandbox.md)


