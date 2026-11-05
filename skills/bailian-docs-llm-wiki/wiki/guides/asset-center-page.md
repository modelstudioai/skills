# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，支持筛选、收藏、删除、OSS 转存及 API 直接引用等关键能力。所有用户均可开通使用，平台存储当前限时免费；资产默认保存于百炼平台存储，也可配置自动同步至自有 OSS Bucket。详细功能与行为规范请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **图片生成模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`  
- **视频生成模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`  

> **注意**：资产中心**仅支持图片与视频资产**，不支持音频类资产；该限制在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中明确说明，且无其他文档提出例外。

核心功能包括：按类型/模型/时间/提示词筛选、收藏与“只看收藏”视图、批量删除与回收站管理（保留期 30 天）、OSS 自动转存（含路径模板与释放平台副本选项），以及通过 `asset_id` 在 API 中直接复用资产。

## 关键参数

- `asset_id`：每个资产唯一标识，用于 API 输入（替代 `image_url` 或 `image_base64`）；可在资产详情弹窗中直接复制。  
- OSS 路径模板：默认为 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识。  
- 转存范围策略：支持“全部资产”或“N 天前的资产”，并可选是否勾选**释放平台存储**（勾选后资产不再显示于资产中心）。  
- 平台存储配额：默认 5 GB 免费额度，超量部分按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入已用容量。

## 使用方式

1. **开通与访问**：首次使用需前往 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 点击**立即开通**；入口位于控制台「模型」→「资产中心」。  
2. **OSS 绑定**：右上角点击**绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择未开启版本控制的 Bucket 与目录 → 配置转存范围与释放策略。该配置为全局生效，不随业务空间切换而变更（详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)）。  
3. **API 集成**：调用生图/生视频模型时，在对应输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"`，三选一（`asset_id` / `image_url` / `image_base64`）或二选一（`asset_id` / `video_url`）即可。  
4. **管理操作**：悬停卡片操作收藏/删除；勾选后使用批量删除；点击卡片查看完整元数据（含提示词、参数、生成时间等）。

## 限制和注意事项

- OSS 转存**不支持已开启版本控制的 Bucket**，否则任务失败且重试无效。  
- 删除操作进入回收站，**非立即永久删除**；回收站资产保留 30 天，期间仍占用平台存储并计费，到期后自动清除且不可恢复。  
- 平台存储容量统计实时反映当前业务空间用量（含回收站），但 OSS 转存配置与日志为全局视角。  
- 权限受 RAM 策略控制：普通用户需 `AliyunBailianAssetCenterReader`，配置 OSS 需 `AliyunBailianAssetCenterAdmin`。  
- > **注意**：[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确指出“切换业务空间后，资产会变化”，即资产列表严格按当前 workspace 过滤，但 OSS 配置不变——此逻辑与其他百炼资源（如模型部署）的 workspace 隔离原则一致，无矛盾。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


