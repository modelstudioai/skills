# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在特定任务或数据集上的性能表现。它支持自动化指标计算、多模型横向对比及结果可视化，帮助开发者快速验证模型效果并指导调优。该功能面向模型微调、[Prompt 工程](../concepts/prompt-engineering.md)和模型选型等典型开发场景。

## 支持的模型与功能

- 支持所有已在百炼平台部署的 LLM（包括通义千问系列、自定义微调模型及第三方接入模型）进行离线批量评测；
- 提供标准评测维度：准确率、鲁棒性、幻觉率、响应长度分布、推理耗时等，详见 [评测维度](https://help.aliyun.com/zh/model-studio/evaluation-metrics)；
- 支持自定义评测集（JSONL 格式）与 Prompt 模板注入，可复现真实业务场景下的模型行为。

## 关键参数

- `dataset_id`: 必填，指定评测数据集 ID（需提前上传至数据管理模块）；
- `model_id`: 必填，目标模型唯一标识；
- `metrics`: 可选，指定计算的指标列表（如 `["accuracy", "hallucination_rate"]`），默认启用全部基础指标；
- `timeout`: 可选，单条样本最大推理超时（单位秒），默认 60，最大支持 300；
- `concurrency`: 可选，并发请求数，默认 5，受模型实例规格限制。

## 使用方式

通过 REST API 或 SDK 调用 `/v1/evaluations` 接口提交评测任务：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/evaluations \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "dataset_id": "ds-xxx",
        "model_id": "qwen-max",
        "metrics": ["accuracy"]
      }'
```
任务提交后返回 `evaluation_id`，可通过 `GET /v1/evaluations/{id}` 查询状态与结果。详细接口规范见 [模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)。

## 限制和注意事项

- 单次评测任务最多支持 10,000 条样本；超量需分批提交；
- 自定义指标需通过 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md) 中描述的插件机制注册，否则将被忽略；
- 评测结果中的“幻觉率”基于规则+LLM 判定双校验，但对非事实类任务（如创意生成）不适用——此点与 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md) 的通用说明存在口径差异，> **注意**：实际使用中请以 [原文标题](../../raw/model-user-guide/model-evaluation-introduction.md) 中最新标注的适用范围为准；
- 不支持实时流式响应评测；所有样本按完整输出进行指标计算。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


