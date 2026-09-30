# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台功能访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用能力。所有权限策略均与业务空间强绑定，且 API Key 的行为严格继承其归属空间的模型与限流配置。

## 支持的模型/功能

权限管理覆盖以下核心能力：

- **模型调用**：控制台与 OpenAPI 层面对指定模型的调用许可、QPS 限流与 Token 限流（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）；
- **模型调优（训练）**：允许在业务空间内对支持调优的模型执行微调任务，并部署调优后模型；
- **模型部署**：允许直接部署百炼托管模型（如 Qwen 系列）至专属服务实例；
- **控制台页面级权限**：按菜单项（如“模型体验”“批量推理”“模型观测”）授予 RAM 用户可见性与操作权；
- **API Key 全生命周期管理**：包括创建、删除、查看及 IP 白名单设置（仅华北2支持），但 Key 不可跨空间迁移；
- **OpenAPI 接口权限**：需显式为 RAM 用户授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则默认无权调用应用相关 OpenAPI（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：默认业务空间（Default Workspace）**不支持**任何模型级权限限制（调用、调优、部署均全开），也无法配置限流；生产环境应避免使用默认空间，而应新建独立业务空间进行精细化管控（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspace_id` | 业务空间唯一标识，与地域强绑定 | 每个地域下独立命名，不可跨地域复用 |
| `model_id` | 模型唯一标识（如 `qwen-max`, `qwen-plus`） | 必须已在该空间启用（由超级管理员开通） |
| `qps_limit` | 每秒请求数上限 | ≥ 0；0 表示禁用调用 |
| `token_limit_per_minute` | 每分钟 Token 总消耗上限 | ≥ 0；0 表示禁用调用 |
| `api_key_ip_whitelist` | IP 白名单（CIDR 格式） | 仅华北2（北京）地域支持；最多 10 个条目 |

## 使用方式

### 1. 角色与权限分配
- **超级管理员**：必须拥有 `AliyunBailianFullAccess` 系统策略（主账号或授权 RAM 用户），通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)等）统一管理所有空间。
- **业务空间管理员**：由超级管理员或同空间管理员在「权限管理」页签中为 RAM 用户勾选「管理员」权限。
- **普通用户**：由管理员在「权限管理」页签中为其分配具体功能权限（如「模型体验-操作」）。

### 2. 模型权限开通（超级管理员操作）
1. 进入全局管理 → 「业务空间管理」→ 选择目标空间 → 「模型管理」；
2. 开启目标模型的「调用」「调优」「部署」开关，并设置 `qps_limit` 和 `token_limit_per_minute`。

### 3. API 调用准备
- 创建 API Key：在「权限管理」→ 「API Key 管理」中为用户生成 Key（Key 自动继承其归属空间的模型与限流策略）；
- 调用时无需额外鉴权参数，仅需在请求 Header 中携带 `Authorization: Bearer <api_key>`。

## 限制和注意事项

- **地域隔离**：业务空间严格绑定单一地域，跨地域资源（如模型、API Key、账单）不可共享；
- **默认空间限制**：默认业务空间无法配置任何模型级权限或限流，且不支持设为生产环境；
- **API Key 绑定不可变**：一个 API Key 仅归属一个地域 + 一个业务空间 + 一个用户，创建后不可转移或解绑；
- **OpenAPI 权限独立**：控制台权限（如「模型体验-操作」）**不影响** OpenAPI 调用能力；调用应用类 OpenAPI（如知识库、Prompt 工程）必须单独授予 `AliyunBailianData*Access` RAM 策略；
- **主账号特权**：AI 安全护栏、模型监控、应用观测等功能的首次开通，**必须由阿里云主账号**在控制台完成；
- **北京地域特殊规则**：自 2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号，而非 RAM 用户。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


