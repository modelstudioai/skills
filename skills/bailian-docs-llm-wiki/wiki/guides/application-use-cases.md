# application [use cases](use-cases.md)

百炼平台支持多种主流企业通讯与网站场景下的 AI 应用快速落地，核心模式为“大模型应用 + 私有知识增强（RAG）+ 低代码集成”。所有方案均基于统一的百炼智能体应用构建，通过 AppFlow 实现与外部渠道的零代码对接，并可按需扩展本地知识处理能力。典型部署周期在 10 分钟内，新用户可使用[新用户免费额度](raw/model-user-guide/test-1/new-free-quota.md)覆盖初期调用成本。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2、3、5），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未明确支持状态）。
- **核心功能**：
  - 标准大模型问答（LLM inference）
  - [检索增强生成](../concepts/rag.md)（RAG），支持云端知识库（文档 1、2、3、5）与本地知识库（文档 4）
  - 多模态文件解析（PDF/DOCX/TXT/XLSX/CSV/PNG/JPG 等，见[在企业微信中集成一个 AI 助手](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）
  - 对话状态管理（上下文轮数控制，见[基于本地知识库构建RAG应用](raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）

> **注意**：文档 1 明确推荐 `Qwen3.5-Plus`，而文档 2、3、5 均使用 `千问-Plus`。二者为不同版本命名体系，实际对应同一模型系列；当前控制台中 `Qwen3.5-Plus` 为最新稳定版，建议优先选用。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | 温度（temperature） | 控制输出随机性，值域 0–2，默认 0.8 | [基于本地知识库构建RAG应用](raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 中 `chat.py` 或 Web UI |
| | 最大回复长度（max_tokens） | 限制生成 token 数量 | 同上 |
| | 携带上下文轮数 | 控制历史对话参考深度 | 同上 |
| **RAG 层** | 召回片段数（top_k） | 检索返回最相关文本段数量 | 同上 |
| | 相似度阈值（similarity_threshold） | 过滤低相关性检索结果，0 表示不过滤 | 同上；云端知识库中亦可在应用配置页设置 |
| | 文档处理方式 | 全文引用 / 切片检索 / 自定义处理（仅云端） | [在企业微信中集成一个 AI 助手](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 的应用配置 → 文件处理区域 |

## 使用方式

1. **创建百炼智能体应用**  
   进入[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择**智能体应用**，配置模型（推荐 `Qwen3.5-Plus`）、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。

2. **获取凭证**  
   - 应用 ID：在应用列表页复制  
   - API Key：在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建并保存  

3. **集成至目标渠道**（三选一）  
   - **网站嵌入**：使用 AppFlow 创建 AI 助手 → 配置 Web 页面集成 → 获取悬浮挂件脚本 → 插入 HTML（见[在网站上增加一个AI助手](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）  
   - **微信公众号**：使用 AppFlow 微信模板 → 授权公众号 → 绑定百炼应用 → 发布（见[10分钟让微信公众号成为智能客服](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）  
   - **企业微信/钉钉**：创建对应平台应用 → 获取平台凭证（AgentId/Secret 或 Client ID/Secret）→ 在 AppFlow 中配置连接流 → 配置 Webhook 或机器人接收地址（见[在企业微信中集成一个 AI 助手](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 和 [在钉钉上增加一个AI机器人](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）  

4. **增强私有知识（RAG）**  
   - **云端方案**：上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) → 创建[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 在应用配置中启用并设为“必定调用”  
   - **本地方案**：运行 `local_rag` 示例（见[基于本地知识库构建RAG应用](raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)），支持自定义切分、嵌入模型与向量存储  

## 限制和注意事项

- **免费额度限制**：新用户额度覆盖模型调用，但 AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费（见[在网站上增加一个AI助手](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）  
- **文件上传限制**：云端知识库单文件 ≤100 MB 或 1000 页；本地 RAG 示例建议 ≤100 MB（见[基于本地知识库构建RAG应用](raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）  
- **微信认证约束**：未认证公众号受 5 秒响应限制，超时将无法回复；建议完成认证后使用对应工作流（见[10分钟让微信公众号成为智能客服](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）  
- **企业微信/钉钉可信 IP**：平台强制要求配置可信 IP，若使用 AppFlow Webhook 直连可能失败；需通过内网代理（ECS/Nginx）或计算巢 Nginx 实例转发（见[在企业微信中集成一个 AI 助手](raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）  
- **调试与日志**：所有 AppFlow 连接流均支持添加 SLS 日志节点记录对话（见文档 2、3、5 的“记录 AI 助理对话日志”章节），便于问题排查与效果分析

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


