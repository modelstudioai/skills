# model data overview

模型数据是百炼平台对训练集与评测集的统一管理能力，支撑模型调优、评测及数据增强等核心场景。它提供数据集的创建、版本控制、发布、删除等全生命周期操作，并通过数据流实现可视化清洗与增强。所有数据均按业务空间隔离，确保权限与存储边界清晰。

## 支持的模型/功能

- **数据集类型**：仅支持结构化文本数据集，分为**训练集**（用于[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)）和**评测集**（用于[模型评测](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)），二者在用途、格式校验规则及发布流程上存在差异。  
- **数据流能力**：支持基于可视化画布的数据清洗与增强，包括字段映射、过滤、采样、合成等节点；该能力不直接作用于原始模型推理，仅服务于数据准备阶段。详情见 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流集成**：支持将模型服务调用日志自动回流为评测候选数据，需配合[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)功能启用，适用于持续评估场景。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `dataset_type` | 必填，取值为 `training` 或 `evaluation` | 创建后不可修改 |
| `version` | 自动递增的语义化版本号（如 `v1.0.0`），每次新增版本时由系统生成 | 不支持手动指定或覆盖已有版本 |
| `max_size` | 单数据集最大容量为 100 GB（压缩后） | 超限时上传失败，需清理旧版本或拆分数据 |
| `row_limit` | 单文件行数上限为 500 万行 | 超出部分被截断，且不触发告警 |

> **注意**：原始文档中提及“数据集支持导入方式包括 CSV/JSONL/TXT”，但实际控制台仅接受 JSONL 格式（字段名必须含 `input` 和 `output`）；该不一致已在 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md) 的最新修订版中明确修正。

## 使用方式

1. 进入 [百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)，切换至 **数据集** Tab；  
2. 点击右上角 **创建数据集**，选择类型（训练集/评测集）、名称、描述，完成初始化；  
3. 上传数据文件（JSONL 格式），系统自动校验字段与编码，成功后生成 `v1.0.0` 版本；  
4. 如需更新，点击操作列的 **新增版本**，上传新文件并提交；  
5. 发布前须确保数据集已通过格式与内容校验（如评测集要求 `output` 字段非空），发布后版本不可编辑，仅可新增版本。完整流程详见 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。

## 限制和注意事项

- 数据集一旦发布，其当前版本即冻结，不可删除或修改；仅可通过新增版本迭代；  
- 同一业务空间下，训练集与评测集名称不可重名（即使类型不同）；  
- 数据流处理结果默认不自动保存为新数据集版本，需手动导出并创建新数据集；  
- 所有数据操作均受 RAM 权限控制，`AliyunBaiLianFullAccess` 是最低必要权限；  
- 删除数据集将同步清除其所有历史版本及关联数据流节点引用——该行为不可逆，请谨慎操作。

## 来源文档

- [模型数据](../../raw/model-user-guide/model-data-overview.md)


