# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发框架接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和 Agent 平台等形态。开发者可根据技术栈偏好选择 OpenAI 兼容协议或 Anthropic 兼容协议，使用 [Token](../concepts/token.md) Plan（个人版/团队版）、Coding Plan 或按量计费方案完成快速集成。所有工具均需配置对应套餐的专属 API Key 与地域化 Base URL。

## 支持的模型/功能

百炼支持的模型能力因接入方案而异：
- **[Token](../concepts/token.md) Plan 个人版与团队版**：仅限 AI 编程工具（如 Qwen Code、Hermes Agent）和 OpenClaw 类 Agent 使用，**不支持工作流平台（如 Dify、n8n）或 API 测试工具（如 Postman）** [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)；
- **Coding Plan**：面向开发者固定月费订阅，支持文本生成类模型（如 `qwen3.7-plus`），不支持多模态或思考模式增强模型；
- **按量计费**：适用范围最广，支持全部模型类型（含 Qwen-VL、QVQ、万相、Qwen-Omni 等），且可用于 Dify 等工作流平台 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)；
- **通用模型列表**：各方案支持的具体模型详见对应套餐文档，例如 [Token](../concepts/token.md) Plan 个人版支持 `qwen3.8-max`、`qwen3.6-flash`、`glm-5.3` 等 [Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

> **注意**：千问 APP 工作助理**仅支持 Token Plan（个人版/团队版）**，明确不支持按量计费或 Coding Plan [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。

## 关键参数

所有工具均依赖以下核心参数完成认证与路由：
- **API Key**：必须使用与所选方案严格匹配的专属密钥（Token Plan 个人版、Token Plan 团队版、Coding Plan、按量计费四者密钥互不通用）；
- **Base URL**：需按协议与地域双重匹配：
  - OpenAI 兼容协议：路径为 `/compatible-mode/v1`，例如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；
  - Anthropic 兼容协议：路径为 `/apps/anthropic`，例如 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`；
- **模型 ID**：须与套餐支持范围一致（如 Token Plan 团队版不支持 `wan2.6-t2i`），部分工具要求模型名格式转换（如 Cursor 中 `glm-5.3` → `glm-5-3`）；
- **Workspace ID**：仅按量计费需手动替换 `{WorkspaceId}` 占位符，获取方式见 [Regions 文档](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

## 使用方式

### 安装与初始化
- CLI 工具（如 `qwen`、`hermes`、`kilo`）普遍依赖 Node.js ≥18.0，通过 `npm install -g` 安装；
- 桌面应用（如 Cursor、Cherry Studio、Qoder）需下载安装包，启动后进入设置界面配置；
- Web UI 工具（如 DeepSeek Harness、QwenPaw）通常通过 `npx` 或本地服务启动（如 `npx @deepseek-ai/dsh web`）；
- IDE 插件（如 Cline、Qoder JetBrains 插件）在对应 IDE 扩展市场中搜索安装。

### 配置流程（统一范式）
1. **获取凭证**：登录百炼控制台，根据所选方案获取 API Key 与确认地域；
2. **填写端点**：在工具设置中填入对应协议的 Base URL（OpenAI 或 Anthropic）；
3. **指定模型**：从该方案支持的模型列表中选择 ID（如 `qwen3.8-flash`），部分工具需启用 `enable_thinking` 参数以激活推理模式；
4. **验证连接**：发送测试请求（如“你好”），检查是否返回有效响应。

> **注意**：Claude Code 需额外跳过官方登录验证，编辑 `~/.claude.json` 设置 `"hasCompletedOnboarding": true` [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。

## 限制和注意事项

- **地域绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（如北京 Key 不可配新加坡 URL），否则返回 401；
- **免费额度限制**：新人免费额度**仅限华北2（北京）地域**，跨地域调用将直接计费 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)；
- **模型兼容性**：Qwen3 系列思考模式模型（如 `qwen3.8-max`）在部分工具中需显式开启 `R1 messages format` 或 `enable_thinking`，否则报错 `enable_thinking parameter is restricted to True`；
- **违规调用风险**：将 Token Plan/Coding Plan 的 API Key 用于 Dify、Postman、自定义脚本等非授权场景，将被视为滥用，可能导致订阅暂停或 Key 封禁 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)；
- **图像/视频 API 特殊性**：文生图、文生视频等 AIGC 接口采用**异步机制**（创建任务 + 轮询查询），不适用标准 Chat API 调用方式，详见 [Postman/cURL 调用指南](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

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
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)


