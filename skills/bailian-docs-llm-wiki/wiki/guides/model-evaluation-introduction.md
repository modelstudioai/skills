# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务或数据集上的性能表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与上线前验证等典型研发场景。该功能基于标准化评测框架构建，开发者可通过 API 或控制台快速启动评测任务。

## 支持的模型/功能

- 支持所有已在百炼平台部署并启用推理服务的模型（包括 SFT 微调后模型与 RAG 增强模型），但不支持未发布至生产环境的草稿模型；  
- 提供预置评测集（如 MMLU、CMMLU、C-Eval、AlpacaEval 中文子集）及自定义数据集上传能力；  
- 支持单模型单轮评测、多模型并行评测、A/B 对比评测三种模式，详情见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)；  
- 评测维度覆盖准确性、鲁棒性、安全性、响应一致性等，具体指标定义参见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_ids` | string[] | 是 | 待评测模型 ID 列表，最多支持 5 个模型并发评测 |
| `dataset_id` | string | 是 | 数据集 ID（平台内置或用户上传），需已通过数据校验 |
| `metrics` | string[] | 否 | 指定计算的指标，如 `["accuracy", "bleu", "toxicity_score"]`；留空则使用该数据集默认指标集 |
| `max_new_tokens` | integer | 否 | 生成长度上限，默认为 512；注意部分指标（如 `exact_match`）对截断敏感，详见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |

> **注意**：原始文档中 `model-evaluation-overview.md` 提到支持“历史版本模型回溯评测”，但当前 API v2.3 实际不支持指定 `model_version` 字段，该能力尚未上线，属文档过时内容。

## 使用方式

1. **控制台操作**：进入「模型管理 → 评测中心」，选择模型与数据集，配置参数后提交任务；  
2. **API 调用**：调用 `POST /v2/evaluations`，请求体需符合 OpenAPI Schema（参考 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)）；  
3. **结果获取**：任务完成后，可通过 `GET /v2/evaluations/{id}` 获取结构化 JSON 报告，含各指标原始值、置信区间及样例输出。

## 限制和注意事项

- 单次评测数据集样本数上限为 2000 条（超限需分批提交）；  
- 自定义数据集仅支持 JSONL 格式，每行必须包含 `input` 和 `reference` 字段（`reference` 可为空字符串，但字段不可缺失）；  
- 安全类指标（如 `toxicity_score`）依赖独立鉴权服务，若未开通内容安全模块，对应指标将返回 `null` 且不计入汇总得分；  
- 评测任务最长运行时间为 6 小时，超时自动终止，建议复杂模型搭配小规模采样集先行验证。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


