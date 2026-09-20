# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、客服、法律、金融、数据挖掘、多模态交互等多个垂直场景。所有应用均基于百炼统一模型服务底座构建，支持快速集成与二次定制。开发者可通过控制台或 API 直接调用，无需从零训练模型。

## 支持的模型/功能

应用广场中的每个应用均绑定特定模型栈与功能模块，例如：
- `通义拍照解题辅导` 基于 Qwen-VL 多模态模型 + 教育领域微调策略，支持图像识别与分步解题推理；
- `通义听悟Agent` 依赖 ASR+LLM+TTS 全链路 pipeline，提供会议纪要生成、发言摘要、待办提取等能力；
- `千问联网检索Agent` 集成 RAG 框架与实时网页抓取模块，支持动态知识注入。

全部官方应用清单及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 关键参数

调用任一应用时，需传入以下通用参数（部分应用支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用广场」页获取，如 `edu-tutor`、`tingwu-agent` 等 |
| `input` | object | 是 | 输入结构体，格式依应用而异（如 `tongyi-farui` 要求 `{"query": "..."}`，`ui-agent` 要求 `{"screenshot": "base64..."}`） |
| `timeout` | integer | 否 | 请求超时（秒），默认 60，最大 300 |

各应用具体输入/输出 Schema 及参数约束，请参考对应子文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 中定义了 `voice_style`、`duration_limit` 等专属字段。

## 使用方式

1. **控制台接入**：登录百炼控制台 → 进入「应用广场」→ 选择目标应用 → 点击「立即使用」获取 `app_id` 与调试面板；
2. **API 调用**：向 `POST /v1/applications/{app_id}/invoke` 发起请求，携带认证 Header（`Authorization: Bearer <api_key>`）与 JSON body；
3. **SDK 集成**：使用 `aliyun-openapi-python-sdk` 的 `Bailian` 客户端，调用 `invoke_application(app_id, input)` 方法。

完整调用示例与错误码说明见 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md)。

## 限制和注意事项

- 单应用调用频率上限为 10 QPS（企业版可申请提升），超出将返回 `429 Too Many Requests`；
- 部分应用（如 `web-search-agent`、`tongyi-deepsearch`）依赖外部网络访问，若部署环境无公网出口，需配置代理或启用 VPC 内网通道；
- > **注意**：文档中列出的 `官方应用-伶鹊CCAI-客服对话Agent`（路径 `.../official-application-voicepica-ccai-beebot-agent.md`）与当前控制台实际发布的应用 ID `lingque-ccai-customer-service` 不一致，建议以控制台展示的 ID 为准，该不一致已在 [应用广场](../../raw/application-user-guide/application-gallery.md) 的最新修订版中同步修正；
- 所有应用默认启用内容安全过滤，敏感词拦截策略不可关闭；如需白名单豁免，须提交工单审批。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


