# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速体验与集成。用户可通过标准 API 或控制台界面直接调用各类预置模型，无需自行部署或管理底层基础设施。该能力覆盖文本、视觉、语音、音视频、3D 及全模态等主流 AI 任务类型，详见 [模型体验](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

当前支持以下模型类别（按功能域组织）：

- **文本生成**：包括通用大语言模型（如 Qwen 系列）、代码生成、结构化输出等  
- **视觉理解**：图文理解、OCR、目标检测、图像分类等  
- **图片生成与编辑**：文生图、图生图、局部重绘、风格迁移  
- **视频生成与编辑**：文生视频、视频扩帧、时序编辑  
- **世界模型**：具身智能、环境建模与推理（实验性功能）  
- **3D 模型生成**：基于文本/图像生成可导出的 3D 网格（参见 [TriPo 3D 生成指南](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)）  
- **语音与音频**：语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音频生成、音乐生成（部分能力跳转至阿里云 Model Studio 文档）  
- **向量与重排序**：文本嵌入（embedding）、语义重排序（rerank）  
- **全模态**：跨模态联合理解与生成（如图文音视频混合输入输出），详见 [全模态模型](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：原始文档中语音合成、语音识别、语音转语音三类能力均指向外部 help.aliyun.com 链接，而其他能力均指向 `raw/` 下的本地文档。实际 SDK 和 API 接口已统一纳管至百炼平台，建议优先使用 `dashscope` Python SDK 或 `/v1/models/{model-id}/call` 标准 API 调用，避免依赖外部文档路径。该不一致已在 [模型体验](../../raw/model-user-guide/model-experience.md) 中体现，需以平台控制台「模型广场」实时列表为准。

## 关键参数

所有模型调用共用以下核心参数（部分模型支持扩展参数）：

- `model`: 模型 ID（如 `qwen-max`, `wanx-v1`, `qwen-audio-tts`），必须  
- `input`: 输入数据结构，格式依模型类型而异（如 `{"text": "..."}` 或 `{"image_url": "..."}`）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_output_tokens`）  
- `enable_search`: 仅文本模型支持，启用联网搜索（需开通对应权限）  

具体参数说明请参考各子模型文档，例如 [文本生成模型](../../raw/model-user-guide/model-experience/text-generation-model.md) 中对 `stop` 和 `repetition_penalty` 的定义。

## 使用方式

1. **控制台体验**：登录百炼控制台 → 进入「模型广场」→ 搜索并选择模型 → 在「体验页」填写输入并提交  
2. **API 调用**：使用 DashScope SDK（推荐 v4.0+）或直接调用 REST API  
   ```python
   from dashscope import Generation
   response = Generation.call(model='qwen-max', input={'text': '你好'}, api_key='YOUR_KEY')
   ```
3. **批量/异步调用**：对视频、3D、长音频等耗时任务，需使用 `/v1/jobs` 异步接口，并轮询 `job_id` 获取结果  

完整调用示例和错误码说明见 [文本生成模型](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本模型默认 32768 tokens，视觉模型图像分辨率上限为 1536×1536 像素（超限将自动缩放）  
- 视频与 3D 生成任务暂不支持流式响应，必须等待完整结果返回  
- 免费额度仅适用于部分模型（如 `qwen-turbo`），`qwen-max`、`wanx-v1` 等高性能模型需按 token 计费  
- 所有模型调用受百炼平台 [服务等级协议（SLA）](https://help.aliyun.com/product/42041.html) 约束，超时阈值为 120 秒（同步）或 24 小时（异步）  
- 用户上传的图像、音频、视频文件在处理完成后 24 小时内自动清理，不长期存储  

如遇模型不可用或返回 `ModelNotSupported` 错误，请确认模型 ID 是否在 [模型体验](../../raw/model-user-guide/model-experience.md) 列表中且处于「上线」状态。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


