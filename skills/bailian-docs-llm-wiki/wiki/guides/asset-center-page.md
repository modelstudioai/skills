# asset center page

资产中心是百炼平台提供的统一资产管理入口，用于持久化保存、筛选和操作模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持通过 OSS 转存实现长期归档，并为 API 调用提供 `asset_id` 直接引用能力。所有功能均基于业务空间（workspace）隔离，且需手动开通后方可使用，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间戳的变体（如 `qwen-image-2.0-2026-03-03`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`；
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`；
- **核心功能**：按类型/模型/时间/提示词筛选、收藏、批量删除、回收站管理、OSS 自动转存、API 中通过 `asset_id` 引用资产。

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型名，可能为占位命名或已下线版本；实际可用模型请以控制台实时列表及 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”章节为准。

## 关键参数

- `asset_id`：每个资产唯一标识，可在资产详情弹窗中获取，用于 API 输入（替代 `image_url` 或 `image_base64`）；
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID；
- 转存范围策略：支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本；
- 回收站保留期：固定 30 天，期间仍占用平台存储配额，到期自动永久清除。

## 使用方式

1. **开通**：首次访问 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)，点击“立即开通”启用平台存储；
2. **绑定 OSS**（可选但推荐）：在页面右上角点击“绑定 OSS”，完成 SLR 授权（`AliyunServiceRoleForBailianAssetForward`）、选择未开启版本控制的 Bucket、配置路径与转存策略；
3. **查看与筛选**：顶部统计栏显示容量使用情况；支持按类型、模型、日期、提示词关键词筛选；
4. **管理操作**：
   - 悬停卡片 → 点击星标收藏；
   - 勾选资产 → 点击“删除”进入回收站；
   - 点击卡片 → 查看含提示词、参数、模型名、生成时间的完整详情；
5. **API 集成**：调用生图/生视频 API 时，在对应输入字段（如 `control_image`、`reference_video`）中传入 `"asset_id": "xxx"`，三选一（`asset_id` / `image_url` / `image_base64`）。

## 限制和注意事项

- OSS 转存**不支持已开启版本控制的 Bucket**，否则转存失败（见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “配置 OSS 转存”说明）；
- 平台存储免费额度为 **5 GB/账号**，超量部分按 **0.15 元/GB/月** 计费；已转存并释放副本的资产不计入配额；
- 回收站内资产在 30 天保留期内仍计费，手动永久删除或自动清理后才停止计费；
- OSS 转存配置为**全局生效**，不随业务空间切换而变更；
- 删除至回收站的资产不可直接用于 API 调用，仅恢复后才重新获得有效 `asset_id`；
- 权限需通过 RAM 策略显式授予：普通用户需 `AliyunBailianAssetCenterReader`，OSS 配置权限需 `AliyunBailianAssetCenterAdmin`。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


