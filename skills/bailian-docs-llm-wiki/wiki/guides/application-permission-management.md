# application permission management

阿里云百炼支持基于控制台页面级、模型级的多维度权限控制，满足多地域、多用户的复杂组织架构需求。单个[业务空间](../concepts/workspace.md)是进行精细化权限管理（模型、用户）和阿里云账单分账的最小管理单元，权限管理围绕超级管理员、[业务空间](../concepts/workspace.md)管理员、普通用户三种角色展开。详细的角色定义与权限矩阵见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 角色体系

百炼的身份管理基于以下三种角色，权限范围自上而下递减：

- **超级管理员**：可跨空间统一管理用户权限、空间可用模型、空间模型限流和 [API Key](../concepts/api-key.md)。包含两类账号：阿里云主账号，以及拥有 `AliyunBailianFullAccess`（百炼管理员）系统策略的 RAM 用户。超级管理员可通过百炼全局管理菜单（北京 / 新加坡 / 弗吉尼亚）为任意 RAM 用户授权任意地域、任意空间的几乎所有权限，仅 OpenAPI 接口权限需阿里云主账号添加。
- **[业务空间](../concepts/workspace.md)管理员**：拥有访问某个[业务空间](../concepts/workspace.md)「权限管理」页面的 RAM 用户，只负责该特定[业务空间](../concepts/workspace.md)内的用户权限和资源管理。管理员权限包含可访问该[业务空间](../concepts/workspace.md)下所有页面的权限。
- **普通用户**：根据分配的权限使用资源，可访问/使用被授权的空间、页面、资源。

### 权限矩阵

| [业务空间](../concepts/workspace.md)权限 | 超级管理员 | [业务空间](../concepts/workspace.md)管理员 | 普通用户 |
| --- | --- | --- | --- |
| 允许特定模型调用 & 限流 | 支持 | 不支持 | 不支持 |
| 允许特定[模型调优](../concepts/fine-tuning.md) | 支持 | 不支持 | 不支持 |
| 允许特定[模型部署](../concepts/model-deployment.md) | 支持 | 不支持 | 不支持 |
| 用户管理 | 支持 | 支持 | 不支持 |
| 用户可用页面管理 | 支持 | 支持 | 不支持 |
| [API Key](../concepts/api-key.md) 管理 | 支持 | 支持 | 不支持 |
| 访问/使用被授权的空间、页面、资源 | 支持 | 支持 | 支持 |
| OpenAPI 接口权限 | 不支持 | 不支持 | 不支持 |

> **注意**：OpenAPI 接口权限不通过[业务空间](../concepts/workspace.md)角色授予，必须由阿里云主账号在 RAM 控制台为 RAM 用户添加专用系统策略。

## [业务空间](../concepts/workspace.md)权限管理

百炼按地理区域划分资源和[业务空间](../concepts/workspace.md)，**单个[业务空间](../concepts/workspace.md)不能跨地域存在**，即使是各地域的默认[业务空间](../concepts/workspace.md)，也是不同的空间。[业务空间](../concepts/workspace.md)是精细化权限管理的最小单元，可管理以下维度（默认[业务空间](../concepts/workspace.md)无法设置这些限制）：

- **限制模型调用**：管理某个模型可否在该[业务空间](../concepts/workspace.md)调用（控制台 & API），并设置该模型的请求数限流和 [Token](../concepts/token.md) 限流。默认[业务空间](../concepts/workspace.md)所有模型均可调用且无法限流。
- **限制模型训练**：管理某个模型可否在该[业务空间](../concepts/workspace.md)进行调优和调优后部署。默认[业务空间](../concepts/workspace.md)所有支持调优的模型均可调优及部署。
- **限制[模型部署](../concepts/model-deployment.md)**：管理某个模型可否在该[业务空间](../concepts/workspace.md)直接部署。默认[业务空间](../concepts/workspace.md)所有支持部署的模型均可部署。
- **用户控制台权限管理**：管理某个 RAM 用户是否能使用该业务空间控制台的功能及能使用哪些功能，但无法限制归属该用户的 [API Key](../concepts/api-key.md) 的调用。阿里云主账号无须设置，可访问所有业务空间的所有页面。

关于业务空间的地域隔离与限流细节，可进一步参考 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## API-Key 权限

单个 [API Key](../concepts/api-key.md) 只能归属一个地域内的一个业务空间和一个用户，且不能转移。[API Key](../concepts/api-key.md) 可调用的功能和模型限流与**归属业务空间**的权限保持一致，不受用户控制台权限管理的影响，也无需为不同模型（如文生文、文生图、语音合成）创建不同的 [API Key](../concepts/api-key.md)。

[API Key](../concepts/api-key.md) 的状态随归属用户操作变化：

| 触发操作 | 主账号的 [API Key](../concepts/api-key.md) | RAM 账号的 [API Key](../concepts/api-key.md) |
| --- | --- | --- |
| 主动删除 [API Key](../concepts/api-key.md) | 失效，不可恢复 | 失效，不可恢复 |
| 将账号移出业务空间 | — | 失效（重新加入后恢复生效） |
| 在 RAM 控制台删除账号/角色 | — | 失效，不可恢复 |
| 为 [API Key](../concepts/api-key.md) 设置 IP 访问白名单 | 华北2（北京）地域支持 | 华北2（北京）地域支持 |

