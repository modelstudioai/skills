# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认保存在百炼平台存储中，支持按业务空间隔离查看；OSS 转存为可选配置，用于长期归档与成本优化。详细功能与行为规范请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：该列表以控制台实时展示为准，可能随版本迭代动态更新；具体支持范围请以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”章节为准。

功能覆盖：  
- 资产筛选（类型/模型/时间/提示词）  
- 收藏与“只看收藏”视图  
- 批量删除 + 回收站（保留 30 天，可恢复或永久删除）  
- OSS 自动转存（含路径模板、转存范围、释放平台副本选项）  
- 资产详情页展示完整生成上下文（提示词、参数、模型、时间）  
- API 层直接通过 `asset_id` 引用资产（替代 `image_url` / `image_base64`）

> **注意**：资产中心**不支持音频资产**，且仅管理由百炼模型直接生成的资产（非用户上传文件），此限制明确记载于 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 关键参数

| 参数 | 说明 | 取值示例 |
|------|------|----------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用 | `asst_abc123xyz` |
| `{workspace}` | 路径模板变量，取值为当前业务空间 ID | `ws-prod-2024` |
| `{yyyy}/{mm}/{model}/{id}.{ext}` | 默认 OSS 路径模板 | `ws-prod-2024/2025/04/qwen-image-3.0/asst_xxx.png` |
| 转存范围 | 全部资产 或 N 天前资产（N ≥ 1） | `7`（表示 7 天前生成的资产） |
| 释放平台存储 | 布尔开关，启用后资产同步至 OSS 后即从平台存储移除 | `true` / `false` |

## 使用方式

1. **开通**：首次访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**（全量开放，无需申请）。  
2. **OSS 绑定**（可选但推荐）：右上角 → **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择 Bucket/地域/路径模板 → 设置转存范围与是否释放平台副本。  
3. **筛选与操作**：使用顶部筛选栏按类型、模型、日期、提示词快速定位；悬停卡片操作收藏/删除；勾选后批量处理。  
4. **API 集成**：在调用生图（如 `qwen-image-3.0`）或生视频（如 `wan2.7-t2v`）API 时，在对应输入字段（如 `control_image`、`reference_video`）中传入 `"asset_id": "asst_xxx"`，无需再提供 URL 或 Base64。  

## 限制和注意事项

- **存储生命周期**：回收站内资产保留 30 天，期间仍占用平台存储配额并计费；超期自动清除且不可恢复。  
- **OSS 转存全局性**：绑定配置对账号下所有业务空间生效，切换空间不影响已配置的 Bucket 和规则。  
- **权限隔离**：子账号需显式授予 `AliyunBailianAssetCenterReader`（基础查看/删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置）策略，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 权限说明章节。  
- **计费逻辑**：免费额度为 5 GB/账号；超出部分按 0.15 元/GB/月计费；已释放平台副本的 OSS 转存资产不计入用量。  
- **数据责任**：平台不承担因欠费、服务终止或回收站过期导致的数据丢失风险，建议重要资产及时转存至自有 OSS 或本地备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


