# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台页面，提供筛选、收藏、删除、OSS 转存及 API 引用等能力。所有资产默认持久化于百炼平台存储（限时免费），用户可通过控制台或 API 全生命周期管理生成内容。详细功能与行为规范请参考 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

资产中心当前支持管理以下模型生成的**图片与视频资产**（不支持音频）：  
`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro-2026-06-22`、`qwen-image-2.0-pro-2026-04-22`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-2.0-2026-03-03`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image`、`wan2.7-videoedit`、`wan2.7-r2v`、`wan2.7-i2v`、`wan2.7-t2v`。  
> **注意**：模型列表以控制台资产中心页面实时展示为准，[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中所列版本号（如 `2026-06-22`）为快照标识，实际可用模型可能因灰度发布而存在滞后，建议以控制台下拉菜单为准。

核心功能包括：  
- 多维筛选（类型、模型、时间、提示词关键词）  
- 收藏/取消收藏、批量删除、回收站恢复与永久清除  
- OSS 自动转存（含路径模板、释放平台副本策略）  
- 通过 `asset_id` 在生图/生视频 API 中直接引用已有资产（替代 `image_url` 或 `image_base64`）

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用；在资产详情弹窗中可见 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `{workspace}/{yyyy}/{mm}/{model}/{id}.{ext}` | 默认 OSS 路径模板，其中 `{workspace}` 为当前业务空间 ID | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |
| `AliyunServiceRoleForBailianAssetForward` | OSS 转存必需的服务关联角色（SLR），授权后自动创建 | [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) |

> **注意**：OSS 转存**不支持已开启版本控制的 Bucket**，否则同步失败；该限制未在控制台配置页显式提示，需开发者主动校验 Bucket 配置。

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击「立即开通」；开通后入口固定，无需重复操作。  
2. **OSS 绑定**：右上角「绑定 OSS」→ 授权 SLR → 选择地域/Bucket/目录 → 设置路径模板与转存范围（全部 or N 天前）→ 选择是否「释放平台存储」。  
3. **API 引用**：调用 `qwen-image-*` 或 `wan2.7-*` 等模型 API 时，在对应输入字段（如 `control_image`、`first_frame`）中传入 `"asset_id": "xxx"`，**不可与其他输入方式（URL/Base64）共存**。  
4. **回收站操作**：删除资产后进入回收站，30 天内可恢复；超期自动永久清除且不可逆。

## 限制和注意事项

- **存储限制**：平台存储默认 5 GB 免费额度，超量按 0.15 元/GB/月计费；**回收站中的资产在保留期内仍占用配额**，释放需手动清空或等待自动清理。  
- **OSS 全局性**：转存配置对账号全局生效，不随业务空间切换而变更；但资产列表仅显示当前业务空间下的生成结果。  
- **权限隔离**：`AliyunBailianAssetCenterReader` 仅允许浏览与删除，`AliyunBailianAssetCenterAdmin` 才可配置 OSS；子账号无权限时将隐藏「绑定 OSS」按钮。  
- **数据安全责任**：转存至自有 OSS 后，存储费用、ACL 控制、加密策略及合规责任均由用户承担，详见《阿里云存储服务协议》。  
- **关键风险提示**：平台不承诺数据长期保存，因欠费、服务终止或回收站超期导致的资产丢失**不可恢复**，强烈建议重要资产及时转存至自有 OSS 或本地备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


