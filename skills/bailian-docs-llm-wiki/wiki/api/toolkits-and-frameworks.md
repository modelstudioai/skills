# toolkits and [frameworks](frameworks.md)

百炼平台提供多种主流工具包与框架的兼容接口，帮助开发者快速集成大模型能力。当前重点支持 OpenAI 兼容 API（覆盖 Chat、Vision、Embedding、Batch 等场景）及 LangChain 生态接入。所有兼容层均基于百炼原生模型能力封装，不引入额外模型或中间服务。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：支持 `chat/completions`、`embeddings`、`vision`（Qwen-VL）、`files`（上传与管理）、`batches`（异步批量请求）、`conversations`（会话状态管理）等标准端点，底层调用百炼托管的 Qwen 系列模型（如 qwen-plus、qwen-max）及专用多模态/向量模型。  
- **LangChain 集成**：提供 `BailianLLM` 和 `BailianEmbeddings` 封装类，可直接替换 LangChain 中的 `OpenAI` 类，无需修改链逻辑。具体用法见 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
- 所有 OpenAI 兼容能力均要求使用百炼平台颁发的 `api_key`，且 endpoint 域名为 `https://dashscope.aliyuncs.com/api/v1` —— 该细节在 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 和 [OpenAI兼容-Responses](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 中均有明确说明。

## 关键参数

- `model`：必须指定为百炼平台注册的模型标识符（如 `qwen-max`），**不可使用 OpenAI 的模型名（如 `gpt-4`）**；否则返回 404。  
- `api_key`：仅接受百炼平台生成的密钥，不兼容 OpenAI 密钥。  
- `base_url`：客户端需显式设置为 `https://dashscope.aliyuncs.com/api/v1`，部分旧版 LangChain 示例未强调此配置，易导致连接失败。> **注意**：[OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中给出的 Python 示例已更新 base_url，但 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md) 文档中部分代码片段仍沿用默认 OpenAI 地址，实际使用时须手动覆盖。  
- `response_format`：仅 `chat/completions` 支持 `{"type": "json_object"}`，其他端点（如 `embeddings`）不支持该参数，强行传入将被忽略。

## 使用方式

1. **HTTP 直连**：按 OpenAI API 规范构造请求，替换 `Authorization: Bearer <your_api_key>` 和 `base_url` 即可调用。  
2. **Python SDK（OpenAI 客户端）**：安装 `openai>=1.0.0`，初始化时指定 `base_url` 和 `api_key`：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key="sk-xxx",
       base_url="https://dashscope.aliyuncs.com/api/v1"
   )
   ```
3. **LangChain**：导入 `BailianLLM`，用法与 `ChatOpenAI` 一致，详见 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **不支持 streaming + function calling 组合**：`stream=True` 时 `functions` 或 `tool_choice` 参数将被静默忽略，该限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中有明确标注。  
- **Batch 接口仅支持 JSONL 格式输入文件**，且单文件上限 100MB；`batches` 端点不支持 `response_format=json_object`，与 `chat/completions` 行为不一致。  
- Vision 模型（Qwen-VL）暂不支持 `image_url` 方式传图，仅接受 `image_url.data:image/*;base64,...` 内联 base64 编码，该约束在 [OpenAI兼容-Vision](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) 中有详细说明。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


