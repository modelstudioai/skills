# bailian [application call](../api/application-call.md)ing

百炼平台支持通过统一 API 接口调用智能体应用（Agent 1.0）和工作流应用（Flow Agent），开发者可使用 DashScope SDK 或原生 HTTP 请求完成集成。所有调用均基于 `POST /api/v1/apps/{app_id}/completion` 端点，核心逻辑围绕 `prompt` 输入与 `biz_params` 扩展参数展开，适用于对话生成、插件编排、多轮会话等场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Agent 1.0）**：面向单任务轻量交互，适用于问答、工具调用等简单场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用（Flow Agent）**：支持节点化编排（大模型节点、插件节点、条件分支等），适用于复杂业务流程；注意其**仅支持华北2（北京）地域**，且**不支持文生图类大模型** [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮/多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）；
  - 自定义插件参数透传（需在插件配置中将输入参数设为“业务透传”）；
  - 调试信息返回（通过 `debug` 字段启用）；
  - 模型用量统计（`usage.models` 中返回各节点实际调用的 `model_id`、`input_tokens` 和 `output_tokens`）。

> **注意**：文档 3 明确声明“工作流不支持使用文生图大模型”，而文档 1 和 2 均未提及该限制；实际集成时若涉及多模态生成节点，须确认所选模型是否在[模型限流文档](../../raw/model-user-guide/get-started-with-models/rate-limit.md)支持列表中，否则将触发模型维度限流而非应用维度限流。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，从控制台「应用管理」页面获取 |
| `prompt` | string | ✓（若未提供 `messages`） | 当前轮次用户输入文本；若使用 `messages` 则此项忽略 |
| `messages` | array | ✗（推荐用于多轮） | 格式同 OpenAI `messages`，含 `role`（`user`/`assistant`）和 `content`，由客户端自行维护历史 |
| `session_id` | string | ✗（云端存储模式） | 服务端自动加载并维护该 ID 对应的对话历史，有效期 1 小时，最多 50 轮；**若同时传 `session_id` 和 `messages`，系统优先使用 `messages`** |
| `biz_params` | object | ✗ | 扩展参数对象，用于传递插件参数等业务上下文：<br>• `user_defined_params`: `{ "plugin_code": { "param_key": "param_value" } }`，对应[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；<br>• 其他字段（如 `trace_id`）暂无公开语义，建议避免自定义非标准键 |
| `parameters` | object | ✗ | 预留字段，当前版本为空对象 `{}` 即可 |
| `debug` | object | ✗ | 启用调试模式时设为 `{}`，返回更详细的执行链路信息 |

## 使用方式

### 1. 前置准备
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐通过环境变量 `DASHSCOPE_API_KEY` 注入；
- 若使用 SDK，安装对应语言版本（Python ≥2.0.1，Java ≥2.12.0）；
- 确认应用已发布，且调用方与应用处于同一业务空间（插件关联要求）。

### 2. 调用示例（以 Python SDK 为例）
```python
import os
import dashscope
from dashscope.v2 import DashScopeError

client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

# 基础调用（单轮）
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# 多轮调用（显式 messages）
response = client.apps.completions.create(
    app_id="YOUR_APP_ID",
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "我是千问。"},
        {"role": "user", "content": "今天天气如何？"}
    ]
)

# 带插件参数调用
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

### 3. HTTP 等效请求
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

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，跨地域请求将失败；
- **限流策略**（双维度独立生效）：
  - **单应用并发**：默认 100 QPS（每秒请求数），按 `app_id` 统计；
  - **账号总流量**：默认 15,000 QPM（每分钟请求数），按阿里云主账号汇总全部应用调用；
  - 工作流[异步任务](../concepts/asynchronous-task.md)提交请求与同步调用**共享单应用 QPS 配额**；
  - 模型节点（如大模型、意图分类）还受所调用模型自身 RPM/TPM 限制，与应用限流正交 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)；
- **错误处理**：
  - 触发限流时返回 HTTP 429 + 错误码 `Throttling.RateQuota`，SDK 抛出对应异常；
  - 建议实现指数退避重试（如 1s→2s→4s），并设置最大重试次数；
- **安全实践**：
  - 禁止硬编码 API Key，必须通过环境变量或密钥管理服务注入；
  - 插件鉴权配置（如 Basic Auth）需在插件创建时明确开启，`biz_params` 不参与鉴权流程；
- **兼容性说明**：
  - 智能体编排应用已被工作流应用替代，旧应用迁移后需更新 `app_id`；
  - 文档 1 中 Java 示例依赖 `com.alibaba.dashscope.app.*`，但文档 2 和 3 均注明 SDK 版本 ≥2.12.0，低版本可能缺少 `ApplicationParam.builder()` 等新接口。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)


