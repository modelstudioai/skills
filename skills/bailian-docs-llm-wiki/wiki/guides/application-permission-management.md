# application permission management

百炼平台的权限管理基于“业务空间”这一最小管理单元，提供跨地域、多角色、模型级的精细化控制能力，覆盖控制台操作、API 调用、模型调用/调优/部署、限流及账单等维度。权限体系由超级管理员、业务空间管理员和普通用户三级角色驱动，所有策略均绑定至具体地域内的业务空间，不支持跨地域共享。

## 支持的模型/功能

- **模型调用**：支持为业务空间开启/关闭特定模型（如 Qwen 系列、Qwen-VL、语音合成等）的调用权限，并可配置请求频次（QPM）与 [Token](../concepts/token.md) 总量双维度限流。> **注意**：默认业务空间无法设置模型调用限制，全部模型默认可调用且不限流 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持在业务空间内授权特定模型的调优能力（含数据集管理、训练任务提交、快照保存），调优完成后需额外授权“模型部署”权限方可对外提供服务。
- **模型部署**：支持独立开关某模型在该业务空间的直接部署权限（即非调优后部署），适用于预置模型的一键上线场景。
- **OpenAPI 接口访问**：RAM 用户默认无权调用应用类 OpenAPI（如知识库、Prompt 工程、[长期记忆](../concepts/long-term-memory.md)等），需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **细粒度页面权限**：支持按菜单项（如“模型体验”“批量推理”“模型评测”）为用户分配控制台功能可见性与操作权，但**不影响其 API Key 的实际调用能力**。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `business_space_id` | 业务空间唯一标识，绑定地域（如 `cn-beijing`），不可跨地域复用 | 必填，API 调用与控制台操作均依赖此 ID |
| `model_id` | 模型全局唯一 ID（如 `qwen-max`, `qwen-vl-plus`） | 仅当业务空间已开通该模型权限时生效 |
| `qpm_limit` / `token_limit` | 每分钟请求数上限 / 每分钟 [Token](../concepts/token.md) 总量上限 | 限流值不能超过主账号总配额；默认业务空间不支持配置 |
| `api_key_id` | API Key 唯一标识，严格绑定单一地域 + 单一业务空间 + 单一用户 | 不可迁移；2026-03-25 后北京地域新创建的 Key 归属主账号，与 RAM 用户解耦 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |

## 使用方式

1. **角色初始化**  
   - 超级管理员：由阿里云主账号或持有 `AliyunBailianFullAccess` 策略的 RAM 用户担任，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置空间、模型、用户与 API Key。
   - 业务空间管理员：由超级管理员在对应空间的「权限管理」页签中，为 RAM 用户授予「管理员」角色。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单中为业务空间启用目标模型的调用、调优或部署权限；未开通则后续用户授权无效。

3. **用户权限分配**  
   - 控制台权限：在业务空间「权限管理」页签中，为用户勾选对应功能模块（如“模型体验-操作”“模型调优-操作”）。  
   - API 调用权限：为用户创建或分配 API Key，其可用模型与限流策略**完全继承自所属业务空间配置**，与用户个人控制台权限无关。

4. **API Key 管理**  
   - 创建/删除/查看 API Key 需用户具备该业务空间的「API Key 管理」权限。  
   - 支持为华北2（北京）地域的 API Key 设置 IP 白名单。

## 限制和注意事项

- **地域强绑定**：业务空间与地域严格绑定，同一逻辑空间名在不同地域（如北京 vs 新加坡）代表完全独立的权限域，无法互通 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **默认空间限制**：默认业务空间不支持任何模型级权限开关与限流配置，仅适用于快速试用；生产环境必须创建独立业务空间。
- **API Key 生命周期**：  
  - 2026-03-25 前由 RAM 用户创建的 API Key，在 RAM 控制台删除该用户时将**级联删除且不可恢复**；  
  - 2026-03-25 及之后创建的 API Key 与 RAM 用户解耦，删除用户不影响 Key 生效。
- **OpenAPI 权限隔离**：应用类 OpenAPI（如 `/v1/knowledge_bases`）的访问权限**不通过百炼控制台配置**，必须由主账号在 RAM 控制台单独授权策略，详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **账单与预付费权限**：RAM 用户默认无权查看账单或购买预付费资源，需主账号额外授予 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess` 策略。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


