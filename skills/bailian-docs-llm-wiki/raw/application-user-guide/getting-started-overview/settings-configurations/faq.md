# 常见问题

解答 ParseX 在能力选择、文件限制、配置、异步任务、结果复用和计费方面的常见问题。

Parse 和 Extract 有什么区别？

Parse 将文件还原为适合 Agent 和应用使用的结构化内容，可处理图文、音频和视频。Extract 按 JSON Schema 从图文内容中提取强类型业务字段，并可返回字段状态和原文 Citation。

Extract 可以处理音频或视频吗？

不可以。Extract 当前仅支持图文文件，也只能复用图文 ParseResult。音频和视频请使用 Parse。

控制台体验页可以上传多大的文件？

体验页当前限制为单文件不超过 200 MB。该限制不等同于 API 上限；API 能接受的文件大小以正式接口文档和服务返回为准。完整格式列表见[支持的文件与限制](raw/application-user-guide/getting-started-overview/settings-configurations/supported-files-and-limits.md)。

为什么保存配置前必须先运行样本？

配置会成为可重复使用的稳定资产。使用真实样本运行并检查结果，可以在保存前验证参数、Schema、字段状态和 Citation 是否符合预期。

可以同时传 config\_id 和内联参数吗？

可以。引用已保存的 `config_id`，或者直接传入内联能力设置。如果两个都传的话，优先取内联参数的配置。

提交任务后为什么没有立即返回结果？

Parse 和 Extract 都是异步任务。已定稿 REST 协议规定提交响应返回 `biz_id`，结果响应返回 `processing`、`success` 或 `failed` 状态；正式生产入口发布后，只有状态为 `success` 才能获取最终结果。

如何排查失败任务？

正式 REST 入口发布后，调用方应使用原 `biz_id` 查询结果，并记录 `request_id`、错误码和 `config_id`。参数、格式或 Schema 错误应先修正请求。控制台任务则从“任务记录”界面查看页面提供的信息。

ParseResult 可以复用多久？

当前可复用的图文 ParseResult 保留 7天。结果下载地址可能更早过期，请以接口返回的过期时间为准。

Extract 返回 missing 或 conflict 是否代表任务失败？

不代表。只要系统完整评估了整个 Schema，REST 任务状态仍可为 `success`。`missing` 表示未找到字段，`conflict` 表示原文存在冲突候选。

ParseX 如何计量？

Parse 和 Extract 分项记录用量。可在控制台查看用量信息；具体计量口径、价格、额度和结算规则以[计量与计费](raw/application-user-guide/getting-started-overview/settings-configurations/pricing.md)页面为准。

为什么切换 Workspace 后看不到原来的配置或任务？

文件、配置、任务和结果按 Workspace 隔离。请切换回创建资源时使用的 Workspace
