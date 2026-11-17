# 模型部署与推理方案对比：高并发推理、模型管理与生产就绪

本文档面向百炼平台开发者，系统对比三类核心能力模块在**高并发推理支撑能力、模型全生命周期管理成熟度、生产环境就绪度（SLA/可观测性/稳定性/运维闭环）** 三个维度的技术特性与适用边界。对比目的在于帮助团队基于业务流量特征（如峰值TPS、延迟敏感度、成本弹性）、组织治理需求（如多项目配额隔离、权限分级、审计合规）及交付阶段（PoC验证 → 灰度上线 → 全量生产）做出可落地、可演进的技术选型决策。

---

## 关键维度对比表

| 维度 | **高并发推理（Model High Speed Inference）** | **模型管理（Model Management）** | **生产就绪（Model Production）** |
|------|---------------------------------------------|-----------------------------------|----------------------------------|
| **核心定位** | 面向**运行时性能优化**的推理加速层，聚焦“如何更快、更稳、更省地调用模型” | 面向**运行时访问治理**的策略控制层，聚焦“谁能在何时、以何种配额调用哪个模型” | 面向**模型服务化交付**的工程化平台，聚焦“如何将训练/微调成果可靠、可控、规模化地投入生产” |
| **输入格式** | 标准 OpenAI 兼容请求体（`messages`, `model`, `stream`, `enable_thinking` 等）；Batch 场景需 JSONL 文件 | REST API 请求体（JSON），含 `model_id`, `rate_limit`, `permissions` 等策略对象 | OpenAPI 请求体（JSON），含 `plan`, `model_name`, `service_tier`, `charge_type`, `deploy_spec` 等部署/调优参数 |
| **输出格式** | 标准 OpenAI 兼容响应（含 `choices`, `usage`, `model`）；Batch 返回[异步任务](../concepts/asynchronous-task.md) ID 及结果下载链接 | REST API 响应（JSON），返回模型元数据列表、当前限流值、授权范围等策略快照 | OpenAPI 响应（JSON），含 `operation_status`, `output.model_code`, `output.finetuned_output`, `output.quantized_output` 等异步作业结果 |
| **支持模型** | ✅ Prime：`glm-5.2-fast-preview`, `glm-5.3-prime`, `wan3.0-video-prime`<br>✅ 吞吐预留/PTU/DTU：`Qwen3.8-Max`, `GLM-5.3`, `DeepSeek-v4-Pro` 等数十种 SaaS 模型 + LoRA 微调模型<br>✅ Batch：`qwen3.8-max`, `qwen3-vl-plus`, `text-embedding-v4`<br>✅ 智能路由：动态匹配 `qwen3.8-flash`, `deepseek-v4-pro-0813` 等备选模型 | ⚠️ 仅支持**百炼预置 SaaS 模型**（如 `qwen-max`, `qwen-plus`, `qwen-turbo`）<br>❌ 不支持用户自定义部署的私有模型实例（如 DTU/MU/Lora 部署产出） | ✅ 支持四类模态：文本（`qwen3`, `glm-5`）、图像（`wan2.1`）、视频（`wan3.0-video`）、语音（`cosyvoice-v3-flash`）<br>✅ 支持基础模型、LoRA 微调模型、全参微调模型、压缩后模型<br>✅ DTU/MU 部署支持物理级隔离模型 |
| **API 端点** | - 实时推理：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/v1/chat/completions`（兼容模式域名用于 Prime）<br>- Batch 提交：`POST /v1/batch/jobs`（控制台或 API） | `GET /v1/models`, `GET /v1/models/{model_id}/quotas`, `PATCH /v1/models/{model_id}/quotas`, `PATCH /v1/models/{model_id}/permissions` | `POST /api/v1/fine-tunes`, `POST /api/v1/deployments`, `POST /api/v1/fine-tunes/compress/jobs`, `GET /api/v1/deployments/{deployment_id}` |
| **计费方式** | - Prime：按 token 计费，无额外费用<br>- 吞吐预留（PTU）：预付费（包年包月）或后付费（按实际 TPM 使用量）<br>- DTU：预付费（强制 `pre_paid`），按 `input_tpm`/`output_tpm` 容量计费<br>- MU：按模型单元（MU）数量 × 时长计费<br>- Batch：按 token 计费，成本约为实时推理的 50%<br>- 智能路由：后付费，按实际调用模型计费 | ❌ **不产生直接费用** —— 属于平台治理能力，无独立计费项 | - 调优：按 GPU 小时 + 存储计费<br>- 部署（Lora/MU/DTU/PTU/MR）：对应资源类型计费（见高并发推理列）<br>- 模型压缩：按 GPU 小时计费 |
| **典型场景** | - 秒级响应的对话机器人、实时搜索摘要<br>- 大促期间保障核心接口 SLA（99.9% < 500ms）<br>- 批量处理历史日志/文档生成报告<br>- A/B 测试多模型效果与成本平衡 | - 多团队共享模型池，防止某项目突发流量挤占全局资源<br>- 合规要求下限制敏感模型仅对特定部门开放<br>- 新模型灰度期设置低配额，逐步放量 | - 将业务专属微调模型（如金融客服 LoRA）上线为稳定服务<br>- 为语音合成服务申请独占 MU 资源保障 TTS 延迟<br>- 对高频调用的 `qwen3.5-flash` 模型启用吞吐预留防抖动<br>- 自动化 CI/CD 流水线集成模型训练→压缩→部署→压测全链路 |

---

## 各方案适用场景建议

| 方案 | 推荐使用场景 | 不推荐场景 | 关键风险提示 |
|------|--------------|------------|--------------|
| **高并发推理（Prime / PTU / DTU / Batch / MR）** | • 业务已明确模型选型，追求极致性能与成本效率<br>• 流量存在明显波峰波谷，需容量弹性或硬隔离<br>• 非实时批处理任务（如日报生成、知识库索引）<br>• 多模型效果/成本探索期（智能路由） | • 模型尚未完成调优或验证，仍处于算法迭代阶段<br>• 需要频繁变更模型结构（如修改 LoRA adapter）<br>• 跨地域（非北京/新加坡）部署需求 | • PTU/DTU 创建后需预热，突发流量可能短暂超时<br>• Batch 不返回 `reasoning_content`，无法满足深度思考审计需求<br>• 智能路由备选模型若无调用权限，将静默降级至默认模型，需提前校验权限 |
| **模型管理（Model Management）** | • 多项目/多租户共用百炼平台，需精细化配额管控<br>• 满足 SOC2/GDPR 等合规审计要求（记录谁在何时调用了哪个模型）<br>• 新模型上线前进行沙箱限流测试（如设 `requests_per_minute=5`） | • 单项目单模型简单场景，无治理复杂度<br>• 需要管理自定义部署模型（如 DTU 实例）的访问策略<br>• 期望通过该能力实现模型版本灰度（其本身不支持版本概念） | • 权限更新为**全量覆盖**，误删 `permissions` 数组将导致模型不可用<br>• `tokens_per_minute=0` 不合法，禁用模型需结合权限移除+极低配额双重措施 |
| **生产就绪（Model Production）** | • 模型从实验走向生产，需标准化、可复现、可追踪的服务化流程<br>• 语音/视频等强资源敏感模态，需 MU/DTU 级别资源保障<br>• 需要自动化集成（如 GitOps 触发微调→部署→通知）<br>• 对模型体积敏感，需量化压缩降低推理成本 | • 快速原型验证（PoC），仅需临时调用预置模型<br>• 无定制化需求，纯使用百炼标准 SaaS 模型且无配额治理诉求<br>• 跨地域（如华东1）部署需求（当前仅支持华北2/北京） | • **HTTP 200 ≠ 业务成功**：必须检查响应体中 `output.operation_status` 字段<br>• 模型压缩不可逆，压缩后模型不支持继续微调<br>• DTU 续费、自动续费开关仅支持控制台操作，API 不开放 |

---

## 技术选型参考（面向开发者）

请按以下逻辑分步决策：

### 第一步：确认模型来源与成熟度
- ✅ 若使用**百炼预置 SaaS 模型**（如 `qwen-max`）且无需微调 → 直接进入 **高并发推理** 选型（Prime/PTU/Batch/MR），搭配 **模型管理** 进行配额与权限治理。
- ✅ 若已完成**LoRA/全参微调**或**导入自定义模型** → 必须通过 **生产就绪（Model Production）** 完成部署（`plan=lora`/`mu`/`dtu`），再基于部署产出的 `model_code` 调用 **高并发推理** 接口。
- ⚠️ 若需**模型压缩**或**语音/视频专用部署** → 强制使用 **生产就绪**，因其是唯一支持这些能力的入口。

### 第二步：评估流量特征与 SLA 要求
| 流量特征 | 推荐方案 | 理由 |
|----------|----------|------|
| **超高频、低延迟（<200ms）、强稳定性**（如核心APP对话） | DTU 或 PTU（`ptu_fast`） | 物理/逻辑独占资源，规避多租户干扰，TPM 可精确承诺 |
| **高并发、可容忍秒级延迟**（如后台任务调度） | Batch | 成本优势显著（≈实时推理50%），适合离线批量 |
| **流量波动大、需弹性伸缩**（如电商大促） | PTU（后付费）+ 溢出至按量 | 预留基线容量保 SLA，溢出部分自动兜底，成本可控 |
| **多模型效果探索、AB测试** | 智能路由（MR） | 统一入口，策略驱动（效果优先/成本优先），免客户端改码 |

### 第三步：明确治理与运维需求
- 需**跨项目配额隔离**？ → 必用 **模型管理** 配置 `project_id` 级限流。
- 需**审计模型调用行为**？ → 开启 **模型管理** 的权限策略，并结合百炼平台操作日志。
- 需**自动化发布流水线**？ → 以 **生产就绪** OpenAPI 为核心编排，调用 `/api/v1/fine-tunes` → `/api/v1/deployments` → `/v1/chat/completions`。
- 需**生产环境可观测性**？ → 所有方案均支持百炼平台统一监控（TPM/延迟/错误率），但 **DTU/MU** 提供更细粒度的实例级指标。

> 💡 **最佳实践组合推荐**  
> - **企业级对话中台**：`生产就绪（LoRA 微调 + PTU 部署）` + `高并发推理（PTU model_code 调用）` + `模型管理（按业务线 project 划分配额）`  
> - **AI 增强型 BI 工具**：`高并发推理（Batch 处理历史报表）` + `模型管理（限制 `text-embedding-v4` 调用量防滥用）`  
> - **合规敏感型客服系统**：`生产就绪（CosyVoice MU 部署）` + `高并发推理（MU model_code + stream=true）` + `模型管理（仅授权客服 project 调用）`

---  
*最后更新：2025年4月*

## 被对比主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model management](../api/model-management.md)
- [model production](../api/model-production.md)


