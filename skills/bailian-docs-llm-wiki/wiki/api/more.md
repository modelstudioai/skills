# more

本页汇总百炼应用 API 的补充参考内容，包括服务关联角色（SLR）管理、临时 API Key 生成，以及知识库 Retrieve 接口的 SearchFilters 高级检索能力。这些功能分别解决权限委托、前端安全调用和结构化数据精准检索三类典型需求。

## 服务关联角色

百炼通过服务关联角色（Service Linked Role, SLR）获取对 FC、OSS、ADB-PG、MNS、内容安全等云服务的访问权限。首次授权开通相关功能时，系统自动创建对应角色，无需手动配置。详细的角色列表与权限策略参见[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

百炼目前创建的主要 SLR 包括：

| 角色名称 | 用途 |
| --- | --- |
| AliyunServiceRoleForSFMAccessFC | 工作流应用和流程编排访问函数计算 |
| AliyunServiceRoleForSFMDataHubOSSImport | 数据管理导入 OSS 数据 |
| AliyunServiceRoleForAccessOSS | 安全存储空间读写 OSS |
| AliyunServiceRoleForSFMAccessADB | 知识库和安全存储空间访问 ADB-PG |
| AliyunServiceRoleForSFMAccessingMNS | 数据管理监听 OSS 变更消息 |
| AliyunServiceRoleForSFMTelemetry | 用量监控访问 OpenTelemetry |
| AliyunServiceRoleForSFMAccessingCIP | 应用访问内容安全服务 |
| AliyunServiceRoleForSFMAccessSLS | 模型监控访问 SLS |
| AliyunServiceRoleForSFMAccessCMS | 模型监控访问云监控 |
| AliyunServiceRoleForAccessCusOss | 平台托管操作用户 OSS |
| AliyunServiceRoleForSFMConnectorAccessDTS | 通过 DTS 接入外部数据源 |
| AliyunServiceRoleForSFMFineTuning | 模型调优访问 CPFS 和 OSS |

> **注意**：删除 SLR 前必须先移除依赖该角色的资源（如函数计算节点、OSS 连接等），否则相关功能将不可用。具体的删除前置条件因角色而异，请参阅原文档中各角色的"删除服务关联角色"章节。

## 临时 API Key

在浏览器或移动 App 等不可信环境中调用百炼模型服务时，应通过后端服务生成临时 API Key，避免永久 Key 泄露。完整使用说明参见[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

### 使用方式

向 `/api/v1/tokens` 发送 POST 请求，使用永久 API Key 进行 Bearer 认证：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 关键参数与限制

- **有效期**：通过 `expire_in_seconds` 设置，范围 1~1800 秒，默认 60 秒。
- **权限继承**：临时 Key 继承生成它的永久 Key 的全部权限，包括模型和知识库的访问限制。
- **不可删除**：临时 Key 到期自动失效，无法提前撤销。

### 响应

成功时返回 `token`（临时 Key）和 `expires_at`（UNIX 时间戳）。错误时返回 `code`、`message` 和 `request_id`。

## 知识库 SearchFilters

在调用知识库 Retrieve 接口时，如果语义检索返回过多干扰结果，可通过 `searchFilters` 参数对检索结果进行结构化过滤，尤其适合结构化数据场景。详细语法和完整代码示例参见[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

### 支持的查询类型

| 查询类型 | 字段类型 | 说明 |
| --- | --- | --- |
| 单值查询 | 数值、字符串 | 精确匹配单个值 |
| 多值查询 | 纯数值或纯字符串数组 | 匹配数组中任一值 |
| 范围查询（等值） | 数值、字符串 | 支持 `eq`、`neq` |
| 范围查询（区间） | 数值 | 支持 `gt`、`gte`、`lt`、`lte` |
| 模糊查询 | 字符串 | 使用 `like` 属性，`%` 匹配任意字符 |
| 标签查询 | tags | 仅文档搜索、音视频搜索知识库支持 |

### 语法结构

`searchFilters` 是一个数组，每个元素为一个子分组（对象），子分组之间为 **AND** 关系且不可更改。子分组内包含一组或多组键值对，用于指定过滤条件。

```json
{
  "searchFilters": [
    { "姓名": "张三", "性别": "男" },
    { "岗位": "技术员" }
  ]
}
```

### 前置条件

- 子账号需获取 `AliyunBailianDataFullAccess` 策略并加入业务空间。
- 需安装阿里云百炼 SDK 并配置 AccessKey 环境变量。
- 知识库需为"数据查询"类型，且相关字段已配置为参与检索。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


