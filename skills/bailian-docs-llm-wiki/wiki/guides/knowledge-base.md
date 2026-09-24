# knowledge base

阿里云百炼知识库（RAG Knowledge Base）是面向企业级场景的[检索增强生成](../concepts/rag.md)（RAG）基础设施，提供文档解析、切片、向量化、多模态索引构建及联合检索能力。它支持通过控制台、CLI、REST API、MCP 协议等多种方式接入，并可与 Agent、Dify、Coze 等主流 AI 平台深度集成。所有知识库运行于业务空间（workspace）隔离环境中，按规格（标准版/旗舰版）和模型调用分别计费。

## 支持的模型与功能

- **嵌入模型**：默认使用 `text-embedding-v4`（中英文通用），创建知识库时选定且不可更改；支持自定义选择，详见[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **重排（Rerank）模型**：支持 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）等系列模型，在[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)或[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)的服务配置中启用；若关闭排序模型，则仅返回原始召回结果。
- **生成模型**：问答服务支持 Qwen 系列（如 `qwen3.6-plus`）、DeepSeek 等大模型，可在调试窗口实时切换对比效果，见[Playground](raw/application-user-guide/knowledge-base/playground.md)。
- **核心功能**：
  - 多源数据接入（文件、表格、数据库、OSS、飞书、钉钉、语雀、SharePoint）；
  - 智能切片（智能切分/按长度/按页/按标题等六种策略）；
  - 标签过滤、元数据抽取、Query 改写、多知识库路由与混排；
  - 静态注入（`on_system_prompt`）与自主调用（`list_tools`）双模式接入 AgentScope；
  - 全链路日志投递至 SLS，支持审计、监控与用量分析，详见[知识库日志与监控](raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)。

> **注意**：文档 24（`rag-knowledge-base-api-guide.md`）明确指出“知识库相关功能在中国站仅支持**华北2（北京）**地域”，而文档 27（`rag-knowledge-retrieval.md`）示例中使用的 endpoint 域名为 `cn-beijing.maas.aliyuncs.com`，二者一致；但文档 21（`quickstart.md`）未声明地域限制，实际部署需以文档 24 为准。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **切片** | 最大分段长度 | 10–6000 token | 默认 600；在[导入数据](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)时配置，创建后不可改 |
| **检索** | 初步向量/关键词 TopK | 1–100 | 各知识库独立配置，影响召回广度 |
| **检索** | 最大召回数量 | 1–20 | 全局或单库生效；问答服务最大为 20，见[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) |
| **检索** | 相似度阈值 | 0.01–1.0 | 过滤低分切片，值越高越严格 |
| **服务** | RCU（旗舰版） | 1–200 | 1 RCU ≈ 支撑 50 QPS；按需变配，1 日限 1 次，见[知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md) |
| **标签** | 单标签长度 | ≤32 字符 | 仅支持中文、英文字母、数字、`_`、`-`；多值需拆分为多个字符串 |

## 使用方式

### 1. 控制台快速验证  
- 在 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground) 中选择知识库，切换「知识问答」或「知识检索」模式，输入问题实时查看召回切片与模型回答。  
- 通过 [知识管理 → 文档列表 → 切片详情](raw/application-user-guide/knowledge-base/data-connection-overview/documents.md) 人工抽检并修正切片内容。

### 2. API 集成  
- **底层检索**（单库）：`POST /api/v1/indices/rag/index/retrieve`，需传 `index_id`、`query`、`top_k`；不触发重排。  
- **应用级检索**（多库联合）：`POST /api/v1/indices/knowledge/search`，传 `query` 和 `agent_id`，由检索服务配置驱动路由、混排与权重。  
- **流式问答**：`POST /api/v2/apps/knowledge/chat`，支持 SSE，需携带 `agent_options.agent_id`。  
- 完整接口规范见 [API 参考](raw/application-api-reference/rag-api/rag-api-overview.md)。

### 3. CLI 与 SDK  
- CLI 命令：`bl knowledge search --query "xxx" --agent-id <aid-xxx>`（推荐）；`bl knowledge retrieve` 已弃用（见文档 9）。  
- Python SDK：需安装 `alibabacloud_bailian20231229`，配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 等环境变量（见文档 24）。

### 4. 第三方平台接入  
- **Agent**：通过 MCP Server 或 Skill 包（如 Claude Code、Qoder），需配置 `DASHSCOPE_API_KEY`（见文档 6 和文档 8）。  
- **Dify/Coze/n8n**：使用 DashScope Endpoint + API Key + 知识库 ID 配置外部知识源（见文档 7）。  
- **AgentScope**：编写自定义中间件 `KnowledgeStudioRAGMiddleware`，支持 `static`（注入 system [prompt](prompt.md)）与 `agentic`（暴露 `search_knowledge` 工具）双模式（见文档 22）。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站（华北2 北京）和国际站（新加坡）可用，其他地域（如德国法兰克福）不支持（见文档 24）。
- **容量上限**：单业务空间最多 50 个知识库、单知识库最多 100,000 个文档；单次上传限 50 个文件；切片最大长度 6000 字符（见文档 26）。
- **计费关键点**：  
  - 免费额度（720 小时）**仅抵扣标准版规格费用**，不覆盖模型调用或旗舰版费用（见文档 4）；  
  - 删除知识库将**永久清除数据且无法恢复**，并立即停止计费；  
  - 若使用自购 ADB-PG 作为向量存储，需额外支付 ADB-PG 费用（见文档 4）。
- **同步行为**：OSS/飞书/钉钉等来源的定时同步基于**文件副本机制**，源文件删除不影响百炼平台内副本（见文档 25）。
- **切片不可变**：切片方式与最大分段长度在导入时锁定，后续无法修改，需重新创建知识库（见文档 18 和文档 26）。

## 来源文档

- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)


