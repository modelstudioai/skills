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
- `rate_limit`: 限流配额单位为 QPS，可通过 `list-quotas` 和 `update-model-rate-limits` 接口动态调整  

> **注意**：部分旧版文档将 `async` 参数描述为字符串 `"true"`/`"false"`，但实际 API 仅接受布尔类型；请以 [原文标题](../../raw/model-api-reference/more-about-models.md) 中链接的官方接口文档为准。

## 使用方式

- **同步调用**：直接发送 POST 请求至 `/v1/services/aigc/text-generation/generation` 等模型端点  
- **异步调用**：在请求体中设置 `"async": true`，随后轮询 `GET /v1/tasks/{task_id}` 或监听回调  
- **SDK 配置**：使用 DashScope Python SDK 时，启用连接复用需显式设置 `connection_pool=True`（见 [DashScope SDK连接复用配置](https://help.aliyun.com/zh/model-studio/connection-multiplexing-configuration)）  
- **临时凭证**：敏感环境建议使用临时 API Key（有效期≤24h），生成方式见 [生成临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)

## 限制和注意事项

- 子业务空间调用模型需单独授权，未配置时默认无权限（[子业务空间的模型调用](https://help.aliyun.com/zh/model-studio/model-calling-in-sub-workspace)）  
- 文件类模型（如 `qwen-vl-plus`）需先调用 `POST /v1/files` 上传并获取临时 URL，不可直接传本地路径  
- 模型限流策略按模型 ID 维度独立生效，修改后 30 秒内全量生效；超限请求返回 `429 Too Many Requests`  
- 所有异步任务最长保留 7 天，过期后 `task_id` 不可查；建议业务侧及时消费回调或主动拉取结果

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


