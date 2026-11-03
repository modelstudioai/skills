# asset center page

资产中心是百炼平台统一管理模型生成图片与视频资产的核心控制台，支持筛选、收藏、删除、OSS 转存及 API 直接引用等关键能力。所有用户均可开通使用，平台存储当前限时免费；资产默认保存于百炼托管存储，也可通过配置自动同步至用户自有 OSS Bucket。详细背景和设计目标请参见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)。

## 支持的模型/功能

- **图片生成模型**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.0-pro`、`qwen-image-2.0`、`z-image-turbo`、`wan2.7-image-pro`、`wan2.7-image` 等（含多个带时间后缀的版本）  
- **视频生成模型**：`wan3.0-video`、`wan3.0-video-prime`、`happyhorse1.1-t2v/i2v/r2v`、`wan2.7-t2v/i2v/r2v`  
- **不支持类型**：音频资产暂未纳入管理范围（详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中“说明”部分）  
- **核心功能**：按类型/模型/时间/提示词筛选、收藏、批量删除、回收站恢复、OSS 自动转存、资产详情查看、API 中通过 `asset_id` 引用已有资产  

> **注意**：文档中列出的 `qwen-image-2.0-pro-2026-06-22` 等带未来日期后缀的模型名，疑似为占位符或过时命名规范；实际调用应以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中「支持的模型」列表为准，并结合控制台模型下拉选项或 `/models` API 返回结果验证可用性。

## 关键参数

| 参数 | 说明 | 是否必需 | 备注 |
|------|------|----------|------|
| `asset_id` | 资产唯一标识符，用于 API 输入引用 | 否（与 `image_url` / `image_base64` 三选一） | 在资产详情弹窗中获取；生图/生视频 API 均支持 |
| `workspace` | 业务空间标识，影响资产归属与统计范围 | 是（隐式） | 切换业务空间后仅显示该空间内资产，但 OSS 配置全局生效 |
| `{yyyy}/{mm}/{model}/{id}.{ext}` | 默认 OSS 路径模板 | 否（可编辑） | `{workspace}` 由系统注入，不可修改；路径中不含用户自定义前缀 |

## 使用方式

1. **开通与访问**：首次使用需访问 [资产中心](https://bailian.console.aliyun.com/cn-beijing/model/asset-center) 并点击「立即开通」；开通后入口固定，无需重复操作。  
2. **OSS 转存配置**（推荐长期资产管理）：  
   - 点击右上角「绑定 OSS」→ 授权 SLR 角色 `AliyunServiceRoleForBailianAssetForward` → 选择**未开启版本控制**的 OSS Bucket 与目录 → 设置路径模板、转存范围（全部/指定天数前）、是否释放平台存储副本。  
   - 绑定成功后，可在「OSS 转存配置」中查看日志、编辑或解绑；失败任务自动重试。  
3. **资产操作**：  
   - 筛选：顶部筛选栏支持类型、模型、日期、提示词关键词；  
   - 收藏：悬停卡片 → 点击星标；勾选「只看收藏」快速过滤；  
   - 删除：单选/多选 → 点击删除 → 进入回收站（保留 30 天）；  
   - 查看详情：点击卡片 → 弹窗展示完整元数据（含提示词、参数、模型、时间、`asset_id`）。  
4. **API 集成**：在生图/生视频请求体中，将原 `image_url` 或 `image_base64` 字段替换为 `"asset_id": "xxx"` 即可复用已存资产（具体字段名依模型接口文档而定）。

## 限制和注意事项

- **OSS 兼容性限制**：不支持已开启版本控制的 Bucket，否则转存失败（明确记载于 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)「配置 OSS 转存」章节）。  
- **存储计费逻辑**：  
  - 回收站内资产在 30 天保留期内**仍占用平台存储并计费**；  
  - 选择「释放平台存储」后，资产不再显示于资产中心，也不计入容量统计；  
  - 免费额度为 5 GB/账号，超量按 0.15 元/GB/月计费（自然月结算）。  
- **权限隔离**：资产列表按业务空间隔离，但 OSS 转存配置为全局设置，切换空间不影响已绑定 Bucket。  
- **数据安全提醒**：平台不承诺因欠费、服务终止或回收站过期导致的数据恢复；重要资产务必及时转存至自有 OSS 或本地备份。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md)


