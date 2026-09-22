# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将已发布的百炼工作流应用或智能体应用集成至业务系统的过程。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心能力，适用于华北2（北京）地域。所有调用均需有效 API Key 和已发布的 APP_ID。

## 支持的模型/功能

- **支持的应用类型**：工作流应用（Workflow Application）和智能体应用（Agent 1.0），[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 和 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 文档均明确说明此覆盖范围。
- **不支持的模型**：工作流应用明确不支持文生图类大模型（如 wanx 系列），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心功能**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件专属参数）
  - 调试信息返回（`debug` 字段）

> **注意**：文档2（调用智能体应用）未声明地域限制，而文档1（调用工作流应用）明确要求“仅适用于华北2（北京）地域”。鉴于当前生产环境统一部署于北京，**所有应用调用均应限定在华北2（北京）地域**，否则可能返回 404 或 403 错误。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片获取 |
| `prompt` | string | 否（若提供 `messages` 则非必填） | 单轮指令文本；若使用 `messages` 模式则不应传入 |
| `messages` | array | 否（若提供则替代 `prompt`） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于完全控制上下文 |
| `session_id` | string | 否 | 由服务端维护的会话 ID，有效期 1 小时，最多 50 轮；与 `messages` 同时存在时，**优先使用 `messages`** |
| `biz_params` | object | 否 | 用于插件参数透传，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `parameters` | object | 否 | 通用模型参数（如 `temperature`, `top_p`），按工作流/智能体中配置的节点生效 |
| `debug` | object | 否 | 开启调试模式（如 `{"enable": true}`），返回中间执行日志 |

## 使用方式

### 1. 前置准备
- 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）：参见 [获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- 创建并发布应用（工作流或智能体），在控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面获取 `APP_ID`
- （SDK 方式）安装对应语言 SDK：Python（`pip install -U dashscope`）、Java（≥2.12.0）、Node.js（`axios`）等

### 2. 调用示例（统一接口）
所有语言均调用同一 HTTP 端点：  
`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`

- **SDK 调用（Python）**
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.output.text)
  ```

- **HTTP 调用（curl）**
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "input": {"prompt": "你是谁？"},
        "parameters": {},
        "debug": {}
    }'
  ```

- **插件参数透传（关键场景）**  
  在 `input.biz_params.user_defined_params` 中嵌套插件 ID 及其参数：
  ```json
  {
    "input": {
      "prompt": "查询寝室公约",
      "biz_params": {
        "user_defined_params": {
          "plugin_abc123": {"article_index": 2}
        }
      }
    }
  }
  ```
  此能力在 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中有完整说明。

## 限制和注意事项

- **地域限制**：必须使用华北2（北京）地域的 endpoint（`dashscope.aliyuncs.com`），其他地域 endpoint 不可用。
- **会话管理**：
  - `session_id` 有效期为 1 小时，最多承载 50 轮对话；
  - 若同时传入 `session_id` 和 `messages`，系统**强制优先使用 `messages`**，忽略云端历史；
  - 推荐自行管理 `messages`，以获得确定性上下文控制。
- **安全实践**：
  - **禁止硬编码 API Key**：所有示例均强调“不建议在生产环境中直接将 API Key 写入代码”，必须通过环境变量或密钥管理服务注入。
- **错误处理**：
  - 非 200 响应需检查 `response.request_id`、`response.status_code` 和 `response.message`；
  - 错误码参考：[开发者错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)
- **插件调用前提**：
  - 插件必须与应用处于同一业务空间；
  - 插件工具的输入参数“传参方式”必须设为 **业务透传**；
  - 插件 ID 需从控制台插件卡片准确复制，不可手写猜测。

> **注意**：文档1和文档2的代码示例完全一致（包括注释、错误处理逻辑、响应解析），表明工作流与智能体应用的调用协议已完全统一；但文档3中 Java 示例使用了 `JsonUtils.parse()` 解析 `biz_params`，而文档1/2未涉及该字段——这印证了 `biz_params` 是可选扩展能力，不影响基础调用流程。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


