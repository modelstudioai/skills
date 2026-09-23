# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于平台存储（限时免费），支持按业务空间隔离查看，并可通过全局 OSS 转存配置实现长期归档与成本优化。详细功能与行为规范请参阅 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；  
- **支持模型**：包括 `qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-*` 系列、`z-image-turbo`、`wan2.7-*` 全系（如 `wan2.7-t2v`、`wan2.7-i2v`、`wan2.7-r2v`、`wan2.7-videoedit`）等；具体列表以控制台实时展示为准，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)；  
- **核心功能**：资产筛选（按类型/模型/时间/提示词）、收藏/取消收藏、批量删除与回收站管理、OSS 自动转存、资产详情查看、以及通过 `asset_id` 在 API 中直接引用已有资产。

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型名疑似版本命名错误或已过时，实际可用模型请以控制台资产中心页面下拉菜单中动态加载的列表为准；该矛盾信息已在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中明确提示“支持的模型列表可能随产品迭代而变化”。

## 关键参数

- `asset_id`：每个资产唯一标识符，用于 API 输入（替代 `image_url` 或 `image_base64`），可在资产详情弹窗中直接复制；  
- OSS 路径模板：默认为 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID；  
- 平台存储配额：默认 5 GB 免费额度，超量部分按 0.15 元/GB/月计费；  
- 回收站保留期：30 天（含已删除但未永久清除的资产，期间仍占用平台存储）；  
- 转存范围策略：支持“全部资产”或“N 天前资产”，并可选是否释放平台存储副本（释放后资产不再显示于资产中心）。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**；  
2. **OSS 绑定**：右上角点击**绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/路径 → 配置转存范围与副本策略；  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词；  
   - 收藏：悬停卡片 → 点击星标；勾选**只看收藏**快速过滤；  
   - 删除：勾选后点击删除按钮 → 进入回收站（非永久）；  
   - 查看详情：点击卡片 → 弹窗中获取 `asset_id` 及完整生成上下文；  
4. **API 集成**：在生图/生视频请求体中，将原 `image_url` 或 `video_url` 字段替换为 `{ "asset_id": "xxx" }`（三选一或二选一，不可混用）；更多示例见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 限制和注意事项

- OSS 转存配置为**全局生效**，不随业务空间切换而变更；  
- 若绑定 OSS 时选择“释放平台存储”，则资产**不会出现在资产中心列表中**，仅存在于目标 OSS Bucket；  
- 回收站中的资产在 30 天保留期内仍计入平台存储用量并参与计费；  
- 删除至回收站 ≠ 永久删除，需手动执行“永久删除”或等待自动清理；  
- 平台存储免费期为限时策略，商用计费启动后，超出 5 GB 的部分将按自然月结算；  
- > **注意**：文档中“平台存储目前限时免费使用”与“商用计费启动后……”存在状态模糊性，建议开发者主动监控控制台通知及账单中心更新，避免因计费策略切换导致意外扣费——该风险点已在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“平台存储与计费”章节中强调。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


