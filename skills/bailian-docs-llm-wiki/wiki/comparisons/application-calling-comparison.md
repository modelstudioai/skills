# 应用调用方式对比：API 直调与百炼应用调用

阿里云百炼平台为已编排好的应用（智能体、工作流、新版智能体 Agent 2.0）提供两套对外调用路径：一是面向 OpenAI 生态的 **Responses API（OpenAI 兼容模式）**，二是面向百炼原生的 **DashScope `Application.call` / `/completion` API**。两者底层均指向同一个 `APP_ID`，但在端点形态、SDK 选型、输入结构、多轮与多模态能力、扩展参数等方面存在差异。本文从技术选型视角对比两种方式，帮助开发者根据现有技术栈与功能需求做出取舍。

## 关键维度对比

| 维度 | OpenAI 兼容 Responses API（API 直调） | DashScope 原生 API（百炼应用调用） |
| --- | --- | --- |
| 调用端点 | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` |
| SDK 选型 | OpenAI SDK（多语言） | DashScope SDK（Python / Java），或直接 HTTP |
| base_url 配置 | `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1` | 无需 base_url，SDK 内置或直接 POST |
| 输入格式 | `input` 为字符串或消息数组，`role` 取 `system`/`user`/`assistant`，多模态 `content` 为数组（`input_text`/`input_image`/`input_file`） | `input.prompt` 字符串，或 `messages` 数组（自行管理多轮历史） |
| 输出格式 | OpenAI Responses 结构，`response.output` 等 | `{"output": {"finish_reason","session_id","text"}, "usage":{...}, "request_id":"..."}`，业务侧消费 `output.text` |
| 支持模型 | 智能体、工作流、新版智能体 Agent 2.0 | 智能体应用、工作流应用（[智能体编排](../concepts/agent-orchestration.md)应用已被工作流应用替代） |
| 同步/异步 | 支持 `background` 异步执行，同步默认；流式 `stream=true` | 主要为同步调用，`session_id` 由云端管理历史 |
| [流式输出](../concepts/streaming-output.md) | 支持（`stream=true`），异步暂不支持流式 | 通过 SDK / HTTP 支持（详见调用文档） |
| 多轮对话 | 传递完整 `input` 消息数组；基于 `pre_response_id`/`conversation_id` 的上下文能力后续支持 | 两种方式：`session_id`（云端托管，1 小时有效、最多 50 轮）或自行维护 `messages`（推荐，更灵活） |
| 多模态 | 原生支持文本、图像、文件（`input_file` 仅智能体应用支持） | 通过 `messages` 与应用内编排支持 |
| 自定义参数透传 | 通过 `input`/应用编排间接实现 | `biz_params.user_defined_params` 透传至自定义插件与工作流插件节点 |
| 业务空间 | 默认空间仅需 APP ID；子空间或海外地域需在请求中包含 Workspace ID | 同样需要 APP_ID；子空间按地域 Base URL 处理 |
| 典型场景 | 复用现有 OpenAI 代码库与工具链、多模态交互、统一 OpenAI 协议接入 | 全面功能与更高性能、自定义插件参数透传、Java/Node.js 直接 HTTP 集成 |

## 适用场景建议

**OpenAI 兼容 Responses API 适合：**

- 已有 OpenAI SDK 代码资产、希望以最小改动接入百炼应用的团队。
- 需要多模态输入（文本 + 图像 + 文件）的智能体交互场景。
- 希望统一在 OpenAI 协议生态下做模型/应用切换、保持代码中立。
- 需要异步执行（`background`）与[流式输出](../concepts/streaming-output.md)能力的实时或长任务交互。

**DashScope 原生 `/completion` API 适合：**

- 追求更全面功能与更高性能，使用百炼原生能力（如自定义插件参数透传 `biz_params`）。
- Java/Node.js 项目希望直接以 HTTP 方式集成，不引入 OpenAI SDK 依赖。
- 工作流应用需要通过 `session_id` 让云端托管对话历史，简化多轮实现。
- 需要在工作流大模型节点中配合 `historyList` 变量精细控制提示词与上下文。

## 技术选型建议

1. **优先看协议生态**：若团队代码栈已围绕 OpenAI SDK 构建（含观测、重试、流式解析），选 Responses API 可降低迁移与维护成本；若以阿里云/DashScope 体系为主，选原生 API 更顺。
2. **看扩展能力**：自定义插件参数透传（`biz_params.user_defined_params`）目前是原生 API 的明确能力，需要此能力的场景应选原生 API。
3. **看多轮管理偏好**：希望云端托管历史、降低客户端状态复杂度，用原生 API 的 `session_id`；希望完全自控历史与上下文，两套 API 都支持 `messages` 数组方式。
4. **看多模态需求**：图像、文件等多模态输入在 Responses API 中有标准化的 `content` 数组结构，接入更直接；原生 API 需结合应用编排实现。
5. **看地域与业务空间**：两套 API 均支持默认空间仅凭 APP ID 调用；子业务空间或海外地域需携带 Workspace ID，选型不影响该约束，但需在请求中正确拼装。
6. **凭证一致**：两套方式都使用同一份 `DASHSCOPE_API_KEY`，无需为不同调用方式分别管理密钥，切换成本主要在 SDK 与请求结构层面。

综上，两种方式并非互斥：同一 `APP_ID` 可同时被两套 API 调用，团队可按业务模块分别选型——面向外部生态集成用 Responses API，面向内部能力扩展用原生 API。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


