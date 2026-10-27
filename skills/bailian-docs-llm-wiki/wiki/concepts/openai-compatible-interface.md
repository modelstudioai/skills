# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求体结构、响应格式与流式传输规范（如 SSE），使开发者能直接复用 OpenAI 官方 SDK（Python/Node.js 等 v1.x 版本）或现有 HTTP 调用逻辑，零代码改造接入百炼的 Qwen 系列及第三方直供模型能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：无需重写业务逻辑，只需将 `base_url` 替换为百炼专属兼容 endpoint，并传入对应地域的 API Key，即可调用 `chat/completions`、`embeddings`、`responses`、`conversations`、`files` 等端点。
- **统一 SDK 集成**：推荐使用 OpenAI 官方 SDK（如 `from openai import OpenAI`），通过配置 `base_url` 和 `api_key`，即可同时驱动文本生成、多模态理解、[向量嵌入](embedding.md)、智能体响应、会话管理等多类能力。
- **工具链无缝对接**：主流开发工具（Cursor、Qwen Code）、IDE 插件、低代码平台等，只要支持 OpenAI 协议，均可通过配置百炼的兼容 endpoint 直接启用 Qwen 模型，无需适配私有协议。
- **按计费方案灵活选型**：不同套餐对应不同 base_url：
  - Token Plan（个人/团队版）：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - Coding Plan：`https://coding.dashscope.aliyuncs.com/v1`
  - 按量计费（推荐）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **能力分层调用**：
  - `chat/completions`：通用对话，支持流式/非流式，但**不支持 Qwen-Audio 及音视频输入**；
  - `responses`：增强型智能体接口，内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 实现轻量上下文延续；
  - `embeddings`：调用 `text-embedding-v4` 等模型，支持 `dimensions` 参数定制向量维度；
  - `conversations`：自动维护会话状态，适用于跨设备、长周期交互场景；
  - `files`：OpenAI 兼容的文件上传/管理接口（路径 `/compatible-mode/v1/files`），替代旧版 DashScope 原生文件 API，推荐新项目使用。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | **必填**，服务入口地址，必须使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），禁用通用域名 `dashscope.aliyuncs.com` | 不同计费方案（Token Plan/Coding Plan/按量）对应不同 base_url，不可混用 |
| `api_key` | **必填**，需从对应地域控制台获取，与 base_url 所属地域强绑定（如北京 Key 不能调用弗吉尼亚 endpoint） | Token Plan 与 Coding Plan 的 Key 由独立控制台发放，不可复用 |
| `model` | **必填**，模型 ID 必须严格匹配官方名称（大小写敏感、含点号），如 `qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v4` | 第三方模型（如 `glm-5.3`、`deepseek-v4.1-flash`）仅限华北2（北京）地域可用；`Qwen-Audio` 不支持该协议 |
| `stream` | 控制是否启用流式响应，默认 `false`；流式响应格式为标准 SSE（Server-Sent Events） | `chat/completions` 与 `responses` 均支持，但 `responses` 的流式为 JSON Lines 格式 |
| `previous_response_id` | `responses` 接口专用，传入上一轮响应的顶层 `id`（UUID 字符串），用于自动继承上下文与工具执行状态 | 非 `output` 内部的 `msg_xxx` ID，不可混淆 |
| `enable_thinking` | Batch 或 Responses 场景可选，显式设为 `false` 可关闭思考模式以降低 token 消耗 | 必须作为请求体顶层字段（与 `model` 同级），不可置于 `extra_body` 中 |
| `dimensions` | `embeddings` 接口专用，仅 `text-embedding-v3/v4` 支持，指定输出向量维度（如 `1024`） | 默认值依模型而定，建议显式声明以确保一致性 |

## 面向开发者，简洁实用

- ✅ **立即上手**：复制以下 Python 示例，替换 `YOUR_WORKSPACE_ID` 和 `YOUR_API_KEY` 即可运行：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",  # 从百炼控制台获取
      base_url="https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好，请用中文简要介绍百炼平台"}]
  )
  print(response.choices[0].message.content)
  ```

- ⚠️ **避坑提醒**：
  - 永远使用**业务空间专属域名**，通用域名已弃用且不稳定；
  - `model` 名称必须一字不差（包括 `.` 和 `-`），`qwen3.8-max` ≠ `qwen38max`；
  - `Qwen-Audio`、`wan2.6-t2i`、`wan2.6-v2v` 等模型**不支持 OpenAI 兼容接口**，请改用 DashScope 原生协议；
  - 文件上传请优先使用 `/compatible-mode/v1/files`（OpenAI 兼容），而非旧版 `/api/v1/files`；
  - 流式响应需正确处理 SSE 事件（`data:` 前缀）或 JSON Lines（`responses`），不要当作普通 JSON 解析。

- 📌 **最佳实践**：
  - 生产环境务必使用按量计费 + WorkspaceId 专属域名，保障功能完整性与地域可控性；
  - 多模态调用（图像/文档）前，先通过 `file-extract` 或兼容 `files` 接口上传并获取 URL，再在 `messages` 中引用；
  - 高并发场景需合理配置 SDK 连接池（如 Python 的 `httpx.Limits`），避免触发服务端限流。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)
- [file management api](../api/file-management-api.md)


