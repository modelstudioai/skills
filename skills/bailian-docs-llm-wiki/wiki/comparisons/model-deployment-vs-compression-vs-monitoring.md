# 模型交付全周期能力对比：部署、压缩与监控

为帮助开发者在模型上线前中后各阶段做出高效、可靠的技术决策，本文系统对比百炼平台三大核心交付能力——**模型部署**、**模型压缩**与**模型监控**——在关键工程维度上的能力边界、适用约束与协同关系。对比聚焦于生产落地最常关注的 7 个技术维度，覆盖从“能否用”（输入/输出兼容性）、“如何用”（API 与配置方式）、“是否划算”（计费逻辑）到“是否稳”（可观测性与风险控制）的完整链路，旨在为模型服务化选型提供可执行的参考依据。

> ⚠️ 重要前提说明：  
> - 三者非互斥能力，而是**正交叠加的分层能力**：部署是基础载体，压缩是性能增强选项，监控是运维保障底座；  
> - **所有能力均需依托已发布的模型版本（`model_id + version`）**，未发布模型不可直接部署/压缩/监控；  
> - 监控能力作用于**已部署的服务实例**（即 `deployment_id` 或 `model_code`），不监控未部署的模型或原始模型版本。

## 关键能力维度对比表

| 维度 | 模型部署（Deployment） | 模型压缩（Compression） | 模型监控（Monitoring） |
|------|------------------------|--------------------------|--------------------------|
| **核心目标** | 提供稳定、可扩展、可计费的模型推理服务入口 | 降低模型体积与推理延迟，提升单位算力吞吐效率 | 实时观测服务健康度、用量成本与异常行为，支撑稳定性治理 |
| **输入格式** | 模型 ID（如 `qwen2-7b`）、版本号（`v1`）、部署方案（`ptu`/`mu`/`lora`）及对应参数（如 `ptu_capacity`） | 已发布的模型 ID 与版本号 + `compression` 对象（含 `method`, `compute_type` 等） | 部署后的 `model_code`（如 `qwen2-7b-ptu-abc123`）或业务空间内 API Key；支持按时间范围、指标类型筛选 |
| **输出格式** | 返回 `deployment_id`、`model_code`、`endpoint` 及服务状态；调用时返回标准 OpenAI/DashScope 格式响应（含 `choices`, `usage` 等） | 返回带压缩标识的新 `model_code`（如 `qwen2-7b-int4-cpu-xyz789`），接口协议与原始模型完全一致，无额外字段 | 控制台图表（折线/柱状图）、结构化用量报表（CSV/Excel 下载）、告警通知（钉钉/邮件/Webhook）、SLS 日志（JSON 格式，含 `request_id`, `prompt_truncated`, `response_length` 等） |
| **支持模型范围** | ✅ 全系支持：<br>• 平台预置模型（Qwen/DeepSeek/GLM/VL 等）<br>• LoRA 微调模型（控制台导入或 API 调优生成）<br>• 白名单全参微调模型（需客户经理开通）<br>❌ 不支持未发布/未导入模型 | ✅ 有限支持：<br>• 仅 Qwen1.5 / Qwen2 / Qwen2.5 / Qwen-VL 的 **FP16 版本**<br>• `int4` 仅限文本模型（Qwen-VL 不支持 `int4`）<br>❌ 不支持 Llama、Phi、自定义架构或非 FP16 模型 | ✅ 广泛覆盖：<br>• 所有已在百炼模型列表可见的模型（含 LoRA、PTU/MU/Lora 部署实例）<br>• 用量统计：100% 支持<br>• 告警与深度监控：**语音/图片/视频/三方直连类模型不支持**（控制台灰显） |
| **API 端点** | `POST /api/v1/deployments`（创建）<br>`GET /api/v1/deployments/{id}`（查询）<br>`DELETE /api/v1/deployments/{id}`（下线） | `POST /api/v1/deployments`（在部署请求中嵌入 `compression` 字段）<br>⚠️ **无独立压缩 API**，必须与部署动作耦合 | `GET /api/v1/monitoring/usage`（用量）<br>`GET /api/v1/monitoring/metrics`（指标）<br>`POST /api/v1/alerts`（告警管理）<br>⚠️ 推理日志投递依赖 SLS OpenAPI，非百炼原生接口 |
| **计费方式** | • **PTU**：按预购 TPM 容量月结（无论是否使用）<br>• **MU/DTU**：按模型单元数量或 TPM 用量实时计费<br>• **[Token](../concepts/token.md) 按量**：按实际 [Token](../concepts/token.md) 数计费（`input_tokens` + `output_tokens`）<br>• **智能路由**：按实际执行模型计费 | **不单独计费**：压缩本身免费，但压缩后模型运行仍计入对应部署模式的计费（如 `qwen2-7b-int4-cpu` 在 PTU 下按 PTU 计费，在 MU 下按 MU 计费） | **不计费**：监控数据采集、存储、展示、告警触发均为平台免费能力；但 SLS 日志投递产生的存储与读写费用由用户承担（按阿里云 SLS 标准计费） |
| **典型场景** | • 高并发线上服务（PTU）<br>• 新模型灰度验证（DTU）<br>• 效果快速验证（[Token](../concepts/token.md) 按量）<br>• 多模型自动选优（智能路由） | • 边缘设备轻量化部署（CPU int4）<br>• 高吞吐低延迟 API 服务（CUDA int4）<br>• 成本敏感型批量推理任务（int8 降本约 35%） | • SLA 保障（失败率/延迟告警）<br>• 成本精细化分析（按 API Key / 模型 Code 用量归因）<br>• 安全审计（调用频次突增检测）<br>• 故障根因定位（首 Token 延时 vs 总耗时对比） |

