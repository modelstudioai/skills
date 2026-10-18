# 多模态

多模态（Multimodal）指模型能够同时接收、理解与生成多种类型数据（如文本、图像、音频、视频、3D结构等）的能力。在百炼平台中，多模态不是单一模型类别，而是一种能力范式——它贯穿于视觉理解、图文生成、音视频合成、世界建模等核心场景，体现为统一的输入结构、协同的参数体系与跨模态的语义对齐机制。

## 在百炼平台的不同场景中，这个概念如何使用

- **视觉理解与图文推理**：以 `qwen-vl-plus` 为代表，支持 `input.messages` 中混合 `text` 和 `image_url`（或 base64），模型在统一 token 空间内联合建模图文语义，用于描述、问答、OCR、逻辑推理等任务。  
- **图像/视频生成**：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`pixverse/pixverse-v6-t2v` 等模型接受文本提示词（`text`）+ 可选参考图（`image_url`）+ 视频帧（`video_url`）组合输入，实现文生图、图生图、参考生视频等多模态条件控制。  
- **全模态（Omni-modal）交互**：`qwen-omni` 等模型支持单次请求中混入文本、图像、音频 URL（或 base64）、甚至结构化 JSON，content 数组长度上限为 8，适用于复杂人机协作、具身智能指令解析等高阶场景。  
- **语音与音视频融合**：TTS 模型（如 `speech-tts-1.2`）可结合 `voice`、`text` 与 `style_reference_audio_url` 实现音色+情感双控；ASR + TTS + 视频生成链路（如对口型 `pixverse-lipsync`）构成端到端多模态输出闭环。  
- **世界模型与具身智能**：`HappyOyster` 系列通过 `scene_state` 字段结构化承载环境图像、角色状态、物理参数、历史动作轨迹等异构信息，驱动多模态状态演化与决策，是“感知-理解-行动”闭环的技术底座。

> ✅ 关键识别特征：所有多模态调用均使用 `input.messages` 或 `input` 对象中的 `content: [{type: "text", text: "..."}, {type: "image_url", image_url: "..."}]` 结构，而非单一字符串输入。

## 关键参数和配置

- **`input.messages[].content[]`（必填）**：多模态输入的核心载体，数组元素必须为对象，且 `type` 字段明确标识模态类型（合法值：`"text"`、`"image_url"`、`"audio_url"`、`"video_url"`、`"file_url"`）。同一 message 中可混搭最多 8 种模态元素（全模态模型限制）。  
- **`model`（必填）**：必须选择明确标注为多模态能力的模型（如 `qwen-vl-plus`、`qwen-image-3.0-pro`、`qwen-omni`、`wan2.7-videoedit`），普通 LLM（如 `qwen-max`）不支持非文本输入。  
- **`parameters.max_output_tokens`（推荐显式设置）**：多模态输出常含长描述、坐标、JSON Schema 等结构化内容，建议设为 ≥2048 避免截断。  
- **`stream`（谨慎启用）**：仅部分多模态模型支持流式（如 `qwen-vl-plus` 支持文本流，但 `qwen-image-*`、视频/3D 模型不支持）。全模态（Omni-modal）模型明确不支持 `stream=True`。  
- **文件大小与格式约束（硬性限制）**：  
  - 图像：≤ 20 MB / 张，支持 JPG/PNG/WebP；  
  - 视频：≤ 500 MB / 个，MP4/MOV/AVI（H.264 编码）；  
  - 音频：≤ 100 MB / 个，WAV/MP3/FLAC（8kHz/16kHz 单声道 PCM 优先）；  
  - 所有 URL 必须可公开访问（无鉴权跳转），且响应头含 `Content-Type`。

## 面向开发者，简洁实用

- ✅ **第一步：确认模型能力** —— 查阅 [模型广场](https://dashscope.console.aliyun.com/model) 或文档中模型名称是否含 `-vl-`（Vision-Language）、`-image-`、`-video-`、`-omni`、`-world` 等后缀，或明确标注“多模态”。  
- ✅ **第二步：构造标准 content 数组** —— 不要拼接字符串，严格使用 `[{ "type": "text", "text": "..." }, { "type": "image_url", "image_url": "https://..." }]` 格式。  
- ✅ **第三步：校验 URL 可达性** —— 用 `curl -I <url>` 确保返回 `200 OK` 且 `Content-Type` 正确，避免因 CDN 缓存或防盗链导致 `403`。  
- ⚠️ **避坑提醒**：  
  - 多模态模型不接受纯 `input.text` 字段，必须用 `messages` 结构；  
  - `qwen-vl-plus` 等视觉模型对图像分辨率敏感，低于 256×256 可能丢失细节，建议上传 ≥512×512 原图；  
  - 全模态模型（`qwen-omni`）暂不支持 `system prompt`，角色设定需写入首条 user message 的 text 中。  

多模态是百炼平台能力扩展的主干道。从图文理解到世界建模，其本质是让模型具备更接近人类的“跨感官认知”能力——开发者只需聚焦于真实业务中的多源信息表达，平台已封装底层对齐与融合逻辑。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [model experience](../guides/model-experience.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [world model api reference](../api/world-model-api-reference.md)


