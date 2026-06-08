# 文本向量与多模态向量对比

百炼平台同时提供文本向量（Text Embedding）和多模态向量（Multimodal Embedding）两类向量化服务。两者均可将输入转换为数值向量用于语义检索与匹配，但在输入模态、模型架构、API 接口和适用场景上存在显著差异。本文从开发者技术选型角度，对两者进行系统对比。

## 关键维度对比

| 维度 | 文本向量（Text Embedding） | 多模态向量（Multimodal Embedding） |
| --- | --- | --- |
| **输入模态** | 纯文本（字符串/字符串列表/文本文件） | 文本、图片、视频、多图；支持跨模态融合 |
| **输出类型** | 独立文本向量 | 独立向量 + 融合向量（跨模态综合表征） |
| **代表模型** | text-embedding-v4（Qwen3-Embedding）、v3、v2、v1 | qwen3-vl-embedding、qwen2.5-vl-embedding、tongyi-embedding-vision 系列 |
| **最大向量维度** | 2048（v4）/ 1536（v2/v1） | 2560（qwen3-vl-embedding） |
| **维度可调** | v3/v4 支持（64~2048 多档） | 部分模型支持（qwen3-vl 可调 256~2048） |
| **文本长度上限** | 8192 Token（v3/v4）/ 2048 Token（v1/v2） | 32K Token（qwen3-vl / qwen2.5-vl）/ 1K Token（tongyi 系列） |
| **API 协议** | OpenAI 兼容（同步）+ DashScope 异步批处理 | DashScope 原生接口 |
| **同步 API 端点** | `POST /compatible-mode/v1/embeddings` | `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` |
| **异步批处理** | 支持（text-embedding-async-v1/v2，单次 10 万行） | 不支持 |
| **SDK 兼容性** | OpenAI SDK + DashScope SDK（Python/Java） | DashScope SDK / HTTP 直调 |
| **计费单价** | 0.0005 元/千Token（v3/v4）；Batch 半价 | 按模型不同定价（详见模型价格页） |
| **语种覆盖** | v4 覆盖 100+ 语种及编程语言；v1/v2 约 10 语种 | 以中英为主，视觉模态无语种限制 |
| **单次请求容量** | 同步最多 10~25 行；异步最多 10 万行 | contents 数组多条目（无批处理模式） |

## API 调用方式对比

| 特性 | 文本向量 | 多模态向量 |
| --- | --- | --- |
| OpenAI SDK 兼容 | 支持（推荐方式） | 不支持 |
| DashScope SDK | 支持（Python/Java） | 支持（Python/Java） |
| HTTP 直调 | 支持 | 支持 |
| [异步任务](../concepts/async-task.md)模式 | 支持（X-DashScope-Async 头） | 不支持 |
| 结果有效期 | 异步结果 24 小时后清除 | 同步返回，无过期问题 |

## 适用场景建议

### 选择文本向量的场景

- **纯文本语义搜索**：知识库问答、文档检索、FAQ 匹配等传统 NLP 检索场景
- **大批量离线向量化**：需要对百万级文本文件进行批量处理，利用异步接口降低成本
- **多语种文本处理**：涉及 100+ 语种的跨语言检索或分类
- **成本敏感型应用**：文本向量单价更低（0.0005 元/千Token），且 Batch 模式可再降 50%
- **OpenAI 生态迁移**：已有 OpenAI Embedding 代码，可直接切换 base_url 使用

### 选择多模态向量的场景

- **跨模态检索**：以文搜图、以图搜视频、图文混合检索等需要统一语义空间的场景
- **图文融合表征**：电商商品（图片+描述）、新闻（图片+标题）等需要将多模态信息融合为单一向量的场景
- **视觉内容理解**：图片分类、视频语义标注、视觉内容聚类
- **富媒体推荐系统**：基于图文视频综合语义进行内容推荐

## 技术选型决策路径

1. **输入是否包含图片或视频？**
   - 是 → 选择多模态向量
   - 否 → 继续判断

2. **是否需要大批量离线处理（万级以上）？**
   - 是 → 选择文本向量的异步批处理接口（成本最优）
   - 否 → 继续判断

3. **是否需要 OpenAI SDK 兼容？**
   - 是 → 选择文本向量（OpenAI 兼容模式）
   - 否 → 根据文本长度和维度需求选择具体模型

4. **对向量维度有特殊要求？**
   - 需要高维（>2048）→ qwen3-vl-embedding（2560 维）
   - 需要灵活调维 → text-embedding-v4 或 qwen3-vl-embedding
   - 固定维度即可 → 按成本选择

## 注意事项

- 文本向量的同步模型（v1~v4）与异步模型（async-v1/v2）是独立模型，不能混用；异步系列当前无 v3/v4 版本。
- 多模态向量的不同模型在融合向量支持上差异较大：qwen3-vl-embedding 通过 `enable_fusion` 参数控制，qwen2.5-vl-embedding 始终返回融合向量，tongyi 旧版仅支持独立向量。
- 两类向量不在同一语义空间中，不能直接进行跨类型的余弦相似度计算。如需统一检索，应在同一模型体系内完成向量化。

## 被对比主题页

- [general text embedding](../api/general-text-embedding.md)
- [multimodal vector](../api/multimodal-vector.md)


