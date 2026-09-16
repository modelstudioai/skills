# [sandbox](../guides/sandbox.md) api

[sandbox](../guides/sandbox.md) api 是百炼平台提供的轻量级隔离执行环境接口，用于安全运行用户提交的代码片段或脚本，适用于代码验证、函数沙箱化执行、AI 工具链中的动态代码调用等场景。该 API 通过 RESTful 接口提供实例生命周期管理、模板预置与复用、资源约束配置等能力。所有请求需携带有效的 `Authorization: Bearer <token>` 头，并遵循平台统一的错误响应格式。

## 支持的模型/功能

- **执行环境**：支持 Python 3.9–3.12、Node.js 18/20、Shell（bash）三种运行时，不支持自定义容器镜像。
- **核心功能**：
  - 创建并启动一次性执行实例（`POST /v1/sandbox/instances`）
  - 基于预置模板快速启动（如 `python-http-server`、`node-fetch-demo`），模板列表见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
  - 实例日志流式获取（`GET /v1/sandbox/instances/{id}/logs`）与状态轮询（`GET /v1/sandbox/instances/{id}`）
- **注意**：文档中提及的 “Java 运行时支持” 在 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 的最新版本中已被移除，当前实际仅支持上述三种运行时；请以该文档为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `runtime` | string | 是 | 取值为 `python`, `nodejs`, `shell`；必须与模板定义一致 |
| `code` | string | 否 | 内联代码内容；若未提供，则必须指定 `template_id` |
| `template_id` | string | 否 | 模板唯一标识，优先级高于 `code`；模板详情参见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) |
| `timeout` | integer | 否 | 执行超时（秒），范围 1–300，默认 60 |
| `memory_mb` | integer | 否 | 内存限制（MB），范围 64–1024，默认 256 |

> **注意**：`code` 与 `template_id` 不可同时为空，也不可同时提供——[API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 明确要求互斥，违反将返回 `400 Bad Request`。

## 使用方式

1. **认证**：使用平台颁发的 API Key 或短期 Token，通过 `Authorization` 请求头传递；
2. **创建实例**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/sandbox/instances \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "runtime": "python",
           "code": "print(2 + 2)",
           "timeout": 10
         }'
   ```
3. **获取结果**：轮询 `status` 字段直至变为 `succeeded` 或 `failed`，再调用 `/logs` 获取完整输出。

## 限制和注意事项

- 单次执行最大内存 1024 MB，最长运行时间 300 秒；
- 代码中禁止访问外网（默认禁用网络），如需启用需显式设置 `network_enabled: true`（仅限企业版租户，且须提前报备）；
- 实例为无状态、一次性资源，创建后不可重启或重用；
- 所有输入代码在服务端执行前会进行静态安全扫描（如危险系统调用检测），可能拒绝含 `os.system("rm -rf /")` 等高危模式的 payload；
- 日志保留时间为 24 小时，超时后自动清理。

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


