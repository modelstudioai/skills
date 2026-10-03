# application permission management

百炼平台的权限管理基于“业务空间”这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别承担全局管理、空间级管理和资源使用职责。所有 API Key 的调用能力严格继承自其归属业务空间的模型权限配置，与用户账号的控制台权限解耦。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全类型模型的调用权限控制（含控制台体验与 OpenAPI 调用），并可独立设置请求数（QPM）与 Token 限流。  
- **模型调优（训练）**：支持为指定模型开通/关闭调优权限，并控制调优后模型的自动部署能力。  
- **模型部署**：支持对已调优或第三方模型的直接部署权限开关。  
- **控制台页面级权限**：支持按菜单项（如“模型体验”“批量推理”“模型观测”）授予 RAM 用户可见性与操作权，但**不约束 API Key 行为**。  
- **OpenAPI 接口权限**：需通过 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则默认无权调用应用相关 OpenAPI（如知识库、Prompt 工程等接口）[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。  

> **注意**：文档中多次出现“默认业务空间无法设置模型调用/调优/部署限制”的说明，但实际在控制台中，部分新创建的默认空间已支持基础限流配置。该差异表明 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中关于默认空间的限制描述可能已过时，请以控制台最新 UI 为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `QPM limit` | 每分钟最大请求数，作用于单个模型在该业务空间的全部调用入口（控制台 + API） | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `Token limit` | 每分钟最大 Token 消耗量，按输入+输出总 Token 计算，与 QPM 独立生效 | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `API Key 所属空间` | 单个 API Key 仅绑定一个地域内的一个业务空间，不可迁移；其模型权限完全继承自该空间配置 | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `IP 白名单` | 仅华北2（北京）地域的 API Key 支持配置，其他地域暂不支持 | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一管理多空间。  
   - 业务空间管理员：由超级管理员在对应空间的「权限管理」页签中为 RAM 用户授予「管理员」角色。  

2. **模型权限开通（必需前置步骤）**  
   - 超级管理员需先在全局管理菜单中为业务空间启用目标模型的「调用」「调优」或「部署」开关（默认空间除外）。  

3. **用户权限分配**  
   - 控制台权限：在业务空间「权限管理」页签中，为 RAM 用户勾选具体功能项（如“模型体验-操作”）。  
   - API 调用权限：为用户创建 API Key（需具备「API-Key 管理」权限），该 Key 自动继承业务空间模型权限。  
   - OpenAPI 权限：必须在 RAM 控制台单独附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。  

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域同名空间互不影响，权限不可复用。  
- **默认空间限制**：除华北2（北京）外，其他地域的默认业务空间**不支持模型限流与调优开关配置**；若需精细化管控，必须新建非默认空间。  
- **API Key 绑定刚性**：API Key 创建后不可变更所属空间或用户，删除后不可恢复；RAM 用户被移出业务空间将导致其 API Key 失效（重新加入后恢复）。  
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台独立授权，**不包含在 `AliyunBailianFullAccess` 内**。  
- **主账号特权**：阿里云主账号天然拥有所有业务空间全部权限，无需额外配置；但开通 AI 安全护栏、模型监控等增值服务，**建议使用主账号一次性完成控制台授权**。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


