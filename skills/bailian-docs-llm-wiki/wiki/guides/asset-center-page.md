# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认存储于百炼平台存储（限时免费），用户可通过配置 OSS 自动转存实现长期归档与成本优化。该功能面向已开通百炼服务的开发者，需在控制台显式开通后方可使用，详情请参阅 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持以下模型生成的图片与视频资产：  
- 图像类：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间戳的 2.0 Pro 版本、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`；  
- 视频类：`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型版本名，与百炼当前实际发布的模型命名规范不一致（如无 `2026` 年版本），建议以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 控制台实时展示的模型列表为准，避免硬编码过期标识。

资产中心**仅支持图片与视频**，明确不支持音频类资产（见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “支持的模型”章节说明）。

## 关键参数

- `asset_id`：每个资产的全局唯一标识符，用于 API 中直接引用（替代 `image_url` 或 `image_base64`）；  
- `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`：OSS 转存默认路径模板，其中 `{workspace}` 为当前业务空间 ID；  
- 平台存储配额：默认 5 GB 免费额度，超限按 0.15 元/GB/月计费；  
- 回收站保留期：30 天，期间资产仍占用平台存储容量。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)，点击“立即开通”；  
2. **OSS 转存配置**：右上角点击“绑定 OSS”，依次完成 SLR 授权、Bucket 与路径选择、转存范围设置（支持“仅转存 N 天前资产”及“释放平台存储”选项）；  
3. **资产筛选与管理**：支持按类型（图片/视频）、模型、生成时间、提示词关键词筛选；支持单个/批量收藏、删除（进入回收站）、查看详情；  
4. **API 集成**：调用生图/生视频 API 时，在对应输入字段（如 `reference_image`、`first_frame`）中传入 `{"asset_id": "xxx"}`，三选一（`asset_id` / `image_url` / `image_base64`）或二选一（`asset_id` / `video_url`）。

## 限制和注意事项

- OSS 转存配置为**全局生效**，不随业务空间切换而变更；但资产列表仅展示当前业务空间下的资产；  
- 若绑定 OSS 时勾选“释放平台存储”，该资产将**不再显示在资产中心**，也无法通过 `asset_id` 在 API 中引用（因平台侧副本已清除）；  
- 删除至回收站的资产在 30 天保留期内仍计入平台存储用量，且不可被 API 引用；  
- > **注意**：文档中“平台存储目前限时免费使用”与“商用计费启动后……”的表述存在时效模糊性。实际计费状态请以控制台顶部容量栏显示的计费标识及阿里云账单中心为准，避免依赖静态描述。最新策略详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。  
- 权限需通过 RAM 策略显式授予：普通用户需 `AliyunBailianAssetCenterReader`，OSS 配置权限需 `AliyunBailianAssetCenterAdmin`。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


