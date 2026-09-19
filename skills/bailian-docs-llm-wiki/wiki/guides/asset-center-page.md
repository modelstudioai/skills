# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于百炼平台存储（限时免费），支持按业务空间隔离查看，并可通过全局 OSS 配置实现长期归档与成本优化。详细功能与行为边界请严格参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 文档。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；对应模型包括 `qwen-image-*` 系列（如 `qwen-image-3.0-pro`）、`wan2.7-*` 全系列（如 `wan2.7-t2v`, `wan2.7-i2v`, `wan2.7-videoedit`）等，完整列表以控制台实时展示为准。  
- **核心功能**：资产筛选（按类型/模型/时间/提示词）、收藏/取消收藏、单个或批量删除（进入回收站）、查看详情（含提示词、参数、生成时间）、OSS 自动转存、以及通过 `asset_id` 在 API 中直接引用资产。  
- **API 集成能力**：生图模型输入参数（如 `control_image`, `reference_image`）和生视频模型输入参数（如 `input_video`, `first_frame`）均支持 `asset_id` 字段，与 `image_url` / `image_base64` / `video_url` 互斥使用——该机制显著降低客户端带宽与编码开销。具体字段兼容性详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“在 API 中使用资产”章节。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，字符串格式，可在资产详情弹窗中直接复制；是 API 中替代 URL/Base64 的关键字段 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| OSS 路径模板 | 默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID；路径模板不可自定义，仅可选择 Bucket 和目录前缀 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 转存范围策略 | 支持“全部资产”或“N 天前资产”；启用后可选是否勾选“释放平台存储”（即不保留副本） | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

> **注意**：文档中明确说明“OSS 转存配置为全局设置，不随业务空间切换而变化”，但同一账号下不同业务空间的资产仍独立统计与展示。这意味着：若在业务空间 A 绑定 OSS，业务空间 B 生成的资产也会触发转存（只要满足转存范围条件），但 B 的资产列表中不会显示转存状态按钮——该行为易引发权限与归属混淆，建议在多业务空间场景下由统一管理员配置并同步告知各空间负责人。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**；开通后入口固定，无需重复操作。  
2. **OSS 绑定**：右上角 → **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/目录 → 设置路径模板与转存策略 → 完成。绑定后可在**OSS 转存配置**中编辑或解绑。  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词组合过滤；  
   - 收藏：悬停卡片 → 点击星标；勾选“只看收藏”快速聚焦；  
   - 删除：勾选后点删除 → 进入回收站（保留 30 天）→ 可恢复或永久删除；  
   - 查看详情：点击卡片 → 弹窗中获取 `asset_id` 及完整元数据。  
4. **API 引用**：在调用 `qwen-image-*` 或 `wan2.7-*` 模型时，将原 `image_url` 字段替换为 `{ "asset_id": "xxx" }` 对象（JSON 结构），服务端自动解析并加载对应资产。

## 限制和注意事项

- **存储生命周期**：  
  - 回收站内资产**仍占用平台存储容量**，30 天保留期满后自动永久清除且不可恢复；  
  - 已转存至 OSS 并勾选“释放平台存储”的资产，**立即从资产中心列表消失且不计入平台容量**；  
  - 平台存储免费额度为 5 GB/账号，超量部分按 0.15 元/GB/月计费（自然月结算）。  
- **权限隔离**：资产列表按业务空间隔离，但 OSS 配置、SLR 授权、回收站操作均跨空间生效；子账号需显式授予 `AliyunBailianAssetCenterReader` 或 `AliyunBailianAssetCenterAdmin` 策略方可操作。  
- **安全与责任**：  
  > **注意**：文档强调“因账户欠费、服务终止或回收站保留期届满等原因导致的数据丢失，平台不可恢复”。这意味着资产中心**不提供跨账号/跨区域容灾备份能力**，生产环境必须依赖 OSS 转存或主动导出至本地，不可将平台存储视为唯一持久化层。  
- **模型覆盖范围**：仅支持明确列出的图像与视频生成模型；其他模型（如文本类、音频类、`qwen-vl` [多模态](../concepts/multimodal.md)理解模型）输出不进入资产中心，亦无法通过 `asset_id` 引用。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


