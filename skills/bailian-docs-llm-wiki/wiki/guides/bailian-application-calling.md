# bailian [application call](../api/application-call.md)ing

百炼平台支持通过统一 API（DashScope SDK 或 HTTP 接口）调用智能体应用（Agent 1.0）、工作流应用（替代原智能体编排应用）等类型的应用。所有调用均基于 `POST /api/v1/apps/{app_id}/completion` 端点，核心参数为 `input.prompt` 和可选的 `input.biz_params`，适用于单轮与多轮对话场景。开发者需预先配置 API Key 并获取目标应用的 APP_ID。

## 支持的模型/功能

- **应用类型**：支持调用两类应用：
  - **智能体应用（Agent 1.0）**：面向任务导向的轻量级智能体，适用于简单工具调用与意图理解场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用**：支持复杂节点编排（如大模型节点、条件分支、插件节点等），已取代旧版“智能体编排应用”；**不支持文生图类大模型** [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮问答与指令执行；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组）；
  - 自定义插件参数透传（仅限关联了插件的智能体/工作流应用）；
  - 调试信息返回（通过 `debug` 字段）。

> **注意**：文档 1 中提及“智能体编排应用已被工作流应用替代”，而文档 2 和 3 均未再提及其存在，确认该表述为当前事实，旧文档中残留的“智能体编排应用”术语应视为过时，以工作流应用为准。

## 关键参数

| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| `app_id` | URL path | string | 是 | 应用唯一标识，在控制台「应用管理」页面获取 |
| `prompt` | `input.prompt` | string | 是（除非使用 `messages`） | 用户输入的自然语言指令，驱动应用执行逻辑 |
| `biz_params` | `input.biz_params` | object | 否 | 业务扩展参数，用于传递自定义插件参数等，结构见下文 |
| `session_id` | `input.session_id` | string | 否 | 启用云端历史上下文管理（有效期 1 小时，最多 50 轮） |
| `messages` | `input.messages` | array | 否（启用时替代 `prompt`） | 显式维护的对话历史数组，格式同 OpenAI `messages`，优先级高于 `session_id` |
| `parameters` | top-level | object | 否 | 预留字段，当前无实际作用，建议保持空对象 `{}` |
| `debug` | top-level | object | 否 | 设置为 `{}` 可返回调试信息（如 trace_id、节点执行日志） |

- **`biz_params.user_defined_params`**（插件参数透传）：  
  当应用关联了自定义插件时，通过此字段传递插件所需参数。结构为 `{ "plugin_code": { "param_key": param_value } }`，其中 `plugin_code` 为插件 ID，`param_key` 必须与插件工具配置中定义的**输入参数名称**完全一致（如 `article_index`），且该参数的**传参方式必须设为“业务透传”** [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 使用方式

### 1. 前置准备
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 安装对应语言的 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)（HTTP 调用可跳过）；
- 确保应用已发布，且（如需插件）已完成插件关联与发布。

### 2. SDK 调用（Python 示例）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="查询寝室公约第三条",
    biz_params={
        "user_defined_params": {
            "your_plugin_code": {"article_index": 3}
        }
    }
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 调用（curl 示例）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "查询寝室公约第三条",
          "biz_params": {
            "user_defined_params": {
              "your_plugin_code": {"article_index": 3}
            }
          }
        },
        "parameters": {},
        "debug": {}
      }'
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **SDK 版本要求**：
  - Python SDK：插件参数透传需 `dashscope >= 1.14.0`（文档 1）；通用调用建议 `>= 1.14.0`；
  - Java SDK：文档 2 与 3 均建议 `>= 2.12.0`，但文档 1 未明确要求，**以较新版本为准，避免兼容性问题**。
- **安全实践**：
  - **禁止硬编码 API Key**：所有示例均强调“不建议在生产环境中直接将 API Key 写入代码”，必须通过环境变量或密钥管理服务注入。
- **插件参数约束**：
  - 插件工具的输入参数**传参方式必须选择“业务透传”**，否则 `biz_params.user_defined_params` 无效；
  - 插件描述与工具描述需使用自然语言，直接影响大模型是否正确触发插件。
- **多轮对话**：
  - 若同时提供 `session_id` 和 `messages`，系统**优先使用 `messages`**；
  - `session_id` 由服务端生成并返回于响应 `output.session_id` 中，客户端需自行保存并在后续请求中复用。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


