# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、API Key 管理及控制台页面访问等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保资源隔离与安全合规。所有权限策略均与阿里云 RAM 深度集成，开发者需结合 RAM 策略与百炼控制台配置协同生效。

## 支持的模型/功能

权限管理覆盖以下关键能力：
- **模型调用**：控制特定模型在业务空间内是否可通过控制台或 OpenAPI 调用，并支持 QPM（每分钟请求数）和 Token 限流；默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：控制是否允许在业务空间内对指定模型执行微调（Fine-tuning）、LoRA 训练等操作，并管理调优后模型的部署权限；默认业务空间无限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：控制是否允许将模型（含调优后模型）直接部署为服务实例。
- **控制台页面级权限**：为 RAM 用户分配“模型体验-操作”“批量推理-操作”“模型观测-操作”等细粒度菜单权限，影响其在控制台的功能可见性与可操作性。
- **OpenAPI 接口权限**：RAM 用户默认无权调用应用相关 OpenAPI（如知识库、Prompt 工程、[长期记忆](../concepts/long-term-memory.md)等），需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `business_space_id` | 业务空间唯一标识，按地域隔离，不可跨地域复用 | 文档中明确“单个业务空间不能跨地域存在” |
| `model_id` | 模型全局唯一 ID（如 `qwen-max`, `qwen-vl-plus`），用于模型级权限绑定 | 权限配置界面中模型选择项 |
| `qpm_limit` / `token_limit` | 模型级限流阈值，单位分别为 QPM 和 tokens/minute，仅对非默认业务空间生效 | 文档中“限制模型调用”章节 |
| `api_key_scope` | API Key 绑定至**单一地域 + 单一业务空间 + 单一 RAM 用户**，不可迁移 | “API-Key 权限”章节 |
| `ram_policy` | 必须通过 RAM 控制台附加策略（如 `AliyunBailianFullAccess`, `AliyunBailianDataFullAccess`）才能启用对应高阶能力 | 多处强调需 RAM 授权 |

> **注意**：文档中多次提及“默认业务空间无法设置模型调用/调优/部署限制”，但未明确定义何为“默认业务空间”。根据控制台行为，通常指首次开通百炼服务时自动创建的、名称含 `default` 或未重命名的初始空间。该表述易引发歧义，建议以控制台实际显示的 `业务空间列表` 中标注为 `默认` 的空间为准。

## 使用方式

1. **角色初始化**  
   - 超级管理员：由阿里云主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户担任，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一管控所有空间。  
   - 业务空间管理员：由超级管理员或同空间管理员在**权限管理 → 用户管理**中为 RAM 用户勾选“管理员”角色赋予。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单中为指定业务空间**启用目标模型**（如 `qwen-plus`），否则即使用户有操作权限也无法调用。

3. **用户权限分配**  
   - 控制台权限：在业务空间内进入 **权限管理 → 用户管理 → 编辑用户 → 页面权限**，勾选所需功能（如“模型体验-操作”）。  
   - API 调用权限：为用户创建 API Key（需用户归属该空间），其可调用模型范围与限流策略**完全继承自业务空间配置**，与用户个人控制台权限无关。

4. **OpenAPI 授权（独立流程）**  
   必须由阿里云主账号登录 [RAM 控制台](https://ram.console.aliyun.com/users)，为目标 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略——此步骤**不经过百炼控制台**，且文档明确指出 RAM 用户默认无此权限 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 限制和注意事项

- **地域强隔离**：业务空间严格绑定地域，北京空间的 API Key 无法在新加坡地域使用，跨地域需分别创建空间并重复配置权限。
- **默认空间限制**：所有模型级权限控制（调用、调优、部署）在默认业务空间中**完全不可配置**，生产环境务必创建独立命名空间。
- **API Key 生命周期**：API Key 状态受归属用户生命周期影响——若用户被移出业务空间，其 API Key 将失效（重新加入后恢复）；若用户在 RAM 控制台被删除，则 API Key **永久失效**。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，百炼控制台不提供入口。
- **IP 白名单仅限北京地域**：目前仅华北2（北京）地域的 API Key 支持设置 IP 访问白名单，其他地域暂不支持。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


