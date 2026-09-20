# API 总览与认证

Managed Agents API 是阿里云百炼提供的智能体托管运行时，由平台托管会话、沙箱、工具执行与事件流。

## 前提条件

1.  **开通阿里云百炼并创建 API Key**：通过[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取，并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
2.  **获取工作空间 ID**：阿里云百炼控制台右上角下拉菜单查看，形如 `ws_xxxxxxxxxxxx`。

## Endpoint

API 基地址按工作空间与地域拼装：

```
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio
```

-   `workspace_id`：工作空间 ID，例如 `ws_xxxxxxxxxxxx`
-   `region`：地域 ID，当前仅支持 `cn-beijing`

## 鉴权

全部请求通过 HTTP Header 携带 API Key，一个 Key 可访问其归属工作空间下的全部资源。

```
Authorization: Bearer <your-api-key>
```

## SDK

除直接调用 REST 接口外，还可通过 Python 或 Java SDK 接入。Managed Agents 模块要求 Python SDK v1.26.2 及以上、Java SDK v2.22.24 及以上。若已安装旧版本，请重新执行安装命令以升级。

python

```
pip install dashscope
```

java

```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
</dependency>
```

## 请求与响应

-   请求体为 JSON，`Content-Type: application/json`
-   每次响应携带 `x-request-id` 头，提工单时附上此 ID 可加速定位
-   列表端点支持分页：`limit`（默认 20，最大 100）、`page`（首次不传，后续传上一次响应的 `next_page`）。响应不含 `next_page` 表示已是末页

## 可用 API

**资源**

**端点**

**用途**

[Agent](raw/application-api-reference/managed-agents-api/agent-api.md)

`POST /agents`

创建 Agent

`GET /agents/{agent_id}`

获取 Agent

`GET /agents`

列出 Agent

`POST /agents/{agent_id}`

更新 Agent（自动生成新版本号）

`POST /agents/{agent_id}/archive`

归档 Agent

[Environment](raw/application-api-reference/managed-agents-api/environment-api.md)

`POST /environments`

创建 Environment

`GET /environments/{environment_id}`

获取 Environment

`GET /environments`

列出 Environment

`POST /environments/{environment_id}`

更新 Environment

`DELETE /environments/{environment_id}`

删除 Environment

`POST /environments/{environment_id}/archive`

归档 Environment

[Session and Event](raw/application-api-reference/managed-agents-api/session-api.md)

`POST /sessions`

创建 Session

`GET /sessions/{session_id}`

获取 Session

`GET /sessions`

列出 Session

`POST /sessions/{session_id}`

更新 Session（如重命名）

`DELETE /sessions/{session_id}`

删除 Session

`POST /sessions/{session_id}/archive`

归档 Session

`POST /sessions/{session_id}/events`

发送 Event（向 Agent 投递用户消息或工具回执）

`GET /sessions/{session_id}/events`

列出 Event 历史；订阅 SSE 事件流（流式输出）

[File](raw/application-api-reference/managed-agents-api/files-api.md)

`POST /files`

上传 File（multipart/form-data）

`GET /files/{file_id}`

查询 File 元数据

`GET /files`

列出 File

`DELETE /files/{file_id}`

删除 File

[Memory Store](raw/application-api-reference/managed-agents-api/memory-store-api.md)

`POST /memory_stores`

创建 Memory Store

`GET /memory_stores`

列出 Memory Store

`GET /memory_stores/{memory_store_id}`

获取 Memory Store

`POST /memory_stores/{memory_store_id}`

更新 Memory Store

`POST /memory_stores/{memory_store_id}/archive`

归档 Memory Store

`POST /memory_stores/{memory_store_id}/memories`

创建 Memory（记忆文件）

`GET /memory_stores/{memory_store_id}/memories`

列出 Memory

`GET /memory_stores/{memory_store_id}/memories/{memory_id}`

获取 Memory

`POST /memory_stores/{memory_store_id}/memories/{memory_id}`

更新 Memory

`DELETE /memory_stores/{memory_store_id}/memories/{memory_id}`

删除 Memory

`GET /memory_stores/{memory_store_id}/memory_versions`

列出 Memory Version（历史版本）

`GET /memory_stores/{memory_store_id}/memory_versions/{memory_version_id}`

获取 Memory Version

`POST /memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact`

擦除 Memory Version 正文

[Skill](raw/application-api-reference/managed-agents-api/skills-api.md)

`POST /skills`

创建 Skill

`GET /skills/{skill_id}`

查询 Skill

`GET /skills`

列出 Skill

`DELETE /skills/{skill_id}`

删除 Skill

`POST /skills/{skill_id}/versions`

上传 Skill 新版本

`GET /skills/{skill_id}/versions/{version}`

查询 Skill 版本

`GET /skills/{skill_id}/versions`

列出 Skill 版本

`GET /skills/{skill_id}/versions/{version}/content`

下载 Skill 包

[Vault](raw/application-api-reference/managed-agents-api/vault-api.md)

`POST /vaults`

创建 Vault

`GET /vaults/{vault_id}`

获取 Vault

`GET /vaults`

列出 Vault

`POST /vaults/{vault_id}`

更新 Vault

`DELETE /vaults/{vault_id}`

删除 Vault

`POST /vaults/{vault_id}/archive`

归档 Vault

[Credential](raw/application-api-reference/managed-agents-api/credential-api.md)

`POST /vaults/{vault_id}/credentials`

创建 Credential

`GET /vaults/{vault_id}/credentials/{credential_id}`

获取 Credential

`GET /vaults/{vault_id}/credentials`

列出 Credential

`POST /vaults/{vault_id}/credentials/{credential_id}`

更新 Credential

`DELETE /vaults/{vault_id}/credentials/{credential_id}`

删除 Credential

`POST /vaults/{vault_id}/credentials/{credential_id}/archive`

归档 Credential

[Webhook](raw/application-api-reference/managed-agents-api/webhook-api.md)

`POST /webhook_endpoints`

创建 Webhook

`GET /webhook_endpoints/{id}`

查询 Webhook 详情

`GET /webhook_endpoints`

查询 Webhook 列表

`PUT /webhook_endpoints/{id}`

更新 Webhook

`DELETE /webhook_endpoints/{id}`

删除 Webhook

`POST /webhook_endpoints/{id}/enable`

启用 Webhook

`POST /webhook_endpoints/{id}/disable`

禁用 Webhook

`POST /webhook_endpoints/{id}/test`

测试 Webhook

`POST /webhook_endpoints/{id}/reset_secret`

重置 Signing Secret

`GET /webhook_endpoints/{id}/events`

查询 Webhook 事件
