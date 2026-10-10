# bailian [application call](../api/application-call.md)ing

阿里云百炼平台支持通过统一 API（DashScope SDK 或 HTTP 接口）调用两类核心应用：智能体应用（Agent 1.0）和工作流应用。调用过程抽象为标准的 `app_id` + `prompt` 请求模型，底层自动路由至对应应用执行逻辑，并返回结构化响应。所有调用均需有效 API Key 和已发布的应用 ID，推荐通过环境变量安全注入密钥。

## 支持的模型/功能

- **智能体应用**：基于 Agent 1.0 架构构建，支持插件调用、工具使用及简单编排逻辑；适用于需轻量级决策与外部系统交互的场景。详情见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
- **工作流应用**：基于可视化节点编排（含大模型节点、条件分支、插件节点等），支持复杂多步骤任务；明确限定仅在华北2（北京）地域可用，且**不支持文生图类大模型**。详情见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **自定义参数传递**：两类应用均支持通过 `biz_params.user_defined_params` 向关联的自定义插件透传业务参数（如 `article_index: 2`），该能力依赖插件配置中“传参方式”设为**业务透传**。详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：文档3明确声明“百炼工作流不支持使用文生图大模型”，而文档1和文档3均未提及此限制对智能体应用是否适用；实际开发中应避免在智能体应用中配置文生图模型节点，以确保兼容性。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取。智能体应用与工作流应用共用同一 ID 命名空间。 |
| `prompt` | string | 是（除非使用 `messages`） | 用户输入的自然语言指令，作为应用执行的初始上下文。 |
| `biz_params` | object | 否 | 用于传递插件参数等扩展信息。必须包含 `user_defined_params` 字段，其值为 `{plugin_code: {param_key: param_value}}` 结构。 |
| `session_id` | string | 否 | 用于启用云端对话历史（有效期 1 小时，最多 50 轮）。若同时传 `messages`，则 `messages` 优先。 |
| `messages` | array | 否（替代 `prompt`） | 自行维护的对话历史数组，格式同 OpenAI `messages`，推荐用于精确控制上下文。 |

## 使用方式

### 1. 前置准备
- 获取 API Key：前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建并配置，建议[配置到环境变量 `DASHSCOPE_API_KEY`](../../raw/model-api-reference/preparations/get-api-key.md)。
- 获取 `app_id`：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中复制已发布应用的 ID。
- （可选）安装 SDK：Python、Java、Node.js 等语言需安装对应 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)，HTTP 方式无需安装。

### 2. 发起调用
- **SDK 调用（Python 示例）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？",
      biz_params={"user_defined_params": {"your_plugin_code": {"article_index": 2}}}
  )
  ```
- **HTTP 调用（curl 示例）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "input": {
            "prompt": "你是谁？",
            "biz_params": {
                "user_defined_params": {
                    "your_plugin_code": {"article_index": 2}
                }
            }
        }
    }'
  ```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域；智能体应用无显式地域限制，但建议与应用部署地域一致以降低延迟。
- **SDK 版本要求**：Java SDK 需 ≥ 2.12.0（见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 和 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)），Python SDK 未明确最低版本，但插件参数功能需 ≥ 1.14.0（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。
- **多轮对话**：`session_id` 由服务端生成并返回（响应中 `output.session_id`），客户端需自行保存并在后续请求中复用；若使用 `messages`，则完全由客户端维护，无需依赖服务端状态。
- **错误处理**：所有调用均返回标准 HTTP 状态码及 `request_id`，失败时务必记录 `request_id` 并参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 定位问题。
- **安全实践**：严禁在代码中硬编码 `DASHSCOPE_API_KEY`；生产环境必须通过环境变量或密钥管理服务注入。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


