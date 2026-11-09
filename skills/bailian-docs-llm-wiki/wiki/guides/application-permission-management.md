# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、细粒度的模型调用、调优、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、空间级管理和资源使用能力。所有 API Key 的调用权限均继承自其归属业务空间的模型策略，与用户账号的控制台权限解耦。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全部百炼托管模型的控制台与 API 调用权限控制（需先在业务空间启用该模型）  
- **模型调优（训练）**：支持对可调优模型（如 Qwen 系列）的训练任务创建、数据集管理、评测与快照发布权限控制  
- **模型部署**：支持对调优后模型或基础模型的在线服务部署权限控制  
- **控制台页面级权限**：支持按功能模块（如“模型体验”“批量推理”“数据管理”“模型观测”等）授予或限制 RAM 用户的界面操作能力  
- **API-Key 管理**：支持为 RAM 用户授权创建、删除、查看本业务空间全部 API Key 的能力，详见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)  

> **注意**：默认业务空间（default workspace）**不支持**任何模型级权限限制（调用、调优、部署均全开），如需精细化管控，必须新建独立业务空间 —— 该约束在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 文档中多次强调。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `region` | 业务空间所属地域，不可跨地域共享 | `cn-beijing`, `ap-southeast-1`, `us-east-1`, `cn-hongkong`（各地域业务空间完全隔离） |
| `workspace_id` | 业务空间唯一标识符，由系统生成 | 不可修改，不可迁移 |
| `model_code` | 模型唯一编码（如 `qwen-max`, `wanx-v1`） | 必须已在该业务空间显式启用（超级管理员操作） |
| `qpm_limit` / `tpm_limit` | 每分钟请求数 / 每分钟 [Token](../concepts/token.md) 数限流阈值 | 整数 ≥ 0；设为 `0` 表示禁用该模型调用 |
| `api_key_scope` | API Key 绑定范围 | 固定为单地域 + 单业务空间 + 单用户，不可变更 |

## 使用方式

### 1. 角色与权限分配
- **超级管理员**：需拥有 `AliyunBailianFullAccess` 策略（主账号或已授权 RAM 用户），通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置空间、模型、用户及 API Key  
- **业务空间管理员**：由超级管理员在对应空间的「权限管理」页签中，为 RAM 用户授予「管理员」角色，即可管理该空间内用户、页面权限及 API Key  
- **普通用户**：仅能使用被显式授权的控制台功能与模型；其 API 调用能力完全取决于所属空间分配的 API Key 及该空间的模型策略  

### 2. 模型权限开通流程（必经步骤）
1. 超级管理员在全局管理菜单中为业务空间**启用目标模型**（如 `qwen-plus`）并设置 `qpm_limit`/`tpm_limit`  
2. 业务空间管理员在「权限管理」→「用户权限」中为 RAM 用户分配对应功能权限（如“模型体验-操作”用于控制台调用，“模型调优-操作”用于训练）  
3. 若需 API 调用，须为该用户在**同一业务空间内创建或分配 API Key** —— 此 Key 自动继承空间级模型策略，无需额外配置模型白名单，详见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)  

### 3. OpenAPI 权限补充
RAM 用户默认**无权调用应用类 OpenAPI**（如知识库、[Prompt 工程](../concepts/prompt.md)、[长期记忆](../concepts/long-term-memory.md)等）。需主账号在 RAM 控制台为其附加以下任一策略：  
- `AliyunBailianDataFullAccess`（全读写）  
- `AliyunBailianDataReadOnlyAccess`（只读，适用于查询文件状态、知识库任务状态等）  
该要求与控制台权限正交，必须显式配置，参见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 部分。

## 限制和注意事项

- **地域强隔离**：业务空间严格绑定单一地域，北京空间的模型策略、API Key、用户权限**无法复用**于新加坡空间；跨地域需重复配置  
- **默认空间不可控**：`default` 业务空间禁止设置模型调用/调优/部署限制，生产环境务必使用自定义空间  
- **API Key 生命周期独立于 RAM 用户**：  
  - 2026年3月25日后创建的 API Key **不随 RAM 用户删除而失效**（推荐做法）  
  - 2026年3月25日前创建的 Key 与 RAM 用户级联，删除用户将**永久丢失 Key**，且不可恢复  
- **控制台权限 ≠ API 权限**：为用户授予“模型体验-操作”仅允许其在控制台调用模型；API 调用能力**完全依赖 API Key 所属空间的模型策略**，与该用户是否拥有控制台权限无关  
- **账单与预付费权限需单独授权**：RAM 用户默认无法查看账单或购买预付费资源，需主账号额外授予 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess` 策略  

> **注意**：文档中关于“超级管理员可添加中国香港地域管理入口”的描述（见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)），与当前控制台实际可用地域列表存在不一致 —— 截至 2024 年 Q3，中国香港地域尚未开放全局管理菜单入口，建议以控制台实时导航为准。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


