# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 与 OpenAI 兼容 Responses API），覆盖单轮/多轮对话、多模态输入（文本、图像、文件）、流式响应、[长期记忆](../concepts/long-term-memory.md)、RAG 检索等关键场景，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，但不同 API 路径和参数支持存在差异。
- **多模态能力**：
  - 图像理解：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或模型入参变量设为 `imageList`（工作流）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - 文件问答：仅智能体应用支持，需配置文件处理方式为“全文引用”或“切片检索” [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **高级功能**：
  - [流式输出](../concepts/streaming-output.md)（`stream=true`）：支持增量输出（`incremental_output=true`）以优化用户体验。
  - 思考过程：通过 `enable_thinking` + `has_thoughts` 组合获取模型思考链（仅新版智能体 API 支持）[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。
  - [长期记忆](../concepts/long-term-memory.md)：通过 `memory_id` 参数启用，仅智能体应用支持 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
  - RAG 检索：通过 `rag_options` 指定知识库（`pipeline_ids`）与文档（`file_ids`）等，仅智能体应用支持 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
  > **注意**：新版智能体 API（`/api/v1/apps/{APP_ID}/completion`）不支持 `rag_options`、`memory_id` 和 `biz_params.user_defined_params`；这些功能仅在工作流与旧版智能体 API 中完整可用。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | ✅ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需填入 URL 路径。 | 全部 |
| `prompt` | string | ✅（部分） | 单轮文本输入。若使用 `messages`，则 `prompt` 不可传。 | DashScope API（新版/旧版） |
| `input` | string/array/object | ✅（部分） | OpenAI 兼容模式的核心输入：支持字符串（单轮）、消息数组（多轮/多模态）。[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 中详细定义了 `content` 的结构。 | Responses API |
| `messages` | array | ⚠️（可选） | 多轮对话上下文数组（system/user/assistant），替代 `prompt` 和 `session_id`。 | 工作流与旧版智能体 API |
| `session_id` | string | ❌ | 对话历史标识，1 小时无请求自动失效。与 `messages` 冲突时优先使用 `messages`。 | DashScope API（新版/旧版） |
| `workspace` | string | ❌ | 子业务空间 ID，仅当应用部署于子空间或特定地域（如法兰克福、北京、新加坡等）时必需。[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档说明其获取方式。 | 全部（Header 或 parameters） |
| `stream` | boolean | ❌ | 是否[流式输出](../concepts/streaming-output.md)。Responses API 中 `background=true` 时不可用。 | 全部 |
| `biz_params` | object | ❌ | 传递自定义参数、插件参数及用户鉴权信息。结构复杂，详见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。 | 工作流与旧版智能体 API |

## 使用方式

- **协议选择**：
  - **DashScope 原生 API**：路径为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，适用于需要最大灵活性和全功能支持的场景（如 RAG、[长期记忆](../concepts/long-term-memory.md)、复杂插件调用）。
  - **OpenAI 兼容 Responses API**：路径为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，适用于快速迁移现有 OpenAI 代码或简化集成。支持同步（`background=false`）与异步（`background=true`）两种模式 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **调用示例（Python）**：
  - DashScope SDK（新版智能体）：
    ```python
    from dashscope import Application
    response = Application.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id="YOUR_APP_ID",
        prompt="你是谁？"
    )
    ```
  - OpenAI SDK（Responses 同步）：
    ```python
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
    )
    response = client.responses.create(input="你是谁？")
    ```
- **调试**：所有应用均支持控制台内“应用卡片 → 发布 → API 调试”进行在线参数填写与运行验证。

## 限制和注意事项

- **地域限制**：所有文档明确指出，当前 DashScope API 与 Responses API 均**仅支持华北2（北京）地域**。调用其他地域的应用必须显式传入 `workspace` 且确保 Base URL 匹配该地域 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **凭证获取**：APP ID 和 Workspace ID **仅能通过控制台手动获取**，不支持 API 或 CLI 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如：
  - `incremental_output`：Java SDK ≥ 2.20.0；
  - `biz_params` 中的插件参数：Java SDK ≥ 2.21.13；
  - `flow_stream_mode`：Java SDK ≥ 2.22.23。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号，普通子账号仅能查看已加入的空间 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **异步限制**：`background=true` 时，`stream=true` 不生效，且无法获取中间流式结果 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)


