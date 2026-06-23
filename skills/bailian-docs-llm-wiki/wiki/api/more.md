# more

本页汇总百炼平台应用 API 的补充参考内容，涵盖临时 API Key 生成、服务关联角色（SLR）管理以及知识库检索过滤（SearchFilters）三个主题。这些功能分别解决前端安全调用、跨云服务权限授予和结构化数据精确检索的需求，是开发者在集成百炼 API 时经常需要查阅的辅助能力。

## 临时 API Key

在浏览器或移动 App 等不可信环境中直接使用永久 API Key 存在泄露风险。百炼提供了通过后端服务[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)的机制，用短生命周期的令牌替代永久密钥。

### 核心参数

| 参数 | 说明 |
|------|------|
| `expire_in_seconds` | 有效期（TTL），范围 1-1800 秒，默认 60 秒 |

### 请求方式

通过 POST 请求生成临时 Key：

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `token` | String | 生成的临时 API Key（以 `st-` 开头） |
| `expires_at` | Number | 过期时间，UNIX 时间戳（秒） |

### 注意事项

- 临时 API Key 继承生成它的永久 API Key 的全部权限，包括模型和知识库的访问限制。
- 各地域的 API Key 不通用，需使用对应地域的 Endpoint。
- 临时 API Key 无法手动删除，到期后自动失效。

## 服务关联角色

百炼通过[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)（Service-Linked Role, SLR）获取对其他阿里云服务的访问权限。首次授权开通相关功能时，系统自动创建对应角色，无需手动配置。

### 角色一览

| 角色名称 | 用途 | 访问的云服务 |
|----------|------|-------------|
| AliyunServiceRoleForSFMAccessFC | 工作流应用 / 流程编排的函数计算节点 | FC |
| AliyunServiceRoleForSFMDataHubOSSImport | 数据管理的 OSS 数据导入 | OSS |
| AliyunServiceRoleForAccessOSS | 安全存储空间访问 OSS | OSS |
| AliyunServiceRoleForSFMAccessADB | 知识库 / 安全存储访问向量数据库 | ADB-PG |
| AliyunServiceRoleForSFMAccessingMNS | 数据管理监听 OSS 变更消息 | MNS |
| AliyunServiceRoleForSFMTelemetry | 用量监控与性能分析 | OpenTelemetry |
| AliyunServiceRoleForSFMAccessingCIP | 应用内容安全审核 | 内容安全 |
| AliyunServiceRoleForSFMAccessSLS | 模型监控日志 | SLS |
| AliyunServiceRoleForSFMAccessCMS | 模型监控指标 | CMS |
| AliyunServiceRoleForAccessCusOss | 平台托管操作用户 OSS 文件 | OSS |
| AliyunServiceRoleForSFMConnectorAccessDTS | 数据源接入 | DTS |
| AliyunServiceRoleForSFMFineTuning | 模型调优和数据管理 | CPFS / OSS |

### 删除角色

删除服务关联角色前，须先移除依赖该角色的资源（如断开安全存储空间连接、删除函数计算节点等）。删除操作不可逆，删除后对应功能将不可用。具体删除方法请参考 RAM 控制台的服务关联角色管理页面。

## 知识库 SearchFilters

当 Retrieve 接口的语义检索返回过多无关结果时，可通过 [SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 参数对检索结果进行结构化过滤，特别适合包含结构化字段的数据表类知识库。

### 支持的查询类型

| 查询类型 | 说明 | 字段类型要求 |
|----------|------|-------------|
| 单值查询 | 精确匹配一个值 | 数值（long/double）、字符串 |
| 多值查询 | 匹配多个值中的任意一个 | 纯数值数组或纯字符串数组 |
| 范围查询 | 支持 `eq`/`neq`/`gt`/`gte`/`lt`/`lte` | 等值：数值、字符串；区间：仅数值 |
| 模糊查询 | 使用 `like` 属性和 `%` 通配符 | 仅字符串 |
| 标签查询 | 按文档标签过滤（多标签为 OR 关系） | 仅文档搜索、音视频搜索类知识库 |

### 语法结构

`searchFilters` 是一个数组，每个元素为一个子分组（JSON 对象），子分组之间为 **AND** 关系，不可更改。

```json
{
  "searchFilters": [
    { "姓名": "张三", "性别": "男" },
    { "岗位": "技术员" }
  ]
}
```

### 使用示例（Python）

```python
retrieve_request.search_filters = [
    {"姓名": "张三"},
    {"年龄": json.dumps({"gte": 20, "lte": 30})}
]
resp = client.retrieve(workspace_id, retrieve_request)
```

### 前置条件

- 子账号需获取 `AliyunBailianDataFullAccess` 策略并加入[业务空间](../concepts/workspace.md)。
- 安装阿里云百炼 SDK 并配置 AccessKey 环境变量。
- 知识库类型需为"数据查询"，且相关字段已设置为参与检索。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)




