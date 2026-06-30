# 函数调用

函数调用（Function Calling）是百炼平台大模型根据用户意图自主选择并调用外部工具（API）的能力：开发者通过结构化的工具描述把可调用接口暴露给模型，模型在对话中决定是否调用、调用哪个工具，并将返回结果合并到最终回复中，从而扩展大模型在获取最新信息、精确计算、图像处理等方面的边界。

## 在百炼平台的使用场景

百炼提供多条函数调用路径，按集成形态可分为三类：

- **智能体应用 / Assistant API**：大模型依据用户输入、工具名称与工具描述自主判断是否调用工具。需要调用时，模型选择合适工具，应用内部完成调用后把工具结果与用户内容合并再次输入模型，由模型生成最终结果；无需调用时直接输出。每个智能体应用最多添加 10 个工具，应用会根据输入选择调用一个或多个。
- **工作流应用**：插件作为工作流的一个节点，按用户编排的方式执行特定任务，而非由模型主动规划和调用，适合需要精确控制执行顺序的固定流程。
- **直接 API 调用**：在 OpenAI 兼容 Chat Completions、Anthropic 兼容 Messages、DashScope 原生接口以及 Qwen-Omni-Realtime 实时多模态接口中，均可按各自协议自定义工具并触发函数调用。Omni Realtime API 通过客户端事件 `response.create` 在工具调用回传结果后手动触发模型再次生成。

## 接口差异与工具能力

| 接口形态 | 函数调用支持 | 内置工具 |
| --- | --- | --- |
| OpenAI 兼容 Chat Completions | 支持自定义工具（function call） | 无，需自行实现 |
| OpenAI 兼容 Responses | 支持自定义工具 | 内置联网搜索、网页抓取、代码解释器、文搜图/图搜图等 |
| Anthropic 兼容 Messages | 支持工具调用 | 无内置工具 |
| DashScope 原生 | 功能集最完整，参数支持最丰富 | 需自行实现或通过插件协议接入 |
| Qwen-Omni-Realtime | 支持 Function Calling | 兼具联网搜索等能力 |

迁移时需注意：兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数；如需使用最全的采样参数、插件或业务字段，建议改用 DashScope 原生接口。联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力，其他接口不内置这些工具，需自行实现或通过工具调用协议接入。

## 插件与工具体系

百炼将函数调用所需的外部能力封装为插件（一个插件下可包含多个工具），分三类：

- **官方插件**：组件广场预置，无需配置输入输出参数即可调用，如 `code_interpreter`（Python 代码解释器）、`calculator`（计算器）、`text_to_image`（图片生成）、`quark_search`（夸克搜索）、`generate_qrcode`（生成二维码）、`github_search`（GitHub 搜索）。
- **三方插件**：涵盖商业服务、图像视频、学习教育等领域，开通后直接调用。
- **自定义插件**：当官方和三方无法满足需求时，用户可创建或从云市场导入，配置 API 路径、请求参数和返回数据，调试发布后即可在应用中被调用。

通过 Assistant API 调用工具时需正确传递工具 ID（在插件详情页"插件工具"下获取，例如 `calculator`）。子业务空间调用官方插件前，需先在插件详情页为子业务空间授权。

## Managed Agents API 中的工具执行

Managed Agents API 把函数调用纳入平台托管运行时：智能体配置中包含工具包与技能，Environment 资源定义工具调用的执行沙箱与预装依赖。会话运行期间，模型触发的工具调用在绑定环境的沙箱中执行；Session 处于 `running` 状态时，客户端可中断、审批工具调用或回填函数结果，再由模型继续生成。

## 关键参数与配置

- **模型选择**：推荐使用具备强工具调用能力的模型（如 `qwen-max` 系列）。插件调用目前支持 `qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`，各模型兼容性以控制台实际执行结果为准。
- **ReAct 最大轮次**：取值范围 1–50，限制单次会话中工具调用的最大次数，超出后自动退出工具调用链路并由智能体生成最终回复。
- **插件描述**：用自然语言描述插件功能与使用场景，帮助大模型判断是否调用，描述质量直接影响调用准确率。
- **预解析文件开关**：关闭时文件 URL 作为上下文传递，由智能体决策是否调用工具；开启时由预置解析器处理文档、图像、视频、音频。千问-VL 系列模型具备多模态能力，即使关闭预解析也能直接解析图片和视频。
- **对话历史**：仅 Responses 接口自动管理历史，其他接口需由调用方维护上下文，避免超出模型上下文窗口。

## 注意事项

- 三方直供模型仅在中国站的中国内地地域可用，调用前需先在百炼控制台开通对应服务。Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。
- 首次访问插件页面需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 子账号会因缺少 `ram:CreateServiceLinkedRole` 权限报错（错误码 140052），需先由主账号创建并授予对应自定义权限策略。
- Python 代码解释器不支持对外访问网络以及上传本地文件；夸克搜索插件仅支持检索网页标题、关键词和摘要，不支持直接访问网页详情。
- Token Plan / Coding Plan 套餐仅限在兼容的 AI 编程和智能体工具中交互式使用，禁止用于自动化脚本、应用后端或非交互式批量调用，违规可能导致订阅暂停或 API Key 封禁。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [token plan guide](../guides/token-plan-guide.md)
- [managed agents api](../api/managed-agents-api.md)


