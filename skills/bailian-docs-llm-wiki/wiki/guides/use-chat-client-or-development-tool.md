# use chat client or development tool

阿里云百炼支持多种主流 AI 编程客户端与开发工具（如 Hermes Agent、Cursor、Qwen Code 等），开发者可通过 Token Plan 个人版/团队版、Coding Plan 或按量计费四种方案接入，使用 Qwen、GLM、DeepSeek 等模型。所有工具均基于 OpenAI 或 Anthropic 兼容协议，配置核心为 `API Key`、`Base URL` 和 `Model ID` 三要素。本文档结构化梳理支持范围、关键参数、配置方式及限制，便于快速选型与调试。

## 支持的模型/功能

百炼支持的模型能力因接入方案而异，**并非所有模型在所有套餐下均可用**：

- **Token Plan 个人版/团队版**：支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.2` 等文本生成模型；部分工具（如 OpenClaw）明确列出其支持的上下文窗口（983616 tokens）与输入模态（text/image）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。  
- **Coding Plan**：主要支持 `qwen3.7-plus`、`qwen3.6-plus` 等侧重代码能力的模型，不支持 `qwen3.8-max` 等最新推理模型 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。  
- **按量计费**：覆盖最全模型集，包括文生图（`wan2.6-t2i`）、视频生成、多模态（`Qwen-VL`、`QVQ`）及语音模型（`Qwen-Audio`），但需通过 HTTP API 或 Dify 的 HTTP 节点调用，**不支持在 Cursor、Qoder 等 IDE 插件中直接选择** [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。  
- **千问 APP 工作助理**：仅支持 Token Plan（个人版/团队版），且**仅限桌面端与 7.1.2+ 手机 APP**，不支持按量计费或 Coding Plan [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。

> **注意**：文档 19 明确指出，Token Plan 个人版/团队版和 Coding Plan **禁止用于工作流平台（如 Dify、Coze）、API 测试工具（Postman、cURL）或自定义后端应用**；违规使用可能导致订阅暂停或 API Key 封禁。Dify 文档也强调其仅接受按量计费 API Key [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 关键参数

所有工具配置均围绕以下三个核心参数，但协议与路径存在差异：

| 参数 | OpenAI 兼容协议 | Anthropic 兼容协议 | 说明 |
|------|----------------|---------------------|------|
| **API Key** | 各方案专属 Key（不可混用） | 同左 | Token Plan 个人版 Key 仅对 `token-plan.cn-beijing.maas.aliyuncs.com` 有效；按量计费 Key 必须与 Base URL 地域一致。 |
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>`https://coding.dashscope.aliyuncs.com/v1`<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` | OpenAI 协议路径为 `/compatible-mode/v1`；Anthropic 协议路径为 `/apps/anthropic`。按量计费 URL 中 `{WorkspaceId}` 必须替换为真实值。 |
| **Model ID** | `qwen3.8-max`、`glm-5-2`（注意 `-` 替代 `.`） | `qwen3.8-max`（保持原名） | Cursor 等工具要求模型名中 `.` 替换为 `-`（如 `glm-5.2` → `glm-5-2`），而 Hermes Agent、Claude Code 等保留原名。 |

## 使用方式

### 安装与初始化
- **CLI 工具**（Hermes Agent、Qwen Code、Kilo CLI）：通常通过 `curl` 脚本或 `npm install -g` 安装，安装后需重载 shell（如 `source ~/.zshrc`）或重启终端。
- **桌面/IDE 工具**（Cursor、Qoder、Cherry Studio）：从官网下载安装包，启动后通过图形界面配置。
- **Web/本地服务**（OpenClaw、QwenPaw、DeepSeek Harness）：通过 `npm install -g` 或一键脚本启动 Web UI（如 `openclaw`、`qwenpaw app`），访问 `http://127.0.0.1:8088` 等地址操作。

### 配置凭证（以 Token Plan 个人版为例）
1. **获取 API Key**：登录百炼控制台 → [Token Plan 个人版页面](https://bailian.console.aliyun.com/cn-beijing/subscription/overview) 复制 Key。  
2. **设置 Base URL**：使用 OpenAI 协议时填 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 协议时填 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`。  
3. **指定 Model ID**：根据工具要求填写（如 `qwen3.8-max` 或 `qwen3-8-max`）。  
4. **验证**：发送测试请求（如 “你好”），成功返回即配置完成。

> **注意**：Claude Code 需额外跳过官方登录验证（写入 `~/.claude.json` 设 `hasCompletedOnboarding: true`），而 Qwen Code 提供 `/auth` 可视化命令简化流程 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。

## 限制和注意事项

- **地域绑定严格**：按量计费的 API Key 与 Base URL 地域必须一致（如北京 Key 不能用于新加坡 URL），否则报错 `401 Incorrect API key provided`。免费额度也仅限华北2（北京）地域生效 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。  
- **模型命名兼容性**：Cursor、Cherry Studio 等工具要求模型名中 `.` 替换为 `-`（如 `kimi-k2.6` → `kimi-k2-6`），而 Hermes Agent、OpenClaw 等保留原名，配置时需按工具文档调整。  
- **思考模式（Thinking Mode）**：Qwen3 系列模型需显式启用 `enable_thinking`（如 Qwen Code 的 `settings.json` 中设 `"enable_thinking": true`；Cline 需勾选 **Enable R1 messages format**），否则可能报错 `The value of the enable_thinking parameter is restricted to True`。  
- **权限与版本限制**：  
  - 千问 APP 需升级至 **7.1.2+** 才支持 Token Plan 模型；  
  - Cursor 免费版仅支持 Auto 模式，调用自定义模型需升级至 **Pro 及以上套餐**；  
  - Qoder CN 企业版**不支持**接入百炼，仅限个人社区版/专业版。  
- **错误排查优先级**：遇到 `401` 错误，先确认 Key 与 URL 方案/地域匹配；遇到 `400 InternalError.Algo.InvalidParameter`，检查是否遗漏思考模式配置；模型不可见时，关闭 Auto 模式再手动选择。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
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


