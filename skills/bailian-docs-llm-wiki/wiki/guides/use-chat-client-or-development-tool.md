# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和自动化工作流等场景。开发者可根据计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）和协议兼容性（OpenAI 或 Anthropic）灵活配置，无需修改业务逻辑即可切换后端模型。

## 支持的模型/功能

- **通用文本生成模型**：所有工具均支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.6-flash` 等 Qwen 系列模型；部分工具（如 OpenClaw、Kilo CLI、Qoder）还支持 `glm-5.3`、`deepseek-v4.*` 等第三方模型。
- **多模态能力**：Qwen Code、千问 APP 工作助理、Dify（通过 Chatflow HTTP 节点）支持图像理解（Qwen-VL）、OCR（Qwen-OCR）及文生图（万相）等 AIGC 功能，但需注意协议限制（如 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 不支持直接配置 Qwen-Omni）。
- **思考模式（Reasoning）**：Qwen3 系列中带 `-max` 或 `-flash` 后缀的模型默认启用思考模式；CLI 工具（如 Cline、Qwen Code）需显式开启 `enable_thinking` 或勾选 **Enable R1 messages format** 才能触发完整推理链。
- **专属限制**：千问 APP 工作助理仅支持 [Token](../concepts/token.md) Plan（个人版/团队版），不支持按量计费或 Coding Plan；Dify 明确[不支持 Token Plan 和 Coding Plan](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)，仅允许使用按量计费 API Key。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，指定百炼服务端点。**OpenAI 兼容协议**路径以 `/compatible-mode/v1` 结尾；**Anthropic 兼容协议**以 `/apps/anthropic` 结尾。地域 URL 中 `{WorkspaceId}` 需替换为真实 ID（见 [获取 Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `api_key` | 必填，与 `base_url` 方案严格匹配：[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 的 API Key 互不通用，且不可用于 Dify 等工作流平台。 | `sk-xxx`（Token Plan 个人版）<br>`sk-yyy`（按量计费） |
| `model` | 必填，模型 ID 需与所选套餐支持列表一致（如 Token Plan 个人版不支持 `kimi-k2.6`，须写为 `kimi-k2-6`）。部分工具（如 Cursor、WorkBuddy）要求精确匹配大小写及命名规范。 | `qwen3.7-plus`<br>`auto`（自动路由） |
| `api_mode` / `api` | 协议标识，仅 Anthropic 兼容场景需显式设置（如 Hermes Agent 的 `anthropic_messages`，DeepSeek Harness 的 `openai-completions`）。 | `anthropic_messages`<br>`openai-completions` |

> **注意**：文档 4（Cursor）与文档 19（WorkBuddy）对 `base_url` 的路径要求存在差异——Cursor 使用 `/compatible-mode/v1`，而 WorkBuddy **强制要求补全 `/chat/completions`**（如 `.../v1/chat/completions`）。若在 WorkBuddy 中配置失败，请检查是否遗漏该路径后缀。

## 使用方式

1. **安装工具**：各工具依赖不同（如 Hermes Agent 需 WSL2 on Windows，OpenClaw 需 Node.js ≥24.16），请严格按对应文档执行安装（例如 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 的 `curl` 安装脚本）。
2. **配置凭证**：
   - CLI 工具（Hermes、Claude Code、Qwen Code）通常通过命令行配置（`hermes config set`）或编辑 `~/.xxx/config.yaml`；
   - 桌面应用（Cursor、Cherry Studio、WorkBuddy）通过 GUI 设置界面填写 `API Key`、`Base URL` 和 `Model ID`；
   - 开发平台（Dify）需先安装插件（如“通义千问”），再在插件设置中填入 API Key 和地域端点。
3. **验证连接**：发送简单请求（如 `"你好"`）并检查响应。若报错，优先参考各工具文档末尾的「常见问题」章节（如 [Cursor 常见问题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 提供错误码排查链接）。

## 限制和注意事项

- **协议与套餐绑定**：Token Plan 和 Coding Plan 同时支持 OpenAI 和 Anthropic 协议，但按量计费的 Anthropic 兼容接口文档（[Anthropic 兼容 API](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）明确要求 `base_url` 必须含 `/apps/anthropic`，而 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)必须含 `/compatible-mode/v1`。混用会导致 404 或 401 错误。
- **地域一致性**：按量计费的 `API Key` 与 `base_url` 地域必须严格匹配（如北京地域 Key 不能用于新加坡 URL），否则产生费用或认证失败（见 [Cherry Studio 常见问题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）。
- **免费额度限制**：新人免费额度仅适用于华北2（北京）地域的按量计费模型，且各模型额度独立计算（[Cherry Studio 常见问题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）。
- **不支持场景**：Token Plan/Coding Plan **禁止用于工作流平台（Dify、n8n）、API 测试工具（Postman）或自定义后端调用**（见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)），违规可能导致订阅暂停。
- **模型命名转换**：Cursor、Cherry Studio 等工具要求将带小数点的模型名（如 `kimi-k2.6`）转换为短横线格式（`kimi-k2-6`），否则报错 `The model xxx does not work with your current plan`（[Cursor 常见问题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)）。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)


