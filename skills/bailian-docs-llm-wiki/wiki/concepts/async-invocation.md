# 异步调用

异步调用是百炼平台针对耗时较长的 AI 生成任务所采用的统一调用模式，核心流程为「创建任务 → 轮询获取结果」，避免客户端因等待超时而失败。

## 适用场景

百炼平台中以下类型的 API 采用异步调用模式：

- **3D 生成**：文生 3D、图生 3D、多图生 3D（Tripo 系列模型）
- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、数字人等（万相、HappyHorse、Pixverse、Vidu、Kling 等模型）
- **应用调用**：智能体和工作流中的长时间任务（Responses API 的 background 模式）
- **图像生成**：部分图像生成与编辑接口

这些场景的共同特点是单次生成耗时通常在数十秒到数分钟，不适合同步阻塞等待。

## 调用流程

### 步骤一：创建任务

向对应的业务 Endpoint 发送 POST 请求，携带异步标识，服务端立即返回 `task_id`。

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/...
Header: X-DashScope-Async: enable
```

### 步骤二：轮询查询结果

使用返回的 `task_id` 定期查询任务状态：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

任务状态流转为：`PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED`（成功）/ `FAILED`（失败）/ `CANCELED`（已取消）。

## 两种异步模式

百炼平台存在两种异步调用方式，适用于不同的 API 体系：

| 方式 | 触发方式 | 适用 API |
| --- | --- | --- |
| DashScope 异步 | 请求头 `X-DashScope-Async: enable` | 3D 生成、视频生成、图像生成等模型 API |
| Responses API 异步 | 请求体 `background: true` | 应用调用（OpenAI 兼容模式） |

两者本质相同，都是提交任务后通过任务 ID 轮询获取结果，区别仅在于触发参数和查询接口的形式。

## 关键参数与配置

| 参数/配置 | 说明 |
| --- | --- |
| `X-DashScope-Async: enable` | 请求头，开启 DashScope 异步模式（3D/视频/图像类必须携带） |
| `background: true` | 请求体参数，开启 Responses API 异步模式 |
| `task_id` | 创建任务后返回的唯一标识，用于后续轮询 |
| 轮询间隔 | 建议 10-15 秒，查询接口默认 RPS 限制为 20 |
| 任务有效期 | task_id 查询有效期通常为 24 小时，超时后返回 UNKNOWN |
| 产物链接有效期 | 生成结果的下载 URL 通常有效 2 小时，需及时下载 |

## 开发建议

1. **不要重复创建任务**：同一请求只需创建一次任务，之后通过轮询获取结果即可。
2. **合理设置轮询间隔**：建议 10-15 秒查询一次，避免触发 RPS 限制。
3. **处理所有终态**：除 SUCCEEDED 外，还需处理 FAILED、CANCELED、UNKNOWN 等状态。
4. **及时保存产物**：下载链接有时效限制，任务成功后应立即下载结果文件。
5. **考虑回调机制**：如需更高频的状态通知，可配置异步任务回调替代主动轮询。
6. **地域一致性**：确保模型、Endpoint URL 和 API Key 属于同一地域，跨地域调用会失败。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [application call](../api/application-call.md)
- [image generation](../api/image-generation.md)


