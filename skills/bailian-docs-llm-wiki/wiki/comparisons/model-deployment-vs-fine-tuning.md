# 模型部署与微调方案对比

本文档旨在帮助开发者清晰区分**模型部署（Model Deployment）** 与**模型微调（Fine Tuning）** 两类核心能力的技术定位、适用边界与选型逻辑。二者虽同属百炼平台“模型即服务（MaaS）”体系，但目标不同：  
- **部署**聚焦于**已有模型的高效、稳定、可扩展的服务化交付**，解决“如何把模型用起来”的问题；  
- **微调**聚焦于**模型能力的定向优化与领域适配**，解决“如何让模型更懂你”的问题。  

正确区分二者，可避免资源错配（如用高成本微调解决本可通过 [Prompt 工程](../concepts/prompt.md)或路由策略解决的场景），提升研发效率与 ROI。

---

## 关键维度对比表

| 维度 | 模型部署（Deployment） | 模型微调（Fine Tuning） |
|------|------------------------|--------------------------|
| **核心目标** | 将已训练完成的模型（官方或用户导入）以 API 形式提供低延迟、高可用的服务 | 基于业务数据对预训练模型进行增量训练，提升其在特定任务/领域/风格上的效果、安全性或可控性 |
| **输入格式** | 标准化推理请求：<br>• `/v1/chat/completions`：`messages` 数组（含 `system`/`user`/`assistant`）<br>• `/v1/completions`：`prompt` 字符串<br>• 支持 `stream=true`（仅 `dedicated`/`dtu` 类型） | 训练数据文件（JSONL 或 ZIP 包）：<br>• SFT：`{"messages": [...]}`<br>• DPO：`{"chosen": [...], "rejected": [...]}`<br>• CPT：`{"text": "..."}`<br>• 视频/语音：ZIP 内含 `data.jsonl` + 媒体文件 |
| **输出格式** | 标准 OpenAI 兼容响应：<br>• 同步：`choices[0].message.content` 或 `choices[0].text`<br>• 流式：SSE 分块返回 `delta.content` | 训练完成后生成**新模型 ID**（如 `ft-qwen2-7b-chat-20240925-123456`），该模型可被**独立部署**，后续调用方式与原模型完全一致 |
| **支持模型** | • 所有百炼官方模型（Qwen 系列、万相、CosyVoice、决策模型等）<br>• 用户通过 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md) 功能上传的 Hugging Face 格式模型（需满足 PyTorch 2.0+、FlashAttention-2 兼容性） | • 文本：Qwen3/Qwen2.5/千问-Plus-Character（SFT/CPT/DPO/RL）<br>• 多模态：Qwen-VL（SFT）<br>• 图像/视频：万相、Qwen-Image（SFT-LoRA）<br>• 语音：CosyVoice（efficient_sft）<br>• 决策：`decision-model-preview-*`（高效微调）<br>⚠️ **不支持用户自定义模型微调**（仅限平台预置模型） |
| **API 端点** | 统一推理端点：<br>`https://dashscope.aliyuncs.com/api/v1/chat/completions`<br>（调用时 `model` 参数填部署生成的 `model_id`） | 训练管理端点：<br>• 数据上传：`POST /api/v1/files`<br>• 提交任务：`POST /api/v1/fine-tunes`<br>• 查询状态：`GET /api/v1/fine-tunes/{fine_tune_id}`<br>• **训练完成后的模型需另行部署才能调用** |
| **计费方式** | • `dedicated`/`dtu`：按实例/卡时长计费（小时级）<br>• `ptu`：按预购 PTU 单元数 + 实际使用时长计费<br>• `token`：按实际输入/输出 token 数计费（无预购）<br>• `routing`：按所路由子模型的实际调用计费 | • 按训练消耗的 GPU 小时 × 单价计费（实时扣费）<br>• 不支持预付费；无训练单元包（如 PTU/DTU）概念<br>• 控制台提供费用预估（基于数据量、模型、超参） |
| **典型场景** | • 客服对话机器人（高并发、低延迟）<br>• 内容审核 API（SLA 保障）<br>• A/B 测试多模型效果（配合路由）<br>• 快速验证模型能力（[Token](../concepts/token.md) 按量）<br>• 私有化部署合规需求（DTU 独占） | • 金融合同摘要（领域术语+格式强化）<br>• 医疗问答助手（专业知识注入+CPT）<br>• 品牌营销文案生成（风格迁移+SFT）<br>• 用户偏好排序（DPO 对齐价值观）<br>• IP 形象图像生成（万相 LoRA 微调）<br>• 单发音人语音合成（CosyVoice 音色定制） |
| **时效性** | • 创建部署：秒级（[Token](../concepts/token.md)）至分钟级（DTU）<br>• 服务就绪后即可调用 | • 训练耗时：数分钟（小数据 SFT）至数天（大模型 RL/CPT）<br>• 训练完成后需额外部署（分钟级）才可对外提供服务 |
| **资源隔离性** | • `dedicated`/`dtu`：物理/逻辑强隔离<br>• `ptu`/`token`：共享资源池，性能受调度影响 | • 训练过程独占分配 GPU 资源<br>• 训练完成后模型为独立资产，部署时可自由选择隔离级别 |

