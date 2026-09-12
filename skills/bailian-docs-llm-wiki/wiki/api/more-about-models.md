# more about models

本文档汇总了百炼平台模型服务的进阶能力与管理接口，涵盖模型发现、权限控制、限流配置、异步任务处理及 SDK 高级用法等开发者常用功能。所有能力均通过 Model Studio API 或 DashScope SDK 提供，适用于需要精细化管控模型调用行为的生产场景。详细实现请参考 [原文标题](../../raw/model-api-reference/more-about-models.md)。

## 支持的模型与功能

- 查询可用模型列表：调用 `GET /v1/models` 获取当前账号可访问的全部模型（含状态、类型、输入/输出限制）  
- 管理模型授权：支持按子业务空间（sub-workspace）粒度配置模型可见性与调用权限，详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models.md)  
- 异步任务支持：对长耗时请求（如大文件解析、批量推理）启用异步模式，并可配置回调地址或轮询结果，参见 [管理异步任务](../../raw/model-api-reference/more-about-models.md) 和 [配置异步任务回调](../../raw/model-api-reference/more-about-models.md)  
- 文件预处理：上传文件后获取临时可读 URL，用于 `file://` 输入（如 PDF、图片），见 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models.md)

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 必填，模型标识符（如 `qwen-max`, `qwen-plus`） | `qwen-max` |
| `async` | 布尔值，启用异步模式（返回 task_id 而非直接响应） | `true` |
| `callback_url` | 异步回调地址（需 HTTPS，且在白名单内） | `https://your.domain/callback` |
| `workspace_id` | 指定子业务空间 ID，用于跨空间调用授权模型 | `ws-abc123` |
| `enable_stream` | 流式响应开关（仅同步模式下生效） | `false` |

> **注意**：`workspace_id` 在 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models.md) 中为路径参数，但在 SDK v3.10+ 中已统一为请求体字段；旧版文档未明确此变更，请以 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models.md) 中的 SDK 示例为准。

## 使用方式

- **API 调用**：所有接口均基于 RESTful 设计，需携带 `Authorization: Bearer <api_key>`，推荐使用临时 API Key（生成方式见 [生成临时API Key](../../raw/model-api-reference/more-about-models.md)）提升安全性  
- **SDK 集成**：推荐使用 DashScope Python/Java SDK，支持连接复用、自动重试、异步任务封装；连接池配置详见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models.md)  
- **限流与配额**：通过 `GET /v1/quotas` 查询各模型当前余量，`PUT /v1/quotas/{model}` 更新配额（需主账号权限）

## 限制和注意事项

- 异步任务最长保留 7 天，超时后结果不可查；任务状态仅支持 `PENDING`/`SUCCESS`/`FAILED`/`TIMEOUT` 四种  
- 临时文件 URL 有效期默认 1 小时，不可续期；单次上传最大支持 512 MB  
- 模型授权更新（`POST /v1/permissions`）为最终一致性，策略生效延迟 ≤ 30 秒  
- 所有模型限流配置（[查询模型限流](../../raw/model-api-reference/more-about-models.md)、[更新模型限流](../../raw/model-api-reference/more-about-models.md)）均按「模型 + workspace」维度独立计费与限速，跨 workspace 不共享 quota

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


