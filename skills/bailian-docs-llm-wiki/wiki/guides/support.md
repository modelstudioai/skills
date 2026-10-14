# support

`support` 是百炼平台为模型调用和服务使用提供的基础支持能力，涵盖模型兼容性、服务范围、售后保障及合规协议等内容。开发者可通过该模块确认所选模型是否受支持、了解服务边界与限制，并获取故障排查和问题反馈路径。所有支持策略均以 [服务支持](../../raw/model-user-guide/support.md) 为准。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包括通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型。
- 功能支持覆盖同步推理（`/v1/chat/completions`）、异步任务（`/v1/async-tasks`）、批量推理（`/v1/batch`）及模型微调结果部署后的在线服务调用。
- 模型能力边界（如上下文长度、输入格式、多模态支持）需以各模型专属文档为准，例如 Qwen-VL 的图像解析限制见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中对应条目。

## 关键参数

- `model`：必需，值必须严格匹配 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中公布的模型 ID（区分大小写与连字符，如 `qwen-max` ≠ `qwen_max`）。
- `enable_search` / `enable_retrieval`：仅部分模型支持，启用前须确认该模型在 [服务支持](../../raw/model-user-guide/support.md) 的“功能矩阵”中明确标注为支持。
- `stream`：设为 `true` 时需按 SSE 协议解析响应；若模型不支持流式（如部分旧版微调模型），API 将返回 `400 Bad Request`，错误码为 `UnsupportedStreamMode`。

## 使用方式

- 所有支持模型均通过统一 API 网关调用，鉴权方式为 Bearer [Token](../concepts/token.md)（`Authorization: Bearer <api_key>`），无需额外配置 endpoint。
- 售后问题提交路径：控制台 →「帮助中心」→「提交工单」，或直接访问 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 查看服务等级协议（SLA）与响应时效。
- 协议与合规要求（如数据不出域、商用授权范围）请务必查阅 [相关协议](../../raw/model-user-guide/support/related-agreements.md)，未签署即调用可能触发服务拦截。

## 限制和注意事项

- 免费试用额度仅适用于 [服务支持](../../raw/model-user-guide/support.md) 明确标注“开放试用”的模型；Qwen3 系列自 2024年7月起已取消通用免费额度，需绑定计费项。
- > **注意**：[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中关于“历史模型永久免费”的描述已过时，实际以 [服务支持](../../raw/model-user-guide/support.md) “计费说明”章节为准。
- 单次请求最大 token 数受模型本身限制（如 `qwen-turbo` 为 8K，`qwen-max` 为 32K），超出将被截断并返回警告头 `X-Warning: input_truncated`，**不会自动降级到其他模型**。
- 跨地域调用（如华东1区 AK 调用华北2区部署的私有模型）不受支持，必须确保 API 请求区域与模型部署区域一致。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


