# preparations

在调用百炼模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、功能可用性及稳定性，是所有模型调用的前提。本文汇总关键操作路径、参数约束与常见陷阱，帮助开发者快速建立可运行的调用环境。

## 支持的模型/功能

百炼支持文本生成、多模态对话、图像/视频生成、语音识别与合成、向量嵌入、重排序、智能体应用等多种模型类型。具体可用模型取决于所选业务空间的授权范围和地域可用性，**同一业务空间内的 API Key 权限一致**，无需为不同模型创建多个 Key [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- 文本生成类（如 `qwen-plus`、`qwen3.7-plus`）支持流式/非[流式输出](../concepts/streaming-output.md)、思考模式（`enable_thinking`）、结构化输出（`response_format={"type": "json_object"}`），但部分能力存在互斥约束（例如思考模式下不支持结构化输出）。  
- 多模态模型（如 `qwen3-vl-plus`）要求 `messages.content` 为包含 `image` 和 `text` 的数组，且仅支持[流式输出](../concepts/streaming-output.md)。  
- 音频类模型（ASR/TTS）强制要求 `stream=True`，否则报错 `audio output only support with stream=true` [错误码](../../raw/model-api-reference/preparations/error-code.md)。  
- Embedding 和 Rerank 模型有明确的批次大小（batch size）上限，超限将触发 `InvalidParameter` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 5 中列出的 DashScope SDK 1.x 接口（如 `Generation.call`、`MultiModalConversation.call`）已冻结维护，**新项目必须使用 SDK 2.0**（`client.chat.completions.create` 等），且 Assistants / Threads / Runs 系列 API 已下线，服务端不再支持 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。

## 关键参数

调用时需关注以下核心参数及其取值约束：

| 参数 | 约束条件 | 说明 |
|------|----------|------|
| `model` | 必填；大小写敏感；须与[模型列表](raw/model-user-guide/get-started-with-models/models.md)中 ID 完全一致（如 `qwen3.7-plus`，非 `Qwen/Qwen3.7-Plus`） | 模型不存在将返回 `ModelNotFound` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `temperature` | `[0.0, 2.0)` | 超出范围报 `Temperature should be in [0.0, 2.0)` |
| `top_p` | `(0.0, 1.0]` | 超出范围报 `Range of top_p should be (0.0, 1.0]` |
| `max_tokens` | `[1, 模型最大输出 Token 数]` | 上限见各模型文档，超限报 `Range of max_tokens should be [1, xxx]` |
| `stream` | `true`/`false` | 部分模型（如 `qwen-image-3.0-pro`）**仅支持流式**，非流式调用报 `This model only support stream mode` [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `enable_thinking` | 与 `stream`、`incremental_output` 强耦合：开启时必须 `stream=true` 且 `incremental_output=true`，且禁用 `response_format=json_object` | 违反任一约束均触发对应 `InvalidParameter` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md) |

## 使用方式

1. **获取并配置 API Key**：在控制台按地域创建 Key，**Key 与地域、Base URL 必须严格匹配**，跨地域混用导致 `401 InvalidApiKey` [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。推荐配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码。  
2. **选择 Base URL**：生产环境优先使用**业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），其提供流量隔离与更高性能；临时测试可用试用域名；中心化 `dashscope.aliyuncs.com` 域名仍兼容但建议迁移 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)。  
3. **安装 SDK**：  
   - Python：`pip install -U "dashscope>=2.0.1"`（官方 SDK）或 `pip install -U openai`（OpenAI 兼容 SDK） [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。  
   - Java/Node.js/Go：参见对应语言的依赖配置 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。  
4. **调用示例（Python + DashScope SDK 2.0）**：  
   ```python
   import os
   from dashscope import Client
   client = Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
   response = client.chat.completions.create(
       model="qwen-plus",
       messages=[{"role": "user", "content": "你好"}],
       stream=True  # 流式必需
   )
   for chunk in response:
       if chunk.choices and chunk.choices[0].delta.content:
           print(chunk.choices[0].delta.content, end="", flush=True)
   ```

## 限制和注意事项

- **API Key 限制**：单账号+单地域最多 50 个 Key；自定义权限下可选模型数上限 30 个；IP 白名单最多 20 个地址 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **时效性**：API Key 无自动过期时间，但可通过控制台主动删除；如需短期凭证，应使用[临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（最长 1800 秒） [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **安全警告**：**切勿在客户端（浏览器、移动 App）或不可信环境中暴露长期 API Key**；应使用临时 Key 或后端代理。环境变量未生效的常见原因包括：未重启 IDE/终端、`sudo` 未传递环境变量、服务管理器（如 systemd）未加载环境文件 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **错误处理**：`401` 错误优先检查 Key/地域/Base URL 匹配性；`429` 错误需降低并发或申请配额；`400` 错误需校验参数格式（如 JSON 合法性、`messages` 非空、`content` 字段存在） [错误码](../../raw/model-api-reference/preparations/error-code.md)。  
- **SDK Expert 工具**：DashScope Python SDK ≥1.27.3 内置 CLI 工具，支持自然语言生成代码、诊断报错、解释逻辑，但需联网且消耗 token，**不修改源码前会生成 diff 并征求确认** [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)


