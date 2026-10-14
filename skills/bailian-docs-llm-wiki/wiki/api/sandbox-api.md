# sandbox api

Sandbox API 是百炼平台提供的用于动态创建、管理隔离执行环境的 RESTful 接口，适用于代码执行、模型推理沙箱化部署等场景。它支持按需启停实例、绑定模板、获取实时日志与状态，并与平台身份认证体系深度集成。该 API 不直接提供模型推理能力，而是为上层应用提供可编程的运行时环境管控能力。

## 支持的模型/功能

Sandbox API 本身**不托管或调用大模型**，其核心功能聚焦于环境生命周期管理：  
- 创建/销毁沙箱实例（`POST /instances`, `DELETE /instances/{id}`）  
- 基于预定义模板启动实例（模板可封装 Docker 镜像、启动命令、资源限制等）  
- 实时获取实例状态、标准输出/错误流、资源使用量（CPU/Mem）  
- 支持 HTTP 和 WebSocket 两种日志流式订阅方式  

> **注意**：部分旧版文档中提及“内置 Python 模型执行器”，该描述已过时；实际执行逻辑完全由用户通过模板注入，详见 [sandbox-api-templates.md](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `template_id` | string | 是 | 模板唯一标识，需提前通过 [sandbox-api-templates.md](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 创建并发布 |
| `timeout_seconds` | integer | 否 | 实例最大存活时间（30–3600 秒），超时自动销毁，默认 300 |
| `cpu_limit` / `memory_limit` | string | 否 | 如 `"500m"`、`"2Gi"`，遵循 Kubernetes resource limits 格式 |
| `env` | object | 否 | 环境变量键值对（仅支持字符串值），敏感信息应通过 Secret 引用而非明文传入 |

## 使用方式

1. **认证**：使用平台颁发的 `API-Key` 或 `Bearer Token`，通过 `Authorization` 请求头传递，详情见 [sandbox-api-authentication.md](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)  
2. **创建实例**：`POST /v1/sandbox/instances`，请求体含 `template_id` 及可选资源配置  
3. **获取日志**：`GET /v1/sandbox/instances/{id}/logs?stream=true`（流式）或 `?tail=100`（尾行）  
4. **销毁实例**：`DELETE /v1/sandbox/instances/{id}`（同步返回，实例立即进入 terminating 状态）

## 限制和注意事项

- 单账户并发沙箱实例数上限为 20，可通过工单申请提升  
- 实例内进程默认以非 root 用户运行，`privileged: true` 模式不被允许  
- 所有网络出向请求受平台 VPC 安全组约束，无法直连公网（如需访问外部服务，须配置代理或使用平台提供的出口网关）  
- 错误响应统一遵循标准格式，常见错误码含义参见 [sandbox-api-errors.md](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)  
- 沙箱实例无持久化存储，重启后文件系统清空；需持久化数据请挂载平台提供的对象存储卷或通过 API 显式上传

## 来源文档

- [Sandbox API](../../raw/application-api-reference/sandbox-api.md)


