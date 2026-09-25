# bailian [application call](../api/application-call.md)ing

阿里云百炼平台支持通过统一的 Application API 调用智能体应用（Agent 1.0）和工作流应用（Workflow Application），开发者可使用 DashScope SDK 或标准 HTTP 接口快速集成。该能力基于 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion` 统一端点，兼容多种编程语言，适用于单轮问答、多轮对话及带插件参数透传的复杂业务场景。所有调用均需有效 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：支持两类核心应用：
  - 智能体应用（Agent 1.0）：面向轻量级任务编排，适用于简单工具调用与角色扮演类场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application）：面向复杂逻辑编排，支持多节点（大模型、条件分支、自定义插件等）协同执行 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **模型能力**：底层自动路由至应用配置的模型（如 `qwen-max`、`qwen-plus` 等），不支持在调用时显式指定模型 ID；**工作流应用明确不支持文生图类大模型** [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **扩展能力**：支持通过 `biz_params.user_defined_params` 向关联的自定义插件透传业务参数（如 `article_index: 2`），实现插件输入动态注入 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：文档 1 和文档 3 均称“智能体应用”为 Agent 1.0，但文档 2 中提及“智能体编排应用已被工作流应用替代”，存在术语混淆。实际当前控制台仅提供“智能体应用（Agent 1.0）”和“工作流应用”两类，**不存在独立的“智能体编排应用”类型**，该表述已过时，应以控制台实际应用类型为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台中创建的应用唯一 ID，位于[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面卡片上。 |
| `prompt` | string | 是（单轮）/ 否（多轮） | 用户输入的自然语言指令；若启用 `messages` 多轮模式，则此项忽略。 |
| `input.prompt` | string | 同上 | HTTP 请求体中 `input` 对象下的 [prompt](prompt.md) 字段，语义同 SDK 的 `prompt` 参数。 |
| `biz_params` | object | 否 | 用于传递自定义插件参数。结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": "<param_value>" } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。 |
| `session_id` | string | 否 | 启用云端会话管理时传入，有效期 1 小时，最多 50 轮。若同时传 `session_id` 和 `messages`，系统优先使用 `messages`。 |
| `messages` | array | 否（推荐用于多轮） | 完整对话历史数组，格式同 OpenAI `messages`（含 `role` 和 `content`），需在应用内配置 `historyList` 变量并发布后生效。 |

## 使用方式

### 前置准备
1. **获取凭证**：在[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 API Key，并[配置为环境变量 `DASHSCOPE_API_KEY`](../../raw/model-api-reference/preparations/get-api-key.md)（强烈推荐，避免硬编码）；
2. **获取 APP_ID**：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)复制目标智能体或工作流应用的 ID；
3. **安装 SDK（可选）**：如使用 SDK，按语言安装对应版本（Python ≥1.14.0，Java ≥2.12.0）[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。

### 调用示例（统一接口）
- **SDK（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？",
      # biz_params={"user_defined_params": {"plugin_abc": {"query": "北京天气"}}}  # 插件参数可选
  )
  print(response.output.text)
  ```

- **HTTP（curl）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {
            "prompt": "你是谁？"
          }
        }'
  ```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **安全实践**：API Key **严禁硬编码**于源码中；必须通过环境变量（如 `DASHSCOPE_API_KEY`）或密钥管理服务注入。
- **多轮对话**：
  - `session_id` 方式依赖百炼云端存储，适合简单会话，但存在 1 小时过期与 50 轮上限；
  - `messages` 方式由客户端完全掌控上下文，更灵活可靠，**推荐生产环境使用**。
- **插件参数**：`biz_params.user_defined_params` 中的插件 ID（`<plugin_code>`）必须与应用内已关联的插件一致，且插件输入参数需配置为“业务透传”方式 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
- **错误处理**：所有请求均返回标准 HTTP 状态码与 `request_id`，错误详情请查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


