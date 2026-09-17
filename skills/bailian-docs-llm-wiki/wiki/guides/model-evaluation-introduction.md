# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务或数据集上的性能表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与效果归因分析。该功能基于标准化评测框架构建，开发者可通过 API 或控制台快速接入。

## 支持的模型/功能

- 支持所有已接入百炼平台的 LLM（包括 Qwen 系列、第三方托管模型及用户自定义微调模型）；
- 提供预置评测任务：文本生成质量（BLEU、ROUGE、BERTScore）、事实一致性（FactScore）、指令遵循度（AlpacaEval 风格）、安全性（ToxiGen 检测）等；
- 支持自定义评测脚本与指标函数，通过 `custom_evaluator` 接口注入逻辑。详细维度说明见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 关键参数

- `dataset_id`: 必填，指定评测数据集 ID（需提前上传至数据管理模块）；
- `model_ids`: 必填，支持单个或多个模型 ID 数组，用于横向对比；
- `metrics`: 可选，指定计算的指标列表（如 `["bleu", "fact_score"]`），默认启用全部适配指标；
- `timeout`: 可选，单样本推理超时（秒），默认 60，最大 300；
- `max_samples`: 可选，限制评测样本数（防资源过载），默认全量，上限 10,000。参数详情请参考 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 使用方式

1. **API 调用**：发送 POST 请求至 `/v1/evaluations`，Body 包含上述参数（JSON 格式）；
2. **控制台操作**：进入「模型管理 → 评测中心」，选择模型与数据集，配置参数后启动；
3. **异步获取结果**：提交后返回 `evaluation_id`，轮询 `/v1/evaluations/{id}` 获取状态与报告。完整流程说明见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- 单次评测最多支持 5 个模型并发对比；
- 自定义指标函数须符合 Python 3.9+ 语法，且执行时间 ≤ 5 秒/样本；
- 数据集格式必须为 JSONL，每行含 `input` 和 `reference` 字段（`reference` 为可选，部分指标如 BLEU 强制要求）；
- > **注意**：文档中提及的 `batch_size` 参数在 v2.3.0+ 版本已废弃，实际由系统自动调度，勿在请求中显式传入；旧版 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) 中仍存在该参数说明，属过时内容。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


