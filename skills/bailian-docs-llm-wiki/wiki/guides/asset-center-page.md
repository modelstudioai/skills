# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认保存在百炼平台存储中，支持按业务空间隔离展示；OSS 转存为可选配置，用于长期归档与成本优化。详细功能与行为以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 文档为准。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的**图片与视频资产**（不支持音频）：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：模型列表可能随产品迭代动态更新，实际可用模型请以控制台资产中心页面实时展示为准，而非硬编码列表——参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”章节。

核心功能包括：  
- 多维度筛选（类型、模型、时间范围、提示词关键词）；  
- 收藏/取消收藏、批量删除、回收站恢复与永久清除；  
- OSS 全局转存配置（含路径模板、转存范围、是否释放平台副本）；  
- 通过 `asset_id` 在生图/生视频 API 中直接引用已有资产，替代 `image_url` 或 `image_base64`。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，可在资产详情弹窗中获取，用于 API 输入参数（如 `reference_image.asset_id`） | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 默认路径模板，其中 `{workspace}` 为当前业务空间标识 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 转存范围策略 | 支持“全部资产”或“N 天前资产”，并可勾选“释放平台存储”（勾选后资产不再显示于资产中心） | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通与访问**：首次使用需前往 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 点击**立即开通**；  
2. **OSS 绑定**：右上角点击**绑定 OSS** → 授权 SLR 角色 → 选择 Bucket/地域/路径 → 设置转存范围与副本策略；  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词搜索；  
   - 收藏：悬停卡片 → 点击星标；勾选“只看收藏”过滤；  
   - 删除：勾选后点击删除 → 进入回收站（保留 30 天）→ 可恢复或永久删除；  
4. **API 集成**：调用 `qwen-image-*` 或 `wan2.7-*` 模型时，在对应输入字段（如 `control_image`）中传入 `"asset_id": "xxx"`，无需再提供 URL/Base64。

## 限制和注意事项

- **存储生命周期**：回收站内资产仍占用平台存储容量，30 天后自动永久清除且不可恢复；  
- **OSS 转存全局性**：配置一次即生效于所有业务空间，切换空间不影响已绑定的 Bucket 和路径规则；  
- **权限隔离**：资产列表仅展示当前业务空间下的资产，但 `AliyunBailianAssetCenterReader` 等 RAM 策略作用域为账号级；  
- **计费逻辑**：免费额度为 5 GB/账号；超出部分按 0.15 元/GB/月计费；已转存并释放平台副本的资产不计入用量；  
- > **注意**：若在 OSS 转存配置中勾选“释放平台存储”，该资产将**立即从资产中心列表消失**，且无法通过界面恢复——此行为与回收站机制完全独立，务必确认后再操作（详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “配置 OSS 转存”说明）。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


