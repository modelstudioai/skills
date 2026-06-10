# knowledge base

百炼知识库（Bailian Knowledge Base）基于 RAG（[检索增强生成](../concepts/rag.md)）为大模型补充私有数据与最新信息，使大模型能够回答特定领域问题。它将文件解析、切分、向量化并落入向量库，应用调用时按语义相似度召回切片并交由大模型生成答案，详见 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 知识库类型与使用场景

创建后**类型不可更改**，需根据数据形态和业务场景选择：

- **文档搜索**：面向 PDF、Word、Markdown、图片等非结构化数据。使用场景细分为：
  - `基础文档问答`：纯文本语义检索。
  - `图文并茂回复`：从插图抽取摘要，由模型决定是否插图返回。
  - `视觉理解（富文本文档）`：使用 `qwen3-vl-embedding` 多模态向量对整页做视觉级理解，保留版面布局；支持纯文字 / 纯图片 / 图文组合命中。
  - `极速问答`：低延迟检索，适合 FAQ、参数表等高度结构化文档，仅支持文本查询。
- **数据查询（NL2SQL / Chatbot）**：结构化 Excel / RDS 表，按列开关「参与检索」与「参与模型回复」。要求多文件**表头完全一致**，首行必须为表头。
- **图片问答（图搜场景）**：数据表中需含 `image_url` 字段（公网可访问 URL，单图 ≤ 3 MB，**字段创建后不可新增或修改**）。
- **音视频搜索**：MP3、WAV、MP4、MOV 等格式，按时间轴对齐语音识别 + 视频帧提取 + 剧情解析。

## 支持的模型

知识库可挂载到智能体或工作流应用，与应用所选模型协同工作。预置模型涵盖千问 QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问 VL-Max/Plus/Flash/OCR、千问开源版（Qwen3/2.5/2）及第三方模型（DeepSeek-R1/V3.1、abab6.5s、Llama3.1、Yi-Large 等）；调优后的自定义模型支持千问 Plus/Turbo、千问 VL-Max/Plus、千问开源版。具体可选项以创建应用时的下拉列表为准（[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)）。

> **注意**：实际支持的模型清单随版本更新，请以控制台为准。

## 核心索引参数

以下参数**仅在创建时可配置，创建后无法修改**（除知识库名称、描述和相似度阈值外）：

| 参数 | 说明 | 默认 / 推荐 |
| --- | --- | --- |
| 向量模型 | 文档/数据/音视频类支持 `text-embedding-v4`（推荐）和 `text-embedding-v3`，均为 512 维；图片问答类目前仅支持 `multimodal-embedding-v1`（1024 维）；视觉理解场景自动使用 `qwen3-vl-embedding` | v4 |
| 切片方式 | `智能切分`（语义自适应）/ `按长度`（含重叠字符数，建议 10-25%）/ `按页` / `按标题` / `按正则` / `按符号`；单切片上限 6000 Token | 智能切分 |
| 排序模型 | 外部 Rerank，推荐 `qwen3-rerank（hybrid）`（综合语义 + BM25），仅语义可选 `qwen3-rerank` | hybrid |
| 排序模式 | `问答模式`（默认） / `相似模式` / `自定义高级`（≤200 字自然语言指令） | 问答模式 |
| Meta 信息抽取 | 支持常量 / 变量（`file_name`、`cat_name`） / 大模型 / 正则 / 关键词；可开启「参与检索 / 参与模型回复」 | 关闭 |
| 多轮对话改写 | 用轻量模型基于历史对话补全当前查询 | 关闭 |
| 相似度阈值 | 仅高于此值的切片被召回；可调（应用侧设置会覆盖知识库默认值） | 视觉理解 0.20 |
| 最大召回数量 | 排序后送入大模型的切片数 K，上限 20 | — |
| 向量存储 | `内置`（免费）或 `ADB-PG`（需开启向量引擎优化，自购计费） | 内置 |

