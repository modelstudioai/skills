# [more](more.md) about models

百炼平台提供多种高级模型调用能力，覆盖[异步任务](../concepts/asynchronous-task.md)管理、跨业务空间调用、临时凭证与文件上传、连接复用等关键场景。本文面向开发者，系统梳理核心功能、参数配置、使用方式及限制条件，帮助构建稳定、高效、安全的模型服务集成。

## 支持的模型/功能

百炼支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen3-vl-plus`）适用于低延迟文本生成、多模态推理等场景，直接返回结果；  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频合成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）需通过任务 ID 轮询或事件通知获取结果，详见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  

此外，平台支持子业务空间隔离调用、临时 API Key 生成、本地文件上传获取临时 OSS URL 等扩展能力，满足权限管控、分账、多模态输入、高并发等生产需求。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | [异步任务](../concepts/asynchronous-task.md)唯一标识符 | UUID 格式字符串（如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1`） | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时必需的模型绑定标识 | 必须与后续模型调用一致，如 `qwen3-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 `32`，建议高并发场景设为 `256` | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `X-DashScope-OssResourceResolve` | 使用 `oss://` URL 时必需的请求头 | 固定值 `enable` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

> **注意**：文档 4 中关于 OpenAI 兼容方式调用子业务空间模型的 `base_url` 配置存在地域不一致问题——北京地域示例使用通用域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，但新加坡地域却要求工作空间专属域名 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。而文档 2 明确指出[异步任务](../concepts/asynchronous-task.md)接口在通用域名和工作空间专属域名均支持，且“调用时 API Key 须与对应业务空间匹配”。因此，OpenAI 兼容方式在北京地域也应优先使用工作空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）以确保权限与路由一致性，避免因通用域名路由到默认业务空间导致授权失败。

## 使用方式

### 1. 异步任务处理（推荐事件通知）
避免轮询限流（20 QPS），优先采用 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) 方案：  
- 在事件总线配置规则，监听 `dashscope:System:AsyncTaskFinish` 事件；  
- 事件数据中提取 `task_id` 和 `task_status`，仅在 `SUCCEEDED` 时调用 `/api/v1/tasks/{task_id}` 获取结果；  
- 若需强可靠性，选用 RocketMQ 目标；若快速验证，可先用 HTTP 回调。

### 2. 子业务空间调用
- **必须使用该子空间的 API Key**（非默认空间 Key）；  
- 标准模型（如 `qwen-plus`）需提前在子空间[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)；  
- 调优部署的模型仅支持 DashScope SDK 调用，**不支持 OpenAI 兼容方式**。

### 3. 多模态文件输入
- 上传前明确目标模型（`model_name`），如 `qwen3-vl-plus`；  
- 上传后获得 `oss://...` URL，**调用模型时必须携带请求头 `X-DashScope-OssResourceResolve: enable`**；  
- 临时 URL 48 小时过期，生产环境请使用阿里云 OSS 自主托管。

### 4. 连接复用优化
- **Java SDK**：通过 `Constants.connectionConfigurations` 设置 `connectionPoolSize`、`maximumAsyncRequests` 等；  
- **Python SDK**：传入自定义 `httpx.Client` 或 `httpx.AsyncClient`，配置 `limits` 控制连接数；  
- 同步调用推荐 `with httpx.Client() as client:` 确保资源释放。

## 限制和注意事项

- **临时 API Key**：继承生成者 Key 的全部权限，无法手动删除，到期自动失效；各地域 API Key 不互通，调用时需匹配地域 Endpoint —— 见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **异步任务查询**：任务完成后保留 24 小时（具体以各模型文档为准），超时后数据被自动清理；`PENDING` 状态任务方可取消，`RUNNING` 或 `SUCCEEDED` 状态调用 cancel 接口将报 `UnsupportedOperation` 错误。  
- **文件上传**：严格绑定模型与主账号，不同模型间不可共享 URL；上传限流为 **100 QPS（按主账号+模型维度）**，且不支持扩容，**严禁用于生产环境或压测**；`oss://` URL 必须配合指定请求头使用，否则模型调用失败。  
- **连接复用**：Python SDK 的 `http_client` 实例应在多个请求间复用（而非每次新建），否则失去复用意义；Java SDK 的 `maximumAsyncRequestsPerHost` 值不可超过 `connectionPoolSize`，否则可能阻塞请求。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)


