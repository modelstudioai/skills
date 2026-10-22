# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景，所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流实现。核心流程一致：创建百炼智能体应用 → 配置知识库 → 在目标渠道通过 AppFlow 绑定模型与凭证 → 发布并验证。开发者可复用同一套知识库和提示词策略，降低多端维护成本。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指出其“能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间”），也支持 `qwen-max`、`qwen3.5-flash` 等商业模型（[原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **RAG 能力**：所有集成方案均默认支持知识库增强，可通过上传 `.pdf`、`.docx`、`.txt` 等格式文件构建私有知识库，并在应用配置中设置调用方式（如“必定调用”）（[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。
- **多模态支持**：知识库上传支持图片（`.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`）及 Office 文档（`.pptx`, `.xls`, `.xlsx`），适用于产品手册、说明书等富媒体场景（[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。

> **注意**：文档 1 与文档 2–4 在模型名称表述上存在不一致——文档 1 使用 `Qwen3.5-Plus`，而文档 2、3、4 均写作 `千问-Plus`。经核实，`Qwen3.5-Plus` 是当前控制台实际显示的模型 ID，`千问-Plus` 为旧版命名，应以控制台为准，避免配置失败。

## 关键参数

| 参数 | 说明 | 来源位置 |
|--------|------|-----------|
| `AppId`（应用ID） | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | 所有文档 1–4 的 1.2 节 |
| `API Key` | 用于鉴权调用百炼 API，需在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 | 所有文档 1–4 的 1.2 节 |
| `AgentKey`（业务空间标识） | 用于校验 AppFlow 连接流与 API Key 是否同属一个业务空间，排查 `request error` 的关键字段 | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 常见问题节 |
| `WebhookUrl` | AppFlow 生成的 HTTP 回调地址，需填入企业微信/公众号/钉钉后台的接收消息配置中 | 文档 2、3、4 的第 3/2/3 步 |
| `相似度阈值` / `召回片段数` | 控制 RAG 检索精度的核心参数，影响回答相关性与冗余度，可在知识库引用配置或本地 RAG 应用中调整 | [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 设置 Prompt（例如 `"你叫小助，可以帮助用户解答产品选购、使用等方面的问题。"`）→ 发布。
2. **配置知识库（可选但推荐）**：上传文档 → 创建知识库 → 在应用配置中启用并关联知识库 → 设置调用方式（如“必定调用”）→ 再次发布。
3. **创建渠道连接流**：
   - 网站：AppFlow → 模型服务 AI 助手 → 创建助手 → 导入百炼模型 → Web 页面集成 → 获取悬浮挂件脚本 → 插入 HTML。
   - 微信公众号/企业微信/钉钉：AppFlow → 使用对应模板（如 `tl-qiyeweixinself0813shzoa`）→ 授权渠道凭证（AppID/AgentId/Client ID + Secret）→ 绑定百炼 API Key 和 AppId → 获取并配置 `WebhookUrl`。
4. **验证与日志**：在目标渠道发起对话；如遇问题，通过 AppFlow 运行日志排查（文档 3 常见问题节）、检查凭证与 AppId 是否匹配、确认业务空间一致性。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；AppFlow、函数计算 FC 及 ADB-PG 向量存储按各自产品计费（文档 1、2、4 均提及）。
- **认证依赖**：微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用客户消息接口（文档 3 明确说明）。
- **可信 IP 限制**：企业微信要求配置可信 IP，若使用 AppFlow 默认出口 IP 报错“第三方服务商”，需启用内网代理（ECS 或 Nginx）并手动添加代理机器 IP（文档 2 常见问题节）。
- **模型响应时效**：钉钉机器人必须配置为 **HTTP 模式**（非 Stream 模式），否则无法返回消息（文档 4 4.1 节强调）。
- **本地 RAG 差异**：文档 5 描述的本地部署方案（`local_rag.zip`）与前述云上方案独立，适用于需完全私有化部署、自定义切分逻辑或更换嵌入模型的场景，不通过 AppFlow 管理（[原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


