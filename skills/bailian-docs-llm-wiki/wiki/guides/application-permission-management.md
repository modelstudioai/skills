# application permission management

应用权限管理用于控制不同用户或角色对百炼应用的访问与操作权限，包括调用、配置、调试和管理等维度。它基于阿里云RAM（Resource Access Management）体系实现细粒度授权，支持按应用实例、模型版本及API端点进行策略配置。开发者需结合业务场景合理分配最小必要权限，避免越权访问风险。

## 支持的模型/功能

- 支持所有百炼平台托管的应用类型：文本生成类（如Qwen系列）、多模态类（如Qwen-VL）、[函数调用](../concepts/function-calling.md)类（Function Calling）及自定义插件集成应用  
- 权限覆盖范围包括：应用调用（`InvokeApplication`）、应用配置编辑（`UpdateApplication`）、日志查看（`ListApplicationLogs`）、监控数据读取（`DescribeApplicationMetrics`）及调试会话管理（`CreateDebugSession`）  
- 不支持对底层模型训练任务或私有模型仓库的直接权限控制，相关能力请参考 [权限管理](../../raw/application-user-guide/application-permission-management.md)

## 关键参数

- `Resource`: 必填，格式为 `acs:baichuan:cn-shanghai:<account-id>:application/<app-id>`，支持通配符 `*`（如 `application/*`）但不推荐在生产环境使用  
- `Action`: 指定允许的操作，例如 `baichuan:InvokeApplication`、`baichuan:UpdateApplication`；完整动作列表见 [权限管理](../../raw/application-user-guide/application-permission-management.md)  
- `Effect`: 取值 `Allow` 或 `Deny`，显式拒绝（`Deny`）优先级高于允许策略  

## 使用方式

1. 登录阿里云RAM控制台 → 进入「权限策略」→ 创建自定义策略（JSON格式）  
2. 在策略中声明上述 `Resource`、`Action` 和 `Effect` 字段，确保 `Resource` 与目标应用ID精确匹配  
3. 将策略授权给目标RAM用户、用户组或角色  
4. 用户调用应用API时，百炼服务端自动校验该用户的RAM策略，拒绝无权限请求  
> **注意**：部分旧版文档提及可通过应用控制台UI直接设置“成员权限”，该功能已于2024年Q2下线，统一收口至RAM策略管理，详见 [权限管理](../../raw/application-user-guide/application-permission-management.md)  

## 限制和注意事项

- 单个RAM策略最多绑定50个应用资源（`Resource` 数量），超出需拆分策略  
- 权限生效存在最长5分钟延迟（受RAM策略缓存机制影响），紧急场景建议调用 `RefreshPolicy` 接口强制刷新  
- 不支持跨地域授权：华东1（杭州）创建的应用无法通过华东2（上海）的RAM策略管控，必须使用对应地域的Resource ARN  
- 调试模式（`debug=true`）下的API调用同样受权限策略约束，不可绕过 —— 此行为与部分早期测试文档描述不符，请以 [权限管理](../../raw/application-user-guide/application-permission-management.md) 为准

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


