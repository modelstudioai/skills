# more about models

本文档汇总了百炼平台模型服务的进阶能力与管理接口，涵盖模型发现、权限控制、限流配置、异步任务处理及 SDK 高级用法等开发者常用功能。所有能力均通过 Model Studio API 或 DashScope SDK 提供，适用于需要精细化管控模型调用行为的生产场景。详细实现请参考 [原文标题](../../raw/model-api-reference/more-about-models.md)。

## 支持的模型与功能

- 查询可用模型列表：调用 `GET /v1/models` 获取当前账号可访问的全部模型（含状态、类型、输入/输出限制）  
- 管理模型权限：支持为子业务空间或 RAM 角色配置细粒度模型调用授权，详见 [原文标题](../../raw/model-api-reference/more-about-models.md) 中的“查询模型授权”与“更新模型授权”  
- 异步任务支持：对长耗时模型（如视频生成、大文件解析）启用异步模式，配合回调配置实现可靠结果获取，相关接口见 [原文标题](../../raw/model-api-reference/more-about-models.md)

## 关键参数

- `model`: 必填，模型标识符（如 `qwen-max`, `qwen-vl-plus`），需与 [查询模型列表](https://help.aliyun.com/zh/model-studio/list-models) 返回值严格一致  
- `async`: 布尔值，设为 `true` 启用异步模式；此时响应体返回 `task_id` 而非直接结果  
- `callback_url`: 异步任务回调地址，需提前在控制台白名单中注册（参见 [配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)）  
- `rate_limit`: 限流配额单位为 QPS 或并发数，通过 [查询模型限流](https://help.aliyun.com/zh/model-studio/list-quotas) 获取当前值，支持按模型/子空间维度更新  

> **注意**：部分旧版文档将 `async` 参数描述为字符串 `"enable"`，实际应为布尔值 `true/false`；以 [原文标题](../../raw/model-api-reference/more-about-models.md) 及最新 OpenAPI Schema 为准。

## 使用方式

1. **获取临时 API Key**：用于短期调试或第三方集成，有效期最长 24 小时（见 [生成临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)）  
2. **上传文件预处理**：调用 `/v1/files/upload` 获取临时 URL，再将该 URL 传入模型请求（如 `qwen-vl-plus` 的 `image_url` 字段），参考 [上传文件获取临时URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)  
3. **SDK 连接复用**：DashScope Python/Java SDK 默认启用连接池，可通过 `dashscope.api_key` + `dashscope.base_http_api_url` 全局配置，并设置 `httpx.AsyncClient(limits=...)` 控制并发（详见 [DashScope SDK连接复用配置](https://help.aliyun.com/zh/model-studio/connection-multiplexing-configuration)）

## 限制和注意事项

- 子业务空间调用模型需显式授予对应模型权限，未授权时返回 `403 Forbidden`，不可依赖主账号默认继承（[子业务空间的模型调用](https://help.aliyun.com/zh/model-studio/model-calling-in-sub-workspace)）  
- 异步任务回调失败重试策略为指数退避（初始 1s，最大 5 次），超时时间为 10 秒；若回调持续失败，需主动轮询 `GET /v1/tasks/{task_id}`  
- 所有模型限流策略均为租户级硬限制，超出后立即拒绝请求（HTTP 429），不进入队列等待；更新限流需调用 [更新模型限流](https://help.aliyun.com/zh/model-studio/update-model-rate-limits) 接口，变更即时生效

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


