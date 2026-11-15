# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型调用的进阶能力与关键配置要点，涵盖异步任务管理、子业务空间隔离、临时凭证与文件上传、连接复用等核心机制。所有功能均基于 DashScope SDK 或标准 HTTP API 实现，无需额外部署中间件。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**（如 `qwen-plus`、`qwen3`）：适用于文本生成类任务，请求即响应，响应时间通常在秒级。
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）：因处理耗时长，需通过任务 ID 轮询或事件通知获取结果。详细支持列表请参见 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

> **注意**：文档 4 中提到“调用在阿里云百炼[调优](https://help.aliyun.com/zh/model-studio/model-training-overview)并部署的模型，无需模型调用授权”，但文档 2 明确指出异步任务查询接口“支持查询当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务）”。这意味着子业务空间中调优模型虽不需显式授权，但仍受主账号级任务可见性约束，实际权限控制需结合 RAM 策略与业务空间隔离共同实现。

此外，多模态模型（如 `qwen3-vl-plus`）依赖外部文件输入，需配合 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) 功能使用；高并发场景下推荐启用 [DashScope SDK连接复用配置](raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) 以优化资源利用率。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `page_size` / `page_no` | 异步任务批量查询分页参数 | `page_size` 默认 10，最大建议 50；`page_no` 从 1 开始 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时必需的模型绑定标识 | 必须与后续模型调用的 `model` 字段完全一致（如 `qwen3-vl-plus`） | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，高并发建议设为 128–256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 异步任务管理
对图像、视频、语音等长耗时任务，推荐采用事件驱动方式替代轮询：
- **轮询方式**：调用 `/api/v1/tasks/{task_id}` 查询单任务，或 `/api/v1/tasks` 批量查询，注意 QPS 限流为 20；
- **事件通知方式**：在[事件总线 EventBridge](https://help.aliyun.com/zh/eventbridge/product-overview/what-is-eventbridge) 配置 HTTP 回调或 RocketMQ 目标，监听 `dashscope:System:AsyncTaskFinish` 事件，收到后仅需一次查询即可获取结果。详见 [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。

### 2. 子业务空间调用
为实现模型权限隔离与费用分账，需：
- 在子业务空间创建专属 API Key；
- 若调用标准模型（如 `qwen-plus`），需在该空间[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)；
- SDK 调用时显式指定 `workspace` 和 `region`（如 `ap-southeast-1`），或 OpenAI 兼容模式下使用对应地域的 `base_url`（如 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）。

### 3. 临时文件 URL
多模态模型输入文件需先上传：
- 调用 `POST https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
- 使用策略参数直传至 OSS，获得 `oss://...` 格式 URL；
- **关键**：模型调用请求头必须包含 `X-DashScope-OssResourceResolve: enable`，否则解析失败。

### 4. 连接复用
- **Java SDK**：通过 `Constants.connectionConfigurations` 全局配置连接池参数（如 `connectionPoolSize`, `readTimeout`）；
- **Python SDK**：构造 `Client` 或 `AsyncClient` 时传入自定义 `httpx.Client` / `httpx.AsyncClient` 实例，并配置 `limits`。

## 限制和注意事项

- **临时凭证时效性**：临时 API Key 最长有效期 1800 秒（30 分钟），且**无法手动删除**，到期自动失效 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **文件生命周期**：上传的临时文件有效期严格为 **48 小时**，超时后 URL 失效且不可恢复；生产环境务必使用 OSS 等持久化存储 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港四地 API Key **完全独立**，不可混用；各区域 Endpoint 域名及 WorkspaceId 绑定关系详见 [Base URL 总览](raw/model-api-reference/preparations/base-url.md)。
- **限流策略**：
  - 文件上传凭证接口：按“主账号+模型”维度限流 100 QPS；
  - 异步任务查询接口：全账号共享 20 QPS；
  - 临时 API Key 生成接口：未明确说明，但受底层鉴权服务通用限流约束。
- **安全边界**：临时 API Key 继承生成者 API Key 的全部权限（含知识库访问），切勿在不可信前端直接暴露 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


