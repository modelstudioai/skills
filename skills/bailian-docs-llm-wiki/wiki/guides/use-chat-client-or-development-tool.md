# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和低代码工作流等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证与端点。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速切换。

## 支持的模型/功能

百炼支持的模型能力因计费方案而异，**仅文本生成类模型**在 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版和 Coding Plan 中可用；图像、视频、语音、OCR 等多模态模型**仅支持按量计费**调用。常见模型包括：

- **Qwen3 系列**：`qwen3.8-max`（强推理）、`qwen3.8-flash`（高速响应）、`qwen3.7-plus`（均衡）、`qwen3.6-flash`（轻量）  
- **其他文本模型**：`glm-5.2`、`deepseek-v4.1-flash`、`deepseek-v4-pro` 等  
- **多模态模型**（按量计费专属）：`qwen-vl`、`qwen-omni`、`qwen-audio`、`wan2.6-t2i`、`wan2.6-v2v`  

> **注意**：[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 明确不支持 Token Plan 个人版、Token Plan 团队版和 Coding Plan，仅允许使用按量计费 API Key；违规使用将导致订阅暂停或 API Key 封禁。该限制在 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档中亦有重申。

思考模式（`enable_thinking`）为 Qwen3 系列核心能力，需在客户端配置中显式启用（如 `qwen-code` 的 `generationConfig.extra_body.enable_thinking: true` 或 `claude-code` 的 `CLAUDE_CODE_SUBAGENT_MODEL` 设置）。部分工具（如 `cherry-studio`）要求手动开启“思考模式”开关，否则报错 `The value of the enable_thinking parameter is restricted to True`。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| **API Key** | 方案专属密钥，不可跨方案复用 | `sk-xxx`（按量计费）、Token Plan 个人版专属 Key（见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)） |
| **Base URL** | 指定协议与地域的服务端点，必须与 API Key 方案及地域严格匹配 | OpenAI 协议：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 协议：<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| **Model ID** | 模型标识符，注意命名规范：`kimi-k2.6` → `kimi-k2-6`，`glm-5.2` → `glm-5-2`（见 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)） | `qwen3.8-max`、`wan2.6-t2i` |
| **WorkspaceId** | 按量计费必需，需从控制台获取并替换 URL 中的占位符（见 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)） | `ws-abc123xyz` |

## 使用方式

### 1. 客户端安装
- **CLI 工具**（如 `openclaw`、`hermes`、`qwen-code`）：依赖 Node.js ≥18，通过 `npm install -g` 或一键脚本安装  
- **桌面应用**（如 `cursor`、`cherry-studio`、`qoder`）：从官网下载安装包，启动后配置模型提供方  
- **IDE 插件**（如 `cline`、`qoder jetbrains`）：在 VS Code 或 JetBrains 市场搜索安装，通过设置界面填入凭证  
- **Web 平台**（如 `dify`、`qwenpaw`）：访问 Web 地址，登录后在模型设置页添加自定义端点  

### 2. 凭证配置
所有工具均需配置三要素：**API Key + Base URL + Model ID**。配置路径示例：
- `openclaw`：`~/.openclaw/openclaw.json`  
- `hermes`：`~/.hermes/config.yaml`  
- `cursor`：Settings > Models > OpenAI API Key + Override Base URL  
- `dify`：设置 > 模型供应商 > 通义千问插件（仅支持按量计费）  

> **注意**：`qwenpaw` 在配置按量计费时，基础 URL 下拉菜单默认为 China (Beijing)，需手动切换地域并替换 `{WorkspaceId}`（见 [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)）；而 `postman/curl` 调用图像 API 时，URL 中的 `{WorkspaceId}` 同样需手动替换（见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。

### 3. 高级能力启用
- **思考模式**：在 `qwen-code` 的 `settings.json` 中设置 `"enable_thinking": true`；在 `cline` 设置中勾选 **Enable R1 messages format**  
- **多模态输入**：`qwen-vl` 等模型需在 Dify LLM 节点打开 **视觉** 开关，并设置分辨率（见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）  
- **异步任务**：图像/视频生成必须使用异步流程（创建任务 → 轮询 `task_id`），不可直接同步请求（见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）  

## 限制和注意事项

- **方案隔离**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key 与 Base URL **完全不通用**。混用将导致 `401 Unauthorized`（见 [Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 和 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 常见问题）  
- **地域绑定**：按量计费的 API Key 必须与 Base URL 所属地域一致（如北京 Key 只能用于 `cn-beijing` URL），否则产生费用或认证失败（见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）  
- **模型兼容性**：`cursor` 免费版仅支持 Auto 模式，无法调用自定义模型；`qoder cn` 企业版不支持接入百炼（见 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 和 [Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)）  
- **禁止场景**：Token Plan/Coding Plan **严禁用于工作流平台（Dify/n8n）、API 测试工具（Postman）、或自定义后端调用**（见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)）  
- **免费额度**：新人免费额度仅限华北2（北京）地域，且按模型独立计算，不跨地域/模型共享（见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)


