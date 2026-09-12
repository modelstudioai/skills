# toolkits and frameworks

百炼平台提供多种主流工具包与框架的兼容接口，帮助开发者快速集成大模型能力。当前重点支持 OpenAI 兼容 API（覆盖 Chat、Completions、Vision、Embedding 等核心场景）及 LangChain 生态集成。所有接口均基于百炼统一认证与配额体系，无需额外部署模型服务。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatibility.md)**：完整支持 `chat/completions`、`completions`、`embeddings`、`vision`、`files`、`batches`（含 Batch Chat）、`conversations` 等端点，底层调用百炼托管的 Qwen 系列模型（如 qwen-max、qwen-plus、qwen-turbo），具体模型映射关系详见 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)。
- **LangChain 集成**：提供官方 `BaiLianChatModel` 和 `BaiLianEmbeddings` 封装，支持 LangChain v0.1.x 与 v0.2.x（需使用 `langchain-bailian` 0.0.8+），详细配置方式见 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)。
- **注意**：`conversations` 接口在 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 中列为支持项，但实际已由 `chat/completions` 的 `messages` + `thread_id` 模式替代；旧 `conversations` 端点将于 2024 年 Q4 下线，请尽快迁移。

## 关键参数

- 所有 [OpenAI 兼容接口](../concepts/openai-compatibility.md)共用标准参数：`model`（必填，如 `qwen-max`）、`temperature`、`max_tokens`、`top_p` 等，语义与 OpenAI 官方一致。
- Vision 接口需通过 `messages.content` 中的 `image_url` 或 `image_data` 传入 Base64 编码图像，格式要求与 [OpenAI兼容-Vision](https://help.aliyun.com/zh/model-studio/qwen-vl-compatible-with-openai) 一致。
- Batch 接口要求 `input_file_id` 必须为通过 `/files` 上传的文件 ID，且仅支持 JSONL 格式；该限制在 [OpenAI兼容-Batch（文件输入）](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai) 中明确说明。

## 使用方式

1. **API 调用**：使用百炼 API Key，将请求发往 `https://dashscope.aliyuncs.com/api/v1/` 下对应路径（如 `/chat/completions`），Header 设置 `Authorization: Bearer <api_key>`。
2. **LangChain 配置**：
   ```python
   from langchain_bailian import BaiLianChatModel
   llm = BaiLianChatModel(model_name="qwen-max", temperature=0.5)
   ```
   依赖库需显式安装：`pip install langchain-bailian>=0.0.8`。
3. 文件上传与引用：先调用 `/files` 创建文件资源，再在 `/chat/completions` 或 `/batches` 中通过 `file_id` 引用——此流程在 [OpenAI兼容-File](https://help.aliyun.com/zh/model-studio/openai-file-interface) 中有完整示例。

## 限制和注意事项

- 单次 `chat/completions` 请求最大 `messages` 数为 100，总 token 上限取决于所选模型（如 `qwen-max` 当前为 32768）。
- Embedding 接口仅支持 `text-embedding-v3` 模型，不支持自定义向量维度；其他模型名（如 `text-embedding-ada-002`）将被静默映射为默认模型。
- > **注意**：文档中列出的 [OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api) 实际为历史遗留名称，当前已统一归入 `/chat/completions` 响应格式，其独立端点不再维护。
- 所有 Batch 任务最长保留 7 天，超时后 `output_file_id` 自动失效；该策略未在 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 中说明，需以控制台提示为准。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)



