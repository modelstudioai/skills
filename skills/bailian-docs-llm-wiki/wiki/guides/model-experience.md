# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的身份认证、配额管理和计费规则。

## 支持的模型与功能

当前支持以下核心模型类别及对应能力：

- 文本生成（含对话、补全、摘要等）  
- 视觉理解（图像分类、OCR、多模态推理）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、帧编辑）  
- 世界模型（具身智能、环境建模与仿真）  
- 3D 模型生成（单图/多图生成可导出 GLB 文件）  
- 语音合成（TTS，支持多语种与音色定制）  
- 音频生成（环境音、SFX 等非音乐类音频）  
- 音乐生成（旋律、编曲、风格迁移）  
- 语音识别（ASR，支持中英文及方言）  
- 语音转语音（跨语言/音色转换）  
- 全模态（多输入模态联合理解与生成）  
- 向量与重排序（文本嵌入、语义检索、结果重排）  

各模型详情请参阅 [模型体验](../../raw/model-user-guide/model-experience.md) 的原始目录结构。其中，[图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md) 和 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 均依赖 GPU 实例资源，需在控制台提前申请配额。

## 关键参数

所有模型调用均支持以下通用参数（部分模型有扩展参数）：

- `model`: 必填，模型 ID（如 `qwen-vl-plus`、`wanx-video-1.0`），详见各子文档  
- `input`: 必填，输入数据结构（格式因模态而异，如 `{"prompt": "..."}` 或 `{"image_url": "...", "text": "..."}`）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`, `seed`）  
- `stream`: 布尔值，是否启用流式响应（仅部分文本/语音模型支持）  

> **注意**：`max_tokens` 在 [语音合成](../../raw/model-user-guide/model-experience/speech-synthesis.md) 中实际表示最大音频时长（毫秒），而非 token 数；该语义与文本模型不一致，调用时需特别注意。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization: Bearer <api_key>` 头  
2. **控制台体验**：登录百炼控制台 →「模型体验」页 → 选择模型 → 输入参数 → 点击「运行」  
3. **SDK 集成**：推荐使用 `dashscope` Python SDK（v1.20.0+），自动处理鉴权与参数序列化  

示例（Python）：
```python
from dashscope import MultiModalConversation
response = MultiModalConversation.call(
    model='qwen-vl-plus',
    messages=[{'role': 'user', 'content': [{'image': 'https://...'}, {'text': '描述这张图'}]}]
)
```

完整调用规范与错误码说明见 [模型体验](../../raw/model-user-guide/model-experience.md)。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型默认 32K tokens，视觉类模型受限于图像分辨率（最高支持 1536×1536 像素）  
- 视频与 3D 模型暂不支持[流式输出](../concepts/streaming.md)，且响应时间较长（通常 10–60 秒），需合理设置客户端超时（建议 ≥90s）  
- 所有生成类模型禁止用于生成违法、侵权、歧视性或高风险内容；平台将依据 [模型体验](../../raw/model-user-guide/model-experience.md) 中的《内容安全策略》进行实时拦截  
- 向量模型（如 `text-embedding-v1`）不支持 `stream=True`，且 `input` 字段必须为字符串数组（不可混用图像或音频）

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


