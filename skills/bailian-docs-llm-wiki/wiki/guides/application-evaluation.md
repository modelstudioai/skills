# application evaluation

应用评测是百炼平台提供的核心质量保障能力，用于系统性评估大模型应用在真实业务场景下的输出质量、稳定性与合规性。支持自动评测与人工评测双模式，可基于预置或自定义评测集对应用进行多维度打分。该能力深度集成于应用开发工作流，适用于上线前验证与迭代优化阶段。

## 支持的模型/功能

- 支持所有已部署的百炼应用（包括基于 Qwen 系列、Qwen2 系列及第三方模型构建的应用）；
- 提供两类评测模式：[自动评测](../../raw/application-user-guide/application-evaluation.md)（基于规则/模型打分）和 [人工评测](../../raw/application-user-guide/application-evaluation.md)（支持多人协同标注与审核）；
- 支持评测集管理，包括导入/导出测试用例、设置期望输出、配置评测维度（如准确性、安全性、流畅性等），详见 [评测集](../../raw/application-user-guide/application-evaluation.md) 文档。

## 关键参数

- `dataset_id`：必填，指定待评测的评测集 ID（可通过控制台或 API 获取）；
- `evaluation_config`：JSON 对象，定义评测策略，含 `scoring_method`（`rule_based` / `llm_judge`）、`judge_model`（仅当 `scoring_method=llm_judge` 时生效，支持 `qwen-max`, `qwen-plus`）、`timeout_seconds`（默认 60）；
- `concurrency`：并发请求数，最大值为 10（超出将被限流）。

## 使用方式

1. **控制台操作**：进入「应用详情页 → 评测」标签页，选择评测集并启动自动评测；人工评测需先分配任务至成员；
2. **API 调用**：调用 `POST /applications/{app_id}/evaluations`，传入上述关键参数；
3. **结果查看**：评测报告包含整体得分、各维度分布、失败用例详情及原始输入/输出对比。新版评测界面与能力已在 [新版应用评测](../../raw/application-user-guide/application-evaluation.md) 中统一说明。

## 限制和注意事项

- 单次自动评测最多支持 500 条测试用例；超量需分批提交；
- `llm_judge` 模式下，若未显式指定 `judge_model`，系统默认使用 `qwen-plus`，但部分旧版 SDK 默认回退至 `qwen-turbo`，> **注意**：该行为已在 v3.2.0+ SDK 中修正，旧版本可能产生不一致评分，请升级 SDK 或显式指定模型；
- 人工评测任务一旦发布不可撤回，且标注结果不可批量修改；
- 评测过程中应用必须处于「已发布」状态，草稿态应用无法触发评测流程。

## 来源文档

- [应用评测](../../raw/application-user-guide/application-evaluation.md)



