# sandbox api

sandbox api 是百炼平台提供的用于动态创建、管理和销毁隔离计算环境的 RESTful 接口，适用于模型调试、代码执行、安全沙箱等场景。它支持按需启动预置或自定义环境，并提供标准 HTTP 接口进行生命周期控制。所有调用需通过平台 API Key 认证，遵循统一的错误响应格式。

## 支持的模型/功能

- 支持基于 Docker 镜像的轻量级沙箱实例（如 `python3.11`, `nodejs20`, `bash` 等运行时）  
- 提供模板化实例创建能力，用户可复用已注册的 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 定义  
- 支持同步执行（`/run`）与异步实例管理（`/instances`）两类模式，后者可用于长时任务或交互式会话  

> **注意**：文档中提及的 `sandbox:cuda` 模板在最新版本中已弃用，实际可用模板请以 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 中 `GET /templates` 响应为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `template_id` | string | 是 | 沙箱模板唯一标识，见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) |
| `timeout` | integer | 否 | 执行超时（秒），默认 30，最大 600 |
| `code` | string | 否（同步模式必填） | 待执行的源码字符串 |
| `env` | object | 否 | 环境变量键值对，如 `{"DEBUG": "1"}` |

## 使用方式

1. **获取模板列表**：`GET /v1/sandbox/templates`  
2. **创建并运行（同步）**：`POST /v1/sandbox/run`，请求体含 `template_id` 和 `code`  
3. **创建实例（异步）**：`POST /v1/sandbox/instances`，返回 `instance_id`；后续通过 `GET /v1/sandbox/instances/{id}` 查询状态  
4. 所有请求需携带 `Authorization: Bearer <api_key>` 头，详见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)

## 限制和注意事项

- 单次同步执行最大输出为 1 MB，超出部分将被截断  
- 沙箱实例默认存活 10 分钟，空闲超时后自动销毁；可通过 `keep_alive` 参数延长（仅限异步实例）  
- 不支持挂载用户私有存储卷，文件系统为临时只读根 + 可写 `/tmp`  
- 调用频率限制：同一 API Key 每分钟最多 60 次 `/run` 请求，实例并发上限为 20  
- 沙箱内网络访问受限，默认禁止外连；如需公网访问，须在模板中显式启用 `network: public`（参见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)）

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


