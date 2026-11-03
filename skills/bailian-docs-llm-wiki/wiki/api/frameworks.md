# frameworks

`frameworks` 是百炼平台为简化大模型应用开发而提供的框架集成能力，支持主流开源框架与百炼 API 的无缝对接。开发者可通过少量配置即可将百炼的模型服务、RAG 能力和工具调用嵌入到现有技术栈中，无需重复实现协议适配与重试逻辑。该能力目前以插件/客户端扩展形式提供，不依赖百炼 SDK 的核心运行时。

## 支持的模型与功能

当前支持以下两类框架集成：

- **LlamaIndex**：提供 `LlamaIndex` 专用的 `LLM` 和 `Embedding` 接口实现，支持同步/异步调用、流式响应、自定义 system [prompt](../guides/prompt.md) 及 metadata 透传；完整支持百炼全部文本生成模型（如 `qwen-max`、`qwen-plus`）及向量模型（如 `text-embedding-v3`）。详见 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md)。

- **Spring AI Alibaba**：面向 Spring 生态的官方适配器，兼容 Spring AI 1.0+ 标准接口，支持 `ChatClient`、`EmbeddingClient` 及 `Tool` 自动发现机制；已验证与 Spring Boot 3.2+ 兼容。其能力覆盖与 LlamaIndex 基本一致，但配置方式和生命周期管理遵循 Spring 约定。具体使用说明见 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：原始文档中未明确说明是否支持 LangChain 集成。截至当前版本（v2024.09），LangChain 官方 `langchain-community` 包暂未发布百炼适配器，相关社区 PR 尚未合入。请勿参考过时的第三方博客或非官方仓库示例——以 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md) 中列出的链接为准。

## 关键参数

所有框架集成均通过标准环境变量或配置属性注入百炼认证与路由信息：

- `QWEN_API_KEY`：必填，百炼平台生成的 API Key  
- `QWEN_BASE_URL`：选填，默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；若使用私有部署实例，需显式指定内网地址  
- `QWEN_MODEL_NAME`：选填，用于覆盖框架默认模型（如 LlamaIndex 默认用 `qwen-max`，Spring AI 默认用 `qwen-plus`）  

部分高级参数（如超时、重试策略）需通过各框架原生配置项设置（例如 LlamaIndex 的 `timeout` 参数、Spring AI 的 `spring.ai.alibaba.timeout` 属性）。

## 使用方式

1. **安装对应适配器包**：  
   - LlamaIndex：`pip install llamaindex-llms-qwen llamaindex-embeddings-qwen`  
   - Spring AI Alibaba：在 `pom.xml` 中添加 `spring-ai-alibaba-spring-boot-starter` 依赖  

2. **初始化客户端**：  
   - LlamaIndex 示例：  
     ```python
     from llama_index.llms.qwen import Qwen
     llm = Qwen(model="qwen-max", api_key=os.getenv("QWEN_API_KEY"))
     ```  
   - Spring AI 示例（`application.yml`）：  
     ```yaml
     spring:
       ai:
         alibaba:
           api-key: ${QWEN_API_KEY}
           base-url: ${QWEN_BASE_URL}
     ```  

3. 在框架标准流程中直接使用（如 `llm.complete()` 或 `chatClient.call()`），无需额外封装。

## 限制和注意事项

- 所有集成均**不支持**百炼控制台中“自定义模型”（即用户上传的 LoRA 或全量微调模型）；仅支持平台预置的公开模型。
- 流式响应（streaming）在 Spring AI Alibaba 中需显式启用 `StreamingChatClient`，且部分 Spring Boot 版本存在 Reactor 兼容性问题，请参考 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 的 “Known Issues” 小节。
- LlamaIndex v0.10.45+ 引入了对 `tool_choice` 的自动解析，但百炼当前 API 尚未完全支持 OpenAI-style tool calling 规范，调用含 `tools` 参数的请求可能被静默忽略——此行为差异已在 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md) 的更新日志中标注。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


