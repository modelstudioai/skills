# [sandbox](../guides/sandbox.md) api

[sandbox](../guides/sandbox.md) api 是百炼平台提供的用于安全隔离环境（沙箱）中运行代码、调试模型或执行不可信脚本的 RESTful 接口集合，适用于需要临时计算资源、结果可验证且无副作用的场景。该 API 支持按需创建/销毁实例、复用预置模板，并与百炼模型服务深度集成。所有操作均需通过标准 API Key 认证，遵循平台统一的配额与审计策略。

## 支持的模型/功能

- 支持在沙箱中调用百炼托管的 **Qwen 系列大模型**（如 qwen-max、qwen-plus）进行推理，但仅限于 `text-generation` 类型请求；不支持多模态输入或流式响应。
- 提供两类核心能力：**实例级执行**（单次代码运行，返回 stdout/stderr 和退出码）和 **模板级复用**（预定义环境镜像、依赖和启动命令，提升重复任务效率）。
- 沙箱底层基于轻量容器实现，支持 Python 3.9–3.12、Node.js 18+ 和 Bash 运行时，但不支持持久化存储、网络外连（默认禁用）或系统级权限操作。  
  更多可用运行时与模型兼容性详见 [Sandbox](../../raw/application-api-reference/sandbox-api.md) 文档中的子页面说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `template_id` | string | 否 | 指定预置模板 ID；若未提供，则使用默认最小化 Python 模板。模板列表见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)。 |
| `code` | string | 是（当未指定 `template_id` 时） | 待执行的源代码（如 Python 脚本），UTF-8 编码，最大 1MB。 |
| `timeout` | integer | 否 | 执行超时时间（秒），范围 1–60，默认 30。超过将强制终止进程。 |
| `enable_network` | boolean | 否 | 是否启用有限网络访问（仅允许访问 `api.qwen.ai` 和 `dashscope.aliyuncs.com`），默认 `false`；开启需额外申请白名单。 |

> **注意**：原始文档中 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 描述 `memory_limit_mb` 为可选参数，但当前 API 实际已弃用该字段，设置将被忽略——请勿在请求中传入。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <your_api_key>`；
2. **创建实例并执行**：向 `POST /v1/sandbox/instances` 发送 JSON 请求体，包含 `code` 或 `template_id` 及其他参数；
3. **轮询结果**：响应中返回 `instance_id`，随后调用 `GET /v1/sandbox/instances/{instance_id}` 获取执行状态与输出；
4. **清理资源**：建议显式调用 `DELETE /v1/sandbox/instances/{instance_id}` 释放资源；未手动清理的实例将在 10 分钟空闲后自动销毁。  
   完整流程与示例代码参见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 限制和注意事项

- 单次执行最大内存占用为 2GB，超出将触发 OOM 终止；
- 每个 API Key 默认 QPS 限制为 5，日配额 1000 次实例创建（含失败请求）；
- 沙箱内禁止 fork 进程、加载动态链接库（`.so`/`.dll`）、读写 `/tmp` 以外路径，且所有文件操作均在内存文件系统中进行，重启即丢失；
- 模板一旦发布即不可修改，更新需新建版本并更新引用；旧模板仍可使用，但不再接收安全补丁。  
  具体配额策略与安全边界详见 [Sandbox](../../raw/application-api-reference/sandbox-api.md) 主页及关联子文档。

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


