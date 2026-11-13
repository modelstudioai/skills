# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、并按需调用外部工具或服务的核心能力。它使模型不再局限于文本生成，而是能动态触发真实世界操作（如查天气、搜网页、解析文件），实现“思考—决策—执行”闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中**不作为独立 API 功能开放**，而是深度集成于以下两类运行时环境，由平台自动编排：

- **智能体（Agent）应用**：  
  - 在 `Managed Agent` 和 `Flow Agent` 中，函数调用通过 `tools` 参数（或 Flow 中的 `nodes[].tool_id`）显式声明可用工具列表；模型根据用户输入和工具 `description` 自动选择并构造结构化调用请求（JSON Schema 格式），平台负责路由、执行、结果注入上下文并生成最终响应。  
  - **注意**：纯千问系列模型 API（如 `/v2/app/completions`）**不支持函数调用**；该能力仅在 Agent 框架下生效。

- **Agent Store 扩展能力**：  
  - 函数调用的实际载体是 **MCP（Model Context Protocol）服务** 和 **Skill（技能包）**。  
    - MCP 服务提供标准化工具接口（如 `web_search`, `maps_weather`），支持远程 HTTP/SSE/stdio 协议，适用于通用 API 集成；  
    - Skill 提供文件与结构化数据处理能力（如 `pdf`, `xlsx`），以 ZIP 包形式封装逻辑，适用于文档解析类任务。  
  - 二者均需在 Agent 配置中启用，并通过 `tools` 字段引用其唯一 ID（如 `"web_search"` 或 `"pdf"`），模型据此生成符合其 Schema 的调用参数。

> ⚠️ 重要限制：  
> - Assistant API 当前**不支持连续调用多个本地函数**；  
> - **不支持 memory 配置功能**（即无法在函数调用链中自动维护会话状态）；  
> - MCP/Skill **不可用于纯模型 API 调用场景**，仅限 Agent 或工作流应用内使用。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `tools` | array of objects | 声明当前 Agent 允许调用的工具列表，每个对象包含 `type`（`mcp` 或 `skill`）、`name`（工具唯一 ID）及可选 `description`（覆盖默认描述，用于提升调用准确率） | 是（Agent 场景） |
| `model_id` | string | 必须选用支持函数调用的模型，如 `qwen-max`、`qwen-plus`、`qwen3.5-flash` 等（`qwen3-vl-plus` 暂不支持） | 是 |
| `enable_memory` | boolean | 控制是否启用会话记忆。**即使设为 `true`，函数调用过程中的中间状态也不会被自动缓存或复用**（平台当前不支持 memory 配置） | 否（但建议设为 `false` 避免误解） |
| `timeout_ms` | integer | 全局执行超时（含函数调用+模型推理）。Managed/Flow Agent 默认 30000ms，Sandbox 最高支持 60000ms；超时将中断调用并返回错误 | 否（使用默认值即可，高延迟工具建议显式设置） |

- **工具定义关键字段（MCP/Skill 配置时）**：  
  - `name`：全局唯一标识符，调用时直接引用（如 `"web_search"`）；  
  - `description`：**必须清晰描述输入格式、支持动作、触发关键词及边界条件**（例如：“仅支持中文城市名查询，不支持未来日期”），直接影响模型调用准确率；  
  - `parameters`（MCP）或 `schema`（Skill）：定义 JSON Schema，约束传入参数类型与必填项，平台在调用前校验合法性。

## 面向开发者，简洁实用

- ✅ **正确做法**：  
  - 在控制台创建 Managed/Flow Agent → 在「技能」区域添加 MCP 或 Skill → 在 API 请求中传入 `tools: [{"type": "mcp", "name": "web_search"}]`；  
  - 使用 CLI 快速测试：`bl mcp call --target web_search --query "杭州天气"`（验证 MCP 服务本身）；  
  - 通过 `enable_tracing: true` 开启 Trace，查看函数调用是否被触发、耗时及返回内容。

- ❌ **避免踩坑**：  
  - 不要在 `/v2/app/completions` 等模型直连 API 中尝试 `functions` 参数——该字段被忽略且无报错；  
  - 不要依赖 `enable_memory` 实现多步函数协作——需自行在 Skill/MCP 逻辑中管理状态或改用 Flow Agent 显式编排；  
  - 不要省略 `description` 或写模糊描述（如“搜索信息”），否则模型大概率跳过调用或传参错误。

- 💡 **调试提示**：  
  - 若函数未被调用：检查 `tools` 中 `name` 是否与 Agent Store 中注册的完全一致（大小写敏感）；  
  - 若调用失败：查看 Trace 日志中的 `tool_call` 事件，确认模型生成的 `function.name` 和 `arguments` 是否合法；  
  - Token 成本：每次函数调用的输入参数 + 返回结果均计入总 Token，复杂工具需预估开销。

## 关联主题页

- [support](../guides/support.md)
- [agent store](../guides/agent-store.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent development](../guides/agent-development.md)


