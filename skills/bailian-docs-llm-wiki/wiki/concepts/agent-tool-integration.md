# 智能体工具集成

智能体工具集成是指在百炼平台中，将外部能力（如 API 服务、数据处理逻辑、专业 SDK）以标准化方式接入智能体执行流程，使其能够按需调用、组合并协同完成复杂任务的能力。该机制是智能体从“纯语言推理”迈向“真实世界行动”的核心支撑。

## 在百炼平台的不同场景中，这个概念如何使用

智能体工具集成并非单一技术实现，而是贯穿于平台多类智能体形态与能力中心的统一范式，具体体现为以下三种协同路径：

- **声明式集成（Managed Agent）**：通过 YAML 配置文件直接声明所需工具（MCP 服务或 Skill），由平台自动注入调用上下文与参数解析逻辑；模型根据用户意图自主触发，无需显式编码。适用于标准化、低维护成本的客服、查询类场景。

- **可视化编排集成（Flow Agent）**：在画布中将工具作为独立节点拖入流程，手动连接 LLM 节点与工具节点，并配置输入映射（如将 LLM 输出 JSON 解析为 `maps_weather` 的 `location` 和 `date` 参数）。支持条件分支与错误重试，适合需要确定性控制与多步骤协同的业务流程。

- **代码级深度集成（Sandbox Agent）**：在 Python 沙箱中直接调用 MCP SDK、Skill SDK 或私有 SDK（如企业内部 ERP 客户端），通过 `app.py` 中的 `run()` 函数完全掌控工具调用时机、参数构造、异常处理与结果后处理；配合 `allow_internet: true` 可访问 VPC 内网资源，适用于高定制化、强状态依赖的生产系统对接。

此外，**Agent Store** 是工具集成的统一能力中枢：  
- MCP 服务提供标准化远程工具调用（如搜索、地图、爬虫），通过 `DASHSCOPE_API_KEY` 统一鉴权，支持云部署与极速模式切换；  
- Skill 提供轻量本地数据处理能力（如 PDF 解析、Excel 生成），由模型语义识别自动触发，无需参数配置，但仅在智能体应用中生效。

> 注意：工具集成能力与智能体类型强绑定——Skill 不可用于工作流或直连千问 API；MCP 在 Sandbox Agent 中需自行编码调用，在 Managed/Flow 中由平台托管调度。

## 关键参数和配置

| 场景 | 参数/配置项 | 说明 | 是否必需 |
|------|-------------|------|----------|
| **通用接入** | `DASHSCOPE_API_KEY` | 所有云部署 MCP 服务的统一认证凭证，需通过 Header `Authorization: Bearer <key>` 传入 | 是（MCP） |
| **Managed/Flow Agent** | `max_iterations` | 最大工具调用轮次（1–50，默认 15），防止无限循环；Sandbox Agent 由代码控制 | 否（默认生效） |
| **Sandbox Agent** | `allow_internet: true` | 创建时显式开启网络访问权限，否则无法调用任何外部 MCP 或 HTTP 接口 | 是（若需联网） |
| **Skill 集成** | `description`（SKILL.md 中） | 决定模型是否触发该 Skill 的核心字段，需精准描述输入类型、触发关键词与边界条件 | 是（影响调用准确率） |
| **MCP 部署** | `deploymentMode: "basic" \| "ultra"` | 基础模式按秒计费，极速模式额外收取部署费但降低延迟；影响工具响应 SLA | 否（默认 basic） |
| **API 调用** | `tool_choice`（Managed Agents API） | 控制工具调用策略：`auto`（模型自主决策）、`required`（强制调用指定工具）、`none`（禁用工具） | 否（默认 auto） |

## 面向开发者，简洁实用

- ✅ **优先选 MCP**：若需调用通用云服务（天气、地图、搜索），直接从 Agent Store 开通官方 MCP，零代码接入；自定义 MCP 请确保函数计算 FC 权限完备且 URL 路径符合 SSE 规范（如 `/mcp`）。
- ✅ **本地数据处理用 Skill**：处理用户上传的 PDF/XLSX 文件？上传 ZIP 包并写好 `SKILL.md` 描述即可，模型会自动识别并调用，不产生额外 [Token](token.md) 计费。
- ✅ **复杂逻辑用 Sandbox**：需调用私有数据库驱动、串联多个内部 API、或实现带状态的审批流程？选择 Sandbox Agent，上传含 `requirements.txt` 和 `app.py` 的 ZIP，完全掌控执行。
- ⚠️ **避坑提示**：
  - Managed/Flow Agent 中，工具调用超时固定为 5 秒（旧版）或由 MCP 服务自身 SLA 决定（新版），长耗时任务请改用 Sandbox + 异步轮询；
  - Skill 的 `description` 过于宽泛（如“处理文件”）会导致误触发，建议模仿官方 `xlsx` 示例：“提取 Excel 表格中第1列姓名和第3列邮箱，输出为 JSON 列表；不支持 CSV 或加密文件”；
  - 所有工具调用均受账号级 RAM 权限约束，确保子账号已授予 `bailian:UseMcpServer` 或 `bailian:UseSkill` 权限。

## 关联主题页

- [agent development](../guides/agent-development.md)
- [agent store](../guides/agent-store.md)
- [managed agents api](../api/managed-agents-api.md)
- [overview](../api/overview.md)
- [agent legacy](../guides/agent-legacy.md)


