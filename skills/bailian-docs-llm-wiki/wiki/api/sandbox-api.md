# [sandbox](../guides/sandbox.md) api

[sandbox](../guides/sandbox.md) api 是百炼平台提供的用于动态创建、管理和销毁隔离计算环境的 RESTful 接口，适用于模型调试、代码执行、安全沙箱等场景。它支持按需启动预置或自定义环境，并提供标准 HTTP 接口进行生命周期控制。所有调用需通过 API Key 认证，且受配额与权限策略约束。

## 支持的模型/功能

- 支持基于官方镜像（如 `qwen2.5-7b`, `llama3-8b`）和用户上传 Docker 镜像启动沙箱实例  
- 提供三种核心能力：**实例管理**（创建/查询/终止）、**模版管理**（CRUD 模板配置）、**交互式执行**（stdin/stdout 实时流式通信）  
- 沙箱内默认启用网络代理（仅限白名单域名），并支持挂载加密密钥、临时存储卷等扩展能力  
详见 [Sandbox](../../raw/application-api-reference/sandbox-api.md) 中的功能概览。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `template_id` | string | 是 | 模板唯一标识；若未提供则使用默认模板，详见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) |
| `timeout_seconds` | integer | 否 | 实例最大存活时间（60–3600 秒），超时后自动销毁；默认 600 |
| `env` | object | 否 | 环境变量键值对（key 须为 ASCII 字符，value 长度 ≤ 4096 字节） |
| `stdin` | string | 否 | 初始输入内容（仅对支持交互的镜像生效） |

> **注意**：`timeout_seconds` 在 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 中明确要求最小值为 60，但部分旧版 SDK 示例中误设为 30，该值将被服务端强制修正为 60。

## 使用方式

1. **认证**：在 `Authorization` Header 中传入 `Bearer <api_key>`  
2. **创建实例**：`POST /v1/sandboxes`，请求体含 `template_id` 和可选参数  
3. **获取输出**：轮询 `GET /v1/sandboxes/{id}/status` 或监听 SSE `/v1/sandboxes/{id}/events`  
4. **终止实例**：`DELETE /v1/sandboxes/{id}`（立即释放资源）  
完整流程与示例见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 限制和注意事项

- 单账号并发沙箱实例数上限为 5（企业版可提升），超出时返回 `429 Too Many Requests`  
- 所有沙箱实例默认无持久化存储，重启即丢失数据；如需保留，须显式配置 `volume_mounts`  
- 不支持 GPU 直通，CUDA 程序需使用 CPU fallback 模式运行  
- 模板更新后，已创建的实例**不会自动继承变更**，需手动重建  
请务必参考 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 中的错误码表与重试建议。

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


