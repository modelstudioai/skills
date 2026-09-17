# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制和高级检索控制等功能。它不直接提供模型推理服务，而是支撑工作流编排、知识库精准检索、数据接入与监控等关键场景的底层能力。开发者需结合具体业务需求，按需启用并配置相关功能。

## 支持的模型/功能

`more` 本身不对应具体模型，而是为以下核心功能提供基础设施支持：

- **服务关联角色（SLR）**：为百炼各模块访问外部云资源（如 FC、OSS、ADB-PG、MNS、OpenTelemetry 等）提供最小权限委托机制。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算节点；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForAccessOSS` 和 `AliyunServiceRoleForSFMAccessADB` 分别对接 OSS 与 ADB-PG [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用百炼 API，避免永久密钥泄露。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行二次精筛，显著提升 RAG 场景下结构化数据（如员工表、产品目录）的召回精度 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺少闭合括号及完整 `Statement`），实际策略应以控制台或最新 SDK 返回为准；该问题已在 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中标记为待修复。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| SearchFilters | `searchFilters` | Array of Object | 否 | 检索过滤子分组列表，每个子分组内字段支持单值、多值、范围（`gte`/`lte`）、模糊（`like`）、标签（`tags`）查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |

## 使用方式

- **服务关联角色**：首次启用对应功能（如创建函数计算节点、导入 OSS 数据、配置安全存储空间）时，系统自动创建 SLR；无需手动调用 API。角色名称与策略已预置，详见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口生成，需在请求头 `Authorization: Bearer <permanent_api_key>` 中携带有效永久密钥。地域 Endpoint 需与密钥所在地域一致（如北京、新加坡、弗吉尼亚、中国香港）。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接传入 `searchFilters` 字段，支持 JSON 格式嵌套。需确保知识库字段已正确映射为可检索属性（如 `姓名`、`年龄` 为 string/double 类型），且子账号已获得 `AliyunBailianDataFullAccess` 权限并加入对应业务空间 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流无法调用 FC）。删除前必须先清理所有依赖该角色的资源（如发布态应用、OSS 导入任务、ADB 连接等），否则操作失败。
- **临时 API Key 不可撤销**：生成后仅能等待过期（最长 30 分钟），不支持主动吊销。务必严格控制 `expire_in_seconds` 值，避免过度授权。
- **SearchFilters 语法约束**：
  - 子分组间为固定 `AND` 逻辑，不可修改；
  - 多值查询需使用 `json.dumps(["val1","val2"])` 编码为字符串；
  - 模糊查询 `like` 值中 `%` 为通配符，`_` 匹配单字符；
  - 标签（`tags`）查询仅适用于文档/音视频类知识库，且多个标签为 `OR` 关系。
- **权限隔离**：子账号只能操作其已加入的业务空间内的资源；主账号无此限制。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


