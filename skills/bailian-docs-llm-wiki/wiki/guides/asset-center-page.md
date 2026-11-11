# asset center page

资产中心是百炼平台提供的生成资产（图片/视频）统一管理界面，支持筛选、收藏、删除、OSS 转存及 API 直接引用等核心能力。所有用户默认可开通使用，平台存储当前限时免费 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。资产数据按业务空间隔离，但 OSS 转存配置为全局生效，需注意权限与生命周期管理。

## 支持的模型/功能

- **支持资产类型**：仅图片和视频（暂不支持音频）  
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`z-image-turbo`、`wan2.7-image-pro` 等共 8 款（详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)）  
- **视频模型**：`wan3.0-video`、`happyhorse1.1-t2v`、`wan2.7-i2v` 等共 8 款（同上文档）  
- **核心功能**：按类型/模型/时间/提示词筛选、收藏、批量删除、回收站管理、OSS 自动转存、资产详情查看、API 中通过 `asset_id` 直接引用  

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期后缀的模型名，可能为占位符或已下线版本；实际可用模型请以控制台「模型体验」页或 `/v1/models` API 返回列表为准。建议开发者优先选用无日期后缀的稳定版模型（如 `qwen-image-3.0`），避免依赖临时命名。

## 关键参数

- `asset_id`：每个资产唯一标识，用于 API 输入（替代 `image_url` 或 `image_base64`）  
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID  
- 转存范围策略：支持「全部资产」或「N 天前的资产」，并可选是否释放平台存储副本  
- 回收站保留期：固定 30 天，期间仍占用平台存储配额  

## 使用方式

1. **开通**：首次访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击「立即开通」  
2. **绑定 OSS**（可选）：右上角「绑定 OSS」→ 授权 SLR 角色 → 选择未开启版本控制的 Bucket → 配置路径与转存策略 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)  
3. **管理资产**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词搜索  
   - 收藏：悬停卡片 → 点击星标；勾选「只看收藏」快速过滤  
   - 删除：勾选后点击「删除」→ 进入回收站（非永久）→ 可恢复或手动永久删除  
4. **API 引用**：在生图/生视频请求中，将 `asset_id` 填入对应输入字段（如 `control_image.asset_id`），三选一（`asset_id` / `image_url` / `image_base64`）  

## 限制和注意事项

- **OSS 限制**：不支持已开启版本控制的 Bucket，否则转存失败  
- **存储计费**：  
  - 免费额度 5 GB，超量部分 0.15 元/GB/月  
  - 回收站内资产在 30 天保留期内**持续计费**  
  - 已转存且勾选「释放平台存储」的资产**立即停止计费**  
- **权限隔离**：资产列表按业务空间展示，但 OSS 配置全局生效；切换空间不影响已绑定的 Bucket  
- **数据安全**：转存至自有 OSS 后，存储、ACL、费用及合规责任归属用户，遵循《阿里云存储服务协议》 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)  
- **重要提醒**：平台不承诺欠费、服务终止或回收站过期导致的数据恢复，请务必对关键资产及时转存或本地备份

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


