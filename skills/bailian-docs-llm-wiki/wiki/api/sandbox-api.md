# sandbox api

sandbox api 是百炼平台提供的用于安全隔离执行用户代码的运行时环境接口，支持动态创建、管理沙箱实例并运行指定代码片段。它适用于需要临时计算、代码验证、AI Agent 工具调用等场景，所有执行均在资源受限、网络隔离的容器中完成。该 API 与百炼统一认证体系集成，需通过 `Authorization: Bearer <token>` 认证。

## 支持的模型/功能

sandbox api **不涉及大语言模型推理**，其核心能力是提供可编程的轻量级执行环境（基于 Linux 容器），支持以下功能：
- 创建/销毁沙箱实例（`POST /v1/sandboxes` / `DELETE /v1/sandboxes/{id}`）  
- 提交代码并获取执行结果（`POST /v1/sandboxes/{id}/run`）  
- 管理预置模版（如 Python 3.11、Node.js 20 等运行时环境）[原文标题](../../raw/application-api-reference/sandbox-api.md)  
- 支持标准输入/输出、超时控制、资源配额（CPU、内存、磁盘）  

> **注意**：文档 [原文标题](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中提及的 “支持多模型上下文注入” 属于过时描述，当前 sandbox api 无模型集成能力，该内容已失效，请以 [原文标题](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 中定义的实例生命周期为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `runtime` | string | 是 | 运行时标识，如 `python311`、`nodejs20`，必须为平台预置模版中的名称 |
| `code` | string | 是 | 待执行的源代码（Base64 编码，避免 JSON 转义问题） |
| `timeout` | integer | 否 | 执行超时（秒），默认 30，最大 120 |
| `memory_limit_mb` | integer | 否 | 内存上限（MB），默认 256，范围 64–1024 |
| `stdin` | string | 否 | 标准输入内容（Base64 编码） |

## 使用方式

1. **获取模版列表**：`GET /v1/sandbox/templates` → 获取可用 `runtime` 值  
2. **创建实例**：`POST /v1/sandboxes`，请求体含 `runtime` 和可选配置  
3. **执行代码**：`POST /v1/sandboxes/{id}/run`，传入 `code`、`timeout` 等参数  
4. **清理资源**：显式调用 `DELETE /v1/sandboxes/{id}`；未删除实例将在 10 分钟空闲后自动回收  

示例（cURL）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/sandboxes \
  -H "Authorization: Bearer $DASHSCOPE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"runtime":"python311","memory_limit_mb":512}'
```

## 限制和注意事项

- 单次执行最大输出（stdout + stderr）为 2 MB；超出部分将被截断  
- 沙箱实例默认存活 10 分钟，超时未操作将自动销毁，不可续期  
- 禁止访问外部网络（包括 DNS 解析）、挂载宿主机路径、执行特权指令（如 `sudo`、`mount`）  
- 所有代码执行日志仅保留 7 天，调试建议主动捕获 `stderr`  
- 实例创建频率限制：同一 API Key 每分钟最多 20 次 `POST /v1/sandboxes` 请求  

请参考完整接口定义与错误码说明：[原文标题](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


