# 多模态

多模态（Multimodal）指模型能够同时理解、生成或联合理解多种类型数据（如文本、图像、音频、视频、3D结构等）的能力。在百炼平台中，多模态不是单一模型类别，而是一种能力范式，体现为跨模态输入/输出支持、统一推理接口和端到端联合建模能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型选型层面**：  
  - `qwen3.8-omni-flash`、`qwen-vl-plus`、`qwen3.5-omni-plus-realtime` 等模型明确标注为“全模态”（Omni-modal），可原生接受图文混合、音视频+文本等组合输入，并生成跨模态响应（如看图说话、听音频写摘要、视频帧描述生成）。  
  - 非全模态模型（如纯文本 `qwen3.8-plus` 或纯图像 `wan2.7-image-pro`）虽不支持混合输入，但通过平台统一的 `model experience` 层，开发者可组合调用多个单模态服务（如先 ASR → LLM → TTS），实现逻辑上的多模态流水线。

- **API 调用层面**：  
  - 同步调用：使用 `multimodal-generation` 服务类型（如 `POST /api/v1/services/aigc/multimodal-generation/generation`），`input` 字段需按模型要求传入结构化多模态数据（例如含 `text` 和 `image_url` 的数组）。  
  - 异步调用：对文生视频、图生视频等长耗时任务，需先上传文件获取临时 OSS URL，再在请求中绑定该 URL 与文本 [prompt](../guides/prompt.md)，体现“文本+图像/视频”的输入耦合。  
  - 实时交互：`qwen3.5-omni-plus-realtime` 等模型通过 WebRTC 或 AOQ 协议支持流式音视频输入，实时融合语音、画面与上下文文本进行推理。

- **开发集成层面**：  
  - SDK 封装了 `MultiModalGeneration.call()` 方法（Python `dashscope>=1.20.0`），自动处理 multipart 请求、文件上传、临时 URL 绑定及结果解析，屏蔽底层协议差异。  
  - 所有 `model experience` 支持的模态（文本、视觉、语音、3D、音乐）均遵循统一参数框架（`model` + `input` + `parameters`），降低多模态应用的集成复杂度。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `model` | string | 是 | 全模态模型标识符，必须与实际支持多模态输入的模型严格匹配（区分大小写、版本号、斜杠） | `"qwen3.8-omni-flash"`, `"qwen-vl-plus"` |
| `input` | object | 是 | 多模态输入结构体，格式由模型决定：<br>• 文图混合：`{"messages": [{"role":"user", "content":[{"text":"..."},{"image_url":"https://..."}]}]}`<br>• 音视频+文本：`{"audio_url":"...", "video_url":"...", "prompt":"..."}` | 见各模型文档的 `input` schema 定义 |
| `parameters.size` | string | 部分模型必填 | 图像/视频输出分辨率（如 `"1024*1024"`），非图像模型忽略 | `"1280*720"` |
| `parameters.n` | integer | 部分模型必填 | 生成数量（如多图输出、多候选描述） | `3` |
| `X-DashScope-OssResourceResolve` | header | 文件类请求必填 | 值为 `"enable"`，启用 OSS 临时 URL 解析 | `"enable"` |

> ⚠️ 注意：  
> - 多模态输入严禁混用字段（如向 `qwen-vl-plus` 传 `audio_url` 会报错）；务必查阅对应模型文档确认支持的 `input` 字段组合。  
> - 临时文件（OSS URL）有效期仅 48 小时，且与 `model_name` 强绑定，不可复用至其他模型。  
> - 同步多模态调用最大输入总大小 ≤ 20 MB（含所有图片/音频 base64 或 URL 指向内容）；[异步任务](asynchronous-task.md)单文件 ≤ 100 MB。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen3.8-omni-flash` + [OpenAI 兼容接口](openai-compatible-api.md)发起一次图文混合请求，5 分钟内跑通基础流程。  
- ✅ **生产推荐**：高精度需求选 `qwen3.8-omni-max`（若已发布），平衡性首选 `qwen3.8-omni-plus`；低延迟场景用 `qwen3.8-omni-flash`。  
- ✅ **避坑提示**：  
  - 不要直接拼接 `base64` 图片字符串到 `input.text` 中——必须使用 `content` 数组中的 `image_url` 或 `image` 字段；  
  - 使用 `dashscope.MultiModalGeneration.call()` 时，SDK 会自动处理文件上传和 URL 绑定，无需手动调用 `/api/v1/uploads`；  
  - 地域限制严格：所有多模态模型（含 `qwen-vl-plus`、`qwen3.5-omni-plus-realtime`）目前**仅在北京地域（华北2）可用**，跨地域调用返回 `404`。  
- ✅ **调试技巧**：开启 `debug=True`（Python SDK）或添加 `X-DashScope-Debug: true` 请求头，查看平台侧解析后的标准化 `input` 结构，快速定位字段错误。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [model experience](../guides/model-experience.md)
- [more about models](../api/more-about-models.md)
- [use cases](../guides/use-cases.md)
- [image generation](../api/image-generation.md)


