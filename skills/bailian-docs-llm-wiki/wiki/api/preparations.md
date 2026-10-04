# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、环境准备及参数校验等基础工作。这些步骤直接影响调用的安全性、兼容性与稳定性。本文汇总关键准备事项，聚焦可执行操作与常见陷阱，不涉及业务逻辑设计或模型选型建议。

## 支持的模型/功能

- **模型调用方式**：支持通过 DashScope SDK（Python/Java）或 OpenAI 兼容 SDK（Python/Node.js/Java/Go）调用。OpenAI SDK 适用于所有[OpenAI 兼容接口](raw/model-api-reference/toolkits-and-frameworks.md)，但部分高级能力（如 SDK Expert、细粒度诊断）仅 DashScope Python SDK（≥1.27.3）提供。
- **功能覆盖**：DashScope SDK Expert 内置能力覆盖文本生成、多模态、语音、向量检索、Rerank、微调与部署、Agent 等全能力域，可通过 `/skill` 命令按需启用（如 `api-doc` 查文档、`sdk-example` 生成代码、`diagnose` 排查问题）[DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。
- **实时语音与多模态**：若需通过 AOQ 调用 Realtime API（如实时语音合成/识别），必须使用 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，标准 DashScope 或 OpenAI SDK 不支持。

> **注意**：文档 2 提到“OpenAI Java SDK 推荐设置为 `3.5.0`”，但文档 4 的错误码示例中明确要求 `response_format` 必须为 `{"type": "json_object"}` —— 此格式在 OpenAI Java SDK 3.5.0 中尚未原生支持（需手动构造 JSON 字符串）。建议优先使用 DashScope SDK 或升级至 OpenAI Java SDK ≥4.0.0。

## 关键参数

- **API Key 与 Base URL**：API Key 按地域隔离，不可跨地域混用；Base URL 需匹配地域（如华北2为 `https://dashscope.aliyuncs.com/compatible-mode/v1`），详见 [各地域接入信息](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **模型名称**：必须使用百炼控制台模型市场中的**官方模型 ID**（如 `qwen3-8b`、`qwen3-235b-a22b-instruct-2507`），不可混用 Hugging Face 格式（如 `Qwen/Qwen3-8B`）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **流式与思考模式**：
  - 启用 `enable_thinking` 时，必须同时设置 `stream=true`、`incremental_output=true`、`result_format="message"`；
  - 结构化输出（`response_format={"type": "json_object"}`）与思考模式互斥，需关闭 `enable_thinking`；
  - 部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `enable_thinking=true`，不可设为 `false`。
- **输入格式**：
  - 纯文本模型（如 `qwen3-max`）的 `content` 必须为字符串，**禁止传入数组**（如 `[{ "type": "text", "text": "..." }]`）；
  - 多模态模型（如 `qwen3-vl`）的 `content` 可为对象数组，但 `type` 仅限 `text`/`image_url`/`video_url` 等显式支持类型，禁止混入数字、布尔值或非法 `type`。

## 使用方式

- **API Key 配置**：
  - **推荐方式**：配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS 用 `export`，Windows 用系统属性或 `setx`），避免硬编码；
  - **安全限制**：**严禁在客户端（浏览器、移动 App）或不可信环境使用长期 API Key**；高风险场景应使用 [临时 API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（最长 1800 秒）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **SDK 安装**：
  - Python：`pip install -U dashscope`（含 SDK Expert）或 `pip install -U openai`；
  - Java/Node.js/Go：按文档 2 的 Gradle/Maven/npm/go get 命令安装对应 SDK。
- **快速验证**：
  - 安装 DashScope SDK ≥1.27.3 后，直接运行 `dashscope` 进入交互式 CLI，用自然语言描述需求（如“用 qwen-plus [流式输出](../concepts/streaming-output.md)并统计 token”）即可生成并执行可运行代码；
  - 报错时，直接粘贴错误码（如 `Throttling.RateQuota`）或文件路径（如 `/skill diagnose gen.py`）触发自动诊断 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 限制和注意事项

- **API Key 限制**：单账号+单地域最多 50 个 API Key；自定义权限下最多勾选 30 个模型；IP 白名单最多 20 个地址/网段（IPv6 仅华北2支持）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **地域与业务空间绑定**：API Key 的调用权限由其**归属业务空间**决定，同一空间内所有 API Key 权限一致；调优后的模型仅能被其所在业务空间的 API Key 调用。
- **常见错误规避**：
  - `Model not exist`：检查模型名大小写、空格及是否已在[模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market)开通；
  - `InvalidParameter`：严格校验参数范围（如 `temperature ∈ [0.0, 2.0)`、`top_p ∈ (0.0, 1.0]`、`max_tokens ∈ [1, xxx]`），参考 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档；
  - `Required body invalid`：使用 JSON 校验工具（如 jsonlint.com）确认请求体语法合法，尤其注意引号闭合与逗号位置。
- **调试必备**：调用失败时务必记录 `request_id`（响应 Header 或 Body 中），用于查询[模型监控日志](../../raw/model-user-guide/model-monitoring/model-telemetry.md)或提交工单。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


