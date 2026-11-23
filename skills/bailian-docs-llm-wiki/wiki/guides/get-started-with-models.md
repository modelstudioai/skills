# get started with models

本文档介绍如何快速开始使用百炼平台的模型服务，涵盖模型选择、调用方式、关键参数配置及常见限制。开发者可通过控制台或 API 接入预置大模型，无需自行部署基础设施。所有模型均通过统一的 `/v1/chat/completions` 等标准接口调用。

## 支持的模型与功能

百炼平台提供多类大语言模型（如 `qwen4-max`、`qwen2.5-72b`、`qwen-audio` 等）及多模态模型，覆盖文本生成、代码补全、语音理解、图像描述等场景。完整模型列表见 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（function calling）和自定义 system prompt，具体能力以各模型文档为准，例如 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md) 明确支持 tool choice 和 structured output。

> **注意**：[选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档中列出的部分旧版模型（如 `qwen1.5-14b-chat`）已进入维护期，新项目推荐优先选用 `qwen2.5` 或 `qwen4` 系列；该文档未同步标注弃用状态，实际选型请以 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中的“当前推荐”标识为准。

## 关键参数

调用模型时需指定以下必需参数：
- `model`: 模型 ID（如 `"qwen4-max"`），必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中的名称完全一致；
- `messages`: 对话历史数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `temperature` / `top_p`: 控制输出随机性，取值范围均为 `0.0–1.0`（默认 `0.8`）；
- `max_tokens`: 限制响应最大 token 数，不同模型有独立上限（详见各模型文档）。

## 使用方式

1. **API 调用**：使用 HTTPS POST 请求至 `https://dashscope.aliyuncs.com/api/v1/chat/completions`，携带 `Authorization: Bearer <api_key>` 头；
2. **SDK 调用**：推荐使用官方 Python SDK（`dashscope` v1.20.0+），示例：
   ```python
   from dashscope import Generation
   resp = Generation.call(model='qwen4-max', messages=[{'role':'user','content':'你好'}])
   ```
3. **控制台调试**：登录百炼控制台 → 进入「Model Studio」→ 选择模型 → 使用右侧「API 调试」面板实时测试。

## 限制和注意事项

- **地域限制**：模型服务仅在杭州、上海、北京、深圳、新加坡等指定地域可用，详情参见 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)；
- **限流策略**：默认 QPS 为 5，TPM（Tokens Per Minute）为 10,000，超出将返回 `429 Too Many Requests`；具体配额与升降级规则见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- **错误处理**：常见错误码（如 `InvalidParameter`、`ResourceNotFound`）含义及修复建议汇总于 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)，建议在生产环境集成重试与降级逻辑。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


