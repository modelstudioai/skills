# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准 API 或控制台界面，按需调用文本、视觉、语音、音视频、3D 等各类模型服务。所有模型均遵循统一的身份认证、计费与配额体系，详见 [模型体验](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

当前支持以下核心模型类别（按模态组织）：

- **文本生成**：支持通用对话、长文本生成、代码补全等，对应 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉理解**：包括图像分类、OCR、多模态推理等，详见 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)  
- **图像生成与编辑**：支持文生图、图生图、局部重绘等，参考 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)  
- **视频生成与编辑**：含短视频生成、帧插值、视频描述等能力，见 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)  
- **世界模型**：提供具身智能与环境交互模拟能力，参见 [世界模型](../../raw/model-user-guide/model-experience/world-model.md)  
- **3D 模型生成**：支持文本/图像驱动的 3D 网格生成，文档位于 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)  
- **语音与音频**：涵盖语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音频生成及音乐生成；其中 TTS 和 ASR 的最新接口规范以阿里云官方帮助中心为准，[语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 与 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition) 文档已迁移至 help.aliyun.com，原始路径已失效  
- **全模态**：支持跨模态联合理解与生成，见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  
- **向量与重排序**：提供嵌入向量生成与检索重排序能力，参见 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)

> **注意**：原始文档中列出的 `语音合成` 和 `语音识别` 链接指向 help.aliyun.com，而其他条目均为相对路径 `raw/...`。经核查，这两个能力的最新 SDK 参数与错误码已在 help.aliyun.com 同步更新，`raw/` 下对应旧版文档已停止维护。请以 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 和 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition) 官方页面为准。

## 关键参数

所有模型调用共用以下基础参数（部分模型支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-max`, `wanx-v1`, `speech_16k_zh-cn`；完整列表见各子文档 |
| `input` | object | 是 | 输入内容，结构因模型类型而异（如 `text`, `image_url`, `audio_url`, `video_bytes`） |
| `parameters` | object | 否 | 模型特定超参，如 `temperature`, `top_p`, `seed`, `max_new_tokens` 等 |
| `enable_streaming` | boolean | 否 | 是否启用流式响应（仅部分文本/语音模型支持） |

具体参数定义请查阅对应模型文档，例如 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 中明确列出了 `temperature` 与 `stop` 字符串的生效范围。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization: Bearer <api_key>` 头；请求体为 JSON 格式，结构与 `input` + `parameters` 一致  
2. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写输入与参数 → 点击「运行」  
3. **SDK 调用**：推荐使用 `dashscope` Python SDK（v1.20.0+），初始化时指定 `model` 即可自动路由，示例见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档中的 Python 片段  

## 限制和注意事项

- 单次请求最大输入长度依模型而定：文本类模型默认上限 32768 tokens，视觉类模型单图分辨率建议 ≤ 1536×1536，视频类模型单视频时长 ≤ 10 秒  
- 所有模型均受项目级 QPS 与总调用量配额约束，超出将返回 `429 Too Many Requests`  
- 图片/视频/音频类模型不支持 Base64 内联编码，必须传公网可访问 URL 或使用 multipart/form-data 上传二进制（详见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)）  
- 世界模型与 3D 模型暂不支持流式响应，且需额外申请试用权限  
- 向量模型（embedding）输出维度固定为 1024，重排序模型仅接受最多 100 个候选文本对进行打分

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


