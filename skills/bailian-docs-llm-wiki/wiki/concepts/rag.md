# 检索增强生成（RAG）

检索增强生成（RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成响应前，系统先从结构化或非结构化知识库中检索相关片段，再将检索结果作为上下文注入提示（prompt），引导模型生成更准确、可溯源、时效性强的回答。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是独立模型，而是**可复用的工程能力模块**，深度集成于以下两类核心路径：

- **零代码应用构建**：在控制台「应用构建」中选择「知识库问答助手」模板后，上传 PDF/DOCX 等文档（单文件 ≤100MB，总容量 ≤10GB），平台自动完成解析（`DashScopeParse`）、向量化与索引构建，并默认启用 RAG 流程——用户提问时，系统实时检索最相关文档段落，拼接至 `messages` 中作为 `system` 或 `user` 上下文，交由指定模型（如 `qwen-plus`）生成答案。全程无需配置检索逻辑，开箱即用。

- **编程式自定义集成**：通过 SDK/API 构建 RAG 应用时，使用 `DashScopeCloudIndex`（基于 LlamaIndex 封装的百炼云端索引服务）：
  - 解析文档：`DashScopeParse.parse_file("doc.pdf")` → 返回结构化文本块；
  - 构建索引：`index = DashScopeCloudIndex.from_documents(documents, workspace_id=...)`（需提前设置 `DASHSCOPE_WORKSPACE_ID` 环境变量绑定业务空间）；
  - 检索+生成：`retriever = index.as_retriever(top_k=3)` 获取检索器，调用 `chat.completions.create()` 时，在 `messages` 中手动注入检索结果（例如追加 `{"role": "system", "content": "参考文档：..."}`）。

> ✅ 提示：百炼 RAG 默认采用语义相似度检索（稠密向量），不支持关键词匹配或混合检索；如需细粒度控制（如过滤时间范围、文档类型），需在索引构建前对原始文档做预处理（如添加元数据字段）。

## 关键参数和配置

| 参数/配置项 | 说明 | 是否必填 | 注意事项 |
|-------------|------|----------|-----------|
| `DASHSCOPE_WORKSPACE_ID` | 绑定 RAG 知识库存储与解析的业务空间 ID | 是（SDK/API 方式） | 必须设为环境变量，确保 `DashScopeCloudIndex` 与 `DashScopeParse` 使用同一 Workspace；控制台零代码方式自动继承当前项目空间 |
| `top_k` | 检索返回的最相关文档片段数量 | 否（默认 `3`） | 建议 `2–5`：过小可能遗漏关键信息，过大易引入噪声并挤占模型上下文窗口 |
| `chunk_size` / `chunk_overlap` | 文档分块参数（仅 SDK 自定义解析时可调） | 否（默认由 `DashScopeParse` 自动优化） | 若使用自定义解析器，建议 `chunk_size=512`、`chunk_overlap=64`，平衡语义完整性与检索精度 |
| `messages` 中的检索内容位置 | 决定模型对知识的感知强度 | 是（需显式构造） | 强烈建议将检索结果放在 `system` 角色或首条 `user` 消息中，并添加明确指令（如“请严格依据以下参考内容回答，不可编造”） |

> ⚠️ 注意：百炼 RAG **不提供独立 API 接口**，所有检索逻辑必须在应用层完成（控制台自动封装，SDK 需手动调用 `retriever.retrieve()`）。流式响应（`stream=true`）与 RAG 兼容，但需确保检索步骤在流式请求发起前完成。

## 面向开发者，简洁实用

- **快速验证**：用零代码模板 5 分钟上线 RAG 应用 → 上传文档 → 发布 → 测试问答 → 确认效果后再决定是否迁移到 SDK 自定义。
- **调试技巧**：开启 `debug_mode=True`（SDK）或在控制台「监控」页查看「检索日志」，可直接看到每次请求命中的原始文档片段及相似度分数。
- **性能优化**：若响应延迟高，优先检查文档解析耗时（大 PDF 可能需数秒）；知识库更新后，需重新触发索引重建（控制台点击「刷新索引」，SDK 调用 `index.refresh()`）。
- **避坑指南**：  
  - ❌ 不要将检索结果塞入 `functions` 或 `tool_calls` 字段（RAG 非工具调用）；  
  - ❌ 不要在 `stream=true` 请求中动态执行检索（必须前置完成）；  
  - ✅ 对敏感问答场景，可在检索后增加规则过滤（如正则匹配涉政/医疗关键词），再注入模型。

## 关联主题页

- [start using](../guides/start-using.md)
- [use cases](../guides/use-cases.md)
- [model data overview](../guides/model-data-overview.md)


