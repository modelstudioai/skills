# [sandbox](../guides/sandbox.md) api

[sandbox](../guides/sandbox.md) api 是百炼平台提供的用于安全隔离执行用户代码的沙箱服务接口，支持按需创建、管理及销毁临时计算环境。它适用于代码验证、函数执行、模型推理预处理等需要资源隔离与快速启停的场景。所有调用需通过标准 HTTP REST 接口完成，并依赖平台统一认证机制。

## 支持的模型/功能

[sandbox](../guides/sandbox.md) api 本身不直接提供模型推理能力，而是为运行用户自定义逻辑（如 Python 脚本、Shell 命令或轻量模型加载）提供受控容器环境。当前支持的运行时包括 `python3.9`、`python3.11` 和 `bash`，可通过 `runtime` 参数指定。模板（template）机制允许复用预配置的镜像与初始化脚本，相关能力详见 [Sandbox](../../raw/application-api-reference/sandbox-api.md) 中的模版管理章节。注意：`tensorflow` 和 `pytorch` 等框架仅在特定模板中预装，非默认可用，具体依赖请参考 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 文档。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `template_id` | string | 是 | 模板唯一标识，决定基础镜像、环境变量和启动脚本；必须来自 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 返回的合法 ID |
| `timeout` | integer | 否 | 执行超时时间（秒），范围 5–300，默认 60 |
| `max_memory_mb` | integer | 否 | 内存上限（MB），范围 128–2048，默认 512 |
| `code` | string | 是（若未指定 `template_id`） | 待执行的源码内容（Base64 编码），优先级低于 `template_id` |

> **注意**：原始文档中 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 提到 `code` 可为明文字符串，但实测 API 已强制要求 Base64 编码，该处文档已过时。

## 使用方式

1. 通过 POST `/v1/sandboxes` 创建沙箱实例，携带上述关键参数；
2. 使用返回的 `sandbox_id` 轮询 `/v1/sandboxes/{sandbox_id}/status` 获取执行状态；
3. 成功后通过 `/v1/sandboxes/{sandbox_id}/output` 获取 stdout/stderr 与退出码；
4. 调用 `/v1/sandboxes/{sandbox_id}` 发起 DELETE 请求以主动回收资源（否则将在 `timeout` 后自动销毁）。

完整流程与请求示例见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 限制和注意事项

- 单次执行最大输出日志为 10 MB，超出部分将被截断；
- 沙箱实例生命周期最长 300 秒（含启动、执行、清理），不可续期；
- 不支持持久化存储、网络外连（除白名单域名如 `api.bailian.com` 外）、GPU 加速；
- 实例并发数受项目配额限制，详情参见配额管理控制台；
- 模板更新后，已创建的实例不受影响，但新创建实例将使用最新模板定义 —— 此行为与 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 描述一致。

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


