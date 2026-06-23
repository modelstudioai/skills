# bailian [application call](../api/application-call.md)ing

百炼平台支持通过 [DashScope SDK](../concepts/dashscope-sdk.md) 或 HTTP API 将智能体应用和工作流应用集成到业务系统中。本页汇总了两类应用的调用方式、多轮对话管理以及自定义插件参数传递的核心要点。

## 前提条件

调用百炼应用前需完成以下准备：

1. **获取 API Key** 并配置到环境变量 `DASHSCOPE_API_KEY`（推荐，避免硬编码）。
2. **创建应用** 并获取 `APP_ID`——在百炼控制台的应用管理页面，应用卡片上可复制。
3. **安装 SDK**（若使用 SDK 调用）：Python 需 `dashscope` 包，Java 需 Maven/Gradle 引入 `dashscope-sdk-java`。HTTP 调用无需安装。

> **注意**：工作流应用调用目前仅适用于中国大陆版（北京地域），详见[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

## 支持的应用类型

| 应用类型 | 说明 | 详细文档 |
|---------|------|---------|
| 智能体应用 | 单 Agent 应用，支持插件挂载与自定义参数传递 | [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) |
| 工作流应用 | 基于工作流编排的应用（已替代原智能体编排应用） | [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) |

两类应用的调用端点相同：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
```

## 基础调用方式

支持多种语言：Python、Java、curl、PHP、Node.js、C#、Go。以 Python 为例：

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

Java SDK 建议使用 `dashscope-sdk-java` 2.12.0 及以上版本。HTTP 调用需在 Header 中传入 `Authorization: Bearer $DASHSCOPE_API_KEY`。

## 多轮对话

两种方式管理对话上下文：

### 方式一：`session_id`（云端存储）

首次调用返回的 `session_id` 传入后续请求，系统自动加载历史对话。

- 有效期：1 小时
- 最多支持：50 轮对话
- 优点：实现简单，无需本地维护历史

### 方式二：`messages` 数组（推荐）

自行维护 `messages` 数组，手动记录并传递每轮对话历史。无需传递 `prompt`。

- 优点：完全控制上下文，更灵活
- 适合需要精细管理对话历史的场景

> **注意**：若请求中同时包含 `session_id` 和 `messages`，系统将优先使用 `messages`。工作流应用使用 `messages` 前，需在大模型节点配置提示词变量 `historyList` 并重新发布应用。

## 自定义插件参数传递

智能体应用可关联自定义插件，通过 API 调用时使用 `biz_params` 字段传递插件参数。详细流程参见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

### 关键步骤

1. **创建自定义插件**：在百炼控制台创建插件，配置输入参数时将传参方式设为"业务透传"。
2. **关联智能体应用**：插件与同一[业务空间](../concepts/workspace.md)内的智能体应用关联后发布。
3. **API 调用时传参**：通过 `biz_params.user_defined_params` 传递插件 ID 和参数。

```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {   # 替换为实际的插件 ID
            "article_index": 2  # 替换为实际的插件参数
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

创建插件时可开启鉴权，支持用户级鉴权，位置可选 Header，类型支持 basic 等。

### 注意事项

- 插件描述和工具描述应使用自然语言，帮助大模型判断何时调用插件。
- 参数名称应具有语义，参数描述要简练准确。
- 输入参数的传参方式务必选择"业务透传"。
- 插件 ID 可在控制台插件卡片上获取。
- 自定义插件参数也可通过工作流应用中的插件节点传递。

## 错误处理

调用失败时，响应中包含 `status_code` 和 `message` 字段。建议参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 排查问题。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)




