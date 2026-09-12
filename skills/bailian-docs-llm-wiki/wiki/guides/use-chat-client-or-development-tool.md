# use chat client or development tool

百炼平台支持通过多种第三方客户端与开发工具接入大模型服务，适用于快速原型验证、本地 IDE 集成、自动化工作流编排等场景。这些工具大多基于标准 OpenAI 兼容 API（`/v1/chat/completions`）或百炼专属协议对接，无需从零实现 SDK。具体支持范围、参数适配及调用约束需结合各工具文档与百炼 API 规范协同使用。

## 支持的模型与功能

当前可接入的客户端/开发工具覆盖通用对话、代码生成、办公辅助、多模态编排等方向，包括但不限于：  
- 通用智能体类：[Hermes Agent](https://help.aliyun.com/zh/model-studio/hermes-agent)、[Cherry Studio](https://help.aliyun.com/zh/model-studio/cherry-studio)、[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)  
- 代码增强类：[Cursor](https://help.aliyun.com/zh/model-studio/cursor)、[Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code)、[Qoder](https://help.aliyun.com/zh/model-studio/qoder-agent)、[Codex](https://help.aliyun.com/zh/model-studio/codex)  
- 办公与轻量应用类：[千问](https://help.aliyun.com/zh/model-studio/qwen-office-assistant)、[QwenPaw](https://help.aliyun.com/zh/model-studio/qwenpaw)  
- CLI 与测试工具类：[Kilo CLI](https://help.aliyun.com/zh/model-studio/kilo-cli)、[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)、[Dify](https://help.aliyun.com/zh/model-studio/dify)  

> **注意**：部分工具（如 [Claude Code](https://help.aliyun.com/zh/model-studio/claude-code) 和 [OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw)）实际依赖百炼托管的 `qwen-max` 或 `qwen-plus` 模型，但其前端界面可能未暴露全部百炼原生能力（如 `tools` 调用、`stream` 分块控制），具体以 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中列出的工具链接为准。

## 关键参数

使用任一客户端/开发工具时，必须正确配置以下核心参数：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `api_key` | 百炼平台生成的 API Key（非阿里云 AccessKey） | `sk-xxx` |
| `base_url` | 百炼 [OpenAI 兼容接口](../concepts/openai-compatibility.md)地址 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `model` | 必须为百炼已开通的模型 ID，区分大小写 | `qwen-max`, `qwen-plus`, `qwen-turbo` |
| `stream` | 是否启用流式响应（部分工具默认关闭，需显式开启） | `true` / `false` |

不支持在客户端中直接设置 `top_p`、`temperature` 等采样参数的工具（如早期版本 [Qoder CN（原 Lingma）](https://help.aliyun.com/zh/model-studio/lingma-agent)），应优先查阅 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中对应工具的最新兼容性说明。

## 使用方式

1. 在百炼控制台「API 密钥管理」中创建并复制有效 `api_key`；  
2. 在目标工具中配置 `base_url` 和 `model`（例如 Cursor 需在 Settings → AI → Custom Model 中填写）；  
3. 验证调用：发送最简请求 `{"model":"qwen-turbo","messages":[{"role":"user","content":"你好"}]}`；  
4. 如需[函数调用](../concepts/function-calling.md)（`tools`）、系统提示词（`system` role）或多轮上下文管理，请确认所选工具是否支持——[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 列出的所有工具均未声明对 `tools` 字段的完整支持，建议在生产环境中优先使用百炼官方 SDK 或自行封装 HTTP 请求。

## 限制和注意事项

- 所有客户端工具均受百炼平台级配额与速率限制约束（如每分钟请求数、最大上下文长度），与工具自身限制叠加生效；  
- 不支持通过客户端上传文件或调用多模态 API（如图像理解），此类能力需直接调用百炼 `/v1/multimodal` 接口；  
- [DeepSeek Harness](https://help.aliyun.com/zh/model-studio/deepseek-harness) 名称易引发误解，其实际仅作为百炼模型的轻量前端代理，**不运行 DeepSeek 自研模型**；  
- Postman 示例中使用的 `/v1/images/generations` 路径属于百炼图像生成 API，**不适用于 chat client 场景**，该路径未在 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 的主列表中归类为 chat 工具，属文档归类偏差，使用时请严格按接口类型选择工具。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


