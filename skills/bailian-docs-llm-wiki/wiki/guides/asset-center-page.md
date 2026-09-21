# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认存储于百炼平台存储（限时免费），用户可通过配置 OSS 自动转存实现长期归档与成本优化。该功能面向已开通百炼服务的开发者，需在控制台显式开通后方可使用，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的**图片与视频资产**（不支持音频）：
- 图像模型：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间戳的 `qwen-image-2.0-pro` 变体、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`
- 视频模型：`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`

> **注意**：模型列表以控制台实时展示为准，部分带日期后缀的模型（如 `qwen-image-2.0-pro-2026-06-22`）可能为灰度或已下线版本，实际可用性请以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 页面筛选器中可选模型为准。

核心功能包括：按类型/模型/时间/提示词筛选、收藏与“只看收藏”视图、批量删除与回收站管理（保留 30 天）、OSS 全局转存配置、以及通过 `asset_id` 在 API 中直接引用资产——该能力显著简化生图/生视频请求体，避免重复上传，详情见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“在 API 中使用资产”章节。

## 关键参数

- `asset_id`：每个资产唯一标识符，用于 API 输入（替代 `image_url` 或 `image_base64`），可在资产详情弹窗中直接复制。
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID，不可修改。
- 转存范围策略：支持“全部资产”或“N 天前资产”，并可独立选择是否“释放平台存储”（即转存后立即从平台删除副本）。
- 平台存储配额：默认 5 GB 免费额度，超限按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入已用容量。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击“立即开通”；
2. **OSS 绑定**：右上角点击“绑定 OSS” → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/路径 → 设置转存范围与释放策略；
3. **资产操作**：
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词；
   - 收藏：悬停卡片点击星标，勾选“只看收藏”快速过滤；
   - 删除：勾选后点击删除按钮，资产进入回收站（非永久删除）；
   - 查看详情：点击卡片弹出完整元数据（含提示词、参数、生成时间）；
4. **API 集成**：调用 `qwen-image-*` 或 `wan2.7-*` 模型时，在对应输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"` 即可。

## 限制和注意事项

- **功能限制**：仅支持图片与视频资产；不支持音频；不支持跨业务空间资产聚合展示（切换 workspace 后列表即时刷新）；
- **存储行为**：
  - 已转存且启用“释放平台存储”的资产**不再显示于资产中心列表**，也不占用平台容量；
  - 回收站内资产保留 30 天，期间仍计费，期满自动永久清除且不可恢复；
- **权限隔离**：OSS 转存配置为全局设置，不随业务空间切换而变更；但资产列表、存储用量统计均按当前业务空间隔离；
- **安全与责任**：转存至自有 OSS Bucket 后，其存储费用、ACL 管理、数据合规性均由用户自行承担，平台不提供额外备份或恢复服务；
- > **注意**：文档中“平台存储目前限时免费使用”与“商用计费启动后……”表述存在时效模糊性，实际计费状态请以控制台顶部容量条右侧信息图标展开的说明为准，最新政策同步更新于 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


