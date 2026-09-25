# use chat client or development tool

百炼平台支持通过标准 Chat API 接入各类第三方客户端与开发工具，无需修改业务逻辑即可调用百炼托管的模型服务。开发者可选择图形化客户端（如 Cursor、Cherry Studio）或命令行工具（如 Kilo CLI、OpenClaw），亦可集成至低代码平台（如 Dify）或 API 调试环境（如 Postman）。所有接入均基于统一的 `/v1/chat/completions` 接口规范，兼容 OpenAI SDK。

## 支持的模型/功能

当前支持全部百炼托管的 Chat 模型，包括 Qwen-Max、Qwen-Plus、Qwen-Turbo 及 DeepSeek-VL 等多模态模型（需工具显式支持图像/视频输入）。部分工具提供增强能力：  
- Hermes Agent 和 Qoder 支持多步推理与插件调用；  
- Cursor、Cherry Studio、Qwen Code 内置代码补全与调试上下文感知；  
- Postman 仅支持基础文本请求，[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 中提及的图像/视频 API 需手动构造 multipart 请求，不适用于通用 Chat 客户端。  
> **注意**：[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 中仍称“Lingma”，但该工具已正式更名为“Qoder CN”，文档未同步更新，实际配置请以 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) 为准。

## 关键参数

所有工具均需配置以下最小参数集：  
- `model`: 必填，如 `qwen-max`、`qwen-plus`；  
- `api_key`: 百炼平台生成的 API Key（非阿里云主账号 AK/SK）；  
- `base_url`: 固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（兼容模式）或 `https://dashscope.aliyuncs.com/api/v1`（原生模式）；  
- `temperature` / `top_p` / `max_tokens`: 各工具默认值不同，建议显式指定以保证行为一致。

## 使用方式

1. 在百炼控制台「API 密钥」页获取有效 `api_key`；  
2. 根据所选工具文档配置 endpoint 与认证信息，例如：  
   - OpenClaw：在 Settings → Model Provider 中选择 “DashScope” 并填入 `base_url` 与 `api_key`；  
   - Kilo CLI：运行 `kilo config set --provider dashscope --api-key <key> --base-url <url>`；  
   - Dify：在「Model Configuration」中添加 DashScope 模型，选择对应 `model` 名称。  
详细步骤见各工具子文档，如 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)、[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)。

## 限制和注意事项

- 单次请求 `messages` 长度上限为 32768 token（Qwen-Turbo 为 65536），超出将返回 400 错误；  
- 流式响应（`stream: true`）在部分 GUI 工具（如 Chatbox、QwenPaw）中可能触发 UI 渲染异常，建议关闭流式或降级为 `stream: false`；  
- DeepSeek Harness 当前仅支持 `deepseek-coder` 系列模型，调用 `qwen-*` 模型会返回 404，该限制未在 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md) 中明确说明；  
- 所有工具均不支持自定义 system [prompt](prompt.md) 的 role 覆盖（即 `role: "system"` 字段会被忽略），实际 system 指令需通过百炼控制台模型微调或 API 参数 `system` 传入（若工具支持）。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


