# [模型部署](../concepts/model-deployment.md)方式对比：Model Deployment 1 vs Model High Speed Inference vs Model Compression

## 对比目的与背景

在百炼平台模型服务落地过程中，开发者常面临「如何选择最适配业务需求的模型交付形态」这一核心问题。`Model Deployment 1`（MD1）、`Model High Speed Inference`（HSI）和`Model Compression`（MC）虽均服务于模型推理，但设计目标、技术路径与适用边界存在本质差异：

- **MD1** 是通用型**部署框架**，聚焦资源隔离、弹性伸缩与生产级运维保障；  
- **HSI** 是面向时延敏感场景的**推理通道优化能力**，不改变部署形态，而是在已有服务上启用加速调度策略；  
- **MC** 是模型层面的**轻量化预处理技术**，通过量化压缩降低硬件门槛，适用于资源受限或成本敏感环境。

本页旨在从工程实践角度，系统对比三者的关键特性，帮助开发者基于性能、成本、灵活性与合规性等多维约束，做出可落地的技术选型决策。

---

## 关键维度对比表

| 维度 | Model Deployment 1 (MD1) | Model High Speed Inference (HSI) | Model Compression (MC) |
|------|---------------------------|-----------------------------------|-------------------------|
| **本质定位** | 生产级模型服务部署范式（Infrastructure-as-Code） | 已部署模型的低延迟推理加速通道（Runtime Optimization） | 模型离线轻量化处理技术（Model Transformation） |
| **输入格式** | 支持标准 OpenAI 兼容格式（`messages`/`prompt`），支持 `stream: true`（除 `token_based` 模式外） | 同 MD1 输入格式，但强制要求 `stream: false`；`input_tokens + max_tokens ≤ 8192` | 无直接输入；作用于模型文件本身（Hugging Face 格式 `.safetensors` 或 `.bin`） |
| **输出格式** | 完整 OpenAI 响应结构（含 `choices`, `usage`, `id` 等），支持流式（部分模式） | 同 MD1 输出结构，但**仅支持非流式响应**（`stream: false` 必须） | 不产生运行时输出；生成新模型 ID（如 `qwen2-7b-int4-awq`），供后续部署或调用 |
| **支持模型** | 所有已发布至「我的模型」的模型（含自定义模型、Qwen 系列、Llama 等） | 仅限白名单模型：<br>• `qwen-max` / `qwen-plus` / `qwen-turbo`<br>• 标注 `high_speed: true` 的定制模型<br>（不支持[多模态](../concepts/multi-modal.md)、Function Calling） | 仅限 Qwen 系列开源模型：<br>• `qwen2-1.5b` / `qwen2-7b` 等<br>• **暂不支持 Llama、Phi、[多模态](../concepts/multi-modal.md)模型** |
| **API 端点** | 独立部署端点（如 `https://dashscope.aliyuncs.com/api/v1/deployments/{id}/chat/completions`） | **复用原模型 API 端点**（如 `/v1/chat/completions`），通过请求体参数 `enable_high_speed: true` 触发 | 无独立端点；压缩后模型需**另行部署（如通过 MD1）或直接调用**（使用新 model_id） |
| **计费方式** | 按部署类型差异化计费：<br>• `dedicated`/`dtu`：按实例时长（小时）+ GPU 资源规格<br>• `ptu`：按预置 PTU 数量（月结）<br>• `token_based`：按实际输入/输出 token 计费（实时扣费） | **不单独计费**，但需满足前置条件：<br>• 吞吐预留（TPM Reservation）需单独购买并计费<br>• Prime 预热实例消耗对应 GPU 资源（计入账号总用量） | **按压缩任务耗时计费**（GPU 小时）；压缩完成后的模型调用费用归属其部署方式（如部署为 MD1，则按 MD1 计费） |
| **典型场景** | • 稳定中高流量 SaaS 服务<br>• 多版本灰度发布（配合模型路由）<br>• 合规强要求场景（独占物理 GPU）<br>• 突发流量业务（`token_based` 模式） | • 实时对话机器人（P99 < 300ms）<br>• 搜索联想/补全（毫秒级响应）<br>• 高并发低延迟批处理（如客服工单摘要） | • 边缘设备/低配云主机推理<br>• 成本敏感型 PoC 或内部工具<br>• 需快速验证模型效果的轻量项目 |

