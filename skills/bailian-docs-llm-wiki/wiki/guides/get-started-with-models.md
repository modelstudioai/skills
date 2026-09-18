# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API 接口，无需额外 SDK 即可集成。

## 支持的模型与核心功能

百炼平台提供多种开源与自研大模型，包括 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、通义万相、通义听悟等多模态模型。模型能力覆盖文本生成、代码补全、多轮对话、图像理解与生成等场景。具体模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态限流与配额管理能力已集成至统一控制面，支持按 Token 或请求数进行细粒度调控，详情参见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `qwen-max`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：非空消息数组，首条消息 `role` 应为 `"user"`；
- `parameters.temperature`：取值范围 `[0.0, 2.0]`，默认 `1.0`；  
- `parameters.top_p`：取值范围 `[0.0, 1.0]`，默认 `1.0`；  
- `parameters.max_tokens`：最大输出 token 数，不同模型有硬性上限（如 qwen-turbo 最高支持 8192）。

> **注意**：部分旧文档中 `top_k` 被列为可选参数，但当前所有公开模型接口已**移除对该参数的支持**，实际请求中传入将被忽略——请以 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的示例为准。

## 使用方式

1. 获取 API Key（通过百炼控制台 → API 密钥管理）；  
2. 构造 HTTP POST 请求，`Content-Type: application/json`，Body 包含 `model` 和 `input` 字段；  
3. Base URL 需根据所选地域确定，例如华东1（杭州）为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；完整域名映射关系见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；  
4. 发起请求并解析 JSON 响应中的 `output.text` 或 `output.choices[0].message.content`。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system [prompt](prompt.md)）不得超过模型上下文窗口的 95%（例如 qwen-max 上下文为 32768 tokens，则输入建议 ≤ 31130 tokens）；  
- 所有模型均强制启用限流，未配置配额的账号默认使用公共流控策略，详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；  
- 地域选择影响延迟与合规性：若未显式指定 `X-DashScope-Region` Header 或在请求中声明 region，系统将依据接入域名自动路由，可能导致跨地域调用失败——务必参考 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 进行显式配置。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


