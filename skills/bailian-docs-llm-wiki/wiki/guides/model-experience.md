# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准化接口调用文本、视觉、语音、视频、3D、世界模型等各类模型，无需单独配置底层服务。所有模型均遵循统一的鉴权、计费与监控机制，详见 [模型体验](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

当前支持以下核心模型类型及对应能力：

- **文本生成**：支持通用对话、指令遵循、代码生成等，模型如 qwen-max、qwen-plus  
- **视觉理解**：图像分类、OCR、图文理解，支持多图输入与结构化输出  
- **图片生成与编辑**：文生图（SDXL、Qwen-VL+）、局部重绘、尺寸扩展等  
- **视频生成与编辑**：支持 2s~10s 短视频生成、关键帧控制、跨帧一致性优化  
- **世界模型**：具备环境建模与推理能力，适用于仿真交互场景  
- **3D模型生成**：通过 TriPo 3D 模型实现单图/多图生成带纹理的 GLB 文件  
- **语音与音乐**：语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音乐生成（FunMusic）  
- **向量与重排序**：支持文本嵌入（embedding）与跨文档相关性重排序（rerank）  

> **注意**：语音合成与语音识别的官方文档已迁移至阿里云帮助中心，[模型体验](../../raw/model-user-guide/model-experience.md) 中保留的链接为历史引用，实际配置请以 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis) 和 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition) 最新文档为准。

## 关键参数

调用模型体验 API 时，需在请求体中指定以下必选或常用参数：

- `model`: 模型标识符（如 `qwen-vl-plus`、`wanx-video-1.0`），必须与所选能力匹配  
- `input`: 输入数据结构，格式依模型类型而异（如 `text` 字段用于文本生成，`images` 数组用于视觉理解）  
- `parameters`: 可选参数对象，常见字段包括：  
  - `temperature`: 控制输出随机性（0.0–2.0，默认 1.0）  
  - `top_p`: 核采样阈值（0.0–1.0）  
  - `max_tokens`: 输出最大 token 数（部分模型强制限制）  
  - `seed`: 固定随机种子（确保结果可复现）  
- `stream`: 布尔值，启用流式响应（仅部分模型支持，详见各子文档）

具体参数约束与默认值请参考对应模型的专项指南，例如 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization` 头（Bearer + API Key）  
2. **SDK 调用**：推荐使用 `dashscope` Python SDK（≥1.18.0）或 `@alibabacloud/pop-core` Node.js SDK  
   ```python
   from dashscope import MultiModalConversation
   response = MultiModalConversation.call(model='qwen-vl-plus', input={'messages': [...]})
   ```
3. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写输入 → 实时查看响应与 Token 统计  

所有调用均计入项目级配额，支持按模型、按 Token 粒度查看用量明细，详情见 [模型体验](../../raw/model-user-guide/model-experience.md)。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型上限为 32768 tokens，视觉类模型单图分辨率不超过 4096×4096，视频类模型单次最长生成 10 秒  
- 图片/视频/3D 类模型暂不支持批量并发调用（即 `batch_size > 1`），需串行处理  
- 世界模型与 TriPo 3D 模型处于 Beta 阶段，接口稳定性与输出质量可能随版本迭代调整，建议关注 [世界模型](../../raw/model-user-guide/model-experience/world-model.md) 和 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) 的更新日志  
- 全模态（Omni-Modal）模型暂不开放自定义 [prompt](prompt.md) 工程，仅支持预设任务模板（如“图文问答”“多图对比分析”）  
- 向量与重排序模型要求输入文本长度 ≤ 512 字符，超长文本需截断或分块处理

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


