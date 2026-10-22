# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务或数据集上的性能表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与效果归因分析。该功能基于标准评测框架构建，开发者可通过 API 或控制台快速接入。

## 支持的模型/功能

- 支持所有已在百炼平台部署并启用推理服务的 LLM（包括 Qwen 系列、Qwen2 系列及第三方兼容模型）；
- 提供预置评测模板（如通用对话、代码生成、数学推理等），也支持自定义 prompt 模板与评测数据集；
- 支持单次运行多模型对比、多轮次稳定性测试及分维度细粒度打分（如事实性、流畅性、安全性等）。  
详见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 关键参数

调用评测 API 时需指定以下关键参数：  
- `model_id`：目标模型唯一标识（必填）；  
- `dataset_id`：评测数据集 ID（支持内置数据集或用户上传的 JSONL 格式文件）；  
- `metrics`：指定计算的指标列表（如 `["accuracy", "bleu", "rouge_l"]`，默认启用基础指标）；  
- `timeout`：单条样本最大执行时间（单位秒，默认 60，上限 300）。  
完整参数说明见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 使用方式

1. **控制台操作**：进入「模型管理 → 评测中心」，选择模型与数据集，配置参数后启动评测；  
2. **API 调用**：使用 `POST /v1/evaluations` 接口提交评测任务，响应中返回 `evaluation_id` 用于轮询结果；  
3. **结果获取**：通过 `GET /v1/evaluations/{id}` 获取结构化报告（含汇总指标、样例输出、错误分布热力图）。  
详细流程请参考 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- 单次评测任务最多支持 1000 条样本；超量需分批提交；  
- 自定义数据集必须为 UTF-8 编码的 JSONL 文件，每行包含 `input` 和 `reference` 字段（`reference` 可为空）；  
- 评测过程中模型若返回 `rate_limit_exceeded` 错误，需检查模型配额或降低并发数；  
> **注意**：文档 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) 中列出的 `faithfulness` 指标在 v2.3.0+ 版本中已更名为 `factuality`，旧参数名将被弃用，请同步更新调用逻辑。  
- 不支持对未启用 streaming 的模型进行 token-level 指标（如 `perplexity`）计算。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


