# 应用调用方式对比

阿里云百炼的应用（智能体应用、[工作流](../concepts/workflow.md)应用、新版智能体 Agent 2.0）可通过 API 集成到业务系统中。官方文档中存在两篇高度相关的主题页：一篇偏 **API 参考**（`application call`），重点介绍两套调用 API（OpenAI 兼容 Responses API 与 DashScope 原生 `/completion`）的端点、参数与同步/异步模式；另一篇偏 **使用指南**（`bailian application calling`），重点介绍通过 DashScope SDK / HTTP 调用智能体与[工作流](../concepts/workflow.md)应用的实操步骤、多轮对话与自定义参数透传。本文对两者做维度对比，帮助开发者在技术选型时快速定位所需信息。

## 关键维度对比

| 维度 | [application call](../api/application-call.md)（API 参考） | bailian [application call](../api/application-call.md)ing（使用指南） |
| --- | --- | --- |
| 文档定位 | API 参考，强调端点、参数、调用模式 | 使用指南，强调 SDK 实操与场景示例 |
| 所属分类 | api | guides |
| 覆盖的 API 模式 | 两套：OpenAI 兼容 Responses API + DashScope 原生 `/completion` | 一套：DashScope 原生 `/completion`（`Application.call` / `POST /apps/{app_id}/completion`） |
| 主 Endpoint | `POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（OpenAI 兼容）<br>`POST /api/v1/apps/{APP_ID}/completion`（DashScope 原生） | `POST /api/v1/apps/{APP_ID}/completion` |
| SDK 推荐 | OpenAI 兼容模式用 OpenAI SDK；DashScope 原生模式用 DashScope SDK | DashScope SDK（Python / Java），Node.js 用 `axios` |
| 支持应用类型 | 智能体、[工作流](../concepts/workflow.md)、新版智能体 Agent 2.0 | 智能体应用、工作流应用（智能体编排应用已被工作流应用替代） |
| 输入格式 | `input` 为 string 或 messages 数组；多模态支持 `input_text` / `input_image` / `input_file` | `input.prompt` 字符串 或 自行管理 `messages` 数组 |
| 多轮对话 | 通过 messages 数组传递完整对话历史；`pre_response_id` / `conversation_id` 上下文后续支持 | 两种方式：`session_id`（云端托管，1 小时 / 50 轮）或自行管理 `messages`（推荐） |
| 同步/异步 | 支持 `stream` 流式、`background` 异步；异步暂不支持流式 | 默认同步；多轮对话通过 `session_id` 或 `messages` 实现 |
| 多模态 | 显式支持图像、文件（`input_image` / `input_file`，文件仅智能体应用支持） | 未专门展开 |
| 自定义参数透传 | 未展开 | 支持 `biz_params.user_defined_params` 透传业务参数到自定义插件 / 工作流插件节点 |
| 业务空间 | 明确说明子业务空间需 Workspace ID，多地域 Base URL 含 Workspace ID | 提及业务空间对插件与应用关联的约束（同一业务空间内） |
| 地域说明 | 明确给出华北2（北京）默认 Endpoint，并列出德国、新加坡、日本等地域需带 Workspace ID | 未专门说明地域差异 |
| 典型代码示例 | Python（OpenAI SDK 同步多轮） | Python / Java / Node.js / curl（基础调用） |
| 凭证准备 | APP ID + Workspace ID + API Key + SDK | API Key + APP_ID + DashScope SDK |

## 适用场景建议

- **选 `application call`（API 参考）**：当你需要复用现有 OpenAI 生态代码库与工具链；需要使用[流式输出](../concepts/streaming-output.md)或异步执行；需要调用新版智能体 Agent 2.0；需要多模态输入（图像、文件）；或部署在非北京地域需要明确 Workspace ID 与 Base URL 拼接规则时。
- **选 `bailian application calling`（使用指南）**：当你首次接入百炼应用、需要 Python / Java / curl 的最小可运行示例；需要通过 `session_id` 实现云端托管多轮对话；需要向自定义插件或工作流插件节点透传业务参数（`biz_params.user_defined_params`）；或团队已习惯使用 DashScope SDK 时。

## 技术选型参考

两篇文档并非互斥，而是互补：`application call` 给出"调哪套 API、用什么端点、传哪些字段"的契约层信息，`bailian application calling` 给出"用哪个 SDK、怎么写代码、怎么传业务参数"的实操层信息。建议的选型路径：

1. 先读 `application call` 确定调用模式（OpenAI 兼容 vs DashScope 原生），明确端点与参数契约；
2. 若选择 DashScope 原生 `/completion`，再读 `bailian application calling` 获取多语言 SDK 示例与多轮、自定义参数等进阶能力；
3. 若选择 OpenAI 兼容 Responses API，则以 `application call` 为主，参考 OpenAI SDK 既有用法，`bailian application calling` 中的 `session_id` / `biz_params` 等能力在该模式下暂不适用。

> 注：两篇文档对应用类型的命名略有差异（"新版智能体 Agent 2.0" vs "智能体编排应用已被工作流应用替代"），接入前请以控制台实际应用类型与最新 API 参考为准。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


