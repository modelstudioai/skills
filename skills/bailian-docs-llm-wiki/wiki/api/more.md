# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务关联角色管理、临时认证凭证生成、知识库高级检索过滤等关键功能，用于增强模型应用的安全性、可观测性和数据精准性。这些能力不直接参与模型推理，而是支撑工作流编排、数据接入、权限隔离与结果后处理等生产级需求。开发者需结合具体场景按需启用，并严格遵循最小权限原则。

## 支持的模型/功能

`more` 本身不对应具体模型，而是为以下核心功能提供底层支撑：

- **服务关联角色（SLR）**：为百炼各子系统（如工作流应用、数据管理、安全存储空间、模型监控等）自动申请并托管对其他云服务（FC、OSS、ADB-PG、MNS、OpenTelemetry 等）的访问权限。例如，`AliyunServiceRoleForSFMAccessFC` 支持函数计算节点调用，`AliyunServiceRoleForSFMDataHubOSSImport` 支持 OSS 数据导入 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：面向不可信前端环境（如浏览器、移动 App）提供短期有效的认证凭证，避免永久密钥泄露风险 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级精筛（如 `{"姓名": "张三"}`），显著提升 RAG 场景下结构化数据的召回准确率 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `]` 及完整 JSON 结构），实际部署时请以控制台或 RAM 策略详情页展示的完整策略为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中明确标注。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 有效期（秒），范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个元素为一个子分组（AND 语义） | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（单值） | 字段名（如 `"年龄"`） | String / Number | 否 | 支持字符串或数值类型字段的精确匹配 | `"张三"` 或 `25` |
| SearchFilters（范围） | 字段名 + `gt`/`gte`/`lt`/`lte` | Object | 否 | 仅支持数值字段的区间查询 | `{"年龄": {"gte": 20, "lte": 30}}` |
| SearchFilters（模糊） | 字段名 + `like` | Object | 否 | 字符串字段模糊匹配（`%` 通配） | `{"岗位": {"like": "技%员"}}` |

## 使用方式

- **服务关联角色**：首次启用依赖该角色的功能（如发布含 FC 节点的工作流）时，系统自动创建；无需手动调用 API。角色名称与策略已预置，开发者只需确保对应云服务资源（如 OSS Bucket、ADB-PG 实例）已存在且标签合规（如 `bailian-safe-workspace-oss-access: ReadAndWrite`）。
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口生成，需在请求头 `Authorization: Bearer $DASHSCOPE_API_KEY` 中传入有效永久密钥。生成后直接用于后续模型调用（如 `Authorization: Bearer st-****`）[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters**：在 `RetrieveRequest` 请求体中作为顶层字段传入，格式为 JSON 数组。各子分组内支持单值、多值、范围、模糊、标签五类查询语法，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **服务关联角色**：
  - 删除前必须解除所有依赖关系（如删除工作流中的 FC 节点、断开安全存储空间的 OSS/ADB-PG 连接），否则功能将中断；
  - 角色权限由百炼预定义，**禁止手动修改策略内容或将其授予非服务关联角色的 RAM 实体**（如用户、用户组）；
  - `AliyunServiceRoleForSFMAccessingMNS` 明确要求“请勿修改、删除，或将其授予除服务关联角色之外的任何RAM身份”。

- **临时 API Key**：
  - 生命周期固定，**无法提前撤销或删除**，仅能等待过期；
  - 权限完全继承自签发它的永久 API Key，若后者被禁用或权限变更，临时 Key 将立即失效；
  - 各地域 Endpoint 独立（北京、新加坡、弗吉尼亚、中国香港），密钥不可跨地域复用。

- **SearchFilters**：
  - 仅作用于 `Retrieve` 接口，不影响向量索引构建过程；
  - 子分组间强制 `AND` 逻辑，不支持 `OR` 或嵌套布尔表达式；
  - 多值查询需使用 `json.dumps()` 序列化为字符串（如 Python SDK 示例所示），原始字段值类型必须与知识库索引配置一致（如 `年龄` 字段在知识库中需定义为 `double` 类型）。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


