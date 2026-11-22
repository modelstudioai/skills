# 多模态

多模态（Multimodal）指模型能够同时理解、生成或处理两种及以上类型的数据模态（如文本、图像、音频、视频、3D 模型等），并在不同模态间建立语义对齐与联合推理能力。在百炼平台中，“多模态”不仅是一种模型能力分类，更是一类统一调用范式——它定义了输入结构、API 路由、参数约束及服务协议的共性规范。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，“多模态”不是单一模型，而是一组**能力范式统一、接口协议收敛、部署策略协同**的服务集合，覆盖以下核心场景：

- **多模态理解与生成（`multimodal-generation`）**：  
  如 `qwen-vl-plus`（图文理解）、`qwen-audio`（音文理解）、`qwen4-max`（支持文本+图像+音频混合输入）等模型，通过 `/v1/services/aigc/multimodal-generation/generation` 接口调用，输入为结构化 `messages` 数组，其中 `content` 字段可混合包含 `text`、`image_url`、`audio_url` 等类型对象（需符合 OpenAI 兼容格式）。适用于跨模态问答、图文摘要、音视频内容分析等任务。

- **图像生成（`image-generation`）**：  
  千问图像（`qwen-image-*`）、万相（`wan2.*-image-*`）、Vidu、可灵等模型虽以“图像输出”为主，但其输入天然支持文本（prompt）+ 参考图（`image_url`）+ 控制图（mask/sketch）等多模态组合，属于典型的**生成式多模态**。调用时需使用 `/v1/services/aigc/image-generation/generation` 路由，并按模型要求组织 `input` 字段（如 `prompt` + `image_url` + `mask_url`）。

- **视频生成（`video-generation`）**：  
  所有视频模型（HappyHorse、万相3.0、PixVerse、Kling、Vidu）均强制要求多模态输入：文生视频需 `prompt`；图生视频需 `first_frame_url`；参考生视频需 `reference_images` 或 `reference_video_url`；动作迁移需 `video_url` + `audio_url`。统一通过 `/v1/services/aigc/video-generation/video-synthesis` 调用，且必须启用异步模式（`X-DashScope-Async: enable`）。

- **3D 生成（`3d-generation`）**：  
  Tripo 系列模型支持文生3D（`prompt`）、单/多图生3D（`image` / `images`）、Gaussian Splat（`image_url`），后处理任务还依赖前序 `task_id` 或 `model_url`，构成“文本→图像→3D→贴图→绑定”的多阶段多模态流水线。全部接口位于 `/v1/services/aigc/3d-generation/...` 下。

- **多模态翻译（`qwen-mt-uni`）**：  
  `qwen-mt-uni` 是百炼唯一标定为“全模态统一翻译”的模型，可接受文本字符串、PDF/DOCX 文档 URL、JPG/PNG 图像 URL、MP3/WAV 音频 URL 等任意输入形式，并自动识别模态、执行端到端翻译与格式保真重构。调用路径为 `/v1/services/aigc/mt-translation/generation`，`input` 字段为泛型 `source`（支持 `string`、`object` 或 `array`）。

> ✅ 关键识别特征：凡调用路径含 `multimodal-`、`image-`、`video-`、`3d-` 或 `mt-translation`（且模型为 `qwen-mt-uni`），即属多模态范畴；其共同约束是：**输入非纯文本，必须显式携带模态标识与对应数据载体（URL 或 Base64）**。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必填 | 适用场景 |
|------|------|------|----------|----------|
| `model` | `string` | 必须为平台已开通的多模态模型 ID（如 `qwen-vl-plus`、`qwen-image-3.0-pro`、`pixverse/pixverse-v6-max-t2v`、`Tripo/Tripo-H3.1`、`qwen-mt-uni`），区分大小写，严格匹配 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) | ✅ | 全部 |
| `input` | `object` | 多模态输入容器，结构因模型而异：<br>• `multimodal-generation`: `messages[]`，每条 message 的 `content` 为 `{type: "text"/"image_url"/"audio_url", text/image_url/audio_url: ...}`<br>• `image-generation`: `{prompt, image_url?, mask_url?, ...}`<br>• `video-generation`: `{prompt?, first_frame_url?, reference_images[], media[]}`<br>• `3d-generation`: `{prompt?, image?, images[], original_model_task_id?, model_url?}`<br>• `mt-translation`: `{source: string/object/array}` | ✅ | 全部 |
| `X-DashScope-Async` | `header` | 异步调用必需头字段，值必须为 `"enable"`（注意引号）。**所有视频、3D、部分图像及文档/长音频翻译任务强制要求**；纯文本/短图/短音频翻译可选同步。 | ⚠️ 条件必填 | 视频、3D、大文件翻译等耗时任务 |
| `size` / `resolution` / `geometry_quality` | `string` | 输出规格控制参数，含义与取值范围依模型而定（如 `qwen-image-3.0-pro` 支持 `"1024*1024"`，`pixverse-v6-max` 支持 `"1080P"`，`Tripo-H3.1` 支持 `"ultra"`） | ❌ 可选 | 图像、视频、3D 生成 |
| `watermark` | `boolean` | 图像生成模型专用，控制是否添加平台水印（默认 `true`） | ❌ 可选 | 图像生成 |
| `sensitives`, `glossary`, `domainHint` | `object/array` | 多模态翻译专属参数，用于敏感词过滤、术语干预、领域提示 | ❌ 可选 | `qwen-mt-uni` 等翻译模型 |

> 💡 开发者提示：  
> - 多模态请求**必须使用业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），且 `region`、API Key、模型三者地域必须严格一致；  
> - 所有图像/视频/3D/音频 URL 必须为**公网可访问的 HTTPS 地址**（不支持本地文件或内网地址）；  
> - 输入内容长度、文件大小、分辨率等硬性限制由具体模型决定，超出将返回 `400 Bad Request`，请查阅对应模型文档的「限制」章节。

## 面向开发者，简洁实用

- ✅ **快速判断是否为多模态调用**：看 API 路径是否含 `multimodal`/`image`/`video`/`3d`/`mt-translation`，且 `input` 中出现 `image_url`、`audio_url`、`video_url`、`fileUrl`、`prompt` + `image` 组合等非纯文本字段。  
- ✅ **统一调试技巧**：先用 `curl -v` 发送最小合法请求（仅 `model` + 最简 `input`），观察返回的 `error.code` 和 `error.message`，90% 的问题源于 `model` ID 错误、地域不匹配、URL 不可达或 `X-DashScope-Async` 缺失。  
- ✅ **错误速查**：  
  > `InvalidParameter.Input` → `input` 格式错误（如 `image_url` 缺失 `type` 字段）；  
  > `Forbidden.AccessDenied` → API Key 未开通该模型或地域不匹配；  
  > `BadRequest.InvalidInput` → URL 不可访问、文件超限或 `size` 超出模型支持范围；  
  > `UnsupportedMediaType` → 请求头 `Content-Type` 未设为 `application/json`。  
- ✅ **生产建议**：关键业务链路优先选用 `qwen-vl-plus`（图文）、`qwen-image-3.0-pro`（图像）、`qwen-mt-uni`（翻译）、`Tripo/Tripo-H3.1`（3D）等主力

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


