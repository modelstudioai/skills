# preparations

在调用阿里云百炼平台模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、基础环境准备等关键步骤。这些准备工作直接影响调用的稳定性、安全性与兼容性。本文汇总核心实践要点，覆盖主流 SDK（DashScope / OpenAI）、多语言支持、关键参数约束及常见排障路径，面向生产环境使用场景。

## 支持的模型/功能

百炼平台支持通过 DashScope SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用多种模型类型，包括文本生成（如 `qwen-plus`、`qwen3-8b`）、图像生成、视频生成、语音合成（TTS）、语音识别（ASR）、[向量嵌入](../concepts/embedding.md)（Embedding）和排序（Rerank）等。具体支持范围请参见[模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)。  
> **注意**：部分实时语音或多模态模型（如 Realtime API）需使用专用 [AOQ SDK](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，标准 DashScope 或 OpenAI SDK 不适用。  
对于高级开发体验，推荐使用 DashScope Python SDK ≥1.27.3 内置的 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)，其提供自然语言驱动的代码生成、错误诊断与自动修复能力，覆盖文本生成、多模态、语音、检索等全部能力域。

## 关键参数

调用时需关注以下核心参数及其约束（详见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)）：

- **`model`**：必须为百炼控制台模型市场中已开通的**精确模型 ID**（如 `qwen3-235b-a22b-instruct-2507`），不可混用开源社区命名（如 `Qwen/Qwen3-235B...`）；未开通模型将返回 `Model not exist` 或 `The product is not activated` 错误。
- **`stream`**：部分模型（如思考模式模型、音频输出模型）**强制要求 `stream=true`**；非流式调用将触发 `This model only support stream mode` 错误。
- **`enable_thinking`**：开启后需同时满足 `result_format="message"` 且 `incremental_output=true`；关闭该参数时，部分专用思考模型（如 `qwen3-235b-a22b-thinking-2507`）会报错 `The value of the enable_thinking parameter is restricted to True`。
- **`messages` / `content`**：纯文本模型仅接受字符串型 `content`；若传入数组（如 `[{ "type": "text", "text": "..." }]`）或含 `image_url` 等多模态元素，将报 `input content must be a string` 或 `Unexpected item type in content`；多模态模型则需严格按 `type`（`text`/`image_url`/`video_url`）校验结构。
- **数值型参数**：`temperature` ∈ [0.0, 2.0)，`top_p` ∈ (0.0, 1.0]，`max_tokens` ∈ [1, 模型最大输出 Token]，`seed` ∈ [0, 9223372036854775807]，越界将直接拒绝请求。

## 使用方式

1. **安装 SDK**：  
   - Python：`pip install -U dashscope`（推荐）或 `pip install -U openai`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）；  
   - Java：通过 Maven/Gradle 引入 [DashScope Java SDK](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java) 或 [OpenAI Java SDK](https://github.com/openai/openai-java?tab=readme-ov-file#openai-java-api-library)（建议 v3.5.0+）；  
   - Node.js/Go：分别执行 `npm install --save openai` 或 `go get 'github.com/openai/openai-go/v3'`。  
   > **注意**：DashScope SDK Expert 需 `dashscope>=1.27.3`，多模态模型需额外安装 `pip install -U 'dashscope[acli-all]'`（见 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)）。

2. **配置 API Key**：  
   - 在百炼控制台 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建 Key（注意地域隔离，不可跨地域混用）；  
   - 推荐将 `DASHSCOPE_API_KEY` 设为**永久环境变量**（Linux/macOS：`~/.bashrc`/`~/.zshrc`；Windows：系统属性 → 环境变量），避免客户端硬编码；  
   - 若需临时密钥，可生成最长 1800 秒的 [临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

3. **设置 Base URL**：  
   - DashScope 协议默认为 `https://dashscope.aliyuncs.com/api/v1`；  
   - [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需按地域配置 Base URL（如华北2为 `https://dashscope.aliyuncs.com/compatible-mode/v1`），详见 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。

## 限制和注意事项

- **地域与权限隔离**：API Key 与地域强绑定，且权限由其**归属业务空间**决定；同一空间内所有 Key 权限一致，无需为不同模型单独创建 Key（见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。  
- **安全红线**：**严禁在浏览器、移动 App 等客户端环境配置长期有效的 API Key**；敏感场景应使用临时 Key 或服务端代理。  
- **SDK 版本兼容性**：DashScope SDK Expert 会主动校验本地版本，过旧时提示升级；OpenAI SDK 的 `openai-java` 推荐固定为 `3.5.0`，避免因版本差异导致参数解析失败。  
- **错误排查优先级**：  
  1. 检查 `Request ID`（响应 Header 或 Body 中），用于日志追踪；  
  2. 使用 [阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)输入错误信息快速定位；  
  3. 对于代码问题，优先用 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的 `/skill diagnose` 自动分析源码根因。  
- **配额与并发**：`Throttling.RateQuota` 类错误需检查账号配额，可通过控制台申请提升；高并发调用需自行实现重试与降级逻辑。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


