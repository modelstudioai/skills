# preparations

在调用阿里云百炼平台模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、环境变量设置等基础准备。这些步骤是所有模型调用（文本生成、多模态、语音、向量等）的共同前置条件，直接影响调用成功率与安全性。本文档结构化梳理关键环节，聚焦可执行操作与常见陷阱。

## 支持的模型/功能

百炼支持通过 DashScope SDK 和 OpenAI 兼容 SDK 调用全栈模型能力，包括文本生成（如 `qwen-plus`、`qwen3.7-max`）、图像生成、视频生成、语音合成（TTS）、语音识别（ASR）、向量嵌入（Embedding）、排序（Rerank）及实时语音/多模态模型（需 AOQ SDK）。**注意**：文档 1 中提到的“AOQ SDK 下载”链接指向 `raw/model-api-reference/realtime-api-user-guide/...`，但该路径下实际内容已迁移至新版 Realtime API 文档体系；请以 [模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2) 为准，避免依赖过时路径。实时语音与多模态模型必须使用 AOQ SDK 或指定 Realtime WebSocket 协议，DashScope HTTP SDK 不支持其底层流式交互语义。

## 关键参数

- **API Key**：必须通过百炼控制台按地域单独创建，**不可跨地域混用**；推荐归属 RAM 用户并绑定业务空间以实现权限隔离 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **Base URL**：华北2（北京）为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，其他地域需查 [Base URL 总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；DashScope SDK Expert 还支持私有 workspace 域名（如 `https://{workspace-id}.{region}.maas.aliyuncs.com/api/v1`）。
- **模型名称（model）**：严格区分大小写与命名规范，必须使用百炼官方模型 ID（如 `qwen3.7-plus`），而非开源社区名称（如 `Qwen/Qwen3.7-Plus`）；错误示例见 [错误码](../../raw/model-api-reference/preparations/error-code.md) 中 `Model not exist.` 条目。
- **流式参数（stream）**：部分模型（如思考模式模型、音频输出模型）强制要求 `stream=true`，否则报错；详见 [错误码](../../raw/model-api-reference/preparations/error-code.md) 中相关条目。

## 使用方式

1. **安装 SDK**：  
   - Python：`pip install -U dashscope`（≥1.27.3 启用 SDK Expert）或 `pip install -U openai`；  
   - Java/Node.js/Go：按文档 1 的 Gradle/Maven/npm/go get 指令配置对应依赖。  
2. **配置 API Key**：  
   - 推荐方式：设为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均有详细步骤）；  
   - 禁止行为：**切勿在客户端代码（浏览器、移动 App）中硬编码长期 API Key**，应使用临时 API Key（最长 1800 秒）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
3. **快速验证**：  
   - 使用 DashScope SDK Expert（`dashscope` CLI）：自然语言描述需求（如“用 qwen-plus [流式输出](../concepts/streaming-output.md)并统计 token”），自动校验版本、生成并执行可运行代码；  
   - 手动调用：确保 `messages` 格式合法（非空数组、`content` 类型匹配模型能力）、`model` 名称准确、`stream` 参数符合模型约束。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，跨地域调用必然失败。  
- **权限继承**：API Key 权限由其**归属业务空间**决定，同一空间内所有 API Key 权限一致；子业务空间的 API Key 仅能调用该空间已授权的模型 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **参数强校验**：`temperature` 必须 ∈ [0.0, 2.0)，`top_p` ∈ (0.0, 1.0]，`max_tokens` ≤ 模型最大输出长度；纯文本模型禁止传入 `image_url` 等多模态 `content`，否则触发 `InvalidParameter` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。  
- **SDK Expert 注意事项**：  
  - 需联网且消耗 token（按百炼计费）；  
  - 修改源码前必生成 diff 并征得用户确认，支持回滚；  
  - 仅校验 Python SDK 版本，生成其他语言代码时不校验其 SDK 版本。  
> **注意**：文档 3 中“多模态或通义以外模型：`pip install -U 'dashscope[acli-all]'`”与文档 1 中“安装 DashScope Python SDK”指令未明确此扩展依赖，实际使用多模态模型时需额外安装该 extra，否则 SDK Expert 可能无法生成正确代码。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


