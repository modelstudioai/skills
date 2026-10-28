# bailian [application call](../api/application-call.md)ing

百炼平台支持通过统一 API 接口调用智能体应用（Agent 1.0）和工作流应用（Flow Agent），开发者可使用 DashScope SDK 或原生 HTTP 请求完成集成。调用过程需提供 `app_id`、`prompt` 及可选的业务参数，底层自动路由至对应应用逻辑并返回结构化响应。所有调用均受统一限流策略约束，需提前规划并发与流量配额。

## 支持的模型/功能

- **智能体应用（Agent 1.0）**：支持单轮问答、多轮对话（通过 `session_id` 或显式 `messages`）、插件调用（需配置自定义插件并透传参数）；[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 文档提供了完整示例。
- **工作流应用（Flow Agent）**：支持复杂编排逻辑（含条件分支、循环、多节点协同），但**不支持文生图类大模型节点**；其调用方式与智能体应用一致，详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **插件能力**：仅在智能体应用或工作流应用中关联的插件节点可被调用，参数需通过 `biz_params.user_defined_params` 透传，且插件工具的输入参数必须配置为“业务透传”；具体实现参见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：文档 3 明确声明“工作流不支持使用文生图大模型”，而文档 2 和文档 3 的调用示例完全一致（均使用 `/apps/{app_id}/completion` 端点），表明二者在 API 层无本质差异，仅后端执行逻辑不同。但文档 1 中提到“智能体编排应用已被工作流应用替代”，说明旧版智能体编排已下线，当前仅维护智能体应用（Agent 1.0）与工作流应用两类。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在控制台「应用管理」页面获取。 |
| `prompt` | string | 是（若未提供 `messages`） | 用户输入的原始指令文本，用于单轮调用或作为多轮对话的最新消息。 |
| `messages` | array | 否（推荐用于多轮） | 消息历史数组，格式为 `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`；若同时传 `prompt` 和 `messages`，系统将忽略 `prompt`。 |
| `session_id` | string | 否（可选） | 用于启用云端会话状态管理，有效期 1 小时，最多 50 轮；若同时传 `session_id` 和 `messages`，系统优先使用 `messages`。 |
| `biz_params` | object | 否 | 业务扩展参数对象，核心字段为 `user_defined_params`，用于向关联插件透传参数（如 `{"user_defined_params": {"plugin_code": {"param_key": "value"}}}`）。 |

## 使用方式

### 1. 前置准备
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 安装对应语言的 DashScope SDK（Python/Java/Node.js 等），或直接使用 HTTP 调用；
- 确保应用已发布，且插件（如需）已在相同业务空间内正确关联。

### 2. 调用示例（通用）
所有应用类型均使用同一 API 端点：  
`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`

- **SDK 调用（Python）**
  ```python
  import os
  import dashscope
  client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
  response = client.apps.completions.create(
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.text)
  ```

- **HTTP 调用（curl）**
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json" \
    --data '{
      "input": {"prompt": "你是谁？"},
      "parameters": {},
      "debug": {}
    }'
  ```

- **插件参数透传（需在 `biz_params` 中指定）**
  ```python
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

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无此限制；[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 文档明确标注了该约束。
- **限流规则**：
  - 单应用并发：100 QPS（按 `app_id` 统计）；
  - 账号总流量：15,000 QPM（全账号下所有应用请求总和）；
  - 工作流异步任务提交与同步调用共享单应用 QPS 配额；
  - 大模型类节点（如大模型节点、意图分类节点）还受所调用模型自身 RPM/TPM 限制，与应用限流独立生效。
- **错误处理**：触发限流时返回 HTTP 429 + 错误码 `Throttling.RateQuota`，建议实现指数退避重试，并提前申请扩容；详情见 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)。
- **安全实践**：禁止硬编码 API Key，务必通过环境变量或密钥管理服务注入。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)


