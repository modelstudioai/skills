# 概览

Managed Agents API 是阿里云百炼提供的智能体托管运行时，由平台托管会话、沙箱、工具执行与事件流。

> **说明**
>
> 调用前请先配置[认证](managed-agents-api-authentication.md)；错误处理见[错误码](managed-agents-api-errors.md)。

<a id="前提条件"></a>

<a id="1cea3ecb89xo6"></a>

## 前提条件

1.  已开通阿里云百炼，并[创建 API Key](managed-agents-api-authentication.md)。
2.  **获取工作空间 ID**：阿里云百炼控制台右上角下拉菜单查看，形如 `ws_xxxxxxxxxxxx`。

<a id="endpoint"></a>

<a id="b9b8655d4821h"></a>

## Endpoint

API 基地址按工作空间与地域拼装：

<a id="code-block"></a>

```text
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio
```

-   `workspace_id`：工作空间 ID，例如 `ws_xxxxxxxxxxxx`
-   `region`：地域 ID，当前仅支持 `cn-beijing`

<a id="sdk"></a>

<a id="h-sdk"></a>

## SDK

除直接调用 REST 接口外，还可通过 Python 或 Java SDK 接入。Managed Agents 模块要求 Python SDK v1.26.2 及以上、Java SDK v2.22.24 及以上。若已安装旧版本，请重新执行安装命令以升级。

会话级智能体配置覆盖（`agent` 对象与 patch）和会话级 MCP 请求头（`mcp_configs`）需要 Python SDK v1.27.7 及以上、Java SDK v2.23.2 及以上；直接调用 REST 接口不受此限制。

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

python

<a id="code-code-group-python"></a>

```python
pip install dashscope
```

<a id="fig-code-group-java-tab"></a>

java

<a id="code-code-group-java"></a>

```java
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
</dependency>
```

<a id="请求与响应"></a>

<a id="h-req-resp"></a>

## 请求与响应

-   请求体为 JSON，`Content-Type: application/json`
-   每次响应携带 `x-request-id` 头，可用于定位具体请求
-   列表端点支持分页：`limit`（默认 20，最大 100）、`page`（首次不传，后续传上一次响应的 `next_page`）。响应不含 `next_page` 表示已是末页

<a id="可用-api"></a>

<a id="h-apis"></a>

## 可用 API

