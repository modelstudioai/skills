# application evaluation

应用评测是百炼平台提供的核心质量保障能力，用于对部署后的 AI 应用进行系统性效果验证。它支持自动化与人工双轨评测模式，覆盖准确性、鲁棒性、安全性等多维指标，并依托结构化评测集实现可复现的量化评估。该能力适用于模型上线前验收、迭代版本对比及 SLO 合规性审计等典型开发者场景。

## 支持的模型/功能

- **自动评测**：基于预置或自定义评测集，调用目标应用 API 批量执行推理并比对期望输出，支持准确率、响应时长、错误率等基础指标计算；详见 [应用评测](../../raw/application-user-guide/application-evaluation.md)。  
- **人工评测**：提供标注界面与协作流程，支持多人协同打分、添加评语、导出评审报告；其操作规范与权限配置说明见 [人工评测](../../raw/application-user-guide/application-evaluation.md)。  
- **评测集管理**：支持上传 CSV/JSONL 格式测试样本（含 input、expected_output、category 等字段），支持标签筛选与版本快照；完整格式要求与示例参见 [评测集](../../raw/application-user-guide/application-evaluation.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `dataset_id` | string | 是 | 评测集唯一标识，需通过 `/v1/datasets` 接口创建后获取 |
| `application_id` | string | 是 | 待评测应用 ID，必须为已发布状态 |
| `timeout_ms` | integer | 否 | 单条请求超时阈值，默认 30000（30 秒） |
| `metrics` | array | 否 | 指定计算的指标列表，如 `["accuracy", "latency_p95", "safety_violation_rate"]`；未指定则启用默认指标集 |

> **注意**：新版应用评测（[新版应用评测](../../raw/application-user-guide/application-evaluation.md)）已将 `metrics` 参数从字符串改为数组类型，旧版 SDK 调用可能因参数格式不兼容而失败，请同步升级至 v2.3.0+。

## 使用方式

1. **准备评测集**：通过控制台或 `POST /v1/datasets` 创建评测集，确保字段符合 [评测集](../../raw/application-user-guide/application-evaluation.md) 规范；  
2. **发起评测任务**：调用 `POST /v1/evaluations`，传入 `application_id`、`dataset_id` 及可选参数；  
3. **查询结果**：使用 `GET /v1/evaluations/{id}` 获取实时状态与最终报告，支持按 `category` 或 `sample_id` 过滤明细。

## 限制和注意事项

- 单次评测任务最多支持 10,000 条样本；超量需分批提交；  
- 自动评测期间应用必须保持在线且具备公网可访问 endpoint（内网 VPC 部署需配置反向代理或白名单）；  
- 人工评测任务不支持 API 创建，仅可通过控制台发起；其生命周期管理逻辑与自动评测不同，详情见 [人工评测](../../raw/application-user-guide/application-evaluation.md)；  
- 评测结果缓存有效期为 30 天，过期后需重新运行任务。

## 来源文档

- [应用评测](../../raw/application-user-guide/application-evaluation.md)


