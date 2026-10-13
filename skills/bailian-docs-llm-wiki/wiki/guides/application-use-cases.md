# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的 RAG 架构，通过百炼大模型应用 + AppFlow 低代码连接流实现，无需自行部署模型或维护推理服务。核心流程均为：创建百炼智能体应用 → 配置知识库（可选）→ 在 AppFlow 中关联目标渠道 → 完成渠道侧配置（如 Web 悬浮窗、公众号服务器地址、钉钉机器人 Webhook 等）。

## 支持的模型/功能

- **基础模型**：所有用例默认推荐 `Qwen3.5-Plus`（文档1）或 `千问-Plus`（文档2、3、4），该模型在效果、速度与成本间取得平衡，适用于通用客服问答；也可按需切换为 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（文档3中用于规避微信5秒限制）。
- **RAG 增强**：全部用例均支持通过百炼知识库接入私有文档（PDF/DOCX/TXT 等），支持“必定调用”模式确保关键问题必检索 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **本地 RAG 变体**：除云端标准方案外，还提供完全本地化部署选项，支持自定义文档切分、本地嵌入模型（如 GTE-Chinese-Large）及灵活参数调优，适用于对数据主权或切分逻辑有强定制需求的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档1明确指定模型为 `Qwen3.5-Plus`，而文档2、3、4仅写为 `千问-Plus`。根据百炼控制台最新命名规范，`千问-Plus` 即 `Qwen3.5-Plus` 的别名，二者指向同一模型版本，无实质差异。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源文档 |
|---------|--------|------|----------|
| **认证凭证** | `AppID` / `AgentId` / `Client ID` | 各渠道平台分配的应用唯一标识（微信公众号、企业微信、钉钉） | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| | `API Key` | 百炼平台调用凭证，用于 AppFlow 连接百炼应用 | 全部文档（1–4） |
| | `应用ID` | 百炼中创建的智能体应用唯一 ID | 全部文档（1–4） |
| **RAG 控制** | `调用方式` | 知识库调用策略，推荐设为 `必定调用` 以保障私域问题响应 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| | `相似度阈值` | 控制知识检索结果过滤强度，值越高返回片段越少但更精准 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **性能优化** | `温度（temperature）` | 控制生成随机性，客服场景建议设为 `0.1–0.3` 保证回答稳定 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `最大回复长度` | 限制 token 输出量，微信未认证号需 ≤5秒响应，建议调低 | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) |

## 使用方式

1. **创建百炼智能体应用**：进入[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），选择模型，发布应用。
2. **获取凭证**：从[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)复制应用ID，从[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建并复制 API Key。
3. **配置知识库（可选但推荐）**：上传文档至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)，在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)创建并关联至应用，设置调用方式为“必定调用”。
4. **在 AppFlow 创建连接流**：
   - 选择对应渠道模板（如“企业微信自建应用大模型自动回复”）；
   - 分步配置渠道凭证（微信 AppID/Secret、企业微信 AgentId/Secret、钉钉 Client ID/Secret）和百炼凭证（API Key + 应用ID）；
   - 获取并保存生成的 `WebhookUrl`（企业微信/钉钉/公众号）或 `悬浮挂件部署脚本`（网站）。
5. **完成渠道侧配置**：
   - **网站**：将悬浮脚本插入 HTML `<head>` 或 `<body>` 底部；
   - **微信公众号**：在[公众号后台 > 开发 > 基本配置](https://mp.weixin.qq.com/)填写 `WebhookUrl`、Token、EncodingAESKey，并配置可信 IP；
   - **企业微信**：在应用详情页“设置API接收消息”中填入 `WebhookUrl`、Token、EncodingAESKey，并在“企业可信IP”中添加 AppFlow 提供的白名单 IP；
   - **钉钉**：在应用详情页“添加应用能力 > 机器人”中启用 HTTP 模式，填入 `WebhookUrl`。

## 限制和注意事项

- **免费额度**：新用户可使用百炼[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)覆盖初期调用，额度耗尽后按 token 计费；AppFlow、函数计算 FC、ADB-PG 等依赖云产品单独计费。
- **微信认证限制**：未认证公众号仅支持被动回复，响应超时（>5秒）即失败；文档3明确建议“完成微信认证”或改用 `qwen-turbo` 加快响应 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **域名与安全**：企业微信/微信公众号配置 Webhook 时若遇“域名主体校验未通过”，必须配置自有备案域名或通过 AppFlow Nginx 代理解决，不可跳过 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **钉钉模式限制**：钉钉机器人仅支持 HTTP 模式，**严禁选择 Stream 模式**，否则消息无法返回 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。
- **本地 RAG 注意事项**：本地部署方案要求 Python 3.9–3.12，大文件（>100MB）可能导致知识库创建超时；嵌入模型若切换为本地，需手动修改 `chat.py` 和 `create_kb.py` 中的注释代码块。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


