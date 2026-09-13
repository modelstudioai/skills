# application evaluation

应用评测（Application Evaluation）是百炼平台提供的用于量化评估大模型应用效果的核心能力，支持通过预设评测集或自定义样本对应用的输出质量、稳定性与业务指标进行自动化或人工验证。评测结果可用于模型选型、提示词优化及服务上线前的质量门禁。该功能面向开发者提供可编程接口与控制台操作双路径支持。

## 支持的模型/功能

- **自动评测**：基于标准评测集（如 AlpacaEval、MT-Bench 子集）或用户上传的测试集，调用指定模型对应用输入批量生成响应，并按预置指标（如正确率、格式合规性、安全性）打分；支持多轮对话场景的链路级评估。  
- **人工评测**：提供标注界面与协作流程，支持多人对同一组输入-输出对进行主观评分（如 1–5 分），结果可导出用于统计分析。  
- **新版应用评测**：统一了自动/人工评测的数据模型与 API 接口，引入评测任务（EvaluationTask）和评测作业（EvaluationJob）两级抽象，支持异步执行、断点续跑与结果聚合。详见 [新版应用评测](../../raw/application-user-guide/application-evaluation.md)。

## 关键参数

- `dataset_id`：必填，指定评测数据集 ID（需提前在控制台创建或通过 `/datasets` API 上传）；支持公共评测集与私有数据集。  
- `application_id`：必填，被评测的应用唯一标识。  
- `evaluator_type`：取值 `"auto"` 或 `"manual"`；若为 `"auto"`，需额外指定 `metric_config`（JSON 字符串，定义指标类型与阈值）。  
- `timeout_seconds`：单条样本最大处理时长，默认 60 秒，超时将标记为 `FAILED`；该参数在 [自动评测](../../raw/application-user-guide/application-evaluation.md) 文档中明确要求不可超过 120 秒。  
- `max_concurrency`：并发请求数上限，影响评测吞吐量，但受账户配额限制（见下文“限制和注意事项”）。

## 使用方式

1. **准备评测集**：通过控制台或 `/v1/datasets` API 创建评测数据集，每条样本需包含 `input`（字符串或对象）与可选的 `expected_output` 字段。  
2. **发起评测任务**：调用 `POST /v1/evaluation-jobs`，传入 `application_id`、`dataset_id` 及其他参数；返回 `job_id` 用于轮询状态。  
3. **获取结果**：使用 `GET /v1/evaluation-jobs/{job_id}` 查询状态；完成后通过 `GET /v1/evaluation-jobs/{job_id}/results` 下载结构化报告（JSON/CSV）。  
完整流程示例见 [应用评测](../../raw/application-user-guide/application-evaluation.md) 中的快速入门章节。

## 限制和注意事项

- 单次评测任务最多支持 10,000 条样本；超出需拆分为多个 `EvaluationJob`。  
- 自动评测不支持[流式输出](../concepts/streaming-output.md)（`stream=true`）的应用配置；若应用启用流式，评测将失败并返回 `INVALID_CONFIG` 错误。  
- 免费版账户默认并发数为 2，专业版为 10；该配额无法通过工单提升，需升级套餐。  
> **注意**：原始文档中 [人工评测](../../raw/application-user-guide/application-evaluation.md) 描述支持“实时协同标注”，但当前 API v1.2 实际未开放 `collaborative_mode` 参数，该功能暂未上线，以 OpenAPI 文档为准。

## 来源文档

- [应用评测](../../raw/application-user-guide/application-evaluation.md)


