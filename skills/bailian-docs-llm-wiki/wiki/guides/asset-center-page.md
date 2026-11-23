# asset center page

资产中心是百炼平台提供的统一资产管理入口，用于持久化保存、筛选和操作模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持通过资产 ID（`asset_id`）在 API 中直接复用已有资产，并提供 OSS 转存、收藏、回收站等核心管理能力。该功能已全量开放，平台存储当前限时免费 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频，**不支持音频资产**（详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)）。
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`。
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-r2v/i2v/t2v`。
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）
  - 收藏/取消收藏、批量删除、回收站（保留 30 天）
  - 资产详情查看（含完整生成参数与提示词）
  - OSS 转存（全局配置，支持路径模板与自动释放平台副本）

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期后缀的模型名，可能为占位符或已下线版本；实际可用模型请以控制台模型列表或 `/v1/models` API 返回为准。建议优先使用无时间后缀的稳定版（如 `qwen-image-2.0-pro`），并参考最新 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 确认兼容性。

## 关键参数

- `asset_id`：每个资产唯一标识，可在资产详情弹窗中获取，用于 API 输入复用。
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识。
- 转存范围策略：支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本。
- 平台存储配额：默认 5 GB 免费额度，超量按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入配额。

## 使用方式

1. **开通**：首次访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**。
2. **OSS 绑定**（可选但推荐）：
   - 授权服务关联角色 `AliyunServiceRoleForBailianAssetForward`
   - 选择**未开启版本控制**的 OSS Bucket（开启版本控制将导致转存失败）
   - 配置路径模板与转存策略
3. **API 复用资产**：
   - 生图模型：在 `image_url` / `image_base64` 参数位置，替换为 `"asset_id": "xxx"`（三选一）
   - 生视频模型：在视频/图片输入字段（如 `input_video`, `first_frame_image`）中同理传入 `"asset_id"`
4. **管理操作**：通过卡片悬停操作（收藏、删除）、顶部筛选栏、右上角回收站入口完成日常管理。

## 限制和注意事项

- OSS 转存**不支持已开启版本控制的 Bucket**，否则任务失败且重试无效（见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)）。
- 回收站资产保留期为 **30 天**，到期自动永久清除，不可恢复；手动永久删除亦不可逆。
- 平台存储容量统计包含回收站内资产；释放平台副本（OSS 转存时勾选）后，该资产不再显示于资产中心，也不再占用配额。
- 权限需显式授予 RAM 策略：普通用户需 `AliyunBailianAssetCenterReader`，OSS 配置权限需 `AliyunBailianAssetCenterAdmin`。
- 切换业务空间后，资产列表实时变更，但 OSS 转存配置保持全局一致，不受业务空间影响。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


