# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台页面，提供筛选、收藏、删除、OSS 转存及 API 引用等完整生命周期能力。所有资产默认保存于百炼平台存储（限时免费），用户可按需配置自动转存至自有 OSS Bucket。该功能面向已开通百炼服务的开发者，需在控制台手动开通后方可使用，详情请参阅 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的**图片与视频资产**（不支持音频）：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
支持的核心功能包括：按类型/模型/时间/提示词筛选、收藏与批量操作、回收站（保留 30 天）、资产详情查看，以及通过 `asset_id` 在 API 中直接引用资产。具体支持模型列表以控制台实时展示为准，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

> **注意**：原始文档中列出的模型版本（如 `2026-06-22`）明显为占位符或过时命名，实际生产环境应以控制台资产中心「模型」下拉菜单中动态加载的模型 ID 为准；建议开发者在集成前通过 `/v1/models` API 或控制台确认可用模型。

## 关键参数

- `asset_id`：每个资产唯一标识，可在资产详情弹窗中获取，用于 API 输入（替代 `image_url` 或 `image_base64`）。  
- OSS 转存路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识。  
- 平台存储配额：默认 5 GB 免费额度，超量部分按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入已用容量。  
- 转存范围策略：支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本（释放后资产不再显示于资产中心）。  
更多参数语义与约束，请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中「配置 OSS 转存」与「平台存储与计费」章节。

## 使用方式

1. **开通入口**：首次访问需前往 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 点击「立即开通」。  
2. **OSS 绑定**：右上角「绑定 OSS」→ 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择未开启版本控制的 Bucket 及目录 → 配置转存范围与释放策略。  
3. **资产操作**：在列表页悬停卡片执行收藏/删除；勾选后使用批量操作栏；点击卡片查看详情（含提示词、参数、`asset_id`）。  
4. **API 集成**：调用生图/生视频 API 时，在对应输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"`，无需再提供 URL 或 Base64。  

## 限制和注意事项

- **OSS 限制**：不支持已开启版本控制的 Bucket，否则转存失败；转存配置为全局生效，不随业务空间切换而变更。  
- **存储行为**：删除至回收站的资产仍占用平台存储并持续计费，30 天后自动永久清除；选择「释放平台存储」后，资产将从资产中心消失且无法通过界面恢复。  
- **权限隔离**：资产列表按业务空间隔离，但 OSS 配置、RAM 权限策略（如 `AliyunBailianAssetCenterAdmin`）作用于账号维度。  
- **数据责任**：平台不承诺长期备份，因欠费、服务终止或回收站过期导致的数据丢失不可恢复，强烈建议重要资产及时转存至自有 OSS 或本地环境。  
以上约束均依据 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确说明，开发者须在部署前完成权限策略配置与存储成本评估。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


