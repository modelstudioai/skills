# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至外部业务系统的开发能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心场景，适用于构建 AI 增强型业务系统。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心功能**：
  - 单轮文本生成（`prompt` 输入）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件专属参数），详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 调试信息返回（启用 `debug` 字段可获取执行路径、节点耗时等诊断数据）。

> **注意**：文档2明确声明“百炼工作流不支持使用文生图大模型”，而文档1和文档3均未提及此限制。实际调用时，请以文档2为准——工作流应用仅支持文本类大模型（如 `qwen-max`, `qwen-plus`），不可用于图像生成类任务。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台中应用卡片上复制的唯一 ID，需与调用地域一致（文档2强调工作流应用**仅支持华北2（北京）地域**） |
| `prompt` | string | 否（若提供 `messages` 则非必填） | 单轮指令文本；若启用多轮对话且使用 `messages` 方式，则不应同时传 `prompt` |
| `messages` | array | 否（推荐用于多轮） | 格式为 `[{"role": "user/system/assistant", "content": "..."}, ...]`，由客户端自行维护历史对话 |
| `session_id` | string | 否（云端存储方式） | 服务端自动加载并续写该会话的历史记录；有效期 1 小时，最多 50 轮 |
| `biz_params` | object | 否 | 用于插件参数透传，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }` |

> **注意**：当请求中同时包含 `session_id` 和 `messages` 时，系统**优先使用 `messages`**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 中“多轮对话”章节说明）。

## 使用方式

### 1. 前置准备
- 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）；
- 在百炼控制台创建对应类型的应用（智能体或工作流），获取 `app_id`；
- 若使用 SDK，按语言安装对应版本（Python ≥1.14.0，Java ≥2.12.0，见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 中的 SDK 版本要求）。

### 2. 调用示例（Python SDK）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    # 多轮对话（推荐）：
    # messages=[{"role": "user", "content": "你好"}],
    # 自定义插件参数：
    # biz_params={"user_defined_params": {"plugin_abc": {"query": "test"}}}
)

if response.status_code == 200:
    print(response.output.text)
else:
    print(f"error: {response.message}")
```

### 3. HTTP 直接调用（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
            "prompt": "你是谁？",
            "biz_params": {
                "user_defined_params": {
                    "your_plugin_code": {"article_index": 2}
                }
            }
        }
      }'
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 开头强调）；智能体应用无明确地域限制说明，但建议与应用部署地域保持一致。
- **会话管理**：
  - `session_id` 方式：自动过期（1 小时）、上限 50 轮，适合轻量级会话；
  - `messages` 方式：完全由客户端控制上下文长度与内容，更灵活且可控，**官方推荐**。
- **插件参数**：
  - `biz_params.user_defined_params` 仅在关联了自定义插件的智能体/工作流应用中生效；
  - 插件 ID（`plugin_code`）需从控制台插件卡片准确复制，不可拼写错误；
  - 插件输入参数必须在插件配置中设置为“业务透传”方式。
- **安全实践**：
  - 禁止硬编码 `API Key`，务必通过环境变量或密钥管理服务注入；
  - 生产环境应配置合理的超时与重试策略（SDK 默认已内置基础重试逻辑）。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


