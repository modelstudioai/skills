# knowledge base

知识库（Knowledge Base）是阿里云百炼平台 RAG 能力的核心载体，用于组织、索引和检索企业私有文档与结构化数据。它通过解析、切片、向量化与索引构建，将原始内容转化为可被语义检索的向量表示，并支持与大模型协同生成带依据的回答。知识库并非静态存储，而是集数据接入、智能检索、多模态问答与服务编排于一体的动态能力单元。

## 支持的模型与功能

知识库支持多种数据类型与检索模式，对应不同模型与处理链路：

- **数据类型与模型适配**：  
  - *文档知识库*（PDF/Word/Markdown）：默认使用 `text-embedding-v4` 向量模型，检索阶段支持 `qwen3-rerank` 系列重排模型；图文混排场景可选 `Qwen-VL` 解析与 `qwen3-vl-rerank` 混排模型 [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)。  
  - *图片知识库*：依赖多模态 Embedding 模型，支持以图搜图与图文问答。  
  - *音视频知识库*：使用语音转写模型 + 时间戳定位，输出结构化片段。  
  - *数据知识库*（CSV/Excel/RDS）：不使用文本嵌入，而是通过 NL2SQL 模型将自然语言查询转为 SQL 执行。

- **核心功能**：  
  - **知识检索**：返回原始切片列表，支持向量+关键词混合召回、Query 改写、标签过滤与多知识库联合排序。  
  - **知识问答**：在检索基础上调用 Qwen 系列大模型（如 `qwen3.6-plus`），生成带引用标注的自然语言回答，并支持流式响应 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。  
  - **Playground 调试**：提供交互式界面，支持单库/多库问答、模型切换与引用高亮，是验证检索质量与回答效果的首选工具 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)。

> **注意**：文档 5 中提及的“新版 Connector”已替代旧版“数据连接”，但知识库本身仍完全兼容旧版数据集作为数据源；迁移截止时间为 2026 年 9 月 30 日，开发者需在此前完成 [数据连接迁移](../../raw/application-user-guide/overview/reference-overview/migration.md)。

## 关键参数

以下参数直接影响检索精度与性能，需根据场景合理配置：

| 参数 | 取值范围 | 说明 | 配置位置 |
|--------|-----------|------|------------|
| **最大分段长度** | 10–6000 token | 控制单切片大小，影响上下文完整性与召回粒度。FAQ 推荐 256，长报告推荐 2048 [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md) | 创建知识库或导入数据时的索引设置 |
| **初步向量检索 TopK** | 1–100 | 向量检索阶段召回的初始切片数，值过小可能漏召，过大增加重排开销 | 知识检索/问答服务中各知识库的独立配置 |
| **相似度阈值** | 0.01–1.0 | 过滤低相关性切片，值越高结果越精确但可能遗漏答案 | 知识检索/问答服务中各知识库的独立配置 |
| **最大召回数量** | 1–20 | 最终返回给上层（模型或用户）的切片总数 | 全局检索配置或知识库独立配置 |
| **混排模型** | `qwen3-rerank` / `qwen3-vl-rerank` / 不使用 | 对多库召回结果统一精排，纯文本选前者，多模态选后者 | 知识检索服务的全局配置 |

## 使用方式

知识库可通过控制台、API 或 CLI 快速接入：

