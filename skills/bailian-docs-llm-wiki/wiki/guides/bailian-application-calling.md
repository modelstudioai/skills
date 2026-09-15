# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）和工作流应用集成至业务系统的过程。所有调用均统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持多语言 SDK 封装与原生 HTTP 请求，适用于生产环境快速接入。该机制不依赖模型直连，而是以应用为单位封装逻辑、插件与编排能力。

## 支持的模型/功能

- **支持的应用类型**：智能体应用（Agent 1.0）和工作流应用（Workflow Application），[智能体编排应用已被工作流应用替代](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
- **不支持的模型类型**：工作流应用明确不支持文生图大模型（如 wanx 系列），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮/多轮对话（通过 `session_id` 或显式 `messages` 数组）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params`）
  - 调试信息返回（启用 `debug` 字段）
  - 模型用量统计（`usage.models` 中含 `model_id`、`input_tokens`、`output_tokens`）

> **注意**：文档 1 和文档 2 均列出相同调用方式与示例代码，但文档 1 明确声明“仅适用于华北2（北京）地域”，而文档 2 未提及地域限制。实际调用需以控制台所选地域为准，建议优先参考 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 的地域说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用管理页面获取的唯一 ID，区分智能体与工作流应用 |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 用户输入的自然语言指令；若使用 `messages` 模式则不应传此字段 |
| `messages` | array | 否（推荐用于多轮） | 格式同 OpenAI：`[{ "role": "user/system/assistant", "content": "..." }]`；优先级高于 `session_id` |
| `session_id` | string | 否（用于云端历史） | 由服务端生成或复用，有效期 1 小时，最多支持 50 轮对话 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "{plugin_code}": { ... } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `parameters` | object | 否 | 预留扩展字段，当前暂无通用语义，可设为空对象 `{}` |
| `debug` | object | 否 | 设为空对象 `{}` 可启用调试模式，返回更详细的执行链路信息 |

## 使用方式

### 前提条件
- 已[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- 已在百炼控制台创建对应类型应用，并复制 `APP_ID`
- 若使用 SDK，需安装对应语言版本（Python 推荐 ≥1.14.0，Java 推荐 ≥2.12.0）

### 调用示例（统一接口）
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
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {"prompt": "你是谁？"},
          "parameters": {},
          "debug": {}
        }'
  ```

- **插件参数透传（关键场景）**：  
  通过 `biz_params.user_defined_params` 传递插件入参，`{your_plugin_code}` 需替换为控制台插件卡片上显示的实际插件 ID，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，其他地域可能返回 404 或权限错误，见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **安全规范**：API Key **严禁硬编码**，必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入；生产环境应配合密钥轮转与访问控制策略。
- **多轮对话约束**：
  - `session_id` 方式：自动加载云端历史，但有效期仅 1 小时，且最多保留 50 轮上下文；
  - `messages` 方式：推荐用于精确控制上下文长度与内容，避免因服务端历史截断导致逻辑异常。
- **插件调用前提**：自定义插件必须已发布，且与目标智能体应用处于同一业务空间；插件输入参数的 `传参方式` 必须配置为 **业务透传**，否则 `biz_params` 无效。
- **错误处理**：所有响应均含 `request_id`，错误时需结合 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 定位问题。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


