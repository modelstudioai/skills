# [more](more.md) about models

百炼平台提供多种高级模型调用能力，以支持不同场景下的安全、高效与可扩展需求。本文档系统梳理了临时凭证管理、[异步任务](../concepts/asynchronous-task.md)处理、文件上传、连接复用及子业务空间调用等核心机制，帮助开发者在生产环境中合理选型并规避常见陷阱。

## 支持的模型/功能

百炼支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen3-vl-plus`）适用于低延迟文本生成、推理等场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）需通过任务 ID 轮询或事件通知获取结果，详见[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- 多模态模型（如 VL 系列）需配合临时文件 URL 使用，文件上传与模型调用必须绑定同一模型名称且归属同一主账号，详见[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 6 中提到“调用在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但文档 2 明确指出[异步任务](../concepts/asynchronous-task.md)查询接口“支持查询当前 API Key 所属阿里云主账号下的所有任务（包括该主账号下通过任意 API Key 提交的任务）”。二者逻辑一致——模型调用权限由 API Key 所属主账号及子业务空间策略共同决定，而非模型本身是否微调；实际权限仍受子空间模型白名单控制。

## 关键参数

| 参数 | 说明 | 取值范围 | 示例/备注 |
|------|------|----------|-----------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒 | 默认 60 秒；见[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识 | UUID 格式字符串 | 必须用于 `fetch`/`list`/`cancel` 接口 |
| `contain_result` | 事件总线回调中是否内嵌结果 | `true`/`false` | `true` 时 `data.output_result` 直接包含完整输出，避免二次查询；见[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) |
| `connectionPoolSize` (Java) / `limit` (Python aiohttp) | 连接池容量 | Java 默认 32；Python aiohttp 默认 100 | 高并发场景建议按压测结果调优，避免阻塞或服务端过载；见[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `model` (上传文件) | 文件绑定模型名 | 必须与后续调用模型完全一致 | 如 `qwen3-vl-plus`；不匹配将导致模型调用失败 |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 中，**禁止硬编码永久 API Key**。应通过后端服务调用 `/api/v1/tokens` 接口生成临时 Key，并设置 `expire_in_seconds=1800`（30 分钟）平衡安全性与体验。

### 2. 异步任务处理
- **轮询方案**：对单个任务使用 `GET /api/v1/tasks/{task_id}`，QPS ≤ 20；对批量任务使用 `GET /api/v1/tasks` 并传入 `start_time`/`end_time`/`status` 等参数。  
- **事件驱动方案**：配置事件总线规则，监听 `dashscope:System:AsyncTaskFinish` 事件，通过 HTTP 回调或 RocketMQ 消费，实现零轮询、高实时性；详见[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 多模态文件输入
- 先调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略；  
- 再直传至 OSS；返回 `oss://...` URL；  
- **关键**：调用模型时必须在 Header 中添加 `X-DashScope-OssResourceResolve: enable`，否则解析失败。

### 4. 子业务空间调用
- 使用子空间专属 API Key；  
- 标准模型需在子空间控制台显式授权；微调模型自动继承空间权限；  
- OpenAI 兼容模式需指定 `base_url`（北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`；新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`）；DashScope 原生模式需配置对应地域的 `base_http_api_url`。

## 限制和注意事项

- **临时 Key 无手动删除**：到期自动失效，无法提前撤销（见[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)）。  
- **文件有效期严格为 48 小时**：超时后 URL 失效，且**不适用于生产环境**；生产环境务必使用 OSS 等长期存储。  
- **异步任务保留期为 24 小时**：超时后数据被清理，`fetch`/`list` 将不可查（见[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)）。  
- **连接复用需匹配 SDK 版本**：Python SDK 要求 `>= 1.27.3` 才支持 `Files.upload`；Java SDK 要求 `>= 2.12.0` 才支持完整连接池配置。  
- **地域隔离严格**：北京与新加坡的 API Key、Endpoint、OSS 域名均不互通，混用将导致 `InvalidApiKey` 错误。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)


