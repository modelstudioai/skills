# [more](more.md) about models

本文档面向开发者，汇总百炼平台中与模型调用密切相关的进阶能力：包括[异步任务](../concepts/asynchronous-task.md)管理、文件上传与临时资源获取、子业务空间隔离调用、连接复用优化，以及安全凭证控制。这些能力不改变模型核心接口语义，但显著影响生产环境的可靠性、性能与权限治理。

## 支持的模型/功能

百炼平台对不同模型类型提供差异化支持能力：

- **异步模型**：图像生成（如 `wanx2.1-t2i-turbo`）、视频合成（如 `wanx2.1-kf2v-plus`）、语音转写（如 `paraformer-16k-1`）等长耗时模型强制采用异步模式，需通过 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 创建、查询与取消任务。
- **多模态模型**：视觉语言模型（如 `qwen3-vl-plus`）需传入图像/视频 URL，支持通过 [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) 快速上传并获得 48 小时有效 `oss://` 地址。
- **标准与定制模型**：标准模型（如 `qwen-plus`）可在默认或子业务空间调用；而[调优后部署的模型](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)仅限其所属子业务空间的 API Key 调用，且不支持 OpenAI 兼容方式。

> **注意**：文档 [子业务空间的模型调用](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 明确指出“调用在阿里云百炼调优并部署的模型，**无需模型调用授权**”，但文档 [异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 的“前提条件”部分要求“需获取与配置 API Key”，未说明子空间模型是否豁免权限设置。实际开发中，**子空间内调优模型仍需确保该空间 API Key 已被授予对应模型的调用权限**，否则将返回 `Forbidden` 错误。请以控制台权限配置为准。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源文档 |
|------|------|----------------|----------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `contain_result` | [异步任务](../concepts/asynchronous-task.md)完成事件是否内嵌结果 | `true` / `false`；设为 `true` 可减少一次查询调用 | [通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md) |
| `model_name` | 上传文件时必需指定的模型标识 | 必须与后续模型调用的 `model` 参数完全一致，例如 `qwen3-vl-plus` | [上传本地文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32；高并发场景建议调至 256 | [DashScope SDK连接复用配置](raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. [异步任务](../concepts/asynchronous-task.md)处理
对长耗时模型，推荐两种轮询替代方案：
- **主动轮询**：使用 `/api/v1/tasks/{task_id}` 查询单任务，或 `/api/v1/tasks` 批量查询，注意遵守 **20 QPS 限流**；
- **事件驱动**：通过 [事件总线配置 HTTP 回调或 RocketMQ](raw/model-api-reference/more-about-models/async-task-api.md)，在任务完成时由系统主动推送 `dashscope:System:AsyncTaskFinish` 事件，避免轮询开销。

### 2. 文件上传与引用
调用多模态模型前：
- 调用 `POST https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；
- 使用策略中的 OSS 表单直传文件，获得 `oss://` URL；
- **关键**：在模型请求 Header 中必须添加 `X-DashScope-OssResourceResolve: enable`，否则服务端无法解析该 URL。

### 3. 子业务空间调用
- **OpenAI 兼容方式**：固定 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡），**无需修改 endpoint 路径**；
- **DashScope 原生方式**：Java 需显式构造 `Generation` 实例并传入完整 URL；Python 需在 `Client` 初始化时指定 `workspace` 和 `region` 参数。

### 4. 连接复用
- **Python**：通过 `httpx.Client` 或 `httpx.AsyncClient` 传入 `dashscope.Client` 构造函数，复用底层 TCP 连接；
- **Java**：通过 `Constants.connectionConfigurations` 全局配置连接池参数，如 `connectionPoolSize` 和 `maximumAsyncRequests`。

## 限制和注意事项

- **临时资源时效性**：临时 API Key 最长 1800 秒，临时文件 URL 仅 48 小时有效，**均不可续期**，超时后必须重新生成。
- **地域与密钥绑定**：北京、新加坡、弗吉尼亚、中国香港四地 API Key **完全独立**，不可混用；子业务空间的 API Key 也仅对该空间生效。
- **生产环境规避项**：
  - 临时文件上传接口限流 **100 QPS 且不可扩容**，严禁用于压测或高并发场景，生产应使用 OSS 自主托管；
  - 临时 API Key 继承父 Key 全部权限，**禁止在前端代码中硬编码或直接暴露**，必须经可信后端签发。
- **权限继承风险**：[生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 文档强调“临时API Key 继承生成它的API Key 所拥有的全部权限”，这意味着若父 Key 拥有跨模型访问权，临时 Key 也将具备同等能力，需严格管控父 Key 权限粒度。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


