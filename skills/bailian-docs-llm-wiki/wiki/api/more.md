# more

本主题汇总百炼平台在应用接入与数据检索中常用的几项辅助能力：临时 [API Key](../concepts/api-key.md) 生成、服务关联角色（SLR）管理，以及[知识库](../concepts/knowledge-base.md) Retrieve 接口的 SearchFilters 过滤语法。它们分别覆盖安全鉴权、跨云服务授权与结构化数据检索过滤三个场景，详细说明可参见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)、[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 与 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 生成临时 [API Key](../concepts/api-key.md)

在浏览器、移动 App 等不可信环境中调用模型服务时，应通过后端服务生成临时 [API Key](../concepts/api-key.md)，避免永久 [API Key](../concepts/api-key.md) 泄露。临时 [API Key](../concepts/api-key.md) 继承生成它的永久 [API Key](../concepts/api-key.md) 的全部权限（包括对特定模型或[知识库](../concepts/knowledge-base.md)的访问限制），到期后自动失效，无法提前删除。

**前提条件**：在百炼密钥管理页面（北京 / 新加坡 / 弗吉尼亚）创建永久 [API Key](../concepts/api-key.md)，并将其配置为环境变量 `DASHSCOPE_API_KEY`。

**请求**：

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**关键参数**：

| 参数 | 说明 |
| --- | --- |
| `expire_in_seconds` | 临时 Key 有效期（TTL），单位秒，范围 `[1, 1800]`，默认 60 秒。 |

**正常响应**：

```json
{
  "token": "st-****",
  "expires_at": 1744080369
}
```

`token` 为生成的临时 [API Key](../concepts/api-key.md)，`expires_at` 为过期 UNIX 时间戳（秒）。错误响应包含 `code`、`message`、`request_id` 三段，常见如 `InvalidApiKey`。

> **注意**：各地域（北京 / 新加坡 / 弗吉尼亚）的 [API Key](../concepts/api-key.md) 不互通，请求时需使用对应地域的 Endpoint 与永久 Key。

## 服务关联角色（SLR）

百炼在实现特定功能时，需通过服务关联角色（Service Linked Role, SLR）访问其他云服务（如 FC、OSS、ADB-PG、MNS、内容安全、SLS、CMS、DTS、CPFS 等）。当您首次在百炼中开通相关功能（如函数计算节点、OSS 数据导入、安全存储空间等）时，系统会**自动创建**对应的 SLR，无需手动创建。所有 SLR 可在 [RAM 控制台](https://ram.console.aliyun.com/) 的角色管理页面查看。

**主要 SLR 与用途**：

| 服务关联角色 | 用途 |
| --- | --- |
| `AliyunServiceRoleForSFMAccessFC` | [工作流](../concepts/workflow.md)应用 / 流程编排访问函数计算（FC）资源 |
| `AliyunServiceRoleForSFMDataHubOSSImport` | 数据管理从 OSS 导入数据 |
| `AliyunServiceRoleForAccessOSS` | 安全存储空间访问 OSS |
| `AliyunServiceRoleForSFMAccessADB` | [知识库](../concepts/knowledge-base.md) / 安全存储空间访问 ADB-PG 实例 |
| `AliyunServiceRoleForSFMAccessingMNS` | 数据管理访问 MNS 队列中的 OSS 变更消息 |
| `AliyunServiceRoleForSFMTelemetry` | 用量监控与性能分析访问 OpenTelemetry 实例 |
| `AliyunServiceRoleForSFMAccessingCIP` | 百炼应用访问内容安全服务 |
| `AliyunServiceRoleForSFMAccessSLS` | 模型监控访问 SLS 资源 |
| `AliyunServiceRoleForSFMAccessCMS` | 模型监控访问 CMS 资源 |
| `AliyunServiceRoleForAccessCusOss` | 百炼平台托管操作用户 OSS 文件 |
| `AliyunServiceRoleForSFMConnectorAccessDTS` | 创建和管理 DTS 任务，从数据源接入数据 |
| `AliyunServiceRoleForSFMFineTuning` | [模型调优](../concepts/fine-tuning.md) / 数据管理访问 CPFS 与 OSS |

每个 SLR 关联一个固定的系统策略（如 `AliyunServiceRolePolicyForSFMAccessFC`），策略中通过 RAM 条件（`ram:ServiceName`）限定只能由百炼服务使用，请勿修改或授予其他 RAM 身份。

**删除前注意事项**：删除 SLR 会导致对应功能不可用，须先清理依赖资源。例如删除 `AliyunServiceRoleForSFMAccessFC` 前须先删除所有已发布[工作流](../concepts/workflow.md)应用和流程中的函数计算节点并重新发布；删除 `AliyunServiceRoleForAccessOSS` 前须在安全存储空间中断开所有 OSS 连接；删除 `AliyunServiceRoleForSFMDataHubOSSImport` 前须确保没有进行中的 OSS 数据导入任务。具体删除步骤参见 [服务关联角色](https://help.aliyun.com/zh/ram/user-guide/service-linked-roles)。

## 知识库 SearchFilters

在调用知识库 [Retrieve](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve) 接口时，若返回结果包含较多与 Query 无关的干扰信息（尤其适合结构化数据场景），可在请求体中传入 `searchFilters` 对语义检索结果做进一步过滤。

**效果对比**：未传入 `searchFilters` 时，Retrieve 可能返回多条低相关切片（如查询「张三」却返回李四、王五）；传入后可仅保留命中过滤条件的切片。

**语法**：`searchFilters` 是一个数组，每个元素是一个由 Key-Value 键值对组成的**子分组**。子分组之间默认采用 **AND** 语义且不可更改。

```json
{
  "searchFilters": [
    { "姓名": "张三", "性别": "男" },
    { "岗位": "技术员" }
  ]
}
```

**支持的查询类型**：

| 查询类型 | 适用字段类型 | 说明 |
| --- | --- | --- |
| 单值查询 | 数值（long/double）、字符串（string） | 字段等于某个值 |
| 多值查询 | 纯数值数组或纯字符串数组 | 字段命中数组中任一值；多值需用 `json.dumps` 序列化后传入 |
| 范围查询-等值 | 数值、字符串 | 支持 `eq`（等于）、`neq`（不等于）；一个字段不可配多个值 |
| 范围查询-区间 | 数值（long/double） | 支持 `gt`/`gte`/`lt`/`lte` |
| 模糊查询 | 字符串 | 支持 `like` 属性，`%` 匹配任意字符（含零个） |
| 标签（Tag）查询 | 仅文档搜索、音视频搜索类知识库 | `tags` 字段，多个标签之间为 OR 关系 |

**前置条件**：子账号需获取 `AliyunBailianDataFullAccess` 策略并加入[业务空间](../concepts/workspace.md)（主账号可操作所有[业务空间](../concepts/workspace.md)），获取[业务空间](../concepts/workspace.md) ID，安装百炼 SDK（2023-12-29 版本）并配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量。

**调用示例（Python，单值查询）**：

```python
retrieve_request = bailian_20231229_models.RetrieveRequest()
retrieve_request.query = '公司中叫张三的员工'
retrieve_request.index_id = '请传入实际的知识库ID'
retrieve_request.search_filters = [{"姓名": "张三"}]
resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
```

多值、范围、模糊、标签查询的写法类似，区别在于将字段的值替换为 `json.dumps` 序列化后的对象（如 `{"like": "技%员"}`、`{"gte": 20, "lte": 27}`、`["张三", "李四"]`）。完整 Python/Java 示例参见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制与注意事项

- 临时 [API Key](../concepts/api-key.md) 无法手动删除，只能等 TTL 到期自动失效；各地域 [API Key](../concepts/api-key.md) 不互通。
- 服务关联角色由百炼自动创建并绑定固定系统策略，不可修改、不可授予其他 RAM 身份；删除前必须先解除对应功能的依赖资源，否则相关功能将不可用。
- SearchFilters 子分组之间为 AND 语义且不可更改；多值 / 范围 / 模糊 / 标签查询的值需通过 `json.dumps` 序列化为字符串后传入；标签查询仅支持文档搜索与音视频搜索类知识库。
- 子账号只能操作已加入[业务空间](../concepts/workspace.md)中的知识库，主账号可操作所有[业务空间](../concepts/workspace.md)。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)





















