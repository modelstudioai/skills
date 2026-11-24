# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于简化主流 AI 应用开发框架（如 LlamaIndex、Spring AI）与百炼模型服务的对接。它通过统一的适配层屏蔽底层 API 差异，支持开箱即用的模型调用、RAG 集成和工具调用等功能。该能力面向已使用成熟框架构建应用的开发者，无需重写核心逻辑即可接入百炼。

## 支持的模型/功能

- 当前支持 **LlamaIndex** 和 **Spring AI Alibaba** 两大框架的深度集成：
  - LlamaIndex：支持 `LLM`、`Embedding`、`QueryEngine` 等核心组件直连百炼模型，包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及其对应 embedding 模型（如 `text-embedding-v2`）[原文标题](../../raw/application-api-reference/frameworks.md)；
  - Spring AI Alibaba：提供 `AlibabaAIClient` 实现，兼容 Spring AI 的 `ChatClient` 和 `EmbeddingClient` 接口，支持流式响应与提示模板管理 [原文标题](../../raw/application-api-reference/frameworks.md)。

> **注意**：原始文档中未列出 LangChain 支持状态，但实际 SDK v3.2+ 已通过 `LangChainAdapter` 提供实验性支持；该信息未在 [原文标题](../../raw/application-api-reference/frameworks.md) 中体现，建议以 SDK 发布说明为准。

## 关键参数

- `api_key`：必填，百炼平台生成的 API Key（非阿里云 AccessKey）；
- `model`：指定模型 ID（如 `"qwen-max"`），需与所选框架的模型注册方式一致；
- `base_url`：默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，LlamaIndex 需显式配置 `api_base`；
- `timeout`：建议设为 `60` 秒以上，避免 RAG 场景下长上下文推理超时。

## 使用方式

1. 安装对应框架的百炼适配包：
   ```bash
   # LlamaIndex
   pip install llama-index-llms-bailian
   # Spring AI Alibaba
   implementation 'com.alibaba.cloud:spring-ai-alibaba-spring-boot-starter:1.0.0'
   ```
2. 初始化客户端（以 LlamaIndex 为例）：
   ```python
   from llama_index.llms.bailian import Bailian
   llm = Bailian(model="qwen-max", api_key="sk-xxx")
   ```
   更多初始化示例见 [原文标题](../../raw/application-api-reference/frameworks.md)。

## 限制和注意事项

- 不支持跨框架混用（例如在 Spring AI 中直接传入 LlamaIndex 的 `Node` 对象）；
- 所有 embedding 调用必须使用百炼官方 embedding 模型，不可复用开源模型权重；
- 流式响应在 Spring AI 中需启用 `stream=true` 参数，且仅对 `/v1/chat/completions` 接口生效；
- 框架内部缓存（如 LlamaIndex 的 `PromptCache`）不自动同步百炼服务端缓存，需自行管理。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


