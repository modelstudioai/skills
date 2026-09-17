# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可快速将智能问答能力嵌入网站、微信公众号、企业微信、钉钉等主流渠道，无需从零训练或部署模型。所有方案均基于百炼托管的推理服务与 AppFlow 的可视化编排能力，兼顾开发效率与生产可控性。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 中统一表述），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景。  
- **高级模型选项**：本地 RAG 方案（文档 5）额外支持 `qwen-max`（高精度）、`qwen-turbo`（低延迟）及 `qwen-plus`，开发者可根据响应时延与质量要求动态切换 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **核心功能**：  
  - 智能体（Agent）应用：支持 Prompt 角色设定（如“你叫小助，解答产品选购问题”）、多轮对话管理；  
  - RAG 增强：通过知识库关联实现私有文档检索，支持文件上传、切片策略配置、相似度阈值调整；  
  - 多端集成：提供 Web 悬浮挂件、微信公众号消息流、企业微信 API 接收、钉钉机器人 HTTP 回调四类标准化接入路径。

> **注意**：文档 1 中模型名称为 `Qwen3.5-Plus`，而文档 2、3、4 均写作 `千问-Plus`。二者实为同一模型（Qwen3.5-Plus 是其新版命名），但文档表述不一致易引发混淆，建议以控制台实际下拉选项为准，避免硬编码模型名。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制生成随机性，值越高越发散 | 本地 RAG 方案中通过 UI 或 `chat.py` 修改 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `max_tokens` | 限制回复最大 token 数 | 同上 |
| | `top_p` / `top_k` | 影响采样范围 | 同上 |
| **RAG 层** | `retrieval_top_k` | 召回片段数，默认 3–5 | 同上；云端方案在知识库引用配置页设置 |
| | `similarity_threshold` | 相似度过滤阈值（0–1），0 表示不过滤 | 同上；云端方案在知识库引用配置页设置 |
| **集成层** | `AgentKey`（业务空间标识） | 用于百炼 API 鉴权，必须与 API Key 所属空间一致 | AppFlow 模型配置页，见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 常见问题排查项 |

## 使用方式

1. **创建百炼应用**：进入[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择**智能体应用**，配置模型（`Qwen3.5-Plus`/`千问-Plus`）与 Prompt，发布后获取 **App ID**；  
2. **获取凭证**：在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 **API Key**；  
3. **集成到目标平台**：  
   - **网站**：通过 AppFlow 创建 AI 助手 → 配置 Web 集成 → 复制悬浮挂件脚本插入 HTML；  
   - **微信公众号**：使用 AppFlow 微信模板 → 授权公众号 → 绑定百炼 App ID 与 API Key；  
   - **企业微信/钉钉**：先创建对应平台应用（获取 AgentId/Client ID 等）→ 使用 AppFlow 模板绑定 → 配置 Webhook URL 与可信 IP；  
4. **增强知识**：上传文档至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) → 创建[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 在百炼应用中启用“必定调用”并发布。

## 限制和注意事项

- **免费额度覆盖范围**：新用户免费额度可覆盖网站、微信、企业微信、钉钉四类场景的初期调用，但 AppFlow、函数计算 FC、ADB-PG 向量存储等依赖服务单独计费 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)；  
- **微信认证约束**：未认证公众号仅支持被动回复（5 秒超时限制），若需稳定服务，必须完成微信认证并选用对应工作流 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)；  
- **企业微信/钉钉可信 IP**：企业微信要求白名单 IP 必须归属本企业，若使用第三方服务（如 AppFlow 默认出口 IP），需配置 Nginx 代理或计算巢实例转发 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；  
- **文件限制**：云端知识库单文件 ≤100 MB 或 1000 页，支持格式包括 `.pdf`, `.docx`, `.txt`, `.xlsx` 等；本地 RAG 方案同样不建议上传 >100 MB 文件，以防 Embedding API 限流超时 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)；  
- **调试关键点**：集成失败时优先检查三项一致性——API Key 与 App ID 是否匹配、`AgentKey`（业务空间）是否与 API Key 所属空间一致、Webhook URL 是否被目标平台（如企业微信）校验通过。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


