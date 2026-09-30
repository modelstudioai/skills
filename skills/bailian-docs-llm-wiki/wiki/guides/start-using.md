# start using

本节介绍如何快速接入百炼平台并启动首个应用，涵盖模型调用、应用构建和基础配置。开发者可选择零代码方式快速搭建知识库问答助手，或通过 API 集成调用大模型能力。所有操作均基于百炼控制台或 OpenAPI v3 接口完成。

## 支持的模型/功能

当前平台默认提供 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类推理模型，支持文本生成、多轮对话、结构化输出（JSON Schema）及[函数调用](../concepts/function-calling.md)（Function Calling）。知识库问答、工作流编排、RAG 增强等高级功能需在应用创建后启用。详细能力矩阵见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 关键参数

- `model`: 必填，取值必须为平台当前可用模型 ID（如 `qwen-plus`），不支持自定义别名  
- `temperature`: 取值范围 0.0–1.0，默认 0.7；设为 0 时启用确定性采样  
- `top_p`: 默认 1.0，与 `temperature` 互斥推荐仅启用其一  
- `enable_search`: 布尔值，仅在启用了知识库的应用中生效，详见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)  

> **注意**：文档 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中提及的 `streaming_timeout` 参数已在 v2.3.0 版本 API 中移除，实际调用将忽略该字段，请勿在请求体中传入。

## 使用方式

1. **零代码方式**：登录控制台 → 创建「知识库问答应用」→ 上传文档 → 发布即用，全程无需写代码，具体步骤参见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)  
2. **API 方式**：调用 `/v1/chat/completions` 端点，需携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`，请求体格式遵循 OpenAI 兼容协议（但 `messages` 字段不支持 `name` 属性）

## 限制和注意事项

- 单次请求最大 `input_tokens + output_tokens ≤ 32768`（`qwen-max` 模型）；其他模型上限详见控制台配额页  
- 知识库问答应用默认启用缓存，首次查询响应可能延迟 1–3 秒（索引构建耗时），后续请求毫秒级返回  
- API 调用频率限制为 10 QPS / key（企业版可申请提升），超出将返回 `429 Too Many Requests`  
- 所有输入内容经平台自动脱敏处理，敏感词过滤策略以 [开始使用](../../raw/application-user-guide/start-using.md) 中最新说明为准

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


