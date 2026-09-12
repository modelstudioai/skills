# model data overview

模型数据是百炼平台对训练集与评测集的统一管理能力，支撑模型调优、评测及数据增强等核心场景。它提供数据集全生命周期管理（创建、版本控制、发布）和可视化数据流处理能力，所有操作均通过百炼控制台「数据管理」页面完成。该功能面向开发者设计，强调可复现性与协作性。

## 支持的模型/功能

- **数据集类型**：明确区分**训练集**（用于[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)）和**评测集**（用于[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)），二者在用途、使用流程和权限约束上不同。  
- **数据流处理**：支持通过可视化画布进行清洗与增强，适用于预处理阶段的数据转换；相关能力详见 [数据清洗或增强](https://help.aliyun.com/zh/model-studio/data-processing)。  
- **统一管理入口**：所有数据集与数据流操作集中于控制台 [百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)，该页面为实际操作唯一权威入口，其功能定义以 [原文标题](../../raw/model-user-guide/model-data-overview.md) 为准。

## 关键参数

- **数据集元信息**：包括名称、类型（训练集/评测集）、最新版本号、数据量（行数）、导入状态、发布状态、存储位置（OSS 路径）、导入方式（控制台上传/URL 导入/API 批量导入）。  
- **版本控制机制**：每次新增版本即生成不可变快照，支持回滚与对比；版本发布后方可被模型调优或评测任务引用。  
- **发布状态语义**：仅已发布的数据集版本可用于生产级任务；未发布版本仅限调试与验证，此行为在 [原文标题](../../raw/model-user-guide/model-data-overview.md) 中明确定义。

## 使用方式

1. 登录百炼控制台，进入 [百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)；  
2. 在「数据集」Tab 点击右上角**创建数据集**，选择类型（训练集/评测集），完成基础配置与文件导入；  
3. 后续通过「操作」列的「新增版本」更新内容，再点击「发布」使其生效；  
4. 如需清洗或增强，切换至「数据流」Tab 搭建处理流程，并将输出结果导出为新数据集版本。  
> **注意**：API 创建数据集时必须显式指定 `dataset_type` 字段（`training` 或 `evaluation`），而控制台 UI 默认强制选择，该约束未在 [原文标题](../../raw/model-user-guide/model-data-overview.md) 中说明，但已在 OpenAPI 文档 v20240610 版本中补充，开发者应以 API 规范为准。

## 限制和注意事项

- 单个数据集最大支持 1000 万行文本样本（按 UTF-8 编码行计数），超限需分拆或采样；  
- 数据集发布后不可编辑内容，仅能新增版本；删除数据集将级联清除其所有历史版本与关联数据流节点；  
- 日志回流产生的反馈数据（如人工标注、badcase）暂不自动归入任一数据集，需手动导入并标记用途，此能力边界参见 [日志回流](https://help.aliyun.com/zh/model-studio/model-log-backflow) 文档说明。

## 来源文档

- [模型数据](../../raw/model-user-guide/model-data-overview.md)


