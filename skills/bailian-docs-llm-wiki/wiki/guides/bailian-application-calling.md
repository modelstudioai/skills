# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至业务系统的过程。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传及调试能力。所有调用均需有效 API Key 和已发布的 APP_ID。

## 支持的模型/功能

- **应用类型**：支持智能体应用（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）和工作流应用（[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)），不支持文生图类大模型。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件专属参数）
  - 调试信息返回（启用 `debug` 字段可获取执行轨迹）
- **模型绑定**：底层调用的模型由应用发布时配置决定，API 调用方无需指定模型 ID；响应中 `usage.models[].model_id` 可查实际使用的模型（如 `qwen-plus`、`qwen-max`）。

> **注意**：文档 1 明确声明“百炼工作流不支持使用文生图大模型”，而文档 2 未提及此限制。以文档 1 为准，工作流应用存在明确的模型类型限制。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用管理页面获取的唯一标识符，区分大小写 |
| `prompt` | string | 否（若提供 `messages` 则不可用） | 单轮指令文本；与 `messages` 互斥 |
| `messages` | array | 否（若提供则替代 `prompt`） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于精确控制多轮上下文 |
| `session_id` | string | 否 | 由服务端生成或客户端指定，用于加载云端存储的对话历史（有效期 1 小时，最多 50 轮） |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "{plugin_code}": { ... } } }`（详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)） |
| `parameters` | object | 否 | 预留扩展字段，当前暂无通用语义 |
| `debug` | object | 否 | 空对象 `{}` 即可启用调试模式，返回详细执行节点日志 |

## 使用方式

### 认证与初始化
- 所有调用必须携带 `Authorization: Bearer <DASHSCOPE_API_KEY>` 请求头。
- 推荐将 API Key 配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。

### SDK 调用（Python 示例）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
if response.status_code == 200:
    print(response.output.text)
```

### HTTP 调用（curl 示例）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": { "prompt": "你是谁？" },
    "parameters": {},
    "debug": {}
  }'
```

### 多轮对话推荐方案
- **显式 `messages`（推荐）**：客户端自行维护完整对话数组并每次全量提交，控制力强、无状态依赖。
- **`session_id`（便捷）**：仅传 `session_id`，服务端自动加载历史；但受 1 小时/50 轮限制，且与 `messages` 共存时后者优先。

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）；智能体应用未明确限制，建议优先使用北京地域。
- **安全要求**：生产环境严禁硬编码 API Key，必须通过环境变量或密钥管理服务注入。
- **插件参数约束**：
  - `biz_params.user_defined_params` 中的 `{plugin_code}` 必须与百炼控制台中插件卡片显示的 ID 完全一致。
  - 插件输入参数的传参方式必须配置为“业务透传”（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。
- **SDK 版本**：Java SDK 建议 ≥ 2.12.0（文档 1 & 2），Python SDK 建议 ≥ 1.14.0（文档 3），低版本可能缺失 `biz_params` 支持。
- **错误处理**：务必检查 `response.status_code` 和 `response.message`，并参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 进行诊断。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