> **注意**：排序模型**不支持**图片问答类知识库；视觉理解和极速问答场景**不支持**排序模式配置。详见 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) 的「排序模型」一节。

## 集成与使用

- **智能体应用**：在应用编辑页点击「文档知识库」右侧 `+` 添加；可单独覆盖相似度阈值与权重。**权重仅在同类型知识库之间生效**。
- **工作流应用**：拖入「知识库」节点，输入变量绑定到 `query`；支持「固定选择」或通过 `CodeList` 变量「动态引入」；下游接大模型节点，提示词中插入 `result` 变量。
- **外部应用**：通过百炼 SDK 调用知识库检索接口；前置需在子账号下授予 `AliyunBailianDataFullAccess` 策略，并设置 `ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`、`WORKSPACE_ID` 环境变量。完整 Python 示例和 `ApplyFileUploadLease → AddFile → SubmitIndexJob → Retrieve` 全流程见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 命中测试与 Rerank 配置

命中测试用于在不调用大模型的前提下，模拟提问验证召回质量并调优阈值。三种排序模式在同一查询上的分数差异显著（如同一切片问答模式 47%、相似模式 69%）。

Rerank 开关位置因调用方式而异（**配置错误可能产生非预期费用**）：

- **旧版智能体 / 工作流应用**：在应用页面的知识库「调试」处设置「重排策略」开关，**应用内配置优先级高于知识库本身**。
- **新版智能体应用（Agent 2.0）**：在知识库卡片的「命中测试」中将「选择排序模型」设为「不使用模型」，**以知识库自身配置为准**。
- **OpenAPI**：可在控制台编辑或命中测试页设置，也可通过 `Retrieve` 接口参数覆盖。**API 参数优先级高于控制台配置**。

## RAG 效果优化

如出现召回不全或回答不准，按 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) 的方法定位：

1. **建立评测基线**：用「自动评测」创建 ≥100 组覆盖事实型 / 比较型 / 教程型 / 分析型问题的评测集。
2. **检索无效（无相关知识）**：补充知识源、修正源文件排版（避免水印、复杂表格）、统一术语、启用多轮对话改写。
3. **检索无效（召回不相关）**：用文件标签做粗筛、用 metadata 做结构化过滤（如按产品名 / 日期）。
4. **切片不完整**：优先 `智能切分`；导入后人工抽检并直接「编辑切片」修正解析异常。
5. **重排不佳**：放宽相似度阈值，并适当提高召回片段数 K（列举 / 总结 / 比较类问题 K=20 通常更好，但需注意拼装后总长度不要超出模型上下文）。

## 更新与维护

- **文档搜索类**：推荐用 OSS + 函数计算 FC 监听文件变更**自动更新**；手动模式下，**修改文件需先删再传**（不支持原地覆盖；保留旧版本可能召回过时内容）。切片可单独编辑、新增（≤6000 字符）或删除。
- **数据查询 / 图片问答类**：推荐挂接 RDS / 自建 MySQL 自动同步（延迟分钟级，高峰小时级）；手动更新需先在数据连接器「增量上传」或「覆盖上传」Excel，再回知识库手动触发同步。
- **音视频搜索类**：不支持自动更新，**仅支持删除切片**，不支持新增 / 编辑切片。
- **变更配置**：标准版 ↔ 旗舰版可互转，旗舰版可调 RCU。**每个自然日仅允许变配 1 次**（超出会被静默拒绝）；从旗舰版降级到标准版前，平台存储须降至 80 GB 以下。
- **删除**：删除前应解除与所有已发布应用的关联；**已发布应用的关联会阻止删除**，未发布应用不影响。

## 配额、限制与计费

容量与限制详见 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md) 与 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。关键项：

