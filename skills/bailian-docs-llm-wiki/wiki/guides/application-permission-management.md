# application permission management

百炼平台的应用权限管理机制用于控制不同用户或角色对应用内资源（如模型调用、数据访问、配置修改等）的操作权限。它基于 RBAC（基于角色的访问控制）模型实现，支持细粒度策略配置，并与百炼统一身份认证体系集成。开发者可通过控制台或 OpenAPI 管理权限策略，适用于多租户、协作开发及生产环境隔离等典型场景。

## 支持的模型/功能

- **权限模型**：支持 `Viewer`（只读）、`Editor`（可编辑应用配置与提示词）、`Admin`（全量操作，含成员管理与权限分配）三类内置角色；也支持通过自定义策略（Custom Policy）声明式定义最小权限（例如仅允许调用特定模型的 `/v1/chat/completions` 接口）。  
- **作用范围**：权限可绑定至单个应用（Application-level）、工作区（Workspace-level）或整个租户（Tenant-level），其中应用级权限优先级最高。  
- **集成能力**：支持与企业 SSO（如 Okta、Azure AD）同步用户组，并将组映射为平台角色；相关配置详见 [权限管理](../../raw/application-user-guide/application-permission-management.md) 的“SSO 集成”章节。  

## 关键参数

调用权限管理 API 时需关注以下核心参数（以 `POST /v1/applications/{app_id}/policies` 为例）：

- `role`: 字符串，取值为 `viewer` / `editor` / `admin` 或自定义策略 ID（如 `policy:llm-inference-read-only`）  
- `principal`: 主体标识，格式为 `user:uid_abc123` 或 `group:grp_def456`  
- `resources`: 资源列表，支持通配符，例如 `["model:qwen-max", "dataset:prod-*"]`  
- `effect`: `"allow"` 或 `"deny"`（当前仅支持 `allow`，`deny` 规则暂未生效 —— 详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的“策略评估逻辑”说明）  

> **注意**：文档中提及的 `effect: deny` 在 v3.2.0+ 版本中仍为预留字段，实际策略引擎仅执行 `allow` 规则。该行为与 [权限管理](../../raw/application-user-guide/application-permission-management.md) 正文描述存在不一致，以当前 API 行为为准。

## 使用方式

1. **控制台操作**：进入「应用详情页 → 权限管理」标签页，点击「添加成员」，选择用户/组并分配角色；支持批量导入 CSV（格式见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 附录 A）。  
2. **OpenAPI 调用**：使用 `PUT /v1/applications/{app_id}/members` 接口更新成员角色；需携带 `X-Api-Key` 认证头及 `application/json` 请求体。  
3. **Terraform 管理**：通过 `bailian_application_permission` 资源声明式配置（需启用 `bailian-provider v1.8.0+`）。

## 限制和注意事项

- 单应用最多绑定 500 个直接成员（不含继承自工作区的成员）；超出需通过工作区级角色统一分配。  
- 自定义策略中 `resources` 字段不支持正则表达式，仅支持前缀匹配（如 `model:qwen-*`）和精确匹配（如 `model:qwen-plus`）。  
- 权限变更后，前端缓存最长延迟 60 秒生效；若需立即生效，客户端应主动调用 `/v1/auth/refresh-permissions`（需 Admin 权限）。  
- 删除用户账号后，其在应用中的权限条目不会自动清理，须手动移除或依赖定时 GC 任务（默认每 24 小时执行一次）。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


