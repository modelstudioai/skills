# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至第三方业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传及调试能力，是生产环境集成的核心方式。所有调用均需有效 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组维护上下文）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 向关联插件传递业务参数），详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 调试信息返回（启用 `debug` 字段可获取中间节点执行详情）。

> **注意**：文档2明确说明“百炼工作流不支持使用文生图大模型”，而文档1和文档3均未提及此限制；实际调用时若涉及图像生成类节点，须确认工作流应用中未配置文生图模型，否则请求将失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上复制的唯一标识符（非模型 ID） |
| `prompt` | string | 否（与 `messages` 互斥） | 单轮指令文本；若使用 `messages` 则不可传此字段 |
| `messages` | array | 否（与 `prompt` 互斥） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于显式管理多轮上下文 |
| `session_id` | string | 否 | 由服务端生成并返回的会话标识，用于自动加载云端历史（有效期 1 小时，最多 50 轮）；若同时传 `messages`，则优先使用 `messages` |
| `biz_params` | object | 否 | 用于插件参数透传，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": "<value>" } } }` |
| `debug` | object | 否 | 空对象 `{}` 即可启用，返回各节点输入/输出、耗时等调试信息 |

## 使用方式

### 1. 前置准备
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并配置，推荐[配置到环境变量 `DASHSCOPE_API_KEY`](../../raw/model-api-reference/preparations/get-api-key.md)；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用卡片上的 ID；
- （SDK 方式）安装对应语言 SDK：Python、Java、Node.js、C#、Go、PHP 均提供示例，版本要求见各文档（如 Java SDK 建议 ≥ 2.12.0）。

### 2. 调用示例（Python SDK）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 自动读取环境变量
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    # biz_params={"user_defined_params": {"plugin_abc": {"query": "2024年报"}}}  # 插件调用时启用
)

if response.status_code == 200:
    print(response.output.text)
else:
    print(f"error {response.status_code}: {response.message}")
```

### 3. HTTP 直连（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "你是谁？"
        }
      }'
```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无此限制（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）；
- **多轮对话上限**：`session_id` 会话有效期为 1 小时，且最多承载 50 轮交互；超出后需新建会话；
- **插件参数安全**：`biz_params.user_defined_params` 中的插件 ID 和参数名必须与控制台配置完全一致（含大小写），否则参数不会被识别；
- **错误处理**：所有调用均返回 `request_id`，用于问题排查；错误码含义请参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
- **鉴权兼容性**：自定义插件若开启鉴权（如 Basic Auth），其凭证由百炼平台在调用插件时自动注入，开发者无需在 `biz_params` 中重复传递；
- **SDK 版本兼容性**：文档1和文档2均要求 Java SDK ≥ 2.12.0，但文档3示例中 Python SDK 要求 ≥ 1.14.0 —— 实际应以 [DashScope SDK 官方发布页](https://github.com/alibaba-dashscope/dashscope-python/releases) 的最新稳定版为准，旧版可能缺失 `biz_params` 支持。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


