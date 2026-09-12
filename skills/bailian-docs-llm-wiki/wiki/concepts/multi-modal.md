# 多模态

多模态（Multimodal）指模型能够同时理解、生成或联合处理两种及以上类型的数据模态（如文本、图像、音频、视频、3D结构等），并建模其跨模态语义关联。在百炼平台中，多模态能力不是单一模型的专属特性，而是贯穿于多个模型族与服务层级的系统性设计原则。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：Qwen-VL / Qwen2-VL 系列模型原生支持“图文联合理解+生成”，可接受图文混合输入（如带标注图的 [prompt](../guides/prompt.md)）并输出符合语义一致性的图像；`creative-tools-v1` 则通过显式传入 `input.image_url` + `input.prompt` 实现图生图、局部重绘等强多模态编辑任务。  
- **视频生成**：`kling`、`vidu`、`portrait-animation` 等模型均依赖文本+时序视觉信号的联合建模；人像驱动类模型更要求图像（人脸）与音频（语音）双输入对齐口型与表情，是典型的多模态对齐任务。  
- **3D生成**：Tripo-3D 支持 `text-to-3D` 和 `image-to-3D` 两种输入路径，同一模型统一处理语言描述与单视角图像，输出结构化三维网格（GLB），体现跨模态到几何空间的映射能力。  
- **音频处理**：`musicgen-v1` 接收纯文本 [prompt](../guides/prompt.md) 生成音乐，属文本→音频模态转换；`voice-translation` 则串联 ASR（音频→文本）与 TTS（文本→音频），构成端到端语音→语音多模态流水线。  
- **模型体验界面**：提供统一入口支持图文混输（如上传图片+提问）、音视频上传+指令等交互方式，底层自动路由至适配的多模态模型，并可视化各模态输入/输出，便于快速验证跨模态行为。  
- **应用广场**：通义 UI Agent（截图+自然语言指令→操作决策）、通义听悟Agent（会议录音+文本摘要→结构化纪要）等预置应用，均以多模态协同为默认工作模式，开发者无需自行拼接 pipeline。

> ⚠️ 注意：并非所有模型都支持任意模态组合。例如，WanX 图像模型仅支持文生图，不接受图像输入；ASR 模型仅接受音频输入，不理解 [prompt](../guides/prompt.md) 文本。务必查阅具体模型文档确认其支持的输入模态类型与格式约束。

## 关键参数和配置

多模态调用本身无全局统一参数，但以下参数在跨模态任务中高频出现且需特别注意：

| 参数 | 所在接口 | 说明 | 实际影响示例 |
|------|----------|------|--------------|
| `input`（object） | `/v1/images/generations`, `/v1/videos/generations`, `/v1/models/tripo-3d:generate`, `/api/v1/audio/transcribe` 等 | **核心多模态输入容器**。结构完全由模型决定：<br>• 文生图：`{"prompt": "..."}`<br>• 图生图：`{"prompt": "...", "image_url": "..."}`<br>• 人像驱动：`{"image_url": "...", "audio_url": "..."}`<br>• ASR：`{"audio_url": "..."}` 或 `{"audio_bytes": "base64..."}` | 错误嵌套（如将 `image_url` 放在 `input.prompt` 下）将导致 `400 Bad Request` |
| `response_format` | 多数 API | 控制返回内容形式：<br>• `"json"`（默认）：返回结构化结果（含 URL、文本等）<br>• `"b64_json"`：对图像/音频等二进制结果返回 base64 编码字符串（避免多次 HTTP 请求） | 调用 `creative-tools-v1` 时若需直接获取编辑后图像字节流，必须显式设置 `"response_format": "b64_json"` |
| `seed` | 图像/视频/3D/音乐生成类 API | 随机种子，用于复现多模态生成结果。**跨模态任务中 seed 对所有输入模态生效**（如固定 seed 后，同一图文输入始终生成相同图像） | 在 A/B 测试多模态 prompt 效果时，建议固定 `seed` 以排除随机性干扰 |
| `model` | 全局必填 | **决定多模态能力边界的关键标识符**。同一任务（如“生成图像”）下不同 model 支持的输入模态不同：<br>• `qwen-vl-plus`：支持图文输入<br>• `wanx-v1`：仅支持文本输入<br>• `creative-tools-v1`：强制要求图像+文本输入 | 误选 model 是多模态调用失败的最常见原因（如用 `wanx-v1` 传 `image_url` 将被拒绝） |

> ✅ 最佳实践：调用前始终查阅目标 `model` 的官方文档（如 [图像生成](../../raw/model-api-reference/image-generation.md)），确认其支持的 `input` 字段结构、必填项及模态组合规则。不要依赖通用参数模板。

## 面向开发者，简洁实用

- 多模态 ≠ 万能输入：每个模型只支持其训练所覆盖的模态组合，**严格按文档定义构造 `input` 对象**，不猜测、不试错。  
- URL 优先：所有媒体文件（图像/音频/视频）首选 `xxx_url` 字段传公网可访问链接（HTTPS），避免 base64 编码带来的体积膨胀与解析开销。  
- 安全合规：上传文件须符合平台白名单格式（PNG/JPEG/WAV/MP3/MP4），且不含可执行内容；多模态 prompt 中避免敏感词与违法信息。  
- 调试技巧：在「模型体验」界面中先用真实图文/音视频样本测试，观察输入解析是否正确（如图像是否显示、音频波形是否加载），再迁移至代码调用。  
- 错误定位：当多模态请求失败时，优先检查 `error.code`（如 `InvalidInput.ImageResolution`, `UnsupportedModel`, `InvalidInput.AudioFormat`），而非仅看 HTTP 状态码。

## 关联主题页

- [image generation](../api/image-generation.md)
- [audio api references](../api/audio-api-references.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [model experience](../guides/model-experience.md)
- [application gallery](../guides/application-gallery.md)


