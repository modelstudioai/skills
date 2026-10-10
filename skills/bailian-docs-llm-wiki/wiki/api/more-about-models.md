# [more](more.md) about models

本文档介绍百炼平台模型调用的进阶能力与配套服务，涵盖临时密钥生成、异步任务管理、子业务空间调用、文件上传支持及连接复用等关键场景。这些功能均通过标准 Model API 或配套 SDK 提供，适用于需要更高灵活性、稳定性或资源隔离的生产级集成。所有能力均需配合 [原文标题](../../raw/model-api-reference/more-about-models.md) 中定义的基础模型调用流程使用。

## 支持的模型/功能

当前支持以下扩展功能（不新增模型本身，而是增强调用方式与上下文）：
- 生成临时 API Key，用于短期、受限权限的模型访问，适用于前端直连或第三方集成场景  
- 异步任务提交与状态轮询，适用于长耗时推理（如长文本生成、多步骤Agent执行）  
- 配置异步任务完成后的 HTTP 回调，避免轮询开销  
- 在子业务空间（sub-workspace）中独立调用模型，实现资源与配额隔离  
- 上传文件并获取带签名的临时 URL，供模型输入（如 `file://` 协议引用）  
- DashScope SDK 的连接复用配置（如 `max_connections_per_pool`），提升高并发下的吞吐与延迟表现  

> **注意**：子业务空间的模型调用能力仅在企业版工作空间中可用，且需管理员开启权限；该限制未在 [原文标题](../../raw/model-api-reference/more-about-models.md) 中明确说明，但已在 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 文档的“前提条件”章节补充。

## 关键参数

| 参数 | 说明 | 示例值 | 是否必需 |
|------|------|--------|----------|
| `api_key` | 临时 API Key（优先于主密钥）或长期密钥 | `sk-xxx-temp-20240501` | 否（若使用临时密钥则必须） |
| `task_id` | 异步任务唯一标识，由 `/v1/tasks` 创建接口返回 | `task-abc123` | 是（查询/取消时） |
| `callback_url` | 异步回调地址，需为 HTTPS 且可公网访问 | `https://your.domain/callback` | 否（启用回调时必填） |
| `workspace_id` | 子业务空间 ID，用于跨空间调用 | `ws-xyz789` | 是（调用子空间模型时） |
| `file_url` | 通过 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口获得的预签名 URL | `https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/...?Expires=...` | 是（模型输入含文件时） |

## 使用方式

1. **临时密钥**：调用 `POST /v1/api-keys/temporary` 获取，有效期最长 24 小时，权限继承自发起者角色  
2. **异步任务**：向 `POST /v1/tasks` 提交请求（body 同同步 `/v1/chat/completions`），响应含 `task_id`；后续用 `GET /v1/tasks/{task_id}` 查询结果  
3. **回调配置**：在创建异步任务时传入 `callback_url` 和可选 `callback_auth`（Bearer [Token](../concepts/token.md)），服务将在任务完成时以 `POST` 发送 JSON 结果  
4. **子空间调用**：在请求 Header 中添加 `X-DashScope-Workspace-ID: ws-xxx`，并确保模型已授权至该子空间  
5. **文件上传**：先调用 `POST /v1/files` 上传二进制文件，响应中 `url` 字段即为可直接用于模型输入的临时 URL  
6. **SDK 连接复用**：初始化 DashScope Client 时设置 `connection_pool_size=20` 等参数，详见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)

## 限制和注意事项

- 临时 API Key 不支持刷新，过期后需重新生成；单个用户每小时最多创建 100 个  
- 异步任务最长保留 7 天，超时未取回结果将被自动清理  
- 回调请求默认超时 10 秒，失败后最多重试 3 次（指数退避）  
- 子业务空间调用不支持流式响应（`stream=true`），仅返回完整结果  
- 临时文件 URL 有效期为 1 小时，且仅限模型服务内部访问，不可直接浏览器打开  
- > **注意**：[管理异步任务](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 文档中提到的 `GET /v1/tasks` 批量查询接口，已于 v2024.04 版本下线，当前仅支持单 `task_id` 查询；最新行为以 [配置异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md) 文档为准。

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)


