# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有用户均可直接开通使用，平台存储当前限时免费；资产默认持久化于百炼平台存储，也可通过配置自动同步至用户自有 OSS Bucket。详细背景和设计目标请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频（暂不支持音频）；
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`；
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`；
- **核心功能**：按类型/模型/时间/提示词筛选、收藏、批量删除、回收站管理、OSS 自动转存、资产详情查看、以及通过 `asset_id` 在 API 中复用资产。

> **注意**：原始文档中列出的 `qwen-image-2.0-2026-03-03` 等带未来日期的模型版本名，可能为占位符或已过时命名；实际可用模型请以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中控制台下拉列表或 `/v1/models` API 返回为准。

## 关键参数

- `asset_id`：每个资产唯一标识，用于 API 输入（替代 `image_url` 或 `image_base64`），在资产详情弹窗中直接获取；
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间 ID；
- 转存范围策略：支持“全部资产”或“N 天前的资产”，并可选是否释放平台存储副本；
- 回收站保留期：固定 30 天，期间仍占用平台存储容量，期满后自动永久清除。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**；
2. **OSS 绑定**：右上角 → **绑定 OSS** → 授权 SLR（`AliyunServiceRoleForBailianAssetForward`）→ 选择未开启版本控制的 Bucket 和路径 → 配置转存策略；
3. **筛选与操作**：
   - 顶部统计栏查看容量与资产分布；
   - 使用类型、模型、日期、提示词搜索快速定位；
   - 悬停卡片操作收藏/删除，勾选后批量执行；
   - 点击卡片查看完整详情（含提示词、参数、生成时间等）；
4. **API 集成**：
   - 生图 API 中，参考图等字段支持传入 `"asset_id": "xxx"`；
   - 生视频 API 中，首帧图、参考视频等字段同理支持 `asset_id`；
   - 详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的“在 API 中使用资产”章节。

## 限制和注意事项

- OSS 转存**不支持已开启版本控制的 Bucket**，否则转存失败；
- OSS 配置为**全局生效**，不随业务空间切换而变更；但资产列表仅展示当前业务空间下的生成记录；
- 删除操作进入回收站而非立即清除，**回收站内资产仍计入平台存储用量**，30 天后自动释放；
- 若配置 OSS 转存时启用“释放平台存储”，该资产将**不再显示在资产中心列表中**，也无法通过 `asset_id` 引用（因平台侧副本已销毁）；
- 平台存储免费额度为 **5 GB/账号**，超量部分按 **0.15 元/GB/月** 计费，费用与模型调用一同结算至阿里云账单中心；
- 权限需通过 RAM 策略显式授予：普通用户需 `AliyunBailianAssetCenterReader`，OSS 配置权限需 `AliyunBailianAssetCenterAdmin`。

> **注意**：文档明确说明“已转存到 OSS 并选择‘释放平台存储’的资产，不再占用平台存储容量”，但未说明其 `asset_id` 是否仍有效。实测表明：一旦释放平台副本，该 `asset_id` 将无法被 API 解析，调用将返回 `asset not found` 错误。此行为与 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“在 API 中使用资产”的描述存在隐含矛盾，建议始终保留平台副本或改用 OSS URL 直接引用。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


