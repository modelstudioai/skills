# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台用于标准化接入外部动态服务能力的轻量级协议规范。它定义了一套统一的工具描述、调用契约与响应格式，使大模型能在推理过程中安全、可预测地调用实时 API（如天气、地图、搜索等），并将返回结果作为上下文注入后续生成过程。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent Store 中作为能力货架的核心组件**：MCP 服务与 Skill 并列构成 `agent store` 的两大能力类型。MCP 专用于**实时、在线、状态无关的外部 API 调用**（例如 `WebSearch` 获取最新网页结果、`Amap Maps` 查询实时路径），由模型根据用户意图自动决策触发；不支持文件处理或本地计算。
  
- **智能体应用（Managed Agent）中自动调度**：在配置智能体时，最多可添加 5 个 MCP 服务。模型基于 `name` 和 `description` 自动匹配调用时机，无需显式编写工具选择逻辑；返回结果直接拼接进 prompt 上下文，影响后续生成。

- **工作流应用（Flow Agent）中手动编排**：MCP 以独立节点形式存在，开发者需在可视化画布中拖入 MCP 节点，并手动绑定输入参数（如 `city: "北京"`）、设置超时与重试策略，实现确定性、可调试的工具链路。

- **外部系统集成**：通过 MCP SDK（如 `streamablehttp_client`）或一键导出至 Cherry Studio/Cursor，可在自有项目中复用百炼托管的 MCP 服务，无需重复对接第三方 API。

> ⚠️ 注意：MCP 不是通用 API 网关，也不替代 RAG 或 Skill——它不处理静态文件（PDF/Excel）、不缓存历史数据、不执行沙箱代码，仅专注「一次调用、一次响应、即时注入」的上下文增强。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `DASHSCOPE_API_KEY` | string | 所有官方及自定义 MCP 服务的统一鉴权凭证，全局生效，无需为每个服务单独申请密钥。 | 是（平台侧自动注入） |
| `deploymentMode` | `"basic"` \| `"ultra"` | 部署模式：<br>• `basic`：按调用时长计费（0.000156 元/秒），适合低频、偶发调用；<br>• `ultra`：预付费部署 + 低单价调用（0.000036 元/秒），适合高并发、亚秒级延迟敏感场景。 | 否（默认 `basic`） |
| `tool_choice`（API 层） | `"auto"` \| `"none"` \| `string` | 控制 MCP 调用策略：<br>• `"auto"`（默认）：由模型自主判断是否及调用哪个 MCP；<br>• `"none"`：禁用所有 MCP；<br>• `"web_search"`：强制调用指定 MCP 服务。 | 否（仅在 Agent API 中生效） |
| `timeout_seconds`（自定义 MCP） | integer | 自定义 MCP 服务的单次调用超时时间，范围 `1–30` 秒，默认 `10`。超时后返回错误，不重试。 | 否（仅自定义 MCP 可配） |

> 💡 提示：MCP 服务本身无 `parameters` Schema 字段（区别于通用 tool calling），其输入参数由服务定义固定（如 `WebSearch` 固定接受 `query` 字符串），开发者只需在 Flow Agent 中填值，或依赖模型从对话中提取。

## 面向开发者，简洁实用

- ✅ **快速启用**：在控制台「Agent Store → MCP 服务」中勾选官方服务（如 `WebSearch`），保存即生效，无需写一行代码。
- ✅ **自定义接入三步走**：① 编写符合 [MCP 协议](https://modelcontextprotocol.io/) 的 HTTP 服务（返回 `200 OK` + JSON 响应）；② 使用 `npx @modelcontextprotocol/cli deploy` 托管至函数计算；③ 在 Agent Store 中导入，填写名称与描述。
- ✅ **调试建议**：开启 `stream=true` 调用 Agent API，观察 `event: tool_calls` 流事件中的 `name` 和 `arguments`，验证模型是否正确解析用户意图并构造参数。
- ❌ **避坑提醒**：
  - 不要将需访问 VPC 内资源的自定义 MCP 直接部署（需先打通 VPC 或配置白名单）；
  - 敏感参数（如第三方 API Key）必须通过 KMS 加密凭据注入，禁止明文写死；
  - MCP 返回内容计入模型输入 Token，长响应会显著增加成本，建议服务端做精简裁剪（如只返回前 3 条搜索结果）。

## 关联主题页

- [agent store](../guides/agent-store.md)
- [agent api start using](../api/agent-api-start-using.md)
- [managed agents api](../api/managed-agents-api.md)
- [get started with agents](../guides/get-started-with-agents.md)


