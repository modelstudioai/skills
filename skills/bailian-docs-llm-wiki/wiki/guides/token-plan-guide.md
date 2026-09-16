# token plan guide

Token Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用量、保障服务稳定性并支持按需弹性伸缩。开发者可通过 Token Plan 统一分配和监控不同模型、环境或团队的调用额度。其设计兼顾灵活性与可审计性，适用于个人开发、团队协作及生产级部署场景。

## 支持的模型/功能

Token Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型），并支持以下核心能力：  
- 按模型 ID 或模型别名（如 `qwen-max`）设置独立配额  
- 区分同步调用（`/v1/chat/completions`）与异步任务（`/v1/batch`）的额度控制  
- 与百炼工作区（Workspace）权限体系深度集成，支持子账号继承父级 Plan 配置  
详细支持列表请参见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 关键参数

创建或更新 Token Plan 时需指定以下必填/关键字段：  
- `model`: 字符串，模型标识（如 `qwen-plus`），支持通配符 `*` 表示全部模型（仅限企业版）  
- `limit`: 整数，单位为千 tokens/日（例如 `500` 表示每日 50 万 tokens）  
- `window`: 字符串，时间窗口类型，仅支持 `"day"`（不支持 `"hour"` 或 `"month"`，该限制在 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中有明确说明）  
- `scope`: 字符串，作用域，可选 `"user"`（当前账号）、`"workspace"`（当前工作区）或 `"team"`（团队版专属）  
> **注意**：原始文档中 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 提到 `window: "hour"` 为合法值，但该描述已过时；实际 API 仅接受 `"day"`，否则返回 `400 Bad Request`。

## 使用方式

1. **创建 Plan**：调用 `POST /v1/token-plans`，传入 JSON body（含 `model`, `limit`, `window`, `scope`）  
2. **绑定调用**：在请求 Header 中添加 `X-Token-Plan-ID: <plan_id>` 即可启用配额校验  
3. **查询用量**：调用 `GET /v1/token-plans/{id}/usage?date=2024-06-01` 获取指定日期用量  
完整示例与错误码说明见 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md)。

## 限制和注意事项

- 单个 Plan 仅能绑定一个 `model`（不支持多模型聚合配额）  
- 配额按自然日（UTC+8）重置，不可跨日累计或借用  
- 若未显式指定 `X-Token-Plan-ID`，请求将走默认无配额通道（受全局速率限制约束）  
- 团队版用户需通过 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档了解成员继承规则与管理员审批流  
> **注意**：`Coding Plan` 是 Token Plan 的专用子集，仅适用于 `/v1/coding` 接口，其配额不与通用模型 Plan 互通；相关细节请参考 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


