# asset center page

资产中心是百炼平台提供的统一资产管理入口，用于持久化保存、筛选和操作模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持通过资产 ID（`asset_id`）在 API 中直接复用已有资产，并提供 OSS 转存、收藏、回收站等核心管理能力。该功能已全量开放，平台存储当前限时免费 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频，**不支持音频资产**（详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)）。
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`。
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-r2v/i2v/t2v`。
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）
  - 收藏/批量删除/回收站（保留 30 天）
  - OSS 转存（含自动重试与日志查看）
  - 资产详情页展示完整生成上下文（提示词、参数、模型、时间）
  - API 层 `asset_id` 直接引用（替代 `image_url` 或 `image_base64`）

> **注意**：文档中列出的 `qwen-image-2.0-2026-03-03` 等带未来日期的模型版本名，可能为占位符或已下线；实际可用模型请以控制台实时列表为准，避免硬编码模型名 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `asset_id` | string | 资产唯一标识，可在资产详情弹窗中获取；API 输入时与 `image_url` / `image_base64` 三选一（图片）或二选一（视频） |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | path template | OSS 转存默认路径模板，其中 `{workspace}` 为当前业务空间标识 |
| 转存范围策略 | enum | `all`（全部资产）或 `older_than_n_days`（N 天前），绑定时配置 |
| 释放平台存储 | boolean | 若启用，转存成功后资产将从资产中心移除且不再占用容量 |

## 使用方式

1. **开通**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。
2. **OSS 绑定**：
   - 授权服务关联角色 `AliyunServiceRoleForBailianAssetForward`
   - 选择**未开启版本控制**的 OSS Bucket（否则转存失败）
   - 配置路径模板、转存范围及是否释放平台存储副本
3. **API 引用**：
   - 生图模型：在 `input.image` 或控制图字段中传入 `{ "asset_id": "xxx" }`
   - 生视频模型：在 `input.video` 或 `input.image` 字段中传入 `{ "asset_id": "xxx" }`
4. **管理操作**：
   - 悬停卡片 → 星标收藏 / 复选框 → 批量删除 → 回收站恢复或永久清除

## 限制和注意事项

- **OSS 限制**：不支持已开启版本控制的 Bucket；转存配置为全局生效，不随业务空间切换而变更。
- **存储计费**：
  - 免费额度：5 GB/账号，超出部分按 0.15 元/GB/月计费
  - 回收站内资产在 30 天保留期内**仍占用平台存储并计费**
  - 已转存且启用“释放平台存储”的资产**立即停止计费**
- **数据安全**：平台不承诺因欠费、服务终止或回收站过期导致的数据恢复；重要资产须主动转存至自有 OSS 或本地备份。
- **权限隔离**：资产列表按业务空间隔离，但 OSS 配置、RAM 权限策略（如 `AliyunBailianAssetCenterAdmin`）作用于账号维度。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