> **注意**：自 2026 年 3 月 25 日起，华北2（北京）地域的所有新创建的 [API Key](../concepts/api-key.md) 均归属主账号。

可通过百炼控制台左侧导航栏「权限管理」页签为 RAM 用户添加 API-Key 权限，赋予其创建、删除、查看该空间下所有 API-Key 的权限。

## OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的数据、[知识库](../concepts/knowledge-base.md)、Prompt 工程及长期记忆等功能的 Open API。需由阿里云主账号在 RAM 控制台为 RAM 用户添加以下权限之一：

- `AliyunBailianDataFullAccess`：可调用百炼应用 API 目录下的所有 API。
- `AliyunBailianDataReadOnlyAccess`：可调用百炼应用 API 目录下的只读类 API，如 `DescribeFile`、`GetIndexJobStatus` 等。

## 账单与预付费权限

RAM 用户默认无权查看阿里云账单和购买预付费产品，需在 RAM 控制台添加特定权限。这两项权限会授予 RAM 用户查看**所有产品**账单或购买**所有预付费产品**的权限，请谨慎授权。

- 查看阿里云账单：添加 `AliyunBSSReadOnlyAccess`。
- 购买阿里云预付费产品：添加 `AliyunBSSOrderAccess`。

## 常用配置流程

### 设置超级管理员

需要阿里云主账号或具备 `AliyunRAMFullAccess` 系统策略的 RAM 用户操作。前往 RAM 控制台为 RAM 用户添加 `AliyunBailianFullAccess` 和 `AliyunBSSOrderAccess` 权限后，即可通过百炼全局管理菜单授权任意地域、空间的权限并购买预付费产品。

### 设置业务空间管理员

需超级管理员或业务空间管理员操作。在百炼控制台左侧导航栏「权限管理」页签内为 RAM 用户添加「管理员」权限。

### 设置模型调用权限

1. 不使用默认业务空间时，需先由超级管理员为业务空间开通特定模型的模型调用权限。
2. 通过控制台调用时，需由超级管理员或业务空间管理员为 RAM 用户添加：**模型体验-操作**（控制台调用模型）、**批量推理-操作**（支持批量推理）、**模型观测-操作**（查看 [Token](../concepts/token.md) 消耗量）。
3. 通过 API 调用时，需为 RAM 用户在对应业务空间创建或分配 API Key。

### 设置[模型调优](../concepts/fine-tuning.md)权限

1. 不使用默认业务空间时，需先由超级管理员为业务空间开通特定模型的[模型调优](../concepts/fine-tuning.md)（训练）权限。
2. 在「权限管理」页签内为 RAM 用户添加以下权限：**模型体验-操作**、**模型调优-操作**、**我的模型-操作**（管理调优后模型快照）、**[模型部署](../concepts/model-deployment.md)-操作**（部署调优后的模型）、**模型[评测](../concepts/evaluation.md)-操作**、**数据管理-操作**（管理调优数据集）、**模型观测-操作**。
3. 通过 API 调优时，无需额外控制台权限，只需为 RAM 用户分配 API Key 即可。

完整的权限配置流程与截图说明见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 生产环境实践

- **空间规划策略**：推荐按环境划分（开发 `project-dev-workspace`、测试 `project-test-workspace`、预发与生产 `project-prod-workspace`），实现严格的环境隔离；也可按业务线划分（如 `marketing-team-workspace`、`customer-team-workspace`），便于权限和成本管理。
- **限流策略**：将主账号总配额按比例分配给各业务空间并预留缓冲。例如账号总配额 1000 QPM，可分配生产 600 QPM（60%）、测试 200 QPM（20%）、开发 100 QPM（10%）、预留缓冲 100 QPM（10%），以应对突发流量。

## 限制与注意事项

- 业务空间不能跨地域存在；不同地域的默认业务空间也是不同空间。
- 默认业务空间无法设置模型调用、调优、部署限制，所有模型均按默认策略可用且无法限流。
- API Key 不可跨业务空间或跨用户转移；账号移出业务空间后其 API Key 失效，重新加入后恢复。
- OpenAPI 接口权限、账单与预付费权限必须由阿里云主账号在 RAM 控制台授权，业务空间管理员无法授予。
- `AliyunBSSReadOnlyAccess` / `AliyunBSSOrderAccess` 为全产品级权限，授权范围远超百炼本身，需谨慎。
- 开通 AI 安全护栏、模型监控、应用观测等功能，建议使用阿里云主账号在控制台一次性授权开通。

## 常见问题

- **如何获取业务空间 ID**：参考应用开发的「获取 Workspace ID」文档。
- **如何使用子业务空间调用模型**：无需特殊设置，使用子业务空间的 API Key 即可。
- **如何使用特定业务空间的应用**：使用 API 管理和调用特定业务空间的应用时，需同时设置 APP ID 和 Workspace ID。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)





















