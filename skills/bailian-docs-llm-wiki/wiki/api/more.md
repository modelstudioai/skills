# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、知识库高级检索控制、临时凭证生成等关键功能。这些能力不直接参与模型推理，但为安全集成、精准数据访问和可信调用提供基础设施支持。开发者需根据具体场景按需启用，并严格遵循最小权限原则。

## 支持的模型/功能

`more` 不对应具体模型，而是支撑以下核心功能模块的底层能力：
- **服务关联角色（SLR）**：为工作流应用、数据管理、安全存储空间、模型监控等模块自动申请跨云服务访问权限（如 FC、OSS、ADB-PG、MNS、OpenTelemetry 等），详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口调用中对语义检索结果进行结构化字段级过滤（如单值、多值、范围、模糊、标签查询），提升 RAG 结果相关性；
- **临时 API Key 生成**：通过后端服务签发短期有效的访问令牌，用于浏览器或移动端等不可信环境的安全调用，避免永久密钥泄露。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾缺失 `log:Get*` 后续权限项），实际策略应以控制台或最新 SDK 返回为准；该问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中标注。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| SearchFilters | `searchFilters` | `Array<Object>` | 是 | 检索过滤条件数组，每个对象为一个 AND 分组，支持 `{"字段": "值"}`（单值）、`{"字段": "[\"v1\",\"v2\"]"}`（多值）、`{"字段": "{\"gte\":20,\"lte\":27}\"}`（范围）、`{"字段": "{\"like\":\"技%员\"}"}`（模糊）等格式 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| 临时 API Key | `expire_in_seconds` | `Integer` | 否 | 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |

## 使用方式

- **服务关联角色**：首次启用对应功能（如函数计算节点、OSS 数据导入）时由系统自动创建，无需手动调用 API；角色策略与权限已预置，禁止修改；
- **SearchFilters**：在调用 `Retrieve` 接口（[API 文档](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)）的请求体中传入 `searchFilters` 字段，需确保知识库字段类型与查询语法匹配（如 `age` 字段为 `double` 才支持 `gte`/`lte`）；
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久Key>` 的 POST 请求，可选添加 `expire_in_seconds` 查询参数；响应中的 `token` 可直接用于后续模型或知识库接口调用（如 `Authorization: Bearer st-****`）。

## 限制和注意事项

- **服务关联角色删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能完全失效（如工作流无法调用 FC），且删除前必须先清理所有关联资源（如已发布的应用、OSS 连接、ADB-PG 连接等）——详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **SearchFilters 依赖知识库结构**：仅对已配置为“参与检索”的字段生效；多值/范围/模糊查询需字段类型严格匹配（字符串字段不支持数值范围），否则返回空结果或报错；
- **临时 API Key 权限继承且不可撤销**：其权限范围完全等同于签发所用的永久 API Key，且到期前无法手动吊销；务必确保签发服务自身具备最小必要权限，并限制 `expire_in_seconds` 时长；
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将失败。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)


