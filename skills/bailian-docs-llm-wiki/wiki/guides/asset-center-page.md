# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有用户均可开通使用，平台存储当前限时免费；资产默认保存于百炼平台存储，也可通过全局 OSS 转存配置自动同步至自有 Bucket。详细功能说明请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心支持管理以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：支持列表动态更新，以控制台资产中心页面实时展示为准；[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中明确说明“暂不支持音频资产”，该限制仍有效。

核心功能包括：  
- 多维度筛选（类型、模型、时间、提示词）  
- 收藏/取消收藏、批量删除、回收站恢复与永久清除  
- OSS 全局转存（含路径模板、转存范围、释放平台副本策略）  
- 通过 `asset_id` 在生图/生视频 API 中直接引用已有资产（替代 `image_url` 或 `image_base64`）

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用；在资产详情弹窗中获取 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 默认路径模板，其中 `{workspace}` 为当前业务空间标识 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 转存范围策略 | 支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。  
2. **OSS 绑定**：右上角点击**绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/目录 → 配置路径模板与转存策略 → 完成绑定。  
3. **API 引用**：调用 `qwen-image-*` 或 `wan2.7-*` 等模型 API 时，在对应输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"`，无需再提供 URL 或 Base64。  
4. **权限控制**：子账号需至少授予 `AliyunBailianAssetCenterReader` 策略方可查看与删除资产；OSS 配置操作需 `AliyunBailianAssetCenterAdmin`。

## 限制和注意事项

- **存储生命周期**：删除至回收站的资产仍占用平台存储容量，保留期为 30 天；到期后自动永久清除且不可恢复。  
- **OSS 转存作用域**：配置为全局生效，不随业务空间切换而变更；但资产列表始终仅显示当前业务空间下的资产。  
- **计费逻辑**：免费额度为 5 GB/账号；超出部分按 0.15 元/GB/月计费；已转存并选择“释放平台存储”的资产不计入用量。  
- **安全责任**：转存至自有 OSS Bucket 后，相关数据安全、访问控制及费用均由用户自行承担，适用《阿里云存储服务协议》。  
- > **注意**：[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确指出“建议及时将重要资产转存至自有 OSS Bucket 或本地环境备份”，因欠费、服务终止或回收站过期导致的数据丢失，平台无法恢复。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


