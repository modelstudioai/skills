# [more](more.md) about models

本文档面向开发者，系统介绍百炼平台模型调用的进阶能力与关键约束，涵盖异步任务管理、子业务空间隔离、连接复用、临时凭证与文件上传等核心机制。所有能力均基于标准 API Key 或其派生凭证（如临时 API Key）实现，不依赖控制台操作。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen-vl-plus`）：适用于文本生成、多模态理解等毫秒级响应场景，直接返回结果。  
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频生成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）：因处理耗时长，需通过任务 ID 轮询或事件通知获取结果。相关能力详见 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **子业务空间专属模型**：包括在百炼中[调优并部署的模型](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)，此类模型仅能由其所在子业务空间的 API Key 调用，且无需额外模型调用授权；而标准模型（如 `qwen-plus`）需在子空间中[单独配置权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)。

> **注意**：文档 3 中明确指出“调用在阿里云百炼[调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)并部署的模型，**无需模型调用授权**”，但文档 5 的前提条件中要求“上传文件时必须指定模型名称，且该模型须与后续调用的**模型一致**”。二者逻辑一致——调优模型绑定空间，文件也必须绑定同一空间下的同名模型，不存在跨空间复用。

## 关键参数

| 参数 | 说明 | 取值范围/示例 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识符 | UUID 格式字符串，如 `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时必需的模型标识 | 必须与后续调用模型完全一致，如 `qwen-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 时必需的请求头 | 固定字符串，不可省略 | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |

## 使用方式

### 1. 安全调用（不可信环境）
在浏览器或移动 App 等前端场景中，**禁止硬编码永久 API Key**。应通过后端服务调用 `/api/v1/tokens` 接口生成临时 API Key，并设置合理 TTL（建议 ≤ 180 秒），其权限继承自生成所用的永久 Key。详情见 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

### 2. 异步任务结果获取
- **轮询方式**：调用 `GET /api/v1/tasks/{task_id}` 查询单个任务，或 `GET /api/v1/tasks` 批量查询。注意 QPS 限流为 20，建议按任务类型设置查询间隔（文本类可 1s，图像/视频类建议 ≥ 5s）。  
- **事件驱动方式**：配置事件总线（EventBridge）接收 `dashscope:System:AsyncTaskFinish` 事件，目标可选 HTTP 回调或 RocketMQ。该方式规避轮询限流，实时性更高，适合高并发场景。详见 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 多模态文件输入
调用图像、视频等模型前，需先上传本地文件获取 `oss://` 开头的临时 URL（有效期 48 小时）。上传时必须指定 `model_name`，且该名称须与后续模型调用完全一致。调用时需在请求头中显式添加 `X-DashScope-OssResourceResolve: enable`。生产环境请使用 OSS 自有存储替代此临时方案。

### 4. 连接优化
- **Python SDK**：通过 `requests.Session`（同步）或 `aiohttp.ClientSession`（异步）复用 TCP 连接，避免高频建连开销。  
- **Java SDK**：通过 `Constants.connectionConfigurations` 配置连接池参数（如 `connectionPoolSize`、`readTimeout`），默认已启用连接池。  

## 限制和注意事项

- **临时凭证时效性**：临时 API Key 与临时文件 URL 均为短期有效（分别 ≤ 1800 秒、48 小时），**严禁用于生产环境长期服务**。生产环境应使用自有 OSS 存储 + 永久 API Key 或 RAM 子账号最小权限策略。  
- **地域与域名强绑定**：各区域（北京、新加坡、弗吉尼亚、中国香港）API Key 不互通；子业务空间调用必须使用对应地域的工作空间专属域名（如 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`），通用域名 `dashscope.aliyuncs.com` 仅适用于默认业务空间。  
- **限流严格**：  
  - 文件上传凭证接口：100 QPS（按“主账号+模型”维度）；  
  - 异步任务查询接口：20 QPS（按主账号全局）；  
  - 临时 API Key 生成接口：未明文声明，但受后端配额管控。  
- **模型与文件强耦合**：上传文件时指定的 `model_name` 必须与后续模型调用的 `model` 参数**完全一致**（含大小写、版本号），否则调用失败。例如上传时用 `qwen-vl-plus`，则调用时 `model` 字段也必须为 `qwen-vl-plus`，不可简写为 `qwen-vl`。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)


