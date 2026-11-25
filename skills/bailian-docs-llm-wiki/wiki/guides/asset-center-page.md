# asset center page

资产中心是百炼平台提供的统一资产管理入口，用于持久化保存和操作模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持筛选、收藏、批量删除、OSS 转存及 API 直接引用等核心能力。所有功能均基于业务空间（workspace）隔离，且 OSS 转存配置为全局生效。

## 支持的模型/功能

- **图片生成模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`  
- **视频生成模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v`、`happyhorse1.1-i2v`、`happyhorse1.1-r2v`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`  

> **注意**：当前仅支持图片与视频资产，**不支持音频资产**，该限制在 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 中明确说明，且无其他文档提出例外。

资产中心提供以下关键功能：  
- 按类型、模型、生成时间、提示词关键词筛选；  
- 单/批量收藏、删除（含回收站机制，保留期 30 天）；  
- 查看资产详情（含完整 prompt、参数、模型名、生成时间）；  
- 通过 `asset_id` 在生图/生视频 API 中直接引用已有资产（替代 `image_url` 或 `image_base64`），详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 关键参数

- `asset_id`：每个资产唯一标识，可在资产详情弹窗中获取，是 API 中复用资产的核心参数；  
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID；  
- 平台存储配额：默认 5 GB 免费额度，超限部分按 0.15 元/GB/月计费；  
- 回收站保留期：固定 30 天，期间仍占用平台存储容量，到期自动永久清除；  
- OSS 转存范围：支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本（释放后资产不再显示于资产中心）。

## 使用方式

1. **开通**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**；  
2. **绑定 OSS**（可选但推荐）：点击右上角**绑定 OSS** → 授权 SLR（`AliyunServiceRoleForBailianAssetForward`）→ 选择未开启版本控制的 Bucket 与路径 → 设置转存范围与释放策略；  
3. **管理资产**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词搜索；  
   - 收藏：悬停卡片 → 点击星标；勾选**只看收藏**快速过滤；  
   - 删除：勾选后点击删除 → 进入回收站 → 可恢复或永久删除；  
4. **API 集成**：在调用 `qwen-image-*` 或 `wan3.0-video*` 等模型时，在对应输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"`，无需再提供 URL 或 Base64，具体字段兼容性请参考 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 限制和注意事项

- OSS 转存**不支持已开启版本控制的 Bucket**，否则转存失败；  
- OSS 转存配置为**全局设置**，不随业务空间切换而变更；  
- 若绑定 OSS 时选择“释放平台存储”，则资产**不会出现在资产中心列表中**，仅存在于目标 OSS；  
- 回收站中的资产在 30 天保留期内仍计入平台存储用量，需手动恢复或等待自动清理；  
- > **注意**：[原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确指出“平台存储目前限时免费使用”，但未说明截止时间；后续商用计费规则（如 0.15 元/GB/月）已写入文档，开发者应提前规划长期资产归档策略，避免账单突增。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


