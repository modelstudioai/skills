# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、环境准备及参数校验等基础工作。这些步骤直接影响调用的可用性、安全性与稳定性。本文汇总关键准备项，聚焦可执行操作与常见陷阱，不涉及模型选型或业务逻辑设计。

## 支持的模型/功能

- **模型接入方式**：支持通过 DashScope SDK（Python/Java）或 OpenAI 兼容 SDK（Python/Node.js/Java/Go）调用。OpenAI SDK 适用于所有 [OpenAI 兼容接口](../concepts/openai-compatibility.md)；DashScope SDK 提供更深度的百炼原生能力支持，如模型诊断、流式控制、多模态结构化输入等 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **功能覆盖**：DashScope Python SDK ≥1.27.3 内置 SDK Expert 工具，支持自然语言生成可运行代码、自动诊断报错、文件级根因分析、API 文档查询等 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。
- **协议与模型匹配**：Realtime API（语音/实时多模态）需使用专用 AOQ SDK；标准文本、图像、视频、语音合成/识别、向量嵌入、排序等模型均通过 DashScope 或 OpenAI SDK 接入 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

## 关键参数

| 参数 | 必填 | 说明 | 示例/约束 |
|------|------|------|-----------|
| `DASHSCOPE_API_KEY` | 是 | 地域隔离，不可跨地域复用；建议配置为环境变量，禁止硬编码于客户端 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) | `sk-xxxxxxxx` |
| `base_url` | 否（推荐显式设置） | 各地域独立域名，华北2（北京）为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；其他地域需查 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md) | `https://{workspace-id}.{region}.maas.aliyuncs.com/api/v1`（DashScope 原生协议） |
| `model` | 是 | 必须与[模型列表](raw/model-user-guide/get-started-with-models/models.md)中 ID 完全一致，区分大小写，不可混用开源名（如 `qwen3.7-plus` ✅，`Qwen/Qwen3.7-Plus` ❌） | `qwen-plus`, `qwen3.7-max`, `deepseek-v4-pro` |
| `stream` | 按模型要求 | 部分模型（如思考模式模型、音频输出模型）强制要求 `true`；非流式调用会返回 `400-InvalidParameter` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md) | `true` / `false` |
| `result_format` | 按场景 | 思考模式模型必须设为 `"message"`；结构化输出需配合提示词含 `json` 关键词且 `enable_thinking=false` | `"message"`, `{"type": "json_object"}` |
| `incremental_output` | 按模型要求 | 开启 `enable_thinking` 时必须为 `true`；部分模型（如 `qwen3.7-plus`）仅支持 `true` | `true` |

> **注意**：文档 3 中 `dashscope-sdk-expert` 的示例代码默认使用 `result_format="message"` 和 `incremental_output=True`，但文档 4 明确指出 `enable_thinking=true` 时 `result_format` **必须**为 `"message"`，而部分模型（如 `qwen3.7-plus`）的 `enable_thinking` **仅支持 `true`**。因此，对这类模型，`result_format="message"` 是强制要求，不可省略或修改。

## 使用方式

1. **获取并配置 API Key**  
   - 登录百炼控制台，在对应地域创建 API Key，注意归属业务空间与权限范围（默认空间可调用全部标准模型）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
   - 推荐配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均有详细命令），避免在代码中硬编码。

2. **安装 SDK**  
   - Python：`pip install -U dashscope`（原生）或 `pip install -U openai`（OpenAI 兼容）。若需 SDK Expert，确保版本 ≥1.27.3；多模态模型需 `pip install -U 'dashscope[acli-all]'` [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。  
   - Java/Node.js/Go：按文档 2 中 Gradle/Maven/npm/go get 命令添加对应依赖。

3. **验证与调试**  
   - 启动 SDK Expert CLI：`dashscope`，使用 `/setup` 配置 key 和 base_url，自然语言提问生成代码或诊断问题 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。  
   - 调用失败时，务必记录 `request_id`（响应 Header 或 Body 中），用于日志查询或提工单 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 限制和注意事项

- **地域隔离**：API Key、base_url、模型列表均按地域独立，**严禁跨地域混用**。华北2（北京）的 Key 无法调用新加坡地域模型 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **安全红线**：**禁止在浏览器、移动 App 等客户端环境配置长期有效的 API Key**。敏感场景应使用临时 API Key（最长 1800 秒） [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **环境变量生效**：设置后需重启 IDE、终端或服务进程；`sudo` 执行时需加 `-E` 参数继承环境变量 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **模型能力约束**：  
  - 纯文本模型（如 `qwen3.7-max`）**不接受 `image_url` 等多模态 content**，否则报 `Unexpected item type in content`；需改用 `qwen3-vl` 等多模态模型 [错误码](../../raw/model-api-reference/preparations/error-code.md)。  
  - `messages` 数组不能为空；`content` 字段必须为字符串（纯文本模型）或合法对象数组（多模态模型）；JSON 请求体需语法正确，否则触发 `Required body invalid` [错误码](../../raw/model-api-reference/preparations/error-code.md)。  
- **配额与计费**：SDK Expert 诊断过程消耗 token，按百炼计费；生成的代码需自行审查生产就绪性（错误处理、并发控制、敏感信息） [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


