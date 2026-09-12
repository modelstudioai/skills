# [模型部署](../concepts/model-deployment.md)方式对比：托管服务 vs 自定义生产部署

为帮助开发者在百炼平台上高效、可靠地将模型投入实际业务，本文系统对比两类主流部署路径：**托管服务（Model Deployment 1）** 与 **自定义生产部署（Model Production + High-Speed Inference）**。二者并非互斥，而是面向不同阶段、不同 SLA 要求与工程成熟度的技术选型组合。本文聚焦关键差异维度，提供可落地的决策依据，避免因模式错配导致成本浪费、延迟超标或运维过载。

---

## 关键维度对比

| 维度 | 托管服务（`model deployment 1`） | 自定义生产部署（`model production` + `high speed inference`） |
|------|----------------------------------|-------------------------------------------------------------|
| **定位与目标** | 快速验证、敏捷迭代、标准化交付；开箱即用的模型服务能力 | 生产级稳定运行、SLA 可承诺、精细化资源治理与性能调优 |
| **输入格式** | 标准 RESTful JSON（兼容 [OpenAI 兼容接口](../concepts/openai-compatibility.md)），支持 `messages` / `prompt` 等字段；部分模式支持二进制输入（如图像上传） | 同上，但 **高速推理（Prime/TPM）仅支持 SaaS 模型的标准 JSON-RPC 输入**；微调模型不支持 Prime 模式 |
| **输出格式** | 完整 JSON 响应（含 `choices`, `usage`, `created` 等）；支持流式响应（`stream=true`）**除 `token` 按量模式外** | 同上；但 **启用 `speed_mode="prime"` 时，`stream=true` 将被强制忽略并静默降级为非流式** |
| **支持模型类型** | ✅ 百炼官方模型（Qwen 系列等）<br>✅ 用户导入的自定义模型（需完成校验与构建）<br>✅ 微调后模型（`ft-xxx`） | ✅ 百炼官方 SaaS 模型（`qwen-max`, `qwen-plus`, `qwen-turbo`）<br>❌ **不支持自定义导入模型或微调模型的高速推理（Prime/TPM）**<br>✅ 微调模型可走 `model production` 的弹性/TPM 模式（无 Prime 加速） |
| **API 端点** | 单一、静态 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`），由部署任务自动生成并长期有效 | 复用同一套 SaaS 模型 endpoint，但通过请求头或 body 参数（如 `speed_mode`, `tpm_reservation`）动态激活加速能力；`model production` 实例亦生成专属 endpoint（如 `/v1/model-productions/{id}/inference`） |
| **计费方式** | • `dedicated` / `dtu`：按实例规格 + 运行时长（小时）计费<br>• `ptu`：按预置 PTU 单位（≈10 QPS@1k token）+ 时长计费<br>• `token`：按实际输入/输出 token 数实时计费 | • `model production` 弹性模式：按实际 token 调用量计费（同 `token` 模式）<br>• `model production` TPM 模式：按预购 TPM 容量（如 500 TPM）+ 时长计费（保底消费）<br>• 高速推理（TPM Reservation）：需**额外购买 TPM 预留配额**（独立于模型调用费），按月预付 |
| **资源隔离性** | • `dedicated` / `dtu`：物理/虚拟 GPU 独占，强隔离<br>• `ptu` / `token`：共享集群，依赖调度与缓存优化保障性能 | • TPM 模式：独占算力保障，SLA 可承诺（如 p95 < 300ms）<br>• 弹性模式：共享资源池，性能波动受整体负载影响<br>• Prime 模式：非资源独占，属运行时优化策略（预热/KV Cache/队列调度） |
| **扩缩容能力** | • `dedicated`：固定规格，不自动扩缩<br>• 其余模式：默认开启自动扩缩容（缩容冷却期 5 分钟） | • TPM 模式：容量固定，**不支持热变更**，需停用后重新创建<br>• 弹性模式：全自动扩缩容，响应流量峰谷<br>• Prime 模式：依赖底层实例状态，滚动升级期间自动暂停 |
| **典型场景** | • 内部 PoC、A/B 测试、低频 API 调用<br>• 中小规模应用（日均 < 10 万 token）<br>• 需快速上线多个模型进行路由灰度 | • 面向终端用户的高并发服务（如客服对话、搜索补全）<br>• 对延迟敏感的实时系统（p99 < 500ms）<br>• 需签署 SLA 协议的企业级集成<br>• 流量存在明显波峰波谷的批处理任务 |

---

## 适用场景建议

### ✅ 推荐选择 **托管服务（`model deployment 1`）** 当：
- 你处于模型选型、[Prompt 工程](../concepts/prompt-engineering.md)验证或 MVP 快速上线阶段；
- 调用量较低且波动平缓（如后台分析、内部工具），无需承诺严格延迟；
- 需要灵活部署**自定义模型或微调模型**，并复用百炼统一 API 接口；
- 团队缺乏专职 MLOps 工程师，倾向“配置即服务”（Configuration-as-Service）；
- 成本敏感，希望按 token 精确计量（`token` 模式）或按需预置吞吐（`ptu` 模式）。

### ✅ 推荐选择 **自定义生产部署（`model production` + `high speed inference`）** 当：
- 你已确认模型效果与业务逻辑，进入**正式生产环境交付**阶段；
- 服务需满足明确 SLA（如 p95 延迟 ≤ 300ms、可用性 ≥ 99.95%），且用户对响应卡顿高度敏感；
- 流量具备可预测性（TPM 预留）或剧烈波动性（弹性模式），需平台级资源保障与自动伸缩；
- 使用的是百炼官方 SaaS 模型（非微调/自定义），且愿意为确定性性能支付 TPM 预留费用；
- 需要深度集成监控（如订阅 p95 延迟、错误率告警）、灰度发布、版本回滚等企业级运维能力。

### ⚠️ 注意：混合使用是最佳实践
- **推荐路径**：先用 `model deployment 1`（`ptu` 或 `dedicated`）完成模型验证与初期上线 → 流量增长后，对核心 SaaS 模型启用 `model production` + `high speed inference`（TPM + Prime）保障主链路 → 对非核心模型或实验模型仍保留 `model deployment 1` 灵活管理。
- **禁止组合**：不要尝试对 `model deployment 1` 创建的 `token` 模式实例启用 `speed_mode="prime"`（无效）；也不要对微调模型调用 `tpm_reservation` 参数（将被忽略或报错）。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键操作指引 |
|----------|-----------|----------------|
| “我想今天就跑通一个 Qwen2-7B 的 API，测试下效果” | ✅ `model deployment 1`（`dedicated` 模式） | 控制台 → [模型部署](../concepts/model-deployment.md) → 选 `qwen2-7b-instruct` → `deployment_type=dedicated` → 部署 → 调用返回 endpoint |
| “我们 App 下周上线，预计峰值 200 QPS，必须保证 95% 请求 < 400ms” | ✅ `model production`（TPM 模式） + `high speed inference`（Prime） | 1. 控制台购买 2000 TPM 配额；2. 调用 `/v1/model-productions` 创建 TPM 实例；3. API 请求中传 `"speed_mode":"prime","tpm_reservation":2000` |
| “我微调了一个金融领域模型 `ft-fin-2024`，需要稳定服务但预算有限” | ✅ `model deployment 1`（`ptu` 模式） | 查 [PTU 规格表](https://help.aliyun.com/zh/model-studio/ptu-long-input-and-cache)，按预期 50 QPS 选择 `ptu_capacity=5` → 部署 → 调用 |
| “后台有批量报告生成任务，每天凌晨触发，耗时 2 小时，但白天零流量” | ✅ `model production`（弹性模式） | 创建 `model production` 实例时不填 `tpm_capacity` → 平台按需扩缩 → 任务结束调用 `DELETE /v1/model-productions/{id}` 释放资源 |
| “我们需要把模型集成进现有 Kubernetes 集群，完全自主管控” | ❌ 两者均不适用 → 请评估 [百炼私有化部署方案](https://help.aliyun.com/zh/model-studio/private-deployment) 或导出模型至自建推理服务 |

> **最后提醒**：所有部署均需通过 [模型导入](https://help.aliyun.com/zh/model-studio/model-import) 或 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-jobs-api) 完成前置准备；生产环境务必启用 [模型路由](https://help.aliyun.com/zh/model-studio/model-routing) 实现灰度与降级，切勿直连单点实例。

## 被对比主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


