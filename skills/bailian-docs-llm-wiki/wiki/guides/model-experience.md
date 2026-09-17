# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准化接口调用文本、视觉、语音、音视频、3D 等各类模型服务，无需单独配置底层资源。所有模型均通过 `model_id` 标识，支持同步/异步调用及流式响应。

## 支持的模型与功能

当前支持以下核心模型类型（按模态分类）：

- **文本生成**：支持通用对话、长文本生成、代码补全等，详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉理解**：包括图像分类、OCR、多模态图文理解等，详见 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)  
- **图片生成与编辑**：支持文生图、图生图、局部重绘等，详见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)  
- **视频生成与编辑**：涵盖文生视频、视频扩时、关键帧控制等能力，详见 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)  
- **3D 模型生成**：基于文本生成可导出的 3D 网格（.glb/.obj），详见 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)  
- **语音与音乐**：含语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音乐生成；其中 TTS 和 ASR 的最新参数与错误码以 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 和 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition) 官方帮助文档为准  
- **全模态**：支持跨模态联合推理（如“描述视频中人物动作并生成对应配音”），详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  
- **向量与重排序**：提供嵌入（embedding）和语义重排序（rerank）服务，适用于 RAG 场景，详见 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)

> **注意**：原始文档中列出的 `fun-music.md`（音乐生成）路径已失效，实际文档位于 `raw/model-user-guide/model-experience/music-generation.md`；请以 [音乐生成](../../raw/model-user-guide/model-experience/music-generation.md) 为准。

## 关键参数

调用模型体验统一 API 时，必传参数包括：

- `model_id`：模型唯一标识（如 `qwen-max`, `wanx-v1`, `speech_16k_zh-cn`），需从控制台或 [模型体验](../../raw/model-user-guide/model-experience.md) 文档中确认可用值  
- `input`：结构化输入，格式依模型类型而异（如文本类为 `{"prompt": "..."}`，视觉类为 `{"image_url": "...", "prompt": "..."}`）  
- `parameters`（可选）：控制生成行为，常见字段包括 `temperature`（仅文本/音乐类）、`top_p`、`max_tokens`、`seed`、`stream`（布尔值）等  

部分模型支持 `enable_search` 或 `retrieval_config` 参数用于增强检索能力，具体参见对应子文档说明。

## 使用方式

1. **API 调用**：使用 `/v1/models/{model_id}/invoke`（同步）或 `/v1/models/{model_id}/async-invoke`（异步）端点，鉴权方式为 Bearer [Token](../concepts/token.md)（AccessKey）  
2. **SDK 调用**：推荐使用 `dashscope` Python SDK（≥1.18.0）或 `@alibabacloud/pop-core` Node.js SDK，初始化时指定 `model_id` 即可复用通用 `call()` 方法  
3. **控制台调试**：在百炼控制台「模型体验」页选择模型，填写 input 并提交，实时查看请求/响应体与耗时  

所有调用均遵循统一错误码体系（如 `InvalidParameter`, `Throttling`），详细含义见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 中的「错误响应」章节。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（视频/3D 类模型建议 ≤5 MB）  
- 异步任务最长保留 7 天，超时后结果不可查；同步调用超时默认为 60 秒（视频类建议设为 300 秒）  
- 免费额度仅限新用户首月，超出后按各模型计费项单独扣费（如 token 数、图片分辨率、音频时长）  
- 视觉与视频类模型暂不支持自定义 LoRA 微调权重注入；若需定制化能力，请参考 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 中的「私有模型部署」指引  
- 所有语音类模型（TTS/ASR/S2S）的采样率、编码格式、语言支持列表以阿里云 Model Studio 官方帮助文档为准，[语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 与 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition) 文档优先级高于本页引用的旧版内部路径

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


