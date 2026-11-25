# application permission management

阿里云百炼的权限管理以“业务空间”为最小单元，提供跨地域、多角色、模型级与页面级的精细化控制能力，支撑开发、测试、生产等多环境隔离及组织内权限分治。权限体系覆盖控制台操作、API 调用、模型使用（调用/调优/部署）、限流配置及账单管理等多个维度，需结合 RAM 系统策略与百炼专属权限协同配置。

## 支持的模型/功能

- **模型级管控**：支持对文生文、文生图、语音合成等全部百炼托管模型进行独立的**调用授权**、**调优授权**和**部署授权**，且可按业务空间粒度开关。
- **功能模块访问控制**：通过页面级权限（如“模型体验-操作”“批量推理-操作”“模型观测-操作”）控制用户在控制台中可访问的功能入口，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的细粒度菜单表。
- **OpenAPI 接口权限**：默认关闭；需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用、知识库、Prompt 工程等 OpenAPI —— 此权限**不继承自业务空间管理员角色**，必须单独配置，参见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md#4adcb2854f9rv)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **业务空间（Workspace）** | 地域绑定的最小权限单元；同一地域下可创建多个空间，但**单个空间不可跨地域**。默认空间无法配置模型限流或调优限制。 | 必须明确指定地域（如 `cn-beijing`）和空间 ID |
| **API Key 归属** | 每个 API Key 严格绑定**一个地域 + 一个业务空间 + 一个用户**，不可迁移。其模型调用能力与限流策略完全继承自归属空间的配置，**不受用户控制台权限影响**。 | 参见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md#f2704153a055r) |
| **限流维度** | 支持双维度限流：<br>• **QPS/QPM（请求数）**<br>• **TPM（[Token](../concepts/token.md) 每分钟）** | 仅超级管理员可在全局管理菜单中为非默认空间设置；默认空间不支持配置 |
| **RAM 策略依赖** | 百炼控制台权限需配合 RAM 系统策略生效，例如：<br>• `AliyunBailianFullAccess` → 超级管理员<br>• `AliyunBailianDataFullAccess` → OpenAPI 全读写权限 | 策略需在 RAM 控制台绑定至对应 RAM 用户，非百炼控制台内配置 |

## 使用方式

1. **角色初始化**  
   - 主账号或具备 `AliyunRAMFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 为指定 RAM 用户附加 `AliyunBailianFullAccess`，使其成为超级管理员（参见 [设置超级管理员](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md#6f98e93909xdj)）。

2. **空间与模型授权**  
   - 超级管理员通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）为业务空间开通所需模型，并设置 QPM/TPM 限流值。

3. **用户权限分配**  
   - 在目标业务空间的**权限管理**页签中：  
     • 分配“管理员”角色 → 获得该空间内用户/页面/API Key 管理权；  
     • 分配“模型体验-操作”等页面权限 → 控制控制台功能可见性；  
     • 创建 API Key → 自动继承空间级模型与限流策略。

4. **OpenAPI 调用启用**  
   - 主账号在 RAM 控制台为该 RAM 用户额外添加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` —— 此步骤**不可省略**，否则即使拥有 API Key 也无法调用应用类 OpenAPI。

## 限制和注意事项

- > **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 同一表格中又列出“允许特定模型调用 & 限流”对超级管理员“支持”。该表述存在矛盾：实际行为是**默认空间的模型权限始终全开、不可关闭或限流**，表格中“支持”应理解为“支持查看状态”，而非“支持配置”。请以控制台实际禁用状态为准。

- > **注意**：API Key 的生命周期与 RAM 用户强耦合仅适用于 **2026年3月25日前创建的华北2（北京）API Key**；此后新建的 API Key 不受 RAM 用户删除影响。此变更已在 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md#f2704153a055r) 中明确标注，集成方需检查 API Key 创建时间并适配清理逻辑。

- **地域隔离刚性**：业务空间与地域强绑定，跨地域资源（如新加坡空间的模型）无法被北京空间直接调用或授权，必须分别在对应地域的全局管理菜单中独立配置。

- **账单与预付费权限独立**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授予，**不包含在 `AliyunBailianFullAccess` 内**，参见 [账单查看与预付费权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md#23e1b216deked)。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


