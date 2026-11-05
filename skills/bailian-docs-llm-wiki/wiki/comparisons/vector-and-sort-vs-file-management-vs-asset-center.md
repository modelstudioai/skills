# 向量与排序、文件管理与资产中心的数据管理能力对比

## 背景与目的

在百炼平台构建 AI 应用（如 RAG、多模态搜索、AIGC 工作流）过程中，开发者需频繁处理**非结构化数据的表征、组织与复用**。当前平台提供三类核心数据管理能力：  
- **向量与排序（Vector and Sort）**：面向语义理解与检索优化，将文本/图像/视频等转化为可计算的向量，并支持跨模态精排；  
- **文件管理（File Management API）**：面向原始文件的生命周期管理，支撑微调、内容提取、批量推理等任务的数据准备；  
- **资产中心（Asset Center）**：面向模型生成结果（图片/视频）的持久化存储与工程化复用，强调可视化管控与跨服务引用。

本对比旨在帮助开发者清晰区分三者的技术定位、能力边界与适用阶段，避免功能误用（如用文件管理 API 存储向量、或用资产中心管理 PDF 原文），从而做出高效、合规、可扩展的技术选型决策。

---

## 关键维度对比

| 维度 | 向量与排序（Vector & Sort） | 文件管理（File Management API） | 资产中心（Asset Center） |
|------|-----------------------------|----------------------------------|---------------------------|
| **核心目标** | 语义表征与相关性计算（Embedding/Rerank） | 原始文件上传、元数据管理与下游任务绑定 | 模型生成资产（图片/视频）的统一存储、发现与复用 |
| **输入格式** | 文本字符串、URL（图片/视频）、Base64 编码、多模态混合对象（JSON 格式 `contents` 数组） | 二进制文件流（`multipart/form-data`），支持 `.jsonl`, `.pdf`, `.zip`, `.mp4`, `.jpg` 等常见格式 | **无主动上传接口**；资产由调用生图/生视频模型时**自动生成并自动入库** |
| **输出格式** | 向量数组（`float` 或 `base64` 编码）、排序得分与重排后文档列表 | 文件元数据（`file_id`, `filename`, `purpose`, `size`, `created_at` 等 JSON 对象） | 资产元数据（`asset_id`, `model`, `prompt`, `parameters`, `created_at`, `oss_path` 等），支持卡片式 UI 与列表视图 |
| **支持模型/能力** | • 文本向量：`qwen3.7-text-embedding`, `text-embedding-v4`<br>• 多模态向量：`qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`<br>• 排序：`qwen3-rerank`, `qwen3-vl-rerank` | **不绑定模型**，通过 `purpose` 字段声明用途：<br>• `fine-tune`（微调数据）<br>• `file-extract`（PDF/Word 解析）<br>• `batch`（批量提示词任务） | 仅支持**图片与视频生成模型**：<br>• 图片：`qwen-image-3.0-pro`, `wan2.7-image`, `z-image-turbo` 等<br>• 视频：`wan3.0-video`, `happyhorse1.1-t2v/i2v/r2v` 等 |
| **API 端点（典型）** | • 同步向量：`POST /api/v1/services/embeddings/qwen3.7-text-embedding`<br>• 异步批处理：`POST /api/v1/services/embeddings/text-embedding/text-embedding`<br>• 排序：`POST /api/v1/services/rerank/qwen3-rerank` | • 上传：`POST /api/v1/files`<br>• 查询单个：`GET /api/v1/files/{file_id}`<br>• 列举：`GET /api/v1/files?page_no=1&page_size=50`<br>• 删除：`DELETE /api/v1/files/{file_id}` | **无独立 REST API**；资产通过以下方式访问：<br>• 控制台 UI（`https://bailian.console.aliyun.com/.../asset-center`）<br>• API 中以 `asset_id` 字符串形式传入（如生图请求中 `"control_image": {"asset_id": "xxx"}`） |
| **计费方式** | • 文本向量：按输入 [Token](../concepts/token.md) 计费（例：`text-embedding-v4` 北京 0.0005 元/千 [Token](../concepts/token.md)）<br>• 多模态向量：文本 + 图片/视频分开计费（例：`qwen3-vl-embedding` 文本 0.0007 元/千 [Token](../concepts/token.md)，图片 0.0018 元/千 Token）<br>• 排序：按 `Query Tokens × Document Count` 计费 | **不单独计费**；文件存储计入百炼平台通用资源配额（总文件数 ≤ 10,000，总空间 ≤ 100 GB），超限后无法上传 | • 平台存储：默认 5 GB 免费；超量部分 **0.15 元/GB/月**<br>• OSS 转存：按所选 OSS Bucket 的标准存储费用计费（百炼平台不额外收费）<br>• 回收站内资产（30 天）**持续计费** |
| **地域支持** | 全地域支持（北京、新加坡等多地部署），模型可用性与单价因地域而异 | **仅北京 Region 开放**；其他地域用户需切换至北京控制台或使用 OpenAI 兼容 File 接口 | 全地域支持（资产按当前 Workspace 隔离），OSS 绑定与转存策略为全局配置 |
| **典型场景** | • RAG 底库向量化预计算<br>• 用户查询实时 Embedding + Rerank 精排<br>• 以图搜文、以文搜视频等跨模态检索<br>• 聚类/去重/相似推荐 | • 上传微调数据集（`.jsonl`）启动 Fine-tuning<br>• 上传 PDF 报告触发结构化文本抽取<br>• 批量提交 10,000 条 [prompt](../guides/prompt.md) 进行 Batch 推理 | • 将多次生成的 Banner 图收藏归档<br>• 将首帧图片 `asset_id` 复用于视频生成任务<br>• 自动同步高质量素材至企业 OSS，释放平台存储压力 |

