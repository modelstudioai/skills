# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API 调用基础配置、关键参数设置及常见约束。适用于首次集成千问（Qwen）等大模型的开发场景，无需部署模型即可通过标准 HTTP 接口调用。所有操作均基于百炼统一 API 网关，需提前完成身份认证与配额配置。

## 支持的模型与核心功能

百炼平台当前支持 Qwen 系列大语言模型（如 qwen-max、qwen-plus、qwen-turbo），以及部分多模态和推理优化模型。模型能力覆盖文本生成、代码补全、结构化输出（JSON Schema）、流式响应等。完整模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态限流与静态配额管理能力已集成至统一控制面，具体策略请参考 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 和 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `"qwen-turbo"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：非空消息数组，首条消息 `role` 应为 `"user"`；
- `parameters.temperature`：建议范围 0.0–1.0，设为 `0` 可启用确定性输出（注意：部分旧版文档未明确此行为，实际以 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 示例为准）；
- `parameters.stream`：布尔值，启用流式响应需显式设为 `true`。

> **注意**：`base_url` 不再硬编码为固定域名；自 2024 年 Q3 起，所有请求必须使用 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 中按地域动态生成的接入地址，旧文档中“默认使用 https://dashscope.aliyuncs.com/api/v1” 已过时。

## 使用方式

1. 获取 API Key（通过百炼控制台 → API 密钥管理）；
2. 根据目标地域选择对应 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中的 endpoint；
3. 构造 POST 请求，Header 包含 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；
4. Body 示例（同步调用）：
```json
{
  "model": "qwen-turbo",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.7}
}
```

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为 32768（具体依模型而异，以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 页标注为准）；
- 免费试用额度仅限新用户首次开通后 30 天内使用，超出后需绑定支付方式并配置配额；
- 流式响应（`stream=true`）下，`output.text` 字段在最终 chunk 中才完整返回，中间 chunk 的 `output.text` 为增量片段；
- 同一 API Key 在单地域内默认共享 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 配额，跨地域调用需分别配置。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


