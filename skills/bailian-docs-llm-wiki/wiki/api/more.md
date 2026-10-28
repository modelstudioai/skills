# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全鉴权机制与高级检索控制三大方向。它不构成独立服务，而是支撑工作流编排、知识库检索、数据接入、监控分析等核心功能的底层基础设施。开发者需根据具体使用场景（如调用函数计算、访问 OSS、过滤 RAG 结果）按需启用对应能力，并严格遵循权限最小化原则配置服务关联角色或临时凭证。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下功能提供关键支撑：

- **服务集成**：通过服务关联角色（SLR）实现与 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等云服务的安全对接。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算；[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)依赖 `AliyunServiceRoleForSFMDataHubOSSImport` 导入 OSS 数据；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForSFMAccessADB` 连接 ADB-PG 向量库。
- **安全鉴权**：提供生成临时 API Key 的能力，用于在不可信前端环境（如浏览器、App）中安全调用模型服务，避免永久密钥泄露。该能力由 `/api/v1/tokens` 接口提供，详见 [生成临时API Key](raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库检索增强**：支持在 `Retrieve` 接口请求中传入 `searchFilters`，对语义检索结果进行结构化过滤，显著提升 RAG 准确率，尤其适用于员工信息、产品文档等结构化知识库场景。详细用法见 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

| 参数 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `expire_in_seconds` | Integer | 临时 API Key 有效期，取值范围 `[1, 1800]` 秒（默认 60 秒） | [生成临时API Key](raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) |
| `searchFilters` | Array of Object | 检索过滤条件数组，每个元素为一个子分组（sub-group），支持 `AND`/`OR` 逻辑、单值/多值/范围/模糊/标签查询 | [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md) |
| `_operator` | String | 子分组内字段关系，可选 `"AND"`（默认）、`"OR"`（大小写不敏感） | [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md) |
| `_conditions` | Array of Object | 仅 RAG API 和 Spring AI SDK 支持，用于同一字段的多条件组合（如 `{"department": "Corporate"}` 和 `{"department": {"like": "%Research%"}}`） | [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md) |

> **注意**：OpenAPI Retrieve SDK 的 `searchFilters` 仅接受平铺 Map，不支持嵌套 `_conditions`。若传入嵌套结构，请求可能成功但过滤逻辑不生效，导致结果未按预期筛选 —— 此行为与 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md) 文档中“RAG API 或 Spring AI Alibaba”部分的描述存在矛盾，生产环境请优先使用 RAG API 或确认 SDK 版本兼容性。

## 使用方式

### 1. 服务关联角色（SLR）
- **自动创建**：首次在控制台开通对应功能（如函数计算节点、OSS 数据导入、ADB-PG 安全存储）时，系统自动创建所需 SLR。
- **手动管理**：可在 [RAM 控制台](https://ram.console.aliyun.com/) 的“角色管理”页查看、删除（需先解除功能依赖）所有 SLR。
- **权限验证**：各 SLR 绑定的系统策略（如 `AliyunServiceRolePolicyForSFMAccessFC`）已明确声明最小必要权限，禁止手动修改策略内容。

### 2. 生成临时 API Key
- **前提**：已在对应地域（北京/新加坡/弗吉尼亚/中国香港）创建永久 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`。
- **调用**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
       -H "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
- **响应**：返回 `token`（临时密钥）和 `expires_at`（UNIX 时间戳），过期后自动失效，**不可手动删除**。

### 3. 使用 SearchFilters
- **适用接口**：仅限知识库 `Retrieve` 接口（[API 文档](raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)）。
- **基本语法**（OpenAPI）：
  ```json
  {
    "indexId": "o73yjlxxxx",
    "query": "公司中姓名为张三的员工",
    "searchFilters": [
      {"姓名": "张三"},
      {"岗位": "技术员"}
    ]
  }
  ```
  表示“姓名=张三 **AND** 岗位=技术员”。

- **高级语法**（RAG API / Spring AI SDK）：
  ```json
  {
    "search_filters": [
      {
        "_operator": "OR",
        "_conditions": [
          {"department": "Corporate"},
          {"department": {"like": "%Research%"}}
        ]
      }
    ]
  }
  ```

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色（如 `AliyunServiceRoleForSFMAccessFC`）将导致其关联功能（工作流函数计算节点）**立即不可用**。删除前必须先解除所有业务依赖（如删除函数节点、断开 OSS/ADB 连接、停止数据导入任务），否则操作失败或引发功能中断。
- **临时 API Key 权限继承**：临时 Key 完全继承生成它的永久 Key 的全部权限（含模型访问、知识库读写等），**无法降权**。务必确保生成服务运行在可信后端，且永久 Key 本身已遵循最小权限原则。
- **SearchFilters 兼容性差异**：
  - OpenAPI SDK 不支持 `_conditions` 嵌套，同一字段多条件（如 `department` 等值 + 模糊）需改用 RAG API 或升级至支持该特性的 SDK 版本。
  - 所有 `searchFilters` 字段名必须与知识库 Schema 中定义的字段名**完全一致**（区分大小写），否则过滤无效。
- **地域隔离**：临时 API Key 的 Endpoint 与永久 API Key 所属地域强绑定（如新加坡地域 Key 必须调用新加坡 Endpoint），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


