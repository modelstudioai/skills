# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务上的性能表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与效果验收等典型场景。评测流程基于标准数据集与可配置的评估维度，开发者可通过 API 或控制台快速启动。

## 支持的模型/功能

- 支持所有已在百炼平台部署并启用推理服务的 LLM（包括通义千问系列、第三方接入模型等），需确保模型具备 `chat` 或 `completion` 接口能力  
- 提供预置评测任务：文本生成质量（BLEU、ROUGE）、事实一致性（FactScore）、指令遵循度（AlpacaEval 风格）、安全性（ToxiGen 检测）等  
- 支持自定义评测脚本（Python 函数），通过 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md) 中描述的 `custom_evaluator` 机制注入逻辑  

## 关键参数

- `dataset_id`: 必填，指定评测数据集 ID（需提前上传至数据管理模块）  
- `model_id`: 必填，目标模型唯一标识（如 `qwen-max-20240601`）  
- `metrics`: 可选，字符串数组，例如 `["bleu", "rouge_l", "fact_score"]`；完整列表见 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md) 的“评测维度”章节  
- `max_concurrency`: 控制并发请求数，默认为 5，过高可能触发限流  

## 使用方式

1. **控制台操作**：进入「模型评测」→「新建评测任务」→ 选择数据集与模型 → 配置指标 → 启动  
2. **API 调用**：调用 `POST /v1/evaluations`，请求体需包含上述关键参数；参考 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md) 提供的 OpenAPI 文档示例  
3. **结果获取**：评测完成后，返回 JSON 格式报告，含各指标分值、样本级明细及失败原因摘要  

## 限制和注意事项

- 单次评测最多支持 10,000 条样本；超量需分批提交  
- 自定义评测脚本须满足沙箱约束（无网络访问、CPU/内存限时），详见 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md) 的“安全限制”说明  
> **注意**：原始文档中提及的 `temperature=0.3` 为旧版默认采样参数，当前 v2.3+ 版本已移除此硬编码，默认由模型自身配置决定，实际调用时请勿显式传入该参数，否则将被忽略。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


