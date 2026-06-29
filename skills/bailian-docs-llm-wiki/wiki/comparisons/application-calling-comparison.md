# 应用调用方式对比（API 调用 vs 百炼应用调用）

百炼平台把控制台编排好的应用（智能体、工作流、新版智能体 Agent 2.0）集成到业务系统时，主要有两条调用路径：一是面向 OpenAI 生态的 **OpenAI 兼容 Responses API**（同步/异步、流式、[多模态](../concepts/multimodal.md)），二是面向百炼原生的 **DashScope API**（`/apps/{APP_ID}/completion`，配合 DashScope SDK）。两者都能触发同一个应用，区别在于接口形态、SDK 选型、可复用的生态与可用的高级能力。本文面向开发者做技术选型参考，对比两种方式的关键维度与适用场景。

## 关键维度对比

| 维度 | OpenAI 兼容模式（Responses API） | DashScope 原生模式（Application.call / completion） |
| --- | --- | --- |
| API 端点 | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` |
| SDK 选型 | OpenAI SDK（Python 等） | DashScope SDK（Python / Java）、Node.js 用 axios 等 HTTP 客户端 |
| base_url 配置 | `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1` | 直连 `/api/v1/apps/{APP_ID}/completion` |
| 输入格式 | `input` 为字符串（单轮）或消息数组（多轮/[多模态](../concepts/multimodal.md)），消息 `role` 取 `system`/`user`/`assistant` | `input.prompt`（单轮）或自行维护 `messages`（多轮）；外层包 `input`/`parameters`/`debug` |
| 多轮对话 | 每次请求传完整对话历史（基于 `pre_response_id`/`conversation_id` 的上下文能力后续支持） | 两种方式：`session_id`（云端托管，1 小时有效、最多 50 轮）或自行管理 `messages`（推荐，更灵活）；同时传时优先 `messages` |
| [流式输出](../concepts/streaming-output.md) | 设置 `stream=True`，工作流应用需在结束/流程输出节点启用「[流式输出](../concepts/streaming-output.md)」并重新发布 | 由 DashScope SDK / HTTP 的 streaming 能力提供，按应用类型与节点配置启用 |
| 异步执行 | `background=true` 走异步调用（异步暂不支持流式） | 主要为同步 `Application.call`；异步能力由 Responses API 侧覆盖 |
| [多模态](../concepts/multimodal.md) | `content` 数组支持 `input_text`/`input_image`/`input_file`（文件仅智能体应用支持）；智能体图像输入需选通义千问 VL 系列并设「自定义处理」 | 由应用内部编排与所选模型决定，能力随 DashScope 应用类型提供 |
| 支持应用类型 | 智能体、工作流、新版智能体 Agent 2.0 | 智能体应用、工作流应用（智能体编排应用已被工作流应用替代），二者调用接口一致 |
| 自定义参数透传 | 通过 OpenAI 兼容字段传递，按 Responses API 字段约定 | `biz_params.user_defined_params` 透传业务参数，用于智能体自定义插件与工作流插件节点 |
| 响应结构 | OpenAI Responses 格式（`output` 等字段） | 统一 `{"output": {"finish_reason","session_id","text"}, "usage": {...}, "request_id": "..."}`，主要消费 `output.text` |
| 生态复用 | 直接复用现有 OpenAI 代码库与工具链 | 更全面的功能与更高的性能；与百炼原生 SDK/工具链深度集成 |
| 业务空间 | 默认空间仅需 APP ID；子空间或海外地域需在请求中带 Workspace ID（为对应地域 Base URL 组成部分） | 子业务空间需 Workspace ID；`bl`/控制台获取 APP ID 与 Workspace ID，不支持 API/CLI 查询 |

## 凭证与前置准备（两者共通）

无论选哪种方式，都需要：

1. **API Key**：在百炼控制台密钥管理页面创建，推荐写入 `DASHSCOPE_API_KEY` 环境变量，避免硬编码。
2. **应用 ID（APP_ID）**：从应用管理页面应用卡片复制；子业务空间还需 Workspace ID。
3. **SDK（按需）**：OpenAI 兼容模式装 OpenAI SDK；DashScope 原生模式装对应语言 DashScope SDK（Java 建议 >= 2.12.0），HTTP 调用可跳过。

> RAM 子账号默认只能查看其已加入业务空间的 ID；查询主账号下全部业务空间需主账号或被授予 `AliyunBailianFullAccess`/`AliyunBailianControlFullAccess` 权限。

## 适用场景建议

- **选 OpenAI 兼容 Responses API**：
  - 已有成熟 OpenAI SDK 代码库或工具链，希望最小改造成本接入百炼应用。
  - 需要同步/异步、流式、多模态（文本+图像+文件）输入组合。
  - 希望在多语言/多框架间保持与 OpenAI 接口一致的调用习惯。
  - 需要异步执行（`background`）的实时交互场景。

- **选 DashScope 原生 API（Application.call / completion）**：
  - 需要更全面的功能与更高的性能，或要使用百炼原生 SDK 的高级能力。
  - 多轮对话希望由云端托管 `session_id`，简化历史管理。
  - 需要通过 `biz_params.user_defined_params` 透传业务参数到自定义插件/插件节点。
  - 团队主力语言为 Java，倾向使用官方 DashScope Java SDK。
  - 调用工作流应用并依赖其节点编排逻辑与扩展能力。

## 技术选型小结

两条路径调用的是同一个百炼应用，选型本质是「接口形态与生态」的取舍：追求 OpenAI 生态复用与多模态/异步组合选 Responses API；追求百炼原生能力、`session_id` 托管多轮、`biz_params` 透传与 Java SDK 选 DashScope 原生 API。两者凭证（API Key、APP_ID、Workspace ID）与控制台侧应用配置通用，可在业务演进中按需切换或并存。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


