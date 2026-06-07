# 文本向量与多模态向量对比

百炼平台同时提供文本向量（General Text Embedding）和多模态向量（Multimodal Embedding）两类向量化能力。前者专注于将文本高效转换为语义向量，适合纯文本检索、分类和聚类等场景；后者则能将文本、图像和视频映射到同一语义空间，支持跨模态检索与匹配。本文从输入模态、模型规格、API 接口、计费方式和典型场景等维度进行对比，帮助开发者快速做出技术选型。

## 关键维度对比

| 维度 | 文本向量 | 多模态向量 |
| --- | --- | --- |
| **输入模态** | 仅文本（字符串、字符串列表或文件） | 文本、图像、视频、多图 |
| **输出类型** | 独立向量（每条输入一个向量） | 独立向量 + 融合向量（多模态融合为单一向量） |
| **代表模型** | text-embedding-v4（Qwen3-Embedding）、v3、v2、v1 | qwen3-vl-embedding、qwen2.5-vl-embedding、tongyi-embedding-vision 系列 |
| **最大向量维度** | 2048（v4） | 2560（qwen3-vl-embedding） |
| **可选维度** | v3/v4 支持 64–2048 多档位 | 因模型而异，qwen3-vl-embedding 支持 256–2560 |
| **单次最大文本长度** | v3/v4：8,192 Token；v1/v2：2,048 Token | qwen3/qwen2.5-vl：32K Token；tongyi 系列：1K Token |
| **API 协议** | OpenAI 兼容（同步）+ DashScope（同步/异步） | DashScope 原生 |
| **同步 API 端点** | `POST /compatible-mode/v1/embeddings` | `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` |
| **异步/批处理** | 支持（text-embedding-async-v1/v2，单次最多 10 万行） | 不支持专用批处理接口 |
| **SDK 支持** | OpenAI SDK（兼容模式）+ DashScope SDK（Python/Java） | DashScope SDK（Python/Java）+ HTTP |
| **同步单次最大行数** | v3/v4：10 行；v1/v2：25 行 | 按 contents 数组传入，无固定行数限制 |
| **计费单价（千 Token）** | v3/v4：0.0005 元（Batch 半价）；v1/v2：0.0007 元 | 按模型定价，详见模型广场 |
| **语种覆盖** | v4：100+ 语种含编程语言；v1/v2：约 10 个语种 | 中英为主，视觉模态不涉及语种 |
| **多区域可用性** | 按区域开通 | 北京区域全模型可用；新加坡仅 tongyi-embedding-vision-plus/flash |

## 模型能力对比

### 文本向量模型

| 模型 | 向量维度 | 单行最大 Token | 特点 |
| --- | --- | --- | --- |
| text-embedding-v4 | 64–2048 | 8,192 | Qwen3-Embedding，100+ 语种，性能最强 |
| text-embedding-v3 | 64–1024 | 8,192 | 多维度可选，性价比高 |
| text-embedding-v2 | 1,536（固定） | 2,048 | 稳定版本，约 10 语种 |
| text-embedding-v1 | 1,536（固定） | 2,048 | 初代版本 |

### 多模态向量模型

| 模型 | 默认维度 | 向量类型 | 文本长度 | 特点 |
| --- | --- | --- | --- | --- |
| qwen3-vl-embedding | 2560 | 独立/融合 | 32K | 最新旗舰，支持 enable_fusion 开关 |
| qwen2.5-vl-embedding | 1024 | 仅融合 | 32K | 始终返回融合向量 |
| tongyi-embedding-vision-plus-2026-03-06 | 1152 | 独立/融合 | 1K | 支持分辨率档位和视频帧数控制 |
| tongyi-embedding-vision-flash-2026-03-06 | 768 | 独立/融合 | 1K | 轻量快速版 |
| multimodal-embedding-v1 | 1024（固定） | 独立 | 512 | 初代多模态向量模型 |

## 适用场景建议

### 优先选择文本向量的场景

- **纯文本语义搜索**：文档检索、FAQ 匹配、知识库问答等只涉及文本的检索任务，文本向量模型在纯文本场景下效果更优且成本更低。
- **大批量离线向量化**：需要处理海量文本（如百万级文档库），可使用异步批处理接口（text-embedding-async），单次最多 10 万行，且 Batch 价格享半价优惠。
- **多语种文本处理**：text-embedding-v4 覆盖 100+ 语种和编程语言，适合国际化和代码检索场景。
- **OpenAI SDK 生态集成**：已有 OpenAI SDK 代码的项目可零成本迁移，直接更换 base_url 即可接入。

### 优先选择多模态向量的场景

- **跨模态检索**：以文搜图、以图搜视频、以图搜图等需要在不同模态之间进行语义匹配的任务。
- **图文融合表征**：电商商品（图片 + 描述）、新闻（标题 + 配图）等需要将多种模态信息融合为统一向量的场景。
- **视频内容理解**：需要对视频进行语义编码并与文本或图像进行相似度匹配的场景。
- **多模态 RAG**：[检索增强生成](../concepts/rag.md)中同时涉及文本和图像内容的知识库构建。

## 技术选型参考

1. **如果只处理文本**，选文本向量模型。text-embedding-v4 是当前推荐版本，维度灵活、语种覆盖广、支持 OpenAI 兼容协议，集成成本最低。
2. **如果涉及图像或视频**，选多模态向量模型。qwen3-vl-embedding 能力最全面，支持独立向量和融合向量两种模式，文本上下文窗口达 32K。
3. **如果需要大批量离线处理**，文本向量的异步批处理接口是唯一选择，多模态向量暂无对应的批处理能力。
4. **如果需要控制向量维度以平衡精度和存储**，两类模型的新版本均支持多维度选择，但可选范围不同，需根据具体模型确认。
5. **如果需要跨区域部署**，注意多模态向量在新加坡区域仅支持 tongyi-embedding-vision-plus/flash 两个模型，文本向量的区域可用性需查看具体模型文档。

## 被对比主题页

- [general text embedding](../api/general-text-embedding.md)
- [multimodal vector](../api/multimodal-vector.md)


