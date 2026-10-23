# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台页面，提供筛选、收藏、删除、OSS 转存及 API 引用等完整生命周期能力。所有资产默认保存于百炼平台存储（限时免费），用户可按需配置自动转存至自有 OSS Bucket。该功能面向已开通百炼服务的开发者，需在控制台显式开通后方可使用，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的**图片与视频资产**（不支持音频）：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
支持的核心功能包括：资产列表筛选（按类型/模型/时间/提示词）、收藏与取消收藏、批量删除与回收站管理、OSS 自动转存、以及通过 `asset_id` 在 API 中直接引用资产。具体支持模型列表以控制台实时展示为准，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

> **注意**：原始文档中列出的模型版本（如 `2026-06-22`）明显为占位符或过时命名（当前日期远早于 2026 年），实际可用模型请以控制台资产中心「模型」下拉筛选器中动态加载的选项为准；该问题已在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“支持的模型”章节末尾明确提示“请以控制台……实际展示为准”。

## 关键参数

- `asset_id`：每个资产唯一标识符，可在资产详情弹窗中获取，用于 API 输入参数（替代 `image_url` 或 `image_base64`）。  
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID。  
- 转存范围策略：支持「全部资产」或「N 天前的资产」，并可选是否勾选「释放平台存储」（即转存后立即清除平台副本）。  
- 平台存储配额：默认 5 GB 免费额度，超限部分按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入已用容量。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击「立即开通」；开通后入口固定，无需重复操作。  
2. **OSS 绑定**：点击右上角「绑定 OSS」→ 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择未开启版本控制的 Bucket 及目录 → 配置路径模板与转存策略 → 完成绑定。绑定后可在「OSS 转存配置」中查看日志、编辑或解绑。  
3. **API 引用**：调用生图/生视频模型时，在对应输入字段（如 `reference_image`、`first_frame`）中传入 `"asset_id": "xxx"`，三选一（`asset_id` / `image_url` / `image_base64`）即可，无需额外鉴权。详细字段定义参见各模型 API 文档，其集成逻辑基于 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 所述机制。

## 限制和注意事项

- **存储限制**：平台存储仅限图片与视频，不支持音频；OSS 转存不兼容开启版本控制的 Bucket，否则任务失败。  
- **权限隔离**：资产列表按业务空间隔离，但 OSS 转存配置为全局生效，切换业务空间不影响已绑定配置。  
- **数据持久性**：删除至回收站的资产保留 30 天，期间仍占用平台存储并计费；释放平台存储后，资产将不再显示于资产中心，且无法通过百炼平台恢复。  
- **安全责任**：转存至自有 OSS Bucket 的资产，其存储成本、ACL 策略、加密与合规责任均由用户自行承担，适用《阿里云存储服务协议》。  
- **关键提醒**：务必及时备份重要资产至本地或自有 OSS；因欠费、服务终止或回收站过期导致的数据丢失，百炼平台不提供恢复能力。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


