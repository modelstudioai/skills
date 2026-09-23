# more

`more` 是百炼平台为高级集成与安全治理场景提供的扩展能力集合，涵盖临时凭证分发、服务关联角色（SLR）授权、以及知识库检索增强等核心功能。这些能力不直接参与模型推理，而是支撑应用安全、资源互通与精准检索等关键环节。开发者需根据具体使用场景选择对应子能力，并严格遵循权限最小化原则。

## 支持的模型/功能

`more` 本身不提供模型服务，而是支撑以下三类关键功能：

- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用模型 API，避免永久密钥泄露。该能力通过 `/api/v1/tokens` 接口提供，详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **服务关联角色（SLR）管理**：百炼通过预置 SLR 自动获取对 FC、OSS、ADB-PG、MNS 等云服务的受控访问权限，支撑工作流、数据导入、安全存储、知识库向量化等场景。完整角色列表及权限策略见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **知识库 SearchFilters 检索过滤**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级精确筛选（如 `{"姓名": "张三"}`），显著提升 RAG 场景下结构化数据的召回精度。用法说明见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `}` 和 `]`），实际策略应以 RAM 控制台或最新版 SDK 返回为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中明确标注。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个对象为一个 AND 分组，支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，需嵌套在字段值中（JSON string 化） | `{"年龄": "{\"gte\": 20, \"lte\": 30}\"}` |

## 使用方式

- **临时 API Key**：  
  后端服务调用 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800`，携带 `Authorization: Bearer <PERMANENT_API_KEY>`。响应返回 `token`（如 `st-****`）和 `expires_at`（UNIX 时间戳）。前端后续所有模型请求均使用该 `token` 替代永久密钥。

- **服务关联角色**：  
  首次启用对应功能（如创建函数计算节点、配置 OSS 数据源）时，百炼自动创建所需 SLR。无需手动调用 API，但需确保主账号具备 `ram:CreateServiceLinkedRole` 权限。角色删除前必须解除所有依赖资源（如删除工作流中的 FC 节点、断开安全存储空间的 OSS 连接），详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

- **SearchFilters**：  
  在 `RetrieveRequest` 请求体中直接传入 `searchFilters` 字段。需确保知识库字段已正确映射为可检索类型（如 `string` 或 `double`），且字段名与原始数据表列名一致。Python SDK 示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- 临时 API Key **不可撤销**，仅能等待自然过期（最长 1800 秒）。其权限完全继承自签发所用的永久 API Key，**切勿使用高权限密钥生成前端可用 [Token](../concepts/token.md)**。
- 所有 SLR 均绑定特定服务主体（如 `fc.sfm.aliyuncs.com`），**禁止手动修改策略或将其授予非百炼服务的其他实体**；删除 SLR 将导致对应功能立即中断，且部分角色（如 `AliyunServiceRoleForSFMAccessingMNS`）明确禁止删除。
- SearchFilters 仅作用于 `Retrieve` 接口，**不适用于 `ChatCompletion` 或 `Embedding` 等模型接口**；多值查询需对数组进行 `json.dumps()` 序列化后作为字符串传入字段值；标签（Tag）查询仅支持文档/音视频类知识库。
- 地域隔离：临时 API Key 接口 Endpoint 与永久 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将失败。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


