# [more](more.md) about models

本文档面向开发者，系统梳理百炼平台模型调用的核心扩展能力，涵盖异步任务管理、子业务空间隔离、文件上传与临时凭证、连接复用优化及安全凭证生成等关键机制。所有能力均基于标准 API 或 SDK 实现，不依赖特定前端或控制台交互。

## 支持的模型/功能

百炼平台支持同步与异步两类模型调用模式：
- **同步模型**（如 `qwen-plus`、`qwen3-vl-plus`）：适用于文本生成、多模态理解等毫秒级响应场景，直接返回结果。
- **异步模型**（如图像生成 `wanx2.1-t2i-turbo`、视频合成 `wanx2.1-kf2v-plus`、语音转写 `paraformer-16k-1`）：因处理耗时长，需通过任务 ID 分步提交与查询，详见[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

多模态模型（VL、OCR、ASR、TTS）调用前，需先将本地文件上传至百炼临时存储并获取 `oss://` 前缀的临时 URL；该 URL 与模型强绑定，且仅限同一主账号下使用，具体流程见[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

> **注意**：文档 4 中明确要求“文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**”，但文档 3 的 DashScope SDK 示例中 `client.files.upload(file_path, purpose)` 方法**无 `model` 参数**，仅支持 `purpose="inference"`。此为接口设计矛盾，实际调用时仍需确保上传与推理所用模型完全一致，否则请求将失败。

## 关键参数

| 参数 | 作用 | 取值范围/说明 | 来源 |
|------|------|----------------|------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒，默认 60 秒 | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `task_id` | 异步任务唯一标识 | UUID 格式字符串，由创建任务接口返回 | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model_name` | 文件上传时声明的模型名 | 必须与后续模型调用的 `model` 字段完全一致（如 `qwen3-vl-plus`） | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `connectionPoolSize` | Java SDK 连接池最大连接数 | 默认 32，高并发建议调至 256 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |
| `max_connections` | Python SDK `httpx.AsyncClient` 总连接数 | 默认无限制，推荐设为 100 | [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) |

## 使用方式

### 1. 异步任务全流程（推荐事件驱动）
避免轮询，优先采用事件总线接收通知：
- 配置 HTTP 回调 URL 或 RocketMQ 作为事件目标；
- 订阅 `dashscope:System:AsyncTaskFinish` 类型事件；
- 在回调或消息消费逻辑中解析 `data.task_id` 和 `data.task_status`；
- 仅当收到通知后，调用一次 `/api/v1/tasks/{task_id}` 查询最终结果。

该方案彻底规避 20 QPS 轮询限流，实时性高，资源消耗低，详见[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。

### 2. 子业务空间调用
用于权限隔离与费用分账：
- 为子空间单独创建 API Key，并配置 `DASHSCOPE_API_KEY` 环境变量；
- 调用标准模型（如 `qwen-plus`）前，需在控制台为该子空间**显式授权**；
- 调用部署模型（Fine-tuned）则无需授权，但**仅限该子空间 API Key 调用**；
- OpenAI 兼容模式统一使用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，DashScope 原生模式需传入 `workspace` 和 `region`。

### 3. 临时凭证与文件上传
- **临时 API Key**：在不可信环境（如浏览器）中，由可信后端调用 `/api/v1/tokens` 接口生成，继承父 Key 全部权限，到期自动失效；
- **临时文件 URL**：调用 `/api/v1/uploads?action=getPolicy&model={model_name}` 获取上传策略，再 POST 至 OSS，返回 `oss://` URL 有效期 48 小时；**调用模型时必须在 Header 中添加 `X-DashScope-OssResourceResolve: enable`**。

## 限制和注意事项

- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港四地 API Key **完全独立**，不可混用；Endpoint 域名、OSS 域名、事件总线地域均需严格匹配（见[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)与[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)）。
- **限流策略**：
  - 临时文件上传：100 QPS（按主账号+模型维度），**禁止用于生产环境与压测**；
  - 异步任务查询：20 QPS（按主账号维度），批量查询 `/api/v1/tasks` 同样受此限制；
  - 临时 API Key 生成：未明文声明限流，但属敏感操作，应合理控制调用频次。
- **安全性**：
  - 临时 API Key 不可手动删除，仅能等待过期；
  - `oss://` URL 仅限模型服务内部解析，业务侧不可直接访问其内容；
  - 子业务空间 API Key 的权限粒度仅到“模型”，无法细化至单个 API 接口。
- **生产环境建议**：
  - 文件存储：弃用临时 URL，改用阿里云 OSS 自建 bucket 并预签名 URL；
  - 连接管理：Java SDK 启用连接池，Python SDK 复用 `httpx.Client` 或 `httpx.AsyncClient`；
  - 异步通知：强制使用事件总线，禁用轮询。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)


