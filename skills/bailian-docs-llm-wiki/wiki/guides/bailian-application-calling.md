# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至外部业务系统的开发方式。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义[插件](../concepts/plugin.md)参数透传等核心能力，适用于构建 AI 增强型业务服务。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **模型能力**：底层自动路由至应用配置所绑定的大模型（如 `qwen-max`、`qwen-plus` 等），不支持在调用时显式指定模型 ID；但需注意：**工作流应用明确不支持文生图大模型**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **高级功能**：
  - 多轮对话（通过 `session_id` 或显式传递 `messages` 数组）；
  - 自定义[插件](../concepts/plugin.md)参数透传（通过 `biz_params.user_defined_params`）；
  - 调试信息返回（启用 `debug` 字段）。

> **注意**：文档 1 和文档 2 中的 Python/Java/HTTP 示例代码完全一致，但文档 2 明确声明“**仅适用于华北2（北京）地域**”，而文档 1 未限定地域。实际部署时请以 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 的地域约束为准，智能体应用调用亦建议优先部署于华北2。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用管理页获取的应用唯一标识（APP_ID） |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 当前请求的用户输入文本；若使用 `messages` 数组则无需此字段 |
| `messages` | array | 否（推荐用于多轮对话） | 按 `[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]` 格式传递完整对话历史，优先级高于 `session_id` |
| `session_id` | string | 否（用于云端维护对话状态） | 由服务端生成或客户端指定，有效期 1 小时，最多支持 50 轮；若与 `messages` 共存，系统**优先使用 `messages`** |
| `biz_params` | object | 否 | 用于传递自定义[插件](../concepts/plugin.md)参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": "<value>" } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 1. 前置准备
- 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）；
- 在百炼控制台创建对应类型应用（[智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md) 或 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)），复制其 APP_ID；
- 若使用 SDK，按语言安装对应版本（Python ≥ 1.14.0，Java ≥ 2.12.0）。

### 2. 调用示例（SDK 通用模式）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
```

### 3. HTTP 调用（curl）
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

### 4. 自定义插件调用（关键扩展）
需在 `input` 中嵌套 `biz_params`：
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
> 插件 ID（`your_plugin_code`）需从控制台插件卡片中获取，且插件须已关联至目标应用。

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用虽未明文限制，但跨地域调用可能失败，建议统一部署于华北2；
- **会话管理**：`session_id` 有效期为 1 小时，最大轮次 50；生产环境推荐自行维护 `messages` 数组以获得确定性行为；
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入；
- **插件兼容性**：自定义插件参数透传仅适用于智能体应用和工作流应用，不适用于已下线的“智能体编排应用”；
- **错误处理**：所有调用均需检查 `status_code`（HTTP）或 `response.status_code`（SDK），失败时参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
- **响应结构**：成功响应中，文本内容位于 `output.text`（SDK）或 `response.output.text`（HTTP JSON），`usage.models` 包含各模型 token 消耗详情。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


