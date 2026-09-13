# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、参数配置、请求调度及售后保障等环节。开发者可通过标准 API 或控制台快速集成，适用于构建对话、内容生成、工具调用等各类 AI 应用场景。该能力依赖平台统一的模型服务网关与权限治理体系，需配合 [应用管理](../../raw/application-user-guide/application-management.md) 和 [API 认证](../../raw/developer-guide/api-authentication.md) 使用。

## 支持的模型/功能

- 支持调用百炼平台全部已上线的**托管模型**（如 Qwen 系列、Qwen-VL、Qwen-Audio）及用户自部署的**私有模型服务**（通过 Model Studio 部署并注册至 Application Center）；
- 提供基础推理能力（`chat` / `completion`）、流式响应（`stream=true`）、[函数调用](../concepts/function-calling.md)（`tools`）、[多模态](../concepts/multi-modal.md)输入（图像 base64 或 URL）；
- 不支持直接调用未在 Application Center 中启用的模型实例，也不支持跨账号模型共享调用 —— 具体权限模型详见 [应用管理](../../raw/application-user-guide/application-management.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID（如 `qwen-max`、`qwen-plus`），必须已在当前应用中授权；ID 列表可通过 `/v1/models` 接口获取 |
| `input` | object | 是 | 请求输入，结构为 `{ "messages": [...] }` 或 `{ "prompt": "..." }`，格式依模型类型而异 |
| `parameters` | object | 否 | 包含 `temperature`、`top_p`、`max_tokens` 等，具体字段以 [模型能力文档](../../raw/model-capabilities/qwen-max.md) 为准 |
| `enable_search` | boolean | 否 | 仅对支持 RAG 的模型生效，启用后自动检索知识库（需提前配置） |

> **注意**：`parameters` 中的 `stop` 字段在部分旧版 SDK 示例中被误标为字符串数组，实际应为字符串（如 `"stop": "\n"`），请以 [应用用户指南](../../raw/application-user-guide/application-support.md) 中的最新接口定义为准。

## 使用方式

1. 在 Model Studio 中完成[模型部署](../concepts/model-deployment.md)或选择托管模型；
2. 进入 Application Center → 创建/编辑应用 → 在「模型接入」页启用目标模型；
3. 调用 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（文本生成）或对应服务路径；
4. 请求头携带 `Authorization: Bearer ${api_key}`，Body 按上述参数格式构造 JSON；
5. 建议使用官方 SDK（Python/Java/Node.js）自动处理签名与重试逻辑，参考 [API 认证](../../raw/developer-guide/api-authentication.md)。

## 限制和注意事项

- 单次请求最大 `input` 大小为 1MB（含图片 base64 编码后长度），超限将返回 `413 Payload Too Large`；
- 流式响应（`stream=true`）下不支持 `tools` 调用，二者不可同时启用；
- 免费额度仅覆盖基础模型调用，Qwen-Max、Qwen-VL 等高性能模型按实际 token 计费，计费规则见 [售后说明](../../raw/application-user-guide/application-support.md)；
- 所有请求受应用级 QPS 与并发数限制，超出时返回 `429 Too Many Requests`，限流策略可在应用详情页查看与调整。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


