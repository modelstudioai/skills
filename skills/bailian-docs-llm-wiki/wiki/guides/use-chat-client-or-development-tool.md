# use chat client or development tool

百炼平台支持通过多种第三方客户端与开发工具接入大模型服务，适用于快速原型验证、本地 IDE 集成、自动化工作流编排等场景。这些工具大多基于标准 OpenAI 兼容 API（`/v1/chat/completions`）或百炼专属协议对接，无需从零实现 SDK。具体支持范围、参数适配及调用约束需结合各工具文档与百炼 API 规范协同使用。

## 支持的模型与功能

当前可接入的客户端/开发工具覆盖通用对话、代码生成、办公辅助、多模态编排等方向，包括但不限于：  
- 通用交互类：[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)、[Cherry Studio](https://help.aliyun.com/zh/model-studio/cherry-studio)、[Cline](https://help.aliyun.com/zh/model-studio/cline)  
- 代码增强类：[Cursor](https://help.aliyun.com/zh/model-studio/cursor)、[Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code)、[Qoder](https://help.aliyun.com/zh/model-studio/qoder-agent)、[Codex](https://help.aliyun.com/zh/model-studio/codex)、[OpenCode](https://help.aliyun.com/zh/model-studio/opencode)  
- 智能体框架类：[Hermes Agent](https://help.aliyun.com/zh/model-studio/hermes-agent)、[Dify](https://help.aliyun.com/zh/model-studio/dify)、[DeepSeek Harness](https://help.aliyun.com/zh/model-studio/deepseek-harness)  
- 办公与轻量 CLI：[千问](https://help.aliyun.com/zh/model-studio/qwen-office-assistant)、[Kilo CLI](https://help.aliyun.com/zh/model-studio/kilo-cli)、[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)  

所有工具均支持调用百炼平台上已部署的 `qwen-max`、`qwen-plus`、`qwen-turbo` 等主流文本模型；部分工具（如 [QwenPaw](https://help.aliyun.com/zh/model-studio/qwenpaw)、[Claude Code](https://help.aliyun.com/zh/model-studio/claude-code)）还支持[函数调用](../concepts/function-calling.md)（function calling）和工具集成（tool use），但需确认其版本是否兼容百炼 v2.1+ 的 `tools` 字段规范 —— 参见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中列出的工具链接说明。

## 关键参数

调用时需确保以下参数与百炼 API 要求一致：
- `model`: 必填，值必须为百炼控制台中实际部署的模型 ID（如 `qwen-max`），不可使用工具内置别名（如 `gpt-4`）；
- `api_key`: 使用百炼平台生成的 API Key（非阿里云主账号 AK/SK），且需具备对应模型的调用权限；
- `base_url`: 应设为 `https://dashscope.aliyuncs.com/api/v1`（标准 OpenAI 兼容入口）或 `https://dashscope.aliyuncs.com/compatible-mode/v1`（兼容模式）；
- `stream`: 若启用流式响应，须按百炼协议解析 `data: {...}` 行格式，部分工具（如旧版 [OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw)）默认解析 OpenAI 格式，可能丢帧 —— 详见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 列表中的工具文档说明。

> **注意**：[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api) 文档标题提及“图像与视频 API”，但其实际示例仍以文本接口为主；该工具对百炼多模态模型（如 `qwen-vl-plus`）的支持尚不完整，建议优先参考 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中“更多工具”链接跳转的最新兼容性说明。

## 使用方式

1. 在百炼控制台开通目标模型服务并获取 API Key；  
2. 在所选工具中配置 `base_url` 和 `api_key`（部分工具如 [Dify](https://help.aliyun.com/zh/model-studio/dify)、[Hermes Agent](https://help.aliyun.com/zh/model-studio/hermes-agent) 提供可视化模型源配置）；  
3. 设置 `model` 参数为实际部署的模型 ID（例如 `qwen-plus`），避免使用工具预设的非百炼模型名；  
4. 发起请求，验证响应状态码（200）与 `usage` 字段是否正常返回。  
调试建议：先用 `curl` 或 Postman 手动构造请求验证基础连通性，再迁移到目标工具 —— 可复用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中提供的各工具官网链接查阅认证细节。

## 限制和注意事项

- 单次请求 `messages` 长度上限为 32768 token（取决于模型上下文窗口），超长内容需截断或分块；  
- 工具侧缓存行为（如 [Cursor](https://help.aliyun.com/zh/model-studio/cursor) 的本地 history 缓存）可能导致重复请求被拦截，建议关闭或定期清理；  
- 部分工具（如 [Qoder CN（原 Lingma）](https://help.aliyun.com/zh/model-studio/lingma-agent)）在 2024 年 Q2 后已更名并调整 API 路径，旧配置将失效；  
- 百炼不提供对未列于 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 的第三方工具的官方支持或兼容性保证。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


