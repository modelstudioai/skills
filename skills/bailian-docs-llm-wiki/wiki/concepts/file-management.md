# 文件管理

文件管理是百炼平台中统一处理用户上传文件资源的核心能力，为多模态模型调用提供安全、可追溯、标准化的文件生命周期支持。所有需以图像、音频或文本作为输入的模型（如 Qwen-VL、Qwen2-Audio、文档解析等），均要求先通过文件管理 API 上传并获得唯一 `file_id`，后续请求方可通过该 ID 引用文件——文件本身不直接传入模型接口。

## 在百炼平台的不同场景中，这个概念如何使用

- **多模态模型调用（Qwen-VL / Qwen2-Audio / Qwen2-VL）**：必须先上传图像/音频文件，获取 `file_id`，再在 `messages` 中以 `{"type": "image_url", "image_url": {"url": "file-xxx"}}` 或类似结构引用；`purpose` 参数决定后端解析策略（如 `vision` 触发 OCR 和结构化解析）。
- **文档与音视频解析（ParseX）**：支持直接上传本地文件（PDF/Word/MP4 等）或提供公网 URL；若上传本地文件，底层仍经由文件管理 API 处理并生成临时 `file_id`，再交由解析服务调度；解析结果中的 `citations` 也基于该 `file_id` 定位原始内容。
- **音频类 API（ASR/TTS/Music Gen）**：当输入为二进制音频（非 URL）时，需通过 `/v1/files` 上传，返回 `file_id` 后在 `input.audio_url` 字段中填入 `"file-{id}"`；此方式规避了公网 URL 部署和有效期限制，适用于私有环境或敏感音频。
- **图像/视频生成类 API**：当前**不直接依赖文件管理 API**，因图生图、首帧生成等任务要求输入为公网可访问 URL；但若用户本地有图像/视频需参与生成，推荐先调用文件管理 API 上传并获取 `file_id`，再将其转换为平台托管的 HTTPS URL（响应中 `url` 字段即为此地址），最后传入图像/视频生成接口。
- **字段抽取（Field Extraction）**：仅支持复用已解析文档的 `biz_id`，**不接受原始 `file_id`**；但文档解析任务本身若以本地文件为输入，则其内部流程已隐式调用文件管理模块完成上传与注册。

> ✅ 关键共识：`file_id` 是百炼平台内文件的“逻辑身份证”，跨服务、跨模型共享；它解耦了文件存储、预处理与模型消费，是实现安全隔离、配额控制和异步状态管理的基础单元。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 原始文件二进制流；图像/音频 ≤ 100 MB，文本 ≤ 50 MB |
| `purpose` | form-data | string | 否 | 取值 `vision`（图像）、`audio`（音频）、`assistants`（通用）；决定后端解析行为，默认 `assistants`；**不可省略或误配，否则模型调用将失败** |
| `file_id` | path / response body | string | — | 上传成功后返回，格式 `file-xxxxxxxx`；全局唯一，永久有效（冷数据可能 90 天后自动清理） |
| `limit` / `offset` | query | integer | 否 | 列表接口分页参数，默认 `limit=20`, `offset=0` |

- **配额控制**：按项目级（Workspace）统一分配总空间，默认 10 GB；可在控制台查看与调整。
- **状态机**：文件生命周期含 `uploaded` → `processing` → `processed`（成功）或 `failed`；仅 `processed` 状态方可用于模型调用。
- **删除约束**：`DELETE /v1/files/{file_id}` 仅在文件未被任何活跃会话、历史 trace 或解析任务引用时允许执行；操作不可逆。

## 面向开发者，简洁实用

- ✅ **必做三步**：上传（带 `purpose`）→ 轮询至 `status == "processed"` → 在模型/解析请求中引用 `file-id`。
- ✅ **推荐实践**：
  - 优先使用 `multipart/form-data` 上传，避免 base64 编码开销；
  - 对图像/音频任务，显式指定 `purpose=vision` 或 `purpose=audio`，勿依赖默认值；
  - 上传后立即轮询（间隔 ≥ 1s），避免在 `processing` 状态下提前调用模型（返回 400）；
  - `file_id` 可缓存复用，无需重复上传相同文件。
- ⚠️ **避坑提示**：
  - 不支持视频直传（需抽帧为图像序列或转为 URL）；
  - `file_id` 不能直接用于图像/视频生成 API 的 `img_url` 字段——需先用 `GET /v1/files/{id}` 获取其托管 URL（`response.url`）再传入；
  - SDK 示例中若出现 `file_type` 或 `type=image` 等旧参数，请忽略，以 `purpose` 为准；
  - 删除前务必确认无引用，否则返回 `409 Conflict`。

文件管理不是辅助功能，而是百炼多模态能力的基础设施层。掌握其状态流转与参数语义，是构建稳定、高效 AI 应用的第一步。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [audio api references](../api/audio-api-references.md)
- [api overview](../api/api-overview.md)


