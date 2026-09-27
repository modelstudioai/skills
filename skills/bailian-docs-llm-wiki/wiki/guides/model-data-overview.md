# model data [overview](overview.md)

模型数据是百炼平台对训练集与评测集的统一管理能力，支撑模型调优、评测及数据增强等核心场景。它提供数据集全生命周期管理（创建、版本控制、发布）和可视化数据流处理能力，所有操作均通过百炼控制台「数据管理」页面完成。该功能面向开发者设计，需结合具体模型任务类型选择对应数据集类型与格式。

## 支持的模型/功能

- **支持的模型任务类型**：当前仅支持文本生成类模型（如 Qwen 系列）的调优与评测，不支持多模态或语音模型的数据集接入。  
- **核心功能模块**：  
  - **数据集管理**：支持训练集与评测集的独立创建、多版本维护、发布/撤回、批量导入（CSV/JSONL 格式）及元数据标注；  
  - **数据流处理**：通过拖拽式画布实现清洗（去重、过滤非法字符）、增强（同义替换、模板扩写）等操作，详见 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；  
  - **日志回流集成**：支持将模型在线服务产生的推理日志自动回流为新数据集版本，用于迭代优化，具体配置见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `dataset_type` | 必填，取值 `training` 或 `evaluation` | 创建时指定，不可修改 |
| `version` | 数据集版本号，自动生成（如 `v1.0.0`），支持语义化版本命名 | 每次新增版本需显式提交变更 |
| `format` | 支持 `csv`、`jsonl`；`jsonl` 要求每行含 `prompt` 和 `completion` 字段（评测集可选 `reference`） | 不支持 Excel、Parquet 等格式 |
| `max_size` | 单数据集总容量上限 100 GB | 超限时上传失败，需清理旧版本或拆分数据 |

> **注意**：原始文档中提及“支持所有大模型相关数据集”，但实际仅验证通过文本生成类模型；图像/语音类模型的数据集接入尚未开放，该信息已在 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) 中明确限定适用范围。

## 使用方式

1. 登录百炼控制台，进入 [百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)；  
2. 在 **数据集** Tab 点击「创建数据集」，选择类型（训练/评测）、格式、存储位置（OSS Bucket），上传文件或粘贴样本；  
3. 完成后可在列表中执行「新增版本」更新数据，或点击「发布」使该版本可用于模型调优/评测任务；  
4. 如需预处理，切换至 **数据流** Tab，基于现有数据集创建处理流程，运行后生成新数据集版本。详细操作步骤参见 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- 单账号最多保留 50 个数据集（含已删除但未彻底清理的版本）；  
- 已发布的数据集版本不可编辑，仅能新增版本或撤回发布；  
- 数据集发布后，其字段结构（如 `prompt`/`completion` 字段名）必须与目标模型任务严格匹配，否则调优或评测任务启动失败；  
- OSS 存储路径需与百炼工作空间地域一致（如华北2），跨地域 Bucket 不可见；  
- 所有数据操作均受 RAM 权限控制，需授予 `bailian:ListDatasets`、`bailian:CreateDatasetVersion` 等最小必要权限。

## 来源文档

- [模型数据](../../raw/model-user-guide/model-data-overview.md)


