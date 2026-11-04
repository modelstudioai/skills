# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，支持筛选、收藏、删除、OSS 转存及 API 直接引用等关键能力。所有用户均可开通使用，平台存储当前限时免费；资产默认保存于百炼平台存储，也可通过配置自动同步至用户自有 OSS Bucket。详细背景和设计目标请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **图片生成模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image` 等（含多个带时间后缀的版本）  
- **视频生成模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`  
- **不支持类型**：音频资产暂未纳入管理范围（详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)）  
- **核心功能**：按类型/模型/时间/提示词筛选、收藏、批量删除、回收站恢复、OSS 自动转存、资产详情查看、API 中通过 `asset_id` 引用已有资产  

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型名疑似为占位符或已过时命名，实际可用模型请以控制台下拉列表或 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中最新维护列表为准。

## 关键参数

| 参数 | 说明 | 是否必需 | 备注 |
|------|------|----------|------|
| `asset_id` | 资产唯一标识符，由平台生成，可在资产详情弹窗中获取 | 否（仅在 API 引用时需提供） | 生图/生视频 API 中可替代 `image_url` 或 `image_base64`；三选一（图片）或二选一（视频） |
| OSS 路径模板 | 默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | 是（绑定时配置） | `{workspace}` 为当前业务空间 ID；路径中不可含 `..` 或绝对路径 |
| 转存范围策略 | “全部资产” 或 “N 天前的资产” | 是 | 影响历史资产是否触发转存 |
| 释放平台存储 | 勾选后，转存成功即删除平台副本 | 否（默认不勾选） | 若勾选，该资产将不再出现在资产中心列表中 |

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**（开通后全局生效）  
2. **OSS 绑定**：右上角 → **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择未开启版本控制的 Bucket 及目录 → 配置转存策略（详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)）  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词搜索  
   - 收藏：悬停卡片 → 点击星标；勾选“只看收藏”快速过滤  
   - 删除：勾选后点击删除按钮 → 进入回收站（保留 30 天）→ 可恢复或永久删除  
4. **API 集成**：在调用 `qwen-image-*` 或 `wan3.0-video*` 等模型时，在输入参数中传入 `"asset_id": "xxx"` 即可复用已有资产，无需重复上传  

## 限制和注意事项

- **OSS 兼容性限制**：不支持已开启版本控制的 OSS Bucket，否则转存失败（明确记载于 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)）  
- **存储计费逻辑**：  
  - 回收站内资产在 30 天保留期内**仍占用平台存储并计费**  
  - 已转存且勾选“释放平台存储”的资产**立即释放容量、停止计费**  
  - 免费额度为 5 GB/账号，超量部分按 0.15 元/GB/月计费  
- **权限隔离**：资产列表按**当前业务空间**隔离，但 OSS 转存配置为全局设置，切换空间不影响已绑定 Bucket  
- **数据安全提醒**：平台不承诺因欠费、服务终止或回收站过期导致的数据恢复；重要资产须及时转存至自有 OSS 或本地备份

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


