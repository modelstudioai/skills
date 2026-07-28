# 业务空间

业务空间（Workspace）是阿里云百炼平台上进行资源隔离、精细化权限管理和账单分账的最小管理单元。每个业务空间归属于一个地域，**不能跨地域存在**——即使是各地域的默认业务空间，也是彼此独立的空间。

## 核心特性

- **地域隔离**：百炼按地理区域（北京、上海、新加坡、弗吉尼亚等）划分资源，业务空间从属于单一地域。
- **默认空间与子空间**：每个地域有一个默认业务空间，其下可创建多个子业务空间。默认业务空间的 API Key 拥有所有模型的调用权限，且**无法设置**模型调用/训练/部署限制和空间级[限流](rate-limit.md)；需要精细化隔离时应创建独立的子业务空间。
- **API Key 归属**：单个 API Key 只能归属一个地域内的一个业务空间和一个用户，且不能转移。API Key 可调用的功能和模型[限流](rate-limit.md)与归属业务空间的权限保持一致，不受用户控制台权限管理影响。

## 在不同场景中的使用

### 权限管理

权限体系围绕三种角色展开：**超级管理员**（主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户，可跨空间管理）、**业务空间管理员**（仅管理特定空间内的用户与资源）、**普通用户**（使用被授权的空间、页面、资源）。超级管理员可按空间维度控制：

- 特定模型是否允许在该空间调用（控制台与 API），并设置请求数[限流](rate-limit.md)和 Token 限流；
- 特定模型是否允许在该空间调优、调优后部署或直接部署；
- RAM 用户在该空间控制台可访问哪些页面。

### 模型调用（子业务空间）

按业务线隔离权限或分账时，使用子业务空间的模型调用：

- 必须使用子空间自身的 API Key 调用；
- 调用标准模型（如 `qwen-plus`）前需先为该空间设置模型调用权限；
- 在百炼上调优并部署的模型无需额外授权，但仅能由其所在空间的 API Key 调用，且仅支持 DashScope 方式。

### API 端点

部分 OpenAI 兼容端点将业务空间 ID 嵌入域名，调用时需替换为真实值，例如文本向量接口：

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings
```

### 监控与观测

- **模型用量**页面按业务空间维度统计调用量、Token 消耗与费用（不支持按阿里云账号维度统计）。
- **模型监控**按"模型 + 业务空间"维度生成监控列表；默认业务空间成员可查看所有空间数据，子空间成员仅能查看当前空间。Prometheus 高级监控指标支持 `workspace_id` 作为过滤标签。
- **应用观测**只能观测当前业务空间内已发布的应用；若列表中找不到应用，常见原因是应用不属于当前空间。

## 关键配置要点

| 配置项 | 说明 |
| --- | --- |
| 模型调用授权与限流 | 超级管理员按空间控制模型可用性，并设置 RPS / Token 限流（默认空间不可设置） |
| 模型训练/部署权限 | 按空间限制特定模型的调优与部署（默认空间不可设置） |
| 用户页面权限 | 控制 RAM 用户在该空间控制台可用的页面，不影响其 API Key 调用 |
| WorkspaceId | 子空间调用部分接口时需在 Endpoint 或请求中指定真实的业务空间 ID |

## 最佳实践

- 生产环境建议按开发、测试、预发、生产划分独立业务空间，并为生产空间预留更高限流配额和更严格的用户权限。
- 需要按业务线分账或限制模型使用范围时，创建子业务空间而非在默认空间内混用。
- OpenAPI 接口权限不通过业务空间角色授予，需主账号在 RAM 控制台为 RAM 用户添加专用系统策略（如 `AliyunBailianDataFullAccess`）。

## 关联主题页

- [application permission management](../guides/application-permission-management.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application monitoring](../guides/application-monitoring.md)
- [vector and sort](../api/vector-and-sort.md)
- [more about models](../api/more-about-models.md)
- [model monitoring](../guides/model-monitoring.md)


