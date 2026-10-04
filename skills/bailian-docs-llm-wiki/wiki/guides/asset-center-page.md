# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心界面，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认保存于百炼平台存储（限时免费），用户可通过控制台开通并配置全局 OSS 同步策略。该功能面向开发者设计，强调资产可追溯性与跨服务复用能力，不支持音频类资产 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持的资产类型**：仅限图片与视频（`image` / `video`），**暂不支持音频资产** [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。  
- **支持的模型**：包括 `qwen-image-*` 系列（如 `qwen-image-3.0-pro`、`qwen-image-2.0-2026-03-03`）、`z-image-turbo`、`wan2.7-*` 全系列（`wan2.7-t2v`、`wan2.7-i2v`、`wan2.7-r2v`、`wan2.7-videoedit` 等）。具体列表以控制台实时展示为准，可能随版本迭代动态更新 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。  
- **核心功能**：  
  - 多维筛选（类型、模型、时间范围、提示词关键词）；  
  - 收藏/取消收藏、批量删除与回收站管理（保留期 30 天）；  
  - 资产详情查看（含完整 prompt、参数、模型名、生成时间）；  
  - 通过 `asset_id` 在生图/生视频 API 中直接引用已有资产，替代 `image_url` 或 `image_base64`。

## 关键参数

| 参数 | 说明 | 来源上下文 |
|------|------|------------|
| `asset_id` | 资产唯一标识符，用于 API 输入参数（如 `reference_image.asset_id`），在资产详情弹窗中获取 | [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 转存默认路径模板，其中 `{workspace}` 为当前业务空间标识 | [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `AliyunServiceRoleForBailianAssetForward` | OSS 绑定所需的服务关联角色（SLR），授权后无需提供 AccessKey | [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) |

> **注意**：OSS 转存配置为**全局设置**，不随业务空间切换而变化；但资产列表始终只显示当前业务空间下的资产。此行为已在文档中明确区分，无矛盾。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。  
2. **OSS 绑定（推荐）**：  
   - 点击右上角**绑定 OSS** → 授权 SLR → 选择目标 Bucket/地域/目录 → 配置路径模板与转存范围（全部 or N 天前）→ 选择是否**释放平台存储**（若勾选，资产将不再显示于资产中心）。  
3. **API 集成**：  
   - 生图模型（如 `qwen-image-3.0-pro`）：在 `input.reference_image` 等字段中传入 `{ "asset_id": "xxx" }`；  
   - 生视频模型（如 `wan2.7-t2v`）：在 `input.first_frame` 或 `input.reference_video` 中同理传入 `asset_id`；  
   - `asset_id` 与 `image_url` / `image_base64` 互斥，三选一（图片）或二选一（视频）。  

## 限制和注意事项

- **存储生命周期**：  
  - 回收站中资产保留 30 天，期间仍占用平台存储容量并计费；  
  - 已转存至 OSS 并勾选“释放平台存储”的资产，**立即停止占用平台容量且不计费**；  
  - 平台存储当前限时免费，商用后超出 5 GB 免费额度部分按 0.15 元/GB/月计费。  
- **权限隔离**：  
  - `AliyunBailianAssetCenterReader`：仅允许浏览、查看、删除；  
  - `AliyunBailianAssetCenterAdmin`：额外支持 OSS 转存配置（需授予该策略方可绑定/编辑 OSS）。  
- **关键约束**：  
  - 不支持跨业务空间共享资产列表；  
  - 删除至回收站后不可直接通过 API 访问 `asset_id`（ID 逻辑失效）；  
  - 建议重要资产及时转存至自有 OSS 或本地备份，因欠费、服务终止或回收站过期导致的数据丢失，平台无法恢复 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


