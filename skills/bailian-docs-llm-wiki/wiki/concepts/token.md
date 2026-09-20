# Token 计量与配额

Token 计量与配额是百炼平台对模型调用资源进行精细化管控的核心机制，指系统按实际消耗的输入与输出 token 总量进行实时统计，并依据预设的配额策略（如速率上限、突发容量、模型白名单等）实施动态限流与用量隔离。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用控制**：每次模型请求（含文本、图像、音频等多模态输入）均触发 token 计量，系统自动计算 `input_tokens + output_tokens` 总和，从绑定的 Token Plan 中实时扣减，并校验 `max_tokens_per_minute` 与 `burst_capacity`。超限即返回 `429 Too Many Requests`，响应头中包含 `X-RateLimit-Remaining` 和 `Retry-After` 供客户端退避。
- **多环境/团队协作**：通过为不同 API Key 绑定独立 Token Plan（如 dev/staging/prod），实现开发、测试、生产环境间的用量完全隔离；团队版支持按成员分配席位（`standard`/`pro`/`max`），每个席位可关联专属 Plan，保障资源归属清晰。
- **成本与稳定性管理**：Token Plan 是计费与用量监控的统一锚点——费用中心账单、模型监控中的「TotalToken 数」、告警规则（如“Token 消耗突增”）均基于同一计量结果；结合吞吐预留（TPM）可进一步保障高并发下的延迟稳定性。
- **安全与合规约束**：通过 `model_whitelist` 限制可调用模型范围（如仅允许 `qwen-plus`），避免误用高成本模型；自定义训练模型的推理 endpoint 不受 Token Plan 约束，需单独配置资源配额。
- **可观测性支撑**：模型监控页面的「Token 消耗」指标、限流错误次数（429）、审计日志中的 token 统计字段，均直接来源于该计量系统，但注意：监控数据延迟 ≤ 2 秒（实时性），而用量统计报表延迟约 1 小时（用于账单与分析）。

## 关键参数和配置

| 参数 | 说明 | 典型值 | 注意事项 |
|------|------|--------|----------|
| `max_tokens_per_minute` | 每分钟最大 token 消耗硬阈值 | `100000`（团队版默认） | 超过立即限流；单位为 token/分钟，非请求/分钟 |
| `burst_capacity` | 突发容量（token），允许短时超额 | `0`（v2.3+ 默认禁用） | 设为 `0` 表示严格限流；启用后需配合客户端退避逻辑 |
| `model_whitelist` | 允许调用的模型 ID 列表 | `["qwen-max", "qwen-plus"]` | 未配置则默认允许所有支持模型；不支持通配符 |
| `enable_quota_isolation` | 是否启用 Plan 间配额隔离 | `true` | 启用后各 Plan 余额互不影响，推荐开启 |
| `X-Parameter-Token-Plan-ID` | 请求头中显式指定 Plan | `tp-abc123` | 优先级高于 API Key 默认绑定的 Plan |

> ⚠️ 提示：`burst_capacity` 默认值已更新为 `0`（禁用突发模式），请以 SDK 初始化返回的 schema 或最新 API 文档为准；删除 Token Plan 后，API Key 自动回退至账户默认配额，历史用量保留 90 天。

## 面向开发者，简洁实用

- ✅ **快速上手**：在控制台「配额管理」创建 Token Plan → 绑定到 API Key → 正常发起模型请求即可生效，无需修改业务代码。
- ✅ **精准调试**：检查响应头 `X-Usage-Token-Count`（本次消耗 token 数）、`X-RateLimit-Limit`（当前 Plan 的每分钟限额）、`X-RateLimit-Remaining`（剩余配额），快速定位限流原因。
- ✅ **规避风险**：  
  - 不要硬编码 `api_key`，务必通过环境变量注入；  
  - 免费额度用户注意：自 2024 年 7 月起，所有免费 Plan 强制 30 天有效期，需手动续订；  
  - 单个 API Key 最多绑定 3 个 Plan（按环境区分），超出需先解绑。
- ✅ **最佳实践**：  
  - 生产环境务必启用 `enable_quota_isolation`；  
  - 高并发场景建议搭配 TPM 预留使用（二者不互斥，TPM 保底，Token Plan 控总量）；  
  - 监控告警中配置「TotalToken 数」突增告警，及时发现异常调用或 Prompt 注入攻击。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [preparations](../api/preparations.md)
- [model monitoring](../guides/model-monitoring.md)


