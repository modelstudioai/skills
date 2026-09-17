# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型服务的核心能力、配置参数、调用方式及关键约束。内容涵盖模型发现与授权、异步任务处理、文件上传、连接优化等高频场景，所有说明均基于当前稳定 API 行为。

## 支持的模型/功能

百炼平台提供统一模型目录，支持按模态（如 `TG` 文本生成、`IG` 图片生成）、供应商（如 `qwen`、`zhipu-ai`）、能力（如 `function-calling`、`structured-outputs`）等多维度筛选模型。通过 [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md) 接口可获取实时模型元数据，包括上下文长度、定价、输入/输出模态及部署模式。  
模型调用权限需显式授予：子业务空间中调用标准模型（如 `qwen-plus`）前，必须通过 [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md) 和 [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md) 接口完成推理权限配置；而调优后部署的模型仅限其所在空间调用，无需额外授权。  
对于多模态模型（如 `qwen-vl-plus`），需先将本地文件上传至百炼临时存储以获取 `oss://` 格式 URL，该 URL 有效期 48 小时，且与模型强绑定——上传时指定的 `model_name` 必须与后续调用模型一致，否则请求失败 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

## 关键参数

- **异步任务**：图像、视频等长耗时任务采用异步模式，需通过 `task_id` 轮询或事件总线回调获取结果。轮询接口限流为 20 QPS，建议根据任务类型设置合理间隔（文本向量可短，图像生成宜长），避免触发限流 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **限流配额**：各模型的请求频率（QPM/QPS）和用量（TPM/[Token](../concepts/token.md)）限制可通过 [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md) 接口查看，并使用 [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md) 接口动态调整。注意：若仅设置 QPM 而未设 TPM，部分模型会因校验逻辑拒绝生效，需按文档推荐的“删除+覆盖”两步法操作。  
- **连接复用**：高并发场景下，Java SDK 默认启用连接池，Python SDK 需显式传入 `requests.Session` 或 `aiohttp.ClientSession` 实现复用。Java 连接池默认大小为 32，建议根据实际负载调整 `connectionPoolSize` 和 `maximumAsyncRequests`；Python 异步调用推荐配置 `limit_per_host` 避免单主机过载 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 使用方式

- **子空间调用**：为实现权限隔离或费用分账，应使用子业务空间的专属 API Key 调用模型。OpenAI 兼容方式需配置对应地域的 `base_url`（如北京为 `https://dashscope.aliyuncs.com/compatible-mode/v1`），且仅支持标准模型；调优模型必须使用 DashScope 原生 SDK 调用 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  
- **异步通知**：为规避轮询资源浪费，推荐通过事件总线配置 HTTP 回调或 RocketMQ 接收任务完成事件（`dashscope:System:AsyncTaskFinish`）。事件中包含 `task_id` 和 `task_status`，收到后仅需一次查询即可获取结果，实时性高且不限流 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。  
- **临时密钥**：在浏览器或移动 App 等不可信环境调用模型时，应通过后端服务生成临时 API Key（TTL 1–1800 秒），避免永久密钥泄露。临时 Key 继承源 Key 的全部权限，到期自动失效，不可手动删除 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 限制和注意事项

> **注意**：文档 5 明确指出“文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景**”，而文档 1 中异步任务查询接口限流为 20 QPS。二者均为硬性限制，无弹性扩容路径，生产环境必须通过事件总线回调或自建 OSS 存储规避。  
> **注意**：文档 4 与文档 9 存在隐含矛盾——文档 4 称“调用调优模型无需模型调用授权”，但文档 9 的权限字段 `inference` 明确控制“模型调用权限”，且其示例返回中 `qwen3-max` 的 `fine_tune:true` 与 `inference:true` 并存。实际行为以 [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md) 接口返回为准：若 `permissions.inference` 为 `false`，即使模型部署在本空间也无法调用。  
- 临时文件 URL 仅支持 `oss://` 协议，调用时必须在 HTTP Header 中添加 `X-DashScope-OssResourceResolve: enable`，否则报错。  
- 临时 API Key 无法用于调用需要 RAM 权限的管理类接口（如模型授权、限额更新），仅适用于模型推理类 API。  
- 所有异步任务数据保留期为 24 小时（以任务完成时间计），超时后无法查询，需及时处理结果。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [查询模型列表](../../raw/model-api-reference/more-about-models/list-models.md)
- [查询模型限额](../../raw/model-api-reference/more-about-models/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/more-about-models/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/more-about-models/update-model-permissions.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [更新模型限流](../../raw/model-api-reference/more-about-models/update-model-rate-limits.md)


