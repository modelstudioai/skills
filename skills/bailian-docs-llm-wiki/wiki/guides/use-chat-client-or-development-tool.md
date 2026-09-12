# use chat client or development tool

百炼平台支持通过多种第三方客户端和开发工具调用大模型服务，适用于快速原型验证、本地 IDE 集成、自动化工作流等场景。所有工具均通过标准 API（如 [OpenAI 兼容接口](../concepts/openai-compatibility.md)或百炼专属 REST API）与平台交互，无需修改模型代码即可切换后端服务。具体能力取决于所选工具的协议兼容性及平台侧开放的模型权限。

## 支持的模型/功能

当前可接入的客户端与开发工具覆盖代码辅助、办公提效、[多模态](../concepts/multi-modal.md)交互、Agent 编排等方向，包括但不限于：  
- 代码类：[Cursor](https://help.aliyun.com/zh/model-studio/cursor)、[Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code)、[Qoder](https://help.aliyun.com/zh/model-studio/qoder-agent)、[Codex](https://help.aliyun.com/zh/model-studio/codex)、[OpenCode](https://help.aliyun.com/zh/model-studio/opencode)  
- Agent/低代码编排类：[Dify](https://help.aliyun.com/zh/model-studio/dify)、[Hermes Agent](https://help.aliyun.com/zh/model-studio/hermes-agent)、[Cherry Studio](https://help.aliyun.com/zh/model-studio/cherry-studio)  
- 通用聊天/调试类：[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)、[Cline](https://help.aliyun.com/zh/model-studio/cline)、[Kilo CLI](https://help.aliyun.com/zh/model-studio/kilo-cli)、[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)  
- 办公增强类：[千问](https://help.aliyun.com/zh/model-studio/qwen-office-assistant)、[QwenPaw](https://help.aliyun.com/zh/model-studio/qwenpaw)  

> **注意**：部分工具（如 [Claude Code](https://help.aliyun.com/zh/model-studio/claude-code) 和 [DeepSeek Harness](https://help.aliyun.com/zh/model-studio/deepseek-harness)）在 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中列出，但其官方文档已下线或迁移，实际接入前请以 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中最新链接为准；若链接跳转失败，建议优先选用 Dify、Cursor 或 Postman 等长期维护的工具。

## 关键参数

所有工具需配置以下基础参数才能成功调用百炼 API：

- `api_key`：从百炼控制台「API 密钥管理」获取，具有作用域限制（如仅限某模型或某项目）  
- `base_url`：统一为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容模式）或 `https://dashscope.aliyuncs.com/api/v1`（原生模式）  
- `model`：必须显式指定，例如 `qwen-max`、`qwen-plus`、`qwen-coder-turbo`；不支持通配符或别名  
- `stream`：部分工具（如 Cursor、Dify）默认启用流式响应，需确保前端能正确处理 SSE 或 chunked transfer encoding  

详细参数说明见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md)。

## 使用方式

1. **确认工具兼容性**：检查目标工具是否支持 OpenAI 兼容 API（推荐）或百炼原生 REST API；不支持的工具需通过中间代理（如 `openai-proxy`）转换请求格式  
2. **配置认证与端点**：在工具设置中填入 `api_key` 和 `base_url`，避免硬编码到项目源码中  
3. **选择模型并发起请求**：在 UI 或配置文件中指定 `model` 名称，调用 `/chat/completions`（兼容模式）或 `/messages`（原生模式）  
4. **验证响应结构**：注意百炼原生 API 的 `output.text` 字段与 OpenAI 兼容模式的 `choices[0].message.content` 语义一致，但字段路径不同  

## 限制和注意事项

- 单次请求最大上下文长度受模型本身限制（如 `qwen-max` 为 32768 tokens），工具层无法突破该上限  
- 流式响应中，`delta.content` 可能为空字符串（表示 token 边界），需忽略空片段而非报错  
- Postman 等 HTTP 客户端需手动设置 `Content-Type: application/json` 和 `Authorization: Bearer <api_key>`，遗漏任一将返回 `401 Unauthorized`  
- 工具内置的模型列表（如 Cursor 的下拉菜单）可能包含未开通权限的模型，实际调用前请先在百炼控制台「模型服务」中开通对应模型的调用权限  

> **注意**：[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中列出的 [Lingma Agent](https://help.aliyun.com/zh/model-studio/lingma-agent) 已更名为 [Qoder CN](https://help.aliyun.com/zh/model-studio/qoder-agent)，旧名称在 API 层面已不可用，配置时务必使用新模型标识 `qoder-cn`。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)



