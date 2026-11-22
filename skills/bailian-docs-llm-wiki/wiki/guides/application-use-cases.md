# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等私域触点，以及本地化部署的 RAG 应用场景。所有方案均基于统一的百炼大模型应用能力，通过 AppFlow 实现零代码连接，结合知识库（RAG）增强实现专业、准确的领域问答。核心流程高度一致：创建百炼智能体应用 → 配置模型与 Prompt → 关联外部渠道 → 可选接入私有知识库 → 发布并验证。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指出其“能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间”），也支持 `qwen-max`、`qwen3.5-flash` 等商业模型（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **核心功能**：
  - 智能体（Agent）应用：支持多步推理、工具调用（如知识库检索）、状态管理；
  - RAG 增强：通过知识库（标准版/ADB-PG）实现私有文档精准问答；
  - 多端嵌入：提供 Web 悬浮挂件、企业微信自建应用、微信公众号客服、钉钉机器人四种开箱即用的集成形态；
  - 本地 RAG：支持在用户本地环境运行检索模块，仅将生成请求发往百炼 API，满足数据不出域需求（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档 1、2、3、4 均将 `千问-Plus` 作为默认模型，但文档 1 的截图和文字描述中出现 `Qwen3.5-Plus`，而其余三篇仅写 `千问-Plus`。根据百炼控制台最新命名规范及文档 1 的明确说明，应以 `Qwen3.5-Plus` 为准；`千问-Plus` 为旧称或简写，实际指代同一模型。

## 关键参数

| 参数 | 说明 | 来源示例 |
|------|------|----------|
| **应用 ID** | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取，用于关联外部渠道 | 所有 5 篇文档均要求配置此参数 |
| **API Key** | 百炼服务调用凭证，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面创建，需与应用 ID 同属一个业务空间 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中强调“确认智能体与 API Key 在同一业务空间” |
| **Prompt** | 定义模型角色与行为，例如 `"你叫小助，可以帮助用户解答产品选购、使用等方面的问题。"`，直接影响回答风格与准确性 | 文档 1、2、3 均提供该 Prompt 示例 |
| **知识库调用方式** | 控制 RAG 触发逻辑，可选 `必定调用`（强制检索）、`按需调用`（模型自主判断）等 | 文档 1、2、3、4 均在知识库引用步骤中指定 `必定调用` |
| **召回片段数 / 相似度阈值** | 本地 RAG 场景下可调参，影响检索精度与生成质量 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 明确列出此参数 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 配置 Prompt → 发布。
2. **获取凭证**：记录应用 ID 和 API Key（确保二者在同一业务空间）。
3. **选择集成渠道**：
   - **网站**：通过 AppFlow 创建 AI 助手 → 导入百炼应用 → 配置 Web 集成 → 获取悬浮挂件脚本 → 插入 HTML。
   - **企业微信/微信公众号/钉钉**：在对应平台创建应用（获取 AppID/AgentID/Client ID 等）→ 使用 AppFlow 预置模板创建连接流 → 分别配置平台凭证与百炼凭证 → 获取 Webhook URL → 在平台后台完成消息接收配置（含 [Token](../concepts/token.md)、EncodingAESKey、可信 IP 等）。
   - **本地 RAG**：下载 `local_rag.zip` → 配置 Python 环境与 API Key → 运行 `uvicorn main:app --port 7866` → 通过 Gradio 界面上传文件、创建知识库、发起问答。
4. **添加私有知识（可选但推荐）**：上传文档（PDF/DOCX/TXT 等）→ 创建知识库 → 在百炼应用中引用该知识库 → 重新发布应用。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费。
- **认证要求**：
  - 微信公众号：未认证账号仅支持被动回复（5 秒超时限制），已认证账号支持主动客服接口（见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）。
  - 企业微信/钉钉：需确保应用具备相应权限（如企业微信需配置可信 IP，钉钉需开通 `Card.Streaming.Write` 权限）。
- **安全与合规**：
  - 企业微信域名主体校验失败时，必须配置自有备案域名或通过 Nginx 代理解决（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。
  - 钉钉机器人**必须**选择 HTTP 模式，Stream 模式不兼容（见 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）。
- **调试与日志**：
  - 所有渠道均支持在 AppFlow 中添加 SLS 日志节点记录对话（文档 2、3、4 均提供详细步骤）。
  - 嵌入网站后若出现 `request error`，需按顺序检查 API Key 状态、业务空间一致性、应用 ID 正确性（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