---

## 适用场景建议

### ✅ 推荐选择 **Model Deployment 1**
- 你的模型需长期稳定在线，SLA 要求 ≥ 99.9%；
- 流量模式可预测（如日均 500 QPS），或存在明显波峰波谷（需自动扩缩）；
- 需要多模型/多版本统一管理、灰度发布、AB 测试；
- 涉及金融、政务等对资源隔离与审计有硬性要求的场景。

> ⚠️ 注意：若追求极致低延迟但流量不稳定，MD1 单独使用可能无法满足 P99 < 200ms 要求，建议叠加 HSI。

### ✅ 推荐选择 **Model High Speed Inference**
- 当前已通过 MD1 或百炼托管模型服务部署了 `qwen-plus` 等白名单模型；
- 业务对首字延迟（Time to First [Token](../concepts/token.md)）极度敏感，且能接受非流式响应；
- 可接受 3–5 分钟预热期，并确保请求持续活跃（避免实例释放）；
- 已购买 TPM 预留资源，需保障确定性吞吐能力。

> ⚠️ 注意：HSI **不是独立部署方案**，必须依附于一个已存在的模型服务（如 MD1 部署实例或百炼标准 API）。不可用于自定义模型（除非明确标注 `high_speed: true`）。

### ✅ 推荐选择 **Model Compression**
- 目标运行环境显存有限（如 < 8GB GPU 或 CPU-only 设备）；
- 模型精度容忍小幅下降（INT4 压缩后 Qwen2-7B 在常规 QA 任务中 BLEU 下降约 1.2–2.5）；
- 需快速验证多个小模型变体，或构建低成本内部工具链；
- 无长期运维诉求，倾向“压缩→部署→使用”极简流程。

> ⚠️ 注意：MC 生成的模型**不可微调**，且长上下文（>8K tokens）下可能出现逻辑连贯性退化，关键业务需增加后处理校验。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 补充说明 |
|----------|----------|----------|----------|
| “我要上线一个企业客服机器人，要求 99.95% 可用率，支持灰度发布” | **MD1 + dedicated 模式** | 独占资源保障 SLA，支持模型路由实现灰度，控制台可观测性强 | 配合 `min_replicas=2` 防止单点故障 |
| “我们的搜索补全接口 P99 延迟超标，当前用 qwen-plus 调用标准 API” | **HSI（启用 `enable_high_speed: true`）** | 无需改代码、不重建服务，5 分钟内生效，实测 P99 降低 40–60% | 务必设置 `max_tokens ≤ 512` 并禁用 `stream` |
| “想在树莓派上跑一个轻量摘要模型，预算只有 100 元/月” | **MC（AWQ 量化） + MD1 token_based 部署** | INT4 模型显存占用降至 1/3，`token_based` 按量付费契合低频场景 | 建议选用 `qwen2-1.5b-int4-awq`，7B 模型在树莓派 5 上仍较吃力 |
| “需要同时支持流式响应 + 低延迟 + 多模型切换” | **MD1（ptu 模式） + HSI（针对白名单模型）** | MD1 提供流式能力与弹性，HSI 为特定模型加速；二者正交叠加 | 注意：HSI 本身不支持流式，因此流式请求走普通通道，非流式请求走高速通道 |
| “我们训练了一个私有 Llama-3-8B 模型，需部署到私有云 GPU 集群” | **MD1（dedicated 模式）** | MC 不支持 Llama 系列，HSI 不支持非白名单模型，MD1 是唯一可行路径 | 可结合 VPC 内网部署提升安全性与延迟 |

> 💡 **终极建议**：  
> - **先压缩，再部署，最后加速**：对 Qwen 白名单模型，优先执行 MC（降低资源成本）→ 用 MD1 部署 → 在高优接口中启用 HSI；  
> - **非 Qwen 模型请绕过 HSI 和 MC**：直接使用 MD1 的 `dedicated` 或 `ptu` 模式，确保功能完整性；  
> - **所有方案均强制 HTTPS**：内网直连需额外配置 VPC 对等连接或 PrivateLink，不可跳过安全层。

---  
*文档更新时间：2024年6月*  
*依据百炼平台 v2.5.0 版本功能矩阵整理，具体以控制台实时能力为准*

## 被对比主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model compression](../guides/model-compression.md)


