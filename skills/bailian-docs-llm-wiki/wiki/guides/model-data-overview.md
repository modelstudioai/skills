# model data overview

阿里云百炼的模型数据功能提供对大模型相关数据集的统一管理，涵盖训练集（用于模型调优）和评测集（用于模型评测）两大类。此外，平台还支持通过数据流对训练集进行数据清洗和数据增强，以提升训练数据质量。本文汇总了数据集的类型、格式要求及数据处理流程。

> **注意**：本文档所述功能仅适用于中国大陆版（北京地域）。

## 支持的数据集类型

根据 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)，模型数据分为以下两大类：

| 类型 | 用途 | 支持的子类型 |
|------|------|-------------|
| **训练集** | 对大模型进行调优，使其学会解决特定任务 | 文本生成（SFT / DPO / CPT）、多模态理解（千问VL）、图生视频（首帧）、图生视频（首尾帧） |
| **评测集** | 评估调优后模型在未见数据上的泛化能力 | 文本生成 |

## 训练集数据格式

### SFT 训练集（文本生成）

采用 ChatML 格式，支持多轮对话和 `system` / `user` / `assistant` 三种角色。

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入1"},
  {"role": "assistant", "content": "期望的模型输出1"},
  {"role": "user", "content": "用户输入2"},
  {"role": "assistant", "content": "期望的模型输出2"}
]}
```

- 不支持 OpenAI 的 `name`、`weight` 参数，所有 assistant 输出都会被训练。
- 支持 `loss_weight` 参数（`0.0 ~ 1.0`）设置各 assistant 行的训练权重（邀测功能）。
- xls/xlsx 格式仅支持单轮对话。

### SFT 思考模型（thinking）

仅针对**最后一个** assistant 输出进行训练，思考内容使用 `<think>` 标签包裹：

```json
{"role": "assistant", "content": "<think>\n思考内容\n</think>\n\n最终输出"}
```

- 思考标签前后的 `\n` 必须保留。
- 中间的 assistant 输出**不应**添加 `<think>` 标签。
- 若训练样本不包含 `<think>` 标签，训练完成后**不建议再开启思考模式调用**。

### SFT 视觉理解（千问VL）

`content` 使用数组格式，支持图片和视频输入：

```json
{"messages": [
  {"role": "user", "content": [
    {"text": "描述这张图片"},
    {"image": "image1.jpg", "resized_width": 200, "resized_height": 200}
  ]},
  {"role": "assistant", "content": [{"text": "模型输出"}]}
]}
```

**关键参数：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `image` | `str` | 图片文件路径 |
| `video` | `str` 或 `List[str]` | 视频文件路径或图片帧列表（仅 qwen3.5 及以后 VL 模型支持） |
| `resized_width` / `resized_height` | `int` | 目标缩放尺寸（像素） |
| `fps` | `float` | 视频输入帧率 |
| `video_start` / `video_end` | `float` | 视频截取起止时间（秒） |

**压缩包要求：** ZIP 格式，最大 2GB；`data.jsonl` 必须位于根目录；图片宽高均不超过 1024px、单张不超过 10MB；文件名仅支持 ASCII 字母、数字、下划线和连字符；图片文件名需全局唯一。

### DPO 训练集

在 `messages` 基础上增加 `chosen` 和 `rejected` 字段，用于训练正负反馈偏好：

```json
{"messages": [...],
 "chosen": {"role": "assistant", "content": "赞同的输出"},
 "rejected": {"role": "assistant", "content": "反对的输出"}}
```

### CPT 训练集

纯文本格式，每行一条：

```json
{"text": "文本内容"}
```

### 图生视频训练集

分为**基于首帧**和**基于首尾帧**两种模式，均要求 ZIP 压缩包内包含 `data.jsonl` 标注文件和对应的图像/视频文件。验证集为可选，无需提供视频文件。

## 评测集数据格式

文本生成评测集为 Excel 格式的单轮对话数据，包含 `Prompt` 和 `Completion` 两列。评测时模型基于 Prompt 推理，评分系统参考 Completion 进行评分。

## 数据集规模建议

| 训练方式 | 最低数据量要求 |
|---------|---------------|
| CPT | 一千万 Token 优质预训练数据 |
| SFT | 上千条优质微调数据 |
| DPO | 上百条人类偏好数据 |

## 数据处理（清洗与增强）

根据 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)，平台提供数据流功能对训练集进行处理，当前**仅支持 SFT 文本生成训练集**（ChatML 格式），不支持图片理解训练集和 DPO 训练集。

### 数据清洗

修正训练数据中的规范性、合规性、一致性及重复问题，支持的算子包括：

- 特殊内容移除（URL、特殊字符等）
- 敏感信息打码
- 文章相似度去重
- 敏感词过滤
- 毒性消除
- 等共十种清洗操作

### 数据增强

通过 Few-Shot 策略调用千问-Max 模型生成新数据，支持以下场景：

- **通用增强**：适用于通用 SFT 训练集
- **文本分类** / **文本抽取** / **文本创作**：针对特定场景优化

关键参数：`生成样本数`（单次最多 2000 条）、`指令生成依赖样本数`、`过滤相似度阈值`、`Prompt 配置`。

### 使用流程

1. **创建数据流**：在控制台拖拽清洗/增强节点，配置算子参数并发布。
2. **创建数据流任务**：选择已发布的数据流和待处理的训练集，系统自动执行。
3. **查看结果**：处理后的训练集自动生成新版本，不会覆盖原数据。

> **注意**：建议先清洗再增强，确保增强操作基于干净的数据集。处理完成后应检查训练集的完整性和真实性。

## 限制和注意事项

- 仅适用于中国大陆版（北京地域）。
- `loss_weight` 参数为邀测功能，需联系商务经理开通。
- 数据处理暂无可用 API，仅支持控制台操作。
- 数据流任务执行期间不支持手动终止。
- 如训练集数据不适合清洗增强（如法律文件、医学记录等），可跳过数据处理步骤。
- 如缺乏训练数据，可考虑使用智能体应用配合知识库索引增强模型能力，作为模型调优的替代方案。详见 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) 中的数据集构建技巧部分。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)






