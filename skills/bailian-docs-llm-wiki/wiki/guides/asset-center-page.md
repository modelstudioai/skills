# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于平台存储（限时免费），支持按业务空间隔离查看，并可通过全局 OSS 转存配置实现长期归档与成本优化。详细功能与行为边界请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；对应模型包括 `qwen-image-*` 系列（如 `qwen-image-3.0-pro`）、`wan2.7-*` 全系列（如 `wan2.7-t2v`、`wan2.7-i2v`、`wan2.7-videoedit` 等），具体列表以控制台实时展示为准。  
- **核心功能**：资产筛选（按类型/模型/时间/提示词）、收藏/取消收藏、批量删除与回收站管理、OSS 自动转存、资产详情查看、以及通过 `asset_id` 在生图/生视频 API 中直接引用已有资产。  
- **API 集成能力**：生图模型输入参数（如 `control_image`, `reference_image`）和生视频模型输入参数（如 `input_video`, `first_frame`）均支持 `asset_id` 字段，与 `image_url` / `video_url` / Base64 三选一或二选一，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“在 API 中使用资产”章节。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，由平台生成，可在资产详情弹窗中获取；用于 API 输入参数替代 URL/Base64 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | OSS 转存默认路径模板，其中 `{workspace}` 为当前业务空间标识 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| 转存范围策略 | 支持“全部资产”或“N 天前资产”，并可勾选“释放平台存储”（勾选后资产不再显示于资产中心） | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

> **注意**：OSS 转存配置为**全局设置**，不随业务空间切换而变化；但资产列表始终只展示当前所选业务空间下的资产。该行为与权限策略中 `AliyunBailianAssetCenterReader` 的作用域一致，需注意权限与数据视图的分离设计。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击“立即开通”。  
2. **OSS 绑定**：右上角 → “绑定 OSS” → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/路径 → 设置转存范围与是否释放平台副本。  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词；  
   - 收藏：悬停卡片 → 点击星标；启用“只看收藏”过滤；  
   - 删除：勾选后点击删除按钮 → 进入回收站（保留 30 天）→ 可恢复或永久删除；  
   - 查看详情：点击卡片 → 弹窗中获取 `asset_id` 及完整生成元信息。  
4. **API 集成示例（生图）**：  
   ```json
   {
     "model": "qwen-image-3.0-pro",
     "input": {
       "prompt": "a cat wearing sunglasses",
       "control_image": { "asset_id": "as-abc123xyz" }
     }
   }
   ```

## 限制和注意事项

- **存储生命周期**：  
  - 回收站内资产保留 30 天，期间仍占用平台存储配额并计费；  
  - 已转存至 OSS 并勾选“释放平台存储”的资产，**立即停止占用平台容量且不再计费**；  
  - 平台存储当前限时免费，商用后超出 5 GB 免费额度部分按 0.15 元/GB/月计费。  
- **权限隔离**：`AliyunBailianAssetCenterReader` 仅允许浏览与删除本空间资产，无法配置 OSS；OSS 相关操作需 `AliyunBailianAssetCenterAdmin` 权限。  
- **数据责任**：平台不承担因账户欠费、服务终止或回收站过期导致的数据丢失风险；强烈建议重要资产及时转存至自有 OSS 或本地备份。  
- **模型覆盖范围**：资产中心**仅收录调用支持模型时产生的输出资产**；若模型未在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 列出的支持列表中，则其输出不会进入资产中心。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


