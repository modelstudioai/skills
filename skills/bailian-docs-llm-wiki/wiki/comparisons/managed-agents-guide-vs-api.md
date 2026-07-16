# 托管智能体：指南与 API 对比

百炼平台的 Managed Agents（托管智能体）提供了两套面向不同使用者的文档视角：**使用指南**侧重在控制台向导中完成端到端配置，适合快速上手与业务验证；**API 参考**则给出完整的 REST 资源模型与端点定义，适合工程化集成与自动化。二者描述的是同一套托管运行时——平台在服务端托管会话状态、沙箱环境与工具执行——但抽象层级、覆盖范围与目标读者不同。本页从关键维度做对比，帮助开发者按阶段选择合适的入口。

## 关键维度对比

| 维度 | 使用指南（guides/managed-agents） | API 参考（api/managed-agents-api） |
| --- | --- | --- |
| 定位 | 概念讲解 + 控制台向导操作流程 | REST 资源模型 + 端点契约 |
| 目标读者 | 初次接入、业务验证、快速体验 | 后端集成、SDK 调用、自动化编排 |
| 核心对象 | Agent、Environment、Session、Event（4 类） | Agent、Environment、Session、Event、Skill、File（6 类） |
| 操作方式 | 控制台向导 + 预览调试标签页 | 直接调用 REST API / SDK |
| 认证方式 | 控制台登录（隐式） | HTTP Header 携带 `Authorization: Bearer <api-key>` |
| API 基地址 | 未强调 | `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio` |
| 支持地域 | 未强调 | 当前仅 `cn-beijing` |
| Agent 端点 | `POST /api/v1/agentstudio/agents`（创建） | 创建/获取/列出/更新/归档/列出版本 全套 |
| 版本管理 | 未展开 | 每次更新递增 `version`，会话锁定当时快照 |
| 事件流 | SSE 事件流（`GET /sessions/{id}/events/stream`） | SSE 长连接 + 事件历史分页（`GET /sessions/{id}/events`） |
| Skill 支持 | 提及可挂载预置工具组合 | 完整生命周期：上传/安全扫描/版本/下载/删除 |
| File 支持 | 上传挂载，路径 `/mnt/session/uploads` | 独立资源：上传/查询/列出/删除，审核状态机 |
| 文件大小上限 | 单文件 10 MB（上传挂载语境） | 单文件 20 MB，工作空间总量 100 GB，保留 30 天 |
| 状态机 | 会话状态、中断续接、工具审批（概念性描述） | `idle` → `running` → `idle` / `terminated`（显式定义） |
| 示例模型 | `qwen3-max`（向导示例另见 `qwen3.7-plus`，以下拉列表为准） | `qwen3-max` |
| 典型场景 | 多步工具调用、代码执行、文件处理等长时任务的快速搭建 | 生产环境集成、批量会话编排、CI/自动化流水线 |

## 关键差异说明

- **抽象层级**：指南把流程压缩成"配置智能体 → 配置环境 → 发起会话 → 发送事件"四步，隐藏了大量端点细节；API 参考把每类资源的增删改查、版本、归档、软/硬删除逐一列清，是精确的契约。
- **资源覆盖**：指南聚焦运行链路的 4 个核心对象（Agent / Environment / Session / Event），而 API 额外把 **Skill** 与 **File** 提升为一等资源，并明确了它们的安全扫描/审核状态机与挂载版本锁定规则。
- **文件配额不一致**：指南上下文提到单文件 10 MB，API 参考给出 20 MB、工作空间 100 GB、保留 30 天。以 API 参考的配额为准，并注意实际以控制台/接口返回为准。
- **端点方法差异**：API 总览页把部分更新端点标注为 `PATCH`，而各资源详情页标注为 `POST`（Agent / Environment / Session 均如此）。集成时以各资源详情页为准。
- **版本与快照语义**：只有 API 参考明确了"会话创建时锁定 Agent 版本、Skill 挂载锁定具体 version、更新不影响已有会话"的重要约束，这对生产环境的稳定性至关重要。

## 适用场景建议

- **选择「使用指南」入口**：
  - 第一次接触 Managed Agents，想快速理解 Agent / Environment / Session / Event 之间的关系。
  - 需要在控制台向导中拖拽配置、用预览调试标签页按事件类型（User、Agent、Tool、Tool_output 等）观察执行过程。
  - 做业务原型、Demo 或轻量验证，暂不需要写代码。

- **选择「API 参考」入口**：
  - 需要把托管智能体嵌入后端服务、批量创建/复用 Agent 与 Environment。
  - 关注鉴权、地域、版本锁定、状态机、配额等工程化细节。
  - 需要管理 Skill 上传/安全扫描/版本挂载，或对 File 做上传/审核/挂载的自动化处理。
  - 构建 CI/自动化流水线，依赖稳定的端点契约与 `x-request-id` 排障能力。

## 技术选型参考

推荐路径是"**先指南、后 API**"：用指南在控制台跑通端到端流程、确认业务可行性，再切换到 API 参考完成工程化集成。两者并非二选一，而是覆盖同一运行时的不同生命周期阶段。集成落地时，务必以 API 参考为准处理认证（Bearer API Key）、地域限制（`cn-beijing`）、版本快照语义与端点方法差异，并按 API 侧的 20 MB / 100 GB / 30 天配额规划文件资源。

## 被对比主题页

- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)


