# Token 管理

Token 管理是百炼平台对模型调用过程中 token 消耗进行计量、配额控制、速率限制与成本归因的核心机制，贯穿 API 调用、组织治理与计费结算全链路。它不直接参与模型推理逻辑，而是作为资源层的“计量器”和“闸门”，确保调用行为可度量、可隔离、可预算、可审计。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用场景（实时/流式/批量推理）**：通过 `x-ak` + 可选 `x-token-plan-id` 请求头，将每次请求的输入 token、输出 token（含 content、tool_calls、stop_reason 等全部生成内容）实时计入对应 Token Plan 的月度总量与每秒速率配额。超额即返回 `429 Too Many Requests`，实现细粒度用量隔离与稳定性保障。  
- **组织级资源治理场景**：Token Plan API 提供席位（seat）、订阅、成员角色等管理能力，使 Token Plan 成为团队协作的资源载体——例如为不同业务线分配独立 Plan，或为测试成员分配低配额 Plan，再通过 API 批量绑定/回收席位，实现自动化配额调度。  
- **计费与成本控制场景**：Token 是百炼统一的计费原子单位。免费额度（100 万 Token/模型/90 天）、按量付费（¥X/百万 Token）、节省计划、TPM 预留等均以 token 消耗量为结算依据；预算管理、用量洞察、账单明细也全部基于 token 统计聚合，支持按 AK、Plan、模型、时间多维下钻分析。  
- **不适用场景**：Token 管理**不覆盖**模型微调（fine-tuning）、向量检索（RAG）、PAI-DSW 训练任务、OSS 存储等非标准 API 调用；此类服务需单独配置 Coding Plan 或使用其他计费体系。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必填 |
|------|------|------|------|----------|
| `x-ak` | HTTP Header | string | 百炼 AccessKey ID，用于身份鉴权及配额归属（决定默认 Token Plan） | 是 |
| `x-token-plan-id` | HTTP Header | string | 显式指定 Token Plan ID；若未传，系统按 AK 所属组织层级（团队 > 个人）自动匹配默认 Plan | 否 |
| `x-rate-limit-policy` | HTTP Header | string | 限速策略：`burst`（允许短时突发，适合交互式请求）或 `smooth`（匀速消耗，适合后台批处理），默认 `burst` | 否 |
| `api_key` | HTTP Header (`Authorization: Bearer <api_key>`) | string | 通用认证凭证，用于基础调用与免费额度抵扣；**与 Token Plan 无绑定关系**，不可替代 `x-ak` 实现配额控制 | 是（基础调用） |

> ⚠️ 注意：`x-token-plan-id` 自 v3.2+ API 起生效，旧版 `x-plan-id` 已废弃；`api_key` 和 `x-ak` 是两类独立凭证——前者用于认证与免费额度，后者用于 Token Plan 配额管控，生产环境建议**同时携带两者**以兼顾安全与治理。

## 面向开发者，简洁实用

- ✅ **快速启用**：控制台「配额管理」→「Token Plan」新建 Plan → 绑定 AK → 在请求头添加 `x-ak` 即可生效。  
- ✅ **调试技巧**：流式响应中 token 统计以服务端实际返回为准；可通过 `/v1/usage`（需 AK 权限）查询当前 Plan 的实时用量与剩余配额。  
- ✅ **最佳实践**：  
  - 生产环境务必显式传 `x-token-plan-id`，避免因组织层级变更导致配额漂移；  
  - 高并发服务优先选用 `x-rate-limit-policy: smooth`，防止突发流量触发限流；  
  - 免费额度仅对 `api_key` 调用生效，若需用 Token Plan 管控，必须使用 `x-ak`；  
  - Token Plan 不影响单次请求上限（由模型上下文窗口决定），仅约束总量与速率。  
- ❌ **避坑提示**：不要混用 `api_key` 和 `x-ak` 的语义——前者是“我能调用”，后者是“我用谁的额度调用”；未传 `x-ak` 的请求不会计入任何 Token Plan，也无法享受 Plan 级限速与用量隔离。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [test 1](../guides/test-1.md)


