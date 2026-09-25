# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准化 API 或 Web 控制台直接调用各类预置模型，无需自行部署或管理底层推理服务。所有模型均经过平台统一封装，提供一致的请求格式、鉴权机制与可观测性支持。

## 支持的模型与功能

当前支持以下模型类型及对应能力：
- 文本生成（如 Qwen 系列大语言模型）  
- 视觉理解（图文理解、OCR、目标检测等）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（短视频生成、帧插值、视频描述）  
- 世界模型（具身智能仿真环境交互）  
- 3D 模型生成（TriPo 等结构化 3D 输出）  
- 语音合成（TTS）、音频生成、音乐生成  
- 语音识别（ASR）、语音转语音（TTS2TTS）  
- 全模态模型（跨文本/图像/音频/视频联合理解与生成）  
- 向量嵌入与重排序（embedding/rerank 模型）  

详细能力说明请参阅 [模型体验](../../raw/model-user-guide/model-experience.md) 的原始目录结构。各子模型的具体输入输出规范、示例和最佳实践，见其对应文档，例如 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

## 关键参数

调用任一模型时，需在请求体中指定以下通用参数：
- `model`: 模型标识符（如 `qwen-max`, `wanx-v1`, `speech-tts-16k-zh-cn`），必须与 [模型体验](../../raw/model-user-guide/model-experience.md) 中列出的名称严格一致  
- `input`: 模型输入数据，结构因模态而异（如文本为 `{"prompt": "..."}`，图像为 base64 编码或 OSS URL）  
- `parameters`: 可选配置项，常见字段包括 `temperature`（仅文本/生成类）、`top_p`、`max_tokens`、`seed`、`style`（图像/视频）、`voice`（语音）等  
- `enable_streaming`: 布尔值，控制是否启用流式响应（部分模型支持，详见各子文档）

> **注意**：部分旧文档（如 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis)）仍引用非百炼标准参数名（如 `text` 而非 `input.text`），实际调用请以 [模型体验](../../raw/model-user-guide/model-experience.md) 中的统一 schema 为准。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization: Bearer <api_key>` 头；  
2. **Web 控制台**：进入「模型体验」页，选择目标模型 → 填写输入 → 点击运行，支持实时调试与历史记录回溯；  
3. **SDK 调用**：推荐使用 `dashscope` Python SDK（v1.20.0+）或 `@alibabacloud/pop-core` Node.js SDK，自动处理签名与重试逻辑。

所有模型均支持同步响应（默认）与流式响应（需显式开启），具体兼容性请查阅对应子文档，例如 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 明确标注了 streaming 支持状态。

## 限制和注意事项

- 单次请求最大 payload 限制为 10 MB（含 base64 图像/音频等二进制内容）；  
- 视频与 3D 模型生成类任务有更长的超时阈值（默认 300 秒），需客户端合理设置 timeout；  
- 部分模型（如世界模型、全模态）处于灰度阶段，需申请白名单权限；  
- 向量与重排序模型不支持流式响应，且 `input` 必须为文本数组（非单文本字符串）；  
- 所有模型均遵循百炼平台统一配额体系，超出后返回 `429 Too Many Requests`；  

> **注意**：[3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) 文档中提及的本地 SDK 集成方式已废弃，当前仅支持通过 `/v1/models/tripo-3d/invoke` 标准 API 调用，请勿参考过时的 CLI 工具说明。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


