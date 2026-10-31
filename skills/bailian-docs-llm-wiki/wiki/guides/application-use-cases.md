# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景，所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 无代码连接流实现。核心流程一致：创建百炼智能体应用 → 配置知识库 → 在目标渠道通过 AppFlow 绑定并发布。开发者可复用同一套模型配置与知识资产，降低多端部署成本。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指出其“能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间”），也支持 `qwen-max`、`qwen3.5-flash` 等商业模型（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。  
- **核心功能**：  
  - 全天候 7×24 客户咨询响应；  
  - 私有知识问答（RAG），支持 PDF/DOCX/TXT/Excel 等格式上传与向量化；  
  - 多端 UI 集成（悬浮挂件、公众号消息、企业微信应用、钉钉机器人卡片）；  
  - 对话日志记录（通过 AppFlow 集成 SLS 日志服务）[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  

> **注意**：文档 1 与文档 2–4 均推荐 `千问-Plus` 或 `Qwen3.5-Plus`，但文档 5 的本地 RAG 示例中明确列出 `qwen-max`、`qwen-plus`、`qwen3.5-flash` 三者可选，且对性能差异有量化说明（如 `qwen3.5-flash` “生成速度较快，价格较低”）。生产环境应根据延迟与精度要求选择，而非默认 `Plus`。

## 关键参数

| 参数 | 说明 | 取值建议 | 来源 |
|------|------|----------|------|
| **模型温度（temperature）** | 控制生成随机性 | 0.1–0.6（客服场景建议偏低以保证稳定性） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **召回片段数（top_k）** | RAG 检索返回的最相关文本段数量 | 3–5（过多引入噪声，过少信息不足） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **相似度阈值（similarity_threshold）** | 过滤低相关性检索结果 | 0.3–0.7（默认 0，即不过滤；设为 0.5 可提升答案精准度） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **最大回复长度（max_tokens）** | 限制模型输出 token 数 | 512–1024（公众号/钉钉卡片需简短，建议 ≤512） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **创建百炼智能体应用**：  
   - 进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择**智能体应用**；  
   - 模型选 `Qwen3.5-Plus`，Prompt 中明确定义角色与约束（如“请总是给出简短的回答”）；  
   - 发布前务必在右侧调试区验证基础问答能力。  

2. **配置私有知识库**：  
   - 上传文件至 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 或 [文件中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)；  
   - 在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建标准版知识库，引用上传的文件；  
   - 在应用配置页的 **文档** 区域添加知识库，调用方式选 **必定调用**（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。  

3. **渠道集成（以 AppFlow 为核心）**：  
   - **网站**：在 AI 助手 Web 集成页获取悬浮挂件脚本，插入 HTML 即可；  
   - **微信公众号/企业微信/钉钉**：使用对应 AppFlow 模板（如 `tl-qiyeweixinself0813shzoa`），按向导完成凭证（AppID/AgentId/Client ID + API Key）与 Webhook 配置；  
   - 所有渠道均需将百炼应用 ID 与 API Key 分别填入 AppFlow 的模型凭证配置项。  

## 限制和注意事项

- **免费额度与计费**：新用户免费额度可覆盖初期测试（见 [新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)），但 AppFlow、函数计算 FC、ADB-PG 向量存储等依赖云产品单独计费，需单独确认。  
- **认证依赖**：  
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），必须完成认证才能启用客户消息接口；  
  - 企业微信配置 API 接收消息时，若报“域名主体校验未通过”，需配置自有备案域名或通过 AppFlow Nginx 代理解决（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。  
- **安全限制**：  
  - 企业微信要求可信 IP 白名单，若使用第三方服务商 IP 会触发报错，必须通过 ECS 或托管实例代理请求；  
  - 钉钉机器人**必须选择 HTTP 模式**（非 Stream 模式），否则无法返回消息（见 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）。  
- **调试要点**：  
  - 出现 `Failed to stream content` 错误，优先检查前端请求地址是否为实际 Webhook URL（非示例代码中的 `/chat`）；  
  - 对话无响应时，务必查看 AppFlow **运行日志**，常见原因包括应用 ID/Key 错误、IP 白名单未配置、公众号未认证却选用认证模板。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


