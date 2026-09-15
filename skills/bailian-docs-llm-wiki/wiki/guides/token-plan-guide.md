# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗总量、分配策略及生命周期。开发者可通过 [Token](../concepts/token.md) Plan 实现细粒度的用量隔离、成本管控和多环境资源调度。本指南聚焦其技术实现逻辑与工程接入要点。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前适用于所有百炼托管的通用大模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及部分插件模型，但**不支持**自定义训练模型（Fine-tuned Model）或私有部署实例的 token 配额绑定。Coding Plan 作为独立子计划，仅限代码生成类任务使用，其配额不可与通用 Token Plan 互换 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。团队版 Token Plan 支持按成员、项目、API Key 多维度分配，而个人版仅支持全局配额 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md)。

## 关键参数

- `plan_id`：必填，Token Plan 的唯一标识符（UUID 格式），创建后不可修改  
- `quota`：整型，单位为千 token（k-token），表示该 Plan 的总配额上限  
- `reset_cycle`：枚举值（`daily` / `weekly` / `monthly`），指定配额重置周期；`weekly` 默认以周一为起始日  
- `grace_period_seconds`：可选，宽限期（秒），超限后允许继续调用的缓冲时间（默认 300）  
- `model_whitelist`：字符串数组，显式声明允许调用的模型 ID（如 `["qwen-max", "qwen-plus"]`），空数组表示不限制  

> **注意**：文档 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中提及 `reset_cycle: "custom"` 已于 v2.3.0 下线，当前仅支持上述三种固定周期，使用该值将导致创建失败。

## 使用方式

1. **创建 Plan**：调用 `POST /v1/token-plans`，传入参数（见上节），返回 `plan_id`  
2. **绑定 API Key**：调用 `PUT /v1/api-keys/{key_id}/token-plan`，指定 `plan_id`  
3. **调用模型时生效**：所有通过该 API Key 发起的 `/v1/chat/completions` 或 `/v1/embeddings` 请求自动计入对应 Plan 配额  
4. **查询用量**：`GET /v1/token-plans/{plan_id}/usage` 返回实时已用 token 数与重置时间戳  

配额检查在请求网关层完成，若超限且无宽限期，直接返回 `429 Too Many Requests` 及 `Retry-After` header。详细调用示例见 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md)。

## 限制和注意事项

- 单个 API Key 最多绑定 1 个 Token Plan；一个 Plan 可绑定多个 API Key（团队版支持跨 Key 共享配额）  
- 配额统计精度为 ±50 token，不保证严格精确到单次请求的 token 数（受分词器差异影响）  
- 删除 Token Plan 后，已绑定的 API Key 将自动回退至账户默认配额（若未设置则为 0），**不会**触发历史用量清零  
- 团队版中，成员被移出团队后，其名下绑定的 Plan 若未转移所有权，将在 7 天后自动解绑并失效  

> **注意**：[团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档中“Plan 可继承父组织配额”的描述已过时；自 v2.4.0 起，所有 Plan 均为独立配额实体，不再支持继承模式。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


