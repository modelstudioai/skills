# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有用户均可开通使用，平台存储当前限时免费；资产默认保存于百炼平台存储，也可通过全局 OSS 转存配置自动同步至用户自有 Bucket。详细功能与行为规范请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心支持管理以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：该列表以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”章节为准；文档中明确说明“暂不支持音频资产”，且未提及文本或 3D 模型资产，开发者不应假设其受支持。

核心功能包括：  
- 多维度筛选（类型、模型、时间、提示词）  
- 收藏/取消收藏、批量删除、回收站恢复与永久清除  
- OSS 全局转存配置（含路径模板、转存范围、释放平台副本选项）  
- 资产详情查看（含完整生成参数与 `asset_id`）  
- 在生图/生视频 API 中直接通过 `asset_id` 引用已有资产（替代 `image_url` 或 `image_base64`）

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用；在资产详情弹窗中可见 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “在 API 中使用资产”章节 |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 默认路径模板，其中 `{workspace}` 为当前业务空间标识 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “配置 OSS 转存”章节 |
| 平台存储配额 | 每账号默认 5 GB 免费额度；超量部分按 0.15 元/GB/月计费 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “平台存储与计费”章节 |

> **注意**：OSS 转存配置为**全局设置**，不随业务空间切换而变化；但资产列表仅展示当前业务空间下的资产——这一关键隔离逻辑在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “常见问题”中有明确定义。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**。  
2. **OSS 绑定（可选但推荐）**：  
   - 点击右上角**绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward`  
   - 选择地域、Bucket、目录，确认路径模板  
   - 设置转存范围（全部 / N 天前）及是否**释放平台存储**（勾选后资产不再显示于资产中心）  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词搜索  
   - 收藏：悬停卡片 → 点击星标；勾选“只看收藏”过滤  
   - 删除：勾选后点击删除 → 进入回收站（保留 30 天）→ 可恢复或永久删除  
4. **API 集成**：  
   - 在生图模型请求中，将参考图等字段设为 `{ "asset_id": "xxx" }`（与 `image_url` / `image_base64` 三选一）  
   - 在生视频模型请求中，将首帧图、参考视频等字段设为 `{ "asset_id": "xxx" }`（与 URL / Base64 二选一）

## 限制和注意事项

- **资产类型限制**：仅支持图片与视频，**不支持音频、文本、3D 模型等其他格式**（见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “支持的模型”说明）。  
- **存储生命周期**：  
  - 回收站内资产保留 30 天，期间仍占用平台存储并计费；  
  - 释放平台存储后（OSS 转存时勾选），资产立即从资产中心消失且不再计费；  
  - 平台存储免费期结束后，超量部分按自然月结算，费用并入阿里云账单。  
- **权限控制**：需显式授予 RAM 权限策略：  
  - `AliyunBailianAssetCenterReader`：仅浏览与删除（不含 OSS 配置）  
  - `AliyunBailianAssetCenterAdmin`：含 Reader 权限 + OSS 转存配置权限  
- **数据安全提醒**：平台不承诺因账户欠费、服务终止或回收站过期导致的数据恢复；重要资产须及时转存至自有 OSS 或本地备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


