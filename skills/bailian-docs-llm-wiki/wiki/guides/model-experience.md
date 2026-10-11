# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与限流机制。

## 支持的模型与功能

当前支持以下核心模型类别及对应能力：

- 文本生成（含对话、补全、摘要等）  
- 视觉理解（图像分类、OCR、图文理解）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、关键帧编辑）  
- 世界模型（具身推理、环境建模与仿真交互）  
- 3D 模型生成（单图/多图生成可导出 GLB 的 3D 网格）  
- 语音合成（TTS，支持多语种与音色定制）  
- 音频生成（环境音、SFX、非音乐类音频）  
- 音乐生成（旋律、编曲、风格化生成）  
- 语音识别（ASR，支持中英文混合与方言）  
- 语音转语音（跨语言/音色转换）  
- 全模态（多输入模态联合理解与生成）  
- 向量与重排序（文本嵌入、多粒度向量表示、检索重排序）

各模型能力详情请参阅 [模型体验](../../raw/model-user-guide/model-experience.md) 中的子模块链接，例如 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 关键参数

调用模型时需关注以下通用参数（部分模型支持扩展参数）：

- `model`: 必填，模型 ID（如 `qwen-max`, `wanx-v1`, `speech-tts-1`），详见各子文档  
- `input`: 输入数据结构，格式依模态而异（如 `text`, `image_url`, `audio_url`, `video_url`）  
- `parameters`: 可选，控制生成质量、长度、温度等（如 `top_p`, `temperature`, `max_output_tokens`）  
- `stream`: 布尔值，是否启用流式响应（仅部分文本/语音模型支持）  

> **注意**：`parameters` 的具体字段和取值范围因模型而异；例如 [语音合成](../../raw/model-user-guide/model-experience/speech-synthesis.md) 使用 `voice`, `speed`, `pitch`，而 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 使用 `temperature`, `repetition_penalty` —— 二者不可混用，且部分参数在新版模型中已被弃用（如旧版 `top_k` 已被 `top_p` + `temperature` 组合替代）。

## 使用方式

1. **API 调用**：通过 HTTPS POST 请求 `https://dashscope.aliyuncs.com/api/v1/services/aigc/{service}/call`，携带 `Authorization: Bearer <api_key>` 与 JSON body  
2. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写输入与参数 → 点击「运行」  
3. **SDK 集成**：使用 `dashscope` Python SDK 或其他官方 SDK，调用对应模块方法（如 `Generation.call()`、`SpeechSynthesis.call()`）  

所有调用均需提前在控制台开通对应模型服务权限，并确保配额充足。详细请求示例见 [模型体验](../../raw/model-user-guide/model-experience.md) 及其子文档，如 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

## 限制和注意事项

- 单次请求最大输入长度/大小受限：文本 ≤ 32768 tokens，图像 ≤ 20MB（PNG/JPEG），视频 ≤ 512MB（MP4），音频 ≤ 100MB  
- 所有模型默认启用速率限制（QPS/TPM），具体阈值见控制台「配额管理」页面  
- 非商用场景下，部分模型（如 `qwen-vl-plus`, `wanx-video`）需申请白名单方可调用  
- 输出内容受内容安全策略过滤，敏感结果可能返回空或拦截提示（不计费）  
- [世界模型](../../raw/model-user-guide/model-experience/world-model.md) 和 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 当前仅支持同步调用，暂不支持流式响应  

> **注意**：[3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) 文档中提及的“支持 OBJ 导出”为历史描述，自 v2.3.0 起仅支持 GLB 格式导出，OBJ 导出接口已下线。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


