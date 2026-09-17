# 向量嵌入

向量嵌入（Vector Embedding）是将文本、图像、视频等非结构化数据映射到高维连续语义空间中的稠密数值向量，使语义相近的内容在向量空间中距离更近（如余弦相似度更高），从而支撑语义检索、相似性计算与跨模态对齐等核心AI能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 与知识库构建**：知识库服务自动调用 `text-embedding-v4` 或 `qwen3.7-text-embedding` 对上传文档进行切片并生成向量，构建可检索的向量索引；开发者也可通过 `/v1/knowledge_bases/{kb_id}/retrieve` 接口触发底层向量检索。
- **纯向量检索与混合检索**：在知识检索（`/api/v1/indices/knowledge/search`）或自定义 RAG 流程中，可显式传入文本或图片作为查询，由 `qwen3-vl-embedding` 等多模态模型统一编码为向量，在同一语义空间内完成跨模态相似匹配。
- **框架集成开发**：LlamaIndex、Spring AI Alibaba 等框架通过 `DashScopeEmbedding` 组件直接调用百炼向量 API（如 `text-embedding-v3`），用于本地索引构建、重排前特征提取等环节。
- **批量建库与离线处理**：对万级文档建库时，使用异步批处理接口 `text-embedding-async-v2`，支持单次提交 10 万行文本（每行 ≤2048 [Token](token.md)），大幅降低建库耗时。
- **多模态融合应用**：启用 `enable_fusion=true`（如 `qwen3-vl-embedding`）或使用 `tongyi-embedding-vision-plus-2026-03-06`，可将图文/视频内容联合编码为单一融合向量，适用于统一召回、跨模态搜索等高级场景。

## 关键参数和配置

| 参数 | 说明 | 典型取值 | 是否必选 |
|------|------|----------|----------|
| `model` | 指定嵌入模型名称 | `"text-embedding-v4"`, `"qwen3-vl-embedding"`, `"multimodal-embedding-v1"` | 必选 |
| `input` | 同步调用时的输入数据 | 字符串、字符串数组，或文件 URL（异步） | 必选（同步）/ `file_url`（异步） |
| `dimensions` | 指定向量维度（部分模型支持） | `256`, `1024`, `2048`（`text-embedding-v4` 默认 1024；`qwen3-vl-embedding` 可选 256–2560） | 可选（不支持则忽略） |
| `encoding_format` | 输出向量格式 | `"float"`（默认，推荐）、`"base64"`（仅同步接口支持，长请求自动降级为 float） | 可选 |
| `enable_fusion` | 多模态模型是否启用融合编码（仅部分模型支持） | `true` / `false`（默认 `false`） | 可选（启用融合时必填 `true`） |
| `res_level` / `max_video_frames` | 视频嵌入精度控制（新版视觉模型） | `"high"`, `"medium"`, `"low"`；`1–32` 帧采样数 | 可选 |

> ⚠️ 注意：  
> - 同步接口单次最多处理 10–20 条文本（依模型而定），超限需分批；  
> - 异步批处理要求输入文件为 UTF-8 编码 CSV/JSONL，每行一个 `{"text": "..."}` 或 `{"content": [...]}` 结构；  
> - 多模态输入需按规范组织 `content` 数组（含 `type: "text"`/`"image_url"`/`"video_url"` 字段），否则返回 `400` 错误。

## 面向开发者，简洁实用

- ✅ **快速上手**：优先使用 OpenAI 兼容路径 `/compatible-mode/v1/embeddings`，复用现有 SDK（如 `openai>=1.0`），只需替换 `base_url` 和 `api_key`。  
- ✅ **生产建议**：实时场景用同步 API（`text-embedding-v4`）；建库任务一律走异步批处理（`text-embedding-async-v2`），避免超时与限流。  
- ✅ **跨模态对齐**：务必选用同一模型家族（如 `qwen3-vl-*` 系列）生成查询与文档向量，禁用混用 `text-embedding-v4` + `qwen3-vl-embedding`。  
- ✅ **性能调优**：对长文本，先用 `DashScopeParse` 解析再切片，比原始文本直接嵌入效果更稳定；维度降维（如 `dimensions=256`）可提升检索速度，但可能轻微损失精度。  
- ❌ **避坑提示**：`gte-rerank` 系列已下线，其配套向量模型（如 `gte-embedding`）不再维护，请迁移至 `text-embedding-v3/v4` 或 `qwen3.7-text-embedding`。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [knowledge](../api/knowledge.md)
- [frameworks](../api/frameworks.md)
- [llm application](../guides/llm-application.md)


