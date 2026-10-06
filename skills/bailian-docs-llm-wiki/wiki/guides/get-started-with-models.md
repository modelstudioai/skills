# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API 调用基础配置、关键参数设置及常见约束。所有操作均基于标准 RESTful API 接口，无需额外 SDK 即可集成。建议首次使用前通读 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 全文以建立整体认知。

## 支持的模型与核心功能

百炼平台提供多类大语言模型（如 Qwen 系列）、多模态模型及定制化推理服务，支持文本生成、[函数调用](../concepts/function-calling.md)（tool calling）、流式响应、JSON Schema 输出约束等能力。模型列表及能力矩阵详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型还支持系统提示词（`system` role）和多轮对话上下文管理，但并非全部模型均兼容 `tools` 字段 —— 具体支持情况请以该文档中“能力标注”栏为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`: 模型 ID（如 `qwen-max`, `qwen-plus`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的可用值严格一致；
- `input.messages`: 至少包含一条 `user` 角色消息；
- `parameters.temperature`: 浮点数（0.0–1.0），控制输出随机性，默认为 0.8；
- `parameters.top_p`: 浮点数（0.0–1.0），影响 token 采样范围，默认为 0.8。

> **注意**：`parameters.max_tokens` 在部分旧版文档中被误标为必填，实际为可选参数；最新行为以 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的请求示例为准 —— 未指定时由模型自动截断。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`；
2. **Endpoint 构造**：根据部署地域选择 Base URL，例如杭州地域为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；完整域名映射见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
3. **发送请求**：推荐使用 `POST` 方法提交 JSON payload，启用流式响应需添加 `Accept: text/event-stream` 头并解析 SSE 格式；
4. **调试建议**：首次调用推荐从 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供的最小可行示例入手，避免一次性组合过多参数。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含角色标记）不得超过模型 context 长度上限，具体数值参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 表格；
- 动态限流策略由账户配额与实时负载共同决定，[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 和 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 两份文档描述存在口径差异：前者强调按分钟级配额池调度，后者仍沿用固定 QPS 限制表述 —— 实际生效策略以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 为准；
- 所有 API 调用必须指定 `X-DashScope-Region` Header（如 `cn-hangzhou`），否则可能因路由失败返回 400；该要求在 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中明确说明，但部分示例代码遗漏，需手动补全。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


