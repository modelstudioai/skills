# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理。所有数据集均以结构化格式存储，并与下游调优、评测任务深度集成。数据质量直接影响模型效果，建议在调优前完成清洗与增强。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 与 CPT 仅限北京地域可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，用于模型泛化能力评估，不可用于训练 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：支持对已发布的 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）和增强（如 Few-Shot 生成），暂不支持 DPO、CPT 或视觉类训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志自动转化为结构化 JSONL 数据集，可用于训练集（SFT/DPO/CPT）或评测集，当前仅在北京和新加坡地域可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出数据处理“暂不支持[SFT-图片理解训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)和[DPO-文本生成训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)”，而文档 1 表述为“训练集支持4种训练场景”，未限定数据处理兼容性。此处以文档 2 的明确限制为准。

## 关键参数

| 参数 | 说明 | 必填 | 取值范围/约束 |
|------|------|------|----------------|
| 数据集类型 | 创建后不可变更 | 是 | `训练集` / `评测集` |
| 训练场景 | 仅训练集需填写 | 是 | `文本生成` / `视觉理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集固定为文本生成 |
| 训练方法 | 仅训练集需填写 | 是 | `SFT`（全地域）、`DPO` / `CPT`（仅北京） |
| 数据格式 | 影响导入解析逻辑 | 是 | `Jsonl 格式`（推荐） / `Excel 格式` |
| 存储位置 | 决定计费主体与管理方式 | 是 | `平台 OSS 存储`（免费，自动发布） / `云存储挂载`（需 OSS 授权，仅训练集可用） |
| 导入方式 | 决定前置条件与适用规模 | 是 | `本地上传`（无依赖） / `从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`） / `日志回流`（需 SLS 授权） / `API 上传`（需编程集成） |

- 数据集名称 ≤ 50 字符（支持中文、英文、数字、下划线、连字符、点）；描述 ≤ 200 字符。
- 日志回流时间范围严格限定为**最近 30 天内**，单次上限 10 万条；预估条数仅为近似值，实际结果可能略有差异 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data) → 点击**创建数据集** → 按向导填写参数 → 选择导入方式并上传/配置数据 → 点击**确认**（提交即发布，无草稿模式）。
2. **数据处理（仅 SFT 文本训练集）**：在 [数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow) 中创建数据流（含清洗/增强节点）→ 发布后，在**任务列表**中新建任务 → 选择目标训练集 → 启动任务。处理完成后自动生成新版本（如 V1 → V2），原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
3. **日志回流**：先在 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) 完成审计日志与推理日志的授权与开启 → 返回任一入口（模型监控页、详情页或数据管理页）→ 配置时间范围、API Key、模型等参数 → 提交。平台存储模式下导入完成即自动发布 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
4. **引用数据集**：下游模型调优 API 通过 `training_file_ids` 参数传入已发布数据集 ID；评测任务在控制台选择已发布评测集即可。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理功能、日志回流均**仅支持华北2（北京）地域**；日志回流额外支持新加坡地域 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **不可变性**：数据集类型、训练场景、训练方法、存储位置、数据格式一旦创建即锁定，不可修改。
- **发布与删除**：发布操作不可逆，已发布版本不可编辑；删除操作不可恢复，且会清除该数据集下所有版本，请谨慎执行 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **空数据集禁止创建**：系统拒绝创建或发布无数据的训练集/评测集。
- **OSS 挂载限制**：评测集不支持 OSS 挂载；OSS 挂载数据集不支持“新增版本”操作，追加数据须通过“导入数据”页完成 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理限制**：仅支持 ChatML 格式的 SFT-文本生成训练集；不支持 API 调用，仅限控制台操作 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务将产生独立费用，详见百炼计费文档。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


