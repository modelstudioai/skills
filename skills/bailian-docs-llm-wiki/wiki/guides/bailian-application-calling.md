# bailian [application call](../api/application-call.md)ing

百炼应用调用是将已发布的智能体应用或工作流应用通过标准 API 集成至业务系统的统一方式，支持同步调用、多轮对话及插件参数透传。调用基于 DashScope SDK 或 HTTP 接口，需配置有效的 API Key 和应用 ID，适用于各类开发者场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Agent 1.0）**：面向单任务、轻量级交互场景，适用于快速构建问答、[工具调用](../concepts/tool-calling.md)类服务 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用（Flow Agent）**：面向复杂编排场景，支持节点化流程（如大模型节点、插件节点、条件分支等），但**不支持文生图类大模型** [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮/多轮对话（支持 `session_id` 云端历史管理或手动维护 `messages` 数组）；
  - 自定义插件参数透传（仅限工作流应用中的插件节点，或关联了插件的智能体应用）；
  - 调试模式（通过 `debug` 字段启用）；
  - [异步任务](../concepts/asynchronous-task.md)提交（工作流应用支持，与同步调用共享单应用 QPS 配额）。

> **注意**：文档 1 中称“智能体编排应用已被工作流应用替代”，但文档 2 和文档 3 并列描述两类应用且均提供完整调用示例，说明当前平台**同时维护智能体应用（Agent 1.0）和工作流应用两个并行产品形态**，开发者应根据实际需求选择，而非强制迁移。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)页面获取 |
| `prompt` | string | 是（若未传 `messages`） | 当前轮次用户输入文本；若使用 `messages` 数组则此项可省略 |
| `messages` | array | 否（推荐用于多轮） | 完整对话历史数组，格式同 OpenAI `messages`，优先级高于 `session_id` 和 `prompt` |
| `session_id` | string | 否 | 用于加载云端存储的对话上下文，有效期 1 小时，最多 50 轮 |
| `biz_params` | object | 否 | 业务扩展参数，关键子字段：<br> • `user_defined_params`: 用于传递自定义插件参数，结构为 `{ "plugin_code": { "param_key": value } }` [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `parameters` | object | 否 | 模型级参数（如 `temperature`, `top_p`），按所用大模型实际支持项填写 |
| `debug` | object | 否 | 开启调试模式，返回中间节点执行详情 |

## 使用方式

### 1. 前置准备
- 获取并配置 API Key：[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- 创建并发布目标应用（智能体或工作流），记录其 `app_id`；
- （可选）安装 DashScope SDK：Python、Java、Node.js 等主流语言均支持，版本建议 ≥2.12.0（Java）或 ≥2.0.1（Python）。

### 2. 同步调用示例（Python）
```python
import os
import dashscope
from dashscope.v2 import DashScopeError

client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

# 基础调用
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# 带插件参数的调用（智能体或工作流应用）
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}
    }
}
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    prompt="查询寝室公约第二条",
    biz_params=biz_params
)
```

### 3. 多轮对话（推荐手动维护 `messages`）
```python
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！我是千问。"},
    {"role": "user", "content": "今天天气如何？"}
]
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    messages=messages  # 不传 prompt
)
```

### 4. HTTP 直接调用（curl）
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

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)；
- **限流策略**（双维度独立生效）：
  - **单应用并发**：默认 100 QPS（每秒请求数），超限返回 HTTP 429 + `Throttling.RateQuota`；
  - **账号总流量**：默认 15,000 QPM（每分钟请求数），涵盖该主账号下所有应用；
  - 工作流[异步任务](../concepts/asynchronous-task.md)提交请求与同步调用**共享单应用 QPS 配额**；
  - 工作流中大模型类节点还受**所调用模型自身 RPM/TPM 限流约束**，该约束与应用限流正交 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)；
- **安全实践**：
  - 禁止在代码中硬编码 `DASHSCOPE_API_KEY`，务必通过环境变量配置；
  - 插件鉴权配置（如 Basic Auth）需在插件创建时显式开启并正确设置 Header；
- **插件参数要求**：
  - 输入参数的**传参方式必须设为“业务透传”**；
  - 插件描述与工具描述需使用自然语言，直接影响大模型对插件意图的理解准确性；
- **错误处理**：
  - 遇 `429` 错误应实施指数退避重试（如 1s → 2s → 4s），避免持续触发；
  - 完整错误码参考 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)


