# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、功能扩展、参数配置及售后保障等环节。开发者可通过该支持体系快速集成和调试应用，确保生产环境稳定运行。具体能力与约束详见下文。

## 支持的模型/功能

当前 `application support` 支持所有已在 [百炼控制台「模型服务」页](https://dash.aliyun.com/model-studio) 上线的托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方授权模型），并提供标准 API 调用、异步任务提交、流式响应、回调通知等核心功能。不支持直接调用未在控制台启用的私有微调模型实例——此类实例需通过 [模型部署服务](../../raw/application-user-guide/model-deployment.md) 单独发布后方可接入。部分旧版文档中提及的“本地模型直连”能力已下线，详见 [服务支持](../../raw/application-user-guide/application-support.md) 中的协议范围说明。

## 关键参数

调用 `application support` 接口时，必需参数包括：  
- `app_id`（应用唯一标识，由控制台生成）  
- `model_id`（必须为控制台已启用的服务模型 ID，不可使用训练任务 ID）  
- `input`（结构化输入，格式依模型类型而异；文本类模型要求 `{"messages": [...]}`，多模态模型需按 [服务支持](../../raw/application-user-guide/application-support.md) 规范组织 `images`/`audio` 字段）  
- `parameters.temperature` 等推理参数仅在模型支持时生效，具体可配项以 [模型能力清单](../../raw/application-user-guide/model-capabilities.md) 为准。

> **注意**：`stream` 参数设为 `true` 时，部分小模型（如 qwen-turbo）可能返回非标准 SSE 格式，建议客户端兼容 `data:` 前缀缺失场景；该行为与 [服务支持](../../raw/application-user-guide/application-support.md) 中描述的“全模型统一流式协议”存在偏差，属已知兼容性问题，将在 v2.4.0 版本修复。

## 使用方式

1. 在百炼控制台创建应用，获取 `app_id` 并绑定目标模型；  
2. 调用 `POST /v1/applications/{app_id}/chat/completions`（同步）或 `/v1/applications/{app_id}/tasks`（异步）；  
3. 携带合法 `Authorization: Bearer <api_key>` 头，`api_key` 需具备对应应用的 `AppInvoke` 权限。  
完整请求示例与错误码说明见 [服务支持](../../raw/application-user-guide/application-support.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含文本、Base64 图片、音频等）；  
- 异步任务最长保留 7 天，超期自动清理；  
- 免费额度仅覆盖基础模型调用，Qwen-VL/Qwen-Audio 等多模态模型按实际 token + media unit 计费；  
- 应用级限流默认为 10 QPS，如需提升，请提交工单申请，审批依据见 [售后说明](https://help.aliyun.com/zh/model-studio/application-after-sales-service-scope)。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


