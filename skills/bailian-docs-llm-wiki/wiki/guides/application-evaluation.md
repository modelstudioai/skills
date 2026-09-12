# application evaluation

应用评测是百炼平台提供的核心质量保障能力，用于对部署后的 LLM 应用进行自动化或人工方式的效果验证与指标量化。支持基于预设评测集的批量打分、多维度指标（如准确性、安全性、流畅性）分析，以及结果可视化对比。该能力适用于模型迭代验证、A/B 测试及上线前合规审查等典型场景。

## 支持的模型/功能

- **自动评测**：调用平台内置评估模型（当前默认为 `qwen-plus-eval`）对应用响应进行零样本打分，支持自定义评分规则和阈值告警；详情见 [应用评测](../../raw/application-user-guide/application-evaluation.md)。  
- **人工评测**：提供标注工作台，支持多人协同标注、标签管理与一致性校验，适用于需语义理解或主观判断的复杂场景；参考 [人工评测](../../raw/application-user-guide/application-evaluation.md)。  
- **评测集管理**：支持上传结构化测试用例（JSONL 格式），包含输入、期望输出、权重与分类标签；评测集可复用、版本化，并与自动/人工流程绑定；详见 [评测集](../../raw/application-user-guide/application-evaluation.md)。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `dataset_id` | string | 必填，评测集唯一标识（通过 `/v1/datasets` 接口创建后获取） |
| `eval_mode` | string | 可选 `"auto"` 或 `"manual"`；自动模式下需指定 `eval_model`（如 `"qwen-plus-eval"`） |
| `metrics` | array | 可选，指定计算的指标列表，如 `["accuracy", "toxicity", "latency"]`；未指定时使用默认指标集 |
| `timeout_ms` | integer | 单条用例超时时间，默认 30000（30 秒），仅对自动评测生效 |

> **注意**：文档 [新版应用评测](../../raw/application-user-guide/application-evaluation.md) 中提及的 `eval_mode: "hybrid"` 模式目前尚未在 API v1.2 中开放，实际调用将返回 `400 Unsupported mode` 错误，请暂勿使用。

## 使用方式

1. **准备评测集**：通过控制台或 `/v1/datasets` 创建并上传测试数据；确保字段 `input` 和 `expected_output` 存在（人工评测可省略后者）。  
2. **发起评测任务**：调用 `POST /v1/applications/{app_id}/evaluations`，传入 `dataset_id` 与 `eval_mode` 等参数；示例请求见 [应用评测](../../raw/application-user-guide/application-evaluation.md)。  
3. **查询结果**：使用 `GET /v1/evaluations/{task_id}` 获取状态与聚合报告；原始明细可通过 `/v1/evaluations/{task_id}/results` 分页拉取。

## 限制和注意事项

- 单次自动评测任务最多支持 500 条用例；超量需拆分提交。  
- 评测集中的 `input` 字段长度上限为 8192 字符，超出部分将被截断且不触发报错。  
- 人工评测任务一旦启动，不可中途修改评测集内容；若需更新，须新建任务并重新分配标注员。  
- 所有评测任务默认保留 90 天，过期后原始响应与标注记录将被自动清理。  
- 当前不支持跨地域评测（例如华东1应用调用华北2评测模型），必须保证应用与评测资源位于同一 Region。

## 来源文档

- [应用评测](../../raw/application-user-guide/application-evaluation.md)


