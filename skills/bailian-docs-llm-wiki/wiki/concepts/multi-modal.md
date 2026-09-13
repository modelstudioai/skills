# 多模态

多模态（Multimodal）指模型能够同时理解、生成或协同处理两种及以上类型的数据模态（如文本、图像、音频、视频、3D 网格等），并建立跨模态语义关联的能力。在百炼平台中，多模态不是单一模型类别，而是贯穿于多个 AIGC 能力的核心设计范式，体现为输入支持混合模态、输出可跨模态对齐、以及底层模型具备统一的多模态表征空间。

## 在百炼平台的不同场景中，这个概念如何使用

- **图像生成**：部分模型（如 Qwen-VL 系列）支持图文混合输入（text + image），实现条件化生成（例如“将这张草图渲染为写实风格”）；万相、Z-Image 等虽以文生图为主，但其编辑能力（局部重绘、风格迁移）隐式依赖图像特征与文本指令的对齐，属于多模态协同工作流。
  
- **视频生成**：Vidu、Kling、HappyHorse 等模型原生支持「文+图」双输入（如 `input: {text: "...", image_url: "..."}`），用于构图引导或动作锚定；人像驱动类模型则严格要求「图像 + 音频/文本」联合输入，实现口型-语音-表情的跨模态同步。

- **3D 生成**：Tripo-3D 明确提供 `text-to-3D` 和 `image-to-3D` 两种路径，同一模型共享底层多模态编码器，能将语言描述或单张 RGB 图映射至统一的 3D 潜在空间，是典型的多模态生成范例。

- **音频生成**：音乐生成（`musicgen-2b`）接受文本 [prompt](../guides/prompt.md) + 风格标签（如 `"jazz, upbeat, piano solo"`），将语义意图转化为时序音频信号；语音对话（Voice Chat）则串联 ASR（语音→文本）、LLM（文本理解与推理）、TTS（文本→语音）三阶段，构成端到端多模态闭环。

- **模型体验界面**：统一支持上传图片/音频/视频文件并配合文本 [prompt](../guides/prompt.md) 进行交互，自动识别输入模态组合，并路由至适配的全模态模型（如 `qwen2-vl`, `omni-modal`），开发者可零代码验证跨模态能力边界。

> ✅ 关键判断标准：若一个 API 的 `input` 字段允许同时包含 `text` 和 `image_url`（或 `audio_url`、`video_url`），且文档明确标注“支持多模态输入”或“图文混合理解”，即属多模态能力；仅支持单一模态输入（如纯 text 或纯 image）的模型，即使输出为多模态（如文生图），也不属于本概念定义下的多模态模型。

## 关键参数和配置

多模态任务本身无全局独有参数，但以下参数在跨模态场景中尤为关键，需按模型文档严格校验：

| 参数名 | 说明 | 注意事项 |
|--------|------|----------|
| `input` | **核心多模态字段**：结构为 JSON 对象，必须显式声明模态类型及内容。常见形式：<br>• `{ "text": "..." }`<br>• `{ "text": "...", "image_url": "https://..." }`<br>• `{ "image_url": "...", "audio_url": "..." }` | • 所有 URL 必须为公网可访问 HTTPS 链接<br>• 图像建议 ≥512×512，宽高比接近 1:1（3D/视频场景）<br>• 音频需为 PCM/WAV/MP3，采样率匹配模型要求（如语音对话强制 16kHz） |
| `model` | 必须选择明确支持多模态的模型标识符，例如：<br>• `qwen2-vl`（视觉语言理解）<br>• `vidu-1.0`（文图视频统一建模）<br>• `tripo-3d`（文图→3D）<br>• `kling-v1`（文图→视频） | ❌ 不支持将单模态模型（如 `qwen-turbo`）用于多模态输入，会返回 `400 InvalidInput` |
| `seed` | 启用结果可复现性。多模态生成中，相同 `seed` + 相同 `input`（含图像/音频二进制哈希一致）可保证输出一致性。 | 部分轻量模型（如某些 TTS）可能不支持 `seed`，调用前请查阅对应模型文档 |
| `parameters.guidance_scale` | 控制文本 [prompt](../guides/prompt.md) 对生成过程的约束强度（常见于扩散类多模态模型）。值越高，输出越贴近 prompt，但可能牺牲多样性。典型范围：3.0–15.0。 | 仅对支持 Classifier-Free Guidance 的模型生效（如 WanX、Kling），Qwen-VL 类理解模型不适用此参数 |

## 面向开发者，简洁实用

- **第一步：确认模型能力** —— 查阅 [模型体验](../../raw/model-user-guide/model-experience.md) 或各领域 API 文档，认准 “支持多模态输入”、“图文混合理解”、“文图视频统一建模” 等明确表述，勿凭模型名称推测。
- **第二步：构造 input 对象** —— 严格按文档要求组织 JSON 结构，避免混用字段（如向 `tripo-3d` 传 `audio_url`）；图像/音频 URL 请提前测试可访问性。
- **第三步：调试与容错** —— 多模态请求失败常见原因：① `input` 字段格式错误（JSON 解析失败）；② URL 不可达或超时；③ 模态组合不被模型支持（如对 `paraformer-v1` 传 `image_url`）。优先检查响应中的 `error.code`（如 `invalid_input`、`unsupported_modality`）。
- **第四步：生产集成建议** —— 对延迟敏感场景（如实时数字人），优先选用专有多模态模型（如人像驱动）而非拼接 ASR+LLM+TTS；对版权敏感内容，注意多模态输入中图像/音频也需符合《AIGC内容安全规范》。

多模态是百炼平台实现“一个接口、多种输入、一致体验”的技术基座。善用它，即可用统一范式打通文本、视觉、听觉与空间智能的生成链路。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [audio api references](../api/audio-api-references.md)
- [model experience](../guides/model-experience.md)


