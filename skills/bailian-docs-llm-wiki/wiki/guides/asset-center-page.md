# asset center page

资产中心是百炼平台提供的生成资产（图片/视频）统一管理界面，用于持久化保存、筛选、收藏、删除及转存模型输出结果。它解耦了模型 API 返回的临时 URL 与长期资产存储，支持通过 `asset_id` 在后续 API 调用中直接复用已有资产。平台存储当前限时免费，但容量有限，建议高频或长期使用的资产及时配置 OSS 转存。

## 支持的模型/功能

资产中心当前**仅支持图片和视频类资产**，不支持音频（详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)）。  
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`；  
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-r2v/i2v/t2v`。  

所有上述模型在调用成功后，其输出将自动同步至当前业务空间的资产中心（前提是已开通且未禁用自动入库）。该能力依赖于模型服务端的资产注册机制，具体行为请以 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“查看资产列表”章节为准。

## 关键参数

- `asset_id`：每个资产唯一标识符，可在资产详情弹窗中获取，用于 API 复用（如生图时作为 `reference_image.asset_id`）；  
- `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`：OSS 转存默认路径模板，其中 `{workspace}` 为当前业务空间 ID；  
- 平台存储配额：默认 **5 GB 免费额度**，超限部分按 **0.15 元/GB/月** 计费（[原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确说明计费规则与回收站保留期内仍计费）；  
- 回收站保留期：**30 天**，到期自动永久清除，期间可恢复。

> **注意**：文档中提及“OSS 转存暂不支持已开启版本控制的 Bucket”，但最新版 RAM 权限策略 `AliyunServiceRoleForBailianAssetForward` 已适配部分版本控制场景。若绑定失败，请优先检查 Bucket 版本控制状态，并参考控制台实时错误提示，而非仅依赖该条说明。

## 使用方式

1. **开通**：首次访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**；  
2. **筛选与查看**：顶部统计栏显示资产总数、类型分布及平台存储用量；支持按类型、模型、日期范围、提示词关键词筛选；  
3. **OSS 转存配置**：右上角点击**绑定 OSS** → 授权 SLR 角色 → 选择地域/Bucket/路径 → 设置转存范围（全部 or N 天前）及是否释放平台副本；  
4. **API 复用**：在生图/生视频请求体中，将原 `image_url` 或 `video_url` 字段替换为 `"asset_id": "xxx"`（三选一或二选一，不可混用）；  
5. **权限控制**：通过 RAM 授予 `AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置）策略。

## 限制和注意事项

- 资产中心**按业务空间隔离**：切换空间后仅显示该空间内生成的资产，但 OSS 转存配置全局生效；  
- 删除操作分两级：勾选删除 → 进入回收站 → 30 天内可恢复，超期自动永久清除；  
- **已转存并释放平台副本的资产，不再占用配额，也不再显示在资产中心列表中**（即使 OSS 写入失败，系统会重试，但不会回退到平台存储）；  
- OSS 转存失败任务可在“转存日志”中排查原因（常见如 Bucket 权限不足、路径无写入权限），需人工干预修复后触发重试；  
- 所有资产元信息（提示词、参数、模型名、时间戳）仅在资产详情弹窗中展示，不提供批量导出接口。  

> **注意**：文档中“平台存储目前限时免费使用”为时效性描述，实际商用时间节点以阿里云官网公告为准；开发者应主动监控 `已用容量 / 免费额度` 比值，避免因超限导致新资产入库失败（该限制在 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“平台存储与计费”章节有明确预警）。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


