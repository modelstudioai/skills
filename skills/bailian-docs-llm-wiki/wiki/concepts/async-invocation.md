# 异步调用

异步调用是百炼平台针对耗时较长的生成类任务所采用的标准调用模式，流程为「创建任务 → 轮询获取结果」，适用于视频生成、3D 模型生成、部分图像生成等场景。

## 调用流程

异步调用统一分为两步：

1. **创建任务**：向对应能力的 API 端点发送 POST 请求，请求头中必须携带 `X-DashScope-Async: enable`，否则会报错 `current user api does not support synchronous calls`。请求成功后返回 `task_id`。
2. **轮询查询结果**：使用返回的 `task_id`，向 `GET /api/v1/tasks/{task_id}` 发送查询请求，根据 `output.task_status` 判断任务状态。

## 任务状态流转

异步任务的状态枚举如下：

| 状态 | 含义 |
| --- | --- |
| `PENDING` | 排队中，任务已提交但尚未开始处理 |
| `RUNNING` | 处理中 |
| `SUCCEEDED` | 任务成功完成，可从响应中获取产物 |
| `FAILED` | 任务失败，响应中包含错误码和错误信息 |
| `CANCELED` | 任务已取消 |
| `UNKNOWN` | 任务不存在或已超过有效期 |

正常流转路径为 `PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。

## 适用场景

百炼平台以下能力采用异步调用模式：

- **视频生成**：万相（Wan）系列、HappyHorse、Pixverse、Vidu、Kling 等所有视频生成接口，单次生成耗时通常 1-5 分钟。
- **3D 模型生成**：Tripo 系列模型的文生 3D、图生 3D、多图生 3D 接口。
- **图像生成**：部分图像生成与编辑接口（如万相文生图 V1 版、涂鸦作画等）。
- **模型调优**：微调训练任务通过轮询或监听方式获取训练进度和结果。

## 关键参数与配置

### 请求头

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `X-DashScope-Async` | 是 | 固定值 `enable`，开启异步模式 |
| `Authorization` | 是 | `Bearer $DASHSCOPE_API_KEY`，鉴权令牌 |

### 轮询策略

- 建议轮询间隔约 **15 秒**，避免过于频繁触发限流。
- 查询接口默认 RPS 限制为 **20**，如需更高频率可配置异步任务回调通知。
- `task_id` 有效期为 **24 小时**，超时后查询返回 `UNKNOWN` 状态。

### 地域与域名

调用异步接口时需确保模型、Endpoint URL、API Key 属于同一地域。推荐使用[业务空间](workspace.md)专属域名：

- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

旧域名 `dashscope.aliyuncs.com` 仍可使用。

## 最佳实践

1. **避免重复创建任务**：创建成功后保存 `task_id`，通过轮询获取结果即可，不要对同一请求重复提交。
2. **及时下载产物**：生成产物（视频、3D 模型等）的下载链接通常有时效限制（如 2 小时），请及时保存。
3. **使用回调替代轮询**：对于高频调用场景，建议配置异步任务回调通知，减少轮询请求开销。
4. **处理失败状态**：任务失败时响应中包含 `code` 和 `message` 字段，可参照百炼错误码文档排查问题。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [model production](../api/model-production.md)


