# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三级，分别对应全局管理、空间级管理和资源使用能力。所有 API Key 的调用权限严格继承自其归属业务空间的模型配置，与用户账号的控制台权限解耦。

## 支持的模型/功能

权限管理覆盖以下核心能力：
- **模型调用**：控制台体验、批量推理、模型观测（Token 消耗统计），需显式开通模型在业务空间的“可调用”状态并授予用户对应操作权限；
- **模型调优（训练）**：支持对已授权模型进行微调（Fine-tuning），需业务空间级开启“允许特定模型调优”，且用户需具备 `模型调优-操作` 权限；
- **模型部署**：支持将调优后模型或基础模型直接部署为服务，依赖业务空间级“允许特定模型部署”开关；
- **控制台页面权限**：按菜单粒度控制用户可见性与操作能力（如是否可见“知识库”“Prompt 工程”等子页），但**不影响 API 调用能力**；
- **API Key 管理**：支持创建、删除、查看本空间内所有 API Key，该权限需单独授予（见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）；
- **OpenAPI 接口权限**：默认禁用，需主账号在 RAM 控制台为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：文档中多次出现“默认业务空间无法设置模型调用/调优/部署限制”，但实际在控制台中，部分新创建的默认空间已支持基础限流配置。建议以控制台实时界面为准，或参考最新版 [权限管理概述](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的说明。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `业务空间地域` | 业务空间绑定唯一地域（如 `cn-beijing`），不可跨地域共享；API Key 仅在其归属地域生效 | 必填，创建时确定 |
| `模型调用开关` | 控制台中“模型管理”页下针对单个模型的“启用/禁用”开关，决定该模型是否可在本空间被调用（含 API 和控制台） | 仅超级管理员可配置 |
| `QPM / TPM 限流值` | 每分钟请求数（QPM）与每分钟 Token 数（TPM）上限，作用于整个业务空间对该模型的全部调用（含所有 API Key） | 仅超级管理员可设置 |
| `API Key 归属用户` | 单个 API Key 绑定且仅绑定一个 RAM 用户，但其调用权限由所属业务空间的模型配置决定，**不受该用户控制台权限影响** | 创建时指定，不可迁移 |
| `IP 白名单` | 仅华北2（北京）地域支持，用于限制 API Key 的调用来源 IP 段 | 配置在 API Key 级别 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置；  
   - 业务空间管理员：由超级管理员在目标空间的 **权限管理 → 用户管理** 中为 RAM 用户勾选“管理员”角色（见 [设置业务空间管理员](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

2. **模型权限开通流程**  
   - 超级管理员进入全局管理 → 选择业务空间 → “模型管理”，为所需模型开启“调用”“调优”或“部署”开关；  
   - 业务空间管理员进入该空间 → “权限管理 → 用户管理”，为 RAM 用户分配对应操作权限（如“模型体验-操作”）；  
   - 若需 API 调用，须在“权限管理 → API Key 管理”中为该用户创建或分配 API Key。

3. **OpenAPI 调用准备**  
   - 主账号登录 RAM 控制台 → 找到目标 RAM 用户 → 添加 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略；  
   - 注意：该策略授权范围为百炼应用层 OpenAPI（如知识库、数据连接等），不包含模型推理类接口（后者由业务空间模型开关控制）。

## 限制和注意事项

- **默认业务空间无权限管控能力**：所有模型默认可调用、可调优、可部署，且无法设置限流；生产环境务必使用**非默认业务空间**；
- **API Key 与用户权限分离**：即使用户被移出业务空间，其已创建的 API Key 在重新加入后自动恢复生效；但若其 RAM 账号被从 RAM 控制台删除，则 API Key 永久失效；
- **地域强隔离**：同一 RAM 用户在不同地域的业务空间需分别授权，API Key 不跨地域复用；
- **账单与预付费权限独立**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需主账号在 RAM 控制台显式授予，不随百炼权限自动继承；
- **OpenAPI 权限不自动同步**：即使用户是业务空间管理员，若未在 RAM 控制台添加 `AliyunBailianData*Access` 策略，仍无法调用应用层 OpenAPI（如 `/v1/knowledge_bases`）；
- **华北2（北京）特殊规则**：自 2026年3月25日起，该地域所有新创建 API Key 默认归属主账号，RAM 用户需由主账号代为创建并分配。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


