# frameworks

`frameworks` 是百炼平台提供的框架集成能力，用于简化主流 AI 应用开发框架（如 LlamaIndex、Spring AI）与百炼模型服务的对接。它通过标准化适配层屏蔽底层 API 差异，支持开箱即用的模型调用、RAG 集成及流式响应处理。该能力面向已使用成熟框架构建应用的开发者，无需修改核心业务逻辑即可接入百炼。

## 支持的模型/功能

- 当前支持 **LlamaIndex**（v0.10.35+）和 **Spring AI Alibaba**（v0.8.1+）两个框架的深度集成；
- 功能覆盖：同步/异步模型调用、Embedding 服务注入、Retriever 配置、StreamingCallbackHandler 回调注册；
- 所有集成均默认启用百炼的 token 自动续期、请求重试与错误码映射机制。详细能力请参阅 [框架集成](../../raw/application-api-reference/frameworks.md)。

## 关键参数

- `api_key`：必填，百炼平台生成的 API Key（非 AccessKey），需通过环境变量 `QWEN_API_KEY` 或显式传入；
- `model`：指定百炼模型 ID（如 `qwen-max`, `qwen-plus`），LlamaIndex 中需通过 `llm=QwenLLM(model="qwen-max")` 设置；
- `stream`：布尔值，控制是否启用流式响应（仅 Spring AI Alibaba 支持 `StreamingChatClient` 显式启用）；
- `timeout`：全局超时（秒），默认 60，建议在高延迟场景下调大；更多参数说明见 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 和 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 文档。

## 使用方式

1. 安装对应框架适配包：
   ```bash
   pip install llamaindex-qwen  # LlamaIndex 专用
   # 或
   mvn dependency:add -DgroupId=com.alibaba.spring.ai -DartifactId=spring-ai-alibaba-spring-boot-starter -Dversion=0.8.1
   ```
2. 初始化客户端并注入百炼服务（以 LlamaIndex 为例）：
   ```python
   from llamaindex_qwen import QwenLLM
   llm = QwenLLM(model="qwen-max", api_key="sk-xxx")
   ```
3. 后续调用与原生框架一致，无需额外封装。完整示例可参考 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md)。

## 限制和注意事项

- 不支持跨框架混用（例如在 Spring AI 中直接使用 `QwenLLM` 类）；
- LlamaIndex 的 `QwenEmbedding` 仅兼容 `text-embedding-v2` 模型，不支持 `text-embedding-v1`（后者已下线）；
- > **注意**：[Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 文档中提及的 `alibaba.qwen.model` 配置项在 v0.8.1+ 已废弃，应统一使用 `spring.ai.alibaba.chat.options.model`，避免配置失效；
- 单次请求最大上下文长度受所选模型限制（如 `qwen-max` 为 32768 tokens），超出将触发截断且无警告；
- 流式响应中 `delta.content` 字段可能为空字符串（尤其在首 chunk），需做空值判断。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


