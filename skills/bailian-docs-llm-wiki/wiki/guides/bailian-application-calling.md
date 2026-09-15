# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将已发布的百炼工作流应用或智能体应用集成至业务系统的过程。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传及调试能力，适用于华北2（北京）地域。所有调用均需有效 API Key 和已发布的 APP_ID。

## 支持的模型/功能

- **应用类型**：支持[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)和[智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md)，不支持文生图类大模型（如万相）。
- **核心能力**：
  - 单轮文本生成（基于 `prompt`）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件专属参数）
- **模型绑定**：底层调用的模型由应用发布时配置决定（如 `qwen-max`、`qwen-plus`），调用方无需指定模型 ID；响应中 `usage.models[].model_id` 可用于追溯实际执行模型。

> **注意**：文档 1 明确声明“百炼工作流不支持使用文生图大模型”，而文档 2 未提及此限制。以文档 1 为准，该限制具有强制性，见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用在控制台「应用管理」页面获取的唯一 ID，见 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) |
| `prompt` | string | 否（若提供 `messages` 则不可用） | 单轮指令文本；与 `messages` 互斥 |
| `messages` | array | 否（若提供则替代 `prompt`） | 格式为 `[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]`，推荐用于精确控制多轮上下文 |
| `session_id` | string | 否 | 由服务端维护的会话 ID，有效期 1 小时，最多支持 50 轮；若同时传 `messages`，则优先使用 `messages`（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)） |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{"user_defined_params": {"{plugin_code}": {"param_key": "value"}}}`；详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 1. 前置准备
- 获取并配置 API Key：[获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 并设为环境变量 `DASHSCOPE_API_KEY`
- 确保应用已发布，且位于华北2（北京）地域
- SDK 用户需安装对应版本：Python（`dashscope>=1.14.0`）、Java（`dashscope-sdk-java>=2.12.0`）

### 2. 调用示例（HTTP）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
      "prompt": "你是谁？",
      "biz_params": {
        "user_defined_params": {
          "plugin_abc123": {"query_id": 42}
        }
      }
    },
    "parameters": {},
    "debug": {}
  }'
```

### 3. 多轮对话推荐实践
- **自行管理 `messages`（推荐）**：客户端完整维护对话历史数组，每次请求携带全部 `messages`，避免服务端状态依赖。
- **云端 `session_id`（简化场景）**：首次调用不传 `session_id`，服务端返回 `response.output.session_id`；后续请求复用该 ID 即可加载历史。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，其他地域调用将失败（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **安全要求**：API Key **严禁硬编码**，必须通过环境变量或密钥管理服务注入；SDK 默认从 `DASHSCOPE_API_KEY` 读取。
- **插件参数约束**：
  - `biz_params.user_defined_params` 中的 `{plugin_code}` 必须与控制台插件卡片上显示的 ID 完全一致；
  - 插件输入参数的 `传参方式` 必须配置为 **业务透传**（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。
- **错误处理**：所有语言 SDK 示例均包含 `request_id` 输出，用于排查问题；错误码参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


