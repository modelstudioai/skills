# 异步任务调用

异步任务调用是百炼平台为图像生成、视频生成、3D 模型生成等长耗时模型提供的一种调用机制，采用"创建任务 → 轮询获取结果"两步式交互，避免长时间阻塞 HTTP 连接，支持高并发场景下的任务管理与状态追踪。

## 适用场景

百炼平台中以下能力均采用异步调用方式：

- **图像生成与编辑**：千问（Qwen-Image）、万相（Wan/Wanx）、Z-Image、可灵（Kling）等模型系列，覆盖文生图、图像编辑、风格迁移、虚拟试衣等。
- **视频生成**：万相、HappyHorse、可灵、爱诗 PixVerse、Vidu 等模型族，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人/人像动画等场景。
- **3D 模型生成**：Tripo 系列（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`），支持文生 3D、单图生 3D、多图生 3D。
- **异步任务管理 API**：提供查询、批量查询、取消等通用操作。

## 调用流程

### 步骤 1：创建任务

发送 POST 请求到对应模型的 endpoint，必须设置以下请求头：

- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（必须，未设置将报错 "current user api does not [support](../guides/support.md) synchronous calls"）

成功响应返回 `task_id`，有效期 24 小时，请勿重复创建任务。

示例（以 Tripo 文生 3D 为例）：

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-P1.0",
    "input": {
        "prompt": "一只可爱的猫"
    },
    "parameters": {
        "texture_quality": "standard"
    }
}'
```

### 步骤 2：轮询查询结果

使用 GET 请求查询任务状态：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

任务状态流转：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`。此外还可能出现 `CANCELED`、`UNKNOWN`（`task_id` 过期后返回）。建议轮询间隔 15 秒，查询接口默认 RPS 限制为 20。

## 关键参数与配置

| 配置项 | 说明 |
|--------|------|
| `X-DashScope-Async: enable` | 创建任务时必须携带的请求头，启用异步模式 |
| `task_id` | 创建任务返回的任务标识，有效期 24 小时 |
| 轮询间隔 | 建议 15 秒，避免触发限流（查询接口 20 QPS）|
| 结果下载链接有效期 | 通常 2 小时，请及时下载 |

## 通用任务管理 API

百炼提供一组通用的异步任务管理接口，适用于当前 API Key 所属主账号下的所有任务：

- **查询单个任务结果**：`GET /api/v1/tasks/{task_id}`，返回任务状态及结果，限流 20 QPS。
- **批量查询任务状态**：`GET /api/v1/tasks/`，支持按 `task_id`、`start_time`/`end_time`（格式 `YYYYMMDDhhmmss`）、`model_name`、`status` 等条件组合筛选，分页返回。时间范围不超过 24 小时。
- **取消排队中的任务**：`POST /api/v1/tasks/{task_id}/cancel`，仅支持取消状态为 `PENDING` 的任务，已进入 `RUNNING` 的任务无法取消。

> **注意**：异步任务完成后通常保留 24 小时，超时后系统自动清理，无法再查询。

## 异步任务完成通知

频繁轮询会消耗资源并可能触发限流。百炼已接入阿里云事件总线 EventBridge，支持任务完成后主动推送通知，提供两种接收方案：

| 方案 | 适用场景 | 特点 |
|------|---------|------|
| HTTP 回调 URL | 通用场景 | 需公网或 VPC 可达的 HTTP POST 端点 |
| RocketMQ | 对消息可靠性要求高 | 支持失败重试，消息无丢失 |

事件源为 `acs.dashscope`，事件类型为 `dashscope:System:AsyncTaskFinish`，事件 `data` 中包含 `task_id`、`task_status`、`region` 等字段，可据此调用查询接口一次获取最终结果。可通过事件模式按 `user_api_unique_key` 的模型后缀过滤特定事件。

## 地域约束

模型、Endpoint URL、API Key 必须属于同一地域，跨地域调用将失败。部分模型（如 Tripo 3D、可灵图像/视频生成等）仅适用于"中国内地（北京）"地域，必须使用该地域的 API Key。

## 关联主题页

- [3d generation](../api/3d-generation.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [more about models](../api/more-about-models.md)


