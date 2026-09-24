# bailian [application call](../api/application-call.md)ing

阿里云百炼平台支持通过统一的 DashScope SDK 或标准 HTTP API 调用已发布的智能体应用（Agent 1.0）和工作流应用，实现低代码集成。调用过程抽象为 `Application.call()`（SDK）或 `/api/v1/apps/{app_id}/completion`（HTTP），核心输入为 `prompt` 和可选上下文参数，输出为结构化响应文本及用量信息。所有调用均需有效 API Key 和应用 ID。

## 支持的模型/功能

- **应用类型**：当前支持两类应用调用：
  - **智能体应用（Agent 1.0）**：基于单一大模型（如 `qwen-max`、`qwen-plus`）构建的对话式应用，适用于问答、内容生成等场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用**：支持多节点编排（大模型节点、插件节点、条件分支等），但**不支持文生图类大模型**，且目前仅限华北2（北京）地域使用 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **扩展能力**：
  - 自定义插件参数透传：通过 `biz_params.user_defined_params.{plugin_code}` 向关联插件传递业务参数（如 `article_index: 2`），适用于寝室公约查询等场景 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 多轮对话支持：可通过 `session_id`（云端自动维护，有效期 1 小时，最多 50 轮）或显式传入 `messages` 数组（推荐，完全可控）实现上下文延续。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上获取的唯一标识符，区分智能体与工作流应用 |
| `prompt` | string | 是（若未传 `messages`） | 当前轮次的用户指令，纯文本输入；若启用 `messages` 模式则此项忽略 |
| `messages` | array | 否（推荐用于多轮） | 格式为 `[{"role": "user/system/assistant", "content": "..."}]`，完整覆盖对话历史与当前请求 |
| `session_id` | string | 否（单轮可省略） | 用于恢复云端存储的会话状态；若与 `messages` 同时存在，**优先使用 `messages`** |
| `biz_params` | object | 否 | 高级参数对象，用于插件透传：<br>– `user_defined_params.{plugin_code}`：键为插件 ID，值为该插件所需 JSON 参数对象（如 `{"article_index": 3}`） |

> **注意**：文档 1 和文档 3 均未明确说明 `biz_params` 在工作流应用中的兼容性，但文档 2 明确指出其适用于“智能体应用和工作流应用”。实践中，工作流应用调用插件节点时同样依赖 `biz_params.user_defined_params`，因此该参数对两类应用均有效。

## 使用方式

### 前置准备
1. 获取并配置 API Key：前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，**强烈建议通过环境变量 `DASHSCOPE_API_KEY` 注入**，避免硬编码 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
2. 获取 `app_id`：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面复制目标应用卡片上的 ID；
3. （可选）安装 SDK：Python、Java、Node.js 等语言需安装对应 DashScope SDK（如 Python 执行 `pip install -U dashscope`）。

### 调用示例（SDK - Python）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？",
    # 多轮对话（推荐）：传入 messages 替代 prompt
    # messages=[{"role": "user", "content": "你好"}, {"role": "assistant", "content": "我是千问"}],
    # 插件参数透传
    # biz_params={"user_defined_params": {"your_plugin_code": {"article_index": 2}}}
)

if response.status_code == 200:
    print(response.output.text)
else:
    print(f"Error {response.status_code}: {response.message}")
```

### HTTP 调用（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "你是谁？"
          // "messages": [...], // 替代 prompt
          // "biz_params": {"user_defined_params": {"your_plugin_code": {"article_index": 2}}}
        },
        "parameters": {},
        "debug": {}
      }'
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)；
- **安全实践**：API Key **严禁硬编码**于源码中，必须通过环境变量或密钥管理服务注入；
- **版本兼容性**：
  - Java SDK 建议 ≥ 2.12.0（文档 1 & 3），Python SDK 无显式最低版本要求，但插件透传功能需 ≥ 1.14.0（文档 2）；
- **参数冲突**：当请求同时包含 `session_id` 和 `messages` 时，系统**强制优先使用 `messages`**，`session_id` 将被忽略；
- **插件鉴权**：若插件配置了鉴权（如 Basic Auth），调用方无需额外处理，百炼平台会在转发请求时自动注入鉴权头；
- **错误处理**：所有调用均返回标准 HTTP 状态码及 `request_id`，错误详情请参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


