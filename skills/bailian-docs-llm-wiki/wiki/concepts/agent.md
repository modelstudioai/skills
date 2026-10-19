# 智能体（Agent）

智能体（Agent）是百炼平台中具备自主规划、工具调用、状态管理与多步推理能力的可执行 AI 应用单元。它不仅响应用户输入，还能在沙箱环境中主动调用工具、读写文件、执行代码、访问记忆库，并支持中断续接与跨会话上下文保持。

## 在百炼平台的不同场景中，这个概念如何使用

- **托管型智能体（Managed Agents）**：这是百炼推荐的现代 Agent 范式，适用于需长期运行、多步协作、状态持久化的复杂任务（如数据分析、自动化报告生成、多模态内容处理）。平台自动托管会话状态、沙箱环境、工具执行生命周期和事件历史，开发者只需定义行为逻辑，无需运维底层资源。

- **API 调用入口（Application Call）**：已发布的智能体可作为服务被外部系统通过 `application call` API 同步或异步调用。支持[流式输出](streaming.md)、多模态输入（图像/文件）、长期记忆（`memory_id`）、RAG 检索（`rag_options`）及思考过程透出（`enable_thinking=true`），是构建生产级 AI 应用的核心集成方式。

- **场景化落地（Use Cases）**：智能体常作为高阶能力载体嵌入典型工作流——例如结合 RAG 构建知识助手、接入 Realtime 模型实现语音交互闭环、或多智能体编队完成提案生成与校验。其灵活性使其成为连接 Prompt 工程、模型服务、工具生态与业务逻辑的关键抽象层。

## 关键参数和配置

| 类别 | 参数名 | 说明 | 是否必填 | 备注 |
|--------|---------|------|-----------|------|
| **Agent 定义** | `name` | 智能体名称，用于控制台识别 | 是 | 字符串，长度 ≤64 |
| | `model.id` | 所用大模型 ID（如 `qwen3.8-max`） | 是 | 决定基础推理与多模态能力；仅 `qwen3.8-max` 和 `auto` 明确支持图片识别 |
| | `system` | 系统提示词，定义角色、约束与能力边界 | 否（但强烈建议） | 影响工具调用准确性与行为一致性 |
| | `tools` | 启用的内置或 MCP 工具列表 | 否（无工具则为纯 LLM） | 每个工具必须在 `configs[]` 中显式启用 `enabled: true`，否则不可用 |
| **环境配置** | `environment.config.type` | 沙箱类型：`"cloud"`（托管）或 `"sandbox"`（独立） | 是（若需工具执行） | `"cloud"` 使用百炼统一托管沙箱；`"sandbox"` 可选 `code-interpreter-v1`/`browser`/`all-in-one` 镜像 |
| | `environment.config.packages` | 运行时依赖（`apt`/`pip`/`npm` 格式） | 否 | 如需 `pandas` 或 `playwright`，需在此声明 |
| | `environment.config.networking.type` | 网络策略：`"unrestricted"`（默认）或 `"blocked"` | 否 | 外部调用（如 `web_search`）需设为 `unrestricted` |
| **会话控制** | `session_id`（DashScope） | 对话唯一标识，1 小时空闲自动失效 | 否 | 用于延续上下文；若传 `messages`，则优先级高于 `session_id` |
| | `memory_id`（Application Call） | 挂载的长期记忆库 ID | 否 | 仅智能体应用支持，用于跨会话状态共享 |
| | `tools[].configs[].permission_policy.type` | 工具调用审批策略 | 否 | `"always_allow"`（自动执行）或 `"always_ask"`（需人工确认）；仅主智能体生效 |

> ⚠️ 注意：  
> - 模型能力以控制台实时支持列表为准，文档中关于 `qwen3.7-plus` 的多模态描述存在不一致，实际使用前请验证；  
> - 所有 API 调用均受地域限制（默认华北2 北京），跨地域需显式指定 `X-DashScope-WorkSpace` Header；  
> - 工具启用必须双重声明：既在 `tools[]` 列表中声明，又在对应 `configs[].enabled: true`，缺一不可。

## 面向开发者，简洁实用

- ✅ **起步最快**：在控制台「智能体开发」页 → 创建 Agent → 选择 `qwen3.8-max` + 启用 `bash`/`read`/`write` 工具 → 发布 → 用 `application call` API 调用即可跑通首个带文件处理的 Agent。  
- ✅ **调试关键**：开启 `enable_thinking=true` 查看完整推理链；搭配 `stream=true` 实时观察工具调用与结果注入过程。  
- ✅ **生产就绪**：用 `Skill` 封装高频流程（如“PDF 解析→摘要→表格提取”），版本化复用；用 `Memory Store` 实现用户画像/项目上下文持久化；用 `MCP` 接入自建数据库或业务系统。  
- ❌ **避坑提醒**：勿混淆 `session_id`（短期对话）与 `memory_id`（长期记忆）；勿遗漏 `tools[].configs[].enabled` 导致工具静默失效；勿在非北京地域省略 `X-DashScope-WorkSpace` Header。

## 关联主题页

- [agent development](../guides/agent-development.md)
- [application call](../api/application-call.md)
- [use cases](../guides/use-cases.md)


