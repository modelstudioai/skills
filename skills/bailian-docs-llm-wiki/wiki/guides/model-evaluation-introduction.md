# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务或数据集上的表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与效果归因分析。所有评测功能均通过 API 调用或控制台交互触发，底层统一调用评测引擎执行。

## 支持的模型/功能

- 支持对百炼托管模型（如 qwen-max、qwen-plus）及用户自部署的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)模型进行评测  
- 支持的评测类型包括：单轮问答（QA）、多轮对话（Chat）、指令遵循（Instruction Following）、事实一致性（Factuality）等，具体维度详见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)  
- 提供内置基准数据集（如 CMMLU、C-Eval 子集）和自定义数据集上传能力；自定义数据格式需符合 JSONL 规范，每行包含 `input` 和 `expected_output` 字段  

## 关键参数

- `model_id`：必填，指定待评测模型 ID（如 `qwen-max`），不支持别名或版本通配符  
- `dataset_id`：必填，可为平台内置数据集 ID（如 `cmmlu-v1.0`）或用户上传数据集的 UUID  
- `metrics`：可选数组，指定计算的指标（如 `["accuracy", "rouge_l", "faithfulness"]`）；若为空则使用该数据集默认指标集  
- `max_workers`：并发请求数上限，默认 5，最大支持 20；超过限制将被限流，详见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)  

## 使用方式

1. **API 调用**：向 `POST /v1/evaluations` 提交评测任务配置，响应返回 `evaluation_id`，后续通过 `GET /v1/evaluations/{id}` 查询状态与结果  
2. **控制台操作**：进入「模型管理 → 模型评测」页面，选择模型、数据集、指标后点击「启动评测」  
3. 结果以结构化 JSON 返回，含 `summary`（整体指标）、`details`（逐样本预测与得分）、`error_cases`（低分样本抽样）三部分；原始日志可通过 `evaluation_id` 在对象存储中按路径 `eval-logs/{evaluation_id}/raw.jsonl` 获取，该路径约定见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)  

## 限制和注意事项

- 单次评测任务最多支持 10,000 条样本；超量需分批提交  
- 自定义数据集上传大小上限为 50 MB，且 `input` 字段长度不得超过 8192 token（按模型 tokenizer 计算）  
- > **注意**：文档 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) 中提及“支持流式返回中间结果”，但当前 v2.3.0 API 实际仅支持全量结果一次性返回，流式能力计划于 v2.4.0 版本上线  
- 评测任务默认保留 30 天，过期后 `evaluation_id` 不再可查；如需长期存档，请及时导出 JSON 结果  
- 所有评测均基于同步推理调用，不启用缓存；若模型响应超时（默认 120s），该样本标记为 `timeout` 并计入 `error_cases`

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


