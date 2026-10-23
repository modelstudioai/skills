# application permission management

百炼平台的应用权限管理机制用于控制不同用户或角色对应用（如 API 服务、工作流、模型调用等）的访问与操作范围，支持细粒度的读写、执行、配置和删除权限控制。该机制基于 RBAC 模型实现，与百炼统一身份认证体系深度集成。权限策略在应用创建时默认继承项目级策略，也可按需单独配置。

## 支持的模型/功能

- **权限主体**：支持用户、用户组、服务账号（Service Account）三类主体；其中服务账号适用于后端系统间调用场景，详见 [权限管理](../../raw/application-user-guide/application-permission-management.md)。
- **权限对象**：覆盖应用实例（Application）、模型绑定（Model Binding）、API 端点（Endpoint）、调试会话（Debug Session）等核心资源。
- **权限动作**：包括 `read`、`execute`、`update`、`delete`、`manage_permissions` 五类标准动作；`manage_permissions` 权限仅限项目管理员或显式授予的高级角色持有，参考 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的权限矩阵说明。

## 关键参数

- `principal_id`: 主体唯一标识，格式为 `user:uid_xxx`、`group:gid_xxx` 或 `service_account:said_xxx`。
- `resource_type`: 资源类型，如 `application`、`endpoint`、`model_binding`。
- `resource_id`: 资源实例 ID（可为空，表示对该类型所有资源生效）。
- `actions`: 字符串数组，例如 `["read", "execute"]`；不支持通配符，必须显式声明。
- `effect`: 仅支持 `"allow"`（当前不支持 deny 策略）。

> **注意**：原始文档中提及的 `scope: "project"` 参数已废弃，自 v2.3.0 起权限作用域由 `resource_type` 和 `resource_id` 组合隐式决定，实际行为以 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 的最新定义为准。

## 使用方式

1. **控制台配置**：进入应用详情页 →「权限」标签页 → 点击「添加权限」→ 选择主体、资源、动作并保存。
2. **API 配置**：调用 `POST /v1/applications/{app_id}/permissions`，请求体需符合上述关键参数结构；需持有 `manage_permissions` 权限。
3. **Terraform 支持**：通过 `bailian_application_permission` 资源声明，支持 IaC 方式管理；具体字段映射见 [权限管理](../../raw/application-user-guide/application-permission-management.md) 的附录章节。

## 限制和注意事项

- 单个应用最多绑定 200 条显式权限策略（不含继承的项目级策略）。
- 权限变更非实时生效：策略更新后最长 60 秒内同步至各服务节点。
- 不支持跨项目授权；若需跨项目访问，须在目标项目中单独配置权限。
- 删除应用时，其关联的显式权限策略自动清除，但项目级策略不受影响。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


