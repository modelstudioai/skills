# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用、工作流应用等集成至外部业务系统的能力。该能力统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心场景，适用于从简单问答到复杂业务编排的各类需求。所有调用均需有效 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：支持两类主流应用——[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)（Agent 1.0）和[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，后者为智能体编排应用的演进形态。
- **核心功能**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件专属参数）
- **模型绑定**：应用在控制台发布时已绑定底层大模型（如 `qwen-max`、`qwen-plus`），调用时无需指定模型 ID；响应中 `usage.models[].model_id` 可回溯实际执行模型。

> **注意**：文档 2 明确声明“百炼工作流不支持使用文生图大模型”，而文档 1 和 3 均未提及此限制。鉴于工作流应用是当前主推架构，该限制应视为有效约束，开发者不可在工作流应用中配置或触发图像生成类节点。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 |
| `prompt` | string | 否（若提供 `messages` 则非必填） | 当前轮次用户输入文本；与 `messages` 互斥，同时存在时以 `messages` 为准 |
| `messages` | array | 否（若提供则替代 `prompt`） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于精确控制多轮上下文 |
| `session_id` | string | 否 | 由服务端生成的会话标识，启用云端历史加载；有效期 1 小时，最多 50 轮 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |

## 使用方式

### 1. 前置准备
- 获取 API Key：前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建并配置，推荐[配置为环境变量 `DASHSCOPE_API_KEY`](../../raw/model-api-reference/preparations/get-api-key.md)。
- 获取 `app_id`：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中复制目标应用卡片上的 ID。
- （可选）安装 SDK：Python、Java、Node.js 等语言需安装对应 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)；HTTP 调用无需 SDK。

### 2. 调用示例（Python SDK）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 调用（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
      "prompt": "你是谁？"
    }
  }'
```

### 4. 自定义插件调用（需配置插件）
```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    }
}
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="寝室公约内容",
    biz_params=biz_params
)
```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无此限制（见[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。
- **多轮对话策略**：
  - `session_id` 方式便捷但灵活性低，且受 1 小时/50 轮硬限制；
  - `messages` 方式需客户端自行维护完整对话历史，推荐用于生产环境以保障上下文可控性。
- **安全实践**：
  - **严禁硬编码 API Key**：所有示例均强调应通过环境变量（如 `DASHSCOPE_API_KEY`）注入，而非写入源码。
  - 插件鉴权：若插件开启鉴权，需在插件配置中正确设置 Header/BASIC 等方式，SDK 与 HTTP 调用均不自动处理插件级鉴权逻辑。
- **错误处理**：所有调用均返回 `request_id`，务必记录该字段用于问题排查；错误码参考[错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


