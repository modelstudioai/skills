# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和工作流系统等场景。开发者可根据使用习惯选择合适工具，并按计费方案（Token Plan 个人版/团队版、Coding Plan 或按量计费）配置对应 API Key 与 Base URL。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速切换。

## 支持的模型/功能

百炼支持的模型能力因接入方案而异，**并非所有模型在所有工具中均可用**：

- **Token Plan 个人版/团队版**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro`），不支持图像/视频/语音/OCR 等多模态模型；[Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 列出了完整清单。
- **Coding Plan**：仅支持 `qwen3.7-plus` 及其变体（如 `qwen3.6-plus`），不支持 `qwen3.8-*` 系列或第三方模型；详见 [Coding Plan 支持的模型](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。
- **按量计费**：支持最全模型集，包括文生图（`wan2.6-t2i`）、文生视频（`wan2.1-v2v`）、视觉理解（`qwen-vl`、`qvq`）、语音（`qwen-audio`）、OCR（`qwen-vl-ocr`）等；但需注意 Dify 等工作流平台**不支持 Token Plan/Coding Plan 套餐**，必须使用按量计费 API Key —— 此限制明确记载于 [Dify 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 中。
- **千问 APP 工作助理**：仅支持 Token Plan（个人版/团队版），且**不支持按量计费或 Coding Plan**；可用模型限于 `Qwen3.8-Max`、`Qwen3.8-Flash` 等 5 款 Qwen 系列文本模型，详见 [千问文档](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。

> **注意**：部分文档存在模型兼容性矛盾。例如，[OpenClaw 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 的配置示例中列出了 `qwen3.8-flash`（支持 image 输入），但 [千问 APP 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md) 明确声明其仅支持“文本生成模型”，且未列出任何带图像输入能力的型号。实际使用时请以各工具官方支持列表为准，避免依赖配置文件中的非功能性字段。

## 关键参数

所有工具均需配置以下三类核心参数，但协议与路径细节存在差异：

| 参数 | OpenAI 兼容协议 | Anthropic 兼容协议 | 说明 |
|------|------------------|------------------------|------|
| **API Key** | 各方案专属密钥，不可混用（如 Token Plan 个人版 Key 不能用于 Coding Plan） | 同左 | 必须与 Base URL 所属方案严格匹配；[更多错误排查见此文档](../../raw/model-api-reference/preparations/error-code.md) |
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/v1`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（按量） | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量） | 地域必须一致：按量计费的 `WorkspaceId` 需与 API Key 所属地域匹配；Token Plan/Coding Plan 的 URL 是固定地址，无地域变量 |
| **Model ID** | `qwen3.8-max`、`glm-5-3`（注意：Cursor 要求将 `glm-5.3` 写为 `glm-5-3`） | `qwen3.8-max`、`auto`（Anthropic 协议下 `auto` 为有效值） | 模型命名需严格匹配文档规范；部分工具（如 Cursor、Cherry Studio）要求对含点号的模型名做连字符转换 |

此外，部分工具需额外启用特性：
- 思考模式（Reasoning）：Qwen3 系列模型需显式设置 `enable_thinking: true`（如 [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)）或 `effort: "xhigh"`（如 [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)）；
- 异步任务：图像/视频生成必须使用异步流程（创建任务 + 轮询查询），详见 [Postman/cURL 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 使用方式

### 安装与初始化
- **CLI 工具**（如 `claude-code`、`qwen`、`kilo`、`hermes`）：统一要求 Node.js ≥ v18（部分如 OpenClaw 需 v22.19.0+），通过 `npm install -g <pkg>` 安装；
- **桌面应用**（如 Cursor、Cherry Studio、Qoder CN）：从官网下载安装包，无需本地运行时依赖；
- **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains IDE 扩展市场中搜索安装；
- **Web 平台**（如 Dify、QwenPaw）：通过浏览器访问，后端部署可选。

### 配置流程（通用步骤）
1. **获取凭证**：根据所选方案，在 [百炼控制台](https://bailian.console.aliyun.com/) 对应页面获取 API Key（Token Plan 个人版 → `/subscription/overview`；Coding Plan → `/subscription/coding-plan`；按量 → `/preparations/get-api-key.md`）；
2. **填写 Base URL**：严格按方案选择 OpenAI 或 Anthropic 协议的 URL（参见上表），**切勿混用**；
3. **指定模型**：从该方案支持的模型列表中选择 ID（注意命名规范）；
4. **验证连接**：发送测试请求（如 `"你好"`），确认返回非空响应。

> **注意**：[Dify 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 明确指出其**不支持 Token Plan/Coding Plan**，仅允许按量计费 API Key。若误用其他套餐 Key，将触发违规检测并可能导致订阅暂停。

## 限制和注意事项

- **套餐适用范围严格隔离**：Token Plan 个人版/团队版、Coding Plan 仅限 AI 编程工具（如 Claude Code、Qwen Code、Cursor）和 Agent 类工具（如 OpenClaw、QwenPaw）；**工作流平台（Dify、n8n、Coze）、API 测试工具（Postman、cURL）、自定义后端调用均被禁止** —— 此政策在 [更多工具文档](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中有强制声明；
- **地域绑定**：按量计费的 API Key 与 `WorkspaceId` 必须同地域（北京/新加坡/弗吉尼亚），跨地域调用将失败且不计入免费额度；
- **免费额度限制**：新人免费额度**仅适用于华北2（北京）地域的按量计费模型**，Token Plan/Coding Plan 无免费额度，且各模型额度独立不共享；
- **模型能力差异**：同一模型 ID 在不同协议下行为可能不同（如 `qwen3.8-max` 在 Anthropic 协议下支持 `thinkingFormat: "openai"`，在 OpenAI 协议下需通过 `extra_body.enable_thinking` 控制），务必查阅对应工具的配置示例；
- **错误处理**：HTTP 401 表示 Key/URL 不匹配；HTTP 400 `InvalidParameter` 常因未启用思考模式（如 [Cline 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 所述）；异步任务超时需检查 `task_id` 有效期（24 小时）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
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
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)


