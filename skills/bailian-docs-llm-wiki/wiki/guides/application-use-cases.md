# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可快速将智能问答能力嵌入网站、微信公众号、企业微信、钉钉等主流渠道，无需从零搭建模型服务或维护向量数据库。所有方案均基于百炼托管的模型 API 和 AppFlow 可视化编排能力实现，兼顾开发效率与生产可控性。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）、`千问-Plus`（文档 2、3、4 中统一命名），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（高吞吐）等变体，具体见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的参数说明。
- **核心功能**：
  - 智能体（Agent）应用：支持 Prompt 角色设定（如“你叫小助…”）、多轮对话管理；
  - RAG 知识增强：通过百炼知识库或本地知识库接入私有文档（PDF/DOCX/TXT/Excel 等），支持全文引用、切片检索、自定义处理三种模式；
  - 多端集成：提供 Web 悬浮挂件、微信公众号消息流、企业微信应用、钉钉机器人四种开箱即用的集成路径。

> **注意**：文档 1 中模型名称写作 `Qwen3.5-Plus`，而文档 2–4 统一写作 `千问-Plus`。二者实为同一模型（Qwen3.5-Plus 是其新版命名），但控制台 UI 显示可能存在滞后。建议以百炼控制台实际下拉选项为准，避免硬编码模型名。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源参考 |
|----------|--------|------|----------|
| **认证凭证** | `AppID` / `Application ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| | `API Key` | 百炼调用密钥，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面创建 | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) |
| **RAG 配置** | `调用方式` | 知识库调用策略，推荐设为 `必定调用` 以确保私有知识生效 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| | `相似度阈值` / `召回片段数` | 控制知识检索精度与范围，影响回答相关性与长度 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **模型推理** | `temperature` | 控制输出随机性（0–2），客服场景建议设为 0.1–0.5 保证稳定性 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建**智能体应用** → 选择模型（如 `Qwen3.5-Plus`）→ 配置 Prompt → 发布；
2. **准备私有知识（可选但推荐）**：
   - 云端方案：上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) → 创建[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 在应用配置中启用并设为 `必定调用`；
   - 本地方案：使用 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 提供的 CLI 工具，支持结构化/非结构化数据上传与自定义切分；
3. **选择集成渠道并配置 AppFlow**：
   - **网站**：AppFlow → 模型服务 AI 助手 → 创建助手 → 导入百炼应用 → Web 页面集成 → 获取悬浮挂件脚本并嵌入 HTML；
   - **微信公众号**：AppFlow → 使用预置模板 → 授权公众号凭证 → 配置百炼应用 ID 与 API Key → 发布；
   - **企业微信/钉钉**：AppFlow → 使用对应模板 → 配置企业微信 AgentId/Secret 或钉钉 Client ID/Secret → 关联百炼应用 → 获取 WebhookUrl → 在企业微信/钉钉后台完成 API 接收配置；
4. **验证与日志**：通过前端界面或聊天窗口测试；如需分析对话，可在 AppFlow 连接流中添加 SLS 日志节点记录上下文。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费；
- **文件限制**：
  - 云端知识库：单文档 ≤ 100 MB 或 1000 页，支持格式包括 PDF/DOCX/TXT/XLSX/PNG/JPG 等（文档 3 明确列出）；
  - 本地 RAG 应用：不建议上传 > 100 MB 文件，受限于 Embedding API 限流（文档 5）；
- **微信认证要求**：未认证公众号仅支持被动回复（5 秒超时限制），若需稳定响应，必须完成微信认证并使用对应工作流（文档 2）；
- **可信 IP 与域名**：企业微信/钉钉要求配置可信 IP；企业微信还可能报“域名主体校验未通过”，需通过 AppFlow 域名管理或 Nginx 代理解决（文档 3）；
- **调试提示**：出现 `Failed to stream content` 或 `request error` 时，优先检查三项是否一致且有效：① 百炼应用 ID、② API Key、③ 所属业务空间（AgentKey）——三者必须同属一个百炼业务空间（文档 1）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


