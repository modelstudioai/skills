# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用、工作流应用等集成至外部业务系统的能力。该能力统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心场景，是构建 AI 原生应用的关键链路。所有调用均需有效 API Key 与合法 APP_ID。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心功能**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组维护上下文）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 向关联插件传递业务参数），适用于智能体应用和工作流应用中的插件节点；
  - 调试信息返回（启用 `debug` 字段可获取执行路径、节点耗时等诊断数据）。

> **注意**：文档2明确说明“百炼工作流不支持使用文生图大模型”，而文档1未提及此限制；实际调用中，若工作流应用内含图像生成节点，将直接报错。请以 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 的约束为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台生成的应用唯一标识，见 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)。 |
| `prompt` | string | 否（与 `messages` 互斥） | 单轮指令文本；若提供 `messages`，则忽略此字段。 |
| `messages` | array | 否（与 `prompt` 互斥） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于显式管理多轮上下文（推荐方式）。 |
| `session_id` | string | 否 | 由服务端生成或客户端指定的会话 ID，用于自动加载云端历史（有效期 1 小时，最多 50 轮）。 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。 |
| `parameters` | object | 否 | 应用级超参（如 `temperature`, `max_output_tokens`），具体字段取决于应用配置。 |
| `debug` | object | 否 | 空对象 `{}` 即启用调试模式，返回详细执行日志。 |

## 使用方式

### 1. 前置准备
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并配置，推荐[配置为环境变量 `DASHSCOPE_API_KEY`](../../raw/model-api-reference/preparations/get-api-key.md)；
- 获取 APP_ID：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用卡片上的 ID；
- （可选）安装 SDK：Python、Java、Node.js 等语言需安装对应 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)，HTTP 方式无需安装。

### 2. 调用示例（Python SDK）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 自动读取环境变量
    app_id="YOUR_APP_ID",
    prompt="你好，请介绍自己",
    biz_params={  # 透传插件参数（按需）
        "user_defined_params": {
            "plugin_abc123": {"query_id": 42}
        }
    }
)

if response.status_code == 200:
    print(response.output.text)
else:
    print(f"Error {response.status_code}: {response.message}")
```

### 3. HTTP 调用（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "input": {
      "prompt": "你好",
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

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无此限制（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）；
- **会话管理**：`session_id` 有效期为 1 小时，且最多承载 50 轮对话；超出后需新建会话或改用 `messages` 显式管理；
- **参数优先级**：当请求同时包含 `session_id` 和 `messages` 时，系统**优先使用 `messages`**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）；
- **插件参数安全**：`biz_params.user_defined_params` 中的插件 ID 必须与应用已关联的插件完全一致，否则参数被忽略；
- **错误处理**：所有调用均返回标准 HTTP 状态码及 `request_id`，错误详情请参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


