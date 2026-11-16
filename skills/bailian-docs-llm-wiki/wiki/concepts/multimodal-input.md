# 多模态输入支持

多模态输入支持是指百炼平台允许模型接收并联合理解多种类型的数据输入（如文本、图像、音频、视频等），从而实现跨模态语义对齐与协同推理的能力。该能力是 Qwen 系列多模态大模型（如 `qwen3-vl-plus`、`qwen3.8-omni-flash`、`qwen-audio`）及专用多模态模型（如 `qwen-image-*`、`qwen-mt-uni`、`wan2.7-t2v`）的核心基础，贯穿于生成、理解、翻译、编辑等全链路 AI 服务。

## 在百炼平台的不同场景中，这个概念如何使用

多模态输入并非统一接口规范，而是根据**模型类型**和**API 协议**差异化实现，开发者需按实际调用路径选择适配方式：

- **语言大模型（Qwen LLM）调用**（如 `qwen4-max`、`qwen3-vl-plus`）：  
  - ✅ 支持文本 + 图像混合输入（如图文问答、图表理解）；  
  - ✅ 支持文本 + 视频输入（需抽帧，DashScope 协议支持 `max_frames` 控制）；  
  - ⚠️ 音频仅限 `qwen-audio` 模型，且**仅可通过 DashScope 原生协议调用**，OpenAI 兼容的 Chat/Responses API 不支持；  
  - ❌ OpenAI 兼容的 `chat.completions` 接口**不支持音频输入**，也**不支持视频输入**（仅图像）；  
  - ✅ Anthropic Messages 协议支持结构化多模态内容（`type: "image"` / `"text"`），适合精细控制输入顺序与角色。

- **图像生成类模型**（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`vidu/vidu-image-pro_reference2image`）：  
  - ✅ 所有主流模型均支持 `text` + 可选 `image`（1–14 张参考图）组合输入；  
  - ✅ 输入图像支持 URL 或 Base64 编码（部分模型如 FaceChain 要求前置人脸检测）；  
  - ✅ 可灵（Kling）支持多图输入用于分镜生成，Vidu 支持中英文文本精准渲染与 UI 图表像素级还原。

- **视频生成类模型**（如 `wan2.7-t2v`、`pixverse/pixverse-v6-t2v`、`kling/kling-v3-omni-video-generation`）：  
  - ✅ 文生视频：纯 `prompt` 文本；  
  - ✅ 图生视频：`first_frame`（首帧）或 `first_frame` + `last_frame`（首尾帧）；  
  - ✅ 参考生视频：`reference_images`（多图）或 `media`（图片/视频混合数组）；  
  - ✅ 数字人驱动：`image_url`（肖像）+ `audio_url`（语音）双输入；  
  - ⚠️ 所有视频 API **强制异步调用**，需通过 `task_id` 轮询结果。

- **多模态翻译模型**（如 `qwen-mt-uni`、`qwen-mt-image-2.0`）：  
  - ✅ `qwen-mt-uni`：支持 PDF/DOCX/PPTX/XLSX/HTML/Markdown + 图像（PNG/JPG）+ 音频（MP3/WAV）任意组合输入，输出保持原始格式；  
  - ✅ `qwen-mt-image-*`：专精图像内文字识别与翻译，支持主体分割（`imageSegment`）跳过 Logo/人脸区域；  
  - ⚠️ `qwen-mt-image` **仅支持异步调用**，`qwen-mt-uni` 同步/异步均可。

- **世界模型**（如 `happyoyster/directing`）：  
  - ✅ 当前以结构化文本输入为主（如 `world_state`、`current_shot`），暂未开放原始图像/视频输入；  
  - 🔜 未来版本规划支持视觉输入辅助镜头调度与情绪建模（详见邀测路线图）。

## 关键参数和配置

| 输入类型 | 协议/模型上下文         | 关键字段与格式示例                                                                 | 注意事项 |
|----------|--------------------------|------------------------------------------------------------------------------------|----------|
| **图像** | OpenAI Chat Completions  | `{"type": "image_url", "image_url": {"url": "https://...", "detail": "high"}}`     | `detail` 可选 `"low"`/`"high"`，影响分辨率与 token 消耗 |
|          | DashScope（Qwen VL）     | `{"image": "https://...", "detail": "high"}`                                        | 支持 Base64：`{"image": "data:image/png;base64,..."}` |
|          | Anthropic Messages       | `{"type": "image", "source": {"type": "url", "url": "https://..."}}`              | 必须与 `text` 类型消息同属一个 `content` 数组 |
| **视频** | DashScope（Qwen Omni）   | `{"video_url": "https://...", "max_frames": 32}`                                    | `max_frames` 仅 DashScope 支持，OpenAI 兼容 API 不可用 |
|          | Video Generation API     | `"input": {"img_url": "https://..."}`（首帧）或 `"first_frame"` + `"last_frame"` | 万相3.0 支持单接口五种模式，无需切换 endpoint |
| **音频** | DashScope（Qwen-Audio）  | `"input_audio": "https://..."` 或 `"audio": "data:audio/wav;base64,..."`          | **仅 DashScope 协议支持**；OpenAI Chat/Responses 均不支持 |
| **多格式文档** | Qwen-MT-Uni           | `"input": {"file_url": "https://...", "file_type": "pdf"}` 或直接传 Base64 文件体 | 支持 ZIP 打包多文件；敏感词过滤需显式传 `ext.sensitives` |
| **混合输入** | Qwen-MT-Uni           | `"input": {"text": "请翻译此段说明", "image": "https://..."}`                      | 图像中文字将被 OCR 并与文本共同参与翻译决策 |

> 💡 **通用提示**：  
> - 所有 URL 必须可公开访问（或配置白名单），私有存储需预签名；  
> - Base64 编码建议压缩后 ≤ 10 MB（具体上限见各模型文档）；  
> - 多模态输入会显著增加 token 计算量（尤其高分辨率图像/长视频），请合理设置 `max_tokens` 并监控计费；  
> - 异步模型（视频、图像编辑、`qwen-mt-image`）必须携带 `X-DashScope-Async: enable` 请求头。

## 面向开发者，简洁实用

- ✅ **先确认模型能力**：不是所有模型都支持全部模态。查清模型 ID（如 `qwen3-vl-plus` 支持图文，`qwen-audio` 仅支持音频，`qwen-mt-uni` 支持全模态）；  
- ✅ **再选协议路径**：[OpenAI 兼容接口](openai-compatible-interface.md)便捷但模态支持受限；DashScope 原生协议功能最全，推荐新项目首选；  
- ✅ **严格匹配地域与域名**：多模态模型（尤其第三方）常有地域限制（如三方模型仅华北2可用），务必使用 `{WorkspaceId}.{region}.maas.aliyuncs.com`；  
- ✅ **调试用小样本**：首次集成时，用 1 张低分辨率图 + 短文本验证流程，再逐步扩展模态与规模；  
- ✅ **错误优先看 `input` 结构**：90% 的 400 错误源于字段名错（如 `image_url` 写成 `image`）、嵌套层级错（如 `content` 数组缺失）、或模态不被当前协议支持。  

多模态输入是百炼平台“一个入口、全模态就绪”的关键体现。善用它，即可让模型真正“看见”、“听见”、“读懂”你的业务数据。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [world model api reference](../api/world-model-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