| 项 | 标准版 | 旗舰版 |
| --- | --- | --- |
| 最高并发 | 1 QPS（固定） | 50-10,000 QPS（1-200 RCU 可调） |
| 平台存储 | ≤ 100 GB | ≤ 9,999 GB（或自购 ADB-PG） |
| 规格费用 | 0.03 元/知识库/小时 | 0.2 元/RCU/小时 |
| 文件格式（文档类） | pdf/docx/doc/wps/pptx/ppt ≤100 MB、≤1000 页；txt/md/html ≤10 MB；xlsx ≤10 MB、≤10 万行；图片 ≤20 MB | 同左 |
| 单文件切片上限 | 无限制 | 无限制 |
| 单切片 Token | 6,000 | 6,000 |
| 单次召回切片数上限 | 20 | 20 |
| 数据查询/图片问答类 Excel | ≤10 万行、≤100 列 | 同左 |
| 音视频文件 | ≤512 MB | 同左 |

应用挂载知识库数量：**Agent 2.0 不限**；旧版智能体 / 工作流应用按类型分别为文档 5 / 数据 5 / 图片 1 / 音视频 5（工作流不支持音视频），合计 ≤16（旧版智能体）或 11（工作流）。

**计费要点**（自 2026-01-04 起正式计费）：

- 后付费按小时出账；扣费顺序为「免费额度 > 资源包 > 按量」。
- **所有用户**赠送一次性 720 小时免费额度，仅抵扣**标准版规格费**；新用户 30 天内有效，老用户截止 2026-02-03。
- **模型调用费用独立计费**：创建/更新按新增 Token 数；检索按 `Query 向量化 + Rerank（初步召回总切片数 × 平均切片 Token × 单价）`。**Rerank 费用由初步召回总数决定，与最终返回数无关**。
- 应用挂多个知识库时，每次 Query 在每个库各执行一次，Token 消耗 ×N。
- 降本可关闭 Rerank 或调低初步向量 / 关键词 TopK（默认各 50，范围 10-100）。

> **注意**：删除知识库内文件**不会停止计费**，唯一停止计费方式是删除整个知识库实例。平台存储欠费保留 14 天，自购 ADB-PG 仅保留 7 天，逾期数据永久删除。

## 日志与监控

所有检索调用以 `topic=log_dispatch` 投递至日志服务（SLS）的固定 LogStore，按 SLS 存储和流量计费（详见 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)）。

核心字段：

- `request_id` / `pipeline_id`（知识库 ID）/ `workspace_id` / `user_id`：定位与聚合。
- `path` / `latency` / `response_status_code` / `response_code`（`Success` 或如 `Index.IndexNotExist` 的点分错误码）/ `response_message`：监控与排错。
- `request_body` / `response_body`：召回切片在 `response_body.data.nodes[]`，每节点含 `score`、`text`、`metadata.doc_name` 等，可用于召回审计。

常见聚合：按 `pipeline_id` / `workspace_id` 统计调用量、按 `path` 拆调用接口、按 `response_code != Success` 监控业务错误率、按 HTTP 5xx 监控服务异常。SLS 查询框内置 Copilot 可辅助生成 SQL。

> **注意**：关闭「检索日志」开关仅停止新日志投递，**已投递的历史日志仍按 SLS 计费**；如需彻底停止，请到 SLS 控制台删除对应 LogStore。

## 权限与安全

- RAM 子账号默认无写权限，需主账号授予「管理员」或同时包含「应用数据-操作」与「知识库-操作」的页面权限。
- 知识库**仅限其所在[业务空间](../concepts/workspace.md)内成员访问**，不对外公开；阿里云不会将其用于回答他人或模型训练。
- 调用 API 报 `BailianIndexServiceNotOpen` 表示服务未激活，需在控制台手动开通。

## 长文本 LLM vs RAG 选型

长文本大模型（如 Qwen-Long）逐 Token 全量审视输入，深度理解与长文摘要更优，但计算成本高；RAG 跨源快速检索、只关注最相关 Token，适合事实型问题与最新信息补充。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)






