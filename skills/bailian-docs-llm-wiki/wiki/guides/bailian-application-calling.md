# bailian [application call](../api/application-call.md)ing

百炼 Application Calling 是百炼平台提供的统一 API 调用入口，支持通过 DashScope SDK 或标准 HTTP 接口调用已发布的智能体应用（Agent 1.0）和工作流应用（Workflow Application），实现模型能力与业务逻辑的快速集成。该机制屏蔽底层模型调度与编排细节，开发者仅需关注应用 ID、输入提示与可选参数即可完成端到端调用。所有调用均需在华北2（北京）地域发起。

## 支持的模型/功能

- **支持的应用类型**：智能体应用（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）和工作流应用（[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。  
- **不支持的模型类型**：工作流应用明确不支持文生图类大模型（如 wanx 系列），仅限文本生成类模型（如 `qwen-max`、`qwen-plus` 等）。  
- **核心能力**：单轮问答、多轮对话（通过 `session_id` 或显式 `messages`）、自定义[插件](../concepts/plugin.md)参数透传（需在应用中配置[插件](../concepts/plugin.md)节点或关联[插件](../concepts/plugin.md)）、调试信息返回（`debug` 字段）。  
- **智能体编排应用已下线**：文档明确指出“智能体编排应用已被工作流应用替代”（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)），当前仅维护工作流应用作为标准编排载体。

> **注意**：文档 1 和文档 2 均提供几乎完全一致的 SDK/HTTP 调用示例（含 Python/Java/curl/PHP/Node.js/C#/Go），但文档 1 明确限定“仅适用于华北2（北京）地域”，而文档 2 未提及地域限制。实际部署时请以文档 1 的地域约束为准，避免跨地域调用失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取。 |
| `prompt` | string | 否（若提供 `messages` 则不可用） | 单轮输入文本；若启用多轮对话且使用 `messages`，则此字段应省略。 |
| `messages` | array | 否（若提供则替代 `prompt`） | 显式对话历史数组，格式为 `[{"role": "user/system/assistant", "content": "..."}]`；优先级高于 `session_id`。 |
| `session_id` | string | 否 | 由服务端维护的会话 ID，有效期 1 小时，最多支持 50 轮对话；若同时传 `messages`，系统将忽略 `session_id`。 |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{"user_defined_params": {"<plugin_code>": {<key: value>}}}`（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。 |
| `parameters` | object | 否 | 预留模型级参数（如 `temperature`），当前工作流/智能体应用暂不开放用户直接配置。 |
| `debug` | object | 否 | 开启后返回详细执行链路信息（如节点耗时、插件调用日志），仅用于调试。 |

## 使用方式

### 前提条件
- 已获取并[配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)（推荐设为环境变量 `DASHSCOPE_API_KEY`）；
- 已创建目标应用并获取 `APP_ID`；
- 若使用 SDK，需安装对应语言的 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)，Python 推荐 ≥1.14.0，Java 推荐 ≥2.12.0。

### 调用示例（Python）
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

### 多轮对话（推荐方式：显式 `messages`）
```python
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "我是千问。"},
        {"role": "user", "content": "今天天气如何？"}
    ]
)
```

### 自定义插件参数传递
```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    }
}
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="查询寝室公约",
    biz_params=biz_params
)
```

## 限制和注意事项

- **地域限制**：所有调用必须在华北2（北京）地域发起，其他地域 endpoint 不可用（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）。  
- **API Key 安全**：严禁在代码中硬编码 `sk-xxx`，务必通过环境变量或密钥管理服务注入。  
- **会话管理**：`session_id` 由服务端生成并返回于响应头或 `output.session_id` 中；其有效期为 1 小时，超时后需新建会话。  
- **插件参数要求**：自定义插件的输入参数必须在控制台配置为“业务透传”方式，否则 `biz_params` 无法生效。  
- **错误处理**：响应非 `200` 时，需检查 `response.request_id` 并参考[错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)定位问题。  
- **HTTP Content-Type**：所有 HTTP 请求必须设置 `Content-Type: application/json`，否则返回 `415 Unsupported Media Type`。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


