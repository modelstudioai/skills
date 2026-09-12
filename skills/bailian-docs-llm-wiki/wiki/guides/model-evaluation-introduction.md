# model evaluation introduction

模型评测是百炼平台中用于系统性评估大语言模型在特定任务上性能的核心能力，支持开发者通过标准化指标量化模型输出质量、鲁棒性与业务适配度。它适用于模型选型、迭代优化及上线前验收等关键研发阶段。评测流程基于结构化测试集与可配置的评估维度，结果可导出用于横向对比。

## 支持的模型/功能

- 支持所有已在百炼平台部署并启用 API 调用的 LLM（包括通义千问系列、第三方接入模型），但不支持未发布或仅处于调试态的模型实例；  
- 提供预置评测模板（如问答准确性、指令遵循、安全性、幻觉检测）和自定义评测任务；  
- 支持多轮对话场景下的连贯性与上下文保持能力评估。详细能力说明见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)。

## 关键参数

- `dataset_id`：必填，指定评测所用的测试数据集 ID（需提前上传并标注）；  
- `metrics`：数组，指定评估指标，例如 `["accuracy", "toxicity_score", "latency_p95"]`，完整列表参见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction.md)；  
- `model_id` 或 `endpoint`：二者选一，用于标识被测模型；  
- `timeout`：单条样本最大推理等待时间（单位秒），默认 60，上限 300。

## 使用方式

1. 通过控制台「模型评测」模块创建评测任务，或调用 `/v1/evaluations` REST API 提交 JSON 请求体；  
2. 评测启动后，系统自动执行批量推理与指标计算，状态可通过 `GET /v1/evaluations/{id}` 查询；  
3. 完成后支持下载 CSV 报告及可视化图表。API 使用示例与字段说明详见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)。

## 限制和注意事项

- 单次评测任务最多支持 10,000 条样本，超量需分批提交；  
- 自定义指标函数需符合 Python 3.9+ 环境约束，且不可访问外网或持久化存储；  
- > **注意**：原始文档中提及“支持实时流式评测”，但当前 API 实际仅支持全量批处理模式，该描述已过时，请以 [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md) 中最新接口文档为准。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)