<table><thead><tr><th><p><strong>资源</strong></p></th><th><p><strong>端点</strong></p></th><th><p><strong>用途</strong></p></th></tr></thead><tbody><tr><td rowspan="5"><p><a href="agent-api.md">Agent</a></p></td><td><p><code>POST /agents</code></p></td><td><p>创建 Agent</p></td></tr><tr><td><p><code>GET /agents/{agent_id}</code></p></td><td><p>获取 Agent</p></td></tr><tr><td><p><code>GET /agents</code></p></td><td><p>列出 Agent</p></td></tr><tr><td><p><code>POST /agents/{agent_id}</code></p></td><td><p>更新 Agent（自动生成新版本号）</p></td></tr><tr><td><p><code>POST /agents/{agent_id}/archive</code></p></td><td><p>归档 Agent</p></td></tr><tr><td rowspan="6"><p><a href="environment-api.md">Environment</a></p></td><td><p><code>POST /environments</code></p></td><td><p>创建 Environment</p></td></tr><tr><td><p><code>GET /environments/{environment_id}</code></p></td><td><p>获取 Environment</p></td></tr><tr><td><p><code>GET /environments</code></p></td><td><p>列出 Environment</p></td></tr><tr><td><p><code>POST /environments/{environment_id}</code></p></td><td><p>更新 Environment</p></td></tr><tr><td><p><code>DELETE /environments/{environment_id}</code></p></td><td><p>删除 Environment</p></td></tr><tr><td><p><code>POST /environments/{environment_id}/archive</code></p></td><td><p>归档 Environment</p></td></tr><tr><td rowspan="8"><p><a href="session-api.md">Session and Event</a></p></td><td><p><code>POST /sessions</code></p></td><td><p>创建 Session</p></td></tr><tr><td><p><code>GET /sessions/{session_id}</code></p></td><td><p>获取 Session</p></td></tr><tr><td><p><code>GET /sessions</code></p></td><td><p>列出 Session</p></td></tr><tr><td><p><code>POST /sessions/{session_id}</code></p></td><td><p>更新 Session（如重命名）</p></td></tr><tr><td><p><code>DELETE /sessions/{session_id}</code></p></td><td><p>删除 Session</p></td></tr><tr><td><p><code>POST /sessions/{session_id}/archive</code></p></td><td><p>归档 Session</p></td></tr><tr><td><p><code>POST /sessions/{session_id}/events</code></p></td><td><p>发送 Event（向 Agent 投递用户消息或工具回执）</p></td></tr><tr><td><p><code>GET /sessions/{session_id}/events</code></p></td><td><p>列出 Event 历史；订阅 SSE 事件流（流式输出）</p></td></tr><tr><td rowspan="4"><p><a href="files-api.md">File</a></p></td><td><p><code>POST /files</code></p></td><td><p>上传 File（multipart/form-data）</p></td></tr><tr><td><p><code>GET /files/{file_id}</code></p></td><td><p>查询 File 元数据</p></td></tr><tr><td><p><code>GET /files</code></p></td><td><p>列出 File</p></td></tr><tr><td><p><code>DELETE /files/{file_id}</code></p></td><td><p>删除 File</p></td></tr><tr><td rowspan="13"><p><a href="memory-store-api.md">Memory Store</a></p></td><td><p><code>POST /memory_stores</code></p></td><td><p>创建 Memory Store</p></td></tr><tr><td><p><code>GET /memory_stores</code></p></td><td><p>列出 Memory Store</p></td></tr><tr><td><p><code>GET /memory_stores/{memory_store_id}</code></p></td><td><p>获取 Memory Store</p></td></tr><tr><td><p><code>POST /memory_stores/{memory_store_id}</code></p></td><td><p>更新 Memory Store</p></td></tr><tr><td><p><code>POST /memory_stores/{memory_store_id}/archive</code></p></td><td><p>归档 Memory Store</p></td></tr><tr><td><p><code>POST /memory_stores/{memory_store_id}/memories</code></p></td><td><p>创建 Memory（记忆文件）</p></td></tr><tr><td><p><code>GET /memory_stores/{memory_store_id}/memories</code></p></td><td><p>列出 Memory</p></td></tr><tr><td><p><code>GET /memory_stores/{memory_store_id}/memories/{memory_id}</code></p></td><td><p>获取 Memory</p></td></tr><tr><td><p><code>POST /memory_stores/{memory_store_id}/memories/{memory_id}</code></p></td><td><p>更新 Memory</p></td></tr><tr><td><p><code>DELETE /memory_stores/{memory_store_id}/memories/{memory_id}</code></p></td><td><p>删除 Memory</p></td></tr><tr><td><p><code>GET /memory_stores/{memory_store_id}/memory_versions</code></p></td><td><p>列出 Memory Version（历史版本）</p></td></tr><tr><td><p><code>GET /memory_stores/{memory_store_id}/memory_versions/{memory_version_id}</code></p></td><td><p>获取 Memory Version</p></td></tr><tr><td><p><code>POST /memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact</code></p></td><td><p>擦除 Memory Version 正文</p></td></tr><tr><td rowspan="8"><p><a href="skills-api.md">Skill</a></p></td><td><p><code>POST /skills</code></p></td><td><p>创建 Skill</p></td></tr><tr><td><p><code>GET /skills/{skill_id}</code></p></td><td><p>查询 Skill</p></td></tr><tr><td><p><code>GET /skills</code></p></td><td><p>列出 Skill</p></td></tr><tr><td><p><code>DELETE /skills/{skill_id}</code></p></td><td><p>删除 Skill</p></td></tr><tr><td><p><code>POST /skills/{skill_id}/versions</code></p></td><td><p>上传 Skill 新版本</p></td></tr><tr><td><p><code>GET /skills/{skill_id}/versions/{version}</code></p></td><td><p>查询 Skill 版本</p></td></tr><tr><td><p><code>GET /skills/{skill_id}/versions</code></p></td><td><p>列出 Skill 版本</p></td></tr><tr><td><p><code>GET /skills/{skill_id}/versions/{version}/content</code></p></td><td><p>下载 Skill 包</p></td></tr><tr><td rowspan="6"><p><a href="vault-api.md">Vault</a></p></td><td><p><code>POST /vaults</code></p></td><td><p>创建 Vault</p></td></tr><tr><td><p><code>GET /vaults/{vault_id}</code></p></td><td><p>获取 Vault</p></td></tr><tr><td><p><code>GET /vaults</code></p></td><td><p>列出 Vault</p></td></tr><tr><td><p><code>POST /vaults/{vault_id}</code></p></td><td><p>更新 Vault</p></td></tr><tr><td><p><code>DELETE /vaults/{vault_id}</code></p></td><td><p>删除 Vault</p></td></tr><tr><td><p><code>POST /vaults/{vault_id}/archive</code></p></td><td><p>归档 Vault</p></td></tr><tr><td rowspan="6"><p><a href="credential-api.md">Credential</a></p></td><td><p><code>POST /vaults/{vault_id}/credentials</code></p></td><td><p>创建 Credential</p></td></tr><tr><td><p><code>GET /vaults/{vault_id}/credentials/{credential_id}</code></p></td><td><p>获取 Credential</p></td></tr><tr><td><p><code>GET /vaults/{vault_id}/credentials</code></p></td><td><p>列出 Credential</p></td></tr><tr><td><p><code>POST /vaults/{vault_id}/credentials/{credential_id}</code></p></td><td><p>更新 Credential</p></td></tr><tr><td><p><code>DELETE /vaults/{vault_id}/credentials/{credential_id}</code></p></td><td><p>删除 Credential</p></td></tr><tr><td><p><code>POST /vaults/{vault_id}/credentials/{credential_id}/archive</code></p></td><td><p>归档 Credential</p></td></tr><tr><td rowspan="10"><p><a href="webhook-api.md">Webhook</a></p></td><td><p><code>POST /webhook_endpoints</code></p></td><td><p>创建 Webhook</p></td></tr><tr><td><p><code>GET /webhook_endpoints/{id}</code></p></td><td><p>查询 Webhook 详情</p></td></tr><tr><td><p><code>GET /webhook_endpoints</code></p></td><td><p>查询 Webhook 列表</p></td></tr><tr><td><p><code>PUT /webhook_endpoints/{id}</code></p></td><td><p>更新 Webhook</p></td></tr><tr><td><p><code>DELETE /webhook_endpoints/{id}</code></p></td><td><p>删除 Webhook</p></td></tr><tr><td><p><code>POST /webhook_endpoints/{id}/enable</code></p></td><td><p>启用 Webhook</p></td></tr><tr><td><p><code>POST /webhook_endpoints/{id}/disable</code></p></td><td><p>禁用 Webhook</p></td></tr><tr><td><p><code>POST /webhook_endpoints/{id}/test</code></p></td><td><p>测试 Webhook</p></td></tr><tr><td><p><code>POST /webhook_endpoints/{id}/reset_secret</code></p></td><td><p>重置 Signing Secret</p></td></tr><tr><td><p><code>GET /webhook_endpoints/{id}/events</code></p></td><td><p>查询 Webhook 事件</p></td></tr><tr><td rowspan="2"><p><a href="usage-api.md">Usage</a></p></td><td><p><code>POST /usage/summary</code></p></td><td><p>查询用量汇总（工作空间、Agent 或 Session）</p></td></tr><tr><td><p><code>POST /usage/trend</code></p></td><td><p>分页查询用量趋势（工作空间或 Agent）</p></td></tr></tbody></table>
