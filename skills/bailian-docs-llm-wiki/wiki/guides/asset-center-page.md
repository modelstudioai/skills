# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认保存在百炼平台存储中，支持按业务空间隔离查看，并可通过全局 OSS 转存配置实现长期归档与成本优化。详细功能与行为规范请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：支持模型列表动态更新，实际可用模型以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 控制台页面实时展示为准；音频资产暂不支持，该限制在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中已明确说明。

核心功能包括：  
- 多维度筛选（类型、模型、时间范围、提示词关键词）  
- 收藏/取消收藏、批量删除与回收站管理（保留期 30 天）  
- 资产详情查看（含完整 prompt、参数、模型名、生成时间）  
- 通过 `asset_id` 在生图/生视频 API 中直接引用资产（替代 `image_url` 或 `image_base64`）

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用；可在资产详情弹窗中获取 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 转存默认路径模板，其中 `{workspace}` 为当前业务空间标识 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 转存范围策略 | 支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。  
2. **OSS 绑定**：右上角点击**绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择目标 Bucket/地域/路径 → 设置转存范围与副本策略。  
   > **注意**：OSS 配置为全局生效，不随业务空间切换而变更；若选择“释放平台存储”，该资产将不再出现在资产中心列表中。  
3. **API 集成**：调用 `qwen-image-*` 或 `wan2.7-*` 等模型 API 时，在对应输入字段（如 `reference_image`、`first_frame`）中传入 `"asset_id": "xxx"`，无需再提供 URL 或 Base64。  
4. **权限控制**：通过 RAM 策略授权子账号：`AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置权限）。

## 限制和注意事项

- **存储生命周期**：  
  - 回收站内资产保留 30 天，期间仍占用平台存储容量并计费；  
  - 已转存至 OSS 并启用“释放平台存储”的资产，立即停止占用平台容量且不计费；  
  - 平台存储当前限时免费，商用后超出 5 GB 免费额度部分按 0.15 元/GB/月计费。  

- **功能边界**：  
  - 仅支持图片与视频资产，**不支持音频**（见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确说明）；  
  - OSS 转存失败任务自动重试，失败原因可在转存日志中查看；  
  - 切换业务空间仅影响资产列表可见性，不影响全局 OSS 配置。  

- **数据安全提醒**：  
  > **注意**：因账户欠费、服务终止或回收站超期导致的数据丢失，平台不可恢复。建议重要资产及时转存至自有 OSS Bucket 或本地环境备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


