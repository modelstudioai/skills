# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗量、设置用量上限并实现精细化成本管控。开发者可通过 [Token](../concepts/token.md) Plan 绑定模型实例、配置额度策略，并在服务级或请求级生效。其行为受模型类型、调用方式及账户版本共同约束。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前支持全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入场景，但不适用于直接调用 `dashscope` 原生 SDK 的裸 API（需通过百炼统一网关入口）。[Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 明确指出：“仅当请求经 `/v1/services/aigc/text-generation/generation` 等百炼标准路由转发时，Token Plan 才被识别和执行”。  
> **注意**：[Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 文档中提及的“支持所有代码补全模型”与当前实际不符——截至 v2024.07，CodeQwen 系列暂未接入 Token Plan 配额校验，该描述已过时。

## 关键参数

- `max_tokens`：单次请求允许消耗的最大 token 数（含 [prompt](prompt.md) + completion），硬性截断阈值  
- `quota`：周期内（默认自然日）总可用 token 配额，超限后返回 `429 Too Many Requests`  
- `burst`：突发容量（单位：token），允许短时超额（需配合 `burst_window_seconds` 使用）  
- `model_id`：必须显式指定，Token Plan 与 model_id 强绑定，不同 model_id 不共享配额  

上述参数定义与语义详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 和 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的 Schema 描述。

## 使用方式

1. 在控制台创建 Token Plan 实例，选择适用模型、设置 `quota` 与 `burst`  
2. 将 Plan ID 绑定至目标模型服务（通过 `/v1/models/{model_id}/bindings` 接口或控制台 UI）  
3. 发起请求时，在 HTTP Header 中携带 `X-DashScope-Token-Plan-ID: <plan_id>`  
   - 若未传 Header，则按账户默认 Plan 或无限制策略执行（取决于账户版本）  
   - 多 Plan 绑定同一 model_id 时，以最先匹配的 Plan 为准（按创建时间排序）  

完整示例与调试方法见 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中的「快速上手」章节。

## 限制和注意事项

- Token Plan 不支持跨 region 生效；华东1（杭州）创建的 Plan 无法在华北2（北京）调用中生效  
- `burst` 机制仅对连续高频请求有效，单次请求仍受 `max_tokens` 限制，不可绕过  
- 团队版账户下，子成员继承父团队的 Token Plan 配置，但无法独立修改 quota（权限隔离），详情参见 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)  
- 所有 token 计算均基于百炼内部 tokenizer（非 HuggingFace 或原生模型 tokenizer），实际计数可能与本地估算存在 ±5% 偏差

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


