# 向量嵌入

向量嵌入（Vector Embedding）是将原始非结构化数据（如文本、图像等）映射到高维连续向量空间的数学表示过程，其核心目标是让语义或视觉上相似的输入在向量空间中距离更近（如余弦相似度更高），从而支撑语义检索、聚类、去重等下游任务。该向量为固定维度的稠密浮点数组，已归一化（L2 norm = 1.0），可直接用于相似度计算。

## 在百炼平台的不同场景中，这个概念如何使用

- **语义检索与 RAG**：知识库构建时，系统自动调用指定嵌入模型（如 `text-embedding-v4`）对文档切片进行向量化，并建立向量索引；检索时将用户 query 转为向量，在索引中执行近似最近邻（ANN）搜索，召回语义最相关的切片。
- **通用向量服务（API 直接调用）**：通过 `/v1/embeddings` 接口，开发者可同步获取文本或图文联合的嵌入向量，适用于自建检索系统、特征工程、内容去重等场景。支持单条/批量文本（≤100 条）、多模态输入（单图+文）。
- **框架集成（LlamaIndex / Spring AI）**：通过 `DashScopeEmbedding` 等封装组件，无缝接入本地或云端 RAG 流程，自动处理 tokenization、向量化及向量归一化，无需手动管理模型加载与推理。
- **混合检索增强**：在 `DashScopeCloudRetriever` 等高级检索器中，向量嵌入与关键词（稀疏）检索并行执行，结果经融合排序后返回，兼顾语义泛化性与字面精确性。
- **跨模态理解**：使用 `multimodal-embedding-v1` 模型，将图像（base64 编码）与描述文本联合编码为统一向量，支持“以图搜文”“以文搜图”等跨模态检索任务。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 嵌入模型标识，常用值：<br>• `text-embedding-v3`（推荐通用文本）<br>• `text-embedding-v4`（知识库默认，中英文更强）<br>• `multimodal-embedding-v1`（图文联合） |
| `input` | string / array / object | 是 | 输入格式依模型而定：<br>• 文本模型：字符串或字符串数组（最多 100 项）<br>• 多模态模型：单个 `{ "text": "...", "image": "base64..." }` 对象（不支持数组） |
| `encoding_format` | string | 否 | 输出向量编码格式，可选 `"float"`（默认，返回 float32 数组）或 `"base64"`（压缩传输，需客户端解码） |
| `dimensions` | integer | 否 | （仅部分模型支持）指定输出向量维度，如 `512` 或 `1024`；未指定时使用模型默认维度（如 `text-embedding-v3` 默认 1024） |

> ⚠️ 注意事项：
> - 所有嵌入向量均为 L2 归一化结果，**无需二次归一化**即可直接计算余弦相似度；
> - 单次请求总 token 数上限为 8192（按对应模型 tokenizer 计算）；
> - 多模态输入图像建议分辨率 ≤ 1024×1024，避免超时或 OOM；
> - 向量维度必须与检索索引一致——若知识库使用 `text-embedding-v4`（1024 维），则自定义 query 向量也须用同模型生成。

## 面向开发者，简洁实用

- ✅ **首选模型**：生产环境推荐 `text-embedding-v4`（知识库默认）或 `text-embedding-v3`（API 直调默认），二者均支持中英文混合，精度与稳定性经过大规模验证。
- ✅ **快速验证**：用 curl 一行命令测试文本嵌入：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"text-embedding-v4","input":["百炼平台很强大"]}'
  ```
- ✅ **性能提示**：批量请求比单条请求吞吐更高；但多模态嵌入仅支持单条，需循环调用。
- ✅ **调试技巧**：对比两个向量 `v1` 和 `v2` 的余弦相似度，直接计算 `np.dot(v1, v2)`（因已归一化）；值越接近 1.0 表示语义越相似。
- ❌ **避坑指南**：勿混用不同模型生成的向量做相似度比较；勿对已归一化的向量再次归一化；勿在知识库创建后尝试修改其嵌入模型——该配置不可变。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application component api reference](../api/application-component-api-reference.md)


