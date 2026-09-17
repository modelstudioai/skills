# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于平台存储（限时免费），支持按业务空间隔离展示，并可通过全局 OSS 转存配置实现长期归档与成本优化。详细功能说明请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：支持列表动态更新，实际可用模型以控制台资产中心页面实时展示为准 —— 详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”章节。

功能覆盖全生命周期管理：  
- 筛选（类型/模型/时间/提示词）  
- 收藏与“只看收藏”视图  
- 批量删除 + 回收站（保留 30 天，可恢复）  
- OSS 自动转存（含路径模板 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`）  
- 资产详情查看（含完整生成参数）  
- API 层直接引用（通过 `asset_id` 替代 `image_url` 或 `image_base64`）  

**不支持音频资产**，该限制明确记录在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“支持的模型”说明中。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用 | `asst_abc123xyz` |
| `{workspace}` | 业务空间标识，由百炼自动注入至 OSS 路径模板 | `my-proj-v1` |
| `{yyyy}/{mm}/{model}/{id}.{ext}` | 默认 OSS 路径模板，不可自定义结构 | `my-proj-v1/2024/06/qwen-image-3.0/asst_abc123.png` |
| 平台存储配额 | 每账号默认 5 GB 免费额度，超限按 0.15 元/GB/月计费 | `0.00 / 5 GB`（显示于页面顶部） |

> **注意**：OSS 转存配置为**全局设置**，不随业务空间切换而变化；但资产列表严格按当前业务空间过滤 —— 此行为差异已在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “常见问题”中明确说明。

## 使用方式

1. **开通入口**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。  
2. **OSS 绑定**（推荐）：右上角 → **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择 Bucket/地域/路径 → 设置转存范围（全部 or N 天前）及是否释放平台存储副本。  
3. **API 引用**：调用生图/生视频模型时，在对应输入字段（如 `reference_image`、`first_frame`）中传入 `"asset_id": "asst_xxx"`，无需再提供 URL 或 Base64。  
4. **权限控制**：通过 RAM 策略授权子账号：  
   - `AliyunBailianAssetCenterReader`：仅浏览与删除  
   - `AliyunBailianAssetCenterAdmin`：含 Reader 权限 + OSS 配置权限  

## 限制和注意事项

- **存储生命周期**：  
  - 删除至回收站的资产在 30 天内仍占用平台存储并计费；  
  - 释放平台存储后（OSS 转存时勾选），资产立即从资产中心消失且不再计费；  
  - 回收站到期自动清理，**不可恢复**。  

- **OSS 责任边界**：转存至自有 OSS Bucket 后，存储费用、ACL 控制、数据安全责任均归属用户，适用《阿里云存储服务协议》。  

- **关键风险提示**：  
  > **注意**：因账户欠费、服务终止或回收站超期导致的数据丢失，平台无法恢复 —— 此要求在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “平台存储与计费”末尾已强制强调。  
  - 建议重要资产同步备份至本地或自有 OSS；  
  - 不建议依赖平台存储作为唯一持久化方案；  
  - 切换业务空间不影响 OSS 配置，但资产列表完全隔离。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


