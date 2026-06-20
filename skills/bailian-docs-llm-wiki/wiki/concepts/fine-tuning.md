# 模型微调

模型微调（Fine-tuning）是在预训练大模型基础上，使用特定领域或业务场景的数据对模型进行二次训练，使其在目标任务上获得更优表现的技术。百炼平台提供完整的微调能力，覆盖文本生成、视觉理解、图像生成、视频生成和语音合成等多种模态。

## 三种训练方式

百炼支持三种训练方式，它们构成递进关系：CPT（可选）→ SFT → DPO（可选）。

**CPT（继续预训练）**：通过海量无标记文本补充行业知识，提升模型在特定领域（如金融、医疗、法律）的知识深度。最低需要一千万 Token 的优质预训练数据，数据格式为简单的 `{"text": "..."}` 逐行 JSONL。

**SFT（监督微调）**：通过标注好的输入-输出样本教模型"学做事"，是最常用的微调方式。适用于客服机器人、代码助手、工具调用等场景。支持全参数微调和高效微调（LoRA）两种模式，最低需要上千条优质微调数据。

**DPO（直接偏好优化）**：通过同时提供正样本（chosen）和负样本（rejected）引入偏好反馈，可降低幻觉并针对 bad case 做定向优化。适用于安全合规、回答质量提升等场景，最低需要上百条人类偏好数据。

## 支持的模型与模态

| 模态 | 代表模型 | 支持的训练方式 |
| --- | --- | --- |
| 文本生成 | Qwen3.6、Qwen3.5、Qwen3、Qwen2.5 系列 | SFT（全参/高效）、CPT、DPO（全参/高效） |
| 视觉理解 | Qwen3-VL、Qwen2.5-VL 系列 | SFT（全参/高效） |
| 图像生成 | wan2.7-image-pro、wan2.7-image | SFT-LoRA |
| 视频生成 | wan2.5-i2v-preview、wan2.2-i2v-flash、wan2.2-kf2v-flash | SFT-LoRA |
| 语音合成 | cosyvoice-v3-flash | SFT 高效微调 |

## 数据准备

不同模态和训练方式对数据格式的要求不同：

**文本生成 SFT**：使用 ChatML 格式的 `.jsonl` 文件，每行包含 `messages` 数组（system/user/assistant 角色）。支持多轮对话和思考模型（thinking）格式，可通过 `loss_weight` 参数控制样本重要性。

**视觉理解 SFT**：在 ChatML 格式基础上，`content` 字段使用数组格式混合文本、图片和视频。需将数据与媒体文件打包为 ZIP，`data.jsonl` 位于压缩包根目录。图片单张宽高不超过 1024px，ZIP 最大 2GB。

**图像/视频生成**：训练集包含目标图像或视频与 `data.jsonl` 标注文件，打包为 ZIP 上传。

**语音合成**：训练集包含 `.wav` 音频文件和 `data.jsonl`（含 `wav_fn` 和 `text` 字段），打包为 ZIP 上传。推荐训练音频总时长 1~10 小时，不少于 150 条。

**DPO 训练集**：在标准对话基础上增加 `chosen` 和 `rejected` 字段，分别提供偏好正例和反例。

当训练数据质量不足时，百炼提供数据清洗（去重、脱敏、特殊字符处理）和数据增强（通过 Few-Shot 策略调用千问-Max 生成新数据）功能进行预处理。

## 微调流程

无论哪种模态，微调的核心流程基本一致：

1. **准备数据集**：按目标模态和训练方式整理数据，确保格式正确
2. **上传数据集**：通过 API 将文件上传至百炼平台，获取 `file_id`
3. **创建微调任务**：指定基础模型、训练文件和超参数，启动训练，获取 `job_id`
4. **查询任务状态**：轮询任务接口直到 `status` 变为 `SUCCEEDED`
5. **部署与调用**：将训练产出的模型部署为在线推理服务

关键 API 端点：

- 上传文件：`POST https://dashscope.aliyuncs.com/api/v1/files`
- 创建微调任务：`POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`
- 查询任务状态：`GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>`

## 微调后的模型管理

微调产出的模型可以进行以下操作：

- **模型压缩**：通过量化将全精度模型转换为低精度版本，降低部署成本。压缩后不可逆，不支持继续训练或二次压缩。
- **模型部署**：支持预置吞吐（PTU）、模型单元和 Token 用量三种计费方式。PTU 适合高负载生产环境；模型单元适合大规模推理；Token 用量适合效果验证。
- **模型评测**：通过自定义评测（使用业务数据）或基线评测（使用标准数据集如 C-Eval、MMLU）验证微调效果。

## 使用方式

百炼提供两种操作路径：

- **API / 命令行**：通过 HTTP API 完成上传、训练、部署全流程，适合自动化集成和 CI/CD 流水线
- **控制台**：通过可视化界面操作，适合快速验证和手动管理

## 常见实践建议

- 先用小规模数据（50~100 条）验证流程和格式是否正确，再扩大数据规模
- SFT 是最基础的微调方式，建议优先尝试；CPT 和 DPO 根据实际需求选择性叠加
- 高效微调（LoRA）训练成本更低，适合快速迭代；全参数微调效果上限更高，但需要更多资源
- 微调后建议通过模型评测量化验证效果，避免仅凭主观感受判断
- 部署服务会持续产生费用，不再使用时应及时删除部署实例

## 关联主题页

- [fine tuning](../guides/fine-tuning.md)
- [model production](../api/model-production.md)
- [model data overview](../guides/model-data-overview.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model compression](../guides/model-compression.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


