# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议，严格遵循 OpenAI RESTful 接口规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/images/generations` 等路径），支持使用标准 OpenAI SDK（Python/Node.js/Java/Go）或任意 HTTP 客户端直接调用百炼托管的全栈模型能力，无需修改业务代码逻辑，仅需替换 `base_url` 和 `model` 即可完成迁移。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与原型验证**：开发者可复用现有基于 OpenAI SDK 的代码（如 LangChain、LlamaIndex、Hermes Agent、Cursor、Dify 等），将 `openai.base_url` 改为百炼的兼容模式地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并指定百炼支持的模型名（如 `"qwen3.8-max"`），即可立即调用文本、[多模态](multi-modal.md)、嵌入、工具调用等能力。
  
- **[多模态](multi-modal.md)开发**：通过 OpenAI Vision 兼容接口（`/v1/chat/completions` + `image_url`），调用 `qwen3-vl-plus`、`qwen-vl-ocr` 等模型实现图像理解、OCR 结构化提取；注意需显式传入 `enable_multimodal=true`（部分客户端如 Postman 需手动添加）。

- **向量与检索场景**：使用 `/v1/embeddings` 接口调用 `text-embedding-v4` 或 `qwen3.7-text-embedding`，参数、响应格式与 OpenAI 完全一致，可无缝接入现有 RAG 流程。

- **智能体（Agent）构建**：通过 OpenAI Responses 兼容接口（`/v1/responses`），启用 `tools` 数组和 `previous_response_id` 实现多轮工具调用（如 `web_search`、`code_interpreter`），支持自动上下文管理，替代手动维护 `messages`。

- **批量与文件处理**：通过 OpenAI Batch 兼容接口（`/v1/batch/chat/completions`）提交文件 ID 批量推理，适用于文档分析、报告生成等离线任务；注意 `qwen3.5-omni-plus` 等模型在 Batch 场景下不支持语音输出。

> ⚠️ 例外说明：`Qwen-Audio`、`Qwen-Deep-Research` 明确不支持 OpenAI 兼容接口，必须使用 DashScope 原生协议调用。

## 关键参数和配置

| 参数 | 必填 | 说明 | 示例值 | 注意事项 |
|------|------|------|--------|----------|
| `base_url` | 是 | OpenAI 兼容接口的接入地址，**必须匹配 API Key 所属地域与业务空间** | `https://dashscope.aliyuncs.com/compatible-mode/v1`（通用域名）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（推荐，更高稳定性） | 旧域名仍可用但不推荐；不同地域不可混用（如北京 Key 不能调新加坡 URL） |
| `api_key` | 是 | 百炼平台颁发的 `DASHSCOPE_API_KEY`，非阿里云主账号 AK/SK | `"sk-xxxxxxxx"` | 必须通过 `Authorization: Bearer <api_key>` 请求头传递；严禁硬编码于客户端 |
| `model` | 是 | 模型 ID，**严格区分大小写、空格与版本号**，不可使用开源别名（如 `Qwen/Qwen3-235B`） | `"qwen3.8-max"`, `"qwen3-vl-plus"`, `"text-embedding-v4"`, `"farui-plus"` | 查看控制台「模型市场」确认开通状态；未开通模型将返回 `Model not exist` 错误 |
| `stream` | 否 | 是否启用流式响应（SSE） | `true` / `false` | 流式时需按 `text/event-stream` 解析；思考模式模型（如 `qwen3.8-max`）建议设为 `true` |
| `enable_multimodal` | 否 | [多模态](multi-modal.md)输入必需参数（仅对 `qwen-vl-*`、`qwen3-vl-*` 等生效） | `true` | 部分客户端（如 QwenPaw）会静默忽略该参数，需优先选用明确声明支持的工具（如 Cherry Studio） |
| `previous_response_id` | 否 | Responses API 专用，用于自动注入历史上下文 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` | 替代手动拼接 `messages`，提升多轮对话可靠性 |
| `tools` | 否 | 工具定义数组（函数描述），仅 Responses 和 Anthropic 接口完整支持内置工具 | `[{"type": "function", "function": {...}}]` | OpenAI Chat 接口仅支持基础 `function_call`，无 `web_search` 等内置工具 |

## 面向开发者，简洁实用

- ✅ **三步启动**：  
  1. `pip install -U openai`（或对应语言 SDK）  
  2. 设置环境变量 `export DASHSCOPE_API_KEY=sk-xxxx`  
  3. 初始化客户端：  
     ```python
     from openai import OpenAI
     client = OpenAI(
         base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
         api_key=os.getenv("DASHSCOPE_API_KEY")
     )
     response = client.chat.completions.create(
         model="qwen3.8-max",
         messages=[{"role": "user", "content": "你好"}]
     )
     print(response.choices[0].message.content)
     ```

- ✅ **调试技巧**：  
  - 使用 `dashscope` CLI 的 `dashscope chat --model qwen-plus --stream` 快速验证兼容性；  
  - 响应中 `id`、`object`、`created`、`usage` 字段与 OpenAI 完全一致，可直接复用日志/监控逻辑；  
  - 错误码（如 `401 Unauthorized`、`404 Model not exist`、`429 Rate limit exceeded`）语义与 OpenAI 对齐，便于统一错误处理。

- ❌ **避坑提醒**：  
  - 不要混用协议：`qwen-deep-research` 等模型不支持 OpenAI 接口，强行调用将返回 `404`；  
  - 不要省略 `base_url`：默认指向 `https://api.openai.com/v1`，会导致请求失败；  
  - 不要忽略地域隔离：API Key、`base_url`、模型开通地域必须三者一致。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more models](../api/more-models.md)


