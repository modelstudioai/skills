# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解支持的模型类型、关键调用参数、标准使用流程，以及生产环境中的限制与注意事项。所有操作均基于 RESTful API，无需安装额外 SDK 即可开始。

## 支持的模型与核心功能

百炼平台提供多类预训练大语言模型（如 Qwen 系列）及部分多模态模型，支持文本生成、对话理解、代码补全等通用能力。模型按能力、尺寸和部署形态分为 `qwen-max`、`qwen-plus`、`qwen-turbo` 等规格，具体列表详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。此外，平台支持动态限流策略与地域级服务路由，便于构建高可用应用。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `"qwen-turbo"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：非空消息数组，首条消息 `role` 应为 `"user"`；
- `parameters.temperature`：控制输出随机性（0.0–2.0），默认为 1.0；
- `parameters.top_p`：核采样阈值（0.0–1.0），与 `temperature` 互斥推荐使用其一；
- `base_url`：需根据部署地域选择，参见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 和 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

> **注意**：[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档中描述的每分钟请求数（RPM）限制已过时；当前实际执行策略以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 中定义的配额组为准，该机制支持按 [Token](../concepts/token.md) 数动态计算消耗。

## 使用方式

1. **获取 API Key**：在百炼控制台「API 密钥管理」中创建并复制密钥；
2. **构造请求**：使用 `POST /v1/chat/completions`，Header 设置 `Authorization: Bearer <your_api_key>`；
3. **发送调用**：参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的 cURL 示例完成验证；
4. （可选）集成地域路由逻辑，确保请求命中就近节点。

## 限制和注意事项

- 单次请求 `input.messages` 总长度不得超过 32768 tokens（含 system prompt）；
- 响应超时默认为 60 秒，长上下文或复杂推理任务建议客户端设置更长 timeout；
- 免费试用额度仅适用于 `qwen-turbo` 和 `qwen-plus`，`qwen-max` 需绑定付费账号；
- 所有模型不支持自定义 LoRA 或微调权重上传，仅开放推理接口；
- 模型版本升级可能带来输出格式微调（如 `finish_reason` 字段值变化），建议在生产环境中锁定 `model` 版本标识（如 `qwen-turbo-20240801`），而非使用别名。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


