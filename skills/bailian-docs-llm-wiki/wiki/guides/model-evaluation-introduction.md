# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务或数据集上的表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与效果归因分析。评测流程基于标准输入输出协议，兼容平台托管模型与用户自定义模型。

## 支持的模型与功能

- 支持所有已接入百炼平台的[通义千问系列模型（Qwen）](../../raw/model-user-guide/model-evaluation-introduction.md)，包括 Qwen1、Qwen2、Qwen2.5 及 Qwen3；  
- 支持用户上传的私有模型（需符合 vLLM 或 Triton 推理服务规范），通过 API endpoint 注册后参与评测；  
- 功能覆盖：单轮问答、多轮对话、指令遵循、代码生成、数学推理等 8 类标准任务模板，具体维度详见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `dataset_id` | string | 是 | 数据集唯一标识，须为平台预置或已上传的数据集 ID |
| `model_id` | string | 是 | 模型 ID（平台模型）或 `custom://<endpoint>`（自定义模型） |
| `metrics` | list[string] | 否 | 指定计算的指标，如 `["accuracy", "bleu", "rouge_l"]`；默认使用该任务类型的全量指标 |
| `max_concurrency` | int | 否 | 并发请求数，默认 4，最大 16（受配额限制） |

> **注意**：原始文档中提到“支持 Qwen-VL 多模态模型评测”，但当前版本（v2.3.0）尚未开放视觉输入解析能力，该描述已过时，请以 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) 中的运行时兼容性列表为准。

## 使用方式

1. 通过控制台「模型评测」模块创建评测任务，或调用 REST API `/v1/evaluations` 提交 JSON 请求体；  
2. 评测任务提交后返回 `evaluation_id`，可通过 `/v1/evaluations/{id}` 轮询状态；  
3. 完成后下载结构化报告（JSON/CSV），含逐样本预测、指标汇总及统计显著性检验（p<0.05）。  
完整接口定义与示例见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- 单次评测数据集样本数上限为 10,000 条；超限需分批提交并手动聚合；  
- 自定义模型 endpoint 必须支持 OpenAI 兼容协议（`/v1/chat/completions`），且响应中包含 `choices[0].message.content` 字段；  
- 所有评测均在隔离沙箱中执行，不缓存原始输入数据，但中间推理日志保留 7 天供调试 —— 详情参见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


