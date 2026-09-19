# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务或数据集上的性能表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与效果验收等典型场景。所有评测功能均通过 API 调用或控制台配置触发，底层统一调用评测引擎执行。

## 支持的模型/功能

- 支持对百炼托管模型（如 `qwen-max`、`qwen-plus`）及用户自部署的兼容 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)的模型进行评测；  
- 支持的评测类型包括：单轮问答（QA）、多轮对话（Chat）、摘要生成（Summarization）、分类（Classification）等；  
- 内置 12+ 标准评测维度，涵盖准确性（Accuracy）、事实一致性（Fact Consistency）、有害性（Toxicity）、响应长度合理性等，详情见 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)；  
- 支持自定义评测数据集（JSONL 格式）与自定义评分规则（通过 Python 函数注入），参考 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 关键参数

- `dataset_id`: 必填，指定已上传的评测数据集 ID（需提前通过 `/v1/datasets` 接口创建）；  
- `model_id`: 必填，目标模型 ID（如 `qwen-max`）或自定义模型 endpoint 的别名；  
- `metrics`: 可选，字符串数组，指定需计算的指标（默认全量），例如 `["accuracy", "toxicity"]`；  
- `max_concurrency`: 可选，最大并发请求数（默认 5），影响评测吞吐与资源占用；  
- `timeout`: 可选，单条样本推理超时（秒，默认 60），超过将标记为 `TIMEOUT` 错误。

## 使用方式

1. **准备数据集**：上传符合 schema 的 JSONL 文件（每行含 `input` 和 `reference` 字段），获取 `dataset_id`；  
2. **发起评测任务**：调用 `POST /v1/evaluations`，传入 `dataset_id`、`model_id` 等参数；  
3. **轮询结果**：通过 `GET /v1/evaluations/{task_id}` 查询状态，`status=COMPLETED` 后可下载完整报告（含逐样本明细与聚合指标）；  
4. 所有操作亦可通过控制台「模型评测」模块完成，交互逻辑与 API 严格对齐，详见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- 单次评测任务最多支持 10,000 条样本；超出需分批提交；  
- 自定义模型 endpoint 必须支持 `chat.completions` 或 `completions` 接口，且返回格式需与 OpenAI 兼容（否则解析失败）；  
- > **注意**：原始文档中提及“支持流式响应评测”，但当前评测引擎仅消费最终响应（`choices[0].message.content`），不处理 `delta` 流；该描述已在 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) 的最新修订版中移除，请以实际 API 行为为准；  
- 评测任务默认保留 30 天，过期后结果不可查，建议及时导出；  
- 某些指标（如 Fact Consistency）依赖外部校验服务，若对应服务不可用，该指标将跳过并记录警告。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


