# application [use cases](use-cases.md)

`application use cases` 描述了百炼平台支持的典型端到端应用场景，覆盖从轻量级嵌入式助手到基于私有知识的智能问答系统。这些用例均基于平台提供的标准化 API、SDK 及低代码集成能力实现，开发者可按需选择部署方式与模型组合。所有场景均已在 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中提供可复现的操作路径。

## 支持的模型/功能

- 支持调用通义千问系列大模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）进行对话生成、摘要、推理等任务；  
- 支持 RAG（[检索增强生成](../concepts/rag.md)）模式，可通过 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中“基于本地知识库构建RAG应用”一节配置向量检索+LLM 串联流程；  
- 提供预置插件能力（如网页搜索、数据库查询），部分插件需配合 `qwen-max` 或 `qwen-plus` 使用，详见 [实践教程](../../raw/application-user-guide/application-use-cases.md) 所列各集成指南。

## 关键参数

- `model`: 必填，指定模型 ID（如 `"qwen-turbo"`），不同用例对模型能力要求不同：微信公众号客服推荐 `qwen-turbo`（低延迟），RAG 场景建议 `qwen-plus`（更强长上下文与工具调用）；  
- `enable_search` / `retrieval_config`: 控制是否启用外部检索，RAG 场景必须配置 `retrieval_config` 并关联已创建的知识库 ID；  
- `system_prompt`: 可选，用于定义角色与行为约束，企业微信/钉钉机器人建议显式设置以保障输出一致性。

## 使用方式

1. **嵌入式助手（网站/公众号/企微/钉钉）**：通过平台生成的 Web SDK URL 或 Bot [Token](../concepts/token.md) + 回调地址接入，无需自行托管模型服务；  
2. **RAG 应用**：在控制台创建知识库 → 上传文档并完成向量化 → 在应用中启用检索并绑定知识库；  
3. 所有场景均通过 `/v1/chat/completions` 统一 API 调用，请求体结构与 OpenAI 兼容，具体字段说明见 [实践教程](../../raw/application-user-guide/application-use-cases.md) 对应链接中的示例代码。

## 限制和注意事项

- 单次请求最大 `input_tokens + output_tokens` 不超过 32768（`qwen-max`）或 8192（`qwen-turbo`），RAG 场景需预留 token 给检索结果拼接；  
- 知识库检索仅支持 `.pdf`, `.docx`, `.txt`, `.md` 等常见格式，图片/PPT 中文字需先 OCR 处理（平台暂不内置 OCR）；  
> **注意**：原始文档中“在网站上增加一个AI助手”指南提及支持直接粘贴 HTML 片段快速部署，但该方式已于 v2.3.0 后弃用，当前必须通过 SDK 初始化脚本加载，最新集成方式请参考控制台「应用发布」页提示。

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


