# frameworks

百炼平台提供对主流 AI 应用框架的原生集成支持，使开发者能快速将百炼大模型能力嵌入现有技术栈。当前重点支持 LlamaIndex 和 Spring AI Alibaba 两大框架，通过标准化适配层屏蔽底层 API 差异。所有集成均基于百炼统一的 `model`、`api_key` 和 `endpoint` 抽象，确保行为一致性。

## 支持的模型/功能

- **LlamaIndex**：支持 `LLM`、`Embedding`、`Retriever` 等核心组件接入，可直接使用百炼的 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `bge-m3` 等模型；支持流式响应与自定义 system prompt。详情见 [框架集成](../../raw/application-api-reference/frameworks.md)。
- **Spring AI Alibaba**：提供 `AlibabaAIClient` 实现，兼容 Spring AI 的 `ChatClient` 和 `EmbeddingClient` 接口，支持自动重试、超时配置及 OpenTelemetry 追踪。该实现已通过 Spring AI 1.0.x 全系列兼容性验证，具体能力参见 [框架集成](../../raw/application-api-reference/frameworks.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID（如 `qwen-max`），必须与百炼控制台开通的模型一致 |
| `api_key` | string | 是 | 百炼平台生成的 API Key，需具备对应模型调用权限 |
| `endpoint` | string | 否 | 自定义 endpoint（如私有化部署地址），默认使用百炼公共 endpoint |
| `timeout` | int | 否 | 单位毫秒，默认 60000（60 秒） |

> **注意**：Spring AI Alibaba 文档中曾提及 `region_id` 参数，但该字段在 v1.0.2+ 版本中已被移除，实际运行时传入将被忽略——请以 [框架集成](../../raw/application-api-reference/frameworks.md) 中最新代码示例为准。

## 使用方式

1. 添加对应框架依赖（如 LlamaIndex 的 `llama-index-llms-bailian` 或 Spring AI Alibaba 的 `spring-ai-alibaba-spring-boot-starter`）；
2. 初始化客户端时传入 `api_key`、`model` 等必要参数；
3. 直接调用框架标准接口（如 `llm.complete()` 或 `chatClient.call()`），无需额外封装。

示例（LlamaIndex）：
```python
from llama_index.llms.bailian import Bailian
llm = Bailian(model="qwen-max", api_key="sk-xxx")
response = llm.complete("你好")
```

## 限制和注意事项

- 单次请求最大 token 数受所选模型自身限制（如 `qwen-turbo` 上限为 8192），超出将返回 `400 Bad Request`；
- 流式响应仅支持 `text/event-stream` 格式，不支持 `application/json` 分块；
- 所有框架集成均**不支持**百炼的 `tools` 调用能力（即[函数调用](../concepts/function-calling.md)），该能力需直接调用百炼 `/v1/chat/completions` 原生 API —— 详见 [框架集成](../../raw/application-api-reference/frameworks.md)。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


