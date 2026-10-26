# 向量检索、沙箱环境与文件管理能力对比

本对比旨在帮助开发者清晰理解百炼平台三大基础能力模块——**向量检索（[vector and sort](../api/vector-and-sort.md)）**、**沙箱环境（sandbox API）** 与 **文件管理（file management API）** 的定位差异、技术边界与协同关系。三者虽常在 RAG、Agent、自动化数据处理等复杂场景中组合使用，但其设计目标、抽象层级与适用范围截然不同：向量检索聚焦**语义表征与相关性计算**，沙箱提供**安全隔离的代码执行上下文**，而文件管理则承担**结构化资源的生命周期托管**。本文从核心能力维度出发，为技术选型提供客观、可落地的决策依据。

## 关键能力维度对比

| 维度 | 向量检索（[vector and sort](../api/vector-and-sort.md)） | 沙箱环境（sandbox API） | 文件管理 API（file management） |
|------|-----------------------------|---------------------------|----------------------------------|
| **核心功能** | 文本/多模态向量生成（embedding） + 检索后重排序（rerank） | 创建、管理隔离、可复现的临时计算环境（支持代码执行、联网、文件挂载） | 文件上传、查询、列举、删除；按 `purpose` 分类支撑下游任务（微调/内容提取/Batch） |
| **输入格式** | • 同步：`string` / `array<string>` / 文件流（文本）<br>• 多模态：`input.contents` 数组（含 `text`/`image`/`video` 对象）<br>• 异步批处理：`input.url` 指向文本文件（单行 ≤2048 [Token](../concepts/token.md)，≤100,000 行） | • 模版创建：JSON 定义镜像、资源配置、`mntConfig`（挂载路径必须以 `/home/user/workspace/uploads/` 开头）、网络策略<br>• 实例创建：`templateID` + `timeout` + `allow_internet_access` 等 | `multipart/form-data`：<br>• `files`（文件流，支持多文件）<br>• `purpose`（`fine-tune`/`file-extract`/`batch`，**强烈建议显式指定**）<br>• `descriptions`（可选备注） |
| **输出格式** | • 向量：`data[].embedding`（`float[]` 或 `base64` 编码）<br>• 排序：`results[].index`, `results[].relevance_score`, `results[].document`（当 `return_documents=true`） | • 实例：`sandboxID`, `domain`, `envdAccessToken`, `status`<br>• 模版：`templateID`, `buildID`, `status=ready`<br>• 文件挂载结果：挂载路径下可见文件（需符合路径前缀约束） | • 上传：`id`, `filename`, `purpose`, `size`, `status=uploaded`<br>• 查询/列举：完整文件元信息（含 `id`, `purpose`, `size`, `created_at`, `expires_at`）<br>• 删除：HTTP 204 或错误响应 |
| **支持模型/运行时** | • 文本向量：`qwen3.7-text-embedding`, `text-embedding-v4/v3/v2/v1`, `text-embedding-async-v2`（推荐）<br>• 多模态向量：`qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`<br>• 排序：`qwen3.7-text-rerank`, `qwen3-vl-rerank` | • **无内置模型**，依赖预置或自定义 Docker 镜像（如 `code-interpreter-v1`, `browser`, `all-in-one`）<br>• 运行时由模版定义：CPU/内存规格、是否联网、挂载文件、环境变量 | • **不绑定模型**，通过 `purpose` 字段路由至下游服务：<br>– `fine-tune` → 微调训练管道<br>– `file-extract` → PDF/Word/OCR 结构化解析引擎<br>– `batch` → 批量推理任务调度器 |
| **API 端点（典型）** | • 同步向量：`POST /v1/embeddings`<br>• 异步向量：`POST /v1/vector/batch`（提交）+ `GET /v1/vector/batch/{task_id}`（轮询）<br>• 排序：`POST /v1/services/rerank/text-rerank/text-rerank` | • 模版：`POST /v3/templates`, `GET /v3/templates/{templateCode}/builds/{buildID}`<br>• 实例：`POST /sandboxes`, `POST /sandboxes/{sandboxID}/connect`, `DELETE /sandboxes/{sandboxID}`<br>• 文件挂载：`POST /api/v1/agentstudio/files`（需 `source=sandbox_template`） | • 上传：`POST https://dashscope.aliyuncs.com/api/v1/files`<br>• 查询：`GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}`<br>• 列举：`GET https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20`<br>• 删除：`DELETE https://dashscope.aliyuncs.com/api/v1/files/{file_id}` |
| **计费方式** | • 按 **[Token](../concepts/token.md) 数量** 计费（输入 [Token](../concepts/token.md) + 输出 Token）<br>• 免费额度存在地域差异（如北京地域 `qwen3.7-text-embedding` 享 100 万 Token 免费额度，新加坡无）<br>• 异步批处理 `text-embedding-async-v2` 北京享 2000 万 Token 免费额度 | • 按 **实例运行时长（秒）** 计费（从 `running` 状态开始计时）<br>• 超时自动释放（`maxRunningTimeout` 优先生效），暂停状态不计费<br>• 模版构建、文件上传、连接操作本身不计费 | • **当前免费**（文档未提及计费项）<br>• 受配额约束：总存储 ≤100 GB，总文件数 ≤10,000，单文件大小依 `purpose` 限制（如 `file-extract` ≤150 MB） |
| **典型场景** | • RAG 中的语义召回与结果重排<br>• 跨模态搜索（图文互搜、视频片段检索）<br>• 向量数据库预处理（批量 embedding）<br>• 相似内容去重、聚类 | • Agent 中的安全代码解释与工具调用（如 Python 数据分析、Shell 命令执行）<br>• 浏览器自动化（网页抓取、表单填写）<br>• 沙箱内运行用户上传脚本并返回结构化结果<br>• 需要联网访问外部 API 的可控执行环境 | • 为微调任务准备训练数据集（`.jsonl` 或 `.zip`）<br>• 提交 PDF/Word 文件供内容提取与表格识别<br>• 批量处理大量文本/图像文件（通过 Batch 接口）<br>• 在多个下游任务间共享原始文件资源 |

