# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用、工作流应用等集成至外部业务系统的能力。该能力统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心场景，适用于构建 AI 原生应用和服务编排。所有调用均需有效 API Key 与合法 APP_ID。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心功能**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组维护上下文）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 向关联插件传递业务参数），详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 调试信息返回（启用 `debug` 字段可获取执行路径、节点耗时等诊断数据）。

> **注意**：文档 2 明确指出“百炼工作流不支持使用文生图大模型”，而文档 1 和文档 3 均未提及此限制；实际调用中若涉及多模态节点，须确认所选工作流应用未包含图像生成类模型，否则请求将失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✅ | 百炼控制台应用卡片上复制的唯一 ID，区分智能体与工作流应用。 |
| `prompt` | string | ⚠️（见下文） | 单轮调用时必填；若使用 `messages` 进行多轮对话或调用含 `historyList` 提示词变量的应用，则可省略。 |
| `messages` | array | ❌（但推荐用于多轮） | 替代 `prompt` 的结构化消息数组（格式同 OpenAI ChatML），优先级高于 `session_id`。 |
| `session_id` | string | ❌ | 由服务端自动分配或客户端指定，用于加载云端存储的最多 50 轮历史对话（有效期 1 小时）。 |
| `biz_params` | object | ❌ | 仅当应用关联了自定义插件时需设置，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`。 |
| `parameters` | object | ❌ | 预留扩展字段，当前暂无通用语义，部分应用内节点可能使用。 |
| `debug` | object | ❌ | 设为空对象 `{}` 即可启用调试模式，返回详细执行日志。 |

## 使用方式

### 1. 前置准备
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 在百炼控制台创建对应类型应用（[智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md) 或 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)），获取 `APP_ID`；
- 若使用 SDK，按语言安装对应版本（Python ≥1.14.0，Java ≥2.12.0）。

### 2. 调用示例（统一接口）
所有语言均调用同一 HTTP 端点：  
`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`

- **SDK 方式（Python 示例）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？",
      # biz_params={...}  # 如需透传插件参数，添加此字段
      # session_id="xxx"   # 如需复用会话，添加此字段
  )
  ```

- **HTTP 方式（curl 示例）**：
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

### 3. 多轮对话建议
- **推荐方式**：客户端自行管理 `messages` 数组（如 `[{"role":"user","content":"你好"},{"role":"assistant","content":"我是千问"}]`），每次请求携带完整历史，避免服务端状态依赖；
- **简化方式**：首次调用不传 `session_id`，从响应中提取 `session_id`，后续请求复用该值。

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无此限制（文档 2 明确声明，文档 1 未提及）。
- **插件参数要求**：自定义插件的输入参数必须在控制台配置为“业务透传”方式，否则 `biz_params` 无法生效。
- **安全实践**：
  - 绝对禁止在代码中硬编码 `DASHSCOPE_API_KEY`，必须通过环境变量或密钥管理服务注入；
  - 生产环境应启用 HTTPS 并校验服务端证书。
- **错误处理**：所有调用均返回标准 HTTP 状态码与 `request_id`，错误详情请参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。
- **配额与限流**：具体 QPS 与 Token 限额取决于所购百炼服务包，超出将返回 `429 Too Many Requests`。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


