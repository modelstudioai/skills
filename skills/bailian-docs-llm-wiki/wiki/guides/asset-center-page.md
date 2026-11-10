# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，支持筛选、收藏、删除、OSS 转存及 API 直接引用等关键操作。所有资产默认保存于百炼平台存储（限时免费），用户可通过配置 OSS 自动转存实现长期归档与成本优化。该功能面向已开通百炼服务的开发者，需在业务空间内手动启用 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **图片生成模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`  
- **视频生成模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`  

> **注意**：当前仅支持图片与视频资产，**不支持音频资产**；且所有模型列表以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中最新维护为准，部分旧版模型（如 `qwen-image-2.0-2026-03-03`）可能已进入维护期，建议优先使用无时间后缀的稳定版本。

资产中心提供以下核心功能：  
- 多维筛选（类型、模型、时间范围、提示词关键词）  
- 收藏/取消收藏、批量删除、回收站恢复与永久清除  
- OSS 全局转存配置（含路径模板 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`）  
- 资产详情页展示完整生成参数（提示词、模型名、时间戳等）  
- 在 API 中通过 `asset_id` 直接复用已有资产，替代 `image_url` 或 `image_base64` [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入参数（如生图模型的 `reference_image.asset_id`） | 仅限同账号、同地域下有效；不可跨业务空间复用 |
| OSS 路径模板 | 默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，支持自定义字段（如 `{prompt_hash}`） | 不支持版本控制 Bucket；路径中 `{workspace}` 为当前业务空间 ID |
| 转存范围 | 支持“全部资产”或“N 天前资产” | 若选择“释放平台存储”，资产将不再出现在资产中心列表中 |
| 平台存储配额 | 默认 5 GB 免费额度；超量按 0.15 元/GB/月计费 | 回收站内资产在 30 天保留期内仍计入配额 |

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)，点击**立即开通**；入口地址：`https://bailian.console.aliyun.com/cn-beijing/model/asset-center`  
2. **OSS 绑定**：右上角 → **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择未开启版本控制的 Bucket + 目录 → 配置转存策略  
3. **API 引用**：调用模型 API 时，在对应输入字段（如 `control_image`）中传入 `"asset_id": "as-xxx"`，无需再提供 URL 或 Base64  
4. **权限控制**：通过 RAM 授予 `AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置权）

## 限制和注意事项

- **OSS 限制**：不支持已开启版本控制的 Bucket；转存失败任务自动重试，失败原因可在转存日志中查看  
- **存储生命周期**：  
  - 删除至回收站的资产保留 30 天，期间仍占用平台存储配额  
  - 释放平台存储后，资产**不可在资产中心查看或恢复**，仅存在于目标 OSS  
- **全局性配置**：OSS 绑定状态、路径模板、转存范围均为账号级设置，**不随业务空间切换而变更**  
- **数据安全责任**：转存至自有 OSS 后，存储费用、ACL 策略、加密配置及合规责任均由用户自行承担，详见《阿里云存储服务协议》  
- **重要提醒**：因账户欠费、服务终止或回收站过期导致的数据丢失，平台无法恢复；建议对关键资产及时转存至 OSS 或本地备份

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


