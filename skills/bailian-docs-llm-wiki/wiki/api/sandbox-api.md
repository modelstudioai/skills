# sandbox api

sandbox api 是百炼平台提供的用于安全隔离环境（沙箱）中运行代码、调试模型或执行临时计算任务的 RESTful 接口集合。它支持按需创建、管理及销毁独立沙箱实例，并可绑定预置模板或自定义运行时配置。该 API 主要面向需要动态执行不可信代码、模型推理验证或轻量级函数计算的开发者场景。

## 支持的模型/功能

sandbox api 本身不直接提供模型推理能力，但支持在沙箱实例中加载并运行百炼平台已接入的模型（如 Qwen 系列、Qwen-VL、Qwen2-Audio 等），前提是对应模型已发布为可调用的 `model` 类型服务且具备沙箱兼容运行时。此外，沙箱支持 Python 3.9+ 运行时、基础网络访问（需显式开启）、文件上传/下载及标准输出捕获。所有可用模板均定义在 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 文档中，包括 `python39-cpu`、`qwen2-7b-instruct-gpu` 等典型配置。

## 关键参数

- `template_id`（必填）：指定沙箱启动所用模板 ID，取值需来自 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 列表；
- `timeout`（可选，默认 60s）：沙箱实例最大存活时间（秒），超时后自动销毁；
- `enable_network`（布尔，默认 `false`）：是否允许沙箱内访问公网，启用需额外申请白名单权限；
- `code`（可选）：待执行的 Python 源码字符串，若未提供则需通过 `/instances/{id}/upload` 接口后续上传；
- `env`（可选）：环境变量字典，如 `{"MODEL_NAME": "qwen2-7b"}`，部分模板对此有硬性要求。

> **注意**：原始文档 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中提及 `runtime_version` 参数，但该字段已在 v2.3.0 后废弃，实际请求中传入将被忽略；请以 `template_id` 为准进行运行时选择。

## 使用方式

1. **认证**：使用 Bearer Token 认证，Token 需通过百炼控制台「API 密钥」生成，并具备 `sandbox:instances:create` 权限；
2. **创建实例**：`POST /v1/sandbox/instances`，传入 JSON body（含 `template_id` 等参数），成功返回 `instance_id` 和 `endpoint`；
3. **执行代码**：向 `POST {endpoint}/run` 提交 `code` 或引用已上传文件，响应含 `stdout`、`stderr`、`exit_code` 及执行耗时；
4. **清理资源**：调用 `DELETE /v1/sandbox/instances/{id}` 显式销毁，否则依赖 `timeout` 自动回收。完整流程示例见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 限制和注意事项

- 单实例最大内存 4GB，GPU 实例仅限企业版配额用户申请；
- 沙箱内禁止 fork 进程、加载内核模块、访问 `/proc` 或 `/sys` 等敏感路径；
- 所有实例默认无持久存储，文件需通过 `/upload` 和 `/download` 接口显式传输；
- 模板更新不会影响已创建实例，但新实例将继承模板最新定义 —— 模板版本兼容性说明详见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)。

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


