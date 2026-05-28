# application permission management

阿里云百炼权限管理提供基于业务空间的多维度访问控制体系，支持按角色划分控制台操作边界与 OpenAPI 调用权限。通过精细化的资源隔离、模型级限流策略与 API Key 绑定机制，满足企业级多团队、多环境下的安全协作与成本管控需求。

## 支持的模型/功能
权限体系围绕业务空间与身份角色构建，核心覆盖以下功能域：
* **角色权限分级**：系统内置超级管理员（跨空间全局管控）、业务空间管理员（单空间资源与用户管理）与普通用户（按需访问）三级模型 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
* **控制台功能管控**：支持独立配置模型体验、批量推理、模型调优（训练）、模型部署、数据管理及评测等页面的访问与操作权限。
* **OpenAPI 数据接口**：默认 [[ram-user]] 无法调用应用数据、知识库、Prompt 工程及长期记忆等接口。需主账号通过 RAM 控制台授予 `AliyunBailianDataFullAccess`（全量）或 `AliyunBailianDataReadOnlyAccess`（只读）系统策略。
* **财务与账单**：账单查询与预付费产品采购需独立授权 `AliyunBSSReadOnlyAccess` 与 `AliyunBSSOrderAccess`，避免越权操作企业财务模块。

## 关键参数
权限生效与路由依赖以下核心配置，集成开发时需准确传递：
* `Workspace ID`：业务空间唯一标识。所有模型配额、限流阈值与 [[api-key]] 归属均绑定至此 ID，是权限隔离的最小单元。
* `QPM/Token 限流阈值`：可按业务空间对特定模型设置请求数（QPM）与 Token 消耗上限。默认业务空间强制开放且不可配置限流。
* `IP 白名单`：支持为 API Key 设置访问 IP 限制，目前仅华北2（北京）地域生效。配置后非白名单 IP 发起的请求将被拦截。
* `App ID`：配合 `Workspace ID` 使用，用于在 API 调用时精准定位权限域下的具体应用实例。详细路由规则参考 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 使用方式
### 1. 角色授权与初始化
* **配置超级管理员**：由阿里云主账号或具备 `AliyunRAMFullAccess` 的账号操作。为目标 RAM 账号附加 `AliyunBailianFullAccess` 及财务采购策略后，该账号即可通过全局管理菜单跨地域、跨空间分配权限。
* **配置业务空间管理员**：在控制台左侧导航栏 **权限管理** 页签中，将指定 RAM 用户提升为管理员。该角色仅能管理当前空间内的用户权限、可用模型与 API Key。

### 2. 模型与调用权限分配
* **控制台调用/调优**：若使用非默认业务空间，超级管理员需先开通对应模型的调用/调优开关。随后通过权限管理页签为 RAM 用户勾选细粒度菜单权限（如模型调优-操作、数据管理-操作等）。
* **API 调用集成**：无需依赖控制台页面权限。管理员只需在目标业务空间内为 RAM 用户创建 [[api-key]]，客户端在请求 Header 中携带该 Key 即可。系统自动基于 Key 归属的空间校验模型开关与限流。

### 3. 生产环境配额规划
推荐按环境（`dev`/`test`/`prod`）或业务线隔离空间。主账号总配额建议按比例分配至各空间，并预留 10% 缓冲 QPM 应对突发流量，避免全局限流触发。

## 限制和注意事项
* **地域强隔离**：业务空间严格绑定单一地域，资源、权限与账单无法跨地域继承。不同地域的“默认空间”逻辑上完全独立。
* **控制台与 API 权限解耦**：限制 RAM 用户的控制台可见性 **不会** 阻断其名下 API Key 的接口调用能力。如需阻断 API 调用，必须在业务空间层级关闭模型权限或回收 Key。
* **API Key 状态联动**：API Key 不支持跨空间或跨用户迁移。若所属 RAM 用户被移出业务空间，其 Key 将立即失效（重新加入可恢复）；删除 RAM 用户则 Key 永久失效。
> **注意**：自 2026年3月25日起，**华北2（北京）**地域所有新创建的 API Key 将强制归属阿里云主账号。原有的 RAM 用户绑定逻辑届时将不再适用，请提前规划服务账号体系。
> **注意**：部分旧版文档提及“API Key 需按模型类型创建”，当前版本已统一，单一 API Key 可调用该业务空间授权的所有模型类型，无需重复生成。
* **权限排查路径**：若遇到 `AccessDenied` 或限流拦截，请优先核对 RAM 策略是否已生效、API Key 归属空间是否正确，以及目标模型在该空间的开关状态。完整排查指引详见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)

