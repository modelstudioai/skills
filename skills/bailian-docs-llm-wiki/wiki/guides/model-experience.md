# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准 API 或 SDK 快速集成文本、视觉、语音、音视频、3D 等能力。其核心目标是降低模型使用门槛，同时保持底层模型的灵活性与可扩展性。所有能力均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列模块组织。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类型及对应功能：

- **文本生成**：支持大语言模型（LLM）的 [prompt](prompt.md)-based 推理、流式响应、工具调用等  
- **视觉理解**：图像分类、OCR、图文理解、多图对比分析  
- **图片生成与编辑**：文生图、图生图、局部重绘、尺寸/风格调整  
- **视频生成与编辑**：文生短视频、关键帧控制、时序一致性优化  
- **3D模型生成**：单图生成可导出 GLB 的 3D 网格（依赖 TriPo 模型）  
- **语音合成（TTS）与语音识别（ASR）**：需跳转至阿里云 Model Studio 官方文档，[原文标题](../../raw/model-user-guide/model-experience.md) 中所列链接为外部帮助页，非百炼原生 API  
- **音乐生成、语音转语音、全模态、向量与重排序**：均已纳入统一调用框架，详见各子文档，例如 [原文标题](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：语音类能力（TTS/ASR/S2S）当前不通过 `model experience` 的 `/v1/models/{model}/invoke` 接口提供，而是直连 Model Studio 服务；若在 SDK 中尝试调用 `qwen-audio` 等模型名，将返回 `404 Not Found`，此行为与 [原文标题](../../raw/model-user-guide/model-experience.md) 中的导航结构存在隐含矛盾，请以实际 API 文档为准。

## 关键参数

所有 `model experience` 接口共用以下核心参数（部分模型支持扩展字段）：

- `model`: 必填，模型标识符（如 `qwen-vl-plus`, `wanx-video`, `tripo-3d`），须与 [原文标题](../../raw/model-user-guide/model-experience.md) 中列出的模型路径一致  
- `input`: 必填，结构化输入对象，格式依模型类型而异（如文本模型为 `{"prompt": "..."}`，视觉模型为 `{"image_url": "...", "prompt": "..."}`）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_output_tokens`），各模型支持范围见对应子文档  
- `stream`: 布尔值，启用流式响应（仅文本、语音合成、视频生成等部分模型支持）

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/models/{model}/invoke` 发送 POST 请求，携带认证头（`Authorization: Bearer <api_key>`）  
2. **SDK 调用**（Python 示例）：
   ```python
   from dashscope import MultiModalConversation
   response = MultiModalConversation.call(
       model='qwen-vl-plus',
       messages=[{'role': 'user', 'content': [{'image': 'http://...'}, {'text': '描述这张图'}]}]
   )
   ```
3. **批量与异步任务**：视频、3D、长音频等耗时操作需使用 `/async` 后缀接口，并轮询 `task_id` 获取结果  

## 限制和注意事项

- 单次请求最大输入长度：文本 ≤ 32768 tokens，图像 ≤ 4 张（每张 ≤ 20MB），视频 ≤ 10 秒（MP4/H.264）  
- 免费额度仅覆盖基础模型（如 `qwen-turbo`, `qwen-vl-plus`），高级模型（如 `wanx-video-pro`, `tripo-3d-pro`）需单独开通配额  
- 图片/视频/3D 类模型暂不支持自定义 LoRA 或微调权重加载  
- 所有模型输出内容受百炼内容安全策略约束，违规输入将触发 `400 Bad Request` 并返回 `safety_violation` 错误码

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


