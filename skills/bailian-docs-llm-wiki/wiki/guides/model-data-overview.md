# model data overview

模型数据是百炼平台对训练集与评测集的统一管理能力，支撑模型调优、评测及数据增强等核心场景。它提供数据集全生命周期管理（创建、版本控制、发布）和可视化数据流处理能力，所有操作均通过百炼控制台「数据管理」页面完成。该功能面向开发者设计，强调可复现性与协作性。

## 支持的模型/功能

- **数据集类型**：明确区分**训练集**（用于[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)）和**评测集**（用于[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)），二者在用途、使用流程和权限约束上不同。  
- **数据流处理**：支持通过可视化画布进行清洗与增强，适用于预处理阶段的数据转换；相关能力详见 [数据清洗或增强](https://help.aliyun.com/zh/model-studio/data-processing)。  
- **统一管理入口**：所有数据集与数据流操作均集成于控制台 [百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)，该页面为唯一权威操作界面，对应原始文档 [模型数据](../../raw/model-user-guide/model-data-overview.md)。

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| 数据集名称 | 全局唯一标识符，建议语义化命名（如 `finance_qa_v2_train`） | 创建后不可修改 |
| 类型 | 必选：`training` 或 `evaluation` | 类型决定后续可绑定的模型任务，见 [训练集与评测集](../../raw/model-user-guide/training-set-and-evaluation-set.md) |
| 版本号 | 自动递增（如 `v1`, `v2`），每次新增版本生成新快照 | 不支持手动指定；历史版本只读 |
| 发布状态 | `unpublished` / `published`；仅 `published` 版本可用于模型训练或评测 | 发布即锁定，不可编辑，需新建版本再修改 |
| 存储位置 | 默认为用户专属 OSS Bucket（路径格式：`oss://<bucket>/bailian/<workspace-id>/data/<dataset-id>/`） | 不支持自定义路径，但可通过 OSS 控制台直接访问 |

## 使用方式

1. **创建数据集**：在控制台「数据集」Tab 点击右上角「创建数据集」，选择类型、上传文件（支持 JSONL/CSV/TXT）、填写元信息；  
2. **新增版本**：在数据集操作列点击「新增版本」，上传新数据或调整字段映射；  
3. **发布版本**：在目标版本行点击「发布」，系统校验格式与必填字段（如 `input`/`output` 字段存在性）；  
4. **接入模型任务**：在模型调优或评测配置页中，下拉选择已发布的数据集版本；  
5. **构建数据流**：切换至「数据流」Tab，拖拽组件（如 JSONL 解析、字段过滤、Prompt 模板注入）并连线执行，结果可导出为新数据集版本 —— 此流程详细说明见 [数据清洗或增强](../../raw/model-user-guide/data-processing.md)。

## 限制和注意事项

- 单数据集最大支持 1000 万条样本（JSONL 行数），超限需分拆或采样；  
- 数据集字段名不区分大小写，但推荐统一使用小写加下划线（如 `user_input`），避免与系统保留字段（`_id`, `__version`）冲突；  
- > **注意**：原始文档中提及“导入方式”列为数据集列表字段，但当前控制台实际已移除此列（v2024.07+），最新 UI 仅显示「导入状态」与「操作」；请以 [模型数据](../../raw/model-user-guide/model-data-overview.md) 中截图为准，文字描述存在滞后；  
- > **注意**：[训练集与评测集](../../raw/model-user-guide/training-set-and-evaluation-set.md) 文档指出评测集支持多轮对话格式（含 `history` 字段），但当前模型评测服务仅解析首层 `input`/`output`，`history` 字段被忽略 —— 此行为与文档描述不一致，建议暂勿在评测集中使用嵌套会话结构；  
- 日志回流（Log Backflow）产生的反馈数据**不可直接作为训练集使用**，需经人工审核与格式标准化后，通过「新增版本」导入；具体机制参见 [日志回流](../../raw/model-user-guide/model-log-backflow.md)。

## 来源文档

- [模型数据](../../raw/model-user-guide/model-data-overview.md)


