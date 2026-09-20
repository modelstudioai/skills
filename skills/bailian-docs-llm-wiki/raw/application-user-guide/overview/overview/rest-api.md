# REST API 接入

按已定稿的 REST 字段协议准备 Parse 或 Extract 异步任务集成，并了解生产入口发布边界。

REST API 规划用于后端服务、跨语言系统和工作流编排。公开字段协议已经定稿，定义了 Bearer API Key、`config_id`、`biz_id`、业务路径和异步结果查询语义，可用于准备集成代码。

## 集成准备条件

-   已获得 ParseX 控制台访问权限，并从正式授权入口进入目标 Workspace；未获得入口时先联系服务提供方或管理员，不生成或猜测控制台 URL。
-   已用真实样本验证并保存 Parse 或 Extract 配置，取得 `config_id`。
-   已准备符合要求的输入文件 URL；Extract 复用解析结果时，还需准备有效的 `parsed_file_biz_id`。
-   已规划在生产 Base URL 和正式认证方式发布后，由服务端安全保存 REST 返回的 `biz_id` 并执行异步结果查询。

详细限制见[支持的文件与限制](raw/application-user-guide/overview/configurations/supported-files-and-limits.md)，配置规则见[保存与复用配置](raw/application-user-guide/overview/configurations.md)。

## 已定稿业务路径

方法

业务路径

用途

`POST`

`/parse/submit`

提交 Parse 任务

`POST`

`/parse/result`

查询 Parse 状态、结果或分片

`POST`

`/extract/submit`

提交 Extract 任务

`POST`

`/extract/result`

查询 Extract 状态与结果

所有请求使用 JSON 和 `snake_case` 字段，并携带以下请求头：

```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**说明**API Key 只应保存在服务端或密钥管理系统中。不要把它写入浏览器代码、仓库、任务参数或日志。

## 使用已保存配置

已定稿协议要求在 `config_id` 与内联能力参数之间二选一。正式生产入口发布后，建议引用已验证的配置，以避免不同服务分别维护解析或抽取规则。

#### Parse

配置调用至少需要表达以下语义：

```
- `file_url`：待处理文件的可访问 URL。
- `file_name` 或协议要求的文件类型信息。
- `config_id`：已保存的 Parse 配置 ID。

完整参数和响应字段见[文档解析 API](/zh/model-studio/parse/api/parse-submit)。
```

#### Extract

配置调用需要选择一种输入：

```
- 直接处理图文文件时使用 `file_url`。
- 复用解析结果时使用 `parsed_file_biz_id`，不能传 `request_id` 或从控制台界面推断的标识。对应 ParseResult 必须已完成、为可复用的图文类型，且未超过 30 天保留期。
- 使用已保存的 Extract 配置 ID 作为 `config_id`。

`config_id` 与内联 `processing` 是二选一的处理定义；使用已保存配置时不要同时传递内联参数。字段定义和两种请求示例见[信息抽取 API](/zh/model-studio/parse/api/extract-submit)。
```

**警告**不要在同一次调用中同时传入 `config_id` 与对应的内联处理参数，否则会产生 `ConfigInlineConflict`。需要调整规则时，请创建新配置并切换 ID。

## 调用流程

1.  **等待正式 Base URL 发布**
    
    生产 Base URL 尚未公开确认。在正式生产端点发布前，不要把 `{BASE_URL}` 占位符当作真实地址，也不要用预发或内部地址替代。
    
2.  **提交任务**
    
    正式端点可用后，调用对应的 `submit` 端点，传入文件来源、能力匹配的 `config_id` 和协议允许的单次运行参数。单次运行参数不应改变已保存配置的处理定义。
    
3.  **保存请求与任务标识**
    
    从响应中保存 `request_id` 和 `data.biz_id`。`request_id` 用于定位本次 API 请求，`biz_id` 用于后续查询异步业务任务。
    
4.  **查询任务状态**
    
    使用原 `biz_id` 调用对应的 `result` 端点。`data.status` 为 `processing` 时继续轮询；为 `success` 或 `failed` 时停止。
    
5.  **处理结果或错误**
    
    成功后读取正式 Parse 或 Extract 结果；失败时保存错误码、`request_id`、`biz_id` 和 `config_id`，结合公开错误码排查。
    

## 状态与追踪

标识或状态

含义

客户端处理

`request_id`

一次 API 请求的定位标识

每次提交和查询都记录，排错时与错误码一起提供

`biz_id`

一次异步业务任务的标识

提交后持久化，并用于对应结果端点

`processing`

任务仍在处理

使用退避策略继续查询原任务，避免因等待而重复提交

`success`

正式结果可读取

校验结果结构，并关联 `config_id`、输入与业务记录

`failed`

任务失败

根据错误码决定修正输入、停止或重试

在结果尚未就绪时，接口可能返回 HTTP `409` 和 `ResultNotReady`。客户端应继续查询原 `biz_id`，而不是创建一个无法关联的新任务。

## 重试与重复提交

**警告**当前公开协议未定义客户端幂等键、重复提交去重规则或按 `request_id` 检索任务的端点。不要假设提交请求天然幂等，也不要自行发明幂等请求头。当前仅按结果接口轮询。

-   客户端应保存自身业务关联键、提交时间，以及收到响应时的 `request_id` 和 `biz_id`。
-   如果提交请求超时且未收到响应，公开协议无法让客户端自动确认任务是否已经创建；应进入人工或业务侧对账流程，并接受无法自动排除重复提交的事实。
-   对结果查询采用带上限的退避策略；不要高频轮询。
-   仅对明确标记为可重试的错误执行自动重试，参数、格式或配置冲突应先修正。

## 相关参考

-   [API 概览](raw/application-api-reference/overview.md)：查看认证、Base URL 占位约定、公开业务路径和异步调用流程。
-   [错误码](raw/application-api-reference/overview/errors.md)：根据 HTTP 状态和错误码决定处理方式。
-   [任务与用量](raw/application-user-guide/overview/configurations/usage.md)：了解公开 REST 任务状态，以及控制台“任务记录”和用量界面。
