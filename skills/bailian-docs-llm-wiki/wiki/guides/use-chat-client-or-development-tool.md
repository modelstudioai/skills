# use chat client or development tool

阿里云百炼支持通过多种主流 AI 开发工具和客户端接入模型服务，覆盖终端 CLI、桌面 IDE、Web 应用及低代码平台等场景。开发者可根据使用习惯选择适配的工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证与端点。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速切换。

## 支持的模型/功能

百炼支持的模型能力因接入工具和计费方案而异：

- **文本生成模型**：全方案通用，包括 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.3`、`deepseek-v4-pro` 等。其中 `qwen3.x` 系列普遍支持思考模式（`enable_thinking`），需在请求体或配置中显式启用（如 [Qoder](raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) 和 [Kilo CLI](raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) 的配置示例中均要求设置 `thinking.type: enabled`）。
- **多模态模型**：仅部分工具支持图像/视频输入。例如千问 APP 工作助理明确支持文档与表格处理 [千问](raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)，Qwen Code 和 Claude Code 支持图像输入，但 Cursor 需注意模型名称格式转换（如 `glm-5.3` → `glm-5-3`）[Cursor](raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。
- **视觉与音频模型**：`Qwen-VL`、`QVQ`、`Qwen-Omni`、`Qwen-Audio` 等**不支持直接在 Dify 插件中配置**，必须通过 HTTP 节点调用原生 API [Dify](raw/model-user-guide/use-chat-client-or-development-tool/dify.md)；万相（Wan2）文生图/视频也需走异步任务流程，不可直连 [使用Postman或cURL调用图像/视频生成API](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：Dify 明确**不支持 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版和 Coding Plan**，仅允许使用按量计费 API Key。将套餐 API Key 用于 Dify 等工作流平台属于违规行为，可能导致订阅暂停或 Key 封禁 [更多工具](raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 关键参数

所有工具的核心配置参数一致，但字段名和层级略有差异：

| 参数 | 说明 | 常见取值/格式 |
|------|------|-------------|
| `API Key` | 计费方案专属密钥，**不通用** | Token Plan 个人版：`https://bailian.console.aliyun.com/cn-beijing/subscription/overview`；Coding Plan：`https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan`；按量计费：`raw/model-api-reference/preparations/get-api-key.md` |
| `Base URL` | 必须与 API Key 方案及地域严格匹配 | OpenAI 协议：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Anthropic 协议：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`；`{WorkspaceId}` 需替换为真实 ID [获取Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain) |
| `Model ID` | 模型标识符，区分大小写且需与套餐支持列表一致 | `qwen3.8-max`、`auto`、`qwen3.7-plus`；注意 Cursor 等工具需转义小数点（`glm-5.3` → `glm-5-3`）[Cursor](raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) |
| `API Protocol` | 决定请求格式与鉴权方式 | `openai-completions`（OpenAI v1）、`anthropic-messages`（Anthropic v1）；Hermes Agent 同时支持两种协议 [Hermes Agent](raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) |

## 使用方式

### 1. 安装与初始化
- CLI 工具（如 `qwen`、`hermes`、`claude`、`kilo`）依赖 Node.js ≥18.0（部分如 OpenClaw 要求 ≥22.19.0）[OpenClaw](raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)；
- 桌面应用（如 Cursor、Cherry Studio、Qoder CN）需下载安装包并完成首次登录；
- Web 平台（如 Dify、QwenPaw）通常通过浏览器访问，本地部署需按文档启动服务。

### 2. 配置凭证（三类典型路径）
- **环境变量**：`OPENAI_API_KEY`（Codex）、`BAILIAN_API_KEY`（DeepSeek Harness）、`ANTHROPIC_AUTH_TOKEN`（Claude Code）；
- **配置文件**：`~/.config/opencode/opencode.json`（OpenCode）、`~/.dsh/settings.yaml`（DeepSeek Harness）、`~/.qwen/settings.json`（Qwen Code）；
- **GUI 设置**：Cursor Settings > Models、Cherry Studio > 设置 > 模型、Qoder CN > 设置 > 模型。

### 3. 模型调用
- 终端工具：执行 `/auth`（Qwen Code）、`hermes config set`（Hermes Agent）等命令交互式配置；
- IDE 插件（Cline、Qoder JetBrains）：在侧边栏设置界面填写 Base URL、API Key、Model ID；
- Web 应用（QwenPaw、Dify）：在 Console 或 Studio 中添加自定义提供商，指定协议与端点。

## 限制和注意事项

- **计费方案隔离**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不互通**，且不能用于 Dify、Postman、cURL 等自动化平台 [更多工具](raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。错误混用将导致 401 错误，如 Qoder CN 报错“自定义模型服务异常”即常因类型选错 [Qoder CN（原 Lingma）](raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)。
- **地域强绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（如北京 Key 只能配北京 URL），否则产生费用或调用失败 [Cherry Studio](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **免费额度限制**：新人免费额度**仅限华北2（北京）地域**，且各模型额度独立计算，跨地域或跨模型调用不享受减免 [Cherry Studio](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **协议兼容性**：同一 Base URL 可能同时支持 OpenAI 和 Anthropic 协议，但需同步调整 `api_mode`（Hermes Agent）或 `wire_api`（Codex）等参数，否则返回 400 错误 [Hermes Agent](raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。
- **思考模式启用**：Qwen3 系列模型默认不启用深度推理，需在请求体（`extra_body.enable_thinking: true`）或配置文件（`thinking.type: enabled`）中显式开启，否则可能被拒绝或降级为普通响应 [Qwen Code](raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


