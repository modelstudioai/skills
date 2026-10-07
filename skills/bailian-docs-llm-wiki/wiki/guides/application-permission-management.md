# application permission management

百炼平台的权限管理基于“业务空间”这一最小管理单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、用户访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保资源隔离与安全可控。所有权限策略均与阿里云 RAM 深度集成，需结合 RAM 策略与百炼控制台配置协同生效。

## 支持的模型/功能

权限管理覆盖以下关键能力：

- **模型调用**：控制台模型体验、批量推理、模型观测；API 层面的 `InvokeModel` 等调用能力  
- **模型调优（训练）**：支持在控制台或通过 OpenAPI 启动微调任务，并部署调优后模型  
- **模型部署**：直接部署官方模型或调优后模型为服务端点  
- **控制台页面级权限**：按菜单/子菜单粒度控制用户可见性与操作权（如是否显示“知识库”“Prompt 工程”等页签）  
- **API Key 全生命周期管理**：创建、查看、删除归属本空间的 API Key，并支持 IP 白名单（仅华北2北京地域）  
- **OpenAPI 接口权限**：对应用层数据、知识库、Prompt 工程、[长期记忆](../concepts/memory.md)等组件的读写权限（需显式授予 RAM 策略）  

> **注意**：默认业务空间**不支持**设置模型调用/调优/部署限制，所有模型均默认可用且不可限流；如需精细化管控，必须使用非默认业务空间。详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `region` | 业务空间所属地域，**不可跨地域共享** | `cn-beijing`, `ap-southeast-1`, `us-east-1`, `cn-hongkong`（各地域空间独立） |
| `workspace_id` | 业务空间唯一标识，由系统生成 | 不可修改，不可迁移 |
| `model_call_quota_qpm` | 模型每分钟请求数限流（QPM） | ≥ 0；0 表示禁用该模型调用 |
| `model_call_quota_tpm` | 模型每分钟 [Token](../concepts/token.md) 数限流（TPM） | ≥ 0；0 表示禁用该模型调用 |
| `api_key_ip_whitelist` | API Key 访问白名单（CIDR 格式） | 仅华北2（北京）地域支持；最多 10 个 IP 段 |
| `ram_policy` | 绑定的 RAM 策略（必需） | `AliyunBailianFullAccess`（超级管理员）、`AliyunBailianDataFullAccess`（OpenAPI 全读写）等，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |

## 使用方式

### 1. 角色与权限分配
- **超级管理员**：需主账号或已绑定 `AliyunBailianFullAccess` 的 RAM 用户，在全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://bailian.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)｜[中国香港](https://bailian.console.aliyun.com/cn-hongkong?tab=globalset#/efm/business_management)）中统一配置空间、模型、用户及 API Key。  
- **业务空间管理员**：由超级管理员或同空间其他管理员在**权限管理 > 用户管理**中为 RAM 用户授予“管理员”角色，获得该空间内除全局设置外的全部操作权。  
- **普通用户**：由管理员在**权限管理 > 用户管理**中分配具体页面权限（如“模型体验-操作”“知识库-读写”）及模型调用权限。

### 2. 模型权限开通流程
1. 超级管理员在全局管理菜单中为业务空间**启用目标模型**（如 `qwen-max`），并配置 QPM/TPM 限流值；  
2. 管理员在该空间的**权限管理 > 用户管理**中，为 RAM 用户分配对应模型的控制台操作权限（如“模型体验-操作”）；  
3. 若需 API 调用，须为该用户在**权限管理 > API Key 管理**中创建或分配 API Key —— 其可用模型与限流策略**完全继承自归属业务空间**，与用户个人控制台权限无关。详情见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

### 3. OpenAPI 权限开通
RAM 用户默认**无权调用任何应用层 OpenAPI**（如知识库、Prompt 工程相关接口）。必须由阿里云主账号在 [RAM 控制台](https://ram.console.aliyun.com/users) 显式授予以下任一策略：
- `AliyunBailianDataFullAccess`：全量读写权限  
- `AliyunBailianDataReadOnlyAccess`：仅只读类接口（如 `DescribeFile`, `GetIndexJobStatus`）  

> **注意**：`AliyunBailianData*` 系列策略仅作用于应用组件 API，**不包含模型推理 API（如 `InvokeModel`）**；后者由业务空间模型调用权限控制，无需额外 RAM 策略。

## 限制和注意事项

- **地域强隔离**：业务空间严格绑定单一地域，北京空间的模型权限、API Key、用户配置无法同步至新加坡空间；跨地域需分别配置。  
- **API Key 归属锁定**：单个 API Key 仅归属一个地域+一个业务空间+一个 RAM 用户，**不可转移、不可跨空间复用**；删除用户或将其移出空间将导致其 API Key 失效（重新加入可恢复）。  
- **默认空间无管控能力**：默认业务空间无法设置模型调用/调优/部署限制，亦无法配置限流；生产环境务必使用显式创建的非默认空间。  
- **主账号特权**：开通 AI 安全护栏、模型监控、应用观测等功能，以及为 RAM 用户授予账单/预付费权限（如 `AliyunBSSReadOnlyAccess`），**必须由阿里云主账号操作**，RAM 用户即使拥有 `AliyunBailianFullAccess` 也无法完成。  
- **时间敏感变更**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key **自动归属主账号**，不再支持归属 RAM 用户 —— 此变更已在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确标注。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


