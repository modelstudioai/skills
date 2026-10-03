# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台构建的智能体应用（Agent 1.0）或工作流应用集成至业务系统的标准方式，统一通过 DashScope SDK 或 HTTP API 实现。所有调用均基于 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion` 端点，支持单轮/多轮对话及自定义参数透传，适用于生产环境快速接入。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（原“智能体编排应用”的演进形态），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）；
  - 自定义插件参数透传（`biz_params.user_defined_params`），用于驱动插件节点执行，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 调试信息返回（`debug` 字段可选启用）；
- **不支持能力**：工作流应用明确不支持文生图类大模型（如 `wanx` 系列），该限制在 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 中强调。

> **注意**：文档 1 和文档 2 的代码示例完全一致（包括 Python/Java/curl 等全部语言片段），但文档 2 额外声明“仅适用于华北2（北京）地域”，而文档 1 未提及地域限制。实际调用前请确认应用部署地域与 API Endpoint 匹配，避免因地域不一致导致 `403 Forbidden` 或 `404 Not Found` 错误。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上获取的唯一 ID，非模型 ID |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 当前轮次用户输入文本；若使用 `messages` 数组则无需此字段 |
| `messages` | array | 否（推荐用于多轮） | 格式为 `[{"role": "user/system/assistant", "content": "..."}]`，由客户端维护完整对话历史 |
| `session_id` | string | 否（云端存储模式） | 由服务端生成并返回，有效期 1 小时，最多支持 50 轮；若同时传 `messages`，系统优先使用 `messages` |
| `biz_params` | object | 否 | 用于插件参数透传，结构为 `{"user_defined_params": {"{plugin_code}": {"param_key": "value"}}}` |
| `parameters` | object | 否 | 应用级运行参数（如 `temperature`, `max_output_tokens`），需在应用配置中已声明 |
| `debug` | object | 否 | 开启后返回详细执行链路信息（如节点耗时、插件调用日志），仅调试用 |

> **注意**：`biz_params` 仅在智能体应用和工作流应用中生效，且必须在应用内完成插件关联与发布后才可被识别。其使用方式在 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中有完整示例。

## 使用方式

### 1. 前置准备
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并配置，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用卡片上的 ID；
- （SDK 方式）安装对应 SDK：Python（`pip install -U dashscope`）、Java（Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java`）、Node.js（`npm install axios`）等，版本要求见各文档示例注释（如 Java SDK ≥ 2.12.0）。

### 2. 调用方式（任选其一）
- **DashScope SDK（推荐）**：封装了认证、重试、错误处理，代码简洁。例如 Python：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.output.text)
  ```
- **HTTP API（通用）**：兼容任意语言，直接 POST 至 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`，需携带 `Authorization: Bearer ${API_KEY}` 头。示例 curl：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"input": {"prompt": "你是谁？"}}'
  ```

### 3. 多轮对话实现
- **云端存储模式**：首次调用不传 `session_id`，服务端返回 `response.output.session_id`；后续请求复用该值即可自动加载历史；
- **客户端管理模式（推荐）**：构造 `messages` 数组并随每次请求发送，例如：
  ```python
  messages = [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "你好！有什么可以帮您？"},
      {"role": "user", "content": "今天天气如何？"}
  ]
  response = Application.call(app_id="...", messages=messages)
  ```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无明确地域限制，但建议保持应用与调用方地域一致以降低延迟；
- **会话限制**：`session_id` 有效期为 1 小时，单个会话最多支持 50 轮对话；超出后需新建会话；
- **插件参数安全**：`biz_params.user_defined_params` 中的插件 ID 和参数名必须与控制台配置完全一致（含大小写），否则插件不会被触发；
- **错误处理**：所有调用均返回 `request_id`，用于问题排查；错误码含义参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
- **生产安全**：严禁硬编码 `api_key`，必须通过环境变量或密钥管理服务注入；
- **模型绑定**：应用调用不指定底层模型，模型由应用创建时选定并固化，调用时不可动态切换。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


