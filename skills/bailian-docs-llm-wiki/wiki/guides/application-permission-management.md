# application permission management

百炼平台的应用权限管理机制用于控制不同用户或角色对应用（Application）的访问与操作权限，支持细粒度的读写分离和资源级授权。该能力基于平台统一的身份认证与 RBAC 模型实现，适用于多租户协作场景下的安全治理需求。开发者可通过控制台或 OpenAPI 配置权限策略，所有变更实时生效。

## 支持的模型/功能

- 支持 **RBAC（基于角色的访问控制）** 模型，预置 `admin`、`editor`、`viewer` 三类内置角色，也可自定义角色并绑定权限集  
- 支持 **应用级权限**（如 `app:read`、`app:write`、`app:delete`）和 **资源级权限**（如 `app:config:read`、`app:log:read`）  
- 支持通过 [权限管理](../../raw/application-user-guide/application-permission-management.md) 页面进行可视化配置，也支持通过 OpenAPI 批量管理  
- 权限继承关系明确：组织 > 应用 > 版本/环境（当前仅应用维度生效，版本级权限暂未开放，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）

## 关键参数

调用 OpenAPI 管理权限时需关注以下核心字段：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 目标应用唯一标识，可在控制台应用详情页获取 |
| `principal_type` | string | 是 | 主体类型，取值 `user` 或 `role` |
| `principal_id` | string | 是 | 用户 ID 或角色 ID（如 `role:custom-deployer`） |
| `permissions` | string[] | 是 | 权限列表，例如 `["app:read", "app:config:read"]`；不支持通配符，必须显式声明 |

> **注意**：`permissions` 字段中若传入未注册的权限码（如 `app:debug:*`），API 将静默忽略该条目而非报错——此行为与 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“非法权限触发 400 错误”的旧版描述矛盾，以当前 API 实际行为为准。

## 使用方式

1. **控制台操作**：进入目标应用 → 左侧导航栏点击「权限管理」→ 添加成员或角色 → 分配权限 → 保存  
2. **OpenAPI 调用**：使用 `POST /v1/apps/{app_id}/permissions` 接口批量授予权限（参考 [权限管理](../../raw/application-user-guide/application-permission-management.md) 中的 API 示例）  
3. **权限同步**：当用户所属角色变更时，其应用权限将在 30 秒内自动刷新，无需手动触发同步  

## 限制和注意事项

- 单个应用最多绑定 500 个权限主体（用户 + 角色总数）  
- `admin` 角色不可被删除或撤销，但可解除其在特定应用上的绑定  
- 删除用户账号后，其直接授予的权限立即失效，但通过角色继承的权限仍保留，需单独清理角色绑定  
- 当前不支持条件权限（如基于 IP 或时间的动态策略），所有权限均为静态授权

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


