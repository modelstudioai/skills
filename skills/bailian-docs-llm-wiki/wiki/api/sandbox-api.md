# sandbox api

Sandbox API 是百炼平台提供的用于动态创建、管理与销毁隔离计算环境的 RESTful 接口，适用于代码执行、模型推理沙箱化部署等场景。它支持按需启动轻量级容器实例，并提供模板化配置能力。所有调用需通过 Bearer Token 认证，且受配额与生命周期策略约束。

## 支持的模型/功能

- 支持基于预置镜像（如 `python3.11`, `nodejs20`）或自定义 Docker 镜像启动沙箱实例；
- 提供同步执行（`/run`）与异步托管（`/instances`）两种模式；
- 支持挂载用户上传的代码包、配置文件及 secret（通过 `mounts` 参数），详见 [概览](../../raw/raw/application-api-reference/sandbox-api/sandbox-api-overview.md)；
- 模板功能允许复用配置（如资源规格、启动命令、环境变量），模板管理接口见 [模版管理](../../raw/raw/application-api-reference/sandbox-api/sandbox-api-templates.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `template_id` | string | 否 | 指定模板 ID；若未提供，需显式声明 `image`, `command`, `resources` 等字段 |
| `timeout` | integer | 否 | 执行超时（秒），范围 1–300，默认 60 |
| `resources.cpu` / `.memory_mb` | integer | 否 | 实例资源限制，单位为 vCPU 核数和 MB；最小值分别为 0.1 和 128，最大值见配额限制 |
| `mounts` | array | 否 | 支持 `type: "file"`（base64 编码内容）或 `type: "object"`（OSS/BOS 对象 URI），详见 [实例管理](../../raw/raw/application-api-reference/sandbox-api/sandbox-api-instances.md) |

> **注意**：`resources.memory_mb` 在部分旧版文档中被误标为 `memory_mb`（正确），而 [实例管理](../../raw/raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 中示例使用 `memory`（无 `_mb` 后缀）——实际 API 仅接受 `memory_mb`，该不一致已在 v2.3.0+ 版本修复。

## 使用方式

1. 获取认证 Token（参考 [认证](../../raw/raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）；
2. （可选）创建或查询模板，简化后续请求；
3. 发起 POST 请求至 `/v1/sandbox/run`（同步）或 `/v1/sandbox/instances`（异步）；
4. 同步调用直接返回执行结果（含 `stdout`/`stderr`/`exit_code`）；[异步调用](../concepts/asynchronous-invocation.md)返回 `instance_id`，需轮询 `/v1/sandbox/instances/{id}` 获取状态。

## 限制和注意事项

- 单次同步执行最长 300 秒，超时将强制终止并返回 `504 Gateway Timeout`；
- 每个账号默认并发实例上限为 10，可通过工单申请提升；
- 沙箱内网络默认禁止外连（`network_mode: none`），如需访问公网，须在模板或请求中显式设置 `network_mode: "default"`；
- 所有输出日志截断上限为 1MB，超出部分被丢弃；
- 错误响应结构统一，具体含义参见 [错误码](../../raw/raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。

## 来源文档

- [Sandbox API](../../raw/application-api-reference/sandbox-api.md)


