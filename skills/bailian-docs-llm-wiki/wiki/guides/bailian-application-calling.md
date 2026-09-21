# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至外部业务系统的开发方式。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心能力，适用于构建 AI 原生业务逻辑。所有调用均需有效 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **模型能力**：底层自动路由至应用所绑定的大模型（如 `qwen-max`、`qwen-plus` 等），不支持在调用时显式指定模型 ID；**工作流应用明确不支持文生图类大模型**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **高级功能**：
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params`）；
  - 调试信息返回（启用 `debug` 字段）。

> **注意**：文档 1 和文档 2 中的 Python/Java/HTTP 示例代码完全一致，但文档 2 明确声明“**仅适用于华北2（北京）地域**”，而文档 1 未提及地域限制。实际部署时请以 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 的地域约束为准，智能体应用调用亦建议优先部署于华北2。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用管理页获取的应用唯一标识符（APP_ID） |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 当前轮次用户输入文本；若使用 `messages` 数组则无需此字段 |
| `messages` | array | 否（若提供则替代 `prompt`） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于精确控制上下文（推荐方式） |
| `session_id` | string | 否 | 由服务端生成的会话标识，用于自动加载历史对话（有效期 1 小时，最多 50 轮） |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": "<value>" } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `parameters` | object | 否 | 预留扩展字段，当前暂无公开可用参数 |
| `debug` | object | 否 | 设为空对象 `{}` 可启用调试模式，返回更详细的执行链路信息 |

## 使用方式

### 1. 前置准备
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 在百炼控制台创建并发布目标应用，复制其 `app_id`；
- 若使用 SDK，按语言安装对应版本（Python ≥1.14.0，Java ≥2.12.0）。

### 2. 调用示例（SDK 方式）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你好",
    # 或使用 messages 实现多轮（推荐）
    # messages=[{"role": "user", "content": "你好"}]
)
print(response.output.text)
```

### 3. HTTP 直连方式
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
            "prompt": "你好",
            "biz_params": {
                "user_defined_params": {
                    "your_plugin_code": {"article_index": 2}
                }
            }
        }
      }'
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用虽未明文限制，但跨地域调用可能失败，建议统一部署于华北2；
- **会话管理**：`session_id` 有效期为 1 小时且最多承载 50 轮对话；若同时传入 `session_id` 和 `messages`，系统**优先使用 `messages`**；
- **插件参数**：`biz_params.user_defined_params` 仅对已关联插件的智能体/工作流应用生效，插件 ID 需与控制台中插件卡片显示的 ID 完全一致；
- **安全实践**：严禁在代码中硬编码 `DASHSCOPE_API_KEY`，必须通过环境变量或密钥管理服务注入；
- **错误处理**：所有调用均返回 `request_id`，用于问题排查；错误码参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


