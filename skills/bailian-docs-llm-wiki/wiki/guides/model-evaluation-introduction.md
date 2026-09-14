# model evaluation introduction

模型评测是百炼平台提供的核心能力之一，用于系统性评估大语言模型在指定任务上的性能表现。它支持自动化执行多维度指标计算、结果可视化与对比分析，帮助开发者快速定位模型瓶颈并指导优化方向。该功能面向已部署或待上线的模型实例，适用于文本生成、问答、摘要等常见 NLP 任务。

## 支持的模型/功能

- 支持所有已在百炼平台完成部署的 LLM（包括 Qwen 系列、第三方接入模型），需满足输入输出格式为标准 JSONL（每行一个 `{"input": "...", "output": "...", "reference": "..."}` 样本）；  
- 提供预置评测集（如 CMMLU、C-Eval 子集）及自定义评测集上传能力；  
- 内置 8 类评测维度：准确性、流畅性、事实一致性、指令遵循度、安全性、偏见性、鲁棒性、时延（仅限在线服务模式）——详见 [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)；  
- 支持单模型单次评测、多模型横向对比、同一模型不同版本纵向追踪。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `dataset_id` | string | 是 | 评测数据集唯一标识，可通过 `/v1/datasets/list` 获取；参考 [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md) 中的数据集管理说明 |
| `model_id` | string | 是 | 待评测模型 ID（非模型名称），须为 `published` 状态；注意：`model_name` 字段**不被接受**，仅支持 `model_id` —— 此处与旧版文档 [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md) 中示例代码存在不一致，> **注意**：示例中误用 `model_name`，实际 API 仅校验 `model_id`，请以 OpenAPI 文档为准；  
| `metrics` | array[string] | 否 | 指定评测指标列表，如 `["accuracy", "faithfulness"]`；未指定则启用全部默认指标；  
| `timeout` | integer | 否 | 单样本推理超时（毫秒），默认 30000，最小值 5000。  

## 使用方式

1. 准备评测数据集（JSONL 格式，字段含 `input`、`output`（可选）、`reference`（必选））并上传至平台，获取 `dataset_id`；  
2. 调用评测任务创建接口：`POST /v1/evaluations`，传入 `model_id`、`dataset_id` 及其他参数；  
3. 轮询 `GET /v1/evaluations/{task_id}` 获取状态，`status: "completed"` 后下载报告（含原始打分、统计摘要、错误样例）；  
4. 批量任务支持通过 `batch_eval` 模式一次性提交多组 `(model_id, dataset_id)` 组合。

## 限制和注意事项

- 单次评测任务最大支持 10,000 条样本；超量需分批提交；  
- 自定义评测集需确保 `reference` 字段非空且语义完整，否则影响事实一致性等指标计算；  
- 安全性与偏见性指标依赖内置规则引擎，不支持用户自定义规则；  
- > **注意**：离线评测（`mode: "offline"`）仅支持同步返回结果，不生成持久化报告；若需存档，请显式设置 `save_report: true` —— 此行为在 [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md) 中未明确说明，但为实际生效逻辑。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction.md)