## 各方案适用场景建议

| 场景描述 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| **构建高精度语义搜索系统**（如客服知识库、技术文档问答） | ✅ 向量检索 | 提供端到端 embedding + rerank 能力，支持文本/多模态统一语义空间，`qwen3.7-text-rerank` 显著提升 Top-K 准确率；异步接口满足海量文档预处理需求。 | 避免使用已进入下线周期的 `gte-rerank-v2`；注意 Token 限制（超限直接 400 错误，不截断）。 |
| **需要执行不可信用户代码或调用外部 API**（如数据分析 Agent、网页爬虫） | ✅ 沙箱环境 | 提供硬件级隔离、网络策略可控（白/黑名单）、文件挂载安全、实例生命周期明确（自动超时释放），远超普通容器或函数计算的安全边界。 | 模版必须 `status=ready` 才能创建实例；挂载路径必须以 `/home/user/workspace/uploads/` 开头；仅支持 `.yaml` 等有限文件类型上传。 |
| **集中管理训练数据、PDF 报告、批量待处理文件** | ✅ 文件管理 API | 统一入口上传/查询/删除，`purpose` 字段自动路由至对应下游服务（微调管道、OCR 引擎、Batch 调度器），避免重复上传与路径管理混乱。 | **强烈推荐迁移到 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) `/compatible-mode/v1/files`**（多 Region 支持、长期维护）；原生接口仅限北京 Region。 |
| **需在沙箱内处理用户上传的文件（如读取 CSV 并绘图）** | ⚠️ **组合使用：文件管理 + 沙箱** | 文件管理 API 上传文件获取 `file_id` → 沙箱 API 创建模版时通过 `mntConfig.originFileId` 挂载 → 在沙箱内安全访问并处理。 | 文件管理上传的文件需 `source=sandbox_template` 且 `status=available`；沙箱挂载路径有严格前缀要求。 |
| **对已有向量数据库做实时相似性检索（非百炼托管）** | ❌ 三者均不直接适用 | 向量检索 API 仅提供 embedding/rerank，**不提供向量存储与近似最近邻（ANN）检索服务**；沙箱与文件管理亦无此能力。 | 需自行集成 Milvus、Qdrant 或阿里云 OpenSearch 等向量数据库。 |

## 面向开发者的选型指南

- **优先确认“做什么”，而非“用哪个 API”**：  
  若目标是**计算语义相似度或打分** → 选 *向量检索*；  
  若目标是**安全地运行一段代码** → 选 *沙箱环境*；  
  若目标是**上传一份文件供后续流程使用** → 选 *文件管理 API*（并立即规划迁移到 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）。

- **警惕能力错配陷阱**：  
  - 不要用沙箱 API 去生成向量（性能差、成本高、无优化）；  
  - 不要用文件管理 API 去执行排序逻辑（它只存文件，不提供计算）；  
  - 不要期望向量检索 API 返回可执行代码结果（它只返回数字向量或分数）。

- **生产环境关键实践**：  
  - **向量检索**：对大批量文本，务必使用 `text-embedding-async-v2` 异步接口；对低延迟查询，选用 `qwen3.7-text-embedding` 同步接口并预热连接池。  
  - **沙箱环境**：始终设置 `maxRunningTimeout` 防止实例无限运行；敏感任务禁用 `allow_internet_access` 或配置精细 `network.allowOut` 白名单。  
  - **文件管理**：所有新项目必须使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) `/compatible-mode/v1/files`；上传时强制指定 `purpose`，避免文件“游离”于业务流程之外。

- **协同模式推荐（RAG + Agent 典型链路）**：  
  ```mermaid
  graph LR
    A[用户上传 PDF] --> B[文件管理 API：purpose=file-extract]
    B --> C[自动触发 OCR/结构化提取]
    C --> D[提取文本存入向量库]
    D --> E[向量检索 API：embedding + rerank]
    E --> F[召回 Top-K 文档]
    F --> G[沙箱环境：运行 Python 脚本聚合答案/生成图表]
    G --> H[返回最终响应]
  ```

> **最后提醒**：三者并非竞争关系，而是百炼平台“数据层→计算层→执行层”的有机组成。技术选型的本质，是将业务问题精准映射到最匹配的能力抽象上。善用组合，方能构建健壮、可扩展的 AI 应用。

## 被对比主题页

- [vector and sort](../api/vector-and-sort.md)
- [sandbox api](../api/sandbox-api.md)
- [file management api](../api/file-management-api.md)


