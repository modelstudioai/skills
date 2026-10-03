# token plan guide

Token Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗额度、分配策略及生命周期。开发者可通过 Token Plan 实现细粒度的用量隔离、成本管控和多环境资源调度。该机制适用于所有支持按 token 计费的模型服务。

## 支持的模型/功能

- 当前支持全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入（需开启 `enable_third_party` 配置）  
- 支持同步推理（`/v1/chat/completions`）、异步任务（`/v1/async/tasks`）、批量处理（`/v1/batch/invoke`）三种调用模式  
- 仅限 HTTP API 调用生效；SDK v3.2.0+ 默认启用 Token Plan 校验，旧版 SDK 需显式传入 `plan_id` 参数 —— 具体兼容性请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `plan_id` | string | 是 | Token Plan 唯一标识，创建后不可修改；可在控制台「配额中心」获取 |
| `model` | string | 是 | 显式声明调用模型（如 `qwen-max`, `qwen-plus`），必须与 Plan 绑定模型一致 |
| `max_tokens` | integer | 否 | 单次请求最大生成 token 上限，受 Plan 的 `per_request_limit` 约束 |
| `priority` | integer | 否 | 优先级（1–100），影响队列调度顺序；默认为 50 |

> **注意**：`priority` 参数在 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中被标记为“仅团队版生效”，但 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 文档明确指出个人版 v2.1+ 已支持该字段。建议以控制台实际行为为准，或升级至 SDK v3.4.0+。

## 使用方式

1. **创建 Plan**：在控制台「配额中心 → Token Plan」新建计划，选择模型、设置总配额（`total_quota`）、单请求上限（`per_request_limit`）及有效期  
2. **绑定调用**：在请求 Header 中添加 `X-Plan-ID: <plan_id>`，或在 JSON Body 中传入 `plan_id` 字段（二者任选其一）  
3. **监控用量**：通过 `/v1/plans/{plan_id}/usage` 接口实时查询剩余配额，响应含 `used_tokens`、`reset_time` 等字段  

示例请求：
```http
POST https://dashscope.aliyuncs.com/api/v1/chat/completions
Authorization: Bearer YOUR_API_KEY
X-Plan-ID: pln-abc123xyz
Content-Type: application/json
```

## 限制和注意事项

- 单个 Plan 最多绑定 5 个不同模型（跨模态模型如 `qwen-vl` 视为独立模型）  
- Plan 生效延迟 ≤ 3 秒，新创建或更新后需等待缓存刷新；紧急场景可调用 `/v1/plans/{plan_id}/refresh` 强制同步  
- 若请求未携带 `plan_id` 或 `X-Plan-ID`，系统将回退至账户级默认配额，**不触发 Token Plan 计费逻辑** —— 详见 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md)  
- Coding Plan 为独立子类型，需使用专用 endpoint `/v1/coding/completions` 并指定 `coding_plan_id`，不兼容通用 `plan_id` 字段

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


