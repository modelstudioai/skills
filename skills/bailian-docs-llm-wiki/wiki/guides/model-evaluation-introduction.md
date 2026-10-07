# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务或数据集上的性能表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与效果验收等典型场景。该功能基于标准评测框架构建，开发者可通过 API 或控制台快速接入。

## 支持的模型/功能

- 支持所有已在百炼平台部署并启用推理服务的 LLM（包括 Qwen 系列、Qwen2 系列及第三方兼容模型）；
- 提供预置评测任务：文本生成质量（BLEU、ROUGE、BERTScore）、事实一致性（FactScore）、指令遵循度（AlpacaEval 风格）、安全性（ToxiGen 样式检测）等；
- 支持自定义评测集上传（JSONL 格式）与自定义指标脚本注入（Python 函数），详见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)；
- 多维度结果聚合与对比分析能力，覆盖单模型多轮次、多模型单任务、多模型多任务三种评测模式。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 百炼平台内注册的模型唯一标识（如 `qwen-max-20240815`） |
| `dataset_id` | string | 是 | 已上传至评测数据集管理的 ID，或内置数据集别名（如 `alpaca_eval_v2`） |
| `metrics` | list[string] | 否 | 指定计算的指标列表；默认使用该数据集关联的全量指标；支持值见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| `timeout` | int | 否 | 单样本推理超时（秒），范围 30–300，默认 120 |

> **注意**：`metrics` 参数若传入未在目标数据集 schema 中声明的指标，将被静默忽略——该行为与 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) 文档中“强制校验指标兼容性”的旧描述矛盾，以当前 API 实际行为为准。

## 使用方式

1. **控制台操作**：进入「模型管理 → 评测中心」，选择目标模型与数据集，配置参数后启动评测任务；
2. **API 调用**：调用 `POST /v1/evaluations`，请求体需符合 OpenAPI Schema（参见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)）；
3. **结果获取**：任务完成后，通过 `GET /v1/evaluations/{task_id}` 获取结构化 JSON 报告，含原始预测、标注、各指标分项值及统计摘要。

## 限制和注意事项

- 单次评测任务最大支持 10,000 条样本；超限需分批提交；
- 自定义指标脚本运行环境为 Python 3.10，依赖需显式声明于 `requirements.txt`，且总包体积 ≤ 50 MB；
- 评测过程中模型处于只读推理状态，不触发训练或权重更新；
- 内置数据集 `alpaca_eval_v2` 与 `factscore_zh` 的中文样本覆盖率存在差异，建议优先选用 `factscore_zh` 进行中文事实性评测——此结论依据 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) 中的最新数据集说明更新。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


