# more

本页汇总百炼应用 API 参考中暂未归入主体专题的三类辅助能力：**服务关联角色（SLR）** 用于让百炼安全访问您账号下的其他云资源；**临时 API Key** 用于在不可信环境调用模型服务时避免永久 Key 泄露；**知识库 SearchFilters** 用于对 Retrieve 接口的语义检索结果做结构化过滤。三者面向的场景不同，请按需取用。

## 服务关联角色（SLR）

服务关联角色（Service Linked Role, SLR）是百炼为访问您账号下其他云服务（FC、OSS、ADB-PG、MNS、SLS、CMS、内容安全等）专门创建的 RAM 角色。当您在百炼控制台**首次开通**相关功能（如工作流的函数计算节点、安全存储空间、知识库等）时，系统会自动创建对应 SLR，无需手动配置。

参考[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)，百炼当前提供的 SLR 主要包括：

| 角色名 | 用途 | 关联策略示例 |
| --- | --- | --- |
| `AliyunServiceRoleForSFMAccessFC` | 工作流应用 / 流程编排访问 FC 函数 | `fc:ListFunctions`, `fc:InvokeFunction` |
| `AliyunServiceRoleForSFMDataHubOSSImport` | 数据管理从 OSS 导入数据 | `oss:GetObject`, `oss:ListObjects`（需 BucketTag `bailian-datahub-access=read`） |
| `AliyunServiceRoleForAccessOSS` | 安全存储空间读写 OSS（需 BucketTag `bailian-safe-workspace-oss-access=ReadAndWrite`） | `oss:GetObject` / `oss:PutObject` / `oss:DeleteObject` |
| `AliyunServiceRoleForSFMAccessADB` | 知识库 / 安全存储空间访问 ADB-PG 向量库 | `gpdb:CreateCollection`, `gpdb:QueryCollectionData` 等 |
| `AliyunServiceRoleForSFMAccessingMNS` | 数据管理消费 MNS 中的 OSS 变更消息 | `mns:ReceiveMessage`, `mns:DeleteMessage` |
| `AliyunServiceRoleForSFMTelemetry` | 用量监控与性能分析读取 OpenTelemetry / XTrace | `arms:*`, `log:Get*`, `xtrace:Read*` |
| `AliyunServiceRoleForSFMAccessingCIP` | 百炼应用访问内容安全 | 内容安全相关只读 |
| `AliyunServiceRoleForSFMAccessSLS` | 模型监控访问 SLS | SLS 只读 |
| `AliyunServiceRoleForSFMAccessCMS` | 模型监控访问 CMS | CMS 只读 |
| `AliyunServiceRoleForAccessCusOss` | 百炼平台托管操作用户 OSS 文件 | OSS 读写 |
| `AliyunServiceRoleForSFMConnectorAccessDTS` | 通过 DTS 接入外部数据源 | DTS 任务管理 |
| `AliyunServiceRoleForSFMFineTuning` | 模型调优 / 数据管理访问 CPFS、OSS | CPFS / OSS 读写 |

### 删除前注意

> **注意**：删除 SLR 会直接导致对应能力不可用。例如：
> - 删除 `AliyunServiceRoleForSFMAccessFC` 之前必须先删除所有工作流 / 流程中的函数计算节点，并重新发布。
> - 删除 `AliyunServiceRoleForAccessOSS` / `AliyunServiceRoleForSFMAccessADB` 之前必须先在安全存储空间中断开所有 OSS / ADB-PG 连接。
> - 删除 `AliyunServiceRoleForSFMDataHubOSSImport` 之前必须先停止所有 OSS 导入任务。
>
> 删除步骤请前往 RAM 控制台 → 角色管理执行，详见原文。

## 临时 API Key

在浏览器、移动 App 等**不可信前端环境**调用 DashScope 模型服务时，应通过可信后端用永久 API Key 兑换出短期有效的临时 API Key 下发给客户端，避免永久 Key 直接暴露。详见[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

### 关键事项

- **权限继承**：临时 Key 完全继承生成它的永久 Key 的权限（包括模型 / 知识库白名单）。生成前应先在密钥管理页面把永久 Key 配置为最小权限。
- **有效期**：默认 60 秒，可通过 `expire_in_seconds` 参数指定，范围 `[1, 1800]` 秒。
- **不可提前撤销**：临时 Key 一旦生成只能等到 TTL 过期，**不支持手动删除**。
- **地域差异**：各地域 Endpoint 不同，新加坡 / 北京 / 弗吉尼亚需分别申请永久 Key 后再调用对应地域接口。

### 调用示例

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应结构

正常响应：

```json
{
  "token": "st-****",
  "expires_at": 1744080369
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `token` | String | 临时 API Key，前缀固定为 `st-` |
| `expires_at` | Number | UNIX 时间戳（秒），到期后自动失效 |

错误响应包含 `code` / `message` / `request_id`，例如 `InvalidApiKey` 表示永久 Key 无效。

## 知识库 SearchFilters

`SearchFilters` 是知识库 [Retrieve](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve) 接口的可选参数，用于在语义检索之后对返回的文本切片做**结构化字段过滤**，对结构化数据（数据表导入的知识库）尤其有效。完整示例见[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

### 顶层语义

`searchFilters` 是一个数组，每个元素是一个**子分组**（Key-Value 集合）；子分组之间为 **AND** 关系且不可更改；同一子分组内的多个键也是 AND。

```json
{
  "searchFilters": [
    { "姓名": "张三", "性别": "男" },
    { "岗位": "技术员" }
  ]
}
```

### 支持的查询类型

| 查询类型 | 适用字段 | 写法要点 |
| --- | --- | --- |
| 单值查询 | string / long / double | 直接 `{"字段": 值}` |
| 多值查询 | 纯字符串数组 / 纯数值数组 | 值需 `json.dumps(list)` 序列化后传入 |
| 范围 - 等值 | string / 数值 | 使用 `eq` / `neq`，一字段一值，不区分大小写 |
| 范围 - 区间 | long / double | 使用 `gt` / `gte` / `lt` / `lte` |
| 模糊查询 | string | 使用 `like` 属性，`%` 匹配任意字符（含 0 个） |
| 标签查询 | 文档 / 音视频类知识库 | `{"tags": json.dumps([...])}`，同一数组内为 OR；多个 `tags` 分组之间为 AND |

### 前置条件

- 子账号需获取 `AliyunBailianDataFullAccess` 策略并加入对应[业务空间](../concepts/workspace.md)；主账号无此限制。
- 已安装阿里云百炼 SDK（`alibabacloud_bailian20231229`）。
- 已配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 到环境变量。
- 知识库的字段需在创建时设置为**参与检索**，否则无法被 SearchFilters 命中。

### 典型用法（Python 节选）

```python
retrieve_request = bailian_20231229_models.RetrieveRequest()
retrieve_request.query = "公司中姓名为张三的员工"
retrieve_request.index_id = "请传入实际的知识库ID"
retrieve_request.search_filters = [
    {"姓名": "张三"}
]
resp = client.retrieve("请传入实际的业务空间ID", retrieve_request)
```

> **注意**：多值 / 范围 / 模糊 / 标签查询的 value 都需要先 `json.dumps(...)` 成字符串再放入 dict，不能直接传 Python list/dict，否则 SDK 序列化后 server 端会按单值字符串解析。

### 效果对比

未传 `searchFilters` 时，Retrieve 会按语义返回多条相关度递减的切片（如同时返回张三、李四、王五）；传入 `[{"姓名": "张三"}]` 后只返回严格匹配该过滤条件的张三记录，可显著减少干扰信息。完整对比表见[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)的"效果对比"章节。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)













