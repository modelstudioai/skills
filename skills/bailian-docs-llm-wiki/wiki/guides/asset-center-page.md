# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认保存于百炼平台存储（限时免费），用户可通过配置 OSS 自动转存实现长期归档与成本优化。该功能面向已开通百炼服务的开发者，需在控制台显式开通后方可使用，详情请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的**图片与视频资产**（不支持音频）：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
支持的核心功能包括：按类型/模型/时间/提示词筛选、收藏与“只看收藏”视图、批量删除与回收站管理、OSS 全局转存配置、以及通过 `asset_id` 在生图/生视频 API 中直接引用已有资产。具体支持模型列表以控制台实时展示为准，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

> **注意**：文档中列出的模型版本如 `qwen-image-2.0-pro-2026-06-22` 含未来日期，实际可用性需以控制台资产中心页面的下拉选项为准；部分旧版模型可能已下线，建议优先使用 `qwen-image-3.0` 系列。该信息与 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”章节一致，但需注意时效性。

## 关键参数

- `asset_id`：每个资产唯一标识符，用于 API 输入（替代 `image_url` 或 `image_base64`），可在资产详情弹窗中直接复制。  
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID，不可修改。  
- 转存范围策略：支持“全部资产”或“N 天前资产”，并可选是否勾选**释放平台存储**（勾选后资产不再显示于资产中心）。  
- 平台存储配额：默认 5 GB 免费额度，超限按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍占用配额。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。  
2. **OSS 绑定**：右上角点击**绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/路径 → 设置转存范围与释放策略。绑定后配置全局生效，不随业务空间切换而变更。  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词；  
   - 收藏：悬停卡片点击星标，勾选**只看收藏**快速过滤；  
   - 删除：勾选后点击删除按钮，进入回收站（保留 30 天）；  
   - 查看详情：点击卡片弹出完整元数据（含提示词、参数、生成时间）。  
4. **API 集成**：调用 `qwen-image-*` 或 `wan2.7-*` 模型 API 时，在对应输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"` 即可，无需额外上传。

## 限制和注意事项

- **功能限制**：仅支持图片与视频资产；音频资产暂不纳入管理；回收站资产不可直接用于 API 引用（需先恢复）。  
- **存储行为**：  
  - 已转存至 OSS 并勾选“释放平台存储”的资产，**立即从资产中心列表消失且不计入平台容量**；  
  - 回收站内资产在 30 天保留期内持续占用平台存储配额，到期自动永久清除；  
  - 平台存储费用按自然月结算，与百炼模型用量合并入阿里云账单。  
- **权限控制**：子账号需至少授予 `AliyunBailianAssetCenterReader` 策略才可查看与删除资产；OSS 配置权限需 `AliyunBailianAssetCenterAdmin`。  
- **数据责任**：平台不承诺长期保存，建议重要资产及时转存至自有 OSS 或本地备份。因欠费、服务终止或回收站过期导致的数据丢失，不可恢复——该原则在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“平台存储与计费”与“说明”章节中多次强调。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


