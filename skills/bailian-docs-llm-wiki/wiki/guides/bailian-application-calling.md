# bailian [[application-call|application call]]ing

本文介绍如何通过 DashScope SDK 或 HTTP API 集成阿里云百炼平台的应用，实现[[智能体应用]]与[[工作流应用]]的程序化调用。开发者可通过标准请求接口快速接入对话服务，并结合云端会话管理、业务参数透传及自定义插件扩展业务场景。

## 支持的应用类型与功能
百炼平台应用调用接口统一基于 DashScope API 规范，主要覆盖以下场景：
- **单轮/多轮对话**：支持传入当前提示词（`[[prompt|prompt]]`）或完整历史消息数组（`messages`），适用于问答、内容生成等场景。
- **自定义插件调用**：支持通过业务透传参数动态注入[[自定义插件]]所需的运行时变量，实现外部系统数据与 AI 流程的无缝对接。
- **工作流节点控制**：工作流应用中的插件节点、代码节点等均可通过标准化参数结构接收调用指令。

> **注意**：早期的“智能体编排应用”架构已被[[工作流应用]]全面替代，旧版接口与概念已逐步下线，新建项目请直接采用工作流模式。详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 关键参数
调用接口请求体（JSON）核心字段如下：

| 参数路径 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 百炼控制台分配的应用唯一标识。 |
| `input.[[prompt|prompt]]` | string | 否* | 当前用户输入。若使用自行管理的 `messages` 数组，可留空或省略。 |
| `input.messages` | array | 否 | 对话历史数组，格式为 `[{"role":"user","content":"..."}, {"role":"assistant","content":"..."}]`。推荐用于灵活控制上下文。 |
| `input.session_id` | string | 否 | 云端会话 ID，用于自动拉取服务端缓存的历史对话。 |
| `input.biz_params` | object | 否 | 业务透传参数，主要用于向关联插件传递键值对。结构见下方。 |

**插件参数透传结构 (`biz_params.user_defined_params`)**：
```json
{
  "user_defined_params": {
    "<your_plugin_code>": {
      "<param_key_1>": <value_1>,
      "<param_key_2>": <value_2>
    }
  }
}
```

> **注意**：若请求中同时包含 `session_id` 与 `messages`，服务端将**优先解析 `messages`**，忽略云端会话缓存。需根据业务场景明确选择其中一种多轮维护策略。

## 调用方式
支持主流语言 SDK（Python, Java, Go 等）与原生 HTTP RESTful 接口。

### 1. 环境准备
1. 获取[[API Key]]，建议配置至环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。
2. 安装 [[dashscope-sdk]]。非 SDK 调用可直接跳过此步。
完整前置步骤与依赖配置参考 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。

### 2. 核心代码示例（多语言）
调用入口统一为 `Application` 类或 `POST /api/v1/apps/{APP_ID}/completion` 端点。
- **Python (SDK)**: `Application.call(api_key=..., app_id=..., [[prompt|prompt]]=...)`
- **Java (SDK)**: `ApplicationParam.builder().appId(...).prompt(...).build()`
- **HTTP (cURL)**: 携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 头发起 POST 请求。

### 3. 多轮对话与插件透传实现
- **多轮对话**：首次调用记录返回的 `session_id`（有效期 1 小时，上限 50 轮）并在后续请求中复用；或业务侧自行维护 `messages` 列表逐轮追加。
- **插件透传**：在应用关联插件并配置输入参数为“业务透传”后，通过 `biz_params` 注入实际值。具体实现逻辑与完整代码示例参见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

## 限制与注意事项
- **地域限制**：当前接口与 SDK 默认仅支持**中国大陆版（北京地域）**，海外 Region 暂未开放调用。
- **速率与配额**：Token 消耗统计位于响应体 `usage.models` 中。频繁调用需关注账户配额，建议在生产环境增加指数退避重试机制。
- **响应处理**：成功响应状态码为 `200`（HTTPStatus.OK）。解析结果优先读取 `output.text`。异常时需依据 `request_id` 与 `code` 排查错误码文档。
- **插件兼容性**：只有插件创建时将输入参数的传参方式配置为**业务透传**，`biz_params` 中的键值对才会被正确路由至插件内部。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)

