# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 RESTful API 协议，语义与 OpenAI 官方 v1 接口（如 `/v1/chat/completions`、`/v1/embeddings`）保持高度一致，使开发者可复用现有 OpenAI SDK、框架适配器或工具链，零代码改造即可接入百炼的模型能力、智能体应用及向量服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用（LLM）**：通过 `https://dashscope.aliyuncs.com/compatible-mode/v1` 或工作区专属 endpoint（如 `https://{workspace-id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），使用标准 OpenAI Python SDK（`openai==1.0+`）调用 `client.chat.completions.create()`，支持 `qwen-max`、`qwen-plus` 等全量 Qwen 系列模型，兼容 system/user/assistant 消息格式、`tools` 工具调用、`stream=True` 流式响应等核心能力。

- **智能体与工作流调用（Application Call）**：在 OpenAI 兼容的 *Responses API* 模式下，通过 `POST /v1/apps/{app_id}/chat/completions` 调用已发布的智能体或工作流应用。输入统一使用 `messages` 数组（支持多轮对话与多模态内容），并可通过 `input_image`、`input_file` 字段传递图像或文件；启用异步任务只需设置 `background=true`，返回 `task_id` 后轮询结果。

- **向量与排序服务（Embedding / Rerank）**：文本向量化服务（如 `qwen3.7-text-embedding`）支持 OpenAI 兼容模式，调用 `client.embeddings.create(input=..., model=...)` 即可；但多模态向量（`qwen3-vl-embedding`）和排序（`qwen3-rerank`）暂不提供 OpenAI 兼容路由，需使用 DashScope 原生接口。

> ✅ 提示：所有 OpenAI 兼容接口均要求 `Authorization: Bearer <DASHSCOPE_API_KEY>`，不接受 `QWEN_API_KEY`；API Key 必须为 DashScope 类型，且需在控制台开通对应服务权限。

## 关键参数和配置

| 参数 | 说明 | 是否必填 | 备注 |
|------|------|----------|------|
| `model` | 百炼模型 ID（如 `qwen-max`、`qwen3.7-text-embedding`） | 是 | 必须与所选服务类型匹配；不支持别名或通配符 |
| `base_url` | OpenAI 兼容 endpoint 地址 | 否（推荐显式指定） | 默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；跨地域或需 Workspace 隔离时，应替换为工作区专属地址（如 `https://{workspace-id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`） |
| `api_key` | DashScope API Key | 否（SDK 自动读取环境变量） | 推荐设为环境变量 `DASHSCOPE_API_KEY`；若手动传参，需确保密钥未硬编码 |
| `stream` | 是否启用流式响应 | 否（默认 `false`） | 设为 `true` 时，响应为 SSE 格式；客户端需按 `data:` 行解析 `delta.content` 和 `finish_reason` |
| `tools` / `tool_choice` | 工具调用声明 | 否（仅模型支持且需启用时） | 仅 `qwen-max`、`qwen-plus` 等支持 tools 的模型生效；`tool_choice="auto"` 或 `{"type": "function", "function": {"name": "xxx"}}` 均受支持 |
| `input_image` / `input_file` | 多模态输入（仅 Application Call） | 否（按需） | `input_image` 接收 base64 编码字符串或公开 URL；`input_file` 接收文件 URL（需提前上传至百炼文件服务并获取有效链接） |

## 面向开发者：简洁实用提示

- ✅ **快速验证**：用 curl 一行测试  
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen-max","messages":[{"role":"user","content":"你好"}]}'
  ```

- ✅ **SDK 接入（Python）**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen-max",
      messages=[{"role": "user", "content": "写一首五言绝句"}],
      stream=True
  )
  for chunk in response:
      if chunk.choices[0].delta.content:
          print(chunk.choices[0].delta.content, end="", flush=True)
  ```

- ⚠️ **注意限制**：  
  - 不支持 OpenAI 的 `response_format`（JSON mode）、`logprobs`、`n > 1` 等非标准扩展字段；  
  - Application Call 的 `session_id`、`memory_id`、`rag_options` 等百炼特有能力，需通过 `extra_body` 参数透传（SDK v1.40+ 支持）；  
  - 所有 OpenAI 兼容接口**仅限华北2（北京）地域可用**；若使用 Workspace ID，请确保其归属北京地域，否则请求将失败。

## 关联主题页

- [frameworks](../api/frameworks.md)
- [application call](../api/application-call.md)
- [vector and sort](../api/vector-and-sort.md)


