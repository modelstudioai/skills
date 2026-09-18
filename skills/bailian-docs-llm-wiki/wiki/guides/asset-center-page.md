# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于百炼平台存储（当前限时免费），用户可通过控制台或 API 全生命周期管理资产。详细功能与行为规范请参阅 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅图片与视频（不支持音频）；对应模型包括 `qwen-image-*` 系列（如 `qwen-image-3.0-pro`、`qwen-image-2.0-2026-03-03`）、`wan2.7-*` 全系列（`t2v`/`i2v`/`r2v`/`videoedit` 等）及 `z-image-turbo`。完整列表以控制台实时展示为准，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）
  - 收藏/取消收藏、批量删除、回收站恢复
  - OSS 自动转存（含路径模板、释放平台副本选项）
  - 资产详情查看（含完整生成参数与提示词）
  - 在 API 中通过 `asset_id` 直接引用已有资产（替代 `image_url` 或 `image_base64`）

> **注意**：文档中明确说明“OSS 转存配置为全局设置，不随业务空间切换而变化”，但同一账号下不同业务空间的资产独立隔离——这意味着资产归属严格按业务空间划分，而转存策略共享。该设计易引发权限误判，建议在子账号策略中结合 `workspace` 条件精细化授权，参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的权限说明章节。

## 关键参数

| 参数 | 说明 | 取值示例 |
|------|------|----------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用 | `asst_abc123xyz` |
| `{workspace}` | 路径模板变量，取值为当前业务空间 ID | `ws-prod-2024` |
| `{yyyy}/{mm}/{model}/{id}.{ext}` | 默认 OSS 路径模板，不可自定义结构 | `prod/2024/06/qwen-image-3.0-pro/asst_xxx.png` |
| 转存范围 | 支持“全部资产”或“N 天前资产” | `30`（表示仅转存 30 天前生成的资产） |

## 使用方式

1. **开通与访问**：首次使用需前往 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 点击**立即开通**（控制台入口见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)）。
2. **OSS 绑定**：
   - 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward`
   - 选择目标地域、Bucket、目录及路径模板
   - 设置转存范围与是否释放平台副本（若选“释放”，资产将不再显示于资产中心）
3. **API 引用**：
   - 生图模型：在 `input.image` 等字段中传入 `{ "asset_id": "asst_xxx" }`，与 `image_url` / `image_base64` 三选一
   - 生视频模型：在 `input.reference_image` 或 `input.reference_video` 中同理传入 `asset_id`

## 限制和注意事项

- **存储与计费**：
  - 平台存储默认 5 GB 免费额度，超量按 0.15 元/GB/月计费（自然月统计）
  - 回收站内资产在 30 天保留期内**仍占用平台容量并计费**，清理后停止计费
  - 已转存至 OSS 并启用“释放平台存储”的资产，**立即从资产中心消失且不计入容量**
- **权限约束**：
  - `AliyunBailianAssetCenterReader` 仅允许浏览与删除，**不包含 OSS 配置权限**
  - `AliyunBailianAssetCenterAdmin` 是唯一支持绑定/编辑 OSS 配置的策略
- **关键风险提示**：
  - 删除至回收站的资产 30 天后自动永久清除，**不可恢复**
  - 因欠费、服务终止或回收站过期导致的数据丢失，平台不提供恢复服务
  - 建议重要资产同步备份至自有 OSS 或本地环境

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


