# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台页面，提供筛选、收藏、删除、OSS 转存及 API 引用等完整生命周期能力。所有资产默认保存于百炼平台存储（限时免费），用户可按需配置自动转存至自有 OSS Bucket。该功能面向已开通百炼服务的开发者，需在控制台显式开通后方可使用，详情请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；  
- **支持模型**：包括 `qwen-image-3.0-pro`、`qwen-image-3.0`、`wan2.7-t2v`、`wan2.7-i2v`、`wan2.7-r2v`、`wan2.7-videoedit` 等全部生图/生视频模型（完整列表以控制台实时展示为准）；  
- **核心功能**：资产筛选（按类型/模型/时间/提示词）、收藏/取消收藏、批量删除与回收站管理、OSS 自动转存、资产详情查看，以及通过 `asset_id` 在 API 中直接引用已有资产——该能力显著简化输入构造，避免重复上传，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“在 API 中使用资产”章节。

> **注意**：文档中列出的模型版本如 `qwen-image-2.0-2026-03-03` 含未来日期，属占位命名，实际可用模型请以控制台资产中心「模型」筛选下拉菜单为准；过期或下线模型不会出现在筛选项中，也不会产生新资产记录。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入（替代 `image_url` 或 `image_base64`），可在资产详情弹窗中直接复制 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 转存默认路径模板，其中 `{workspace}` 为当前业务空间 ID，不可修改 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 转存范围策略 | 支持「全部资产」或「N 天前资产」；启用后可选是否「释放平台存储」（即不保留副本） | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通入口**：首次访问需前往 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击「立即开通」；  
2. **OSS 绑定**：右上角「绑定 OSS」→ 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择未开启版本控制的 Bucket 及目录 → 配置转存策略；  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词组合过滤；  
   - 收藏：悬停卡片点击星标，勾选「只看收藏」快速聚焦；  
   - 删除：勾选后点击「删除」，资产进入回收站（保留 30 天）；  
   - 查看详情：点击卡片弹出完整元数据（含提示词、参数、生成时间）；  
4. **API 集成**：调用生图/生视频 API 时，在对应输入字段（如 `control_image`、`reference_video`）中传入 `"asset_id": "xxx"`，三选一（`asset_id` / `image_url` / `image_base64`）即可。

## 限制和注意事项

- **存储限制**：平台存储默认 5 GB 免费额度，超量部分按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内**仍占用配额并计费**；  
- **OSS 约束**：仅支持**未开启版本控制**的 Bucket，否则转存失败；转存配置为全局生效，不随业务空间切换而变更；  
- **权限隔离**：资产列表按当前业务空间隔离，但 `AliyunBailianAssetCenterReader` 和 `AliyunBailianAssetCenterAdmin` 权限策略需通过 RAM 显式授予子账号；  
- **数据安全**：转存至 OSS 后，存储费用、ACL 控制、加密策略及合规责任均由用户自行承担，平台不干预也不备份；  
- **风险提示**：平台存储非持久化备份方案，因欠费、服务终止或回收站超期导致的数据丢失不可恢复，请务必及时转存至自有环境。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


