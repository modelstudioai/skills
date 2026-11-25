# 概览

OpenAI 兼容 API 的 Endpoint、认证方式和可用接口。

<a id="前提条件"></a>

<a id="h-oa-prereq"></a>

## 前提条件

1.  已开通阿里云百炼，并[创建 API Key](openai-compatible-agents-api-authentication.md)。
2.  已获取工作空间 ID（`ws_xxxxxxxxxxxx`）。

<a id="endpoint"></a>

<a id="h-oa-endpoint"></a>

## Endpoint

<a id="code-block"></a>

```text
https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
```

-   `workspace_id`：工作空间 ID。
-   当前地域为 `cn-beijing`。
-   将 `{workspace_id}` 替换为实际工作空间 ID。
-   请求路径拼接在 Base URL 之后，例如 `POST {Base URL}/agents`。

<a id="认证"></a>

<a id="h-oa-auth"></a>

## 认证

全部请求通过 HTTP Header 携带 API Key：

<a id="code-block-2"></a>

```text
Authorization: Bearer $DASHSCOPE_API_KEY
```

兼容客户端可以同时发送 `OpenAI-Beta: agents=v1`；该接口不依赖该 Header 选择默认值。鉴权、工作空间路由和权限配置见[认证](openai-compatible-agents-api-authentication.md)。

<a id="可用-api"></a>

<a id="h-oa-apis"></a>

## 可用 API

| 资源 | 端点 | 用途 |
| --- | --- | --- |
| [Agent](openai-compatible-agents-api-agent.md) | `POST /agents` | 创建可复用 Agent |
|  | `GET /agents/{agent_id}` | 获取 Agent |
|  | `GET /agents` | 列出 Agent |
|  | `POST /agents/{agent_id}` | 更新 Agent |
|  | `DELETE /agents/{agent_id}` | 删除 Agent |
| [Session](openai-compatible-agents-api-session.md) | `POST /agents/sessions` | 创建 Session 并提交首轮输入 |
|  | `GET /agents/sessions` | 列出 Session |
|  | `GET /agents/sessions/{session_id}` | 获取 Session |
|  | `POST /agents/sessions/{session_id}` | 更新 Session 配置 |
|  | `DELETE /agents/sessions/{session_id}` | 删除 Session |
| [Event](../../_short/openai-compatible-agents-api-event-e5798de5ec27ab06.md) | `POST /agents/sessions/{session_id}/events` | 提交消息、取消或工具结果 |
|  | `GET /agents/sessions/{session_id}/events` | 订阅实时 SSE 事件流 |
| [History](../../_short/openai-compatible-agents-api-turns-0aaad77002ed96fb.md) | `GET /agents/sessions/{session_id}/turns` | 查询 Turn |
|  | `GET /agents/sessions/{session_id}/items` | 查询 Item |
|  | `GET /agents/sessions/{session_id}/subagents` | 查询子 Agent |
| [Environment](openai-compatible-agents-api-environment.md) | `POST /agents/environments` | 创建托管环境 |
|  | `GET /agents/environments/{environment_id}` | 获取环境 |
|  | `GET /agents/environments` | 列出环境 |
|  | `GET /agents/environments/templates` | 列出环境模板 |
|  | `GET /agents/environments/templates/{template_id}` | 获取环境模板 |
|  | `POST /agents/environments/templates` | 创建环境模板 |
|  | `POST /agents/environments/templates/{template_id}` | 更新环境模板 |
|  | `DELETE /agents/environments/templates/{template_id}` | 删除环境模板 |
| [File](../../_short/openai-compatible-agents-api-file-118d31ecb47de41d.md) | `POST /agents/file` | 上传源文件 |
|  | `GET /agents/file` | 列出源文件 |
|  | `GET /agents/file/{file_id}` | 获取源文件 |
|  | `DELETE /agents/file/{file_id}` | 删除源文件 |
|  | `POST /agents/environments/{environment_id}/files` | 将源文件写入环境 |
| [Artifact](../../_short/openai-compatible-agents-api-artifact-320164f67e4f22df.md) | `GET /agents/sessions/{session_id}/artifacts` | 查询产物 |
|  | `GET /agents/sessions/{session_id}/artifacts/{artifact_id}/content` | 下载产物 |
| [Vault](openai-compatible-agents-api-vault.md) | `POST /vaults` | 创建 Vault |
|  | `POST /vaults/{vault_id}/credentials` | 创建 Credential |

上表是常用接口示例，不是完整清单；完整接口见左侧导航。

<a id="sdk-安装"></a>

<a id="h-oa-sdk"></a>

## SDK 安装

安装 OpenAI Python SDK：

<a id="code-block-3"></a>

```bash
pip install openai requests
```

调用示例见[快速开始](openai-compatible-agents-api-quickstart.md)。
