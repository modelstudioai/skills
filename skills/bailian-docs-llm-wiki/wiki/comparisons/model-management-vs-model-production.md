# 模型管理与高性能推理部署对比

本文旨在帮助开发者清晰区分百炼平台中**模型管理（Model Management）** 与**高性能推理部署（Model Production + High-Speed Inference）** 两大能力体系的核心定位、技术边界与适用阶段。二者虽均围绕“模型可用性”展开，但分属不同生命周期层级：前者聚焦**已上线模型的运行时策略治理**（谁可调用、调多少、何时限流），后者覆盖**模型从训练、压缩、部署到加速服务的全生产链路**（如何构建、交付并保障高性能推理）。准确理解差异是避免权限误配、资源错投与架构返工的关键前提。

以下从关键维度进行结构化对比：

| 维度 | 模型管理（Model Management） | 高性能推理部署（Model Production + High-Speed Inference） |
|------|------------------------------|----------------------------------------------------------|
| **核心目标** | 对**已部署上线**的推理模型实施细粒度访问控制与流量治理 | 完成模型的**训练、优化、部署及性能增强**，构建可对外提供服务的推理实例 |
| **生命周期阶段** | 运行时（Runtime）——模型已处于 `RUNNING` 状态后 | 全生命周期（Training → Optimization → Deployment → Serving） |
| **输入格式** | RESTful API 请求体（JSON），含 `model_id`、`qps_limit`、`tpm_limit`、`principals` 等策略参数 | 多样化输入：<br>• 微调：训练数据集（OSS URI）、超参配置（`hyper_parameters`）<br>• 部署：`model_name`、`plan`（如 `"ptu_v2"`）、容量参数（`ptu_capacity`）<br>• 批量推理：标准 JSONL 文件（每行一个 OpenAI 兼容请求） |
| **输出格式** | 标准 HTTP 响应（JSON），返回操作结果（如 `200 OK` + 更新后的限流/授权状态）或错误码（`403 Forbidden`, `400 Bad Request`） | 多形态输出：<br>• 微调：任务 ID、最终微调模型 ID（`finetuned_output`）<br>• 部署：专属 `deployed_model` code、服务端点（Endpoint）、SLA 指标<br>• 批量推理：异步任务 ID、结果文件 OSS URL、完成状态报告 |
| **支持模型范围** | **仅限平台已上线的推理模型**：<br>• Qwen 系列（`qwen-max`/`qwen-plus`/`qwen-turbo`）<br>• 第三方接入模型<br>• *不支持未部署模型、训练中模型或私有导入模型* | **全栈覆盖**：<br>• 基础模型（`qwen3-14b`, `glm-5.3`）<br>• 微调模型（SFT/DPO LoRA、全参微调）<br>• 压缩模型（量化版 `qwen3.5-flash`）<br>• 多模态模型（图像生成 `wan2.7-i2v`、视频生成 `wan3.0-video-prime`、语音合成 `cosyvoice`） |
| **API 端点** | `/v1/models`（列表）<br>`/v1/models/{model_id}/rate-limits`（限流）<br>`/v1/models/{model_id}/permissions`（授权） | `/api/v1/fine-tunes`（微调）<br>`/api/v1/deployments`（部署）<br>`/v1/batches`（批量推理）<br>`/v1/chat/completions`（Prime/PTU/智能路由等加速调用） |
| **计费方式** | **不直接计费**：<br>模型管理本身为管控能力，无独立费用；其配置的限流/授权策略影响下游调用产生的实际计费（按 token 或请求量） | **多模式计费**：<br>• 按量付费（[Token](../concepts/token.md)/Request）：基础调用<br>• 预付费（刚性）：DTU（独占吞吐）、MU（模型单元）、PTU（吞吐预留）——创建即扣费，无论是否调用<br>• 异步降本：Batch 推理成本约为实时调用的 50% |
| **典型场景** | • 多租户 SaaS 平台中为不同客户分配差异化 QPS/TPM 配额<br>• 禁用测试账号对生产模型的调用权限（`qps_limit=0`）<br>• 为运维监控服务（`service:monitoring-bot`）授予只读模型元信息权限 | • 企业定制专属客服模型（微调 + PTU 保障高并发）<br>• 构建离线内容生成流水线（批量推理处理万级文档）<br>• 为低延迟交互应用启用 Prime 模式（首字延迟 <200ms）<br>• 为金融风控系统部署 DTU 专属实例（物理隔离+确定性 SLA） |

