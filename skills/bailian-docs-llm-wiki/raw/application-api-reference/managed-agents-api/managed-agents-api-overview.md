# API 总览与认证

Managed Agents API 是百炼提供的智能体托管运行时，由平台托管会话、沙箱、工具执行与事件流。

## 前提条件

1.  **开通百炼并创建 API Key**：通过[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取，并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
2.  **获取工作空间 ID**：百炼控制台右上角下拉菜单查看，形如 `ws_xxxxxxxxxxxx`。
    

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

## 请求与响应

-   请求体为 JSON，`Content-Type: application/json`
    
-   每次响应携带 `x-request-id` 头，提工单时附上此 ID 可加速定位
    
-   列表端点支持分页：`limit`（默认 20，最大 100）、`page`（首次不传，后续传上一次响应的 `next_page`）。响应不含 `next_page` 表示已是末页
    

## 可用 API

**资源**

**端点**

**用途**

[Agent](https://help.aliyun.com/zh/model-studio/agent-api/)

`POST /agents`

创建 Agent

`GET /agents/{agent_id}`

获取 Agent

`GET /agents`

列出 Agent

`PATCH /agents/{agent_id}`

更新 Agent（自动生成新版本号）

`POST /agents/{agent_id}/archive`

归档 Agent

[Environment](https://help.aliyun.com/zh/model-studio/environment-api/)

`POST /environments`

创建 Environment

`GET /environments/{environment_id}`

获取 Environment

`GET /environments`

列出 Environment

`PATCH /environments/{environment_id}`

更新 Environment

`DELETE /environments/{environment_id}`

删除 Environment

`POST /environments/{environment_id}/archive`

归档 Environment

[Session and Event](https://help.aliyun.com/zh/model-studio/session-api/)

`POST /sessions`

创建 Session

`GET /sessions/{session_id}`

获取 Session

`GET /sessions`

列出 Session

`PATCH /sessions/{session_id}`

更新 Session（如重命名）

`DELETE /sessions/{session_id}`

删除 Session

`POST /sessions/{session_id}/archive`

归档 Session

`POST /sessions/{session_id}/events`

发送 Event（向 Agent 投递用户消息或工具回执）

`GET /sessions/{session_id}/events`

列出 Event 历史；订阅 SSE 事件流（流式输出）

[File](https://help.aliyun.com/zh/model-studio/files-api/)

`POST /files`

上传 File（multipart/form-data）

`GET /files/{file_id}`

查询 File 元数据

`GET /files`

列出 File

`DELETE /files/{file_id}`

删除 File

[Skill](https://help.aliyun.com/zh/model-studio/skills-api/)

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

`GET /skills/{skill_id}/versions/{version}/download`

下载 Skill 包
