# 检索增强生成

检索增强生成（Retrieval-Augmented Generation, RAG）是一种将外部知识检索与大模型生成相结合的技术范式。在百炼平台中，RAG 通过知识库将私有数据与最新信息注入大模型上下文，使其能够回答特定领域问题，弥补模型训练数据的时效性和覆盖面不足。

## 工作原理

百炼 RAG 的核心链路为：文件解析 → 文档切分 → 向量化 → 落入向量库 → 语义检索召回 → 大模型生成答案。用户提问时，系统先将查询向量化并在向量库中检索语义最相关的文档切片，再将召回的切片作为上下文传递给大模型生成最终回答。

## 在百炼平台中的使用场景

### 智能体应用集成

- **Agent 2.0（推荐）**：知识库作为工具之一，由智能体自主规划调用时机，支持通过标签限定查询范围。
- **Agent 1.0**：知识库检索先行，再决策是否调用其他工具，适用于意图单一、流程固定的简单任务。

两种版本均可在应用编辑页关联知识库，并可单独覆盖相似度阈值与权重。

### 工作流应用

在工作流中拖入「知识库」节点，将输入变量绑定到 `query`，支持「固定选择」或通过 `CodeList` 变量「动态引入」知识库，下游接大模型节点并在提示词中插入 `result` 变量即可完成 RAG 链路。

### 渠道集成

通过 AppFlow 可将基于 RAG 的智能体快速接入网站（悬浮挂件）、微信公众号、钉钉群机器人、企业微信等渠道，10 分钟内即可完成最小可用版本。

### 框架集成

- **LlamaIndex（Python）**：通过 `DashScopeCloudIndex` 对接百炼云端知识库，配合 `DashScopeRerank` 做语义重排，构建端到端 RAG 应用。
- **Spring AI Alibaba（Java）**：通过 `DashScopeDocumentRetriever` 检索百炼知识库切片，结合 `DocumentRetrievalAdvisor` 自动注入上下文。

### API 调用

通过百炼 SDK 调用知识库检索接口（`Retrieve`），前置需授予 `AliyunBailianDataFullAccess` 策略。完整流程为 `ApplyFileUploadLease → AddFile → SubmitIndexJob → Retrieve`。

## 关键参数与配置

以下参数大多在知识库创建时确定，创建后不可修改：

| 参数 | 说明 | 推荐值 |
| --- | --- | --- |
| 向量模型 | 文档向量化模型；视觉理解场景自动使用 `qwen3-vl-embedding` | `text-embedding-v4` |
| 切片方式 | 智能切分、按长度、按页、按标题、按正则、按符号；单切片上限 6000 Token | 智能切分 |
| 排序模型（Rerank） | 对召回结果做二次排序，综合语义 + BM25 | `qwen3-rerank（hybrid）` |
| 排序模式 | 问答模式 / 相似模式 / 自定义高级 | 问答模式 |
| 相似度阈值 | 低于此值的切片不召回；应用侧设置会覆盖知识库默认值 | 视场景而定 |
| 最大召回数量 | 排序后送入大模型的切片数 K，上限 20 | — |
| 向量存储 | 内置（免费）或 ADB-PG（自购计费） | 内置 |

## 知识库类型选择

创建后类型不可更改，需根据数据形态选择：

- **文档搜索**：面向 PDF、Word、Markdown 等非结构化数据，细分为基础文档问答、图文并茂回复、视觉理解（富文本）、极速问答四种场景。
- **数据查询（NL2SQL）**：结构化 Excel / RDS 表，按列控制检索与回复参与。
- **图片问答**：数据表含 `image_url` 字段，实现以图搜图。
- **音视频搜索**：按时间轴对齐语音识别 + 视频帧提取 + 剧情解析。

## Rerank 配置注意事项

Rerank 开关位置因调用方式而异，配置错误可能产生非预期费用：

- **旧版智能体 / 工作流**：应用内配置优先级高于知识库本身。
- **Agent 2.0**：以知识库自身配置为准。
- **OpenAPI**：API 参数优先级高于控制台配置。

## 效果优化要点

当出现召回不全或回答不准时，可从以下方向调优：

1. **数据质量**：优化文档切分策略，确保切片语义完整。
2. **检索参数**：调整相似度阈值、召回数量、排序模式。
3. **Rerank 策略**：启用排序模型提升召回精度。
4. **Prompt 设计**：在应用提示词中明确指示模型基于检索结果回答。
5. **多轮对话改写**：开启后用轻量模型基于历史对话补全当前查询，提升多轮场景下的检索准确率。

## 计费说明

从知识库召回的文本切片会占用模型上下文窗口并增加输入 Token 消耗。知识库本身已正式商业化计费，费用由规格费用和模型调用费用构成，可通过降低向量检索 TopK 控制成本。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [llm application](../guides/llm-application.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [application component api reference](../api/application-component-api-reference.md)
- [start using](../guides/start-using.md)
- [data connection overview](../guides/data-connection-overview.md)


