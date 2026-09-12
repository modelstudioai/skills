# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在指定任务上的性能表现。它支持自动化指标计算、多模型横向对比及结果可视化，适用于模型选型、迭代优化与效果归因分析等典型场景。评测流程基于标准数据集与预设评估协议执行，确保结果可复现、可比较。

## 支持的模型/功能

- 支持所有已在百炼平台部署并启用推理服务的 LLM（包括 Qwen 系列、第三方接入模型等），需模型具备标准 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或百炼 native 接口；
- 提供文本生成类任务的完整评测链路：包括分类、摘要、问答、指令遵循（instruction following）、事实一致性（factuality）等 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md)；
- 内置 12+ 通用评测维度（如 BLEU、ROUGE、BERTScore、Exact Match、Self-Check GPT 等），同时支持用户自定义指标脚本（Python 函数）；  
- 支持单次评测运行跨模型、跨数据集、跨提示模板的组合实验，结果自动聚合至评测报告页。

## 关键参数

- `dataset_id`: 必填，指定评测所用数据集 ID（需提前上传并校验格式，详见 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md)）；
- `model_ids`: 必填，字符串数组，如 `["qwen-max", "qwen-plus"]`；
- `metrics`: 可选，指定启用的内置指标列表，如 `["rouge-2", "exact_match"]`；未指定则启用默认指标集；
- `max_samples`: 可选，限制评测样本数（默认全量，上限 5000）；
- `timeout`: 可选，单条样本推理超时（秒），默认 60，最大 300。

## 使用方式

1. 通过控制台：进入「模型评测」模块 → 创建评测任务 → 配置数据集、模型、参数 → 启动；
2. 通过 API：调用 `POST /v1/evaluations`，请求体为 JSON 格式，字段与上述关键参数一一对应；
3. 通过 SDK（Python）：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   req = bailian_models.CreateEvaluationRequest(
       dataset_id="ds-abc123",
       model_ids=["qwen-max"],
       metrics=["rouge-2"]
   )
   client.create_evaluation(req)
   ```
   完整参数说明见 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md)。

## 限制和注意事项

- 单次评测任务最多支持 5 个模型并发评估，超出需分批提交；
- 数据集格式必须为 JSONL，每行含 `input` 和 `reference` 字段（`reference` 可为空，但字段需存在）；
- > **注意**：原始文档中提及“支持[流式输出](../concepts/streaming-output.md)评测中间结果”，但当前 API 实际仅返回最终聚合报告，该描述已过时，以 SDK v2.3.0+ 行为为准；
- 评测任务状态轮询间隔不得小于 5 秒，高频轮询将触发限流（HTTP 429）；
- 自定义指标脚本须满足沙箱约束（无网络访问、CPU/内存受限、执行时间 ≤ 10s），否则任务失败。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


