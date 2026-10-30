# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于简化主流 AI 应用开发框架（如 LlamaIndex、Spring AI）与百炼模型服务的对接。它通过标准化适配层屏蔽底层 API 差异，使开发者可复用原有框架代码快速接入百炼模型。该能力不提供独立 API 接口，而是以 SDK 集成和配置驱动方式生效。

## 支持的模型/功能

当前支持以下两类框架集成：
- **LlamaIndex**：支持 `LLM`、`Embedding`、`Retriever` 等核心组件对接，兼容 `llama-index-core>=0.10.0`；支持同步/异步调用及流式响应透传。详细用法见 [框架集成](../../raw/application-api-reference/frameworks.md)。
- **Spring AI Alibaba**：提供 `AlibabaAIClient` 和 `AlibabaEmbeddingClient`，适配 Spring AI 0.8.x+ 的抽象接口，支持自动注入与 `application.yml` 配置驱动。具体配置项和依赖版本请参考 [框架集成](../../raw/application-api-reference/frameworks.md)。

## 关键参数

所有框架集成均通过环境变量或配置文件统一控制行为：
- `QWEN_API_KEY`：必填，用于身份认证（部分框架也支持显式传入）；
- `QWEN_BASE_URL`：可选，用于指定百炼 API 地址，默认为 `https://dashscope.aliyuncs.com/api/v1`；
- `QWEN_MODEL_NAME`：可选，指定默认模型（如 `qwen-max`），若框架中已显式指定则以框架为准；
- `QWEN_TIMEOUT`：可选，单位秒，默认 60。

> **注意**：`QWEN_MODEL_NAME` 在 Spring AI Alibaba 中实际被映射为 `model` 属性，而 LlamaIndex 中需通过 `model_name` 参数显式传递——二者语义一致但配置路径不同，详见 [框架集成](../../raw/application-api-reference/frameworks.md)。

## 使用方式

1. **安装对应 SDK**：  
   - LlamaIndex：`pip install llama-index-core llama-index-llms-qwen`  
   - Spring AI Alibaba：添加 `spring-ai-alibaba-spring-boot-starter` 依赖（Maven 坐标见 [框架集成](../../raw/application-api-reference/frameworks.md)）

2. **配置认证与模型**：  
   设置环境变量或在框架配置文件中声明（如 `application.yml` 或 `Settings.llm`）。

3. **初始化并使用**：  
   框架内直接构造 LLM/Embedding 实例，无需手动处理 HTTP 请求或 token 刷新。

## 限制和注意事项

- 不支持自定义模型微调后的私有部署模型接入（仅限百炼平台托管的公开模型）；
- LlamaIndex 的 `QueryEngine` [流式输出](../concepts/streaming-output.md)需配合 `streaming=True` 及 `response_gen` 迭代器，Spring AI 则需启用 `StreamingChatClient`；
- 所有请求受百炼平台 [API 速率限制](../../raw/rate-limiting.md) 约束，超限返回 `429`；
- > **注意**：原始文档中提及的 `llama-index-llms-dashscope` 包名已废弃，当前应使用 `llama-index-llms-qwen`（参见 [框架集成](../../raw/application-api-reference/frameworks.md)），旧包无法连接新版百炼服务。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


