# bailian [application call](../api/application-call.md)ing

阿里云百炼支持通过 [DashScope SDK](../concepts/dashscope-sdk.md) 或 HTTP API 将已创建的应用集成到业务系统中。可调用的应用类型包括**[智能体应用](../concepts/agent-application.md)**和**[工作流](../concepts/workflow.md)应用**（[智能体编排](../concepts/agent-orchestration.md)应用已被[工作流](../concepts/workflow.md)应用替代），二者调用方式一致，均通过 `Application.call` / `POST /apps/{app_id}/completion` 触发，区别仅在于应用内部编排逻辑和可附加的扩展能力（如自定义参数传递）。

## 前提条件

无论调用哪种应用，都需要先完成以下准备：

1. **获取 [API Key](../concepts/api-key.md)**：在百炼控制台密钥管理页面创建 [API Key](../concepts/api-key.md)。
2. **配置环境变量（推荐）**：将 [API Key](../concepts/api-key.md) 写入 `DASHSCOPE_API_KEY` 环境变量，避免在代码中硬编码。SDK 会自动读取该变量。
3. **获取应用 ID**：在应用管理页面创建对应应用（[智能体应用](../concepts/agent-application.md) / [工作流](../concepts/workflow.md)应用），并从应用卡片复制 `APP_ID`。
4. **安装 [DashScope SDK](../concepts/dashscope-sdk.md)**（HTTP 调用可跳过）：Python 通过 `python3 -m pip install -U dashscope`；Java 通过 Maven/Gradle 添加 `com.alibaba:dashscope-sdk-java` 依赖（建议版本 >= 2.12.0）；Node.js 安装 `axios`。

## 基本调用方式

[智能体应用](../concepts/agent-application.md)与[工作流](../concepts/workflow.md)应用的调用接口完全相同，详见[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)与[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。核心请求结构如下：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json

{
  "input": { "prompt": "你是谁？" },
  "parameters": {},
  "debug": {}
}
```

### Python

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
else:
    print(response.output.text)
```

### Java

```java
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.*;

ApplicationParam param = ApplicationParam.builder()
    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
    .appId("YOUR_APP_ID")
    .prompt("你是谁？")
    .build();

Application application = new Application();
ApplicationResult result = application.call(param);
System.out.printf("text: %s\n", result.getOutput().getText());
```

### Node.js / curl

Node.js 使用 `axios` 发起 POST 请求即可，结构与 curl 示例一致：

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

响应统一为 `{"output": {"finish_reason", "session_id", "text"}, "usage": {...}, "request_id": "..."}` 结构，业务侧主要消费 `output.text`。

## 多轮对话

[工作流](../concepts/workflow.md)应用支持多轮对话，详见[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。两种实现方式：

- **使用 `session_id`**：系统自动从云端加载历史对话，实现简单。`session_id` 有效期 1 小时，最多支持 50 轮对话。
- **自行管理 `messages`（推荐）**：手动维护 `messages` 数组传递每轮历史，无需传 `prompt`，控制更灵活。

> **注意**：若请求中同时包含 `session_id` 和 `messages`，系统将优先使用 `messages`。

使用 `messages` 时，需先在[工作流](../concepts/workflow.md)的大模型节点中配置提示词变量 `historyList` 并发布应用，再发起调用。

## 自定义参数传递

针对自定义插件与自定义节点，百炼支持通过 `biz_params` 的 `biz_params.user_defined_params` 透传业务参数，详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。该能力可用于[智能体应用](../concepts/agent-application.md)的自定义插件，以及工作流应用中的插件节点。

### 使用流程

1. **创建自定义插件**：在百炼控制台插件页面新增自定义插件，按需配置鉴权（如用户级鉴权 + Header + basic）。创建工具时，输入参数的**传参方式务必选择「业务透传」**，并发布插件。
2. **关联应用**：插件工具只能与同一[业务空间](../concepts/workspace.md)内的[智能体应用](../concepts/agent-application.md)关联；工作流应用则在插件节点中引用。关联后发布应用。
3. **API 调用**：通过 `biz_params.user_defined_params` 传递插件 ID 与入参键值对。

### 请求示例

```python
import os
from http import HTTPStatus
from dashscope import Application

biz_params = {
    "user_defined_params": {
        "your_plugin_code": {   # 替换为实际插件 ID（在插件卡片获取）
            "article_index": 2
        }
    }
}

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='寝室公约内容',
    biz_params=biz_params
)
```

HTTP 请求体中 `biz_params` 位于 `input` 下：

```json
{
  "input": {
    "prompt": "寝室公约内容",
    "biz_params": {
      "user_defined_params": {
        "your_plugin_code": { "article_index": 2 }
      }
    }
  },
  "parameters": {},
  "debug": {}
}
```

Java SDK 通过 `JsonUtils.parse(...)` 将 JSON 字符串转为对象传入 `ApplicationParam.bizParams`。

## 关键参数

| 参数 | 位置 | 说明 |
| --- | --- | --- |
| `app_id` / `APP_ID` | URL path | 应用 ID，从应用卡片获取 |
| `prompt` | `input.prompt` | 单轮对话的输入指令（与 `messages` 二选一） |
| `messages` | `input.messages` | 自行维护的多轮对话历史（推荐，优先级高于 `session_id`） |
| `session_id` | `input.session_id` | 云端会话 ID，有效期 1 小时，最多 50 轮 |
| `biz_params` | `input.biz_params` | 业务透传参数，含 `user_defined_params` |
| `parameters` | 顶层 | 应用级参数 |
| `debug` | 顶层 | 调试信息 |

## 限制和注意事项

- **地域限制**：[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 文档明确仅适用于华北2（北京）地域。
- **应用类型替代关系**：[智能体编排](../concepts/agent-orchestration.md)应用已被工作流应用替代，新场景应使用工作流应用。
- **`session_id` 约束**：有效期 1 小时，最多 50 轮；与 `messages` 同时存在时优先使用 `messages`。
- **插件业务透传**：自定义插件的输入参数传参方式必须选择「业务透传」，否则无法通过 `biz_params` 传递；插件 ID 在插件卡片获取，替换示例中的 `your_plugin_code`。
- **[业务空间](../concepts/workspace.md)隔离**：插件工具只能与同一[业务空间](../concepts/workspace.md)内的[智能体应用](../concepts/agent-application.md)关联。
- **密钥安全**：不要在生产环境硬编码 [API Key](../concepts/api-key.md)，统一通过 `DASHSCOPE_API_KEY` 环境变量注入。
- **Responses API**：如需使用 OpenAI 兼容的 Responses API 调用工作流应用，需参阅 Responses API 文档，不在本文调用方式范围内。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)


































