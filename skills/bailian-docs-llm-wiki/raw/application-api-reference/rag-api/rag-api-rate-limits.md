# 限流策略

RAG API 各接口的请求频率限制（QPS）与超限处理建议。

为保障服务稳定性，各接口设有请求频率限制（QPS，每秒请求数）。超出限制时返回 HTTP `429 Too Many Requests`。

## 知识库管理接口

接口

端点

QPS 上限

检索

`/rag/index/retrieve`

2,000

[查询任务状态](raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)

`/rag/index_job/status`

20

[查询文档列表](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)

`/rag/index/files`

15

[查询文件详情](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)

`/rag/list/index/file/details`

10

[创建知识库并导入](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)

`/rag/index/create_v2`

10

[提交导入任务](raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)

`/rag/index/job/create`

10

[查询知识库列表](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)

`/rag/index/list`

10

[更新知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)

`/rag/index/update`

10

[删除知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)

`/rag/index/delete`

10

[删除文档](raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)

`/rag/index/delete_file`

10

[查询切片列表](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)

`/pipeline/{id}/chunklist`

10

[更新切片](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)

`/rag/index/chunk/update`

10

[删除切片](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)

`/rag/index/chunk/delete`

10

[获取监控数据](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)

`/rag/index/monitor`

1

## 数据导入接口

接口

端点

QPS 上限

[查询文件详情](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)

`/describeFile`

10

[删除文件](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)

`/deleteFile`

10

[申请上传租约](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)

`/applyFileUploadLease`

10

[注册文件](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)

`/addFile`

10

[查询类目列表](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)

`/listCategory`

5

[新增类目](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)

`/addCategory`

5

[删除类目](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)

`/deleteCategory`

5

[查询文件列表](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)

`/listFile`

5

[查询连接器](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)

`/getConnector`

5

[批量更新标签](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)

`/batchUpdateFileTag`

5

[新增连接器](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)

`/addConnector`

2

[OSS 批量导入](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)

`/addFilesFromAuthorizedOss`

5

## 知识检索与问答

[知识检索](raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)（`/knowledge/search`）和[知识问答](raw/application-api-reference/rag-api/knowledge/knowledgechat.md)（`/knowledge/chat`）的限流规则暂未公布，后续更新。

## 超限处理

触发限流时，接口返回：

```
{
  "code": "Throttling",
  "status_code": 429,
  "message": "Requests rate limit exceeded, please try again later.",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**建议：**

-   收到 429 后，使用指数退避策略重试（如间隔 1s → 2s → 4s）
-   批量操作控制并发数，避免瞬时突发
-   监控数据等低 QPS 接口，建议客户端缓存结果，减少调用频率

**重要**如果当前限额无法满足业务需求，请通过工单申请提升配额。
