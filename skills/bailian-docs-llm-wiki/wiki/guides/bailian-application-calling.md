# bailian [application call](../api/application-call.md)ing

阿里云百炼平台支持通过统一 API（DashScope SDK 或 HTTP 接口）调用两类核心应用：智能体应用（Agent 1.0）和工作流应用。调用方式一致，但功能边界、参数支持与地域限制存在差异，开发者需根据业务场景选择合适类型。所有调用均基于 `POST /api/v1/apps/{app_id}/completion` 端点，依赖有效的 API Key 和应用 ID。

## 支持的模型/功能

- **智能体应用**：支持单轮/多轮对话、插件调用（含自定义插件参数透传）、工具编排等完整 Agent 能力。详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
- **工作流应用**：支持节点化编排（大模型节点、条件分支、变量赋值等），适用于复杂逻辑流程；**不支持文生图类大模型**，且**仅限华北2（北京）地域可用** [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **共性能力**：两者均支持基础文本生成、`session_id` 多轮会话管理、`debug` 字段调试输出及标准用量统计（`usage.models` 中返回实际调用的模型 ID，如 `qwen-max`、`qwen-plus`）。

> **注意**：文档 2 中提及“智能体编排应用已被工作流应用替代”，但文档 1 和文档 3 均未使用该术语，且当前控制台仅提供“智能体应用”与“工作流应用”两类入口。此处以控制台实际命名为准，避免使用已废弃的“智能体编排应用”表述。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取。 |
| `prompt` | string | 是（除非使用 `messages`） | 用户输入的自然语言指令，作为本轮对话主输入。 |
| `input.prompt` | string | 同上 | HTTP 请求中 `input` 对象下的 [prompt](prompt.md) 字段。 |
| `biz_params` | object | 否 | 用于传递自定义插件参数。结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": "<value>" } } }`，仅对关联了自定义插件的智能体应用生效 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。 |
| `session_id` | string | 否 | 启用云端多轮会话（有效期 1 小时，最多 50 轮）。若同时传 `messages`，则 `messages` 优先。 |
| `messages` | array | 否（替代 `prompt`） | 自行维护的对话历史数组，格式同 OpenAI `messages`（`role`/`content`），推荐用于精确上下文控制。 |
| `parameters` | object | 否 | 预留扩展字段，当前无通用语义，部分节点可能支持特定参数（如温度、最大 token 数），需参考具体应用配置。 |

## 使用方式

### 前提条件
1. 获取并配置 API Key：通过[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，**强烈建议配置为环境变量 `DASHSCOPE_API_KEY`**，避免硬编码 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
2. 获取应用 ID：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面复制对应智能体或工作流应用的 APP_ID。
3. （可选）安装 SDK：Python、Java、Node.js 等语言需安装对应 DashScope SDK；HTTP 调用无需安装。

### 调用示例（核心逻辑）
- **SDK（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
      # biz_params={...}  # 如需透传插件参数
      # session_id="xxx"   # 如需多轮会话
  )
  ```

- **HTTP（curl）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {"prompt": "你是谁？"},
          "parameters": {},
          "debug": {}
        }'
  ```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **插件参数适用范围**：`biz_params.user_defined_params` 仅对**已关联自定义插件的智能体应用**有效；工作流应用中插件节点的参数传递机制不同，本文档不覆盖。
- **SDK 版本要求**：Java SDK 建议 ≥ 2.12.0（文档 1 & 3），Python SDK 建议 ≥ 1.14.0（文档 2 中插件调用示例明确要求）。低版本可能缺少 `biz_params` 支持。
- **安全实践**：API Key **严禁硬编码**于源码或前端代码中；必须通过环境变量或安全凭证服务注入。
- **错误处理**：所有调用均需检查 `status_code`（SDK）或 HTTP 状态码（HTTP），失败时解析 `request_id` 和 `message` 并参考[错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


