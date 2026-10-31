# Token 管理

Token 管理是百炼平台对模型调用过程中输入与输出文本所消耗的 token 资源进行计量、配额控制、监控与治理的核心机制。它贯穿 API 调用生命周期，支撑成本可控、资源隔离、灰度发布与生产可观测性等关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **配额控制（Token Plan）**：通过 `Token Plan` 为不同业务线、环境或团队分配独立的 token 消耗上限（`max_tokens_per_minute`）和突发容量（`burst_ratio`），实现资源硬隔离。Plan 通过 `X-BC-Plan-ID` 请求头或请求体参数生效，与 API Key 权限体系深度协同，适用于个人开发、团队协作及企业级多租户场景。

- **身份与访问治理（Token Plan API）**：Token 管理的组织层能力由 Token Plan API 提供支撑——席位（`SeatType: standard/pro/max`）本质是 token 消耗权限的载体，每个席位绑定特定规格的月度 Credits 额度；API 支持批量分配/回收席位、查询剩余额度（`SeatRemainingCredits`）、校验成员席位状态，实现基于角色的 token 资源分发与审计。

- **调用初始化与安全约束（Preparations）**：`api_key` 是 token 消耗的身份凭证，其生命周期、QPS 限流（默认 5 QPS）及泄露防护（禁止硬编码、推荐环境变量注入）均属于 Token 管理的基础安全边界。未携带有效 `api_key` 或超出配额的请求将被拒绝并返回 `429 Too Many Requests`。

- **可观测与闭环优化（Model Monitoring）**：所有模型调用的 `TotalToken 数`（含 input + output）被实时采集为监控指标，支持按业务空间、API Key 维度查看、告警（如“TotalToken 数突增”）及对账。审计日志记录每次调用的 token 消耗量与状态码，推理日志（需手动开启）则可关联具体 prompt/response 进行 token 效率分析。

## 关键参数和配置

| 参数名 | 所属模块 | 说明 | 是否必填 | 典型值示例 |
|---------|-----------|------|-----------|-------------|
| `plan_id` | Token Plan | Plan 唯一标识符，用于路由配额策略 | 是 | `team-prod-v2`, `coding-staging` |
| `max_tokens_per_minute` | Token Plan | 每分钟最大允许消耗 token 总数（input+output） | 是 | `10000`, `50000` |
| `burst_ratio` | Token Plan | 突发系数（1.0–3.0），允许短时超额，超限后返回 429 | 否（企业/团队版默认启用） | `2.0`, `2.5` |
| `model_whitelist` | Token Plan | 显式限定可调用的模型 ID 列表，未设置则继承 Plan 绑定范围 | 否 | `["qwen-max", "qwen-plus"]` |
| `SeatType` | Token Plan API | 席位规格，决定每月 token Credits 额度等级 | 是（分配时） | `"standard"`, `"pro"`, `"max"` |
| `SeatRemainingCredits` | Token Plan API | 当前席位剩余可用 token 额度（监控/告警依据） | 只读返回 | `1248000` |
| `TotalToken 数` | Model Monitoring | 单次调用实际消耗的 token 总量（监控告警核心指标） | 只读统计 | `1842` |

> ⚠️ 注意：  
> - `burst_ratio` 配置变更后，burst 缓存可能延迟 1–2 分钟生效；  
> - `plan_id` 与 `api_key` 必须匹配所属组织上下文，跨组织使用将触发鉴权失败；  
> - `TotalToken 数` 是监控口径（含所有调用类型），与计费口径的「模型用量」数据分离，不可混用对账。

## 面向开发者，简洁实用

- ✅ **快速上手**：在请求 Header 中添加 `X-BC-Plan-ID: your-plan-id`，即可启用配额控制；无需修改业务逻辑。  
- ✅ **安全第一**：永远通过环境变量（如 `DASHSCOPE_API_KEY`）注入密钥，Never hardcode `api_key` 或 `plan_id` 到前端代码。  
- ✅ **排查 429**：先查 Model Monitoring 的「限流错误次数」和「TotalToken 数」趋势，再核对对应 `plan_id` 的 `max_tokens_per_minute` 是否已满。  
- ✅ **调试建议**：启用 SDK DEBUG 日志（`logging.basicConfig(level=logging.DEBUG)`），直接观察请求中 `X-BC-Plan-ID` 是否正确透传、响应头是否含 `X-RateLimit-Remaining`。  
- ✅ **企业实践**：用 Token Plan API 自动化席位分配 + Webhook 告警（当 `SeatRemainingCredits < 10%` 时通知运维），实现 token 资源自治闭环。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [model monitoring](../guides/model-monitoring.md)


