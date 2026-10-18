# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗量、设置用量上限并实现精细化成本管控。开发者可通过 [Token](../concepts/token.md) Plan 绑定模型实例、分配额度、监控消耗，并支持按个人或团队维度灵活配置。该机制适用于所有通过百炼 API 接入的模型服务，是生产环境稳定调用的关键基础设施。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等）均支持 [Token](../concepts/token.md) Plan 配额绑定  
- 支持同步推理（`/v1/chat/completions`）、异步任务（`/v1/batch`）、流式响应（`stream=true`）等调用方式  
- 支持多模型共用同一 Token Plan（需在创建时显式声明 `model_ids`），但不支持跨版本混用（如 `qwen-max-20240601` 与 `qwen-max` 视为不同模型）  
- Coding Plan 作为独立子类，提供额外的代码生成专属配额与审计能力，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `plan_id` | string | 是 | Token Plan 唯一标识，由平台分配或自定义（需全局唯一） |
| `quota` | integer | 是 | 总配额（单位：token），最小值为 1000，最大值依版本而定（团队版最高支持 10M/日） |
| `reset_cycle` | string | 否 | 重置周期，可选 `"daily"`（默认）、`"weekly"`、`"monthly"` |
| `model_ids` | string[] | 否 | 绑定的模型 ID 列表；若为空，则默认绑定当前账号下所有已授权模型 |
| `enable_alert` | boolean | 否 | 是否开启用量超 80% 邮件告警（仅对主账号生效） |

> **注意**：原始文档中 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 将 `reset_cycle` 描述为“仅支持 daily”，但最新 API 文档已明确支持 `weekly` 和 `monthly` —— 请以 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的参数定义为准。

## 使用方式

1. **创建 Plan**：调用 `POST /v1/token-plans`，传入 `quota`、`reset_cycle` 等参数  
2. **绑定模型实例**：在创建模型服务（`POST /v1/models`）时，通过 `token_plan_id` 字段关联；或对已有实例调用 `PATCH /v1/models/{model_id}` 更新绑定关系  
3. **查询用量**：调用 `GET /v1/token-plans/{plan_id}/usage` 获取实时 token 消耗、剩余配额及重置时间  
4. **动态调整**：支持运行时修改 `quota`（立即生效）和 `reset_cycle`（下次重置周期起生效），无需重启模型实例  

示例（curl）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/token-plans \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"quota": 50000, "reset_cycle": "daily", "model_ids": ["qwen-plus"]}'
```

## 限制和注意事项

- 单个 Token Plan 最多绑定 20 个模型 ID；超出需拆分多个 Plan  
- 配额按自然日（UTC+8）重置，非按 24 小时滚动；重置时刻不可配置  
- 流式响应（stream）的 token 计费以实际返回的完整 token 数为准，**不按 chunk 预占**  
- 若模型未显式绑定 Token Plan，则使用账号默认 Plan（个人版默认为 `personal-default`，团队版需管理员预设）  
- 删除 Token Plan 前，必须解绑所有关联模型实例，否则返回 `409 Conflict` 错误；该约束在 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 和 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档中一致明确。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


