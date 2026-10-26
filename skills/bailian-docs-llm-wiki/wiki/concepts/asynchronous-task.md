# 异步任务

异步任务是百炼平台中一类需“提交后轮询或回调获取结果”的模型调用模式，适用于计算密集、耗时较长（通常 >2 秒）的生成类或解析类操作。与同步调用立即返回响应不同，异步任务通过唯一 `task_id` 解耦请求与结果，保障服务稳定性与资源可伸缩性。

## 在百炼平台的不同场景中，这个概念如何使用

异步任务是图像生成、视频生成、3D 生成及文档/音视频解析等重计算能力的**默认且强制的调用范式**：

- **图像生成（`/image-generation/generation`）**：虽部分轻量模型（如 Z-Image）支持快速响应，但平台统一采用异步接口设计；所有请求均返回 `task_id`，需轮询 `GET /api/v1/tasks/{task_id}` 获取最终图片 URL 或 Base64 结果。
- **视频生成（`/video/generation`）**：因视频合成耗时显著（数秒至数十秒），所有模型（包括 `Vidu`、`可灵`、`人像驱动`）必须走异步流程；任务状态包含 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`，成功后 `output.video_url` 提供直连播放地址（有效期 24 小时）。
- **3D 生成（`/3d-generation`）**：Tripo 模型严格要求异步，**必须显式携带请求头 `X-DashScope-Async: enable`**；缺失该头将直接报错 `current user api does not support synchronous calls`。
- **文档与音视频解析（ParseX）**：所有解析与结构化抽取任务均为异步，提交后返回 `biz_id`（功能等价于 `task_id`），用于后续查询解析结果、OCR 文本、表格数据或 Schema 抽取字段。
- **其他场景**：语音转写（`paraformer`）、大文件多模态推理、长上下文结构化处理等也普遍采用异步模式，以避免网关超时（默认同步超时为 60 秒）。

> ✅ **关键识别方式**：若 API 文档中明确出现“返回 `task_id`”、“需轮询 `GET /api/v1/tasks/{id}`”、“支持 HTTP 回调或 MQ 通知”、“必须设置 `X-DashScope-Async: enable`”，即为异步任务。

## 关键参数和配置

| 参数/配置 | 说明 | 必填性 | 注意事项 |
|-----------|------|--------|----------|
| `task_id` | 异步任务全局唯一标识符（UUID 格式） | 返回值，非请求参数 | 所有轮询、取消、批量查询操作的必需输入；24 小时内有效（3D 生成）或 7 天内有效（视频、ParseX） |
| `X-DashScope-Async: enable` | 强制启用异步模式的 HTTP 请求头 | **3D 生成必填**；其余异步 API 推荐显式设置 | 缺失时 3D 接口直接报错；图像/视频等接口虽可省略（因路由已隐含异步语义），但显式声明更健壮 |
| `callback_url`（可选） | HTTP 回调地址，用于事件总线推送完成通知 | 否 | 需提前在控制台配置白名单；推荐用于高并发生产环境，替代轮询；支持 `contain_result=true` 内嵌完整输出，避免二次查询 |
| `status`（轮询参数） | 任务状态过滤（如 `succeeded`, `failed`, `running`） | 否（仅批量查询 `/api/v1/tasks` 时使用） | 单任务轮询无需传此参数 |
| 轮询间隔 | 建议 ≥15 秒 | 否（开发者控制） | 频繁轮询（如 <5 秒）易触发限流（默认 20 RPS）；高并发场景请改用回调机制 |

## 面向开发者，简洁实用

- **不要阻塞等待**：永远不要在主线程循环 `sleep(1)` 等待结果；使用指数退避轮询（如 1s→2s→4s→8s）或优先接入 HTTP 回调/MQ。
- **务必持久化 `task_id` 或 `biz_id`**：它是你获取结果的唯一钥匙，丢失即无法恢复任务状态。
- **检查有效期**：`task_id` 不是永久凭证——3D 任务 24 小时、视频/ParseX 任务 7 天后自动清理，超时查询返回 `UNKNOWN` 或 `404`。
- **错误要主动查**：异步任务失败不会在提交时暴露；必须轮询或监听回调，检查 `status == "failed"` 及 `error.code`/`error.message`。
- **生产环境禁用临时文件 URL**：上传的图片/视频/文档临时 URL 有效期仅 48 小时，且不适用于高可用场景；请使用 OSS 等长期存储，并确保 `file_url` 公网可达。
- **SDK 友好提示**：最新版 DashScope SDK（v4.15+）已内置异步任务封装，调用 `async_generate()` 等方法可自动处理轮询与重试，推荐直接使用。

## 关联主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)


