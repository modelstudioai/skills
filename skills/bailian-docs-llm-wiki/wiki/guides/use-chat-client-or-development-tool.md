# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务。开发者可根据使用场景（如终端编程、IDE 辅助、低代码工作流）选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速集成。

## 支持的模型/功能

百炼支持的模型能力取决于所选计费方案与接入协议：

- **[Token](../concepts/token.md) Plan 个人版/团队版**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro`），不支持图像、音频、OCR 等多模态模型；[Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 均明确限定为文本生成类。
- **Coding Plan**：支持 `qwen3.7-plus` 等指定文本模型，详见 [Coding Plan 支持的模型](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。
- **按量计费**：覆盖最全模型谱系，包括文生图（`wan2.6-t2i`）、文生视频（`wan2.6-t2v`）、视觉理解（`qwen-vl`）、语音（`qwen-audio`）、OCR（`qwen-ocr`）等，但需通过专用 API（非 OpenAI/Anthropic 兼容接口）调用；[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz) 页面仅列出兼容协议模型，完整列表请参见控制台。
- **特殊限制**：Dify 等工作流平台**不支持** [Token](../concepts/token.md) Plan 及 Coding Plan，仅允许使用按量计费 API Key —— 此限制在 [Dify 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 中被明确强调。

> **注意**：文档 7（千问 APP）明确指出“仅支持 Token Plan（个人版和团队版），不支持按量计费或 Coding Plan”，而文档 17（Dify）则规定“**不支持**使用 Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入”，二者适用范围完全正交，无冲突。

## 关键参数

所有工具共用以下核心参数，但协议与路径存在差异：

| 参数 | OpenAI 兼容协议 | Anthropic 兼容协议 | 说明 |
|------|------------------|------------------------|------|
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/v1`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（按量） | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量） | 协议决定路径后缀；按量计费必须替换 `{WorkspaceId}` 为真实值，详见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain) |
| **API Key** | 各方案专属密钥，**不通用**：<br>- Token Plan 个人版：[控制台链接](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)<br>- Token Plan 团队版：[控制台链接](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)<br>- Coding Plan：[控制台链接](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)<br>- 按量计费：[获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md) | 同上，但部分工具（如 Claude Code）要求环境变量名为 `ANTHROPIC_AUTH_TOKEN` | Key 与 Base URL 必须同属一方案且地域一致，否则返回 401；[Qoder CN 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 明确提示“提供商或类型与实际套餐不一致”是常见报错原因 |
| **Model ID** | `qwen3.8-max`、`glm-5-3`（注意：Cursor 要求将 `glm-5.3` 写为 `glm-5-3`） | `qwen3.8-max`、`auto`（OpenClaw 配置中 `auto` 为默认值） | 模型名需严格匹配，部分工具（如 Cursor）要求格式转换；[更多工具文档](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 指出 Token Plan 仅支持文本生成类模型 |

## 使用方式

### 1. 工具安装
- **终端工具**（如 Hermes Agent、Qwen Code、Claude Code）：依赖 Node.js ≥18（文档 2、3、8），推荐使用 `curl` 脚本或 `npm install -g` 安装。
- **桌面客户端**（如 Cursor、Cherry Studio、Chatbox）：从官网下载安装包，无需额外依赖。
- **IDE 插件**（如 Cline、Qoder）：在 VS Code 或 JetBrains 扩展市场直接安装。
- **平台类**（如 Dify）：通过 SaaS 控制台或自托管部署，无需本地安装。

### 2. 凭证配置
- **图形界面工具**（Cursor、Cherry Studio、Qoder IDE）：在设置 → 模型 → 添加中填写 API Key、Base URL、Model ID。
- **命令行工具**（OpenClaw、Hermes Agent、Kilo CLI）：通过 CLI 命令（如 `openclaw onboard`、`hermes config set`）或编辑配置文件（如 `~/.openclaw/openclaw.json`、`~/.kilo/config.json`）完成。
- **Web 平台**（Dify）：在「设置」→「模型供应商」中配置插件及 API Key；[Dify 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 特别说明需使用「通义千问」插件而非原生 OpenAI 插件。

### 3. 高级功能启用
- **思考模式（Reasoning）**：Qwen3 系列模型需显式开启。CLI 工具（如 Qwen Code、Kilo CLI）通过 `enable_thinking: true` 或 `extra_body.enable_thinking` 控制；GUI 工具（如 Cline、Cherry Studio）需在设置中勾选「Enable R1 messages format」或「思考模式」。
- **多模态输入**：仅按量计费支持图像/视频/音频，需调用专用 API（非兼容协议）。[Postman/cURL 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 详细说明异步任务创建与轮询机制，适用于快速验证。

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不通用**，混用将导致 401 错误；[Qoder CN 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 和 [Cline 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 均强调此风险。
- **地域强绑定**：按量计费的 API Key 与 Base URL 必须同地域（如北京 Key 配北京 URL），跨地域调用将产生费用或失败；[Cherry Studio 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 指出“免费额度仅适用于华北2（北京）地域”，其他地域调用不享受免费额度。
- **工具类型限制**：Token Plan 及 Coding Plan **禁止用于工作流平台**（Dify、n8n、Coze）和 **API 测试工具**（Postman、cURL）；[更多工具文档](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 明确列出“不支持的工具类型”，违规使用可能导致订阅暂停或 Key 封禁。
- **模型兼容性**：千问 APP（文档 7）仅支持 Token Plan，不支持按量/Coding；Dify（文档 17）仅支持按量，不支持 Token Plan/Coding —— 二者形成互补覆盖，开发者需按工具类型严格选型。
- **配置生效延迟**：部分工具（如 QwenPaw）需重启应用或重新加载配置；长对话超限问题可通过在提供商设置中调整 `max_tokens` 等参数解决，详见 [QwenPaw 常见问题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


