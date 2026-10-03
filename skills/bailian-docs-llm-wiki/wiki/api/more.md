# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制和高级检索控制等功能。它不构成独立服务，而是支撑工作流编排、知识库检索、数据接入、监控分析等核心场景的关键基础设施。开发者需根据具体使用场景按需启用对应能力，并严格遵循最小权限原则配置服务关联角色与临时凭证。

## 支持的模型/功能

`more` 本身不提供模型推理能力，但为以下关键功能提供底层支持：

- **服务关联角色（SLR）**：自动创建并托管跨云服务访问权限，支撑工作流调用函数计算（FC）、OSS数据导入、ADB-PG向量库接入、MNS事件监听、OpenTelemetry/SLS/CMS监控集成、内容安全审核等能力。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 访问FC资源；[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)使用 `AliyunServiceRoleForSFMDataHubOSSImport` 扫描带标签的OSS Bucket；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)通过 `AliyunServiceRoleForSFMAccessADB` 操作ADB-PG向量实例。  
- **临时API Key生成**：提供 `/api/v1/tokens` 接口，用于在不可信前端环境（如浏览器、App）中安全派生短期凭证，避免永久密钥泄露。该能力由后端服务调用，继承源API Key的全部权限范围。  
- **知识库检索过滤（SearchFilters）**：增强 `Retrieve` 接口的语义检索精度，支持基于结构化字段的单值、多值、范围、模糊及标签查询，适用于员工信息表、产品目录等强Schema场景。详见 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档1中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `log:Get*` 后续内容），实际策略应以控制台或RAM策略详情页为准；其描述中“用量监控与性能分析”功能在文档3中未被提及，属独立监控链路，与SearchFilters无交集。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|-----------|
| 临时API Key生成 | `expire_in_seconds` | integer | 否 | 临时Token有效期（秒） | `[1, 1800]`，默认 `60` |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个元素为一个子分组（AND语义） | 子分组内支持 `{"字段": "值"}`（单值）、`{"字段": "[\"v1\",\"v2\"]"}`（多值）、`{"字段": "{\"gte\":20,\"lte\":27}\"}`（范围）、`{"字段": "{\"like\":\"技%员\"}"}`（模糊）、`{"tags": "[\"A大学\",\"学生会主席\"]"}`（标签） |

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加FC节点、配置OSS数据源）时，系统自动创建SLR；无需手动调用API。角色名称与策略已预置，不可修改。查看路径：[RAM控制台 > 角色管理](https://ram.console.aliyun.com/)。  
- **临时API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久APIKey>` 的POST请求，可选传 `expire_in_seconds`。响应返回 `token`（前缀 `st-`）与 `expires_at`（Unix时间戳）。  
- **SearchFilters**：在调用知识库 `Retrieve` 接口时，于请求体中嵌入 `searchFilters` 字段。需确保知识库字段已正确映射为可检索类型（如`姓名`为string，`年龄`为double），且子账号已获 `AliyunBailianDataFullAccess` 权限并加入对应业务空间。参考示例见 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR删除风险**：删除任一SLR将导致其关联功能完全失效。例如，删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的FC节点无法调用；删除 `AliyunServiceRoleForAccessOSS` 将中断安全存储空间对OSS的读写。删除前必须先解除业务侧依赖（如删除FC节点、断开OSS连接）。  
- **临时API Key不可撤销**：生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。务必严格控制 `expire_in_seconds` 时长，避免过度授权。  
- **SearchFilters兼容性**：仅适用于知识库类型为“数据查询”的结构化知识库；文档/音视频类知识库仅支持标签（Tag）查询。多值查询需显式使用 `json.dumps` 序列化数组（如Python示例所示），原始字符串 `"张三,李四"` 不被识别为多值。  
- **地域隔离**：临时API Key的Endpoint与永久API Key地域强绑定（北京/新加坡/弗吉尼亚/中国香港），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


