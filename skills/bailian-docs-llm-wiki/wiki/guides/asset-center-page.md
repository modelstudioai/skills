# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台页面，提供筛选、收藏、删除、OSS 转存及 API 引用等完整生命周期能力。所有资产默认保存于百炼平台存储（限时免费），用户可自主配置自动转存至自有 OSS Bucket 并选择是否释放平台副本。该功能面向已开通百炼服务的开发者，需在控制台显式开通后方可使用，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：支持模型列表动态更新，实际可用模型请以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 控制台实时展示为准；音频资产暂不支持，该限制未在文档其他位置明确说明，但与正文“暂不支持音频资产”一致。

核心功能包括：按类型/模型/时间/提示词筛选、收藏与“只看收藏”视图、批量删除与回收站管理（保留 30 天）、OSS 全局转存配置、以及通过 `asset_id` 在生图/生视频 API 中直接引用资产——该能力显著简化输入参数构造，避免重复上传，具体用法见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) “在 API 中使用资产”章节。

## 关键参数

- `asset_id`：每个资产唯一标识符，用于 API 输入（替代 `image_url` 或 `image_base64`），可在资产详情弹窗中直接复制。  
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识，不可自定义替换逻辑。  
- 转存范围策略：支持“全部资产”或“N 天前资产”，并强制要求选择是否“释放平台存储”（即删除平台副本）。若启用释放，该资产将不再出现在资产中心列表中。  
- 平台存储配额：默认 5 GB 免费额度，超限部分按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入已用容量。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击“立即开通”。  
2. **OSS 绑定**：右上角点击“绑定 OSS”，依次完成 SLR 角色授权（`AliyunServiceRoleForBailianAssetForward`）、Bucket 与路径选择、转存范围及释放策略配置。  
3. **资产操作**：  
   - 筛选：顶部统计栏下方支持按类型、模型、日期、提示词搜索；  
   - 收藏：悬停卡片点击星标，勾选“只看收藏”过滤；  
   - 删除：勾选后点击删除按钮，进入回收站（非永久）；  
   - 查看详情：点击卡片弹出完整元数据（含提示词、参数、生成时间）。  
4. **API 集成**：调用 `qwen-image-*` 或 `wan2.7-*` 系列模型时，在对应输入字段（如 `reference_image`、`first_frame`）中传入 `"asset_id": "xxx"` 即可。

## 限制和注意事项

- OSS 转存**不支持已开启版本控制的 Bucket**，否则任务失败且重试无效；必须使用未开启版本控制的标准 Bucket。  
- OSS 配置为**全局生效**，不随业务空间切换而变更；但资产列表仅显示当前业务空间下的生成结果。  
- 回收站资产保留期严格为 **30 天**，到期自动永久清除且不可恢复；手动永久删除亦不可逆。  
- 平台存储计费以自然月为周期，删除至回收站的资产在保留期内持续计费；仅当明确选择“释放平台存储”或 OSS 转存成功且勾选释放后，才停止占用配额。  
- 权限隔离依赖 RAM 策略：普通用户需 `AliyunBailianAssetCenterReader`，OSS 配置权限需 `AliyunBailianAssetCenterAdmin`。  
> **注意**：文档中“平台存储目前限时免费使用”与“正式商用后将按以下规则计费”存在隐含时效矛盾，当前无明确截止时间说明；建议开发者同步关注控制台公告及 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 最新修订记录。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


