# 模型调优

模型调优（Fine-tuning）是百炼平台基于开发者自有数据对基础模型进行定制化训练的能力，用于提升模型在特定行业或业务场景下的表现、降低输出延迟、抑制幻觉并对齐人类偏好。它处于「调优 → 压缩 → 部署」模型生产链路的起点，产出的自定义微调模型可作为模型压缩、模型部署和基线评测的输入。

## 调优方法

百炼提供三种递进式调优方法，推荐按 `CPT（可选）→ SFT → DPO（可选）` 的顺序使用：

| 方法 | 目标 | 数据要求 | 典型场景 |
| --- | --- | --- | --- |
| CPT（继续预训练） | 注入领域知识 | 1000 万+ Token 无标签文本 | 金融/医疗/法律等垂直领域适配 |
| SFT（监督微调） | 学会遵循指令 | 1000+ 条高质量问答对 | 客服、代码助手、Agent 工具调用 |
| DPO（直接偏好优化） | 对齐人类偏好 | 100+ 组正负样本对 | 安全合规强化、降低幻觉 |

每种方法又区分**全参训练**和**高效训练（LoRA）**两种模式：全参训练效果更好但耗时更长；高效训练收敛快、成本低，适合快速验证和时间敏感的场景。

## 支持的模态与模型

- **文本生成**：Qwen3.6/3.5/3/2.5 系列多个规格，覆盖全参训练与 LoRA 高效训练。
- **视觉理解（千问 VL）**：Qwen3-VL-8B/4B-Instruct、Qwen2.5-VL-72B/32B/7B-Instruct 等，支持 SFT 全参和高效训练。
- **图像生成**：wan2.7-image-pro、wan2.7-image（SFT-LoRA），支持文生图与图生图微调。
- **视频生成**：wan2.5-i2v-preview、wan2.2-i2v-flash、wan2.2-kf2v-flash（SFT-LoRA）。
- **语音合成**：cosyvoice-v3-flash（SFT 高效微调），用于高还原度专属音色定制。

具体支持模型清单以百炼控制台「模型调优」页面的实时列表为准。

## 使用方式

### 控制台操作

1. 在「数据管理」页面上传训练数据集并发布。
2. 在「模型调优」页面创建训练任务，选择模型、训练方式和超参数。
3. 观察 Training Loss / Validation Loss 曲线判断训练状态。
4. 训练完成后在「模型部署」页面一键部署，或进入「模型压缩」进行量化降本。

### API 操作

通过 DashScope API 完成全流程：

```bash
# 1. 上传训练文件
curl --request POST 'https://dashscope.aliyuncs.com/api/v1/files' \
  --header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
  --form 'files=@"/path/to/file.jsonl"' \
  --form 'purpose="fine-tune"'

# 2. 创建调优任务
curl --location "https://dashscope.aliyuncs.com/api/v1/fine-tunes" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --header 'Content-Type: application/json' \
  --data '{"model":"qwen3-8b","training_file_ids":["<file_id>"],"training_type":"sft"}'

# 3. 查询任务状态（轮询直到 SUCCEEDED）
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

## 训练数据格式

- **SFT 文本生成**：ChatML 格式的 JSONL，每行一个 `messages` 数组，支持 system/user/assistant 多轮对话；不支持 OpenAI 的 `name`、`weight` 参数；assistant 行可选 `loss_weight`（0.0~1.0，邀测参数）。
- **SFT 思考模型（Thinking）**：只能针对最后一条 assistant 输出训练，思考内容须用 `<think>...</think>` 标签包裹，标签前后的换行需保留。
- **SFT 视觉理解（千问 VL）**：在 ChatML 基础上 user content 使用数组格式，支持 `image`、`video`（路径或帧列表）、`resized_width/height`、`fps/sample_fps`、`video_start/end` 等字段；训练数据与图片/视频打包为 ZIP 上传。
- **DPO 数据集**：在 `messages` 之外增加 `chosen` 与 `rejected` 字段，对最后一条用户输入训练正负偏好；`chosen` 支持 `loss_weight`（邀测）。
- **CPT 训练集**：纯文本格式，每行 `{"text":"文本内容"}`。
- **图生视频训练集**：标注文件固定命名 `data.jsonl`（≤20MB），含 `prompt`、`first_frame_path`、`last_frame_path`（首尾帧）、`video_path`（仅训练集）；图像最大 4096×4096，支持 BMP/JPEG/PNG/WEBP，视频支持 MP4/MOV。

## 关键参数

| 参数 | 说明 |
| --- | --- |
| `model` | 选择的基础模型名称，须在支持调优的模型清单内 |
| `training_file_ids` | 已上传的训练文件 ID 列表 |
| `training_type` | 调优类型：`sft` / `dpo` / `cpt` |
| 训练方式 | 全参训练 或 高效训练（LoRA） |
| `loss_weight` | assistant/chosen 行可选，控制样本重要性（0.0~1.0，邀测） |
| `custom_calibration_file_ids` | 用于模型压缩阶段的校准数据（压缩任务用） |

## 下游衔接

- **模型压缩**：对全参微调产出的模型执行量化，进一步降低部署成本；已量化的模型不支持二次压缩或继续训练。
- **模型部署**：将微调或压缩后的模型发布为在线推理服务。
- **基线评测**：仅支持调优后的模型，用于验证通用能力（学科、数学、推理）。
- **数据管理**：训练集与评测集统一在「数据管理」中创建、清洗与增强，仅「内部上传」类型且「已发布」状态的数据集可用于校准。

## 限制和注意事项

- 调优任务为异步执行，需通过 API 或控制台轮询任务状态（待开始 / 排队中 / 运行中 / 成功 / 失败 / 已取消）。
- 训练数据须符合对应方法的最低规模要求；若评测结果不佳，最直接的改进方式是收集更多高质量数据。
- 视觉理解训练中如需传入 `system` 消息，content 必须使用数组格式 `[{\"text\":\"...\"}]`。
- 数据管理能力当前仅适用于华北2（北京）地域，且暂无可用的数据处理 API，需在控制台完成。
- 思考模型训练后若在样本中关闭了思考标签，部署后不建议再开启思考模式调用。

## 关联主题页

- [model production](../api/model-production.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)
- [model data overview](../guides/model-data-overview.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


