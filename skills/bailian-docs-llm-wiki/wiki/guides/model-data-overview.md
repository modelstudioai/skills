# model data overview

模型数据是百炼平台对训练集与评测集的统一管理能力，支撑模型调优、评测及数据增强等核心场景。它提供数据集全生命周期管理（创建、版本控制、发布）和可视化数据流处理能力，所有操作均通过百炼控制台「数据管理」页面完成。该功能面向开发者设计，强调可复现性与工程化协作。

## 支持的模型/功能

- **数据集类型**：明确区分**训练集**（用于[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)）和**评测集**（用于[模型评测](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)），二者在用途、格式校验与发布流程上存在差异。
- **数据流处理**：支持通过可视化画布构建清洗与增强流程，例如字段映射、样本过滤、文本标准化等，具体能力详见[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流集成**：支持将线上推理日志自动回流为新数据集版本，用于持续迭代，相关机制见[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 关键参数

- **数据集名称**：全局唯一，仅支持字母、数字、下划线和短横线，长度 2–64 字符。
- **数据量上限**：单个数据集版本最大支持 100 万条样本；总存储容量受业务空间配额约束。
- **版本标识**：自动按 `v1`, `v2`, … 递增；发布后版本不可修改，仅可新增版本。
- **发布状态**：未发布的数据集无法被模型调优或评测任务引用；发布即生成只读快照。

## 使用方式

1. 登录百炼控制台，进入 [百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)；
2. 在 **数据集** Tab 点击右上角「创建数据集」，选择类型（训练集/评测集），上传文件或配置 OSS 路径；
3. 数据导入完成后，可在列表中点击「新增版本」更新内容，或点击「发布」使其可用于下游任务；
4. 如需预处理，切换至 **数据流** Tab，拖拽组件构建流程并绑定目标数据集，运行后自动生成新版本——该流程说明见[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 限制和注意事项

- 训练集与评测集的 schema（如字段名、是否必需）由所选模型任务类型强约束，不匹配将导致任务提交失败；详细规则参见[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- > **注意**：原始文档中提及“数据集支持删除”，但当前控制台 UI 已移除「删除」操作按钮，仅保留「下线」（使历史版本不可用）；实际删除需提工单申请，此为平台策略变更，以控制台实际能力为准。
- 单次导入文件大小上限为 2 GB（ZIP 解压后），超限需拆分或使用 OSS 分片上传。
- 发布后的数据集版本不可撤销，若需修正，必须创建新版本并重新发布。

## 来源文档

- [模型数据](../../raw/model-user-guide/model-data-overview.md)


