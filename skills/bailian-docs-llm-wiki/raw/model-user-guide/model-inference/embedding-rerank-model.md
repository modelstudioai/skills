# 向量与重排序

选择适合语义搜索、RAG（Retrieval-Augmented Generation）检索、跨模态匹配和重排序场景的模型。

## 文本Embedding

纯文本搜索、RAG或聚类场景，推荐使用`text-embedding-v4`。如果需要迁移已有的v3索引，可使用`text-embedding-v3`（维度兼容）。

### 如何选择维度？

-   大规模搜索且存储空间有限：选择256或512维。
    
-   通用场景：选择1024维（默认值，平衡效果好）。
    
-   对检索精度要求高：选择1536或2048维。
    

## 多模态Embedding

如需跨模态检索（文本搜图片、文本搜视频），根据需求选择融合向量或独立向量。

### 融合向量 vs 独立向量

-   **融合向量**：将文本和图片融合为一个向量，适用于图文混合检索。推荐使用`qwen3-vl-embedding`或`qwen2.5-vl-embedding`。
    
-   **独立向量**：为每种模态分别生成向量，适用于跨模态搜索（文搜图、图搜图）。推荐使用`tongyi-embedding-vision-plus`。
    

### 只有纯文本数据？

建议使用`text-embedding-v4`，速度更快、成本更低、维度选择更多。多模态Embedding适用于跨模态检索（文本和图片互搜、文本和视频互搜）。

## 重排序（Rerank）

用于提升RAG精度：在Embedding检索之后使用重排序模型对Top-N结果进行重排序，通过交叉注意力机制提高排序质量。

-   **纯文本重排序**：使用`qwen3-rerank`，支持100+语言，最多500个文档。
    
-   **多模态重排序**：使用`qwen3-vl-rerank`，支持文本、图片和视频混合排序。
    

## 所有模型

**模型**

**类型**

**向量维度**

**最大Token数**

**适用场景**

`text-embedding-v4`

文本Embedding

64~2048（默认1024）

8,192

文本搜索、RAG、聚类

`text-embedding-v3`

文本Embedding

512~1024（默认1024）

8,192

已有v3索引迁移

`qwen3-vl-embedding`

多模态Embedding

256~2560（默认2560）

32,000

图文混合检索（融合向量+独立向量）

`qwen2.5-vl-embedding`

多模态Embedding

512~2048（默认1024）

32,000

图文混合检索（仅融合向量）

`tongyi-embedding-vision-plus-2026-03-06`

多模态Embedding

64~1152（默认1152）

1,024

跨模态搜索（融合向量+独立向量）

`tongyi-embedding-vision-flash-2026-03-06`

多模态Embedding

64~768（默认768）

1,024

跨模态搜索，注重成本

`tongyi-embedding-vision-plus`

多模态Embedding

64~1152（默认1152）

1,024

跨模态搜索（仅独立向量）

`tongyi-embedding-vision-flash`

多模态Embedding

64~768（默认768）

1,024

跨模态搜索，注重成本（仅独立向量）

`qwen3-vl-rerank`

重排序

\-

8,000/条

多模态搜索结果重排序

`qwen3-rerank`

重排序

\-

4,000/条

文本搜索结果重排序、RAG

`gte-rerank-v2`

重排序

\-

4,000/条

文本语义检索、RAG
