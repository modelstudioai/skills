# 模型可观测性对比：Model Evaluation Introduction vs Model Monitoring vs Application Evaluation

## 背景与目的  
在大模型应用研发全生命周期中，“可观测性”是保障质量、提升迭代效率与支撑规模化落地的关键能力。百炼平台围绕不同阶段、不同对象、不同目标，提供了三类互补但定位清晰的可观测能力：  
- **Model Evaluation Introduction**（模型评测）聚焦 *离线、静态、任务级* 的模型能力验证，服务于模型选型、微调效果验证与 [Prompt 工程](../concepts/prompt-engineering.md)优化；  
- **Model Monitoring**（模型监控）聚焦 *在线、实时、系统级* 的服务运行态观测，服务于稳定性保障、容量治理与故障根因分析；  
- **Application Evaluation**（应用评测）聚焦 *端到端、场景化、业务闭环* 的应用效果度量，服务于提示链（Prompt Chain）、RAG 应用、Agent 工作流等复合体的质量门禁与持续优化。  

本页旨在从技术视角系统对比三者的核心差异，帮助开发者根据实际需求快速完成技术选型，避免能力误用或观测盲区。

---

## 关键维度对比表

| 维度 | Model Evaluation Introduction（模型评测） | Model Monitoring（模型监控） | Application Evaluation（应用评测） |
|------|------------------------------------------|-----------------------------|-------------------------------------|
| **核心目标** | 评估模型在**特定任务/数据集**上的固有能力表现（What can the model do?） | 监测模型 API 在**真实线上流量**下的运行健康状态（Is the model serving well?） | 评估**完整应用逻辑**（含 Prompt、工具调用、后处理等）在**业务场景**中的端到端效果（Does the app solve the user’s problem?） |
| **观测对象** | 单一 LLM 实例（`model_id`） | 单一已部署模型的 API 接口（`model_id` + endpoint） | 完整大模型应用（`application_id`），可包含多模型协同、[函数调用](../concepts/function-calling.md)、条件分支等 |
| **输入格式** | JSONL 格式评测集（每行含 `input` 和可选 `expected_output`）；支持 Prompt 模板注入 | 无显式“输入集”；自动采集所有符合 `model_id` 的生产请求（含 `input`, `parameters`, `headers` 等原始调用上下文） | JSONL 或控制台上传的结构化评测集（`input` 支持字符串/JSON 对象；支持多轮对话历史 `messages` 字段） |
| **输出格式** | 结构化评测报告（JSON）：含各指标聚合值（如 `accuracy: 0.82`）、样本级明细（`per_sample_results`）、可视化图表链接 | 分钟级聚合时序指标（JSON）：如 `RequestCount`, `P95LatencyMs`, `ErrorRate`, `InputTokenSum`, `OutputTokenSum`；支持 CSV 导出 | 多层级结果：① 任务级汇总（`overall_score`, `pass_rate`）；② 样本级打分（`score`, `reason`, `trace_id`）；③ 人工标注结果（含评分分布、一致性统计） |
| **支持模型** | ✅ 所有已部署 LLM（含通义系列、自定义微调模型、第三方接入模型）<br>❌ 不支持工作流内嵌子模型 | ✅ 所有**已启用 API 访问**的部署模型<br>❌ 不支持仅用于内部工作流、未暴露独立 endpoint 的模型实例 | ✅ 所有已发布的应用（无论底层是否为单模型、RAG、Agent 或多跳编排）<br>✅ 支持跨模型调用链路追踪（通过 `trace_id` 关联） |
| **API 端点** | `POST /v1/evaluations`（提交任务）<br>`GET /v1/evaluations/{id}`（查状态/结果） | `POST /api/v1/monitoring/describe`（OpenAPI `DescribeModelMonitoringData`）<br>控制台「监控」页签为默认入口 | `POST /v1/evaluation-jobs`（提交评测作业）<br>`GET /v1/evaluation-jobs/{job_id}/results`（获取结构化结果） |
| **执行模式** | 离线批量异步执行（非实时）；单任务串行/并发处理样本 | 全自动实时采集（延迟 1–3 分钟）；无主动“启动”动作 | 异步执行（自动评测）或半同步（人工评测需人工介入）；支持断点续跑与并发控制 |
| **计费方式** | 按**评测任务消耗的推理 [Token](../concepts/token.md) 总量**计费（同模型调用计费规则）；不额外收取评测服务费 | **免费**（基础监控能力默认启用）；告警通知、高级分析（如异常检测）可能涉及额外费用 | 按**评测过程中实际触发的应用调用所消耗的 [Token](../concepts/token.md) 总量**计费；人工评测环节不产生 [Token](../concepts/token.md) 费用 |
| **典型场景** | • 微调前后模型效果对比<br>• Prompt A/B 测试<br>• 新模型上线前基准测试（vs Qwen-Max/Qwen-Plus）<br>• 幻觉率、鲁棒性等专项能力验证 | • SLO 达标监控（如 P95 延迟 ≤ 3s）<br>• 突发流量导致的错误率飙升告警<br>• Token 消耗异常分析（定位高成本输入模式）<br>• 多区域服务性能基线比对 | • RAG 应用答案准确率验收<br>• Agent 工作流任务完成率评估<br>• 多轮客服对话满意度自动化打分<br>• 上线前 QA 人工抽检流程集成 |
| **数据保留周期** | 评测结果永久存储（关联 `evaluation_id` 可长期访问） | **30 天**（原始分钟级聚合数据）；超期后不可查（需主动导出） | 评测作业结果默认保留 **90 天**；支持手动归档与 CSV/JSON 导出 |

