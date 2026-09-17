# model data [overview](overview.md)

模型数据是百炼平台对训练集与评测集的统一管理能力，支撑模型调优、评测及数据增强等关键任务。它提供数据集全生命周期管理（创建、版本控制、发布）和可视化数据流处理能力，所有操作均通过百炼控制台「数据管理」页面完成。该功能面向开发者设计，聚焦数据可用性、可追溯性与可复用性。

## 支持的模型/功能

- **数据集类型**：明确区分**训练集**（用于[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)）和**评测集**（用于[模型评测](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)），二者在用途、格式校验规则和发布流程上存在差异。
- **核心功能模块**：
  - **数据集管理**：支持创建、导入（支持 CSV/JSONL）、多版本快照、发布（仅发布版本可用于训练/评测）、删除；
  - **数据流**：基于可视化画布进行清洗与增强（如去重、格式标准化、[prompt](prompt.md) 模板注入），详见[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - **日志回流**：支持将线上推理日志自动回流为新数据集，用于持续迭代，具体机制见[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `dataset_type` | 必填，取值为 `training` 或 `evaluation` | 决定后续可用的训练/评测任务类型，创建后不可修改 |
| `version` | 自动递增的语义化版本号（如 `v1.0.0`），首次创建默认为 `v1.0.0` | 同一数据集下版本不可重复；未发布的版本不可被任务引用 |
| `max_size` | 单数据集最大容量 | 免费版上限 100 MB，企业版默认 10 GB（可申请提升） |
| `schema` | JSON Schema 校验规则（仅评测集强制启用） | 训练集 schema 校验为可选，但推荐启用以保障 fine-tuning 输入一致性 |

> **注意**：原始文档中提及“导入方式”列为数据集列表字段，但当前 API 和控制台实际不暴露该字段的可读值；真实导入来源需通过 `created_by` 和操作日志追溯，此为文档过时描述，以[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)中最新接口定义为准。

## 使用方式

1. **控制台入口**：访问 [百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)，切换至「数据集」Tab 创建或管理；
2. **API 集成**：调用 `CreateDataset` / `PublishDatasetVersion` 等 OpenAPI（参考[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)）；
3. **数据流编排**：在「数据流」Tab 中拖拽组件（如 Filter、Mapper、Sample），连接形成 DAG，保存后可一键触发执行或绑定至数据集版本。

## 限制和注意事项

- 数据集名称需全局唯一且符合 `[a-z0-9][a-z0-9\-]{1,62}[a-z0-9]` 正则，不支持中文与特殊字符；
- 已发布的数据集版本不可编辑或删除，仅能新增版本并重新发布；
- 评测集必须通过 `publish` 操作才可用于模型评测任务，未发布版本在评测任务配置中不可见；
- 数据流执行失败时，错误日志仅保留最近 7 天，建议及时导出关键中间结果；
- 所有数据存储于用户所属地域的 OSS Bucket，跨地域训练/评测任务需确保数据与模型部署地域一致，否则会触发隐式跨域拷贝并产生额外费用。

## 来源文档

- [模型数据](../../raw/model-user-guide/model-data-overview.md)


