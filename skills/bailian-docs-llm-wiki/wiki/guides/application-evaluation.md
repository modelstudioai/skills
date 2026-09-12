# application evaluation

应用评测（Application Evaluation）是百炼平台提供的用于量化评估大模型应用效果的核心能力，支持通过预设评测集或自定义样本对应用的输出质量、稳定性、安全性等维度进行自动化或人工打分。该功能适用于模型选型、提示词优化、服务迭代等典型研发场景。评测结果可导出为结构化报告，便于团队协作分析。

## 支持的模型/功能

- **自动评测**：基于规则或参考答案对应用输出进行批量打分，支持准确率、召回率、BLEU、ROUGE-L 等指标；需应用已部署为可调用服务（HTTP endpoint 或 SDK 调用）。  
- **人工评测**：提供可视化标注界面，支持多人协同标注、标签管理与一致性校验，适用于主观性强或需领域专家判断的场景。  
- **评测集管理**：支持上传 CSV/JSONL 格式评测数据（含 input、expected_output、metadata），并复用 [评测集](../../raw/application-user-guide/application-evaluation-dataset.md) 中定义的标准数据集。新版评测功能已在 [新版应用评测](../../raw/application-user-guide/application-evaluation.md) 中统一入口，旧版自动/人工评测页面将逐步下线。  
> **注意**：[自动评测](../../raw/application-user-guide/application-evaluation.md) 文档中列出的旧版独立入口链接已失效，实际使用请以新版评测控制台为准。

## 关键参数

- `dataset_id`：必填，指定评测所用数据集 ID（可通过 `/v1/datasets/list` 获取）；  
- `model_id` 或 `app_id`：二选一，指定被评测的应用实例；  
- `metrics`：数组，如 `["accuracy", "latency_ms", "safety_score"]`，部分指标需启用对应插件；  
- `timeout_ms`：单条样本最大响应等待时间，默认 30000（30 秒）；  
- `concurrency`：并发请求数，免费版上限为 5，企业版可配置至 50。  
详细参数说明见 [新版应用评测](../../raw/application-user-guide/application-evaluation.md) 的 API 参考章节。

## 使用方式

1. 在控制台「应用管理 → 应用详情 → 评测」页创建评测任务；  
2. 选择评测类型（自动/人工）、目标应用及评测集；  
3. 配置参数（如指标、并发数），点击「启动评测」；  
4. 自动评测任务完成后生成报告，人工评测需完成标注后手动发布结果。  
SDK 调用示例（Python）：
```python
from alibabacloud_bailian20231229 import models as bailian_models
client = BailianClient(...)
req = bailian_models.CreateEvaluationJobRequest(
    dataset_id="ds-xxx",
    app_id="app-yyy",
    metrics=["accuracy", "latency_ms"]
)
resp = client.create_evaluation_job(req)
```
完整调用规范参见 [新版应用评测](../../raw/application-user-guide/application-evaluation.md)。

## 限制和注意事项

- 单次自动评测最多支持 10,000 条样本；超量需分批提交；  
- 人工评测任务不支持暂停/续标，创建后需一次性完成全部标注；  
- 评测过程中若应用服务不可达或返回非 200 响应，该样本标记为 `failed`，不计入有效得分；  
- 当前仅支持同地域内应用与评测服务通信（如华东1区应用只能被华东1区评测任务调用）；  
> **注意**：[自动评测](../../raw/application-user-guide/application-evaluation.md) 文档中提及的“支持跨地域评测”为历史版本描述，已于 v2.3.0 版本移除，当前行为以控制台实际限制为准。

## 来源文档

- [应用评测](../../raw/application-user-guide/application-evaluation.md)


