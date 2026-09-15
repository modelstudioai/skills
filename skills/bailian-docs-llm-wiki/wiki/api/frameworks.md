# frameworks

`frameworks` 是百炼平台提供的模型集成框架支持模块，用于简化主流 AI 开发框架与百炼大模型服务（如 Qwen 系列）的对接。它不提供独立 API，而是通过预置适配器封装认证、请求路由、流式响应解析等共性逻辑，降低 LlamaIndex、Spring AI Alibaba 等框架的接入成本。详细实现和配置说明见 [框架](../../raw/application-api-reference/frameworks.md)。

## 支持的模型/功能

当前支持以下两类框架集成：
- **LlamaIndex**：提供 `LlamaIndex` 专用的 `LLM` 接口实现，兼容 `llama-index-core>=0.10.0`，支持同步/异步调用、流式生成、工具调用（Tool Calling）及结构化输出（JSON mode）。具体能力参见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)。
- **Spring AI Alibaba**：作为 Spring AI 的官方扩展，提供 `AlibabaAIChatClient` 和 `AlibabaAIEmbeddingClient`，完整支持百炼的 chat/completion 和 embedding 接口，并兼容 Spring Boot 自动配置。使用细节请参考 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

> **注意**：原始文档中未明确说明对 LangChain 的支持；若需 LangChain 集成，请直接使用百炼标准 REST API 或 `qwen-sdk`，而非本 `frameworks` 模块——该限制在 [框架](../../raw/application-api-reference/frameworks.md) 中未被提及，属隐含约束。

## 关键参数

所有框架适配器均继承统一参数体系，核心参数包括：
- `model`: 必填，指定百炼模型 ID（如 `qwen-max`, `qwen-plus`），需与所选框架的模型注册机制一致；
- `api_key`: 可选，若未配置全局凭证，则需显式传入；
- `base_url`: 可选，用于指向私有部署实例（如 `https://your-domain/v1`）；
- `stream`: 布尔值，控制是否启用流式响应（部分框架如 Spring AI Alibaba 默认关闭，需手动启用）。

参数优先级为：调用时传入 > 初始化时传入 > 环境变量（`QWEN_API_KEY`, `QWEN_BASE_URL`）。完整参数定义以 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 中的 `QwenLLM` 类签名为准。

## 使用方式

1. 安装对应框架的百炼扩展包：
   ```bash
   # LlamaIndex 用户
   pip install llama-index-llms-qwen

   # Spring AI Alibaba 用户
   ./gradlew dependencies --include spring-ai-alibaba-spring-boot-starter
   ```
2. 初始化客户端并传入必要参数（示例以 LlamaIndex 为主）：
   ```python
   from llama_index.llms.qwen import QwenLLM
   llm = QwenLLM(model="qwen-plus", api_key="sk-xxx")
   ```
3. 在框架原生流程中直接使用（如 LlamaIndex 的 `Settings.llm = llm` 或 Spring AI 的 `ChatClient.create(...)`）。

更多初始化模式和错误处理示例见 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md)。

## 限制和注意事项

- 不支持跨框架混用（例如将 `QwenLLM` 实例传给 Spring AI 的 `ChatClient`）；
- 所有适配器默认启用重试（3 次）和指数退避，但超时时间不可配置（硬编码为 60s），如需自定义请绕过框架层直调 SDK；
- 流式响应在 LlamaIndex 中返回 `StreamingResponse` 对象，在 Spring AI 中需显式调用 `stream()` 方法，行为差异详见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 与 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 的对比说明；
- 百炼平台不保证对旧版框架（如 LlamaIndex < 0.10.0 或 Spring AI < 0.8.0）的向后兼容性。

## 来源文档

- [框架](../../raw/application-api-reference/frameworks.md)