- **控制台快速启动**：  
  登录控制台 → [知识管理](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list) → 创建知识库（选择“文档搜索”类型与“基础文档问答”场景）→ 上传文件 → 等待状态变为“已就绪” → 进入 [Playground](https://bailian.console.aliyun.com/cn-beijing/rag/playground) 试问 [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)。

- **API 集成**：  
  - *底层检索*（单库）：调用 `/api/v1/indices/rag/index/retrieve`，传入 `index_id` 和 `query`。  
  - *应用级检索*（多库联合）：调用 `/api/v1/indices/knowledge/search`，传入 `agent_id`（对应已发布的检索服务）。  
  - *RAG 问答*：调用 `/api/v2/apps/knowledge/chat`，启用 SSE 流式响应，需在 `parameters.agent_options.agent_id` 中指定问答服务 ID [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。

- **CLI 调试**：  
  ```bash
  # 检索服务调用（推荐）
  bl knowledge search --query "如何配置切片？" --agent-id <检索服务ID>
  # 问答服务调用
  bl knowledge chat --message "切片策略怎么选？" --agent-id <问答服务ID>
  ```
  > **注意**：`bl knowledge retrieve` 命令已被标记为“已弃用”，应改用 `search` 或 `chat` [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)。

## 限制和注意事项

- **地域与权限限制**：知识库功能在中国站仅支持**华北2（北京）**，国际站仅支持**新加坡**；子账号需被授予 `AliyunBailianDataFullAccess` 策略并加入目标业务空间 [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)。

- **容量硬限制**：  
  - 单业务空间最多 50 个知识库，单知识库最多 100,000 个文档。  
  - 单次上传最多 50 个文件，PDF/DOCX 单文件 ≤ 150 MB 或 1000 页，图片单图 ≤ 20 MB [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)。  
  - 切片配置（切片方式、最大分段长度）**创建后不可更改**，需在导入数据时慎重设置。

- **计费与生命周期**：  
  - 自 2026 年 1 月 4 日起正式计费，费用由**规格费**（标准版 0.03 元/小时，旗舰版按 RCU 计费）与**模型调用费**（Embedding/Rerank/QA 模型单独计费）构成。  
  - 免费额度（720 小时）仅抵扣**标准版知识库**的规格费，且老用户额度有效期至 2026 年 2 月 3 日 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。  
  - 删除知识库将**永久清除所有数据且不可恢复**，务必谨慎操作。

- **调试与可观测性**：  
  所有检索请求日志自动投递至 SLS，字段包含 `pipeline_id`（知识库 ID）、`latency`（耗时）、`response_code`（业务码）与 `response_body.data.nodes[]`（召回切片详情），可用于审计、慢查询分析与错误排查 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/knowledge-base/quickstart.md)
- [核心概念](../../raw/application-user-guide/knowledge-base/concepts.md)
- [Playground](../../raw/application-user-guide/knowledge-base/playground.md)
- [数据接入](../../raw/application-user-guide/knowledge-base/data-connection-overview.md)
- [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
- [创建知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)
- [文档管理与解析](../../raw/application-user-guide/knowledge-base/data-connection-overview/documents.md)
- [切片与向量化](../../raw/application-user-guide/knowledge-base/data-connection-overview/chunking.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-sync-guide.md)
- [知识服务](../../raw/application-user-guide/knowledge-base/service.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
- [最佳实践](../../raw/application-user-guide/knowledge-base/best-practices.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/best-practices/rag-optimization.md)
- [多轮对话：正确传递工具调用历史](../../raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)
- [文件自动打标：用大模型生成文档标签](../../raw/application-user-guide/knowledge-base/best-practices/auto-tag.md)
- [接入 AgentScope](../../raw/application-user-guide/knowledge-base/best-practices/knowledge-as-memory.md)
- [应用集成](../../raw/application-user-guide/knowledge-base/integration.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/integration/rag-knowledge-base-api-guide.md)
- [服务渠道](../../raw/application-user-guide/knowledge-base/integration/channels.md)
- [快速配置到 Agent](../../raw/application-user-guide/knowledge-base/integration/agent-cli.md)
- [使用 CLI](../../raw/application-user-guide/knowledge-base/integration/cli.md)
- [参考](../../raw/application-user-guide/knowledge-base/reference.md)
- [第三方平台接入](../../raw/application-user-guide/knowledge-base/integration/third-party.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)
- [容量与限制](../../raw/application-user-guide/knowledge-base/reference/rag-knowledge-base-specifications.md)
- [更新日志](../../raw/application-user-guide/knowledge-base/changelog.md)


