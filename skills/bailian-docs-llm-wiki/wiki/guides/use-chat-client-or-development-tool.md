# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务。开发者可根据使用场景（如终端编程、IDE 集成、低代码工作流）选择适配的客户端，并按计费方案（Token Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速迁移。

## 支持的模型/功能

百炼支持的模型能力取决于所选计费方案与接入协议：

- **Token Plan 个人版/团队版**：支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus` 等 Qwen3 系列文本生成模型，部分工具（如 OpenClaw、Qwen Code）还支持图像输入；但**不支持**多模态（VL）、音频（Qwen-Audio）、OCR（Qwen-OCR）或 Omni 模型 [OpenClaw (raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。
- **Coding Plan**：仅支持 `qwen3.7-plus` 等指定文本模型，不支持思考模式（`enable_thinking`）或图像输入 [Hermes Agent (raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。
- **按量计费**：覆盖最全模型集，包括文生图（万相）、文生视频、Qwen-VL、QVQ、Qwen-Omni 等，需通过 Dify 的 HTTP 节点或直接调用 AIGC API 使用 [Dify (raw/model-user-guide/use-chat-client-or-development-tool/dify.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
- **千问 APP 工作助理**：仅限 Token Plan（个人版/团队版），支持 `qwen3.8-max` 等 5 款模型处理文档/表格任务，**不支持**按量计费或 Coding Plan [千问 (raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。

> **注意**：Dify 明确不支持 Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key；将套餐 API Key 用于 Dify 将被视为违规 [Dify (raw/model-user-guide/use-chat-client-or-development-tool/dify.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

## 关键参数

| 参数 | 说明 | 示例值 | 协议适配 |
|------|------|--------|----------|
| `Base URL` | 服务端点地址，必须与计费方案和地域严格匹配 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan 个人版）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量计费 + Anthropic 协议） | OpenAI 协议用 `/compatible-mode/v1`；Anthropic 协议用 `/apps/anthropic` |
| `API Key` | 方案专属密钥，**不可跨方案复用** | `sk-xxx`（按量计费）<br>`tp-xxx`（Token Plan）<br>`cp-xxx`（Coding Plan） | 所有方案均需对应密钥，401 错误通常因密钥与 URL 不匹配导致 |
| `Model ID` | 模型标识符，注意命名规范差异 | `qwen3.8-max`（标准名）<br>`glm-5-3`（Cursor 中需替换点为短横线）<br>`auto`（自动路由） | Cursor、Cherry Studio 等要求模型名转义；OpenClaw、Hermes Agent 支持原生命名 |
| `Thinking Mode` | 启用深度推理的开关，Qwen3 系列需显式开启 | `"enable_thinking": true`（JSON body）<br>或勾选 `Enable R1 messages format`（Cline 设置） | 仅 Qwen3 及 QwQ 模型有效；Coding Plan 不支持该参数 |

## 使用方式

### 1. 客户端安装
- **终端工具**（如 Hermes Agent、Claude Code、Qwen Code）：依赖 Node.js ≥18，通过 `npm install -g` 或一键脚本安装。
- **桌面应用**（如 Cursor、Cherry Studio、Qoder IDE）：从官网下载安装包，无需本地环境配置。
- **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 市场搜索安装。
- **Web 平台**（如 Dify、QwenPaw）：访问网页或运行 `qwenpaw app` 启动本地服务。

### 2. 凭证配置
所有工具均遵循统一配置逻辑：
- **OpenAI 兼容协议**：设置 `Base URL` + `API Key` + `Model ID`（如 Cursor、Chatbox、QwenPaw）。
- **Anthropic 兼容协议**：设置 `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_MODEL`（如 Claude Code、Hermes Agent）。
- **配置文件路径示例**：
  - OpenClaw：`~/.openclaw/openclaw.json`
  - Hermes Agent：`~/.hermes/config.yaml`
  - Qwen Code：`~/.qwen/settings.json`

### 3. 模型调用验证
- 发送简单请求（如 `"你好"`）确认基础连通性。
- 对于支持思考模式的模型，发送含复杂逻辑的指令（如 `"分析以下代码的潜在内存泄漏并给出修复建议"`）验证 `enable_thinking` 生效。
- 图像/视频生成类任务需使用异步流程：先 `POST /image-synthesis` 获取 `task_id`，再 `GET /tasks/{task_id}` 轮询结果 [使用Postman或cURL调用图像/视频生成API (raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 限制和注意事项

- **方案隔离**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不通用**；按量计费 Key 仅限该方案使用。混用将触发 401 错误。
- **地域绑定**：按量计费的 `Base URL` 中 `{WorkspaceId}` 必须与 API Key 所属地域一致（如北京 Key 配北京 WorkspaceId），否则产生费用或调用失败 [Cherry Studio (raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **免费额度限制**：新人免费额度**仅限华北2（北京）地域**，且各模型额度独立计算，不可跨模型共享 [Cherry Studio (raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **不支持场景**：
  - Token Plan/Coding Plan **禁止用于工作流平台**（Dify、n8n、Coze）、API 测试工具（Postman、Insomnia）或自定义后端调用；
  - 千问 APP 工作助理**仅支持 Token Plan**，不支持按量计费或 Coding Plan；
  - Cursor 免费版**仅支持 `auto` 模型**，调用具体模型需升级至 Pro 版本。
- **模型兼容性**：部分工具对模型特性支持有限 —— 如 Coding Plan 不支持 `enable_thinking`，Qoder CN 企业版不支持百炼接入，Trae 等通用客户端需手动配置协议类型（OpenAI/Anthropic）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)


