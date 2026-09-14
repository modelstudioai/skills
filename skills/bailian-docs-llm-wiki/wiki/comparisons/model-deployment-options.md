# [模型部署](../concepts/model-deployment.md)方案对比：高并发推理、[模型部署](../concepts/model-deployment.md)基础与生产化部署

为帮助开发者在百炼平台上高效选型，本文系统对比三种核心模型服务能力：**High Speed Inference（高速推理）**、**Model Deployment 1（MD1，[模型部署](../concepts/model-deployment.md)基础方案）** 和 **Model Production（模型生产化部署）**。三者定位不同——高速推理聚焦 *已有SaaS模型的极致性能优化*，MD1 提供 *标准化、多策略的通用部署基座*，而 Model Production 则面向 *从微调模型到生产上线的全生命周期管理*。理解其差异对保障低延迟、控成本、提稳定性及加速 MLOps 落地至关重要。

---

## 关键维度对比

| 维度 | High Speed Inference（高速推理） | Model Deployment 1（MD1） | Model Production（模型生产化部署） |
|------|----------------------------------|----------------------------|-------------------------------------|
| **定位目标** | 在标准 SaaS 模型调用链路上叠加毫秒级延迟保障与确定性吞吐 | 提供可配置、可隔离、可计费的模型服务实例部署能力，覆盖轻量到严苛 SLA 场景 | 将训练/调优后的模型（含自定义微调模型）正式投入生产环境，支持灰度、扩缩容与资源预留 |
| **支持模型类型** | ✅ 仅限已上线 SaaS 模型（如 `qwen-max`, `qwen-plus`, `qwen-turbo`）<br>❌ 不支持 Fine-tuned 模型 | ✅ 所有已发布模型：SaaS 模型 + 导入的自定义模型（含 LoRA 微调模型） | ✅ 支持 Fine-tuned 模型（`fine_tuned_model_id`）<br>✅ 支持官方基础模型（如 `qwen-max`） |
| **输入格式** | 标准 OpenAI 兼容请求体（`/v1/chat/completions`），需显式携带 `speed_mode` 字段 | 标准 OpenAI 兼容请求体（`/v1/chat/completions`），Endpoint 独立，无需额外字段 | DashScope OpenAPI 格式（`/v1/deployments/{id}/chat/completions`），需使用专属 endpoint 与 api_key |
| **输出格式** | 完全兼容 OpenAI 标准响应结构（含 `choices`, `usage`, `id` 等） | 完全兼容 OpenAI 标准响应结构 | 兼容 OpenAI 标准响应结构，但部分字段（如 `system_fingerprint`）可能因部署模式略有差异 |
| **API 端点** | 复用全局 SaaS 接口：<br>`POST https://dashscope.aliyuncs.com/api/v1/chat/completions` | 独立部署 endpoint：<br>`POST https://{deployment-id}.aliyuncs.com/v1/chat/completions` | 独立生产部署 endpoint：<br>`POST https://dashscope.aliyuncs.com/api/v1/deployments/{deployment_id}/chat/completions` |
| **核心资源控制机制** | • `speed_mode`: `"prime"`（预热+常驻）或 `"reserved"`（TPM 预留）<br>• `tpm_reservation`（仅 reserved 模式） | • `deployment_type`: `dedicated` / `ptu` / `dtu` / `mu` / `pay_as_you_go`<br>• `instance_type`, `ptu_capacity`, `max_concurrent_requests` 等精细参数 | • `tpm_capacity`（TPM 预留上限）<br>• `replicas`（副本数）<br>• `timeout`（单请求超时） |
| **计费方式** | ✅ 独立计费项，单价高于标准推理<br>✅ TPM 预留配额按自然日重置，不累计<br>❌ 不支持跨模型共享预留 | ✅ 按部署类型差异化计费：<br> - `dedicated`/`dtu`/`mu`: 按实例时长或算力单元计费<br> - `ptu`: 按预置吞吐量包年/包月<br> - `pay_as_you_go`: 按实际 token 数计费 | ✅ TPM 预留费用独立计费（与高速推理的 `tpm_reservation` 分开）<br>✅ 副本（`replicas`）按实例时长计费<br>✅ 不支持纯 token 按量模式（无 `pay_as_you_go` 类型） |
| **典型场景** | • 实时对话机器人首响应（<300ms P99）<br>• 搜索下拉补全（高频短请求）<br>• API 网关后端强 SLA 服务 | • 内部工具后台服务（稳定中等流量）<br>• 客户侧集成 SDK（需专属 endpoint 与权限隔离）<br>• 成本敏感型 PoC 或灰度验证（`pay_as_you_go`） | • LoRA 微调模型上线交付客户<br>• 多版本模型 AB 测试（如 `v1` vs `v2` 微调版）<br>• 金融/政务类需审计追踪与副本冗余的生产系统 |
| **冷启延迟保障** | ✅ Prime 模式：内存常驻 + 请求队列优化，首次调用无冷启<br>✅ Reserved 模式：TPM 预留保障最低吞吐，降低排队抖动 | ⚠️ `dedicated`/`dtu`/`mu`: 启动耗时 3–5 分钟，就绪后无冷启<br>⚠️ `ptu`: 自动扩缩，存在毫秒级弹性冷启<br>❌ `pay_as_you_go`: 存在显著冷启延迟（秒级） | ⚠️ 首次部署需 2–8 分钟（含加载、初始化），就绪后副本常驻；`replicas > 1` 可规避单点冷启风险 |
| **动态调整能力** | ❌ `speed_mode` 与 `tpm_reservation` 不可运行时变更，需重发请求并满足配额 | ❌ `deployment_type` 与 `instance_type` 不可变更<br>✅ `max_concurrent_requests` 可热更新（部分模式）<br>✅ `pay_as_you_go` 可随时停用 | ❌ `tpm_capacity` 不可动态调整（需删除重建）<br>✅ `replicas` 支持运行时水平扩缩（1→10）<br>✅ 支持通过路由规则切换流量（灰度/回滚） |

