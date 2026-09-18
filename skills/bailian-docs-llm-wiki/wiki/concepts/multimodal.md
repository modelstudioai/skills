# 多模态能力

多模态能力指百炼平台中模型对多种感知模态（如文本、图像、视频、音频、3D 网格等）进行联合理解、生成或跨模态转换的能力。它不是单一模型的特性，而是平台级能力抽象，体现为统一输入结构、协同参数体系与一致调用范式，支撑文生图、图生视频、语音对话、音视频理解、3D重建等跨模态任务。

## 在百炼平台的不同场景中，这个概念如何使用

多模态能力在百炼平台中贯穿于多个垂直能力域，具体表现为以下四类典型使用模式：

- **多模态输入 → 单模态输出**  
  如 `qwen3-vl-plus` 接收图文混合 [prompt](../guides/prompt.md)（`messages` 中含 `text` + `image`），输出纯文本回答；`tripo-3d` 接收单张图像 URL 或文本描述，输出 `.glb` 三维模型。此时多模态体现为**输入异构性**，需通过 `input` 字段结构化组织（如 `{"text": "...", "image_url": "..."}`）。

- **单模态输入 → 多模态输出**  
  如 `kling/kling-v3-omni-image-generation` 支持一次请求返回多张不同风格/构图的图像（`n=3`）；`musicgen-pro-v1` 输入文本提示词，输出带元信息的 WAV+MP3 双格式音频。此时多模态体现为**输出多样性**，由 `n`、`response_format` 或 `output_format` 等参数控制。

- **跨模态生成与编辑**  
  如 `vidu/vidu-image-pro_reference2image` 将参考图像中的文字内容像素级还原到新图；`emo-v1` 需先调用检测 API 获取人脸坐标（`face_bbox`），再结合音频驱动生成口型同步视频。此时多模态体现为**模态间强依赖**，要求前置步骤输出作为后续输入字段（如 `input.face_bbox`），不可省略。

- **全链路多模态闭环**  
  如 `voice-dialog-pro-v1` 整合 ASR（语音→文本）、LLM（文本推理）、TTS（文本→语音）三阶段，开发者只需传入原始音频，平台自动完成模态流转；`qwen3.8-omni-flash` 支持 `input_audio` + `input_video` 同时输入，实现音画协同理解。此时多模态体现为**服务内聚性**，由统一 endpoint 和协议（如 DashScope `multimodal-generation`）封装，无需手动拼接。

> ⚠️ 注意：并非所有模型都具备完整多模态能力。例如 `qwen3.8-max` 仅支持文本，`paraformer-v2` 仅支持语音识别；务必以模型文档中标注的 `multimodal` 标签或 `input` 字段支持类型为准。

## 关键参数和配置

多模态能力的启用与行为控制高度依赖以下通用参数（按优先级排序）：

| 参数 | 类型 | 必填 | 说明 | 典型取值示例 |
|------|------|------|------|--------------|
| `model` | string | 是 | 模型标识符，决定模态支持范围。**必须选择明确标注支持多模态的模型**（如 `qwen3-vl-plus`、`wan2.7-image-pro`、`tripo-3d`），而非纯文本模型（如 `qwen3.8-max`） | `"qwen3-vl-plus"`, `"tripo-3d"` |
| `input` | object | 是 | 统一输入容器，结构由模型能力决定：<br>• 文图模型：`{"text": "...", "image": "base64..."}` 或 `{"image_url": "https://..."}`<br>• 音视频模型：`{"audio_url": "...", "video_url": "..."}`<br>• 3D模型：`{"text": "...", "image_url": "..."}`（二者选一） | `{"text": "一只蓝猫坐在窗台", "image": "data:image/png;base64,..."}` |
| `X-DashScope-Async` | header | 是（视频/3D/部分图像编辑） | HTTP 请求头，**异步任务必需**。值必须为 `"enable"`，否则报错 `"current user api does not support synchronous calls"` | `"enable"` |
| `min_pixels` / `max_pixels` | number | 否（图像/视频模型推荐） | 控制图像/视频帧缩放边界（总像素数）。避免因分辨率超限导致失败，尤其在 `qwen-vl` 系列中影响显著 | `min_pixels=65536`, `max_pixels=2621440` |
| `max_frames` | number | 否（视频模型专用） | DashScope 协议下指定视频抽帧总数，替代 `fps` 的粗粒度控制。适用于长视频理解场景 | `max_frames=32` |
| `size` | string | 否（图像生成模型必需） | 输出图像分辨率，格式 `"W*H"`。不同模型约束不同：`wan2.7-image-pro` 支持 `3840*2160`，`qwen-image-3.0` 限 `2048*2048` 内 | `"1024*1024"` |

> ✅ 实用提示：  
> - 所有图像/视频 URL 必须公网可访问且支持 `HEAD` 请求；Base64 数据需符合 `data:<mime>;base64,<payload>` 格式；  
> - 多模态输入严禁混用不兼容字段（如向 `paraformer-v2` 传 `image_url`）；  
> - 异步任务（视频/3D/复杂编辑）必须轮询 `GET /v1/tasks/{task_id}`，不可直接解析响应体。

## 面向开发者，简洁实用

- **第一步：确认模型能力**  
  查阅模型文档标题栏或参数说明中是否含 `multimodal`、`VL`（Vision-Language）、`Omni`、`Audio-Visual` 等关键词。无此标识的模型（如 `qwen-turbo`）不支持多模态。

- **第二步：构造合规 input**  
  严格按文档要求组织 `input` 字段：  
  • 图文模型 → `input.messages[0].content = [{type:"text", text:"..."}, {type:"image_url", image_url:"..."}]`  
  • 视频模型 → `input.video_url = "https://..."`（勿用 `input.image_url`）  
  • 3D模型 → `input.text` 与 `input.image_url` **二选一**，不可共存。

- **第三步：设置关键 headers**  
  ```http
  Authorization: Bearer sk-xxx
  Content-Type: application/json
  X-DashScope-Async: enable   # 异步任务强制要求
  ```

- **第四步：处理响应差异**  
  • 同步调用（如 `qwen3-vl-plus`）：直接解析 `output.text`；  
  • 异步调用（如 `tripo-3d`）：从 `output.model_url` 下载 `.glb` 文件（24小时有效）；  
  • 流式响应（如 `cosyvoice-300m`）：按 SSE 解析 `data:` 行，非 JSON body。

- **避坑清单**  
  ❌ 跨地域调用（API Key、Endpoint、模型地域不一致）→ `403 Forbidden`  
  ❌ 向 `qwen3.8-max` 传图像 → `InvalidInput: unsupported modality`  
  ❌ `X-DashScope-Async` 缺失或值非 `"enable"` → `400 Bad Request`  
  ❌ 图像 URL 返回 404 或无 `Content-Length` → `InvalidUrl` 错误  

多模态不是魔法，而是结构化的输入-处理-输出契约。遵循文档定义的 `input` 结构、`model` 约束与 `header` 规则，即可稳定复用百炼平台的跨模态能力。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [audio api references](../api/audio-api-references.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)


