# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、知识库高级检索控制、临时凭证生成等关键功能。这些能力不直接参与模型推理，但为安全集成、精准数据访问和可信调用提供基础设施支持。开发者需根据具体场景按需启用，并严格遵循最小权限原则。

## 支持的模型/功能

`more` 不对应具体模型，而是支撑以下核心功能模块的底层能力：

- **服务关联角色（SLR）**：为百炼与外部云服务（如 FC、OSS、ADB-PG、MNS、SLS 等）的安全交互提供托管式权限委托。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForSFMAccessADB` 访问 ADB-PG 向量库 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级后过滤，显著提升结构化数据（如员工信息表）的召回精度 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **临时 API Key 生成**：通过后端服务调用 `/tokens` 接口，为前端不可信环境（如浏览器、App）签发短期有效的访问令牌，避免永久密钥泄露风险 [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的策略定义被截断（末尾缺失 `log:Get*` 后续权限及完整 JSON），实际使用时请以控制台或最新版 RAM 策略为准。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 有效期（秒），范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个对象为一个 AND 分组，支持单值、多值、范围、模糊、Tag 查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gt`, `gte`, `lt`, `lte`, `eq`, `neq` | string/number | — | 字段比较操作符，仅数值字段支持区间，字符串支持等值 | `{"年龄": {"gte": 20, "lte": 27}}` |
| SearchFilters（模糊查询） | `like` | string | — | 字符串字段模糊匹配，`%` 通配任意字符 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

- **服务关联角色**：首次开通对应功能（如函数计算节点、OSS 数据导入）时由系统自动创建，无需手动调用 API。角色名称与权限策略已预置，详见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **SearchFilters**：在 `POST /retrieve` 请求体中直接嵌入 `searchFilters` 字段，需确保知识库字段类型与查询语法匹配（如 `age` 字段为 `double` 才支持 `gte`）。完整示例见 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <permanent_key>` 的 POST 请求，可选 `expire_in_seconds` 查询参数。响应中的 `token` 可直接用于后续模型或知识库 API 调用。

## 限制和注意事项

- **服务关联角色删除风险高**：删除任一 SLR 均将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的函数计算节点无法调用）。删除前必须先解除所有业务依赖（如删除函数节点、断开 OSS/ADB 连接等），否则操作将被拒绝。
- **SearchFilters 语法约束**：
  - 子分组间固定为 `AND` 逻辑，不可配置 `OR`；
  - 多值查询需用 `json.dumps(["val1","val2"])` 序列化为字符串；
  - 标签（Tag）查询仅适用于文档/音视频类知识库，且多个 Tag 间为 `OR` 关系。
- **临时 API Key 权限继承与不可撤销**：临时 [Token](../concepts/token.md) 完全继承签发者 API Key 的全部权限（含模型、知识库白名单），且**无法手动删除或提前失效**，仅能等待自然过期。务必确保签发服务自身权限最小化。
- **地域隔离**：临时 API Key 的 Endpoint 与签发所用 API Key 地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将失败。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)