---

## 各方案适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **需要对 100 万条商品标题做语义聚类** | ✅ 向量与排序（异步批处理） | `text-embedding-async-v2` 支持单次 100,000 行，可分批次高效完成；向量直接用于聚类算法，无需中间文件落地。 |
| **上传一份合同 PDF，从中提取条款文本供后续分析** | ✅ 文件管理 API（`purpose=file-extract`） | 文件管理 API 是 `file-extract` 服务的**唯一前置入口**；上传后系统自动触发解析，返回结构化文本。 |
| **生成 50 张营销海报后，需长期保存、打标签、并复用于下一轮视频生成** | ✅ 资产中心 | 海报作为模型输出自动进入资产中心；支持收藏、OSS 转存、并通过 `asset_id` 直接作为 `first_frame` 输入视频模型，形成闭环工作流。 |
| **想把已有的向量数据库（Parquet 格式）导入百炼平台进行 Rerank** | ⚠️ 不适用任一方案 → **应自行托管向量库** | 向量与排序 API **只生成向量，不存储向量**；文件管理 API 不支持向量文件类型；资产中心仅接受图片/视频。建议将向量存于自有向量数据库（如 Milvus/Pinecone），百炼仅调用 Rerank 接口做精排。 |
| **为新上线的客服机器人准备 500 条 FAQ 微调数据** | ✅ 文件管理 API（`purpose=fine-tune`） | 必须通过此 API 上传 `.jsonl` 文件，才能在「模型调优」控制台中可见并启动训练任务。 |
| **希望将用户上传的头像图片（Base64）直接用于多模态向量计算** | ✅ 向量与排序（多模态 Embedding） | 支持 `{"image": "data:image/png;base64,..."}` 格式直传，无需先存为文件；比“上传→查ID→再调用”更轻量、低延迟。 |

---

## 面向开发者的技术选型参考

### ✅ 优先选择「向量与排序」当：
- 你的核心需求是**语义理解、相似计算或排序决策**；
- 输入是纯文本、URL 或 Base64，且需实时/准实时响应（同步）或大规模预处理（异步）；
- 你正在构建 RAG、智能搜索、推荐系统等 AI 应用链路；
- **避坑提示**：不要试图用它存储原始文件——它不提供文件 ID 或下载能力。

### ✅ 优先选择「文件管理 API」当：
- 你需要为**下游特定服务（微调/抽取/Batch）准备原始文件输入**；
- 文件需被平台识别用途（`purpose`），并与其他服务深度集成；
- 你接受其**仅北京地域可用**的限制，且文件规模在配额内（≤100 GB / ≤10,000 个）；
- **避坑提示**：该接口已标记为“历史兼容”，新项目应评估 [OpenAI 兼容 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) 是否满足需求。

### ✅ 优先选择「资产中心」当：
- 你的数据是**百炼模型生成的图片或视频**（非用户上传、非第三方来源）；
- 你需要**UI 可见、可筛选、可收藏、可一键转存 OSS** 的资产管理体验；
- 你计划在多个模型间复用同一资产（如用 A 模型生图 → B 模型生视频）；
- **避坑提示**：资产中心**不支持音频、文本、PDF 等非生成类资产**；也不支持直接上传或 API 创建资产。

### 🔁 协同使用模式（推荐组合）
- **RAG 全流程**：文件管理 API 上传 PDF → `file-extract` 解析出文本 → 向量与排序 API 向量化 → 存入自有向量库 → 用户查询时调用 Rerank 精排。  
- **AIGC 内容工厂**：调用 `qwen-image-3.0-pro` 生成图 → 自动入库资产中心 → 收藏优质图 → 在 `wan3.0-video` 请求中传入 `asset_id` 作为首帧 → 视频生成后再次入库 → 形成可追溯的内容资产谱系。

> **最后建议**：技术选型不应孤立看待单点能力。请始终以**端到端业务流**为单位设计数据通路——明确每个环节的输入源、处理动作、输出形态与下游依赖，再匹配百炼对应能力。平台能力矩阵持续演进，建议定期查阅最新 [API 参考文档](https://help.aliyun.com/zh/dashscope/developer-reference) 与 [用户指南](https://help.aliyun.com/zh/dashscope/user-guide)。

## 被对比主题页

- [vector and sort](../api/vector-and-sort.md)
- [file management api](../api/file-management-api.md)
- [asset center page](../guides/asset-center-page.md)


