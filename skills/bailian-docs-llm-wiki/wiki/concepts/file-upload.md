# 文件上传

文件上传是百炼平台中将本地或外部文件安全、可靠地传输至平台托管存储的服务能力，为模型微调、内容解析、多模态推理、知识库构建及翻译等下游任务提供结构化数据输入基础。该能力不直接执行模型计算，而是作为前置数据准备环节，通过统一的 API 接口完成文件注册、元信息绑定与资源标识生成。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型微调（Fine-tuning）**：上传 `.jsonl`（文本微调）或 `.zip`（图像/视频微调，单个 ≤ 1 GB），指定 `purpose=fine-tune`，文件将被校验格式并接入训练流水线；  
- **文件内容提取（File Extract）**：上传 PDF、Word、Excel 等文档（≤ 150 MB），设 `purpose=file-extract`，触发 OCR、表格识别、语义切片等结构化解析；  
- **Batch 异步推理**：上传批量请求文件（如含多条 [prompt](../guides/prompt.md) 的 `.jsonl`，≤ 500 MB），设 `purpose=batch`，用于创建大规模异步任务；  
- **多模态模型调用（如 VL 模型）**：通过「上传获取临时 URL」能力，将本地图片/音视频上传至百炼临时存储，获得带签名的 `oss://` URL（48 小时有效），再在模型请求中传入该 URL（需 Header 添加 `X-DashScope-OssResourceResolve: enable`）；  
- **知识库构建**：在知识库数据源配置中上传本地文档（PDF/DOCX/TXT 等，单文件 ≤ 200 MB），平台自动完成解析、切片与向量化，无需手动调用文件管理 API；  
- **Qwen-MT-Uni 翻译**：支持直接传入 `input.fileUrl`（HTTPS 链接），但若文件仅存于本地，需先调用文件上传 API 获取可公开访问的临时 URL，再填入翻译请求。

> ⚠️ 注意：所有上传操作必须使用与后续调用场景**同属一个阿里云主账号**的 API Key；子业务空间调用时，上传与模型请求的 API Key 必须属于该子空间所属主账号。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必选 | 说明 |
|------|------|------|------|------|
| `files` | `multipart/form-data` body | 文件流 | ✅ | 支持一次上传多个文件；每个 `files` 字段对应一个文件（如 `--form 'files=@file1.pdf' --form 'files=@file2.jsonl'`） |
| `purpose` | `multipart/form-data` body | string | ⚠️ 强烈建议指定 | 取值：`fine-tune` / `file-extract` / `batch`；未指定则文件可上传成功，但无法被下游任务自动识别和调度 |
| `descriptions` | `multipart/form-data` body | string | ❌ | 文件描述，建议 ≤ 500 字符，便于人工管理 |
| `model`（仅临时 URL 场景） | `multipart/form-data` body | string | ✅（临时 URL 场景） | 必须与后续模型调用的 `model` 参数完全一致（如 `qwen-vl-plus`），否则调用失败 |

**地域限制**：文件管理 API（`/api/v1/files`）当前仅在北京 Region（`cn-beijing`）可用；其他地域用户请通过对应地域控制台操作，或使用 [OpenAI 兼容接口](openai-compatible-interface.md)（`/compatible-mode/v1/files`），后者支持多地域。

**配额约束**（按账号维度）：
- 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（`.zip` 包 ≤ 1 GB）；
- 总存储空间：100 GB（有效文件）；
- 总文件数量：10,000 个（有效文件）。

## 面向开发者：推荐实践

- ✅ **新项目首选 [OpenAI 兼容接口](openai-compatible-interface.md)**：使用 `/compatible-mode/v1/files`（支持标准 `file` + `purpose` 字段），语义清晰、持续演进、多地域可用；  
- ✅ **批量上传优先合并请求**：一次 `POST /api/v1/files` 可传多个 `files`，减少 HTTP 开销；  
- ✅ **用途必须显式声明**：始终传 `purpose`，避免因元信息缺失导致下游任务失败；  
- ✅ **大文件/敏感文件走 OSS 挂载**：视频/图像微调数据量大时，推荐将原始数据集挂载至 OSS 后通过路径引用，跳过上传环节；  
- ❌ **勿混用 API Key 所属账号**：上传用的 API Key 与模型调用用的 API Key 必须归属同一主账号，跨账号无效；  
- 🔍 **上传后务必检查响应**：成功响应中 `data.uploaded_files[].file_id` 是后续查询、删除、任务绑定的唯一凭证；失败时检查 `data.failed_uploads[]` 中的错误码（如 `BadRequest.TooLarge`）。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [more about models](../api/more-about-models.md)
- [application call](../api/application-call.md)
- [knowledge base](../guides/knowledge-base.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


