# application [use cases](use-cases.md)

阿里云百炼平台支持将大模型能力快速集成到主流企业通讯与服务平台中，构建面向业务场景的 AI 助手。当前已验证的典型用例覆盖企业微信、钉钉、微信公众号和网站四大渠道，均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过 AppFlow 无代码连接流实现消息路由与服务编排。所有方案均支持私有知识注入、对话日志记录与效果评测闭环，适用于客服应答、内部知识助手、销售支持等高频场景。

## 支持的模型/功能

- **核心模型**：推荐使用 `qwen-plus`（文档 1、3、4）或 `qwen3.5-plus`（文档 2），二者在效果、速度与成本间取得平衡；`qwen-max` 适用于高精度需求，`qwen3.5-flash` 适用于低延迟场景（文档 5）。  
- **RAG 能力**：所有用例均依赖知识库检索增强，支持 `.pdf`, `.docx`, `.txt`, `.xlsx` 等格式（单文件 ≤100 MB），默认采用“文档智能解析”切分策略（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。  
- **扩展功能**：支持卡片消息（钉钉）、悬浮挂件（网站）、公众号被动/主动回复（认证/未认证公众号）、对话日志写入 SLS（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）等。

> **注意**：文档 1 与文档 2 对默认模型的描述存在差异——文档 1 推荐 `qwen-plus`，文档 2 明确推荐 `qwen3.5-plus`。实际部署时请以控制台最新模型列表为准，并优先测试 `qwen-plus` 或 `qwen3.5-plus` 的推理稳定性与响应时延。

## 关键参数

| 参数 | 说明 | 取值建议 | 来源 |
|------|------|----------|------|
| `应用ID` | 百炼应用唯一标识 | 在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面复制，注意去除首尾空格（[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)） | 文档 1、2、3、4 |
| `API Key` | 百炼 API 认证凭证 | 创建后需保存，且必须与应用处于同一业务空间（文档 2 常见问题明确指出跨空间会导致鉴权失败） | 文档 1、2、3、4 |
| `知识库调用方式` | 控制知识检索触发逻辑 | 生产环境建议设为 `必定调用`，避免漏检关键私域信息 | 文档 1、2、3、4 |
| `相似度阈值` | 过滤低相关性检索片段 | 默认 0（不过滤），建议生产环境设为 0.3–0.6，平衡召回率与噪声 | 文档 5 |
| `召回片段数` | 检索返回给 LLM 的文本段数量 | 默认 3，若知识库结构复杂可增至 5；过高易引入干扰信息 | 文档 5 |

## 使用方式

1. **创建百炼应用**：进入[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），发布前务必测试基础问答能力。  
2. **准备私有知识**：上传文档至百炼[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)或[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)页签，再于[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)中创建并关联。  
3. **配置目标平台**：  
   - **企业微信/钉钉/公众号**：在对应开放平台创建应用，获取 `CorpID/AgentID/ClientID/AppID` 等凭证；  
   - **网站**：直接使用 AppFlow 的“模型服务AI助手”功能创建 Web 集成，无需独立平台应用。  
4. **构建连接流**：  
   - 企业微信/钉钉/公众号：使用预置 AppFlow 模板（链接见各文档），按向导配置企业凭证 + 百炼 API Key + 应用ID；  
   - 网站：在 AppFlow “模型服务AI助手” 中导入百炼模型，配置 Web 集成参数（字体、颜色、预置问题等）；  
   - 本地 RAG：运行 `local_rag` 示例（文档 5），通过 Gradio UI 或 API 调用，支持自定义嵌入模型与切分逻辑。  
5. **发布与验证**：完成配置后发布连接流或 Web 集成，通过平台内测（如企业微信搜索应用、钉钉群 @ 机器人、公众号发送消息）验证端到端链路。

## 限制和注意事项

- **平台认证要求**：微信公众号未认证时仅支持被动回复（5 秒超时限制），必须完成认证才能启用客户消息接口（文档 4）；企业微信/钉钉需确保开发者权限已开通（文档 3）。  
- **IP 白名单**：企业微信/钉钉要求配置可信 IP，AppFlow 提供计算巢 Nginx 代理或自有 ECS 代理方案解决第三方 IP 限制（文档 1 常见问题）。  
- **知识库时效性**：上传文档后需等待 1–6 分钟完成解析（文档 1、2、3、4 均明确提示），期间知识库不可用。  
- **本地 RAG 限制**：`local_rag` 示例（文档 5）依赖 Python 3.9–3.12，Windows 用户需额外安装 `msvc-runtime`，且 Embedding API 有流控，单文件不宜超过 100 MB。  
- **错误排查重点**：若出现 `request error` 或无响应，优先检查三项：API Key 状态、应用 ID 与 API Key 是否同属一个业务空间、Webhook URL 是否被正确填入目标平台（文档 2 常见问题）。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


