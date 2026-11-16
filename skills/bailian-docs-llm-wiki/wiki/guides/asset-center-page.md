# asset center page

资产中心是百炼平台提供的生成资产（图片/视频）统一管理界面，支持筛选、收藏、删除、OSS 转存及 API 直接引用等核心能力。所有用户均可开通使用，平台存储当前限时免费；资产 ID 可在 API 中替代 URL 或 Base64 作为模型输入参数，提升调用效率与稳定性。详细功能说明请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **支持资产类型**：仅图片与视频（暂不支持音频）；
- **图片模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro` 等共 8 款（含带时间戳的版本），详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)；
- **视频模型**：`wan3.0-video`、`happyhorse1.1-t2v`、`wan2.7-i2v` 等共 8 款；
- **核心功能**：
  - 多维筛选（类型、模型、时间、提示词）；
  - 收藏/批量删除/回收站管理（保留期 30 天）；
  - OSS 转存（支持自动同步与可选释放平台副本）；
  - API 层 `asset_id` 直接引用（生图/生视频模型均支持）。

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期的模型名，可能为内部测试版本或命名规范残留；实际可用模型请以控制台下拉列表或 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中最新支持列表为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `asset_id` | string | 资产唯一标识，可在资产详情弹窗中获取；API 调用时可替代 `image_url` / `image_base64`（图片）或 `video_url` / `image_url`（视频）等字段 |
| `{workspace}` | string | OSS 路径模板中的业务空间标识，默认取当前 workspace ID |
| `{yyyy}/{mm}/{model}/{id}.{ext}` | path template | 默认 OSS 转存路径格式，不可自定义修改，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击**立即开通**；
2. **OSS 绑定**：
   - 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward`（无需 AccessKey）；
   - 选择**未开启版本控制**的 OSS Bucket（否则转存失败）；
   - 配置转存范围（全部/指定天数前）及是否释放平台存储副本；
3. **API 引用**：
   - 生图模型：在 `control_image`、`reference_image` 等参数中传入 `{ "asset_id": "xxx" }`；
   - 生视频模型：在 `first_frame`、`reference_video` 等参数中同理传入 `asset_id`；
4. **权限配置**：通过 RAM 授予 `AliyunBailianAssetCenterReader`（只读+删除）或 `AliyunBailianAssetCenterAdmin`（含 OSS 配置）策略。

## 限制和注意事项

- **OSS 兼容性限制**：不支持已开启版本控制的 Bucket，绑定将失败；
- **存储计费逻辑**：
  - 回收站内资产在 30 天保留期内**仍占用平台存储并计费**；
  - 选择“释放平台存储”后，资产不再显示于资产中心，且不计入容量统计；
- **全局配置约束**：OSS 转存配置对账号全局生效，**不随业务空间切换而变更**；
- **数据安全责任**：转存至自有 OSS 后，存储费用、ACL 控制、合规性等均由用户自行承担，平台不提供额外保障；
- **时效性提醒**：平台存储免费政策为限时措施，商用后按 0.15 元/GB/月计费，建议高频/长期资产优先转存 OSS。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


