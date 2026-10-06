# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至外部业务系统的开发方式。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心能力，适用于构建 AI 增强型业务服务。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **模型能力**：底层自动路由至应用配置所绑定的大模型（如 `qwen-max`、`qwen-plus` 等），不支持在调用时显式指定模型 ID；**工作流应用明确不支持文生图类大模型**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **扩展能力**：
  - 多轮对话：支持 `session_id`（云端维护，有效期 1 小时，最多 50 轮）或手动传递 `messages` 数组（推荐，更可控）；
  - 自定义插件参数透传：通过 `biz_params.user_defined_params` 向关联的插件节点传递业务参数，适用于智能体应用和工作流应用中的插件节点，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：文档 1 和文档 2 的代码示例完全一致，但文档 2 明确声明“**仅适用于华北2（北京）地域**”，而文档 1 未提及地域限制。实际部署时请以文档 2 的地域约束为准，避免跨地域调用失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用管理页获取的应用唯一标识符（APP_ID） |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 当前请求的用户输入文本；若使用 `messages` 数组则无需此字段 |
| `messages` | array | 否（若提供则替代 `prompt`） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于实现精确上下文控制的多轮对话 |
| `session_id` | string | 否 | 用于启用云端会话历史加载；若同时传 `messages`，系统优先使用 `messages` |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": "<value>" } } }` |

## 使用方式

### 前提条件
1. 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）：参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
2. 创建对应类型的应用（智能体或工作流），并在控制台复制其 `app_id`；
3. 若使用 SDK，按语言安装对应版本的 DashScope SDK（Python ≥ 1.14.0，Java ≥ 2.12.0）。

### 调用方式（三选一）
- **DashScope SDK（推荐）**：封装了认证、序列化与错误处理，各语言调用接口统一。例如 Python：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```
- **HTTP API（通用）**：直接调用 RESTful 接口，适用于所有语言及无 SDK 环境：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"input": {"prompt": "你是谁？"}}'
  ```
- **Responses API（OpenAI 兼容）**：需额外开通，详见 [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)。

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用虽未明示，但建议统一部署在北京地域以确保兼容性（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **安全实践**：严禁在代码中硬编码 `api_key`；必须通过环境变量（如 `DASHSCOPE_API_KEY`）或密钥管理服务注入。
- **插件参数格式**：`biz_params.user_defined_params` 中的 `<plugin_code>` 必须与百炼控制台插件卡片上显示的插件 ID 完全一致，且插件需已发布并正确关联至目标应用。
- **调试与排错**：
  - 所有响应均含 `request_id`，用于服务端日志追踪；
  - 错误码含义请查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
  - HTTP 调用需严格校验 `Content-Type: application/json` 及 `Authorization` 请求头格式。

> **注意**：文档 3 中 Java 示例使用 `JsonUtils.parse(bizParams)` 解析字符串形式的 `biz_params`，而文档 1 和 2 的 Java 示例未涉及该参数。开发者若需透传插件参数，应参考文档 3 的完整实现，而非直接复用文档 1/2 的基础调用代码。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


