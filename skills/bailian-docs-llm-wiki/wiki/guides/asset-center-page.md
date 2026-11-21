# asset center page

资产中心是百炼平台提供的统一资产管理入口，用于持久化保存、筛选和操作模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持通过资产 ID（`asset_id`）在 API 中直接复用已有资产，并提供 OSS 转存、收藏、回收站等核心管理能力。该功能已全量开放，平台存储当前限时免费 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅限图片与视频，**不支持音频资产**（详见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)）。
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `2026-06-22`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`。
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-r2v/i2v/t2v`。
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）
  - 收藏/取消收藏、批量删除、回收站（保留 30 天）
  - 资产详情查看（含完整生成参数与提示词）
  - OSS 转存（全局配置，支持路径模板与自动释放平台副本）

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型版本名，疑似为占位符或过时命名规范；实际调用请以控制台或 OpenAPI 文档中最新发布的模型 ID 为准。该信息未在其他权威文档交叉验证，建议以 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 中的列表为初始参考，但需结合 `/v1/models` 接口实时枚举确认可用性。

## 关键参数

- `asset_id`：每个资产唯一标识，可在资产详情弹窗中获取，用于 API 输入复用。
- OSS 路径模板：默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识。
- 转存范围策略：支持“全部资产”或“N 天前资产”，并可选是否勾选**释放平台存储**（勾选后资产不再显示于资产中心）。
- 平台存储配额：默认 5 GB 免费额度，超限按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍计入已用容量。

## 使用方式

1. **开通**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**。
2. **OSS 绑定**：
   - 授权服务关联角色 `AliyunServiceRoleForBailianAssetForward`（SLR）；
   - 选择**未开启版本控制**的 OSS Bucket（否则转存失败）；
   - 配置地域、Bucket、目录及转存策略。
3. **API 复用资产**：
   - 生图模型：在 `image_url` / `image_base64` / `asset_id` 三者中**仅传其一**；
   - 生视频模型：在 URL / Base64 / `asset_id` 中**二选一**；
   - 示例字段（以生图控制图为例）：`{"control_image": {"asset_id": "as-xxx"}}`。
4. **管理操作**：通过卡片悬停触发收藏/删除；右上角切换“只看收藏”或进入“回收站”执行恢复/永久删除。

## 限制和注意事项

- OSS 转存**不支持已开启版本控制的 Bucket**，绑定前须确认 Bucket 版本控制状态为关闭（见 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)）。
- 回收站资产保留期为 **30 天**，到期自动永久清除且不可恢复；手动永久删除亦不可逆。
- 平台存储计费以自然月为周期，删除至回收站的资产在保留期内**持续计费**；仅当 OSS 转存并勾选“释放平台存储”后，才停止占用配额。
- 权限隔离基于业务空间：资产列表按当前业务空间过滤，但 OSS 转存配置为账号级全局设置，切换空间不影响已绑定配置。
- 建议对重要资产及时转存至自有 OSS 或本地备份；因欠费、服务终止或回收站超期导致的数据丢失，平台不提供恢复能力。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


