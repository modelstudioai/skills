# 文件上传与管理

文件上传与管理是百炼平台中统一处理用户数据输入的核心能力，用于将本地或外部文件安全、高效地导入平台，并按用途绑定至下游模型任务（如微调、内容解析、批量推理、多模态推理等），实现文件的生命周期管控与跨场景复用。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型微调（Fine-tuning）**：上传训练数据（如 `.jsonl` 文本数据集，或含图像/视频的 `.zip` 包），需指定 `purpose=fine-tune`；文本类单文件 ≤300 MB，视频/图像微调 zip 包 ≤1 GB。上传后文件可在控制台「模型调优」页直接选用。
- **文档内容提取（File Extract）**：上传 PDF、Word、Excel、PPT 等格式文档，指定 `purpose=file-extract`（单文件 ≤150 MB），供结构化内容解析服务调用。
- **异步批量任务（Batch）**：上传 JSONL 格式输入文件，指定 `purpose=batch`（单文件 ≤500 MB），用于创建 OpenAI 兼容的 Batch 任务，实现低成本、高吞吐的离线推理。
- **多模态模型推理（Vision/Audio/Video）**：不通过文件管理 API，而是调用 `/api/v1/uploads?action=getPolicy` 获取临时上传策略，直传至 OSS 并获得 `oss://...` URL；模型请求时需携带该 URL 及请求头 `X-DashScope-OssResourceResolve: enable`。
- **[OpenAI 兼容接口](openai-compatible-interface.md)集成**：推荐优先使用 OpenAI 兼容的 File 接口（`POST /v1/files`），行为与 `openai.Files.create()` 一致，支持相同参数和响应格式，兼容主流 SDK（如 `openai`、`langchain_openai`），且无地域限制（原生文件管理 API 仅限北京 Region）。

> ✅ 最佳实践：新项目请统一使用 OpenAI 兼容 File 接口；历史系统迁移时，注意 `purpose` 字段必须显式声明，否则文件无法被下游任务自动识别。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `files` | `multipart/form-data` | 文件流 | 是 | 支持一次上传多个文件；每个 `files` 字段对应一个独立文件 |
| `purpose` | `multipart/form-data` | string | 建议必填 | 取值：`fine-tune` / `file-extract` / `batch`；决定文件用途与下游能力绑定，**未指定则文件不可被自动调度** |
| `model`（多模态场景） | query 或 body | string | 是（仅临时 URL 场景） | 必须与后续模型调用的 `model` 完全一致（如 `qwen3-vl-plus`），用于生成匹配的上传策略 |
| `page_no` / `page_size` | query | integer | 列举时必填 | 分页查询参数；`page_size` 范围 1–100（默认 10） |

**配额约束（生效于所有上传路径）**：
- 总存储空间：100 GB（仅计算未删除的有效文件）
- 总文件数量：10,000 个（仅计算未删除的有效文件）
- 单文件大小：依 `purpose` 动态限制（见上文各场景说明）

**地域说明**：
- 原生文件管理 API（`/api/v1/files`）仅在北京 Region 可用；
- OpenAI 兼容 File 接口、临时文件上传策略（`/api/v1/uploads`）支持全部开通地域（如北京、上海、新加坡、弗吉尼亚等），推荐新接入使用。

## 面向开发者：快速开始

```bash
# ✅ 推荐：使用 OpenAI 兼容接口（无需改 SDK，仅换 base_url）
curl -X POST "https://<workspace-id>.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/files" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -F "file=@data.jsonl" \
  -F "purpose=fine-tune"

# ⚠️ 兼容：原生接口（仅北京可用）
curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -F "files=@report.pdf" \
  -F "purpose=file-extract"

# 📸 多模态：先获策略，再直传 OSS（返回 oss:// URL）
curl -X POST "https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model=qwen3-vl-plus" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

> 💡 提示：上传成功后，响应中 `file_id` 可用于后续查询、删除或作为任务输入；所有文件操作均需 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证，API Key 需与目标地域匹配。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)
- [model production](../api/model-production.md)


