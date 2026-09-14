# use chat client or development tool

百炼平台支持通过多种第三方客户端与开发工具接入大模型服务，适用于快速原型验证、本地 IDE 集成、自动化工作流编排等场景。这些工具大多基于标准 OpenAI 兼容 API（`/v1/chat/completions`）或百炼专属协议对接，无需从零实现 SDK。具体支持范围、参数适配及调用约束需结合各工具文档与百炼 API 规范协同使用。

## 支持的模型与功能

当前可接入的客户端/开发工具覆盖通用对话、代码生成、办公辅助、多模态编排等方向，包括但不限于：  
- 通用智能体类：[Hermes Agent](https://help.aliyun.com/zh/model-studio/hermes-agent)、[Cherry Studio](https://help.aliyun.com/zh/model-studio/cherry-studio)、[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)  
- 代码增强类：[Cursor](https://help.aliyun.com/zh/model-studio/cursor)、[Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code)、[Qoder](https://help.aliyun.com/zh/model-studio/qoder-agent)、[Codex](https://help.aliyun.com/zh/model-studio/codex)  
- 办公与轻量应用类：[千问](https://help.aliyun.com/zh/model-studio/qwen-office-assistant)、[QwenPaw](https://help.aliyun.com/zh/model-studio/qwenpaw)  
- CLI 与测试工具类：[Kilo CLI](https://help.aliyun.com/zh/model-studio/kilo-cli)、[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)、[Dify](https://help.aliyun.com/zh/model-studio/dify)  

> **注意**：部分工具（如 [Claude Code](https://help.aliyun.com/zh/model-studio/claude-code) 和 [OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw)）实际依赖百炼托管的 Qwen 系列模型，其底层能力与 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 所列工具清单一致，但不支持直接切换为非 Qwen 模型（如 DeepSeek 或 Llama）。该限制在 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中未明确说明，需以实际 API 响应为准。

## 关键参数

所有兼容 OpenAI 协议的工具需正确配置以下参数：
- `base_url`: `https://dashscope.aliyuncs.com/compatible-mode/v1`（百炼 OpenAI 兼容端点）  
- `api_key`: 百炼平台生成的 API Key（非阿里云 AccessKey）  
- `model`: 必须为百炼已开通的模型 ID，例如 `qwen-max`、`qwen-plus`、`qwen-turbo`；不支持任意字符串或厂商原生模型名（如 `gpt-4o`）  
- `stream`: 仅当工具显式支持 SSE 流式响应时才建议启用；部分 GUI 工具（如 [Cline](https://help.aliyun.com/zh/model-studio/cline)）默认禁用流式，需手动开启  

部分工具（如 [DeepSeek Harness](https://help.aliyun.com/zh/model-studio/deepseek-harness)）使用私有协议，其 `model` 参数需严格匹配百炼控制台「模型服务」页中显示的部署名称，详见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md)。

## 使用方式

1. 在百炼控制台开通目标模型并获取 API Key；  
2. 根据所选工具文档配置 endpoint、key 与 model（参考各工具官网链接）；  
3. 启动工具并发起请求——若返回 `401 Unauthorized`，检查 API Key 是否过期或权限不足；若返回 `404 Not Found`，确认 model 名称是否拼写正确且已在百炼启用；  
4. 对于非 OpenAI 协议工具（如 [Qoder CN（原 Lingma）](https://help.aliyun.com/zh/model-studio/lingma-agent)），需使用百炼专属 SDK 或按其文档要求构造 HTTP 请求头（含 `X-DashScope-DataInspection` 等字段）。

## 限制和注意事项

- 单工具实例默认共享百炼账号的调用配额，不支持按工具粒度限流；  
- 所有工具均**不支持**上传本地文件作为上下文（如 `.pdf`、`.docx`），仅可通过 API 的 `messages[].content` 字段传入文本片段；  
- [Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api) 示例中使用的 `/v1/images/generations` 端点**不适用于 chat 类工具**，该路径专用于文生图，与本主题无关；  
- 若工具文档声称支持“多模态输入”，实际在百炼接入时仅生效于纯文本模式，图像/音频需先经百炼多模态 API 预处理为 embedding 或描述文本。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


