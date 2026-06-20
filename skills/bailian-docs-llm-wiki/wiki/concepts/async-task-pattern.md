# 异步任务模式

异步任务模式是百炼平台中用于处理耗时较长的生成类任务的统一调用范式。其核心流程为"提交任务 → 获取 task_id → 轮询查询结果"，适用于所有无法在单次 HTTP 请求内完成的计算密集型操作。

## 工作原理

异步任务模式将一次完整的 API 调用拆分为两个独立的步骤：

1. **创建任务**：客户端发送 POST 请求提交任务，服务端立即返回 `task_id`，不阻塞等待结果。
2. **轮询结果**：客户端使用 `task_id` 周期性调用 GET 查询接口，直到任务状态变为终态（`SUCCEEDED` 或 `FAILED`）。

这种设计避免了长时间的 HTTP 连接保持，适合生成耗时从数十秒到数分钟不等的多媒体任务。

## 适用场景

在百炼平台中，以下场景均采用异步任务模式：

- **图像生成与编辑**：文生图、图像编辑、风格迁移、虚拟试衣等，涵盖千问图像、万相、Z-Image、可灵等模型系列。
- **视频生成**：文生视频、图生视频、参考生视频、视频编辑、人像动画等，涵盖万相、可灵、HappyHorse、PixVerse、Vidu 等模型系列。
- **3D 模型生成**：文生 3D、单图生 3D、多图生 3D（Tripo 模型）。
- **模型生产**：模型调优（微调训练）、模型压缩、模型部署等长时间运行的生产任务。

## 关键参数和配置

### 请求头

创建任务时必须设置以下请求头：

| 请求头 | 值 | 说明 |
|--------|------|------|
| `X-DashScope-Async` | `enable` | 启用异步模式，缺失时会报错 |
| `Authorization` | `Bearer $DASHSCOPE_API_KEY` | API Key 认证 |
| `Content-Type` | `application/json` | 固定值 |

> `X-DashScope-Async: enable` 是异步调用的必要标识。未设置该请求头时，部分接口会返回 "current user api does not [support](../guides/support.md) synchronous calls" 错误。

### 任务状态

任务的生命周期状态流转如下：

```
PENDING → RUNNING → SUCCEEDED / FAILED
```

- `PENDING`：任务已提交，排队等待执行。
- `RUNNING`：任务正在执行中。
- `SUCCEEDED`：任务完成，可从响应中获取结果。
- `FAILED`：任务失败，响应中包含错误信息。

### 查询接口

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔为 **15 秒**，查询接口默认 RPS 为 20。

## 注意事项

- **task_id 有效期为 24 小时**：超时后无法查询结果，任务状态返回 `UNKNOWN`。请勿对同一请求重复创建任务。
- **结果链接有时效性**：部分任务（如 3D 生成）返回的下载链接有效期仅 2 小时，需及时下载保存。
- **地域限制**：部分模型（如 Tripo 3D、可灵）仅在特定地域（如北京）可用，需使用对应地域的 API Key。
- **模型生产任务**：模型调优、压缩、部署也是异步操作，但通常耗时更长（分钟至小时级别），部署后的模型会持续占用资源，不再使用时应及时下线。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)
- [image generation](../api/image-generation.md)
- [model production](../api/model-production.md)


