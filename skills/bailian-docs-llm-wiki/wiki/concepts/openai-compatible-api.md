# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 API 协议层，完全遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK（Python/Node.js 等）、LangChain、LlamaIndex 等生态工具，**零代码改造**即可调用百炼托管的千问（Qwen）全系列及主流第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速模型调用**：开发者只需替换 `base_url` 和 `api_key`，即可用标准 `openai.OpenAI()` 客户端直接调用 `qwen3.8-plus`、`deepseek-v4-pro-0813` 等数十种文本、多模态、嵌入、重排序模型，无需学习新协议。
- **智能体（Agent）应用集成**：通过 `/v1/responses` 接口（OpenAI Responses 兼容），在保持 OpenAI SDK 调用习惯的同时，获得内置联网搜索、网页抓取、代码解释器等 Agent 原生能力，并支持 `previous_response_id` 实现多轮上下文管理。
- **多模态任务开发**：图像理解（`qwen-vl-plus`）、音视频分析（`qwen3.8-omni-flash`）等能力均通过 OpenAI Vision 兼容格式（`messages.content` 中含 `image_url` 或 `input_audio`）统一接入，降低跨模态开发门槛。
- **批量与[异步处理](asynchronous-processing.md)**：`/v1/batch` 接口支持 JSONL 文件异步批量推理，成本为实时调用的 50%；`/v1/files` 接口支持上传 PDF/DOCX 等文档供 Qwen-Doc-Turbo 进行问答，全部遵循 OpenAI 批量 API 规范。
- **低代码/客户端集成**：Chatbox、Cursor、Dify、OpenClaw 等主流工具仅需配置百炼的 OpenAI 兼容 Base URL 和对应计费方案的 API Key，即可开箱即用——Dify 等平台甚至自动识别 `qwen3.8-max` 等模型名并启用思考模式。

> ⚠️ 注意：并非所有百炼能力都开放于 OpenAI 兼容层。例如 `qwen-audio`（语音理解）、`qwen3.8-audio`（音频生成）、`max_frames`（视频帧控制）等深度能力**仅支持 DashScope 原生协议**；`completions`（代码补全）接口目前也仅限华北2（北京）地域且仅支持 `qwen-coder-turbo`。

## 关键参数和配置

| 参数 | 必选 | 说明 | 百炼特有约束 |
|------|------|------|--------------|
| `base_url` | ✅ | 接口根地址，**必须使用业务空间专属域名** | 格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；旧域名 `dashscope.aliyuncs.com` 已不推荐，将于 2026 年 9 月 30 日起停用新特性支持 |
| `api_key` | ✅ | 认证凭证 | **严格按地域与计费方案绑定**：[Token](token.md) Plan 个人版 Key 只能配 [Token](token.md) Plan Base URL；按量付费 Key 必须与 `WorkspaceId` 所属地域一致（如北京 Key 不能调用弗吉尼亚 endpoint） |
| `model` | ✅ | 模型标识符 | 必须使用[官方文档明确列出的模型名](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope)，如 `"qwen3.8-plus"`；非列表模型可能缺失功能或返回 404 |
| `messages` | ✅（chat/completions） | 对话消息数组，格式 `[{ "role": "user", "content": "..." }]` | 支持多模态内容：`content` 可为字符串，也可为对象数组（含 `text`、`image_url`、`video_url`、`input_audio` 等类型） |
| `stream` | ❌（默认 `false`） | 启用流式响应 | 推荐设为 `true` 以降低超时风险；流式末尾 chunk 可通过 `stream_options={"include_usage": true}` 返回 token 统计 |
| `temperature` | ❌（默认 `0.8`） | 采样温度 | 取值范围 `[0, 2)`，注意与 Anthropic 官方 `[0, 1]` 不同，迁移时需校准 |
| `tools` | ❌ | 工具定义数组 | 仅 `responses` 接口支持内置工具（`web_search`, `code_interpreter`）；`chat/completions` 中部分模型支持自定义 Function Calling |

> 🔑 提示：`WorkspaceId` 是业务空间 ID，可在控制台「业务空间管理」页面查看；不同地域（北京、新加坡、东京、法兰克福等）的 `WorkspaceId`、Base URL、API Key **完全隔离，严禁混用**。

## 面向开发者，简洁实用

- ✅ **立即上手**：复制以下代码，填入你的 `WorkspaceId` 和 `DASHSCOPE_API_KEY` 环境变量，5 秒发起首次调用：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  resp = client.chat.completions.create(model="qwen3.8-plus", messages=[{"role":"user","content":"你好"}])
  print(resp.choices[0].message.content)
  ```

- ✅ **调试技巧**：  
  - 遇到 `401 invalid_api_key`？检查 API Key 是否与 Base URL 所属地域/计费方案匹配；  
  - 遇到 `404 Not Found`？确认 `model` 名拼写正确，且该模型在当前地域可用（如 `deepseek-v4-pro-0813` 仅支持北京）；  
  - 遇到 `413 Payload Too Large`？含 Base64 的请求整体 ≤64 MiB，且解码后文本+二进制内容 ≤16 MiB。

- ✅ **生产建议**：  
  - 始终使用业务空间专属域名（而非 `dashscope.aliyuncs.com`），获得更高吞吐、更低延迟与流量隔离；  
  - 对需要长期对话状态的场景，优先选用 `/v1/responses` + `previous_response_id`，而非自行维护 `messages` 数组；  
  - 多模态输入优先用 `image_url`（公网可访问 URL），避免 Base64 编码增加请求体积。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


