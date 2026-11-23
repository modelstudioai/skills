# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级渠道的 AI 助手/机器人快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流 + 可选私有知识库实现端到端交付，面向开发者提供标准化接入路径与可复用的配置范式。

## 支持的模型/功能

- **核心模型**：默认推荐 `Qwen3.5-Plus`（文档1）、`千问-Plus`（文档2、3、5），该模型在效果、速度与成本间取得平衡；也可按需切换为 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（文档3中用于规避微信5秒限制）。
- **关键能力**：
  - 全链路 RAG 支持：知识上传 → 向量索引 → 检索调用 → 生成增强；
  - 多模态文件解析：支持 PDF、DOCX、TXT、XLSX、PPTX、PNG/JPG 等（文档2明确列出格式及单文件≤100MB限制）；
  - 可视化 Prompt 编排：可在百炼应用配置页直接设置角色指令（如“你叫小助，帮助解答产品选购问题”）；
  - 本地知识库扩展：除云端知识库外，还支持[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)，适用于对数据主权或切分策略有强定制需求的场景。

> **注意**：文档1中称模型为“Qwen3.5-Plus”，而文档2/3/5统一使用“千问-Plus”。经核对百炼控制台当前模型列表，“千问-Plus”即 `qwen-plus`，与 `Qwen3.5-Plus` 为同一模型的不同命名方式，属术语不一致，非功能差异。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|-----------|
| **模型层** | `temperature` | 控制输出随机性，值越高越发散（文档4） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `max_tokens` | 限制生成长度，影响响应简洁性（文档4） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `top_p` / `top_k` | 影响采样多样性（文档4未显式配置但属标准参数） | — |
| **RAG层** | `retrieval_top_k` | 召回片段数，直接影响上下文信息量（文档4） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `similarity_threshold` | 相似度阈值，用于过滤低相关片段（文档4） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `knowledge_call_mode` | 知识调用方式，如“必定调用”（文档1/3/5）或“按需调用”（文档2提及但未展开） | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |

## 使用方式

1. **统一前置步骤**：
   - 在百炼控制台创建**智能体应用**，选择模型、配置 Prompt 并发布；
   - 获取该应用的 `AppID` 与 `API Key`（所有文档均要求此操作，路径一致：`应用管理` → `API Key` 页面）；
2. **渠道侧集成**：
   - **网站嵌入**：通过 AppFlow 创建 AI 助手 → 配置 Web 集成 → 复制悬浮挂件脚本插入 HTML（文档1）；
   - **微信公众号**：使用 AppFlow 微信模板 → 授权公众号凭证 → 配置应用 ID → 发布（文档3）；
   - **企业微信/钉钉**：创建对应平台应用 → 获取平台凭证（CorpID/AgentID/Secret 或 ClientID/Secret）→ 在 AppFlow 中关联百炼应用（文档2、5）；
3. **知识增强（可选）**：
   - 上传文件至百炼「数据连接」或「文件」页签；
   - 在「知识库」页面创建知识库并绑定文件；
   - 在目标百炼应用的「知识库」配置中启用并设为“必定调用”（文档1/2/3/5流程一致）。

## 限制和注意事项

- **免费额度适用性**：新用户免费额度覆盖所有渠道方案的模型调用（文档1/2/5均强调），但 AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费（文档1明确说明）；
- **微信认证约束**：未认证公众号仅支持被动回复，且响应必须 ≤5 秒；超时将失败（文档3）。建议完成认证或改用 `qwen-turbo` 加速响应；
- **可信 IP 与域名校验**：
  - 企业微信要求配置可信 IP，若使用第三方服务（如 AppFlow 默认出口 IP）会报错“属于第三方服务商”（文档2）；
  - 微信公众号配置服务器时若提示“URL存在严重安全风险”，需通过服务商授权或自建 Nginx 代理解决（文档3）；
- **知识库文件限制**：单文档最大 100MB 或 1000 页，图片单张 ≤20MB，最多上传 200 个文件（文档2明确）；
- **本地 RAG 特殊要求**：Python 版本需 ≥3.9 且 ≤3.12；Windows 用户需额外安装 `msvc-runtime`（文档4）；
- **钉钉机器人模式**：必须选择 **HTTP 模式**，Stream 模式不兼容 AppFlow（文档5强调）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


