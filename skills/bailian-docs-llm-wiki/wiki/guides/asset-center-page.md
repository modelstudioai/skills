# asset center page

资产中心是百炼平台提供的统一资产管理入口，用于持久化保存、筛选和操作模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持通过资产 ID（`asset_id`）在 API 中直接复用已有资产，并提供 OSS 转存、收藏、回收站等核心管理能力。所有用户均可开通使用，平台存储当前限时免费 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频，**不支持音频资产** [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。  
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`。  
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`。  
- **核心功能**：按类型/模型/时间/提示词筛选、收藏、批量删除、回收站（保留 30 天）、OSS 转存、资产详情查看、API 级 `asset_id` 引用。

> **注意**：文档中列出的 `qwen-image-2.0-2026-03-03` 等带未来日期的模型版本名，可能为占位符或已过时命名；实际可用模型请以控制台模型列表或 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 中最新维护的模型清单为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `asset_id` | string | 资产唯一标识，可在资产详情弹窗中获取；API 中可替代 `image_url` 或 `image_base64` 使用 |
| `{workspace}` | string | OSS 路径模板中的业务空间标识，默认由当前 workspace 自动填充 |
| `{yyyy}/{mm}/{model}/{id}.{ext}` | path template | 默认 OSS 路径模板，支持自定义；其中 `{model}` 为模型 ID（非显示名称） |

> **注意**：OSS 转存**不支持已开启版本控制的 Bucket**，否则转存失败 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 使用方式

1. **开通**：首次访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**。  
2. **OSS 绑定（可选但推荐）**：右上角 → **绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择未开启版本控制的 Bucket 和路径 → 设置转存范围及是否释放平台存储。  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词搜索；  
   - 收藏：悬停卡片 → 点击星标；勾选“只看收藏”过滤；  
   - 删除：勾选后点删除 → 进入回收站（30 天保留期）→ 可恢复或永久删除；  
   - 查看详情：点击卡片 → 弹窗中获取 `asset_id` 及完整生成参数。  
4. **API 复用**：在生图/生视频请求中，将 `asset_id` 传入对应输入字段（如 `control_image.asset_id`），与 `image_url` / `image_base64` 三选一（图片）或二选一（视频）。

## 限制和注意事项

- **存储限制**：每个账号默认 5 GB 免费平台存储额度，超量部分按 0.15 元/GB/月计费；已转存并释放平台存储的资产不计入用量 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。  
- **回收站行为**：资产删除后进入回收站，**保留期内仍占用平台存储容量并持续计费**；30 天后自动永久清除且不可恢复。  
- **权限隔离**：资产列表按当前业务空间隔离，但 OSS 转存配置为全局设置，切换 workspace 不影响已绑定 Bucket [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。  
- **安全责任**：转存至自有 OSS 后，相关数据安全、访问控制及费用均由用户自行承担，适用《阿里云存储服务协议》。  
- **备份建议**：平台不承诺长期保存，重要资产须及时转存至 OSS 或本地环境。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


