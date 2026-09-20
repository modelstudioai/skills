# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至外部业务系统的开发方式。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心能力，适用于构建 AI 增强型业务系统。所有调用均需有效 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心功能**：
  - 单轮文本生成（`prompt` 输入）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件专属参数），详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 调试信息返回（启用 `debug` 字段可获取执行轨迹）。

> **注意**：文档2明确声明“百炼工作流不支持使用文生图大模型”，而文档1和文档3未提及此限制。该约束具有地域和模型类型双重限定，开发者在华北2（北京）地域调用工作流应用时须规避文生图类模型节点。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上复制的唯一标识符（非模型 ID） |
| `prompt` | string | 否（与 `messages` 互斥） | 单轮指令文本；若使用 `messages` 则不可传此字段 |
| `messages` | array | 否（与 `prompt` 互斥） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于显式管理多轮上下文 |
| `session_id` | string | 否 | 由服务端生成并返回的会话标识，用于自动加载云端历史（有效期 1 小时，最多 50 轮） |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }` |
| `parameters` | object | 否 | 应用级运行参数（如 `temperature`, `max_output_tokens`），具体字段取决于应用内配置的模型节点 |
| `debug` | object | 否 | 启用后返回详细执行日志（如 `{"enable": true}`） |

> **注意**：当请求中同时包含 `session_id` 和 `messages` 时，系统**优先使用 `messages`**（见文档2“多轮对话”章节），此行为覆盖默认会话恢复逻辑。

## 使用方式

### 1. 前置准备
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并配置，推荐[配置为环境变量 `DASHSCOPE_API_KEY`](../../raw/model-api-reference/preparations/get-api-key.md)；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用卡片上的 ID；
- （SDK 方式）安装对应语言 SDK：Python、Java、Node.js 等均需安装最新版 DashScope SDK（文档1建议 Java SDK ≥ 2.12.0；文档3建议 Python SDK ≥ 1.14.0）。

### 2. 调用示例（统一接口）
所有语言均调用同一 HTTP 端点：  
`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`

- **SDK 调用（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```

- **HTTP 调用（curl）**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {"prompt": "你是谁？"},
          "parameters": {},
          "debug": {}
        }'
  ```

- **插件参数透传（HTTP）**：
  ```json
  {
    "input": {
      "prompt": "查询寝室公约",
      "biz_params": {
        "user_defined_params": {
          "your_plugin_code": {"article_index": 2}
        }
      }
    }
  }
  ```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持 **华北2（北京）地域**（见文档2首段强调）；智能体应用无此限制，但建议确认控制台所在地域与 API Endpoint 一致。
- **会话管理**：
  - `session_id` 有效期为 1 小时，超时后需新建会话；
  - 单个 `session_id` 最多承载 50 轮对话，超出后需重置。
- **安全实践**：
  - **禁止硬编码 API Key**：所有示例均强调“不建议在生产环境中直接将 API Key 硬编码到代码中”，必须通过环境变量或密钥管理服务注入；
  - 插件鉴权：若插件开启鉴权，需在插件配置中正确设置 Header/Basic Auth 等参数（见文档3“步骤一”）。
- **错误处理**：
  - 所有调用需检查 `status_code`（HTTP）或 `response.status_code`（SDK），非 `200/OK` 时解析 `request_id` 和 `message` 进行排障；
  - 错误码参考：[错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


