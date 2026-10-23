# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将已发布的智能体应用或工作流应用集成至外部业务系统的过程。该机制支持单轮/多轮对话、自定义插件参数透传、会话状态管理等核心能力，适用于构建 AI 原生应用和服务编排场景。所有调用均需有效 API Key 和应用 ID，并遵循统一的 `/api/v1/apps/{app_id}/completion` 接口路径。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Agent 1.0）**：基于 LLM 的单智能体任务处理，适用于问答、摘要、推理等轻量级场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用（Workflow Application）**：支持节点编排（如大模型节点、条件分支、插件节点等），可构建复杂业务逻辑；注意其**仅限华北2（北京）地域使用**，且**不支持文生图大模型** [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心功能**：
  - 单轮与多轮对话（支持 `session_id` 自动管理或显式 `messages` 数组传递）；
  - 自定义插件参数透传（仅限关联了插件的智能体/工作流应用），通过 `biz_params.user_defined_params` 结构注入；
  - 调试信息输出（启用 `debug` 字段）；
  - 统一响应结构（含 `output.text`、`usage`、`request_id` 等字段）。

> **注意**：文档 3 明确声明“百炼工作流不支持使用文生图大模型”，而文档 1 和 2 均未提及此限制；该约束为工作流应用特有，智能体应用无此限制，开发者需按应用类型区分使用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，从百炼控制台「应用管理」页面获取 |
| `prompt` | string | ✓（若未提供 `messages`） | 当前轮次用户输入文本；若使用 `messages` 模式则**不可填写** |
| `messages` | array | ✗（推荐用于多轮） | 替代 `prompt` 的结构化消息数组，格式同 OpenAI：`[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]` |
| `session_id` | string | ✗（可选） | 启用云端会话历史自动加载；有效期 1 小时，最多 50 轮；若同时传 `messages`，则**优先使用 `messages`** |
| `biz_params` | object | ✗ | 扩展业务参数对象，**自定义插件参数必须置于 `biz_params.user_defined_params` 下**，结构为 `{ "plugin_code": { "param_key": value } }` [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `parameters` | object | ✗ | 模型级超参（如 `temperature`、`top_p`），当前多数应用默认忽略，建议留空 `{}` |
| `debug` | object | ✗ | 启用调试模式（如 `{"enable": true}`），返回中间执行日志 |

## 使用方式

### 1. 前置准备
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 安装对应语言 SDK（Python/Java/Node.js 等），版本要求见各文档（如 Java SDK ≥ 2.12.0）；
- 确保应用已发布，且调用方与应用处于同一业务空间（插件关联场景下必需）。

### 2. SDK 调用（推荐）
使用 `Application.call()` 方法，传入 `app_id`、`prompt`（或 `messages`）及可选参数：

```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    biz_params={"user_defined_params": {"plugin_abc123": {"article_index": 2}}}
)
```

### 3. HTTP 直接调用
向 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion` 发送 POST 请求，`Content-Type: application/json`，Body 示例：
```json
{
  "input": {
    "prompt": "你是谁？",
    "biz_params": {
      "user_defined_params": {
        "plugin_abc123": {"article_index": 2}
      }
    }
  },
  "parameters": {},
  "debug": {}
}
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，跨地域请求将失败；智能体应用无此限制。
- **插件参数透传**：必须满足三项前提——插件已发布、已关联至目标应用、插件工具的输入参数“传参方式”必须设为 **业务透传**（非“模型理解”或“固定值”）。
- **SDK 版本兼容性**：
  - 文档 1 要求 Python SDK ≥ 1.14.0，而文档 2/3 要求 Java SDK ≥ 2.12.0 —— 两者无冲突，但需按语言分别满足；
  - 若混用旧版 SDK（如 Java < 2.12.0），可能因参数解析差异导致 `biz_params` 无法正确传递。
- **安全实践**：**严禁在代码中硬编码 `DASHSCOPE_API_KEY`**；务必通过环境变量或密钥管理服务注入。
- **错误处理**：所有调用均应检查 `response.status_code`（HTTP）或 `response.code`（SDK），并结合 `request_id` 追踪问题，参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


