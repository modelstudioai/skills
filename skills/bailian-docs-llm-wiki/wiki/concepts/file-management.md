# 文件管理

文件管理是百炼平台中统一处理用户上传的原始多模态资源（图像、音频、文本类文件）的核心能力，为后续模型调用提供安全、可追溯、标准化的文件引用机制。所有需输入非文本内容的模型（如视觉、语音、3D、视频等）均要求先通过文件管理 API 上传并获取 `file_id`，再在请求中以该 ID 引用资源，而非直接传输原始二进制数据。

## 在百炼平台的不同场景中，这个概念如何使用

- **多模态大模型调用（Qwen-VL / Qwen2-Audio / Qwen2-VL / Qwen3-VL）**：必须先上传图像或音频文件，指定 `purpose=vision` 或 `purpose=audio`，获得 `file_id` 后，在消息体中以 `{"file_id": "file-xxx"}` 形式引用；未按 purpose 分类上传将导致模型拒绝处理。
- **图像生成与编辑（如 Qwen-Image、WanX 等）**：支持直接传入公网 URL 或 Base64，但若需复用同一文件多次、或文件来自私有存储（如 OSS），推荐先通过文件管理 API 上传，再在图像 API 的 `input` 字段中传 `file_id`（部分模型如 `qwen-image-3.0` 已原生支持该方式）。
- **音频处理（ASR/TTS）**：ASR 异步任务支持 `file_urls` 数组，但若音频源为本地文件或需统一权限管控，建议先上传至文件管理服务，再将生成的 `file_id` 转换为临时可公开访问的 `file_url`（通过 `GET /v1/files/{file_id}` 获取 `download_url`）供 ASR 任务消费。
- **视频生成与 3D 生成**：当前主流视频/3D 模型（如 Wan2.7-i2v、Tripo）暂不直接接受 `file_id`，需提供公网可直连的 `image_url` 或 `video_url`；但开发者可利用文件管理服务作为中间枢纽——上传后立即获取 `download_url`（有效期 24 小时），再将其注入视频/3D 请求的 `input` 字段，实现安全可控的资源流转。
- **跨模型协同工作流**：例如“语音转文字 → 提取关键帧 → 图像生成 → 视频合成”，各环节输出的中间文件（如 ASR 结果文本、抽帧图像）均可通过文件管理 API 上传并持久化，用 `file_id` 串联整个 pipeline，避免重复上传与 URL 失效风险。

## 关键参数和配置

- `purpose`（字符串，非必填，默认 `"assistants"`）：**最关键业务标识**，决定文件解析策略与下游模型兼容性。必须显式设为 `"vision"`（图像）、`"audio"`（音频）或 `"assistants"`（通用文本/PDF），其中视觉模型强制校验此值。
- `file`（multipart 表单字段）或 `file_base64`（字符串）：二进制文件载体；推荐优先使用 multipart 上传，避免 Base64 编码开销与长度限制。
- `file_id`（字符串，只读）：上传成功后返回的全局唯一标识，格式为 `file-xxxxxxxx`，用于所有后续查询、删除及模型引用。
- `limit` / `offset`（整数）：列表接口分页参数，默认 `limit=20`, `offset=0`；适用于批量管理文件生命周期。
- **隐式约束**：
  - 单文件大小上限：图像 ≤ 20 MB，音频 ≤ 100 MB，文本 ≤ 50 MB；
  - 文件自动清理策略：30 天内未被任何模型请求引用的文件将被系统回收；
  - 删除保护：已被模型请求引用中的文件无法删除（API 返回 HTTP 409）。

> ⚠️ 注意：`purpose` 是硬性路由开关——即使上传的是 JPG 文件，若设为 `"assistants"`，后端不会执行 OCR 或视觉特征提取，仅作通用文本附件处理；调用 Qwen-VL 时若遗漏此参数或设错，请求将直接失败。

## 面向开发者，简洁实用

- **一步上传 + 立即可用**：  
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
    -H "Authorization: Bearer $API_KEY" \
    -F "file=@photo.jpg" \
    -F "purpose=vision"
  # 响应含 "id": "file-abc123", "status": "uploaded"
  ```

- **轮询就绪（异步场景必需）**：  
  若响应 `status` 为 `"processing"`，需轮询 `GET /v1/files/file-abc123` 直至 `status == "processed"`（通常 <5 秒）；不可跳过此步直接提交模型请求。

- **模型中引用（标准格式）**：  
  ```json
  {
    "model": "qwen-vl-plus",
    "input": {
      "messages": [
        {
          "role": "user",
          "content": [{"file_id": "file-abc123"}]
        }
      ]
    }
  }
  ```

- **清理旧文件（推荐定期执行）**：  
  先 `GET /v1/files?limit=100` 获取列表，筛选 `created_at` 超过 30 天且 `status == "processed"` 的 `file_id`，再逐个 `DELETE /v1/files/{file_id}`；已删除文件不可恢复，请谨慎操作。

- **调试技巧**：  
  使用 `GET /v1/files/{file_id}` 查看完整元信息（`filename`, `mime_type`, `size`, `status`, `created_at`），快速定位上传失败原因（如 mime_type 识别错误、size 超限、purpose 不匹配）。

## 关联主题页

- [file management api](../api/file-management-api.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [audio api directory](../api/audio-api-directory.md)
- [3d generation](../api/3d-generation.md)


