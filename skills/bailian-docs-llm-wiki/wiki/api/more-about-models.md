# [[more|more]] about models

本文档汇总了阿里云百炼平台在模型调用过程中的高级配套机制，涵盖临时安全凭证、异步长任务管理、业务空间隔离、高并发连接优化及临时文件存储等核心场景。通过合理组合这些能力，开发者可在复杂架构下实现更精细的权限管控、成本分账与服务高可用。

## 支持的模型/功能

- **临时安全凭证**：面向浏览器或移动端等不可信客户端，支持通过安全后端动态生成继承父级权限的临时 Token，有效隔离 [[api-key]] 泄露风险。详见 [生成临时API Key](../../raw/model-api-reference/[[more|more]]-about-models/generate-temporary-api-key.md)。
- **异步任务管理**：针对图像生成、视频合成、语音转写等耗时较长的模型，提供完整的任务生命周期管理接口，支持单任务状态查询、多条件批量检索及排队任务取消。
- **事件总线通知**：将异步任务完成状态接入 [[eventbridge]]，支持通过 HTTP 回调或 [[rocketmq]] 主动推送任务结果，彻底替代低效的轮询机制。详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/[[more|more]]-about-models/async-task-api.md)。
- **子业务空间隔离**：支持为不同团队或业务线创建独立工作区，通过子空间专用的 API Key 限制可调用模型列表，实现细粒度 [[permission-management]] 与成本分账。详见 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。
- **SDK 连接复用**：内置网络层优化机制，Java SDK 提供可配置的连接池，Python SDK 支持透传自定义 Session，显著降低高并发下的握手开销。详见 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。
- **临时文件存储**：提供免费的 OSS 瞬时上传通道，快速将本地图片/音视频转为 `oss://` 协议 URL，直接用于多模态模型输入。

## 关键参数

| 参数/配置项 | 说明 | 默认值 / 范围 |
|:---|:---|:---|
| `expire_in_seconds` | 临时 API Key 的 TTL | 默认 `60s`，支持 `[1, 1800]s` |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 `32`（高并发建议调大） |
| `readTimeout` / `connectTimeout` | Java SDK 读/连超时时间 | 默认 `300s` / `120s` |
| `limit` / `limit_per_host` | Python SDK `aiohttp` 连接限制 | 默认 `100` / `无限制` |
| 事件过滤 `source` / `type` | EventBridge 事件源与类型标识 | `acs.dashscope` / `dashscope:System:AsyncTaskFinish` |
| `X-DashScope-OssResourceResolve` | 使用临时 OSS URL 时的必需 Header | `enable` |

## 使用方式

1. **异步任务轮询与事件驱动**：低并发场景可直接通过 `GET /api/v1/tasks/{task_id}` 轮询；高并发或生产环境推荐配置事件规则，业务端接收通知后仅需执行一次结果查询，大幅降低服务端 QPS 压力。
2. **子空间调用隔离**：在代码初始化客户端时，确保 `base_url` 与 `api_key` 均指向目标子空间。标准模型需在控制台完成显式授权；[[model-fine-tuning]] 部署后的模型自动绑定至原空间，**不支持** [[openai-compatible-api|OpenAI 兼容接口]]调用，仅能通过 DashScope 原生协议访问。
3. **高并发连接优化**：
   - **Java**：通过 `Constants.connectionConfigurations` 静态配置全局连接池与异步请求上限，避免频繁创建 Socket。
   - **Python**：同步架构使用 `with requests.Session() as session:`；异步架构构造 `aiohttp.TCPConnector` 并透传至 SDK 的 `session` 参数中。
4. **临时文件流转**：通过 SDK 或 CLI (`dashscope oss.upload --model <model_name> --file <path>`) 获取 `oss://` 链接。调用模型时，将该链接作为 `image_url`/`audio_url` 传入，**并强制在 HTTP Header 追加 `X-DashScope-OssResourceResolve: enable`**。

## 限制和注意事项

> **注意**：临时存储与临时凭证均**非为生产环境设计**。临时文件 URL 固定有效期为 48 小时，不可续期、不可手动下载；上传凭证接口限流固定为 100 QPS 且不支持扩容。生产环境强烈建议切换至企业级 [[oss-storage]] 服务。

> **注意**：异步任务取消接口仅对状态为 `PENDING` 的任务生效。任务一旦进入 `RUNNING` 或已结算为 `SUCCEEDED`/`FAILED`，将占用计算资源直至完成或超时。部分模型 SDK（如文生图、文生视频）已内置自动轮询逻辑，直接调用 SDK 时无需手动管理 [[async-tasks]]。

> **注意**：临时 API Key 生成后无法手动提前撤销或删除，生命周期完全由服务端控制。若检测到凭证泄露风险，需立即在控制台吊销其对应的永久主 Key。

> **注意**：各地域的 Endpoint 与 API Key **严格隔离**。例如北京地域使用 `https://dashscope.aliyuncs.com`，新加坡地域使用 `https://dashscope-intl.aliyuncs.com`。跨地域部署时，必须同步替换 Base URL 并使用对应地域签发的 Key，否则将返回鉴权失败。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)

