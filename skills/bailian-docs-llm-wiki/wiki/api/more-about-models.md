# more about models

本文档汇总了百炼平台模型服务的进阶能力与管理接口，涵盖模型发现、权限控制、限流配置、异步任务处理及 SDK 高级用法等开发者常用功能。所有能力均通过 REST API 或 DashScope SDK 提供，适用于需要精细化管控模型调用行为的生产场景。详细实现细节请参考 [更多 (raw/model-api-reference/more-about-models.md)](../../raw/model-api-reference/more-about-models.md)。

## 支持的模型与功能

- **模型发现与元数据查询**：可通过 `GET /v1/models` 查询当前可用模型列表，包括模型 ID、类型（text-generation、embedding、multimodal 等）、状态及支持的输入格式；该接口在 [更多 (raw/model-api-reference/more-about-models.md)](../../raw/model-api-reference/more-about-models.md) 中列为“查询模型列表”。
- **异步任务管理**：支持提交长耗时请求（如大文件解析、批量推理），并通过任务 ID 轮询或回调方式获取结果；相关接口包括任务创建、状态查询、结果拉取及回调配置，详见 [更多 (raw/model-api-reference/more-about-models.md)](../../raw/model-api-reference/more-about-models.md) 中“管理异步任务”和“配置异步任务回调”。
- **子空间隔离调用**：企业用户可在子业务空间内独立调用模型，权限与配额隔离；需在请求 Header 中显式指定 `X-DashScope-Workspace`，具体规则见 [子业务空间的模型调用](https://help.aliyun.com/zh/model-studio/model-calling-in-sub-workspace)（原文链接已收录于 [更多 (raw/model-api-reference/more-about-models.md)](../../raw/model-api-reference/more-about-models.md)）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型唯一标识（如 `qwen-max`, `bge-m3`），须与 [查询模型列表](https://help.aliyun.com/zh/model-studio/list-models) 返回值严格一致 |
| `X-DashScope-Async` | string | 否 | 设为 `enable` 触发异步模式；默认同步 |
| `X-DashScope-Callback` | string | 否 | 异步回调地址（需 HTTPS，且已在控制台白名单注册） |
| `X-DashScope-Workspace` | string | 否 | 子业务空间 ID；若未指定，则使用主空间 |

> **注意**：部分旧版文档将 `X-DashScope-Async` 的可选值写作 `true`/`false`，但当前 API 仅接受 `enable` 字符串（参见 [更多 (raw/model-api-reference/more-about-models.md)](../../raw/model-api-reference/more-about-models.md) 中“管理异步任务”章节的最新请求示例）。

## 使用方式

- **同步调用**：直接发送 POST 请求至 `/api/v1/services/aigc/text-generation/generation`，传入 `model` 和 `input`。
- **异步调用**：添加 Header `X-DashScope-Async: enable`，响应体返回 `task_id`；后续通过 `GET /api/v1/tasks/{task_id}` 查询状态。
- **文件上传预处理**：对含图片/PDF 的 multimodal 请求，需先调用 `POST /api/v1/files` 获取临时 URL，再将该 URL 填入 `input.messages[].content[].file_url` —— 此流程依赖 [上传文件获取临时URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
- **SDK 连接复用**：DashScope Python SDK 默认启用连接池，如需自定义（如调整 `max_connections`），请参考 [DashScope SDK连接复用配置](https://help.aliyun.com/zh/model-studio/connection-multiplexing-configuration)。

## 限制和注意事项

- 单次异步任务最长保留 7 天，超时后 `task_id` 失效，不可重查。
- 模型限流策略（QPS/TPM）由租户级配额与模型级配额共同约束，需同时调用 [查询模型限流](https://help.aliyun.com/zh/model-studio/list-quotas) 和 [更新模型限流](https://help.aliyun.com/zh/model-studio/update-model-rate-limits) 接口进行调试。
- 临时 API Key 有效期最长 12 小时，且不继承主账号的模型授权；生成后需主动调用 [查询模型授权](https://help.aliyun.com/zh/model-studio/list-model-permissions) 确认其可访问目标模型。
- 所有回调地址必须提前在控制台完成 HTTPS 域名备案与白名单登记，否则回调失败且无重试机制。

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


