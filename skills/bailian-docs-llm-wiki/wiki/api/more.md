# more

本文档汇总了阿里云百炼平台在应用开发与运维过程中的核心辅助功能与安全配置指南。内容涵盖底层服务关联角色的权限托管、不可信环境下的临时认证机制，以及知识库语义检索的高级过滤策略，旨在帮助开发者以最小权限原则和安全架构高效集成平台能力。

## 支持的模型/功能
本模块不直接涉及大模型调用，而是提供支撑应用全生命周期运行的三项关键基础设施功能：
* **服务关联角色（SLR）**：用于百炼平台跨产品调用底层云资源。[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 会在您首次开通工作流节点、数据管理、安全存储或模型监控等功能时由系统自动创建，托管对 [[函数计算]]、[[对象存储OSS]]、[[AnalyticDB]] 等产品的访问权限。
* **临时 API Key**：解决浏览器、移动端等不可信环境下的鉴权安全问题。[生成临时 API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 提供动态签发的短期凭证，继承主 Key 权限并自动轮转过期。
* **知识库高级检索过滤**：增强 [[RAG 知识库]] 召回准确率。[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 允许在 `Retrieve` 接口调用时注入结构化过滤条件，剔除语义干扰，特别适用于员工信息表、商品库等强结构化数据场景。

## 关键参数
* **SLR 标识与策略映射**
  * `AliyunServiceRoleForSFMAccessFC`：工作流/流程编排调用函数计算，策略绑定 `fc:ListFunctions`, `fc:InvokeFunction`。
  * `AliyunServiceRoleForSFMDataHubOSSImport`：数据导入访问 OSS，策略含 `oss:GetObject`, `oss:ListObjects` 等，受 `oss:BucketTag/bailian-datahub-access=read` 标签约束。
  * `AliyunServiceRoleForSFMAccessADB`：安全存储与知识库访问 ADB-PG 向量库，涵盖 `gpdb:DescribeDBInstances`, `gpdb:UpsertCollectionData` 等。
* **临时 Token 鉴权参数**
  * `expire_in_seconds`（请求）：有效期设置，整型，范围 `[1, 1800]`，默认 `60`。
  * `token`（响应）：临时凭证字符串，前缀固定为 `st-`。
  * `expires_at`（响应）：Unix 时间戳（秒级），标识失效绝对时间。
* **SearchFilters 过滤语法**
  * 数据结构：JSON 数组，支持嵌套子分组。
  * 查询算子：`eq`/`neq`（等值）、`gt`/`gte`/`lt`/`lte`（数值区间）、`like`（通配符）、`tags`（标签数组）。
  * 类型约束：区间仅支持 `long`/`double`；模糊仅支持 `string`；数组值需序列化（如 `json.dumps`）。

## 使用方式
1. **SLR 自动化授权**
   开发者无需编写 IAM 代码。在控制台配置 [[流程编排]]、导入外部数据或关联向量数据库时，系统拦截请求并自动完成 [[服务关联角色]] 创建与信任策略绑定。权限明细可在 RAM 控制台的角色管理页审计。
2. **生成与使用临时 Token**
   后端服务持有 `DASHSCOPE_API_KEY`，通过以下请求获取临时凭证：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=600" \
   -H "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```
   将返回的 `token` 注入前端 `Authorization: Bearer <token>` Header 即可发起模型请求。
3. **SDK 集成 SearchFilters**
   初始化百炼 SDK Client 后，构建 `RetrieveRequest` 对象，将过滤字典赋值给 `search_filters` 字段：
   ```python
   retrieve_request = bailian_20231229_models.RetrieveRequest()
   retrieve_request.index_id = "your_kb_index_id"
   retrieve_request.query = "筛选符合条件的数据"
   # 组合查询：分组1(姓名=张三)，分组2(年龄区间20-27)
   retrieve_request.search_filters = [
       {"姓名": "张三"},
       {"年龄": json.dumps({"gte": 20, "lte": 27})}
   ]
   resp = client.retrieve(workspace_id, retrieve_request)
   ```

## 限制和注意事项
> **注意**：临时 API Key **不支持手动删除或吊销**。其生命周期由服务端严格管控，到达 `expires_at` 后自动失效。请勿在前端缓存或尝试重复刷新未过期的 Token。
* **SLR 删除强依赖**：移除服务关联角色前必须彻底解耦业务。例如删除 `AliyunServiceRoleForSFMAccessFC` 前，需下架并重新发布所有包含函数计算节点的工作流/流程；删除 `AliyunServiceRoleForSFMAccessADB` 前，必须在安全存储空间中手动断开所有数据库连接。
* **权限边界不可越级**：临时 Key 严格继承生成它的永久 Key 的授权范围（如限定模型列表、只读知识库）。若主 Key 无某资源权限，临时 Key 同样无法调用。
* **检索过滤逻辑限制**：
  * `searchFilters` 数组的子分组之间强制为 `AND` 逻辑，暂不支持配置 `OR` 关系。
  * 标签（Tag）查询仅对文档与音视频知识库生效。同一 `tags` 数组内为 `OR` 逻辑；若将不同标签拆分为独立子分组对象，则转为 `AND`。
  * 使用阿里云 SDK 调用前，子账号必须完成 [[RAM 权限]] 授予（`AliyunBailianDataFullAccess`）并加入对应 [[业务空间]]，否则 API 将返回鉴权失败。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时 API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)

