# 文件管理

文件管理是百炼平台中统一处理用户上传文件资源的核心能力，用于为多模态模型（如 Qwen-VL、Qwen2-Audio）提供安全、可控、可追溯的输入文件托管与引用机制。所有需以图像、音频、文档等非文本形式参与推理的请求，必须先完成文件上传并获取唯一 `file_id` 或临时 `oss://` URL，后续调用方可通过该标识引用文件内容。

## 在百炼平台的不同场景中，这个概念如何使用

- **多模态模型推理（Qwen-VL / Qwen2-Audio 等）**：必须通过 `/api/v1/files` 上传文件，获取 `file_id` 后在模型请求中以 `{"file_id": "xxx"}` 形式传入；不支持直接传原始二进制或公网 URL。  
- **图像/音视频生成与编辑（Image Generation / Audio API）**：部分能力（如图生图、语音识别）支持两种路径：① 使用 `file_id`（需先调用文件管理 API）；② 使用临时 OSS URL（需先调用 `/api/v1/uploads?action=getPolicy` 获取上传策略，再直传 OSS）。二者不可混用，且模型请求时需显式声明 `X-DashScope-OssResourceResolve: enable`（OSS 方式）或确保 `file_id` 有效（文件管理方式）。  
- **Agent 上下文中的结构化解析（ParseX）**：当 Agent 配置启用 `parsex_ocr_enabled: true` 且使用 `qwen-vl` 模型时，可将上传的 PDF/图片文件通过 `file_id` 注入上下文，由 ParseX 自动执行 OCR、表格提取等预处理。  
- **[异步任务](asynchronous-task.md)（如视频生成、长音频翻译）**：文件作为任务输入载体，必须提前完成上传流程；任务创建接口（如 `/v1/tasks`）仅接受 `file_id` 或 `oss://` URL，不支持内联文件。  
- **不适用场景**：纯文本模型（如 `qwen-max`、`qwen-plus`）**明确拒绝** `file_id` 输入；若误传将返回 `400 Bad Request`；其上下文扩展依赖 RAG 或 Memory，而非文件管理。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `file` | binary | 是（表单上传） | 原始文件流，支持 PNG/JPEG/MP3/WAV/PDF/TXT/DOCX 等（详见格式清单） |
| `filename` | string | 否（推荐） | 显式指定文件名，影响 MIME 类型推断；缺失且服务端无法识别扩展名时上传失败 |
| `purpose` | string | 否 | 取值 `"vision"`（默认，用于图像理解）或 `"batch"`（用于异步批量任务）；`"audio"` 已废弃，静默转为 `"vision"` |
| `file_id` | string | — | 上传成功后返回的唯一标识，有效期 30 天（无调用记录可能提前清理），不可复用 |
| `oss://` URL | string | — | 通过 `/api/v1/uploads?action=getPolicy` 获取策略后直传 OSS 得到，有效期 48 小时，需与模型名称严格绑定 |

> ⚠️ 注意：  
> - 单文件大小限制：文档类（PDF/DOCX）≤ 100 MB，音视频类（MP3/WAV/MP4）≤ 50 MB；超限返回 `413 Payload Too Large`。  
> - 权限要求：所有文件管理 API 请求必须携带 `Authorization: Bearer <api_key>`，且 `api_key` 需具备 `files:write` 权限。  
> - 幂等性：同一 `file_id` 在 10 秒内不可重复用于不同请求，否则可能触发校验失败。  

## 面向开发者，简洁实用

- ✅ **首选上传方式**：对 ≤100 MB 文件，使用 `multipart/form-data` 调用 `/api/v1/files`（最简、兼容性最好）；避免 base64 编码（仅限 ≤1 MB 文本文件）。  
- ✅ **快速验证**：上传后立即用 `GET /api/v1/files/{file_id}` 查询状态，确认 `status: "uploaded"` 再用于模型调用。  
- ✅ **生产建议**：高并发场景下，优先复用已上传的 `file_id`（如用户头像、模板文档），避免重复上传；定期调用 `GET /api/v1/files` 清理闲置文件。  
- ❌ **禁止操作**：不要将 `file_id` 硬编码进客户端；不要尝试用 `file_id` 调用纯文本模型；不要依赖废弃的 `"audio"` purpose。  
- 🔗 **关联动作**：文件上传是前置步骤，后续必须与具体模型能力对齐——例如 `qwen-vl-plus` 要求 `purpose="vision"`，异步批处理任务需 `purpose="batch"`。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [image generation](../api/image-generation.md)
- [audio api directory](../api/audio-api-directory.md)
- [agent context](../guides/agent-context.md)
- [more about models](../api/more-about-models.md)


