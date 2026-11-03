# bailian [application call](../api/application-call.md)ing

阿里云百炼支持通过统一的 DashScope SDK 或标准 HTTP API 调用已发布的智能体应用（Agent 1.0）和工作流应用（Flow Agent），实现业务系统与 AI 能力的快速集成。调用方式统一、接口一致，开发者可按需选择同步/异步、单轮/多轮等模式，并支持插件参数透传与会话状态管理。

## 支持的模型/功能

- **应用类型**：当前支持调用两类应用：
  - [智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md)，适用于轻量级任务编排；
  - [工作流应用（Flow Agent）](raw/application-user-guide/llm-application/workflow-application.md)，支持复杂节点编排（大模型节点、插件节点、条件分支等）。
- **功能覆盖**：
  - 同步文本生成（`/completion` 端点）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组）；
  - 自定义插件参数透传（仅限关联了插件的智能体/工作流应用）；
  - 工作流异步任务提交（与同步调用共享单应用 QPS 配额）。
> **注意**：工作流应用不支持文生图类大模型节点，详见[调用工作流应用](raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)中获取。 |
| `prompt` | string | ✓（单轮） | 用户输入的自然语言指令；若使用 `messages` 进行多轮对话，则此项可省略。 |
| `messages` | array | ✗（推荐用于多轮） | 替代 `prompt` 的结构化消息数组，格式同 OpenAI，含 `role`（`user`/`assistant`/`system`）与 `content`。优先级高于 `session_id`。 |
| `session_id` | string | ✗（可选） | 用于启用云端会话历史加载，有效期 1 小时，最多 50 轮。 |
| `biz_params` | object | ✗（插件场景必需） | 传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见[应用的自定义参数传递](raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。 |
| `debug` | object | ✗ | 调试开关，设为空对象 `{}` 即可启用调试信息返回。 |

## 使用方式

### 前置准备
1. 获取并配置 API Key：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，**强烈建议通过环境变量 `DASHSCOPE_API_KEY` 设置**，避免硬编码；
2. 安装 SDK（可选）：如使用 Python，执行 `pip install -U dashscope`；Java/Node.js/C#/PHP/Go 等语言请参考对应 SDK 文档；
3. 确认应用已发布且状态为“运行中”。

### 调用示例（Python SDK）
```python
import os
import dashscope
from dashscope.v2 import DashScopeError

client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

# 单轮调用
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
print(response.text)

# 多轮调用（显式 messages）
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "我是千问。"},
    {"role": "user", "content": "今天天气如何？"}
]
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    messages=messages
)

# 插件参数透传
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    }
}
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    prompt="查询寝室公约",
    biz_params=biz_params
)
```

### HTTP 直连（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
      "prompt": "你是谁？",
      "biz_params": {
        "user_defined_params": {
          "your_plugin_code": {"article_index": 2}
        }
      }
    },
    "parameters": {},
    "debug": {}
  }'
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制（[调用工作流应用](raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）；
- **限流策略**（[应用限流](raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)）：
  - 单应用并发：100 QPS（每秒请求数）；
  - 账号总流量：15,000 QPM（每分钟请求数，含所有应用）；
  - 工作流异步任务提交与同步调用**共享单应用 QPS 配额**；
  - 模型节点还受所调用底层模型自身 RPM/TPM 限制，二者独立触发；
- **错误处理**：
  - 限流返回 HTTP 429 + 错误码 `Throttling.RateQuota`，建议采用指数退避重试；
  - SDK 抛出 `DashScopeError`（Python）或 `ApiException`（Java）等异常，可通过 `request_id` 追踪；
- **安全提示**：
  - 切勿在代码中硬编码 `DASHSCOPE_API_KEY`，必须通过环境变量或密钥管理服务注入；
  - 插件鉴权配置（如 Basic Auth）需在插件创建时明确设置，API 调用不透传鉴权凭据。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)


