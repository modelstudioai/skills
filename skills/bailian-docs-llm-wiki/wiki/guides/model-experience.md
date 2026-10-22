# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可一站式试用、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与限流机制。

## 支持的模型与功能

当前支持以下 12 类模型能力，覆盖文本、视觉、语音、音视频、3D、世界建模及检索增强等场景：

- 文本生成：支持长上下文推理、结构化输出、[函数调用](../concepts/function-calling.md)等 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- 视觉理解：包括图文问答、OCR、图表解析等多任务能力 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)  
- 图片生成与编辑：支持文生图、图生图、局部重绘、尺寸扩展等 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)  
- 视频生成与编辑：含文生视频、视频扩时、关键帧控制等功能 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)  
- 世界模型：提供具身交互、环境模拟与动作规划接口 [世界模型](../../raw/model-user-guide/model-experience/world-model.md)  
- 3D模型生成：支持 TriPo 等架构的单图生成 3D 网格与纹理 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)  
- 语音合成（TTS）、音频生成、语音识别（ASR）、语音转语音（S2S）：均基于统一音频处理栈 [语音合成](../../raw/model-user-guide/model-experience/speech-synthesis.md)  
- 全模态：支持跨模态联合输入（如“描述+草图+语音指令”）的端到端理解与响应 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  
- 向量与重排序：提供嵌入向量生成（embedding）与语义相关性重排序（rerank）两类基础检索模型 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  

> **注意**：`world-model.md` 中声明的“支持实时物理引擎反馈”尚未在 v3.2.0 API 中开放，实际调用将返回 `400 UnsupportedFeature`；请参考 [世界模型](../../raw/model-user-guide/model-experience/world-model.md) 的「已知限制」章节确认当前可用能力。

## 关键参数

所有模型调用共用以下核心参数（部分模型支持扩展参数）：

- `model`: 必填，模型标识符（如 `qwen-vl-plus`、`wanx-video-1.0`），详见各子文档的「模型列表」表格  
- `input`: 必填，结构化输入对象，格式依模型类型而异（如 `text_generation` 为 `{ "prompt": "...", "parameters": {...} }`；`vision` 为 `{ "messages": [...], "images": ["base64..."] }`）  
- `parameters`: 可选，通用超参（`temperature`, `top_p`, `max_tokens` 等），但**并非所有模型均支持全部参数**——例如 `embedding` 模型忽略 `temperature`，`rerank` 模型不接受 `max_tokens`  
- `stream`: 布尔值，仅对文本生成、语音合成等流式响应模型生效；其他类型（如图像/3D生成）强制 `false`

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke`，Header 需携带 `Authorization: Bearer <api_key>`  
2. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写输入 → 点击「运行」  
3. **SDK 调用**（Python 示例）：
   ```python
   from alibabacloud_bailian20231219.client import Client
   client = Client("<access_key_id>", "<access_key_secret>", "cn-beijing")
   response = client.invoke_model(
       model="qwen-max",
       input={"prompt": "你好"},
       parameters={"temperature": 0.7}
   )
   ```

## 限制和注意事项

- 单次请求最大输入长度：文本类模型上限 32768 tokens；视觉/视频类模型受 base64 图像/视频体积限制（≤ 50MB）；3D 模型仅支持单张输入图（≤ 4MB）  
- 输出长度限制：文本生成默认 `max_tokens=2048`，不可超过模型原生上下文窗口的 50%；图像生成固定输出分辨率（如 `image-generation-v1` 仅支持 `1024x1024`）  
- 计费粒度：按实际调用次数与资源消耗计费（如 token 数、图像分辨率、视频秒数），详情见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 的「计费说明」章节  
- **重要兼容性提示**：`speech-to-speech.md` 中描述的 `voice_clone` 参数已在 v3.1.0 版本中移除，新流程需先调用 `/v1/voices/create` 创建声纹 ID，再于 `input` 中传入 `voice_id`；旧参数将被静默忽略 —— 请务必更新至最新 SDK 或参照 [语音转语音](../../raw/model-user-guide/model-experience/speech-to-speech.md) 的「迁移指南」

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


