# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，支持筛选、收藏、删除、OSS 转存及 API 直接引用等关键能力。所有用户均可开通使用，平台存储当前限时免费；资产默认保存于百炼平台存储，也可通过配置自动同步至用户自有 OSS Bucket。详细功能说明请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`；
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-r2v/i2v/t2v`；
- **核心功能**：按类型/模型/时间/提示词筛选、收藏、批量删除、回收站管理、OSS 自动转存、资产详情查看、API 中通过 `asset_id` 直接引用资产。

> **注意**：原始文档中列出的 `qwen-image-2.0-2026-03-03` 等带未来日期后缀的模型名，可能为占位命名或已下线版本；实际可用模型请以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 控制台下拉列表或最新 API 文档为准。

## 关键参数

- `asset_id`：每个资产唯一标识符，用于 API 调用中替代 `image_url` 或 `image_base64`（生图模型三选一；生视频模型二选一）；
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID；
- 转存范围策略：支持“全部资产”或“N 天前的资产”；
- 平台存储容量显示格式：`已用容量 / 免费额度`（如 `0.00 / 5 GB`），详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**；
2. **OSS 绑定**：
   - 授权服务关联角色 `AliyunServiceRoleForBailianAssetForward`（SLR）；
   - 选择未开启版本控制的 OSS Bucket（**注意**：开启版本控制的 Bucket 不支持转存）；
   - 配置地域、Bucket、路径模板及转存策略（含是否释放平台存储副本）；
3. **资产操作**：
   - 筛选：顶部筛选栏支持类型、模型、日期范围、提示词关键词；
   - 收藏/取消收藏：悬停卡片 → 点击星标；勾选**只看收藏**可过滤；
   - 删除：单选或多选 → 点击删除 → 进入回收站（保留 30 天）；
   - 查看详情：点击卡片 → 弹窗中获取 `asset_id`、提示词、参数、生成时间等完整元数据；
4. **API 集成**：在调用生图/生视频 API 时，将 `asset_id` 填入对应输入字段（如 `control_image.asset_id`），无需额外上传。

## 限制和注意事项

- **OSS 限制**：不支持已开启版本控制的 Bucket；转存配置为全局生效，不随业务空间切换而变更；
- **存储行为**：
  - 回收站内资产仍占用平台存储容量，30 天后自动永久清除且不可恢复；
  - 选择“释放平台存储”后，资产不再显示于资产中心，也不计入平台存储用量；
- **权限控制**：需显式授予 RAM 权限策略（`AliyunBailianAssetCenterReader` 或 `AliyunBailianAssetCenterAdmin`）；
- **计费说明**：免费额度为 5 GB/账号；超量部分按 0.15 元/GB/月计费，与百炼模型用量合并结算；
- **数据安全提醒**：平台不承担因欠费、服务终止或回收站过期导致的数据丢失责任，建议重要资产及时转存至自有 OSS 或本地备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


