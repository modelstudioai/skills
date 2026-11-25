# sandbox api

Sandbox API 是百炼平台提供的用于动态创建、管理和销毁隔离执行环境的 RESTful 接口，适用于代码执行、模型推理沙箱化部署等场景。它支持按需启动轻量级容器实例，并提供模板化配置能力。该 API 与百炼统一认证体系集成，需通过 Bearer [Token](../concepts/token.md) 认证 [原文标题](../../raw/application-api-reference/sandbox-api.md)。

## 支持的模型/功能

- 支持基于预置镜像（如 `python3.11`, `nodejs20`）或自定义 Docker 镜像启动沙箱实例；
- 提供模版管理能力，允许保存常用配置（环境变量、启动命令、资源限制）为可复用模板 [原文标题](../../raw/application-api-reference/sandbox-api.md)；
- 支持同步执行（`/run`）和异步实例生命周期管理（`/instances`），后者支持 `start`/`stop`/`delete` 操作。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `template_id` | string | 否 | 模板 ID；若未提供，需显式指定 `image`, `command`, `resources` 等字段 [原文标题](../../raw/application-api-reference/sandbox-api.md) |
| `timeout` | integer | 否 | 执行超时（秒），默认 30，最大 300 |
| `resources.cpu` / `resources.memory` | object | 否 | 资源限制，单位为 `mCPU` 和 `MiB`，例如 `{ "cpu": 500, "memory": 1024 }` |

> **注意**：文档中 `resources.memory` 的单位在 [sandbox-api/sandbox-api-instances.md](../../raw/application-api-reference/sandbox-api.md) 中描述为 `MB`，但实际 API 仅接受 `MiB`（即二进制兆字节），请以 OpenAPI Schema 和实测行为为准。

## 使用方式

1. 获取访问 [Token](../concepts/token.md)（参考 [sandbox-api/sandbox-api-authentication.md](../../raw/application-api-reference/sandbox-api.md)）；
2. 创建实例（POST `/v1/sandboxes/instances`）或直接运行（POST `/v1/sandboxes/run`）；
3. 轮询 `status` 字段或监听 Webhook（需提前注册）获取执行结果；
4. 显式调用 `DELETE /v1/sandboxes/instances/{id}` 清理长期运行实例（自动回收策略不保证及时性）。

## 限制和注意事项

- 单次请求最大响应体为 10 MB；超出部分将被截断并返回 `413 Payload Too Large`；
- 沙箱实例默认存活 10 分钟（无活跃连接），超时后自动终止，但不会自动释放挂载卷；
- 不支持 GPU 加速；所有实例运行于 CPU-only 环境；
- 模板创建后不可修改，如需更新需新建模板并更新引用 —— 此行为与 [sandbox-api/sandbox-api-templates.md](../../raw/application-api-reference/sandbox-api.md) 描述一致。

## 来源文档

- [Sandbox API](../../raw/application-api-reference/sandbox-api.md)


