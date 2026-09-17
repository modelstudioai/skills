# preparations

在调用阿里云百炼平台模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、环境准备等基础步骤。这些操作是所有模型调用（文本生成、图像/视频/语音处理、向量检索等）的共同前置条件，直接影响调用成功率与安全性。本文汇总关键实践要点，聚焦可执行、可验证的操作项。

## 支持的模型/功能

百炼平台支持通过 DashScope SDK 或 OpenAI 兼容 SDK 调用全栈模型能力，包括：
- **文本生成**：Qwen 系列（如 `qwen3-8b`、`qwen-plus`）、DeepSeek-R1 等；
- **[多模态](../concepts/multi-modal.md)**：Qwen-VL、Qwen3-VL、文生图（WanImage）、图生视频（WanVideo）；
- **语音**：CosyVoice 语音合成、Paraformer 实时语音识别；
- **向量与排序**：通用文本向量化、Rerank 模型；
- **工具调用与结构化输出**：支持 `tool_calls`、`response_format={"type": "json_object"}` 等高级能力。

> **注意**：部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `enable_thinking=true`，而思考模式模型不支持 `response_format="json_object"`，需关闭思考模式才能启用结构化输出 —— 具体约束详见 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档中对应条目。

## 关键参数

调用必需的核心参数如下（均需在请求或 SDK 初始化时显式指定）：

| 参数 | 说明 | 示例值 | 来源依据 |
|------|------|--------|----------|
| `model` | 模型 ID，**严格区分大小写与空格**，不可混用开源社区命名（如 `Qwen/Qwen3-235B...`） | `"qwen-plus"`、`"qwen3-235b-a22b-instruct-2507"` | [错误码](../../raw/model-api-reference/preparations/error-code.md) 中 “Model not exist” 条目明确要求核对模型市场名称 |
| `DASHSCOPE_API_KEY` | 用于身份认证的密钥，**必须配置为环境变量或代码内显式赋值** | `"sk-xxxxxxxx"` | [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 文档强调其为调用前提 |
| `base_url` | 地域专属接入地址，**不同地域不可混用**；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)使用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，DashScope 原生接口使用 `https://{workspace-id}.{region}.maas.aliyuncs.com/api/v1` | 华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1` | [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档要求显式配置 `DASHSCOPE_HTTP_BASE_URL` |

其他高频校验参数（见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）：
- `stream`：流式模型（如思考模式、语音合成）**必须设为 `true`**；
- `incremental_output`：开启 `enable_thinking` 时**必须为 `true`**；
- `result_format`：思考模式模型**必须为 `"message"`**；
- `messages`：纯文本模型禁止含 `image_url` 等[多模态](../concepts/multi-modal.md)元素，否则触发 `InvalidParameter`。

## 使用方式

### 1. SDK 安装
- **Python**：推荐安装 DashScope SDK（≥1.27.3）以启用 SDK Expert 智能助手，或 OpenAI SDK（≥1.40.0）用于 OpenAI 兼容调用：
  ```bash
  pip install -U dashscope  # 启用 SDK Expert
  pip install -U openai     # OpenAI 兼容
  ```
- **Java/Node.js/Go**：按 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档添加对应依赖（如 Maven/Gradle/GitHub 仓库坐标）。

### 2. API Key 配置
- **环境变量（推荐）**：全局设置 `DASHSCOPE_API_KEY`（Linux/macOS：`~/.bashrc` 或 `~/.zshrc`；Windows：系统属性 → 环境变量）；
- **代码内显式赋值（仅限调试）**：
  ```python
  import dashscope
  dashscope.api_key = "sk-xxxxxxxx"
  ```
- **重要安全提示**：**严禁在客户端（浏览器/移动端）或公开代码中硬编码 API Key**；生产环境应使用临时 API Key（最长 1800 秒）或服务端代理。

### 3. 快速验证
- 使用 DashScope SDK Expert（`dashscope` CLI）输入自然语言需求（如“用 qwen-plus [流式输出](../concepts/streaming-output.md)并统计 token”），自动生成并执行可运行代码；
- 或直接调用示例：
  ```python
  from dashscope import Generation
  response = Generation.call(model="qwen-plus", messages=[{"role": "user", "content": "你好"}])
  print(response.output.text)
  ```

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，**华北2（北京）的 Key 无法调用新加坡地域模型**，详见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配额与权限**：
  - 单个业务空间最多 20 个 API Key，主账号最多 20 个业务空间；
  - 自定义权限下，可选模型上限 30 个，IP 白名单上限 20 个；
  - 临时 API Key 最长有效期 1800 秒。
- **常见失败原因**：
  - 环境变量未生效：重启 IDE/终端，或使用 `sudo -E` 传递变量；
  - 请求体 JSON 格式错误：使用 `jsonlint.com` 校验，避免漏引号、逗号；
  - 模型未开通：调用前需在 [模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market) 确认模型状态；
  - 输入超限：检查 `messages` 总 [Token](../concepts/token.md) 数是否超过模型最大输入长度（见各模型文档）。
- **诊断建议**：
  - 报错时务必记录 `request_id`（响应 Header 或 Body 中），用于日志查询；
  - 复杂问题优先使用 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的 `/skill diagnose` 功能自动分析源码根因。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


