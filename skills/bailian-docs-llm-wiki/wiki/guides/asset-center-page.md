# asset center page

资产中心是百炼平台提供的生成资产（图片/视频）统一管理界面，支持筛选、收藏、删除、OSS 转存及 API 引用等核心操作。所有资产默认保存在百炼平台存储中，用户可自主配置转存策略以控制存储成本与数据主权。该功能已全量开放，无需额外申请 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持的资产类型**：仅限图片和视频（暂不支持音频）；
- **支持的模型**：包括 `qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个 `wan2.7-*` 系列模型（如 `wan2.7-t2v`、`wan2.7-i2v` 等），完整列表请以控制台实时展示为准 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)；
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）；
  - 收藏/取消收藏、批量删除、回收站恢复；
  - OSS 自动转存（含路径模板、释放平台副本选项）；
  - 在生图/生视频 API 中直接通过 `asset_id` 引用已有资产，替代 `image_url` 或 `image_base64` [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用 | `as-abc123xyz` |
| OSS 路径模板 | 决定转存至 Bucket 的文件路径结构 | `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` |
| 转存范围 | 全部资产 或 `N` 天前的资产 | `30`（表示仅转存 30 天前生成的资产） |
| 释放平台存储 | 开启后，转存成功即从平台存储中移除该资产 | `true` / `false` |

> **注意**：OSS 转存**不支持已开启版本控制的 Bucket**，否则任务将失败；该限制在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中明确标注，但部分旧版文档未同步更新此约束。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**；
2. **OSS 绑定**：
   - 授权服务关联角色 `AliyunServiceRoleForBailianAssetForward`（自动完成）；
   - 选择目标地域、Bucket（须为**未开启版本控制**）、目录及路径模板；
   - 设置转存范围与是否释放平台存储副本；
3. **API 集成**：
   - 生图模型：在 `input.image` 等字段中传入 `{ "asset_id": "as-xxx" }`；
   - 生视频模型：在 `input.reference_video` 或 `input.first_frame` 等字段中同理传入 `asset_id`；
4. **权限配置**：通过 RAM 授予 `AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置权限）。

## 限制和注意事项

- **存储生命周期**：回收站中资产保留 30 天，期间仍占用平台存储并计费；超期后自动永久清除，不可恢复；
- **平台存储计费**：当前限时免费，商用后超出 5 GB 免费额度部分按 **0.15 元/GB/月** 计费；已转存且启用“释放平台存储”的资产不计入用量；
- **业务空间隔离**：资产列表按当前选中的业务空间过滤，但 OSS 转存配置为全局生效，切换空间不影响已绑定设置；
- **安全责任**：转存至自有 OSS Bucket 后，其存储费用、ACL 控制、数据安全均由用户自行承担，适用《阿里云存储服务协议》；
- **备份建议**：平台不承诺长期数据可用性，强烈建议对重要资产及时转存至 OSS 或本地环境备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


