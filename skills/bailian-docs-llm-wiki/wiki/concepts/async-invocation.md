# 异步调用

异步调用是百炼平台为耗时较长的 AI 任务提供的非阻塞执行模式。客户端提交任务后立即获得任务 ID，随后通过轮询或回调获取最终结果，避免因长时间等待导致请求超时。

## 核心流程

百炼平台的异步调用遵循统一的「创建任务 → 轮询获取结果」两步模式：

1. **创建任务**：向对应的 API 端点发送 POST 请求，服务端立即返回 `task_id`。
2. **轮询查询**：使用 `GET /api/v1/tasks/{task_id}` 定期查询任务状态，直到任务完成或失败。

任务状态流转通常为：`PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED`（成功）/ `FAILED`（失败）。部分接口还支持 `CANCELED`（已取消）和 `UNKNOWN`（任务不存在或已过期）状态。

## 适用场景

异步调用广泛应用于百炼平台中以下耗时任务：

- **视频生成**：文生视频、图生视频、数字人等任务通常需要 1-5 分钟，所有视频生成 API 均强制使用异步调用。
- **3D 资产生成**：基于 Tripo 模型的文生 3D、图生 3D 任务，仅支持异步调用。
- **图像生成**：部分图像生成任务（如高分辨率文生图、批量图像编辑）可通过异步模式提升稳定性。
- **应用调用**：智能体和工作流应用在执行多步骤工具调用或生成长报告时，可开启异步模式。
- **模型生产**：模型微调训练任务属于长时间运行的后台作业，通过轮询监控训练进度。

## 触发方式

百炼平台提供两种方式开启异步调用，具体取决于所使用的 API 体系：

### DashScope API

在 HTTP 请求头中添加：

```
X-DashScope-Async: enable
```

视频生成和 3D 生成等接口**必须**携带此请求头，否则会报错 `current user api does not support synchronous calls`。

### OpenAI 兼容 Responses API

在请求体中设置参数：

```json
{
  "background": true
}
```

任务创建后通过 `client.responses.retrieve(task_id)` 查询状态，完成状态为 `completed`、`failed` 或 `cancelled`。

## 关键参数与配置

| 参数 | 说明 |
|------|------|
| `task_id` | 创建任务后返回的唯一标识符，用于后续状态查询。有效期通常为 24 小时，过期后返回 `UNKNOWN`。 |
| `task_status` | 当前任务状态，可选值：`PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`、`CANCELED`、`UNKNOWN`。 |
| 轮询间隔 | 建议 10-15 秒轮询一次。查询接口默认 RPS 限制为 20。 |
| 异步回调 | 如需更高频通知，可配置异步任务回调替代轮询，减少不必要的查询请求。 |

## 开发最佳实践

1. **避免重复创建任务**：获得 `task_id` 后应持续轮询，不要因为未立即获取结果而重复提交相同请求。
2. **合理设置轮询间隔**：建议 10-15 秒轮询一次，过于频繁的轮询可能触发限流。
3. **及时处理产物**：部分异步任务的产物下载链接有时效限制（如 3D 模型产物链接有效期仅 2 小时），需在有效期内完成下载。
4. **处理失败状态**：轮询时应同时检查 `FAILED` 状态，读取响应中的 `code` 和 `message` 字段进行错误排查。
5. **注意地域一致性**：确保模型、Endpoint URL 和 [API Key](api-key.md) 属于同一地域，跨地域调用会导致异步任务创建失败。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [application call](../api/application-call.md)
- [model production](../api/model-production.md)
- [image generation](../api/image-generation.md)


