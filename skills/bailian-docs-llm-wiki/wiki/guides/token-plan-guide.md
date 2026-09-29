# token plan guide

Token Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗总量、分配使用权限并支持多层级（个人/团队）配额隔离。开发者需根据模型类型、输入输出长度及调用频次合理规划 token 配额，避免因超限导致请求失败。该机制贯穿模型调用全链路，与鉴权、限流、计费深度耦合。

## 支持的模型/功能

Token Plan 当前覆盖百炼全部公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分定制模型，但不适用于离线批量推理任务或本地部署模型。所有在线同步/异步 API 调用（如 `/v1/chat/completions`、`/v1/embeddings`）均受其约束。Coding Plan 作为独立子计划，专用于代码生成类模型（如 Qwen-Coder），其 token 计量规则与通用 Token Plan 分离，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `token_quota`: 总配额上限（单位：千 token），按自然月重置  
- `token_used`: 当前已消耗量（实时可查，精度至 1 token）  
- `model_id`: 绑定模型标识，决定 token 折算系数（例如 Qwen2-72B 的 input token 按 1:1 计，output token 按 1:1.5 折算）  
- `quota_scope`: 取值为 `personal` 或 `team`，影响配额继承与共享逻辑，具体策略参见 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)

> **注意**：原始文档中 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 提到“output token 默认按 1:1 折算”，但最新模型 SDK v3.2+ 已统一采用动态系数（依据模型上下文长度与架构自动计算），请以实际返回的 `x-bailian-token-used` 响应头为准。

## 使用方式

1. 在控制台「配额管理」页创建 Token Plan 实例，指定 `quota_scope` 和初始 `token_quota`  
2. 调用 API 时在请求头携带 `X-Bailian-Token-Plan-ID: <plan_id>`  
3. 若未显式指定，系统按用户身份自动匹配默认 Plan（个人版优先于团队版）  
4. 配额超限时返回 HTTP 429，响应体含 `{"error": {"code": "QUOTA_EXCEEDED", "message": "...}}"` —— 此行为与 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 文档一致

## 限制和注意事项

- 单次请求 output token 不得超过模型最大 context 长度的 50%（硬限制，不可绕过）  
- Token Plan 不支持跨 region 共享，华东1区创建的 Plan 无法在华北2区生效  
- 修改 `token_quota` 后立即生效，但 `token_used` 不重置；若需清零，须新建 Plan 并迁移流量  
- 个人版 Plan 无法降级为免费额度，团队版成员退出后其历史 token 消耗仍计入团队总量 —— 这一行为在 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 与 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档中描述一致，无冲突

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


