# frameworks

`frameworks` 是百炼平台为简化大模型应用开发而提供的框架集成能力，支持主流开源框架与百炼 API 的快速对接。开发者可通过标准接口调用百炼的模型服务、工具调用、RAG 等能力，无需手动封装 HTTP 请求或处理鉴权细节。该能力目前以插件/适配器形式提供，需配合对应框架版本使用。

## 支持的模型/功能

当前支持通过框架集成调用以下核心能力：
- 百炼全量托管模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）的文本生成；
- 内置 RAG 检索增强（需配合 `llamaindex` 的 `QwenRetriever` 或 `Spring AI Alibaba` 的 `QwenEmbeddingClient`）；
- 工具调用（Function Calling）和结构化输出（JSON Schema）；
- 流式响应（`stream=true`）及[异步任务](../concepts/asynchronous-task.md)提交（`async=true`）。

> **注意**：`Spring AI Alibaba` 文档中声明支持 `qwen-vl` 多模态模型，但 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md) 未列出该模型，且实测 v0.9.2 版本 SDK 会返回 `model_not_supported` 错误——请以 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 文档中明确列出的模型列表为准。

## 关键参数

所有框架集成均透传以下关键参数（命名与百炼 OpenAPI 一致）：
- `model`: 必填，模型 ID（如 `"qwen-max"`）；
- `temperature`: 控制随机性（0.0–2.0，默认 1.0）；
- `top_p`: 核采样阈值（0.0–1.0，默认 0.8）；
- `max_tokens`: 输出最大 token 数（默认 2048，上限 8192）；
- `tools`: 工具定义数组（仅当启用 Function Calling 时有效）；
- `response_format`: 可设为 `{"type": "json_object"}` 启用 JSON 结构化输出。

## 使用方式

1. **安装适配器包**：  
   - LlamaIndex：`pip install llama-index-llms-bailian`  
   - Spring AI Alibaba：`implementation 'com.alibaba.spring.ai:spring-ai-alibaba-spring-boot-starter:0.9.2'`

2. **初始化客户端**（以 LlamaIndex 为例）：  
   ```python
   from llama_index.llms.bailian import Bailian
   llm = Bailian(
       model="qwen-max",
       api_key="YOUR_API_KEY",
       endpoint="https://dashscope.aliyuncs.com/compatible-mode/v1"
   )
   ```

3. **调用示例**：  
   ```python
   response = llm.complete("你好，请用中文简要介绍百炼平台。")
   print(response.text)
   ```

详细配置项与框架特有方法请参考 [Spring AI Alibaba](../../raw/application-api-reference/frameworks/spring-ai-alibaba.md) 和 [LlamaIndex](../../raw/application-api-reference/frameworks/llamaindex.md) 的独立文档。

## 限制和注意事项

- 所有框架集成均**不支持自定义模型微调部署**，仅限调用百炼平台托管的公开模型；
- 流式响应在 Spring AI Alibaba 中需显式启用 `StreamingChatClient`，而 LlamaIndex 默认支持 `stream=True` 参数；
- 跨区域访问（如华东节点调用华北模型）可能触发额外延迟，建议将 `endpoint` 显式指定为与模型部署区匹配的域名；
- 若遇到 `401 Unauthorized`，请确认 `api_key` 具备 `bailian:InvokeModel` 权限，并检查是否误用了 DashScope 的全局密钥而非百炼专属密钥——该问题在 [框架集成 (raw/application-api-reference/frameworks.md)](../../raw/application-api-reference/frameworks.md) 的 FAQ 部分有明确说明。

## 来源文档

- [框架集成](../../raw/application-api-reference/frameworks.md)


