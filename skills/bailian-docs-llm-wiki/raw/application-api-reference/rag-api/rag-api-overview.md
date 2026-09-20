# API 概览

RAG API 的服务地址、协议约定、请求格式、接口清单与限流规则。

通过 RAG API，您可以以编程方式管理知识库、导入文档、执行检索以及调用知识问答服务。所有接口均通过 DashScope 网关提供服务。

**说明**调用 API 前，请先[获取 API Key](raw/application-api-reference/rag-api/rag-api-authentication.md)。

## 服务地址

`{workspace_id}` 是业务空间 ID，格式如 `llm-xxxxxxxxxxxx`，在控制台[**业务空间管理**](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面查看或创建。

所有接口使用统一的服务地址（Base URL）：

```
https://{workspace_id}.cn-beijing.maas.aliyuncs.com
```

RAG API 包含三组接口，路径前缀不同：

接口组

路径前缀

说明

知识库管理

`/api/v1/indices/`

知识库 CRUD、文档管理、切片管理、检索

数据导入

`/api/v1/connector/dash/`

类目管理、文件上传、连接器配置

知识问答

`/api/v2/apps/knowledge/`

知识问答服务（SSE 流式）

例如，检索接口的完整地址为：

```
https://llm-xxxxxxxxxxxx.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve
```

## 协议约定

-   所有接口均通过 **HTTPS** 访问，不支持 HTTP。
-   请求体和响应体均为 **JSON** 格式，字符集 **UTF-8**。
-   知识库管理、文档管理、切片管理、检索、数据导入等接口统一使用 `POST` 方法；少数查询接口使用 `GET` 方法并通过 query string 传参，包括[**查询知识库列表**](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)、[**查询文档列表**](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)、[**查询导入任务状态**](raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)。各接口的实际方法与参数位置以接口说明为准。

## 通用请求头

Header

必填

说明

`Authorization`

是

`Bearer <API-Key>`，在[控制台 API Key 页](https://bailian.console.aliyun.com/?tab=model#/api-key)获取。详见[认证方式](raw/application-api-reference/rag-api/rag-api-authentication.md)。

`Content-Type`

是

POST 请求为 `application/json`。

## 通用响应格式

所有接口返回统一的 JSON 结构。

**成功响应：**

```
{
  "code": "Success",
  "status_code": 200,
  "data": { },
  "success": true,
  "message": "success",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**失败响应：**

```
{
  "code": "Index.InvalidParameter",
  "status_code": 400,
  "message": "Required parameter(xxx) missing or invalid, please check the request parameters.",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

排查问题时，请提供 `request_id`，以便技术支持快速定位。完整错误码说明见[错误码](raw/application-api-reference/rag-api/rag-api-errors.md)。

## 分页

列表接口支持分页查询。不同接口的请求方法、参数命名与传参位置存在差异，调用时需注意区分：

适用接口

方法

页码参数

每页条数

传参位置

[查询知识库列表](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)

GET

`page_number`（从 1 开始）

`page_size`

Query String

[查询文档列表](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)

GET

`page_num`

`page_size`

Query String

[查询切片列表](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)

POST

`page_num`

`page_size`

Request Body

[查询文件详情列表](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)

POST

`pageNumber`（从 1 开始）

`pageSize`

Request Body

**说明**查询知识库列表的分页参数必须通过 query string 传递（`page_number`、`page_size`，注意是 `page_number` 而非 `page_num`）；若放在请求体中，服务端会忽略并按默认值返回。

## 接口清单

### 知识库

接口

说明

[创建知识库并导入](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)

一步完成创建知识库和导入文件

[查询知识库列表](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)

分页查询当前业务空间下的所有知识库

[更新知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)

修改指定知识库的描述信息

[删除知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)

永久删除指定的知识库及其所有文档和切片

[获取知识库监控数据](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)

查询指定知识库的存储用量和 QPS 监控数据

### 文档管理

接口

说明

[查询文档列表](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)

查询指定知识库中的文档列表

[查询文件详情列表](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)

查询文档的详细信息，包括切片数量和解析状态

[删除文档](raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)

从知识库中删除文档及其所有关联切片

### 切片管理

接口

说明

[新增切片](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)

向指定知识库添加切片内容

[查询切片列表](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)

分页查询知识库中的切片

[更新切片](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)

更新指定切片的内容

[删除切片](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)

批量删除切片，单次最多 10 个

### 同步任务

接口

说明

[提交导入任务](raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)

向已创建的知识库追加导入文档

[查询任务状态](raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)

查询知识库导入任务的执行状态

### 数据导入

接口

说明

[查询类目列表](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)

查询当前业务空间下的类目列表，支持按类型、名称过滤

[新增类目](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)

在当前业务空间下创建新的类目

[删除类目](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)

删除指定的类目

[查询文件列表](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)

查询当前业务空间下的文件列表，支持按类目、文件名和文件 ID 过滤

[查询文件详情](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)

查询指定文件的详细信息，包括大小、MD5、标签和时间戳

[删除文件](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)

永久删除指定的文件

[批量更新标签](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)

批量更新多个文件的标签，支持覆盖和追加两种模式

[申请上传租约](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)

上传文件到数据中心的第一步，返回 OSS 预签名 URL 和租约 ID

[注册文件](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)

上传文件的最后一步，将通过 OSS 上传的文件注册到数据中心

[从 OSS 批量导入](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)

从已授权的阿里云 OSS Bucket 批量导入文件到数据中心

[新增连接器](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)

创建新的数据连接器，用于管理数据导入来源

[查询连接器](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)

查询指定连接器的详细信息

### 知识检索与问答

接口

说明

[知识检索](raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)

跨多个知识库执行联合语义检索

[知识问答](raw/application-api-reference/rag-api/knowledge/knowledgechat.md)

基于知识库的 SSE 流式问答

### Agent 管理

接口

说明

[Agent 管理概述](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)

RAG Agent 实例的全生命周期管理 API

[创建 Agent](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)

创建一个新的 RAG Agent，初始状态为 draft

[更新 Agent](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)

更新 Agent 的名称、描述或草稿配置

[发布 Agent](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)

将 beta 草稿发布为新版本

[删除 Agent](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)

软删除 Agent，标记状态为 deleted

[查询 Agent 列表](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)

分页查询当前租户下的 Agent 列表

[查询 Agent 详情](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)

获取 Agent 完整信息，支持指定版本

[复制 Agent](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)

复制已有 Agent，生成新的草稿

## 限流

各接口设有请求频率限制，超出时返回 HTTP `429`。完整的限流规则见[限流策略](raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
