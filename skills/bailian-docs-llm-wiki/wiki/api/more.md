# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大方向。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、可观测性集成等关键场景的底层基础设施。开发者需结合具体功能模块（如知识库、工作流、监控）按需启用和配置。

## 支持的模型/功能

`more` 本身**不提供独立模型**，而是为以下核心功能提供必要支撑：

- **服务关联角色（SLR）**：自动创建并托管云资源访问权限，支撑工作流调用函数计算（FC）、知识库对接 OSS/ADB-PG、数据管理接入 MNS/OSS、用量监控对接 OpenTelemetry/SLS/CMS 等能力。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：用于在不可信前端环境（如浏览器、App）中安全调用百炼 API，避免永久密钥泄露。其权限继承自生成所用的主 API Key。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级后置过滤，显著提升结构化数据（如员工表、产品目录）的召回精度。

## 关键参数

| 参数 | 所属功能 | 类型 | 说明 | 取值范围/示例 |
|------|----------|------|------|----------------|
| `expire_in_seconds` | 临时 API Key | Integer | 临时 Token 有效期（TTL） | `[1, 1800]` 秒，默认 `60`；示例：`?expire_in_seconds=1800` |
| `searchFilters` | 知识库检索 | Array of Objects | 过滤条件数组，支持子分组（AND）、子分组内字段逻辑（AND/OR）、单值/多值/范围/模糊/标签查询 | `[{ "姓名": "张三" }, { "岗位": "技术员" }]`；含 `_operator: "OR"` 或 `_conditions` 的嵌套结构（RAG API / Spring AI SDK） |
| `indexId` | 知识库检索 | String | 目标知识库索引 ID | 必填，由创建知识库时生成 |

> **注意**：`searchFilters` 的语法严格依赖调用方式——OpenAPI Retrieve（`bailian.cn-beijing.aliyuncs.com`）**仅支持平铺 Map 和 `_operator` 字段，不支持 `_conditions` 嵌套**；而 RAG API（`{workspace_id}.cn-beijing.maas.aliyuncs.com`）和 Spring AI Alibaba SDK 明确支持 `_conditions` 数组。混用会导致过滤失效，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 使用方式

### 1. 服务关联角色（SLR）
- **启用**：首次在控制台开通对应功能（如“工作流应用”、“安全存储空间”、“数据管理”）时，系统自动创建所需 SLR（如 `AliyunServiceRoleForSFMAccessFC`），无需手动操作。
- **查看**：前往 [RAM 控制台 > 角色管理](https://ram.console.aliyun.com/)，筛选“服务关联角色”。
- **删除**：必须先解除所有依赖该角色的功能（如删除函数计算节点、断开 OSS/ADB-PG 连接、停止数据导入任务），再通过 RAM 控制台删除。误删将导致对应功能完全不可用。

### 2. 生成临时 API Key
- **前提**：已创建永久 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。
- **调用**：向地域专属 Endpoint 发起 POST 请求：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
- **使用**：将响应中的 `token` 值作为 `Authorization: Bearer <token>` 用于后续 API 调用（如 `Retrieve`、`ChatCompletion`）。过期后需重新生成。

### 3. 使用 SearchFilters
- **前置**：确保知识库字段已正确映射为可检索属性（如 `姓名`、`年龄` 为 string/double 类型）。
- **构造**：
  - 简单 AND 过滤：`"searchFilters": [{"姓名": "张三"}, {"性别": "男"}]`
  - 同字段 OR 查询（RAG API）：`"searchFilters": [{"_operator": "OR", "_conditions": [{"部门": "Corporate"}, {"部门": {"like": "%Research%"}}]}]`
- **调用**：将 `searchFilters` 字段加入 `Retrieve` 请求体，与 `indexId`、`query` 同级。

## 限制和注意事项

- **SLR 删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将立即中断其关联功能（工作流无法调用 FC），且无回滚机制。务必按文档要求先清理依赖资源。
- **临时 API Key 不可撤销**：生成后只能等待自然过期（最长 1800 秒），无法主动吊销。应严格控制 `expire_in_seconds` 时长，并确保生成服务自身安全。
- **SearchFilters 兼容性陷阱**：OpenAPI Retrieve SDK **明确不支持 `_conditions` 嵌套语法**。若错误传入（如 `{"_conditions": [...]}`），请求可能成功但过滤无效，返回未过滤结果。请严格依据 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 文档选择语法。
- **权限继承原则**：临时 API Key 权限完全继承自生成它的永久 API Key。若永久 Key 无某知识库访问权限，则临时 Key 也无法访问。
- **地域隔离**：API Key、Endpoint、业务空间均按地域隔离（北京/新加坡/弗吉尼亚/中国香港），跨地域调用需使用对应地域的凭证与地址。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