---

## 适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| **已上线 `qwen-plus`，需为客服对话接口提供 <200ms P99 延迟保障，且流量平稳可预测** | ✅ High Speed Inference（`speed_mode="reserved"` + `tpm_reservation=3000`） | 直接复用 SaaS 模型能力，无需部署新实例；TPM 预留提供硬性吞吐与延迟 SLA，成本低于独占实例，接入最快（改请求体即可）。 |
| **需将内部微调的 `qwen-turbo-lora-v2` 模型封装为独立 API 供多个业务方调用，并要求权限隔离、独立监控与按调用量计费** | ✅ Model Deployment 1（`deployment_type="pay_as_you_go"`） | 支持自定义模型导入，`pay_as_you_go` 模式零预置成本、按 token 计费透明，专属 endpoint 满足权限与可观测性需求，适合多租户分发场景。 |
| **某银行风控模型完成 LoRA 微调，需上线生产环境，要求双副本高可用、TPM 预留 5000、支持灰度发布至 5% 流量、并保留完整审计日志** | ✅ Model Production（`tpm_capacity=5000`, `replicas=2`） | 唯一支持 Fine-tuned 模型直接生产的方案；原生支持副本扩缩、TPM 预留、灰度路由（配合模型路由功能），且部署状态与生命周期受平台统一管控，符合金融合规要求。 |
| **内部研发团队快速验证 `qwen-max` 在新 Prompt 下的效果，无 SLA 要求，预算有限，希望即开即用** | ✅ Model Deployment 1（`deployment_type="pay_as_you_go"`）或 ✅ High Speed Inference（标准模式，不启用 speed_mode） | `pay_as_you_go` 提供专属 endpoint 便于调试与埋点；若仅需临时测试，直接调用 SaaS 接口（无 speed_mode）成本最低、开通最快。 |
| **构建企业级 AI 中台，需统一纳管 20+ 个模型（含 SaaS 与微调模型），支持自动扩缩容、流量调度、熔断降级与统一计费看板** | ✅ Model Production + ✅ MD1 协同使用 | Model Production 管理微调模型生产部署与 TPM/副本；MD1 管理 SaaS 模型的 PTU/DTU 部署；二者 endpoint 均可接入同一模型路由网关，实现中台级统一调度与治理。 |

---

## 技术选型参考（面向开发者）

- **优先检查模型来源**：  
  → 若使用 **官方 SaaS 模型**（`qwen-*` 系列）且追求**极致低延迟/确定性吞吐** → 选 **High Speed Inference**；  
  → 若使用 **Fine-tuned 自定义模型** → **Model Production 是唯一可行路径**；  
  → 若需 **专属 endpoint、权限隔离或混合部署（SaaS + 自定义）** → 选 **MD1**。

- **关注延迟与稳定性要求**：  
  → P99 < 300ms 且请求长度 ≤2048 tokens → High Speed Inference Prime 模式最优；  
  → 需毫秒级确定性延迟（如实时语音转写）→ MD1 的 `dtu`/`mu` 模式；  
  → 可接受秒级冷启与波动延迟 → MD1 `pay_as_you_go` 或 Model Production（无 TPM）。

- **评估成本结构**：  
  → 流量高度可预测 → High Speed Inference Reserved 或 MD1 PTU；  
  → 流量峰谷明显或处于验证期 → MD1 `pay_as_you_go`；  
  → 需长期稳定运行且有副本冗余要求 → Model Production（按副本计费更清晰）。

- **重视运维与扩展性**：  
  → 需灰度、AB、自动扩缩、多地域部署 → **Model Production 是当前最成熟选择**；  
  → 需与现有 DevOps 工具链（如 Terraform、CI/CD）深度集成 → 查阅各方案 OpenAPI 文档，Model Production 与 MD1 均提供完整 API，High Speed Inference 仅作为请求参数存在。

> **最后提醒**：三者并非互斥，而是互补。例如：可对核心 SaaS 模型启用 High Speed Inference 保障主链路，同时用 Model Production 部署微调模型处理长尾场景，并通过 MD1 的模型路由能力统一接入——这才是百炼平台生产级架构的最佳实践。

## 被对比主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)


