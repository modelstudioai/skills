# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台页面，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于百炼平台存储（限时免费），用户可通过控制台或 API 全生命周期管理资产。详细设计与行为规范请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的**图片与视频资产**（不支持音频）：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：模型列表动态更新，实际可用模型以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 控制台实时展示为准，文档中列举的带时间后缀的模型（如 `2026-06-22`）可能已下线或被新版替代，请优先以控制台为准。

核心功能包括：按类型/模型/时间/提示词筛选、收藏与“只看收藏”视图、批量删除与回收站管理（保留 30 天）、OSS 自动转存（含路径模板与释放策略）、以及通过 `asset_id` 在 API 中直接引用资产。

## 关键参数

- `asset_id`：全局唯一资产标识符，用于 API 输入（替代 `image_url` 或 `image_base64`），在资产详情弹窗中可见；  
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID；  
- 转存范围策略：支持「全部资产」或「N 天前资产」，并可选是否勾选「释放平台存储」；  
- 平台存储配额：默认 5 GB 免费额度，超限部分按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍占用配额；  
- 权限策略：`AliyunBailianAssetCenterReader`（读+删）与 `AliyunBailianAssetCenterAdmin`（含 OSS 配置权），需通过 RAM 授权。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击「立即开通」；  
2. **OSS 绑定**：右上角「绑定 OSS」→ 授权 SLR（`AliyunServiceRoleForBailianAssetForward`）→ 选择未开启版本控制的 Bucket 及目录 → 设置路径模板与转存策略；  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词；  
   - 收藏：悬停卡片点击星标，勾选「只看收藏」过滤；  
   - 删除：勾选后点击「删除」，进入回收站（非永久）；  
   - 查看详情：点击卡片弹出完整元数据（含提示词、参数、生成时间）；  
4. **API 集成**：调用生图/生视频 API 时，在对应输入字段（如 `reference_image`、`first_frame`）传入 `"asset_id": "xxx"`，三选一（`asset_id` / `image_url` / `image_base64`）；该能力详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的「在 API 中使用资产」章节。

## 限制和注意事项

- **OSS 限制**：不支持已开启版本控制的 Bucket，否则转存失败；  
- **存储逻辑**：  
  - 选择「释放平台存储」后，资产**不再显示于资产中心列表**，仅存在于 OSS；  
  - 回收站中资产仍计入平台存储用量，30 天后自动永久清除且不可恢复；  
- **权限隔离**：资产列表按业务空间隔离，但 OSS 转存配置为**全局生效**，切换空间不影响已绑定配置；  
- **数据责任**：平台不承担因欠费、服务终止或回收站过期导致的数据丢失风险，[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确建议用户及时转存至自有 OSS 或本地备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


