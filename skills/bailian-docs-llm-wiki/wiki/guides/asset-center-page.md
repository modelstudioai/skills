# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于百炼平台存储（限时免费），支持按业务空间隔离查看，并可通过全局 OSS 配置实现长期归档与成本优化。详细功能与行为边界请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；对应模型包括 `qwen-image-*` 系列（如 `qwen-image-3.0-pro`）、`wan2.7-*` 全系列（如 `wan2.7-t2v`、`wan2.7-i2v`、`wan2.7-videoedit`）等，完整列表以控制台实时展示为准。  
- **核心功能**：  
  - 多维筛选（类型、模型、时间、提示词关键词）  
  - 收藏/取消收藏、批量删除、回收站恢复与永久清除  
  - OSS 自动转存（含路径模板 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`）  
  - 资产详情查看（含完整 [prompt](prompt.md)、参数、生成时间）  
  - 在 API 中直接通过 `asset_id` 引用已有资产，替代 `image_url` 或 `image_base64` —— 此能力已在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确说明，适用于生图与生视频模型输入参数。

> **注意**：文档中提及的模型版本如 `qwen-image-2.0-2026-03-03` 含未来日期，实际部署版本应以控制台资产中心「模型筛选下拉框」中可选值为准；该命名可能为内部测试标识，生产环境请以运行时可用模型为准。

## 关键参数

- `asset_id`：每个资产唯一标识，用于 API 输入引用，可在资产详情弹窗中直接复制。  
- OSS 路径模板变量：`{workspace}`（当前业务空间 ID）、`{yyyy}/{mm}`（生成时间）、`{model}`（模型名）、`{id}`（asset_id）、`{ext}`（扩展名）。  
- 平台存储配额：默认 5 GB 免费额度，超量部分按 0.15 元/GB/月计费；已释放平台副本的 OSS 转存资产不计入用量。  
- 回收站保留期：30 天，期间仍占用平台存储并计费；到期自动永久清除，不可恢复。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)，点击「立即开通」启用服务。  
2. **OSS 绑定**：右上角「绑定 OSS」→ 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择 Bucket/地域/路径 → 设置转存范围与是否释放平台副本。  
3. **API 集成**：调用生图/生视频 API 时，在图像或视频输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"`，无需再提供 URL 或 Base64。  
4. **权限配置**：子账号需授予 `AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置）策略，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 权限说明章节。

## 限制和注意事项

- OSS 转存为**全局配置**，不随业务空间切换而变更；但资产列表始终仅显示当前业务空间下的数据。  
- 删除操作进入回收站，非立即释放存储；回收站内资产在 30 天保留期内仍计费，且无法通过 API 访问。  
- 若绑定 OSS 时勾选「释放平台存储」，该资产将**不再出现在资产中心列表中**，也无法被筛选或收藏，仅存在于目标 OSS Bucket。  
- 平台存储费用与百炼模型用量合并结算至阿里云账单中心；OSS 存储费用、访问费用及安全策略由用户自行承担，适用《阿里云存储服务协议》。  
- > **注意**：文档中“平台存储目前限时免费使用”与“商用计费启动后……”存在状态模糊性。实际计费策略以控制台资产中心顶部容量条旁的信息图标展开内容为准，建议开发者定期检查实时配额与计费状态。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


