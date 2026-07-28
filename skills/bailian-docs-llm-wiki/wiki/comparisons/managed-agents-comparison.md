# 托管智能体指南与 API 对比

本页对比百炼 Managed Agents 的两份核心文档：面向控制台使用者的「托管智能体指南」与面向开发者的「Managed Agents API」。两者描述的是同一套托管运行时，但视角、详略与关注点差异显著。开发者做技术选型时应先明确自身入口（控制台可视化操作 vs API/SDK 编程调用），再据此选择文档作为主参考。

## 关键维度对比

| 维度 | 托管智能体指南 | Managed Agents API |
| --- | --- | --- |
| 文档定位 | 概念讲解 + 控制台操作向导 | REST/SDK 接口参考 + 端到端调用流程 |
| 目标读者 | 平台使用者、低代码/半托管场景开发者 | 需编程集成的后端/应用开发者 |
| 核心资源对象 | 4 类：Agent、Environment、Session、Event | 6 类：Agent、Environment、Session、Event、Skill、File |
| 使用入口 | 控制台向导 + 预览调试标签页 | REST API + SDK，按地域拼装 endpoint |
| 认证方式 | 未展开，依赖控制台登录态 | `Authorization: Bearer <API Key>`，单 Key 访问工作空间全部资源 |
| 地域支持 | 未显式说明 | 当前仅 `cn-beijing` |
| 默认工具集 | 7 个内置工具（bash/read/write/edit/glob/grep/download_file）全选，可取消 | 通过 Environment 配置沙箱类型与预装依赖，工具粒度未在 API 文档单独枚举 |
| 上下文/文件挂载 | 强调 `/mnt/session/uploads` 路径约定、会话隔离、运行时追加 | 抽象为 File 资源，经安全审核（checking → available/rejected/type_rejected）后挂载 |
| 单文件上传上限 | 10 MB | 20 MB |
| 工作空间配额 | 未提及 | 总容量 100 GB，保留期 30 天 |
| 版本管理 | 未展开 | Agent 每次更新自动递增 version，会话创建时锁定版本；Skill 挂载须指定具体版本号 |
| 状态机描述 | 提及 idle/中断/续接/工具审批，指向会话文档详述 | 明确 idle → running → idle/terminated，含归档与硬删除语义 |
| 安全扫描 | 未提及 Skill/File 审核流程 | Skill：checking → active/rejected；File：checking → available/rejected/type_rejected |
| 事件流 | 会话级 SSE，按事件类型筛选（User/Agent/Tool/Tool_output/Error/Model/System） | `GET /sessions/{id}/events/stream` 长连接 SSE，含分页列出历史 |
| 典型流程步数 | 4 步（配置智能体 → 配置环境 → 发起会话 → 发送事件接收响应） | 5 步（创建 Agent → 配置 Environment → 创建 Session → 发送 Event → 订阅 SSE） |
| API 端点示例 | 仅给出创建类端点（agents/environments/sessions） | 完整 CRUD + 版本/归档/下载端点表格，覆盖全部资源 |
| 已知不一致 | 控制台示例模型名 `qwen3.7-plus` 与 API 示例 `qwen3-max` 不一致 | Agent/Environment/Session 更新端点在总览页标 `PATCH`、详情页标 `POST` |

## 适用场景建议

- **选「托管智能体指南」**：需要快速理解 Managed Agents 是什么、与无状态智能体应用的区别、以及如何用控制台向导跑通最小流程；适合概念入门、POC 验证、非编程使用者。
- **选「Managed Agents API」**：需要把托管智能体嵌入自有产品、做编程化编排与运维；需要精确的端点、字段、版本与状态机语义；适合生产集成、自动化流水线、SDK 封装层开发。

## 技术选型参考

1. 若团队无后端开发资源、仅做内部工具或演示，优先走控制台向导，以指南为主参考。
2. 若需要多智能体复用、版本快照、Skill 市场化分发、文件安全审核等企业级能力，必须基于 API 文档设计资源治理与生命周期策略。
3. 两份文档在模型名、HTTP method 上存在不一致，落地时以控制台模型下拉列表与各资源详情页为准，必要时提工单附 `x-request-id` 确认。

## 被对比主题页

- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)


