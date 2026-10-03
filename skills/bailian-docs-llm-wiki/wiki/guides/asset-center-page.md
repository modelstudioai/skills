# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于平台存储（当前限时免费），用户可通过控制台或 API 全生命周期管理生成内容。详细功能与行为边界请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；对应模型包括 `qwen-image-*` 系列（如 `qwen-image-3.0-pro`）、`wan2.7-*` 全系列（如 `wan2.7-t2v`, `wan2.7-i2v`, `wan2.7-videoedit`）等，完整列表以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 控制台实时展示为准。
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）
  - 收藏/取消收藏、批量删除、回收站恢复
  - OSS 自动转存（含路径模板 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`）
  - 资产详情查看（含完整生成参数与提示词）
  - API 层直接通过 `asset_id` 引用资产（替代 `image_url` 或 `image_base64`）

> **注意**：文档中明确说明“OSS 转存配置为全局设置，不随业务空间切换而变化”，但同一账号下不同业务空间的资产统计独立显示——该行为与 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“切换业务空间后，资产会变化”的描述一致，无矛盾。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用；在资产详情弹窗右侧字段中获取 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}` | 路径模板变量，取值为当前业务空间标识，影响 OSS 转存目录结构 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 平台存储配额 | 默认 5 GB 免费额度，超量按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入用量 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。
2. **OSS 绑定**：
   - 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward`
   - 选择目标 OSS Bucket、地域、目录及路径模板
   - 设置转存范围（全部 / N 天前）及是否**释放平台存储**（勾选后资产不再显示于资产中心）
3. **API 集成**：
   - 生图模型：在 `input.image` 等参数中传入 `{ "asset_id": "xxx" }`，与 `image_url` / `image_base64` 三选一
   - 生视频模型：在 `input.video` 或 `input.image` 等参数中同理传入 `asset_id`

## 限制和注意事项

- **存储生命周期**：删除至回收站的资产保留 30 天，期间仍占用平台存储并计费；期满自动永久清除且不可恢复。
- **OSS 转存约束**：
  - 若绑定时选择“释放平台存储”，资产将**不进入资产中心列表**，仅存在于 OSS；
  - 转存失败任务自动重试，失败原因可查转存日志；
  - 转存后数据安全、访问控制及费用均由《阿里云存储服务协议》约束。
- **权限隔离**：资产列表按业务空间隔离，但 OSS 配置全局生效；子账号需至少授予 `AliyunBailianAssetCenterReader` 策略方可查看/删除资产。
- **重要提醒**：平台存储为临时性托管方案，[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确建议“及时将重要资产转存至自有 OSS Bucket 或本地环境备份”，因欠费、服务终止或回收站过期导致的数据丢失，平台无法恢复。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


