# 托管智能体使用指南与 API 参考对比

百炼平台的 Managed Agents（托管智能体）提供两类文档入口：面向使用者的**使用指南**（guides/managed-agents）和面向开发者的 **API 参考**（api/managed-agents-api）。两者描述的是同一套产品能力，但侧重点、抽象层次和适用阶段不同。本文从开发者技术选型角度，对两类文档的定位、覆盖范围与关键细节进行对比，帮助读者快速判断在不同阶段应参考哪份文档。

## 关键维度对比

| 维度 | 使用指南（guides/managed-agents） | API 参考（api/managed-agents-api） |
|------|----------------------------------|-----------------------------------|
| 目标读者 | 产品经理、初次使用者、需要快速上手的开发者 | 需要程序化集成的后端/平台开发者 |
| 操作方式 | 控制台向导 + API 均可完成 | 纯 REST API / SDK 调用 |
| 核心概念覆盖 | 四个对象：Agent、Environment、Session、Event | 六个资源：Agent、Environment、Session、Event、Skill、File |
| 端点信息 | 仅提及关键端点（如 `POST /agents`、`POST /sessions`） | 完整端点表，含全部 CRUD、归档、版本管理操作 |
| 认证说明 | 未展开 | 详细说明基地址拼装规则（`{workspace_id}.{region}.maas.aliyuncs.com`）、Bearer [Token](../concepts/token.md) 鉴权、`x-request-id` 排障 |
| 版本管理 | 未涉及 | Agent 更新自动递增版本号、会话创建时锁定版本、Skill 挂载需指定具体版本 |
| 状态机 | 提及会话状态机支持中断与续接 | 给出完整状态流转（`idle` → `running` → `idle` / `terminated`） |
| Skill 资源 | 仅说明 Skill 可挂载预置工具组合 | 完整生命周期：上传 zip → 安全扫描（`checking` → `active` / `rejected`）→ 挂载 → 版本更新 |
| File 资源 | 提及单文件不超过 10 MB（上传限制） | 独立 File 资源体系：单文件上限 20 MB、工作空间总量 100 GB、保留期 30 天、审核状态流转 |
| 上下文与资源挂载 | 详细说明挂载时机、路径约定（`/mnt/session/uploads`）、会话隔离机制 | 侧重 API 字段（`resources` 字段、`POST /sessions/{id}/resources`） |
| 调试手段 | 控制台预览调试标签页，按事件类型筛选查看 | 通过 `GET /sessions/{id}/events` 分页列出事件历史 + SSE 流式订阅 |
| 地域支持 | 未明确 | 明确当前仅支持 `cn-beijing` |

## 内容互补关系

两份文档并非替代关系，而是互补：

- **使用指南**解释了"为什么这样设计"：Managed Agents 与智能体应用的本质区别（有状态 vs 无状态、独立沙箱 vs 共享运行时）、会话级事件流与响应级[流式输出](../concepts/streaming.md)的差异、挂载资源的隔离语义等。这些概念是正确调用 API 的前提。
- **API 参考**回答了"具体怎么调"：每个资源的完整端点列表、请求/响应结构、乐观锁（更新需带 `version`）、软归档与硬删除的区别、配额限制等工程细节。

## 适用场景建议

### 优先阅读使用指南的场景

- 初次接触 Managed Agents，需要理解产品定位与核心概念
- 评估 Managed Agents 与智能体应用的技术选型
- 使用控制台向导完成快速验证（PoC）
- 需要理解沙箱隔离、文件挂载路径约定、会话中断续接等运行时行为

### 优先阅读 API 参考的场景

- 将 Managed Agents 集成到自有产品或自动化流水线
- 需要精细控制资源生命周期（版本管理、归档、删除策略）
- 开发 Skill 包并管理其发布与挂载流程
- 需要处理文件上传审核状态、配额规划
- 排查线上问题（利用 `x-request-id`、事件历史分页查询）

### 推荐的阅读顺序

1. 先通读使用指南，建立 Agent → Environment → Session → Event 的心智模型
2. 按使用指南中的四步流程在控制台跑通一次端到端任务
3. 切换到 API 参考，将控制台操作映射为对应的 REST 调用
4. 针对 Skill 和 File 等进阶资源，以 API 参考为准进行程序化管理

## 已知文档差异

在使用两份文档时需注意以下不一致之处：

| 差异点 | 使用指南 | API 参考 | 建议 |
|--------|----------|----------|------|
| 示例模型名称 | 控制台向导示例为 `qwen3.7-plus` | API 代码示例为 `qwen3-max` | 以控制台模型下拉列表中实际可选的模型 ID 为准 |
| 单文件大小限制 | 上传文件不超过 10 MB | File 资源单文件上限 20 MB | 10 MB 可能为控制台上传通道限制，API 直传上限为 20 MB；以实际调用返回为准 |
| Agent 更新端点 | 未涉及 | 总览页标注 `PATCH`，详情页标注 `POST` | 以资源详情页为准 |

## 被对比主题页

- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)



