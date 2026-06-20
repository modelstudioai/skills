# bailian [application call](../api/application-call.md)ing

阿里云百炼平台支持通过 [DashScope SDK](../concepts/dashscope-sdk.md) 或 HTTP API 将已创建的应用集成到业务系统中。本页汇总了工作流应用和智能体应用的调用方式，以及自定义参数传递的用法，帮助开发者快速完成应用集成。

## 前提条件

无论调用哪种类型的应用，都需要先完成以下准备工作：

1. **获取 API Key** — 在百炼控制台的密钥管理页面创建并获取 `DASHSCOPE_API_KEY`，建议配置到环境变量中，避免硬编码。
2. **创建应用并获取 APP_ID** — 在应用管理页面创建工作流应用或智能体应用，复制应用卡片上的 APP_ID。
3. **安装 SDK（可选）** — 若使用 [DashScope SDK](../concepts/dashscope-sdk.md) 调用，需安装对应语言的 SDK；若使用 HTTP 接口则可跳过。

> **注意**：当前应用调用接口仅适用于中国大陆版（北京地域）。详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 的前提条件说明。

## 支持的应用类型

百炼平台当前支持两种应用的 API 调用：

- **工作流应用** — 通过可视化编排节点构建的应用，适合复杂业务流程。详细调用方式参见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **智能体应用** — 基于大模型的单智能体应用，可关联插件和知识库。详细调用方式参见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。

两种应用的调用接口基本一致，均使用 `Application.call()` 方法（SDK）或 `POST /api/v1/apps/{APP_ID}/completion` 端点（HTTP），核心区别在于创建应用的方式和可选参数不同。

## 调用方式

### [DashScope SDK](../concepts/dashscope-sdk.md)

支持 Python 和 Java 两种语言：

**Python 示例：**

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你的问题')

if response.status_code != HTTPStatus.OK:
    print(f'code={response.status_code}, message={response.message}')
else:
    print(response.output.text)
```

**Java 示例：**

```java
// 建议 dashscope SDK >= 2.12.0
ApplicationParam param = ApplicationParam.builder()
    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
    .appId("YOUR_APP_ID")
    .prompt("你的问题")
    .build();

Application application = new Application();
ApplicationResult result = application.call(param);
System.out.println(result.getOutput().getText());
```

### HTTP API

使用 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，请求体结构如下：

```json
{
    "input": {
        "prompt": "你的问题"
    },
    "parameters": {},
    "debug": {}
}
```

需要在请求头中设置 `Authorization: Bearer $DASHSCOPE_API_KEY`。支持 curl、PHP、Node.js、C#、Go 等多种语言，具体示例请参考 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 和 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。

## 多轮对话

应用调用支持两种多轮对话方式：

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| `session_id` | 系统自动从云端加载对话历史，无需开发者维护 | 简单场景，快速接入 |
| `messages` 数组 | 开发者自行维护对话历史并逐轮传递 | 需要精细控制上下文 |

> **注意**：`session_id` 有效期为 1 小时，最多支持 50 轮对话。若请求中同时包含 `session_id` 和 `messages`，系统将优先使用 `messages`。

使用 `messages` 方式时，工作流应用需要在大模型节点中配置提示词变量 `historyList` 并重新发布应用。

## 自定义参数传递

通过 `biz_params` 字段可以向应用中的自定义插件或自定义节点传递业务参数，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

### 自定义插件参数

自定义插件的参数通过 `biz_params.user_defined_params` 传递，适用于智能体应用关联的自定义插件或工作流应用中的插件节点。关键步骤：

1. **创建自定义插件** — 在百炼控制台的插件管理页面创建插件，配置输入参数时将传参方式设为「业务透传」。
2. **关联应用** — 将插件关联到智能体应用或工作流应用，然后发布。
3. **API 调用时传参** — 在 `biz_params` 中指定插件 ID 和参数键值对。

```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {   # 替换为实际的插件 ID
            "article_index": 2  # 插件的输入参数
        }
    }
}
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='查询内容',
    biz_params=biz_params)
```

### 插件鉴权

当自定义插件启用了用户级鉴权（如 Basic Auth）时，需要在调用时通过 `biz_params.user_defined_tokens` 传入用户的鉴权凭证：

```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    },
    "user_defined_tokens": {
        "your_plugin_code": {
            "user_token": "实际的用户凭证"
        }
    }
}
```

### 工作流自定义节点参数

工作流应用中的自定义节点参数也通过 `biz_params` 传递，使用 `customStartNode` 指定起始节点的输入变量：

```python
biz_params = {
    "customStartNode": {
        "variable_name": "variable_value"
    }
}
```

## 关键注意事项

- API Key 应通过环境变量传递，不要硬编码到代码中。
- `APP_ID` 需替换为实际创建的应用 ID，可在应用管理页面的应用卡片上获取。
- Python SDK 建议版本 >= 1.14.0（使用 `biz_params` 时），Java SDK 建议版本 >= 2.12.0。
- 插件 ID 可在百炼控制台的插件卡片上获取。
- 插件参数描述要清晰准确，有助于大模型正确理解和调用插件。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


