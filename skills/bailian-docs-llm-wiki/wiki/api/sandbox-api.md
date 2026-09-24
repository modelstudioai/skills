# [sandbox](../guides/sandbox.md) api

[sandbox](../guides/sandbox.md) api 是百炼平台提供的轻量级代码执行环境接口，用于安全隔离地运行用户提交的 Python 代码片段，适用于代码验证、教学演示和自动化测试等场景。该 API 不提供持久化计算资源，所有执行均在临时沙箱实例中完成，生命周期由请求控制。详细设计目标与安全边界见 [Sandbox](../../raw/application-api-reference/sandbox-api.md)。

## 支持的模型/功能

- 仅支持 Python 3.9–3.12 运行时（无其他语言或自定义镜像支持）  
- 支持标准库及预装的常用包：`numpy`, `pandas`, `requests`, `matplotlib`（基础后端）等；不支持需系统级权限或网络外连的扩展（如 `torch`, `tensorflow`）  
- 提供三种核心能力：单次代码执行（`/run`）、带上下文的多步会话（`/session/{id}/run`）、模板化任务调用（基于预置模版 ID）  
- 模板管理能力详见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)，实例生命周期控制参见 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | string | 是 | 待执行的 Python 代码字符串（UTF-8 编码，最大 10KB） |
| `timeout` | integer | 否 | 执行超时（秒），取值范围 1–30，默认 10 |
| `stdout_limit` | integer | 否 | 标准输出截断长度（字节），默认 4096，最大 65536 |
| `template_id` | string | 否 | 引用预置模版（如 `"py311-dataclean"`），优先级高于 `code`；模版定义见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) |

> **注意**：原始文档中 `sandbox-api-overview.md` 提到 `language` 参数可选填 `"python"` 或 `"javascript"`，但当前生产环境仅实际支持 Python；JavaScript 支持尚未上线，该字段为预留字段，传入非 `"python"` 值将返回 400 错误。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头，API Key 需具备 `sandbox:execute` 权限  
2. **单次执行**：`POST /v1/sandbox/run`，请求体为 JSON，含 `code` 和可选参数  
3. **会话模式**：先 `POST /v1/sandbox/session` 获取 `session_id`，再向 `/v1/sandbox/session/{id}/run` 提交代码（共享内存与变量状态）  
4. **错误处理**：常见响应码包括 `400`（参数非法）、`401`（鉴权失败）、`403`（权限不足）、`429`（配额超限）、`500`（沙箱内部错误）

## 限制和注意事项

- 单次执行内存上限 512MB，CPU 时间硬限制 30 秒（含启动开销）  
- 网络访问仅允许白名单域名（如 `httpbin.org`, `api.bailian.com`），禁止 DNS 查询与原始 socket 操作  
- 沙箱实例无文件系统写入权限（`/tmp` 可读写但重启即清空），不支持 `subprocess.Popen` 调用外部二进制  
- 配额按项目（project_id）统计：免费层为 100 次/日，超出需开通付费配额；具体计费规则以 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 为准  
- 所有执行日志保留 7 天，调试时建议主动在代码中添加 `print()` 输出关键状态

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


