# more

`more` 是百炼平台面向高级集成与安全治理场景提供的一组扩展能力集合，涵盖临时凭证生成、服务关联角色（SLR）管理、以及知识库检索增强等核心功能。这些能力不直接参与模型推理，而是支撑应用安全调用、跨云服务协同和结构化语义检索等关键链路，适用于需在不可信环境运行、依赖外部云资源或对检索精度有强约束的开发者场景。

## 支持的模型/功能

- **临时 API Key 生成**：为浏览器、移动端等不可信客户端提供短期、可配置 TTL 的访问令牌，避免永久密钥泄露风险。该能力独立于具体模型，适用于所有支持 API 调用的百炼服务（如 `qwen-max`、`qwen-plus`、知识库 `retrieve` 等）[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于安全访问用户自有云资源（如 FC、OSS、ADB-PG、MNS、SLS 等）。不同功能模块绑定专属 SLR，权限最小化且策略明确，例如 `AliyunServiceRoleForSFMAccessFC` 仅允许 `fc:ListFunctions` 和 `fc:InvokeFunction` [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **知识库 SearchFilters**：在 `retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级后置过滤（如 `{"姓名": "张三"}`），显著提升结构化数据场景下的召回精准度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `}` 及完整 `Statement`），实际使用请以控制台或最新 SDK 返回的策略为准；完整策略定义请参考 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | Token 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤子分组列表，每个子分组内为 `key: value` 或 `key: {operator: value}` 形式 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gt`, `gte`, `lt`, `lte`, `eq`, `neq` | number/string | 否 | 字段操作符，用于数值或字符串等值/区间过滤 | `{"年龄": {"gte": 25, "lt": 30}}` |
| SearchFilters（模糊查询） | `like` | string | 否 | 字符串模糊匹配，支持 `%` 通配符 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需在 `Authorization` Header 中携带主账号的永久 `DASHSCOPE_API_KEY`。地域 Endpoint 需与主密钥所在地域一致（北京、新加坡、弗吉尼亚、中国香港），各地域密钥不互通 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色**：首次启用对应功能（如工作流中添加 FC 节点、安全存储空间绑定 OSS）时由系统自动创建，无需手动部署。角色删除前必须解除所有依赖（如删除函数计算节点、断开 OSS 连接），否则功能将中断 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **SearchFilters**：作为 `RetrieveRequest` 的顶层字段传入知识库 `retrieve` 接口（非 Query 参数），支持单值、多值、范围、模糊及标签五类查询语法。子分组间为 `AND` 逻辑，不可更改；同一子分组内多字段也为 `AND` [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- 临时 API Key **不可手动删除**，到期后自动失效；其权限完全继承自签发所用的永久 API Key，包括模型访问白名单与知识库权限。  
- 所有服务关联角色均受 RAM 权限管控，**禁止手动修改其策略内容或将其授予非百炼服务主体**；删除前必须按文档要求完成依赖清理，否则将导致对应功能不可用。  
- `searchFilters` 仅作用于 `retrieve` 接口返回的 `nodes` 列表，**不影响语义检索本身的向量相似度计算过程**，属于结果后过滤机制；若知识库未正确配置字段类型（如将数字字段设为 string），范围查询可能失效。  
- > **注意**：文档 3 的 Python 示例中 `multi_query()` 方法使用 `json.dumps(names)` 构造多值，但实际 SDK（`alibabacloud_bailian20231229` v1.0.10+）已原生支持 `List[str]` 直接赋值，无需手动序列化；旧版示例存在兼容性风险，建议优先采用 `{"姓名": ["张三", "李四"]}` 格式。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


