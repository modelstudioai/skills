# bailian [application call](../api/application-call.md)ing

百炼应用调用是通过统一的 `apps/completions` API 接口，将已发布的智能体应用（Agent 1.0）或工作流应用集成至业务系统的标准方式。该机制支持单轮/多轮对话、自定义插件参数透传及上下文管理，适用于构建 AI 原生应用。所有调用均需使用 DashScope SDK 或 HTTP API，并依赖有效的 API Key 和应用 ID。

## 支持的模型/功能

- **应用类型**：仅支持已发布的**智能体应用（Agent 1.0）** 和 **工作流应用**；智能体编排应用已被工作流应用替代 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
- **模型能力**：底层可调度 Qwen 系列大语言模型（如 `qwen-max`、`qwen-plus`），但**工作流应用不支持文生图类大模型** [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心功能**：
  - 单轮指令响应（`prompt` 字段）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组）
  - 自定义插件参数透传（仅限智能体应用与工作流应用中的插件节点）
  - 调试信息返回（`debug` 字段）

> **注意**：文档 2 明确声明“百炼工作流不支持使用文生图大模型”，而文档 1 和 3 均未提及此限制，但未否定该约束。因此该限制以文档 2 为准，开发者在工作流中调用图像生成节点将失败。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 |
| `input.prompt` | string | ✓（单轮） | 用户输入的自然语言指令；若使用 `messages` 则此项可省略 |
| `input.biz_params` | object | ✗ | 用于传递自定义插件参数，结构为 `{"user_defined_params": {"{plugin_code}": {key: value}}}` [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `input.messages` | array | ✗（多轮推荐） | 显式维护的对话历史，格式同 OpenAI `messages`，优先级高于 `session_id` |
| `session_id` | string | ✗（多轮可选） | 由服务端维护的会话 ID，有效期 1 小时，最多 50 轮；若与 `messages` 同时存在，系统**优先使用 `messages`** |
| `parameters` | object | ✗ | 预留扩展字段，当前暂无业务含义，建议传空对象 `{}` |
| `debug` | object | ✗ | 预留调试字段，当前建议传空对象 `{}` |

## 使用方式

### 1. 基础调用（单轮）
所有语言 SDK 和 HTTP 接口均采用相同语义：
- Python SDK：`client.apps.completions.create(app_id='xxx', prompt='xxx')`
- Java SDK：`ApplicationParam.builder().appId('xxx').prompt('xxx').build()`
- HTTP：POST `/api/v1/apps/{app_id}/completion`，body 中 `input.prompt` 为必需字段

示例（Python）：
```python
import os
import dashscope
client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
response = client.apps.completions.create(
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)
print(response.text)
```

### 2. 多轮对话
- **推荐方式（显式 `messages`）**：客户端自行维护 `messages = [{"role": "user", "content": "..."}, ...]`，每次请求携带完整历史。
- **便捷方式（`session_id`）**：首次调用不传 `session_id`，响应中提取 `output.session_id`，后续请求复用该值。

### 3. 自定义插件参数透传
仅适用于已关联插件的智能体应用或含插件节点的工作流应用：
- 插件参数必须在创建工具时配置为 **业务透传（Body）** 方式；
- 通过 `biz_params.user_defined_params.{plugin_code}` 传入键值对；
- 插件 ID 可在控制台插件卡片上获取。

示例（HTTP body 片段）：
```json
{
  "input": {
    "prompt": "查询寝室公约第二条",
    "biz_params": {
      "user_defined_params": {
        "domitory_agreement_tool": {"article_index": 2}
      }
    }
  }
}
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，其他地域请求将失败 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **API Key 安全**：严禁硬编码 `sk-xxx` 到源码；必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入，SDK 默认读取该变量。
- **SDK 版本要求**：
  - Python：`dashscope >= 2.0.1`（插件参数支持）；
  - Java：`dashscope-sdk-java >= 2.12.0`（推荐，兼容多轮与插件）。
- **插件鉴权**：若插件开启用户级鉴权（如 Basic Auth），需确保插件后端能正确解析 Header 中的凭证，百炼平台不代理鉴权逻辑。
- **错误处理**：所有 SDK 均抛出 `DashScopeError`（Python）、`ApiException`（Java）等异常，务必捕获并检查 `request_id` 用于问题定位。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)


