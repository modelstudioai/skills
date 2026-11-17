# asset center page

资产中心是百炼平台提供的统一资产管理入口，用于持久化保存、筛选和操作模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持通过 OSS 转存实现长期归档，并为 API 调用提供 `asset_id` 直接引用能力。所有功能均基于业务空间（workspace）隔离，需开通后方可使用，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间戳的变体（如 `qwen-image-2.0-2026-03-03`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`；
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`；
- **核心功能**：按类型/模型/时间/提示词筛选、收藏、批量删除、回收站管理、OSS 转存、资产详情查看、API 中 `asset_id` 引用。

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型名，可能为占位符或已下线版本；实际可用模型请以控制台 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 页面下拉菜单为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，可在资产详情弹窗中获取；用于 API 输入参数（替代 `image_url` 或 `image_base64`） | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 转存默认路径模板，其中 `{workspace}` 为当前业务空间 ID | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 平台存储配额 | 默认 5 GB 免费额度，超量按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入用量 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**；
2. **OSS 转存配置**：
   - 授权服务关联角色 `AliyunServiceRoleForBailianAssetForward`（SLR）；
   - 选择**未开启版本控制**的 OSS Bucket（否则转存失败）；
   - 设置转存范围（全部 / N 天前）及是否释放平台存储副本；
3. **资产操作**：
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词；
   - 收藏：悬停卡片 → 点击星标；勾选“只看收藏”快速过滤；
   - 删除：勾选后点击删除 → 进入回收站（保留 30 天）→ 可恢复或永久删除；
4. **API 集成**：
   - 生图模型：在 `control_image`、`reference_image` 等字段中传入 `"asset_id": "xxx"`；
   - 生视频模型：在 `input_video`、`first_frame` 等字段中传入 `"asset_id": "xxx"`；
   - `asset_id` 与 URL/Base64 互斥，三选一（图片）或二选一（视频）。

## 限制和注意事项

- **OSS 限制**：不支持已开启版本控制的 Bucket；转存配置为全局生效，不随业务空间切换而变更；
- **存储行为**：
  - 已转存并勾选“释放平台存储”的资产，**不再显示于资产中心列表**，也不占用平台容量；
  - 回收站中资产在 30 天内仍计费，期满自动清除且不可恢复；
- **权限控制**：需显式授予 RAM 权限策略（`AliyunBailianAssetCenterReader` 或 `AliyunBailianAssetCenterAdmin`），子账号无默认访问权；
- **数据安全**：平台不承诺因欠费、服务终止或回收站过期导致的数据可恢复性，强烈建议重要资产及时转存至自有 OSS 或本地备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