---

## 适用场景建议（面向开发者的技术选型参考）

### ✅ 优先选择 **模型部署** 当：
- 你已确认某款百炼官方模型（如 `qwen3-8b-chat`）在你的基准测试中表现达标，只需将其快速上线为服务；
- 业务流量存在明显峰谷（如电商大促），需弹性扩缩容，且能接受 `token` 按量部署的流控与功能限制（无流式、无长缓存）；
- 对延迟（P99 < 500ms）、稳定性（99.95% SLA）或数据不出域有硬性要求，需 `dedicated` 或 `dtu` 独占资源；
- 需要同时调度多个模型（如中文用 Qwen3，英文用 Llama3），通过 `model routing` 实现智能分发；
- 正处于 PoC 验证阶段，希望零配置、免训练地快速集成模型能力。

### ✅ 优先选择 **模型微调** 当：
- 官方模型在你的垂直领域（如法律文书、工业设备日志）上效果不足，且通过 [Prompt 工程](../concepts/prompt.md)、RAG 等方法无法显著改善；
- 需要深度定制模型行为：例如强制拒绝敏感话题（安全微调）、严格遵循模板输出（格式微调）、复刻特定写作风格（风格微调）；
- 业务涉及多模态内容（如商品图+描述生成营销文案），需 VL 模型理解图文关联；
- 需要构建专属 IP 形象（如虚拟主播形象/声音），必须通过 LoRA 微调实现轻量级风格固化；
- 有高质量偏好数据（`chosen`/`rejected` 对），希望用 DPO 直接对齐人类价值观而非依赖 RL 的复杂奖励建模。

### ⚠️ 注意规避的常见误区：
- **误用微调替代部署**：不要为临时性、低频次、无领域特性的需求启动微调（如“试试看 Qwen3 是否比 Qwen2 好”）——应直接部署对比；
- **忽略地域限制**：若需使用 DPO/CPT/视频/语音微调，**必须在华北2（北京）地域操作**，跨地域创建任务将失败；
- **混淆“部署”与“调用”**：微调产出的是新模型 ID，**不是 API 端点**；必须对该 ID 执行一次部署（如 `deployment_type=dedicated`），才能获得可调用的 `endpoint`；
- **低估数据质量门槛**：SFT 效果高度依赖 `messages` 数据的多样性与标注质量；低质数据微调可能劣化通用能力，建议先用小样本验证。

---

> **技术选型口诀**：  
> **“先部署，再微调；能 Prompt，不微调；要定制，看数据；求稳定，选部署；重效果，审微调。”**  
> 百炼平台倡导“部署先行、微调精用”的工程实践——90% 的业务场景可通过合理部署 + [Prompt 工程](../concepts/prompt.md) + RAG 解决；微调是应对剩余 10% 高价值、高壁垒场景的利器，而非默认选项。

## 被对比主题页

- [model deployment index](../guides/model-deployment-index.md)
- [fine tuning](../guides/fine-tuning.md)


