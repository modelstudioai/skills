# application [use cases](use-cases.md)

本节汇总百炼平台支持的典型应用落地场景，涵盖嵌入式AI助手、企业IM集成、智能客服及RAG类应用。所有用例均基于平台提供的标准API与SDK能力实现，无需从零训练模型。开发者可结合业务需求快速复用已有实践路径。

## 支持的模型/功能

- 所有通义千问系列大模型（Qwen1.5、Qwen2、Qwen2.5）均支持上述用例，其中RAG场景推荐使用 `qwen2.5-72b-instruct` 或 `qwen2.5-32b-instruct` 以获得更优检索后生成效果  
- 基础文本生成、多轮对话、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应、系统提示词（system [prompt](prompt.md)）注入等功能全部可用  
- RAG相关能力（如文档切片、向量索引构建、混合检索）由平台统一托管，详见 [实践教程](../../raw/application-user-guide/application-use-cases.md)

## 关键参数

- `model`: 必填，指定模型ID（如 `qwen2.5-7b-instruct`），不同场景对模型尺寸和推理延迟有差异要求  
- `top_p` / `temperature`: 推荐在智能客服类场景中设为 `0.3–0.6` 以保障回复稳定性；创意生成类可放宽至 `0.8–0.95`  
- `enable_search`（RAG专用）：设为 `true` 启用知识库检索，需配合 `retrieval_config` 指定知识库ID；该参数在 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中有完整配置示例  
- `stream`: 所有场景均支持[流式输出](../concepts/streaming-output.md)，但企业微信/钉钉等IM集成需注意其消息长度限制（单条≤2000字符），建议启用 `stream=true` 并做分段处理

## 使用方式

1. **嵌入式AI助手**：通过前端SDK加载轻量版 `@alibaba/bailian-js-sdk`，调用 `createChatSession()` 初始化会话，参考 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中“在网站上增加一个AI助手”步骤  
2. **IM集成（企微/钉钉/公众号）**：后端接收IM平台Webhook事件 → 调用百炼 `/v1/chat/completions` API → 将响应按IM协议格式封装返回；各平台鉴权与消息格式差异较大，务必对照对应文档校验  
3. **RAG应用**：先调用 `/v1/knowledge_bases/{kb_id}/documents` 导入本地PDF/Word/Markdown文件 → 再在请求中启用 `enable_search` 并传入 `retrieval_config` → 平台自动完成检索+LLM生成闭环  

## 限制和注意事项

- 单次请求最大上下文长度取决于所选模型（如 `qwen2.5-7b-instruct` 为32K tokens），超出部分将被截断，RAG场景需特别关注检索结果总token数  
- 企业微信/钉钉机器人需单独申请并配置可信域名与IP白名单，未配置将导致回调失败；该要求在官方帮助中心有明确说明，但 [实践教程](../../raw/application-user-guide/application-use-cases.md) 未强调，开发时请务必补全  
- > **注意**：原始文档中“10分钟实现微信公众号智能客服”链接指向的帮助中心页面已更新为新版接入流程（含新OAuth2.0鉴权机制），旧版[Token](../concepts/token.md)直连方式自2024年9月起不再支持，请以最新帮助文档为准  
- 知识库文档上传后需等待索引构建完成（通常<2分钟），期间发起的RAG请求可能返回空检索结果；可通过 `/v1/knowledge_bases/{kb_id}` 查询 `status: "active"` 确认就绪

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