## 各方案适用场景建议（面向开发者）

| 场景特征 | 推荐首选能力 | 关键理由 | 协同建议 |
|----------|--------------|----------|----------|
| **新模型上线验证期（< 1 周），关注效果而非性能** | ✅ Token 按量部署 | 零固定成本、按需付费、无需预估流量，避免 PTU/MU 的资源浪费；支持 LoRA 快速迭代验证 | 配合「用量统计」查看 Token 消耗分布，结合「审计日志」确认调用一致性；**暂无需开启推理日志或压缩** |
| **高稳定性要求的线上服务（如客服对话、搜索摘要）** | ✅ PTU 部署 + ✅ 全维度监控 | PTU 提供确定性容量与前缀缓存优化；监控提供分钟级失败率/首 Token 告警，满足 SLA 运维闭环 | 可选启用「推理日志」用于疑难问题复现；若延迟敏感，可在 PTU 实例上叠加 `int4` 压缩（需评估精度影响） |
| **大模型私有化部署（GPU 集群），需极致推理速度** | ✅ MU 部署 + ✅ CUDA int4 压缩 | MU 提供独占 GPU 资源保障；`int4+cuda` 在 A10/A100 上实测吞吐提升 1.7×，显著降低单请求成本 | 必须开启「性能监控」中的 `first_token_latency` 与 `total_latency` 对比，验证压缩收益；告警规则应包含 `429 错误次数`（限流感知） |
| **边缘端/低功耗设备部署（如车载、IoT 网关）** | ✅ CPU int4 压缩（绑定 PTU/MU 部署） | `int4` 模型体积缩减约 75%，CPU 推理延迟下降 40%+，适配 ARM/x86 低功耗环境 | 监控重点看 `rpm_limit` 是否成为瓶颈；建议关闭「推理日志」（避免带宽压力），保留「审计日志」做基础追踪 |
| **多模型 AB 测试或动态选型（如不同尺寸 Qwen）** | ✅ 智能路由部署 + ✅ 用量统计按 model_code 分析 | 一个 `auto-model-xxx` 接口自动路由至最优模型；用量统计可精确对比各候选模型的实际 Token 消耗与调用频次 | 需在智能路由调用时传入 `enable_thinking=true` 等参数引导选型；**不推荐对智能路由实例单独配置压缩或复杂告警**（路由逻辑会覆盖底层配置） |

## 技术选型决策 checklist（开发者自查）

请在实施前逐项确认：

- [ ] **部署前**：目标模型是否已成功 `publish`？LoRA 模型是否已完成 OSS 导入且满足 rank/目录约束？  
- [ ] **压缩前**：模型是否为 Qwen 系列 FP16 版本？是否已确认 `int4` 在长上下文场景下的精度衰减可接受（<0.8% BLEU）？  
- [ ] **监控前**：业务空间是否已完成[云监控服务角色授权](https://bailian.console.aliyun.com/cn-beijing/model/alert)？SLS 日志库是否已创建并具备写入权限？  
- [ ] **协同部署**：若需压缩，是否在 `model.deploy` 请求中**同时指定 `plan` 和 `compression`**？（例如 PTU 部署 + int4 压缩需传 `{"plan": "ptu", "ptu_capacity": {...}, "compression": {"method": "int4"}}`）  
- [ ] **调用一致性**：所有下游服务是否统一使用 `model_code`（而非原始 `model_id`）调用？智能路由是否严格使用 `auto-model-xxx` 格式？  
- [ ] **告警有效性**：所配置告警指标（如 `failure_rate`）是否在[监控告警文档](../../raw/model-user-guide/model-monitoring/model-telemetry.md)中标注为“支持告警”？是否设置合理持续时间（建议 ≥3 分钟防抖）？  

> 💡 **最佳实践提示**：  
> - **压测必做**：任何压缩配置上线前，务必使用真实业务流量进行 30 分钟以上压测，对比压缩前后 `failure_rate`、`first_token_latency` 与 `total_latency`；  
> - **监控先行**：新部署服务创建后 5 分钟内，应在控制台完成基础告警规则配置（至少包含失败率 >1% 和 TotalToken 突增 300%）；  
> - **版本隔离**：同一模型的不同压缩变体（如 `int4` 与 `int8`）必须使用不同 `model_code`，禁止混用，避免线上行为不可控。  

本对比基于百炼平台 v2.4.0 文档体系整理，能力细节请以控制台实时提示及最新版 [API 文档](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start) 为准。

## 被对比主题页

- [model deployment index](../guides/model-deployment-index.md)
- [model compression](../guides/model-compression.md)
- [model monitoring](../guides/model-monitoring.md)


