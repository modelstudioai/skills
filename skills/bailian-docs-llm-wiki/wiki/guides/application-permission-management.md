# application permission management

应用权限管理用于控制不同用户或角色对百炼应用的访问与操作权限，包括调用、配置、调试、发布等关键能力。它基于 RBAC（基于角色的访问控制）模型实现，支持细粒度的权限策略配置。权限策略通过平台控制台或 OpenAPI 进行管理，适用于多租户协作场景。

## 支持的模型/功能

- 支持为应用分配 **Viewer（只读）**、**Editor（编辑）**、**Admin（管理员）** 三类内置角色，也可通过自定义策略扩展权限范围  
- 支持按用户、用户组或 RAM 角色绑定权限策略  
- 支持对单个应用实例独立授权，不跨应用继承权限  
- 权限作用域覆盖：应用调用（`invoke`）、调试（`debug`）、配置修改（`update`）、版本发布（`publish`）、日志查看（`view-logs`）等操作  
- 详细能力矩阵可参考 [权限管理](../../raw/application-user-guide/application-permission-management.md) 中的表格说明

## 关键参数

调用 `UpdateApplicationPermission` 或 `CreateApplicationPolicy` API 时需指定以下核心参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `ApplicationId` | string | 是 | 应用唯一标识符（如 `app-xxx`） |
| `Principal` | object | 是 | 授权主体，含 `Type`（`User`/`Group`/`RAMRole`）和 `Id`（如 `alice@aliyun.com`） |
| `Actions` | string[] | 是 | 允许的操作列表，例如 `["invoke", "debug"]`；完整列表见 [权限管理](../../raw/application-user-guide/application-permission-management.md) |
| `Effect` | string | 否 | 默认 `"Allow"`；暂不支持 `"Deny"` 策略（当前仅支持显式授权） |

> **注意**：文档中提及的 `Effect: "Deny"` 在 v2.3.0+ 版本已移除支持，实际调用将返回 `InvalidParameter.EffectNotSupported` 错误；该信息在 [权限管理](../../raw/application-user-guide/application-permission-management.md) 中未同步更新，请以 OpenAPI 文档为准。

## 使用方式

1. **控制台操作**：进入「应用详情页 → 权限管理」标签页，点击「添加成员」，选择用户/用户组并勾选对应权限项  
2. **OpenAPI 调用**：使用 `UpdateApplicationPermission`（批量更新）或 `CreateApplicationPolicy`（单策略创建）接口，推荐使用前者以避免策略冲突  
3. **Terraform 集成**：通过 `alicloud_bailian_application_permission` 资源声明式管理（需 provider >= 1.15.0）  
4. 权限变更后**立即生效**，无需重启应用或刷新缓存；调试界面中的「测试调用」按钮可见性由当前用户对该应用的 `invoke` + `debug` 权限共同决定  

## 限制和注意事项

- 单个应用最多绑定 100 个权限策略（含用户级与组级）  
- RAM 角色授权仅支持阿里云主账号下的可信实体角色，不支持外部身份提供商（IdP）映射的角色  
- 删除用户账号后，其绑定的应用权限**不会自动清理**，需手动解除或通过 `DeleteApplicationPermission` 清理，否则可能造成权限残留  
- 所有权限操作均记录于 ActionTrail 审计日志，事件名称为 `BaiLianApplicationPermissionModified`；审计字段细节参见 [权限管理](../../raw/application-user-guide/application-permission-management.md)

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


