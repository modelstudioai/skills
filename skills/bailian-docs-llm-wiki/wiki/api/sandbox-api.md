# [sandbox](../guides/sandbox.md) api

[sandbox](../guides/sandbox.md) api 是百炼平台提供的轻量级代码执行环境接口，用于安全隔离地运行用户提交的 Python 代码片段，适用于代码验证、教学演示和自动化测试等场景。该 API 不提供持久化计算资源，所有执行均在临时沙箱实例中完成，生命周期由请求控制。详细设计目标与安全边界见 [Sandbox](../../raw/application-api-reference/sandbox-api.md)。

## 支持的模型/功能

- 仅支持 Python 3.9–3.12 运行时（不支持其他语言或自定义镜像）  
- 支持标准库及常用科学计算包（`numpy`, `pandas`, `requests`, `matplotlib` 等），具体依赖列表以 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中的“可用库”章节为准  
- 提供同步执行（`/v1/sandbox/run`）与异步执行（`/v1/sandbox/submit` + `/v1/sandbox/status/{task_id}`）两种模式  
- **不支持**文件持久化、网络外连（除白名单域名如 `httpbin.org`、`api.bailian.ai` 外）、系统调用或进程派生  

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | string | 是 | 待执行的 Python 源码（UTF-8 编码，最大 10 KB） |
| `timeout` | integer | 否 | 执行超时（秒），取值范围 1–30，默认 10 |
| `dependencies` | array of string | 否 | 额外 pip 包名列表（如 `["pyyaml==6.0.1"]`），单次请求最多 5 个，总安装时间计入 timeout |
| `stdout_limit` | integer | 否 | 标准输出截断长度（字节），默认 4096，最大 65536 |

> **注意**：原始文档 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 中提及的 `memory_limit_mb` 参数已废弃，当前版本不再接受该字段，设置将被忽略；请以 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 的最新参数表为准。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <access_token>`，[Token](../concepts/token.md) 通过百炼平台应用密钥生成（参见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）  
2. **同步调用示例**（cURL）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/sandbox/run \
     -H "Authorization: Bearer $DASHSCOPE_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "code": "print(2 + 2)",
           "timeout": 5
         }'
   ```
3. **响应结构**包含 `status`（`success`/`timeout`/`error`）、`stdout`、`stderr`、`exit_code` 和 `duration_ms`

## 限制和注意事项

- 单次请求最大 `code` 长度为 10 KB；`dependencies` 总长度（含版本号）不超过 500 字符  
- 每个 API Key 每分钟限流 60 次（同步+异步合并计数），超出返回 `429 Too Many Requests`  
- 沙箱实例无状态，不保留任何上下文（包括 `import` 缓存、全局变量、临时文件），每次调用均为全新环境  
- 异步任务最长保留结果 24 小时，超时后 `GET /status/{task_id}` 返回 `404`  
- 若发现 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 文档中描述的“预置模板 ID 复用”功能在实际 API 中返回 `400 Unsupported template`，请忽略该文档内容——该功能尚未上线，当前所有执行必须显式传入 `code`

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


