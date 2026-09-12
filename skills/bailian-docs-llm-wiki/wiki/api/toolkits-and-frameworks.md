# toolkits and frameworks

百炼平台提供多种主流工具包与框架的兼容接口，帮助开发者快速集成大模型能力。当前重点支持 OpenAI 兼容 API（覆盖 Chat、Completions、Vision、Embedding 等核心场景）及 LangChain 生态接入。所有接口均基于百炼统一认证与配额体系，无需额外部署模型服务。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**：完整支持 `chat/completions`、`completions`、`embeddings`、`vision`、`files`、`batches`（含 Batch Chat 与文件批量处理）、`conversations` 等端点，底层调用百炼托管的 Qwen 系列模型（如 qwen-max、qwen-plus、qwen-turbo）。  
- **LangChain 集成**：提供官方 `BaiLianChatModel` 和 `BaiLianEmbeddings` 封装，支持 `llm.invoke()`、`embed_documents()` 等标准方法，[LangChain](../../raw/model-api-reference/toolkits-and-frameworks.md) 文档中包含完整示例。  
- 所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)均默认启用流式响应（`stream=true`），且支持 `response_format`（JSON Schema）等高级参数，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks.md) 和 [OpenAI兼容-Responses](../../raw/model-api-reference/toolkits-and-frameworks.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 必填，指定百炼模型 ID | `"qwen-max"`、`"qwen-turbo"` |
| `api_key` | 使用百炼平台 AccessKey（非 OpenAI key） | `"sk-xxx"`（需通过控制台获取） |
| `base_url` | [OpenAI 兼容接口](../concepts/openai-compatible-api.md)固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1` | — |
| `response_format` | 仅部分模型支持（如 `qwen-max`），需配合 `response_format.type="json_object"` 使用 | `{"type": "json_object"}` |

> **注意**：`temperature`、`top_p` 等采样参数在 [OpenAI兼容-Completions](../../raw/model-api-reference/toolkits-and-frameworks.md) 中明确支持，但在 [OpenAI兼容-Vision](../../raw/model-api-reference/toolkits-and-frameworks.md) 的当前版本中暂不生效（2024.06 文档已标注“参数忽略”，请以实际调用返回为准）。

## 使用方式

1. **OpenAI 兼容调用**（Python）：
   ```python
   from openai import OpenAI
   client = OpenAI(api_key="sk-xxx", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
   response = client.chat.completions.create(
       model="qwen-max",
       messages=[{"role": "user", "content": "你好"}]
   )
   ```

2. **LangChain 集成**（需安装 `langchain-bailian`）：
   ```python
   from langchain_bailian import BaiLianChatModel
   llm = BaiLianChatModel(model_name="qwen-plus", temperature=0.3)
   llm.invoke("解释量子纠缠")
   ```

## 限制和注意事项

- 所有 OpenAI 兼容接口**不支持自定义模型权重上传或微调**，仅限调用百炼平台预置模型。
- `batches` 接口要求输入文件必须为 `.jsonl` 格式，且每行符合 `/v1/chat/completions` 请求体结构；[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks.md) 明确要求 `input_file_id` 须先通过 `/files` 上传。
- Vision 接口仅支持 Base64 编码图像（`data:image/png;base64,...`），不支持 URL 或本地路径；该限制在 [OpenAI兼容-Vision](../../raw/model-api-reference/toolkits-and-frameworks.md) 中有详细说明。
- LangChain 封装暂不支持 `structured_output`（Pydantic 模式），如需结构化输出，请改用原生 OpenAI 兼容接口并设置 `response_format`。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


