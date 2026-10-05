# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 直接引用等能力。所有资产默认存储于百炼平台存储（限时免费），用户可通过配置 OSS 自动转存实现长期归档与成本优化。该功能面向所有已开通百炼服务的用户开放，详细说明见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：支持列表动态更新，实际可用模型请以控制台资产中心页面实时展示为准 —— 参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”章节。

功能覆盖全生命周期管理：资产列表浏览与多维筛选（类型/模型/时间/提示词）、收藏与“只看收藏”视图、单/批量删除、回收站（保留 30 天）、详情查看（含完整生成参数），以及关键的 OSS 转存与 API 资产 ID 引用能力。  
> **注意**：资产中心**仅支持图片与视频**，不支持音频类资产 —— 此限制明确记载于 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“支持的模型”说明中。

## 关键参数

- `asset_id`：每个资产唯一标识符，用于 API 输入引用（替代 `image_url` 或 `image_base64`）。可在资产详情弹窗右侧直接复制。
- OSS 路径模板：默认为 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识。
- 转存范围策略：支持“全部资产”或“N 天前的资产”，并可选是否释放平台存储副本（释放后资产不再显示于资产中心）。
- 平台存储配额：默认 5 GB 免费额度；超限部分按 0.15 元/GB/月计费（自然月统计）；回收站内资产在 30 天保留期内仍计入已用容量。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击“立即开通”。
2. **OSS 绑定**：右上角点击“绑定 OSS” → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/目录 → 配置路径模板与转存策略 → 完成绑定。
3. **资产操作**：
   - 筛选：顶部筛选栏支持按类型、模型、日期范围、提示词关键词过滤；
   - 收藏：悬停卡片点击星标；勾选“只看收藏”切换视图；
   - 删除：勾选后点击删除按钮 → 进入回收站（非永久删除）；
   - 查看详情：点击卡片 → 弹窗中获取 `asset_id` 及完整元数据。
4. **API 引用**：
   - 生图模型：在参考图、控制图等参数中传入 `"asset_id": "xxx"`（与 `image_url` / `image_base64` 三选一）；
   - 生视频模型：在首帧图、参考视频等参数中传入 `"asset_id": "xxx"`（与 URL / Base64 二选一）。

## 限制和注意事项

- OSS 转存配置为**全局设置**，不随业务空间切换而变化；但资产列表始终仅展示当前业务空间下的资产。
- 若绑定 OSS 时选择“释放平台存储”，资产将**同步至 OSS 后立即从资产中心移除**，且无法通过资产中心界面恢复（需从 OSS 访问）。
- 回收站中资产保留期为 **30 天**，到期自动永久清除，不可恢复；手动永久删除亦不可逆。
- 平台存储计费逻辑：已转存并释放副本的资产不计费；回收站内资产在保留期内持续计费；商用计费启动后，费用与百炼模型用量合并结算至阿里云账单中心。
- 权限控制依赖 RAM 策略：普通用户需 `AliyunBailianAssetCenterReader`，OSS 配置权限需 `AliyunBailianAssetCenterAdmin`。
- **重要提醒**：因账户欠费、服务终止或回收站过期导致的数据丢失，平台无法恢复。强烈建议通过 OSS 转存或本地下载对重要资产进行备份 —— 此风险提示原文见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “平台存储与计费”末段说明。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


