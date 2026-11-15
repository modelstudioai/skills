# asset center page

资产中心是百炼平台提供的统一资产管理界面，用于持久化保存、筛选、操作和复用模型生成的图片与视频资产。它解耦了临时访问 URL 的生命周期限制，支持通过 asset_id 在 API 中直接引用已有资产，并可配置自动转存至自有 OSS Bucket。平台存储当前限时免费，但容量受业务空间隔离约束。

## 支持的模型/功能

资产中心支持管理以下模型生成的**图片**和**视频**资产（不支持音频）：  
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 及多个带时间后缀的版本（如 `qwen-image-2.0-2026-03-03`）、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`；  
- **视频模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`。  

核心功能包括：按类型/模型/时间/提示词筛选、收藏与“只看收藏”视图、批量删除与回收站管理（保留 30 天）、OSS 转存配置与日志查看、以及通过 asset_id 在 API 中复用资产。详情见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 关键参数

- `asset_id`：每个资产唯一标识，可在资产详情弹窗中获取，用于 API 输入（替代 `image_url` 或 `image_base64`）；  
- OSS 路径模板：默认为 `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}`，其中 `{workspace}` 为当前业务空间标识；  
- 转存范围策略：支持“全部资产”或“N 天前的资产”，并可选是否勾选**释放平台存储**（勾选后资产不再显示于资产中心）；  
- 平台存储配额：默认 5 GB 免费额度，超量部分按 0.15 元/GB/月计费；回收站内资产在 30 天保留期内仍占用配额。该计费逻辑详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

> **注意**：OSS 转存**不支持已开启版本控制的 Bucket**，否则转存任务将失败。此限制在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中明确说明，开发者配置前须确认 Bucket 版本控制状态。

## 使用方式

1. **开通**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**；  
2. **筛选与查看**：顶部统计栏显示当前业务空间资产总数、图片/视频数量及平台存储用量；支持按类型、模型、日期范围、提示词关键词筛选；  
3. **OSS 绑定**：右上角点击**绑定 OSS** → 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择地域/Bucket/路径 → 设置转存范围与释放策略；  
4. **API 复用**：调用生图/生视频模型时，在对应输入字段（如参考图、首帧图）中传入 `"asset_id": "xxx"`，三选一（`asset_id` / `image_url` / `image_base64`）或二选一（`asset_id` / URL/Base64），具体格式参见各模型 API 文档；  
5. **权限控制**：子账号需授予 `AliyunBailianAssetCenterReader`（基础操作）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置）策略。

## 限制和注意事项

- **业务空间隔离**：资产列表严格按当前选中的业务空间展示，但 OSS 转存配置为全局生效，切换空间不影响已绑定配置；  
- **回收站行为**：删除资产进入回收站后仍占用平台存储，30 天后自动永久清除且不可恢复；手动永久删除亦不可逆；  
- **OSS 兼容性**：仅支持未开启版本控制的 Bucket，启用版本控制将导致转存失败；  
- **存储成本提示**：平台存储单价（0.15 元/GB/月）高于阿里云 OSS 标准存储，长期资产建议转存 OSS 并勾选释放平台存储以控本；  
- **数据责任边界**：因账户欠费、服务终止或回收站超期导致的资产丢失，平台不提供恢复能力，强烈建议重要资产同步备份至自有环境。以上约束均依据 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 官方说明整理。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


