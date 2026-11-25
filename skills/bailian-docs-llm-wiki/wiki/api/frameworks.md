# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于将大模型能力无缝嵌入主流开发框架（如 LlamaIndex、Spring AI 等），降低工程化接入门槛。该能力通过标准化适配层封装模型调用、流式响应、[工具调用](../concepts/tool-calling.md)等共性逻辑，开发者无需手动处理协议转换与重试策略。详细实现细节见 [框架集成](../../raw/application-api-reference/frameworks.md)。

## 支持的模型/功能

当前支持以下框架及其对应能力：
- **LlamaIndex**：支持 `LLM`、`Embedding`、`Tool` 三类组件接入，兼容 `0.10.x` 及以上版本，可直接作为 `llama_index.llms.CustomLLM` 使用；  
- **Spring AI Alibaba**：提供 `AlibabaAISpringAiChatClient` 和 `AlibabaAISpringAiEmbeddingClient`，完整支持 Spring AI 0.8.1+ 的 `ChatClient` 和 `EmbeddingClient` 接口规范；  
- 所有框架均支持同步/异步调用、流式响应（`stream=True`）、系统提示词注入及结构化输出（`response_format={"type": "json_object"}`）。更多框架扩展计划参见 [框架集成](../../raw/application-api-reference/frameworks.md)。

## 关键参数

各框架适配器统一接受以下核心参数（以 LlamaIndex 为例）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 百炼平台模型 ID（如 `qwen-max`, `qwen-plus`） |
| `api_key` | string | 否 | 若未配置环境变量 `QWEN_API_KEY`，需显式传入 |
| `base_url` | string | 否 | 默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，可覆盖为私有部署地址 |
| `temperature` | float | 否 | 默认 `0.8`，范围 `[0.0, 2.0]` |

> **注意**：Spring AI Alibaba 的 `base_url` 默认值在 [Spring AI Alibaba](../../raw/frameworks/spring-ai-alibaba.md) 中声明为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，但实际 SDK v0.8.3 已改为 `https://dashscope.aliyuncs.com/api/v1` —— 请以最新 SDK 源码为准，避免因 URL 不匹配导致 404。

## 使用方式

### LlamaIndex 示例
```python
from llama_index.llms import CustomLLM
from llamaindex_adapters import QwenLLM  # 来自 llamaindex-adapters 包

llm = QwenLLM(
    model="qwen-max",
    api_key="sk-xxx",
    temperature=0.5,
)
```

### Spring AI Alibaba 示例
```java
@Bean
public ChatClient chatClient() {
    return new AlibabaAISpringAiChatClient(
        "qwen-max", 
        "sk-xxx", 
        "https://dashscope.aliyuncs.com/api/v1"
    );
}
```

完整初始化代码和依赖版本要求详见 [LlamaIndex](../../raw/frameworks/llamaindex.md) 和 [Spring AI Alibaba](../../raw/frameworks/spring-ai-alibaba.md)。

## 限制和注意事项

- 单次请求最大 token 数受所选模型限制（如 `qwen-max` 上限为 32768），超出将触发 `400 Bad Request`；  
- 流式响应中 `delta.content` 字段可能为空（尤其在[工具调用](../concepts/tool-calling.md)阶段），需判空处理；  
- 不支持跨框架混用组件（例如将 Spring AI 的 `ChatClient` 实例传入 LlamaIndex 的 `LLM` 位置）；  
- 所有框架适配器均不内置重试逻辑，建议上层应用按需集成指数退避重试（参考 [框架集成](../../raw/application-api-reference/frameworks.md) 中的错误码说明）。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


