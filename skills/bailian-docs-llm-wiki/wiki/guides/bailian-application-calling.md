# bailian [application call](../api/application-call.md)ing

本主题汇总阿里云百炼平台两类应用——**智能体应用**与**工作流应用**——的 API 调用方式，涵盖 DashScope SDK 与 HTTP 接口的快速接入、多轮对话上下文管理，以及自定义插件/节点的业务参数透传。所有调用统一指向 `https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，仅通过 `app_id` 区分应用类型。

> **注意**：调用接口仅适用于**中国大陆版（北京地域）**。智能体编排应用已被工作流应用替代，新接入请直接选择工作流应用。

## 支持的应用类型与 SDK

| 应用类型 | 适用接口 | 说明 |
| --- | --- | --- |
| 智能体应用 (Single-Agent) | DashScope SDK / HTTP | 单一智能体，通过关联插件扩展能力。详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。 |
| 工作流应用 (Workflow) | DashScope SDK / HTTP / Responses API | 由开始节点、大模型节点、插件节点等组成的有向图。详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。 |

官方提供的 SDK / 语言覆盖：Python、Java、HTTP（cURL）、PHP、Node.js、C#、Go。建议版本：

- DashScope Python SDK ≥ 1.14.0（自定义参数透传场景）/ 通用场景安装最新即可（`python3 -m pip install -U dashscope`）。
- DashScope Java SDK ≥ 2.12.0（Maven artifact: `com.alibaba:dashscope-sdk-java`）。

## 前置条件

1. **获取 API Key**：[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 页面创建，推荐通过 `DASHSCOPE_API_KEY` 环境变量注入，避免硬编码。
2. **获取 APP_ID**：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 中创建智能体或工作流应用后，从应用卡片复制。
3. **安装 SDK**（仅 SDK 调用需要）：Python `pip install -U dashscope`；Java 在 `pom.xml` / `build.gradle` 中引入依赖。HTTP 调用可跳过此步。

## 核心调用参数

请求体根字段为 `input` / `parameters` / `debug`，SDK 上对应 `ApplicationParam`（Java）或 `Application.call()` 关键字参数（Python）。

| 字段 | 类型 | 必填 | 作用 |
| --- | --- | --- | --- |
| `app_id` / `appId` | string | 是 | 目标应用 ID。 |
| `api_key` / `apiKey` | string | 是 | 鉴权凭证；建议从环境变量读取。 |
| `prompt` | string | 否 | 用户当前轮指令。当传入 `messages` 时可省略。 |
| `messages` | array | 否 | 自行管理的多轮对话历史；存在时优先级高于 `session_id`。 |
| `session_id` | string | 否 | 云端托管的会话 ID，自动加载历史。**有效期 1 小时，最多 50 轮**。 |
| `biz_params.user_defined_params` | object | 否 | 自定义插件/节点的业务透传参数，键为插件 ID 或节点 ID。详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。 |
| `parameters` | object | 否 | 预留扩展字段，通常为空对象。 |
| `debug` | object | 否 | 调试控制，通常为空对象。 |

## 使用方式

### 快速调用（单轮）

最小示例（Python，工作流/智能体写法一致，仅 `app_id` 不同）：

```python
import os
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？')

print(response.output.text)
```

HTTP 等价请求：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"input":{"prompt":"你是谁？"},"parameters":{},"debug":{}}'
```

成功响应结构：

```json
{
  "output": { "finish_reason": "stop", "session_id": "...", "text": "..." },
  "usage":  { "models": [{ "model_id": "qwen-plus", "input_tokens": 74, "output_tokens": 79 }] },
  "request_id": "..."
}
```

调用失败时返回非 200 状态码，`request_id` / `code` / `message` 字段可用于排查，错误码详情参见 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

### 多轮对话

工作流应用在大模型节点中需配置提示词变量 `historyList` 并**发布**后才能进行 API 多轮调用。

两种实现方式：

- **使用 `session_id`**：云端自动维护历史，实现简单；受 1 小时 / 50 轮限制约束，仅适合短周期会话。
- **自行管理 `messages`（推荐）**：客户端维护对话数组，每轮把完整历史和新指令一起发送，无需传 `prompt`；可控性更高、上下文不受时长限制。

> **注意**：若同一请求同时携带 `session_id` 和 `messages`，系统**只使用 `messages`**。

### 自定义参数透传

适用于在自定义插件或工作流自定义节点中接收外部传入的业务变量，例如把内部业务 ID、用户上下文直送插件后端。流程：

1. 在控制台创建插件工具，将目标输入参数的**传参方式**设为**业务透传**（创建步骤、鉴权配置见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。
2. 将插件关联到**同一[业务空间](../concepts/workspace.md)**下的智能体应用，并发布应用。
3. 调用时通过 `biz_params.user_defined_params.<plugin_id>` 传入键值：

```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": { "article_index": 2 }
    }
}
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='寝室公约内容',
    biz_params=biz_params)
```

HTTP 调用时把 `biz_params` 放在 `input` 内：

```json
{
  "input": {
    "prompt": "寝室公约内容",
    "biz_params": {
      "user_defined_params": {
        "{your_plugin_code}": { "article_index": 2 }
      }
    }
  }
}
```

> **注意**：自定义插件参数透传同时支持智能体应用与工作流应用——前者通过关联的智能体应用直接传递，后者通过工作流中的**插件节点**传递。详细规则参考 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 限制与注意事项

- **地域限制**：当前仅支持中国大陆版（北京地域）。
- **`session_id` 限制**：有效期 1 小时，最多 50 轮；超出需改用 `messages` 自管理。
- **插件作用域**：自定义插件仅能与**同一[业务空间](../concepts/workspace.md)**的智能体应用关联。
- **插件描述与参数命名**：插件描述、工具描述、参数名/参数描述都会被大模型用于判断是否调用、如何取参，务必使用自然语言、清晰准确，并尽量给出示例。
- **传参方式**：若希望参数完全由调用方传入而非大模型推断，**必须**将输入参数设为**业务透传**。
- **API Key 安全**：禁止把 `sk-xxx` 硬编码到生产代码，统一通过环境变量加载。
- **错误处理**：所有 SDK 都返回 `status_code` / `request_id` / `message`，建议在生产代码里完整记录这三项以便定位问题。
- **Responses API**：如果偏好使用与 OpenAI 兼容的 Responses 风格调用，可改用 [Responses API](https://help.aliyun.com/zh/model-studio/openai-responses-api/)（工作流应用提供）。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)






