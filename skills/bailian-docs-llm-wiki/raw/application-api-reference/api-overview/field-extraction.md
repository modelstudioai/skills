# 字段解析 API

字段解析 API：提交抽取任务并查询抽取结果。

字段解析 API 用于按 JSON Schema 从图文材料中抽取指定字段，返回结构化结果。调用为异步流程：先提交抽取任务获得 `biz_id`，再轮询查询抽取结果，直到任务成功或失败。

-   [提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md)：按 JSON Schema 提交结构化信息抽取任务，返回 `biz_id` 用于异步查询。
-   [查询抽取结果](raw/application-api-reference/api-overview/field-extraction/extract-result.md)：按 `biz_id` 查询任务状态与抽取结果。

**重要**也可在终端用阿里云百炼 CLI 完成同样流程：`bl parsex extract submit --workspace-id <workspace-id> --file-url "https://example.com/document.pdf" --schema-file schema.json --output json`，再用 `bl parsex extract result --biz-id <biz-id> --follow` 查询结果。详见[使用 CLI](raw/application-user-guide/agent-context/getting-started-overview/integration-overview/cli.md)。
