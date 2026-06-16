# model data overview

阿里云百炼平台提供统一的数据管理功能，用于创建和管理模型训练与评测所需的数据集。数据集分为训练集（用于模型调优）和评测集（用于模型评测）两大类，同时平台还提供数据清洗和数据增强能力，帮助开发者获取更高质量的训练数据。

## 数据集类型

百炼数据管理支持两类数据集：

- **训练集**：用于模型调优，通过有监督训练使模型学会解决特定任务。目前支持文本生成、多模态理解、图生视频（首帧）、图生视频（首尾帧）四种训练集类型。
- **评测集**：用于评估调优后模型在未见过数据上的表现，目前支持文本生成评测集。

详细的数据集格式说明参见[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 文本生成与多模态理解训练集

### SFT 训练集

采用 ChatML 格式，支持多轮对话和多种角色（system/user/assistant）。数据为 JSONL 格式，每行一条 JSON 记录：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

关键限制：不支持 OpenAI 的 `name`、`weight` 参数，所有 assistant 输出都会被训练。支持 `loss_weight` 参数（0.0~1.0）设置训练时的相对重要性（邀测功能）。

### SFT 思考模型（Thinking）

与标准 SFT 类似，但只针对**最后一个** assistant 输出进行训练，需使用 `<think>` 标签包裹思考内容：

```json
{"role": "assistant", "content": "<think>\n思考内容\n</think>\n\n期望输出"}
```

> **注意**：思考标签前后的 `\n` 必须保留。

### SFT 视觉理解（千问 VL）

支持图片和视频输入，content 字段需使用数组格式。训练数据需打包为 ZIP 格式（最大 2GB），data.jsonl 必须位于压缩包根目录下。图片单张分辨率宽高均不超过 4096px，最大 10MB。视频文件路径模式仅 qwen3.5 及以后的 VL 模型支持。

### DPO 训练集

用于人类偏好对齐训练，数据结构在标准 messages 基础上增加 `chosen`（正例）和 `rejected`（负例）字段。一般需要上百条人类偏好数据。

### CPT 训练集

纯文本格式，结构为 `{"text": "文本内容"}`，最少需要一千万 Token 优质预训练数据。

## 图生视频训练集

### 基于首帧

训练集包括首帧图像、训练视频和标注文件（data.jsonl），ZIP 包内 data.jsonl 每行包含 `prompt`、`first_frame_path`、`video_path` 三个字段。验证集可选，仅需首帧图像和标注文件。

### 基于首尾帧

训练集在首帧基础上增加尾帧图像，标注文件增加 `last_frame_path` 字段。验证集同样可选。

## 文本生成评测集

采用 Excel 格式，每行包含 Prompt 和 Completion 两列。评测时模型基于 Prompt 推理，评分员参考 Completion 评分。

## 数据处理

百炼提供数据清洗和数据增强功能，帮助提升训练数据质量。详细操作流程参见[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

### 数据清洗

支持十种清洗算子，包括特殊内容移除、敏感信息打码、文章相似度去重、敏感词过滤、毒性消除等。目前仅支持 SFT 文本生成训练集。

### 数据增强

通过 Few-Shot 策略调用千问-Max 模型生成新数据，支持四种场景：

| 场景 | 说明 |
|------|------|
| 数据增强-通用 | 适用于通用 SFT 训练集增强，每次最多生成 2000 条 |
| 数据增强-文本分类 | 针对文本分类任务优化 |
| 数据增强-文本抽取 | 针对文本抽取任务优化 |
| 数据增强-文本创作 | 针对文本创作任务优化 |

### 数据流使用流程

1. **创建数据流**：在数据管理页面搭建自定义数据流画布，编排清洗和增强算子
2. **发布数据流**：发布后可用于创建任务
3. **创建数据流任务**：选择数据流和目标训练集，系统自动执行处理
4. **查看结果**：处理后自动生成训练集新版本，不覆盖原始数据

> **注意**：数据处理目前暂未提供 API，仅支持控制台操作。建议先清洗再增强，确保增强操作基于干净的数据集。

## 数据集构建建议

- SFT 训练集建议至少准备 1000+ 条优质微调数据
- CPT 预训练数据建议至少一千万 Token
- DPO 一般需要上百条人类偏好数据
- 准备训练集时同步准备不重叠的评测集，便于评估调优效果
- 可借助大模型辅助生成特定业务场景的训练数据来扩充训练集

更多关于训练集格式的详细规范，请参考[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)中的完整说明。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


