# 文档解析 API

文档解析 API：提交解析任务并查询解析结果。

文档解析 API 用于将文档、图片和音视频解析为可读取的结构化内容。调用为异步流程：先提交解析任务获得 `biz_id`，再轮询查询解析结果，直到任务成功或失败。

-   [提交解析任务](raw/application-api-reference/api-overview/document-parsing/parse-submit.md)：提交文档或音视频解析任务，返回 `biz_id` 用于异步查询。
-   [查询解析结果](raw/application-api-reference/api-overview/document-parsing/parse-result.md)：按 `biz_id` 查询任务状态与解析结果。
