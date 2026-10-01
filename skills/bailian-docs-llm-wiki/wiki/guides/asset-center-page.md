# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于平台存储（限时免费），用户可通过控制台或 API 全生命周期管理生成内容。详细功能说明请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；对应模型包括 `qwen-image-*` 系列（如 `qwen-image-3.0-pro`、`qwen-image-2.0-2026-03-03`）、`wan2.7-*` 全系列（`t2v`/`i2v`/`r2v`/`videoedit` 等）及 `z-image-turbo`。完整列表以控制台实时展示为准，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）
  - 收藏/批量删除/回收站恢复
  - OSS 自动转存（含路径模板、释放平台副本选项）
  - 资产详情查看（含完整生成参数）
  - API 层 `asset_id` 直接引用（替代 `image_url` 或 `image_base64`）

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型名，实际为内部版本标识，控制台当前仅显示稳定版模型（如 `qwen-image-2.0-pro`）。请以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 页面实际下拉选项为准，避免硬编码过期模型名。

## 关键参数

- `asset_id`：全局唯一字符串，用于 API 中引用资产（如生图模型的 `reference_image.asset_id` 字段）。
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID。
- 转存范围策略：支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本。
- 存储容量计量：已用容量按自然月统计，回收站内资产在 30 天保留期内持续计费。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。
2. **OSS 绑定**：
   - 授权服务关联角色 `AliyunServiceRoleForBailianAssetForward`
   - 选择目标 OSS Bucket、地域、目录及路径模板
   - 设置转存范围与是否释放平台副本
3. **API 集成**：
   - 在生图/生视频请求体中，将原 `image_url` 或 `video_url` 字段替换为 `{"asset_id": "xxx"}`（具体字段名依模型接口定义而定）
   - 示例（生图参考图）：
     ```json
     "reference_image": { "asset_id": "asst_xxx" }
     ```
4. **权限配置**：通过 RAM 授予 `AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置权）策略。

## 限制和注意事项

- **存储限制**：每个账号默认 5 GB 免费额度，超量部分按 0.15 元/GB/月计费；已转存并释放平台副本的资产不计入用量。
- **回收站行为**：删除后进入回收站，保留 30 天（期间仍占平台存储），到期自动永久清除且不可恢复。
- **OSS 转存约束**：
  - 配置为全局生效，不随业务空间切换变化；
  - 若选择“释放平台存储”，该资产将**不再显示于资产中心列表**，仅存在于 OSS；
  - 转存失败任务自动重试，日志可在控制台查看。
- **安全责任**：转存至自有 OSS 的资产，其存储费用、ACL 控制、数据合规性均由用户自行承担，适用《阿里云存储服务协议》——此条款在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中有明确说明。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


