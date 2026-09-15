# token plan guide

Token Plan 是百炼平台为模型调用设计的配额管理机制，用于控制 API 请求的 token 消耗额度与使用节奏。它支持按模型、场景和用户角色精细化分配资源，并与计费体系深度集成。开发者需理解其参数含义与约束条件，以避免调用中断或配额误配。

## 支持的模型/功能

Token Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入通道。基础功能包括：按日/月周期配额分配、突发流量弹性扩容（需开启 burst mode）、多模型共享池配置。高级功能如模型级 token 限额、跨账号 token 转移，仅在[团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)中提供；个人开发者应参考[个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md)文档确认可用能力。

## 关键参数

- `quota`: 周期总配额（单位：token），支持整数或科学计数法（如 `1e6`）  
- `burst_ratio`: 突发倍率（默认 `1.5`），最大不超过 `3.0`；超出将触发 `429 Too Many Requests`  
- `model_whitelist`: 白名单模型 ID 列表（如 `qwen-max`, `qwen-plus`），空值表示允许全部模型  
- `enforce_mode`: 启用严格模式（`strict`）时，超限请求立即拒绝；设为 `soft` 时允许短时超额（最多 +5% 且持续 ≤30s）  
> **注意**：`enforce_mode=soft` 的行为在[进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)中被标记为“已弃用”，实际生效逻辑以最新 API 文档为准。

## 使用方式

通过 `/v1/token-plans` 接口创建或更新计划，请求体为 JSON 格式：

```json
{
  "name": "prod-qwen-plus-daily",
  "quota": 500000,
  "burst_ratio": 2.0,
  "model_whitelist": ["qwen-plus"],
  "enforce_mode": "strict"
}
```

创建后，需在调用模型 API 的 `X-Task-ID` 或 `X-Plan-ID` 请求头中显式指定 plan ID（详见[Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)）。不指定 plan 的请求将走默认配额池。

## 限制和注意事项

- 单 plan 最大 `quota` 为 `1e9` token/周期；单次请求消耗超过 `1e6` token 将被拦截  
- `burst_ratio` 修改后需 60 秒同步生效，期间新旧策略可能并存  
- 同一账号下所有 plan 的 `model_whitelist` 不可重叠，否则创建失败  
- 团队版中子账号继承父账号 plan 配置，但无法修改 `quota` 和 `burst_ratio` —— 此限制未在[个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md)中说明，属团队版特有行为

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


