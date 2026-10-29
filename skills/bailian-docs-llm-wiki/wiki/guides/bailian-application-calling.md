# bailian [application call](../api/application-call.md)ing

百炼应用调用是将已发布的智能体应用或工作流应用通过 API 集成至业务系统的标准方式，支持同步调用、多轮对话及插件参数透传。调用统一使用 `/api/v1/apps/{app_id}/completion` 接口，兼容 DashScope SDK 与原生 HTTP 请求，适用于各类语言环境。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Agent 1.0）**：基于 LLM 的单节点智能体，适用于简单问答、角色扮演等场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用（Flow Agent）**：支持多节点编排（大模型节点、插件节点、条件分支等），可实现复杂逻辑；注意其**仅支持华北2（北京）地域**，且**不支持文生图类大模型** [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮/多轮对话（支持 `session_id` 自动加载历史或显式传入 `messages` 数组）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件输入参数）；
  - 调试模式（`debug` 字段启用后返回中间节点执行详情）。

> **注意**：文档 3 中称“工作流应用不支持文生图大模型”，而文档 1 和 2 均未提及该限制；该限制为工作流应用特有，智能体应用无此约束，需按实际应用类型区分。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)页面获取 |
| `prompt` | string | 否（若提供 `messages` 则非必填） | 当前轮次用户输入文本；若使用 `messages` 模式则忽略此字段 |
| `messages` | array | 否（若提供则替代 `prompt`） | 格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，用于完全控制上下文 |
| `biz_params` | object | 否 | 扩展参数对象，关键子字段：<br> • `user_defined_params`: `{ "plugin_code": { "param_key": value } }`，用于向关联插件透传参数 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `session_id` | string | 否 | 用于云端自动加载历史对话（有效期 1 小时，最多 50 轮）；若同时传 `messages`，则以 `messages` 为准 |
| `parameters` | object | 否 | 空对象 `{}` 即可，暂无通用业务参数（模型级参数由节点内部配置） |
| `debug` | object | 否 | 设为 `{}` 可启用调试模式，返回各节点执行日志 |

## 使用方式

### 1. 前置准备
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 若使用 SDK，安装对应语言版本（Python ≥2.0.1，Java ≥2.12.0）；
- 确保应用已**发布**，且调用方与应用处于同一业务空间（插件关联前提）。

### 2. 调用示例（Python SDK）
```python
import os
import dashscope
from dashscope.v2 import DashScopeError

client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

# 基础调用（智能体/工作流均适用）
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# 带插件参数透传（仅限已关联插件的应用）
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

# 多轮对话（显式管理 messages）
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "我是千问。"},
    {"role": "user", "content": "今天天气如何？"}
]
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    messages=messages
)
```

### 3. HTTP 调用（curl）
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

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，跨地域请求将失败；
- **限流策略**（双维度独立生效）：
  - **单应用并发**：默认 100 QPS（每秒请求数），超限返回 `HTTP 429` + `Throttling.RateQuota`；
  - **账号总流量**：默认 15,000 QPM（每分钟请求数），涵盖该账号下所有应用；
  - 工作流[异步任务](../concepts/asynchronous-task.md)提交也占用单应用 QPS 配额 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)；
- **模型节点限流**：工作流中大模型类节点（如大模型节点、意图分类节点）还受所调用模型自身 RPM/TPM 配额约束，与应用限流正交；
- **插件参数要求**：自定义插件的输入参数必须在工具配置中设置为 **业务透传（Biz Pass-through）** 方式，否则无法通过 `biz_params` 传递；
- **错误处理**：捕获 `429` 时应采用指数退避重试（如 1s → 2s → 4s），避免持续触发限流；
- **安全建议**：生产环境禁止硬编码 API Key，务必通过环境变量或密钥管理服务注入。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)


