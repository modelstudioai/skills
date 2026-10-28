# 更新日志

Managed Agent 的版本更新记录。

记录 Managed Agent 的功能更新、优化和问题修复。

* * *

## 2026-10-15

### 新功能

-   内置工具新增 `todo_write`：智能体可维护结构化的待办列表，拆解多步任务并跟踪每一步的状态。详见[Agent 工具配置](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
-   可选模型新增 `deepseek-v4.1-flash`、`deepseek-v4.1-flash-1017`、`glm-5.3`。详见[定义 Agent](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。

## 2026-10-14

### 新功能

-   会话级 Agent 配置覆盖与 MCP 请求头：创建会话时可通过 `agent` 对象覆盖系统提示词、工具、MCP Server 与技能，并通过 `mcp_configs` 为指定 MCP Server 注入自定义请求头。详见[发起会话](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)。

## 2026-10-08

### 新功能

-   环境预热：配置预装包的环境创建后可能需要预热，准备中的环境无法被会话引用。详见[云端托管环境](raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
-   智能模式：`model.id` 新增 `auto`、`performance`、`balanced`、`economy` 四档路由。详见[定义 Agent](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。

## 2026-09-21

### 新功能

-   单个文件上传上限提升至 50 MB。详见[文件上传与挂载](raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)。

## 2026-09-20

### 新功能

-   定时任务（Scheduled Task，原部署）上线：绑定智能体后按 cron 表达式或手动触发运行，每次触发创建一个会话。详见[定时任务](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)。

## 2026-09-18

### 新功能

-   内置工具新增 `web_search` 与 `web_fetch`：`web_search` 搜索互联网信息，返回相关网页的标题、链接和内容摘要（0.03 元/次）；`web_fetch` 读取指定网页地址的正文内容并转换为文本（限时免费）。详见[Agent 工具配置](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 2026-09-17

### 新功能

-   记忆库（Memory Store）上线：跨会话持久化的挂载资源，记忆库—记忆—版本三层模型，创建会话时挂载（只读/读写），智能体通过文件工具读写，历史版本自动记录并支持查询与擦除。控制台**记忆库**页面与 Memory Store API 同步开放。详见[记忆库](raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)与 [Memory Store API](raw/application-api-reference/managed-agents-api/memory-store-api.md)。

## 2026-09-09

### 新功能

-   会话事件流支持 Delta 增量推送：订阅时通过 `event_deltas[]` 为 `message`、`reasoning` 开启逐块流式输出。详见[会话事件流](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)。

### 变更

-   内置工具 `download_file` 下线，由 `mark_artifacts` 替代，用于登记智能体产物。详见[Agent 工具配置](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 2026-09-07

### 新功能

-   发送 Event 接口（`POST /sessions/{session_id}/events`）的用户消息 `content` 新增多模态内容块：`image`（`image_url` / `file_id`）、`video`（`video_url` / `file_id`）、`file`（`file_id` + `filename`）。图片与视频进入模型多模态视觉通道；文件由平台物化到会话沙箱文件系统，模型通过工具按需读取。详见[发送 Event](raw/application-api-reference/managed-agents-api/session-api/event-post.md)。
-   会话支持环境变量：创建或更新会话时可传入 `environment_variables`，运行时按名读取。详见[发起会话](raw/application-api-reference/managed-agents-api/session-api/session-create.md)。

## 2026-09-04

### 新功能

-   密钥库新增**密钥替换生效域名**和**替换位置**配置。密钥以占位符 `${变量名}` 形式供智能体引用，请求出网时由网关在指定域名的 Authorization 头中替换为真实密钥，未匹配域名只收到占位符。详见[密钥库认证](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)。

## 2026-08-26

### 新功能

-   Webhook 通知上线，支持将会话、智能体、定时任务等资源的状态变更事件推送到指定回调地址。接入方式见 [Webhook 通知](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-webhook.md)，接口契约见 [Webhook API](raw/application-api-reference/managed-agents-api/webhook-api.md)。

## 2026-08-24

### 新功能

-   百炼 CLI 支持 Managed Agent：可通过 `bl managed-agent` 管理 Agent、环境、会话等资源。详见[使用 CLI](raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)。

## 2026-08-18

### 新功能

-   多智能体协作上线：由 coordinator 智能体编排多个成员智能体协同完成任务。详见[多智能体协作](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
-   工具审批策略上线：可按工具设置总是允许或每次询问。详见[Agent 工具配置](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 2026-08-17

-   Managed Agents 正式商业化计费，自 2026-08-17 09:00:00（UTC+8）起生效。计费项、免费额度与示例详见 [计费说明](raw/application-user-guide/agent-development/managed-agents/managed-agents-billing.md)。

## 2026-07-21

### 新功能

-   Managed Agent 功能上线
