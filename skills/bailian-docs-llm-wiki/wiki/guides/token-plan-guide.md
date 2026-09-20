# token plan guide

Token Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗总量与速率。开发者可通过 Token Plan 实现细粒度的用量隔离、成本管控和稳定性保障，适用于个人开发、团队协作及生产级服务部署。其核心能力围绕模型调用生命周期中的 token 计量、配额分配与限流策略展开。

## 支持的模型/功能

Token Plan 当前支持所有百炼平台托管的通用大模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及部分专用模型（如 CodeQwen），但**不支持直接应用于自定义训练模型的推理 endpoint**。多模态模型的 token 计算遵循 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 中定义的统一计费规则：文本 token 按标准 UTF-8 编码计数，图像 token 按分辨率分段折算（详见 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)）。Coding Plan 作为独立子计划，仅对代码补全类模型（如 CodeQwen-7B）生效，其配额不可与通用 Token Plan 互通 —— 这一限制在 [原文标题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 中有明确说明。

## 关键参数

- `max_tokens_per_minute`：每分钟最大 token 消耗上限（硬限流阈值），默认值因版本而异，团队版初始值为 100,000；
- `burst_capacity`：突发容量（单位：token），允许短时超额调用，超出后触发 429 响应；
- `model_whitelist`：可选白名单，指定该 Plan 允许调用的模型 ID 列表（如 `qwen-max`, `qwen-plus`），未配置则默认允许全部支持模型；
- `enable_quota_isolation`：启用后，不同 Plan 间 token 消耗完全隔离，互不影响。

> **注意**：文档 `raw/model-user-guide/token-plan-guide/token-plan-team-edition.md` 中将 `burst_capacity` 默认值标为 `5000`，但最新 API 文档（v2.3+）已将其调整为 `0`（即默认禁用突发模式），请以实际 SDK 初始化返回的 schema 为准。

## 使用方式

1. 在控制台「配额管理」页创建 Token Plan，或通过 `/v1/token-plans` REST API 提交 JSON 配置；
2. 将 Plan 绑定至具体 API Key（控制台操作）或在请求 Header 中显式声明：`X-Parameter-Token-Plan-ID: tp-xxx`；
3. 调用模型 API 时，系统自动按输入 + 输出 token 总和扣减对应 Plan 余额，并实时校验 `max_tokens_per_minute` 与 `burst_capacity`。

绑定后无需修改客户端代码，所有符合模型白名单的请求均受控于该 Plan。详细配置示例见 [原文标题](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)。

## 限制和注意事项

- 单个 API Key 最多绑定 3 个 Token Plan（按环境区分：dev/staging/prod），超出需解绑旧 Plan；
- Token 统计延迟 ≤ 2 秒，高并发场景下瞬时超限可能被允许（最终一致性）；
- 删除 Token Plan 后，已绑定的 API Key 将自动回退至账户默认配额，历史用量记录保留 90 天；
- 不支持跨地域（Region）复用 Plan；华东 1 创建的 Plan 无法在华北 2 的 endpoint 上生效。

> **注意**：`token-plan-personal.md` 中提及“个人版支持无限期续订”，但自 2024 年 7 月起，所有免费版 Plan 均强制设置 30 天有效期，续订需手动操作 —— 该变更未同步更新至该文档，以控制台实际策略为准。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