## 各方案的适用场景建议

- ✅ **选择「模型管理」当且仅当**：  
  您已拥有一个或多个**已在百炼平台成功部署并处于运行状态的模型**，当前需求是**精细化管控这些现成服务的访问行为**——例如给销售团队开放 `qwen-plus` 的 5 QPS 配额、禁止外包人员调用 `qwen-max`、或临时冻结某第三方模型供安全审计。此时无需关心模型如何训练、部署或加速。

- ✅ **选择「高性能推理部署」当且仅当**：  
  您需要**从零构建或升级一个可服务的 AI 能力**，涉及以下任一动作：  
  • 训练专属模型（微调文本/图像/语音）  
  • 将自研模型导入平台并部署（OSS 导入 + MU/DTU 部署）  
  • 为线上业务保障稳定低延迟（启用 Prime / PTU / DTU）  
  • 处理海量非实时任务（使用 Batch 推理降本）  
  • 动态匹配最优模型（通过智能路由自动选模）  

  > ⚠️ 注意：若您的模型尚未部署（`status ≠ RUNNING`），**必须先通过 `model production` 完成部署**，才能对其执行 `model management` 的限流或授权操作。

## 面向开发者的技术选型参考

| 您的问题 | 推荐路径 | 关键检查点 |
|----------|-----------|-------------|
| “我有一个微调好的模型，想让它在生产环境被多个业务方安全调用，且各自配额不同” | 1. 用 `model production` 部署该模型（获取 `deployed_model` code）<br>2. 用 `model management` 为各业务方设置 `principals` + `qps_limit`/`tpm_limit` | 确保部署成功（`status == "RUNNING"`）；确认 `model_id` 与部署返回的 `deployed_model` 一致 |
| “我的应用突发流量导致 `qwen-max` 调用频繁 429，如何快速缓解？” | 方案 A（短期）：用 `model management` 提升对应 `model_id` 的全局 TPM 上限<br>方案 B（长期）：用 `model production` 为该模型申请 PTU 预留容量 | 方案 A 仅治标（共享资源池竞争仍存在）；方案 B 需预付费，但提供确定性吞吐保障 |
| “我要把内部大模型部署到百炼，并要求 GPU 资源完全独占、网络隔离” | 使用 `model production` 的 `plan=dtu` 部署方式，指定 `dtu_capacity` | DTU 仅支持华北2（北京）地域；需提前申请专属域名；RAM 权限需包含 `AliyunBailianFullAccess` |
| “我们每天要处理 10 万条用户评论摘要，不要求实时返回，追求最低成本” | 使用 `model high speed inference` 的 **Batch 推理**功能 | 输入需为 UTF-8 编码 JSONL；单文件 ≤50,000 行；媒体资源 URL 必须公网可访问；不返回 `reasoning_content` |
| “前端聊天界面要求首字响应 <300ms，但当前 `qwen-turbo` 延迟波动大” | 尝试切换至同系列 Prime 模型（如 `qwen3.8-flash-prime`）或申请 PTU 高速档位（`service_tier=ptu_fast`） | Prime 模型需显式指定 `model` ID；PTU 需先在控制台创建并获取专属 model code；两者均需使用 `maas.aliyuncs.com` 域名 |

> 💡 **最佳实践提示**：  
> - **权限最小化**：`model management` 接口需项目管理员权限，日常开发请使用具备 `model-deployment-read` 和 `model-management-read` 的最小化 RAM 策略，避免滥用 `AliyunBailianFullAccess`。  
> - **地域强约束**：模型部署（DTU/MU/PTU）与高性能调用（智能路由、Prime）均严格绑定地域（北京/新加坡），务必统一 API Key、OSS Bucket、Endpoint 域名的地域配置。  
> - **命名一致性**：`model production` 输出的 `deployed_model` code 是 `model management` 的唯一合法 `model_id`，切勿混用模型显示名（如 `"Qwen-Max"`）或原始基础模型 ID（如 `"qwen-max"`）。

## 被对比主题页

- [model management](../api/model-management.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