---

## 适用场景建议（面向开发者的技术选型指南）

| 你的问题 | 推荐方案 | 关键理由 | 注意事项 |
|----------|-----------|-----------|-----------|
| “我刚微调了一个 Qwen 模型，想确认它在金融问答任务上是否比基线模型更准？” | ✅ **Model Evaluation Introduction** | 提供标准指标（accuracy/hallucination_rate）、支持自定义数据集与 Prompt 注入，专为模型能力横向对比设计。 | 需提前上传评测集；不反映线上并发压力下的性能衰减。 |
| “我们的客服应用最近错误率上升，用户投诉响应慢，如何快速定位是模型、网关还是下游工具的问题？” | ✅ **Model Monitoring** | 实时采集 P95 延迟、HTTP 错误码、模型内部错误率，并通过 `X-Bailian-Trace-ID` 关联全链路，是根因分析第一入口。 | 必须确保调用方透传 trace header；监控数据延迟 1–3 分钟，不适用于毫秒级故障诊断。 |
| “我们上线了一个基于 RAG 的合同审查应用，需要证明它能稳定识别关键条款并生成合规摘要——能否自动化验收？” | ✅ **Application Evaluation** | 将整个应用作为黑盒评测对象，支持多轮输入、自定义业务指标（如‘条款召回率’）、人工复核闭环，直接对齐业务价值。 | 自动评测不兼容[流式输出](../concepts/streaming-output.md)；若应用含强随机性（如 `temperature=1.0`），建议增加多次采样取平均。 |
| “我想对比两个不同 Prompt 版本在 1000 条用户真实 query 上的效果差异” | ⚠️ **优先选 Application Evaluation**（若封装为应用）<br>✅ **Model Evaluation Introduction**（若直接调用模型） | 若 Prompt 已发布为正式应用 → 用 Application Evaluation 更贴近真实体验；若仅做 [Prompt 工程](../concepts/prompt-engineering.md)实验 → Model Evaluation 更轻量、指标更丰富（如幻觉校验）。 | Model Evaluation 不支持应用层后处理逻辑（如正则清洗、格式转换），可能导致指标失真。 |
| “我们需要向客户交付一份 SLA 报告，包含过去 7 天的可用性与性能数据” | ✅ **Model Monitoring** | 原生支持分钟级粒度、多维度（全局/API Key/IP）聚合查询，且控制台可一键导出 CSV，满足合规报告需求。 | Token 统计不含 system [prompt](../guides/prompt.md) 消耗，成本报告需额外校准。 |

---

## 总结：三者关系不是替代，而是协同

- **纵向分层**：`Model Monitoring`（基础设施层）→ `Model Evaluation Introduction`（模型能力层）→ `Application Evaluation`（业务价值层）构成可观测性金字塔；  
- **横向联动**：可将 `Model Monitoring` 中发现的异常时段（如某小时错误率突增），作为 `Application Evaluation` 的重点复测范围；也可用 `Model Evaluation` 的优质评测集，初始化 `Application Evaluation` 的基线任务；  
- **统一归因**：三者均依赖 `X-Bailian-Trace-ID` 实现跨系统链路打通，确保从一次用户请求出发，可下钻查看：监控指标 → 应用执行轨迹 → 底层模型推理日志与评测得分。

> 💡 **开发者行动建议**：  
> - 新项目启动时：**必开 Model Monitoring**（零成本，强依赖）；  
> - 模型/应用迭代期：**组合使用 Model Evaluation + Application Evaluation**，前者控“模型底线”，后者守“业务红线”；  
> - 生产环境巡检：**以 Model Monitoring 为哨兵，以 Application Evaluation 为裁判，以 Model Evaluation 为校准器**。

## 被对比主题页

- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [model monitoring](../guides/model-monitoring.md)
- [application evaluation](../guides/application-evaluation.md)


