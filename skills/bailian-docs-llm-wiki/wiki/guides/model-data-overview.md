# model data overview

模型数据是百炼平台对训练集与评测集的统一管理能力，支撑模型调优、评测及数据增强等核心场景。它提供数据集全生命周期管理（创建、版本控制、发布）和可视化数据流处理能力，所有操作均通过百炼控制台「数据管理」页面完成。该功能面向开发者设计，强调可复现性与工程化协作。

## 支持的模型/功能

- **数据集类型**：明确区分**训练集**（用于[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)）和**评测集**（用于[模型评测](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)），二者在用途、格式校验与发布流程上存在差异。
- **数据流处理**：支持通过可视化画布构建清洗与增强流程，适用于预处理、样本过滤、格式标准化等任务，详见[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流集成**：支持将模型服务调用日志自动回流为数据集候选样本，用于持续迭代，具体机制见[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 关键参数

- **数据集名称**：全局唯一，仅支持字母、数字、下划线和短横线，长度 1–64 字符。
- **数据量上限**：单个数据集版本最大支持 100 万条样本（文本类）；超限需分版本或使用数据流抽样。
- **版本管理**：每次新增版本会生成独立快照，已发布的版本不可修改；历史版本保留策略为最近 10 个活跃版本 + 所有已发布版本。
- **存储位置**：默认使用与业务空间同地域的 OSS Bucket，路径格式为 `oss://<bucket-name>/bailian/<workspace-id>/datasets/<dataset-id>/v<version>/`。

## 使用方式

1. 登录百炼控制台，进入 [百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)；
2. 在「数据集」Tab 点击右上角**创建数据集**，选择类型（训练集/评测集），填写元信息并上传初始数据；
3. 后续通过「操作」列的「新增版本」导入更新数据，或通过「数据流」Tab 构建处理链路后导出为新版本；
4. 发布前需确保数据格式符合对应场景要求（如评测集必须含 `input` 和 `output` 字段），发布后方可被调优或评测任务引用。

## 限制和注意事项

- 单次导入文件大小上限为 512 MB（CSV/JSONL），超限请拆分或使用 OSS 直传；
- 训练集与评测集不可互相转换类型，类型在创建时锁定；
- > **注意**：原始文档中提及“数据集分为训练集和评测集”，但[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)一文未说明字段级格式约束，而实际调优任务会校验 `messages` 或 `prompt/completion` 字段结构——请以控制台导入时的实时校验提示为准，该文档内容已滞后；
- 数据流节点不支持自定义 Python 脚本，仅提供内置清洗器（如去重、长度截断、正则过滤）和增强器（如同义词替换、模板扩增）；
- 已删除的数据集版本无法恢复，且其关联的模型调优任务若引用该版本将失败——建议删除前确认无依赖，详情参见[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 来源文档

- [模型数据](../../raw/model-user-guide/model-data-overview.md)


