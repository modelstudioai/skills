# token plan guide

Token Plan 是百炼平台为模型调用设计的配额管理机制，用于控制 API 请求的 token 消耗额度与计费粒度。开发者可通过 Token Plan 实现细粒度的用量管控、成本预估和多环境资源隔离。该机制适用于所有支持按 token 计费的模型调用场景。

## 支持的模型/功能

Token Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入通道（需开启 `enable_token_plan` 标志）。不支持仅按请求次数计费的旧版模型（如早期 `qwen-1.8b-chat` 免费试用版）。[Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 明确指出：“Token Plan 与模型版本强绑定，v2.3+ 接口默认启用”。

> **注意**：[个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 文档中提及“支持所有模型”，但该描述已过时；实际以 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中的模型兼容性列表为准。

## 关键参数

- `token_plan_id`：必填，Token Plan 唯一标识符（如 `tp-abc123`），在控制台创建后分配  
- `quota`：单次请求允许消耗的最大 token 数（整数，≥100），超限将返回 `429 Too Many Tokens`  
- `burst_quota`：突发配额（默认为 `quota × 2`），用于应对短时高峰，不可持续使用  
- `reset_interval_seconds`：配额重置周期（支持 60、300、3600 秒），需与业务调用节奏对齐  

参数配置需通过 `/v1/token-plans/{id}` 接口或控制台完成，详见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)。

## 使用方式

1. 在控制台「配额管理」中创建 Token Plan，指定 `quota` 和 `reset_interval_seconds`  
2. 调用模型 API 时，在请求 Header 中添加：  
   ```http
   X-Token-Plan-ID: tp-abc123
   ```  
3. 若需动态覆盖配额，可额外传入 Query 参数：  
   `?override_quota=5000&override_burst_quota=10000`（仅限具备 `token_plan:override` 权限的 AK）

完整示例见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 的「HTTP 调用节」。

## 限制和注意事项

- 单个账号最多创建 50 个 Token Plan；单个 Plan 最大 `quota` 为 1,000,000 tokens  
- 不支持跨 Region 复用（如杭州 region 创建的 Plan 无法在北京 region 使用）  
- `burst_quota` 仅在连续 3 个重置周期内累计未超限的前提下生效；否则触发硬限流  
- 与 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 互斥：同一请求不可同时指定 `X-Token-Plan-ID` 和 `X-Coding-Plan-ID`  

> **注意**：[玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中推荐的“多 Plan 轮询策略”在高并发下可能导致配额抖动，建议优先采用 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 提供的异步配额预检方案。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


