# sandbox api

Sandbox API 是百炼平台提供的用于动态创建、管理与销毁隔离计算环境的 RESTful 接口，适用于代码执行、模型推理沙箱化部署等场景。它支持按需启动轻量级容器实例，并提供模板化配置能力。所有调用需通过 Bearer [Token](../concepts/token.md) 认证，且受配额与生命周期策略约束。

## 支持的模型/功能

- 支持基于预置镜像（如 `python3.11-cpu`、`llm-inference-gpu`）或自定义 Dockerfile 构建的运行时环境  
- 提供完整生命周期管理：创建（`POST /instances`）、查询（`GET /instances/{id}`）、终止（`DELETE /instances/{id}`）、日志流式获取（`GET /instances/{id}/logs`）  
- 模板功能允许复用配置（CPU/GPU 规格、启动命令、挂载路径等），详见 [Sandbox API 模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)  

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `template_id` | string | 否 | 引用已保存的模板 ID；若未提供，需显式指定 `image`, `command`, `resources` 等字段 |
| `timeout_seconds` | integer | 是 | 实例最大存活时间（30–3600 秒），超时自动销毁；[原文标题](../../raw/application-api-reference/sandbox-api.md) 明确该值不可超过 3600 |
| `resources.cpu` / `resources.gpu.count` | object / integer | 否（但至少需其一） | CPU 核数或 GPU 卡数；GPU 实例必须指定 `gpu.type`（如 `v100`、`a10`） |
| `mounts` | array | 否 | 支持挂载对象存储（OSS）路径，格式为 `{ "path": "/mnt/data", "oss_uri": "oss://bucket/key" }`；[原文标题](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 要求 OSS Bucket 需与 Sandbox 所在 Region 同地域 |

## 使用方式

1. 获取 Access [Token](../concepts/token.md)（参考 [Sandbox API 认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）  
2. （可选）创建或复用模板：`POST /templates` 或查询已有模板列表  
3. 创建实例：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/sandbox/instances \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "template_id": "tmpl-abc123",
           "timeout_seconds": 600
         }'
   ```
4. 轮询 `status` 字段直至变为 `"running"`，再发送请求至实例暴露的端口（如 `http://<instance-id>.sandbox.dashscope.aliyuncs.com:8080/health`）

> **注意**：原始文档中 [Sandbox API 概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 提到“支持 WebSocket 日志订阅”，但当前 v1.2.0 接口仅提供 HTTP 流式日志（`Transfer-Encoding: chunked`），WebSocket 支持尚未上线，该描述已过时。

## 限制和注意事项

- 单用户默认并发实例上限为 5，可通过工单申请提升  
- 实例内禁止访问公网（出向），仅允许访问阿里云内网服务（如 OSS、VPC 内 SLB）  
- 所有实例在 `timeout_seconds` 到期后强制终止，**不会触发 graceful shutdown**；务必在代码中监听 `SIGTERM` 并完成清理  
- 错误响应遵循统一格式，常见错误码见 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)

## 来源文档

- [Sandbox API](../../raw/application-api-reference/sandbox-api.md)


