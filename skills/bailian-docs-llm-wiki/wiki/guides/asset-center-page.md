# asset center page

资产中心是百炼平台提供的生成资产（图片/视频）统一管理界面，用于持久化保存、筛选、收藏、删除及转存模型输出结果。所有通过百炼支持的生图/生视频模型生成的资产，在开通后自动进入该中心；临时 URL 失效后，仍可通过资产 ID 或平台界面访问已保存内容。平台存储当前限时免费，建议长期资产及时转存至自有 OSS [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅图片与视频（暂不支持音频）；
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`；
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v`、`happyhorse1.1-i2v`、`happyhorse1.1-r2v`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期后缀的模型名，需以控制台实际可用模型列表为准；部分测试模型可能已下线或重命名，具体请以 [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“支持的模型”节最新描述及 API 模型列表接口返回为准。

核心功能包括：
- 多维筛选（类型、模型、时间、提示词关键词）；
- 收藏/取消收藏、批量删除、回收站管理（保留 30 天）；
- OSS 自动转存（含路径模板 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`）；
- 资产详情查看（含完整生成参数、提示词、模型名、时间）；
- 在 API 中直接通过 `asset_id` 引用已有资产，替代 `image_url` 或 `image_base64` [原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `asset_id` | 资产唯一标识，字符串格式，可在资产详情弹窗中获取 | 必须用于 API 输入引用；不可手动构造 |
| OSS 路径模板 | 默认 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，支持自定义 | `{workspace}` 为当前业务空间标识，不可省略 |
| 转存范围 | 全部资产 / N 天前资产 | 若选“释放平台存储”，资产将不再显示于资产中心 |
| 平台存储额度 | 默认 5 GB 免费；超量按 0.15 元/GB/月计费 | 回收站内资产在 30 天保留期内仍计入用量 |

## 使用方式

1. **开通**：首次访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center)，点击**立即开通**；
2. **OSS 绑定**（可选但推荐）：
   - 授权服务关联角色 `AliyunServiceRoleForBailianAssetForward`；
   - 选择**未开启版本控制**的 OSS Bucket（否则转存失败）[原文标题](../../raw/model-user-guide/asset-center-page/asset-center.md)；
   - 配置地域、Bucket、目录及转存策略（是否释放平台副本）；
3. **API 集成**：
   - 生图模型输入字段（如 `control_image`, `reference_image`）支持传入 `{ "asset_id": "xxx" }`；
   - 生视频模型输入字段（如 `first_frame`, `reference_video`）同理支持 `asset_id`；
   - `asset_id` 与 `image_url` / `image_base64` 互斥，三选一（图片）或二选一（视频）；
4. **日常管理**：通过顶部筛选栏快速定位资产，悬停卡片操作收藏/删除，点击查看详情及复制 `asset_id`。

## 限制和注意事项

- ❗ OSS 转存**不支持已开启版本控制的 Bucket**，绑定时若选错将导致所有转存任务失败；
- ❗ 回收站中资产**保留期为 30 天**，到期自动永久清除且不可恢复；手动永久删除亦不可逆；
- ❗ 平台存储计费以自然月为周期，**删除至回收站不释放容量**，仅永久删除或 OSS 转存并勾选“释放平台存储”后才停止计费；
- ❗ OSS 转存配置为**全局生效**，不随业务空间切换而变更；但资产列表仅展示当前业务空间下的生成记录；
- ❗ `asset_id` 仅在本账号、本区域（如 cn-beijing）内有效，跨区域或跨账号不可复用；
- ⚠️ 建议重要资产同步备份至本地或自有 OSS，因欠费、服务终止或回收站过期导致的数据丢失，平台不提供恢复能力。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


