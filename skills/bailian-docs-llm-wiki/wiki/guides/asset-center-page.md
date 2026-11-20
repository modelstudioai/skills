# asset center page

资产中心是百炼平台提供的统一资产管理入口，用于持久化保存、筛选和操作模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持通过资产 ID（`asset_id`）在 API 中直接复用已有资产，并提供 OSS 转存、收藏、回收站等核心管理能力。所有用户均可开通使用，平台存储当前限时免费 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频，**不支持音频资产**（详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)）。
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`。
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-r2v/i2v/t2v`。
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）
  - 收藏/取消收藏、批量删除与回收站管理（保留期 30 天）
  - 资产详情查看（含完整生成参数、提示词、模型名、时间戳）
  - OSS 转存（全局配置，支持路径模板与自动释放平台副本）

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型版本名，与百炼控制台实际可用模型列表存在不一致；请以 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”章节为参考基准，但调用前务必通过 `/models` API 或控制台确认模型真实可用状态。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `asset_id` | string | 资产唯一标识，可在资产详情弹窗中获取；API 中可替代 `image_url` / `image_base64`（图片模型）或 URL / Base64（视频模型）作为输入源 |
| `{workspace}` | string | OSS 路径模板中的业务空间标识，由当前上下文自动注入 |
| `{yyyy}/{mm}/{model}/{id}.{ext}` | template | 默认 OSS 路径模板，不可自定义扩展字段（如 `{prompt_hash}`），详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通**：首次访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**。
2. **OSS 绑定**（可选但推荐）：
   - 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward`
   - 选择**未开启版本控制**的 OSS Bucket（开启版本控制将导致转存失败）
   - 配置转存范围（全部 / N 天前）及是否释放平台存储副本
3. **API 复用资产**：
   ```json
   // 生图示例：使用 asset_id 作为 control_image
   { "control_image": { "asset_id": "as-abc123" } }
   ```
   ```json
   // 生视频示例：使用 asset_id 作为 first_frame
   { "first_frame": { "asset_id": "as-def456" } }
   ```
4. **权限控制**：通过 RAM 策略授权，`AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置权限）。

## 限制和注意事项

- **存储限制**：每个账号默认 5 GB 免费平台存储额度，超量按 0.15 元/GB/月计费；已转存并释放副本的资产不计入用量。
- **回收站行为**：资产删除后进入回收站，**仍占用平台存储容量**，30 天后自动永久清除且不可恢复。
- **OSS 兼容性**：仅支持未开启版本控制的 Bucket；转存失败任务会自动重试，失败原因可查转存日志。
- **业务空间隔离**：资产列表按当前业务空间过滤，但 OSS 配置为全局生效，切换空间不影响已绑定设置。
- **安全责任**：转存至自有 OSS 后，数据安全、访问控制及费用均由用户自行承担，适用《阿里云存储服务协议》。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


