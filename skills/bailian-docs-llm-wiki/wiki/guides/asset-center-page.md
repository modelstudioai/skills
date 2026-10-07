# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心界面，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认保存于百炼平台存储（限时免费），用户可通过控制台开通并配置全局 OSS 同步策略。该功能面向开发者设计，强调资产可追溯性、存储可控性与跨服务复用能力。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的图片与视频资产：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：支持列表以控制台实时展示为准，[原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 中列举的模型版本含已标注日期的快照版（如 `2026-06-22`），实际可用性需结合模型生命周期状态判断；部分旧版模型可能已下线但文档未同步更新。

功能覆盖全生命周期操作：资产列表查看与多维筛选（类型/模型/时间/提示词）、单/批量收藏与删除、回收站管理（保留 30 天）、详情查看（含完整生成参数）、OSS 全局转存配置，以及通过 `asset_id` 在 API 中直接引用资产——该能力显著降低生图/生视频请求的传输开销与格式转换成本，详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“在 API 中使用资产”章节。

## 关键参数

- `asset_id`：每个资产唯一标识符，用于 API 输入参数（替代 `image_url` 或 `image_base64`），可在资产详情弹窗中直接复制。  
- OSS 路径模板：默认为 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识，不可修改但影响路径隔离性。  
- 转存范围策略：支持“全部资产”或“N 天前资产”，并强制要求选择是否**释放平台存储**（即是否保留副本）。若勾选释放，则资产不再出现在资产中心列表中，仅存在于 OSS。  
- 平台存储配额：默认 5 GB 免费额度，超限按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入已用容量，[原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确指出“删除至回收站的资产在保留期内仍占用平台存储容量”。

## 使用方式

1. **开通与入口**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击“立即开通”；开通后，所有后续生成的图片/视频将自动入库。  
2. **OSS 绑定**：点击右上角“绑定 OSS” → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择目标地域/Bucket/目录 → 配置路径模板与转存策略 → 完成绑定。绑定后配置全局生效，不随业务空间切换而变更。  
3. **API 集成**：调用生图（如 `qwen-image-3.0-pro`）或生视频（如 `wan2.7-t2v`）模型时，在对应输入字段（如 `control_image`、`reference_video`）中传入 `"asset_id": "xxx"`，无需额外提供 URL 或 Base64。  
4. **权限控制**：通过 RAM 策略授权子账号，`AliyunBailianAssetCenterReader` 满足基础浏览与删除需求，`AliyunBailianAssetCenterAdmin` 额外支持 OSS 配置操作。

## 限制和注意事项

- **资产类型限制**：仅支持图片与视频，**不支持音频资产**，此限制在 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 中明确声明。  
- **OSS 转存副作用**：若配置转存时勾选“释放平台存储”，则资产将从资产中心列表中消失，且无法通过平台界面恢复——仅能从 OSS 访问。该行为不可逆，需提前确认备份需求。  
- **业务空间隔离性**：资产列表严格按当前选中的业务空间过滤，但 OSS 转存配置、RAM 权限策略均为账号级全局设置，切换空间不影响已绑定的 Bucket 和权限分配。  
- **回收站时效性**：回收站资产保留期固定为 30 天，系统自动清理，无延长机制；手动永久删除亦不可恢复。建议重要资产及时转存至自有 OSS 或本地环境。  
- **计费边界**：已转存且释放平台存储的资产不计入容量统计；但转存失败或重试中的资产仍占用平台空间，直至转存成功并释放。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


