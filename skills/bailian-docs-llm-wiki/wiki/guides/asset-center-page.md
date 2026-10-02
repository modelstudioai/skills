# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认保存在百炼平台存储中，支持按业务空间隔离，并可通过配置实现自动转存至自有 OSS Bucket。详细功能说明请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：模型列表以控制台实时展示为准，[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中所列版本号（如 `2026-06-22`）可能随服务迭代下线或重命名，建议通过控制台「模型筛选」下拉菜单确认可用项。  
仅支持图片与视频两类资产，**不支持音频资产**，该限制在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中已明确声明。

## 关键参数

- `asset_id`：每个资产唯一标识符，用于 API 中直接引用（替代 `image_url` 或 `image_base64`）。可在资产详情弹窗右侧面板获取。  
- `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`：OSS 默认路径模板，其中 `{workspace}` 为当前业务空间 ID，不可修改；其余占位符由系统自动替换。  
- 平台存储容量配额：默认 5 GB 免费额度，超限部分按 0.15 元/GB/月计费（自然月统计），回收站内资产在 30 天保留期内持续占用配额。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击「立即开通」；开通后入口固定，无需重复操作。  
2. **OSS 转存配置**：  
   - 点击右上角「绑定 OSS」→ 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward`（仅需一次）；  
   - 选择目标 OSS Bucket、地域及目录，确认路径模板；  
   - 设置转存范围（全部 / N 天前）及是否「释放平台存储」——若启用，资产将不再显示于资产中心列表。  
3. **API 集成**：调用生图/生视频模型时，在对应输入字段（如 `reference_image`、`first_frame`）中传入 `"asset_id": "xxx"`，三选一（`asset_id` / `image_url` / `image_base64`）即可。

## 限制和注意事项

- OSS 转存配置为**全局生效**，不随业务空间切换而变更；但资产列表始终仅展示当前业务空间下的数据。  
- 删除操作进入回收站，**非立即永久删除**；回收站资产保留 30 天，期间仍占用平台存储配额，到期后自动清除且不可恢复。  
- 若绑定 OSS 时勾选「释放平台存储」，则资产同步完成后即从平台存储移除，资产中心不再显示该条目——此行为不可逆，请务必确认。  
- > **注意**：[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确指出“已转存到 OSS 并选择释放平台存储的资产，不再占用平台存储容量”，但实测发现部分转存失败任务可能残留临时副本，建议定期检查「转存日志」并手动清理失败项。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


