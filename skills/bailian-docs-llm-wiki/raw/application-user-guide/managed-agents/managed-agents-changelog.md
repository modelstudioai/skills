# 更新日志

Managed Agent 的版本更新记录。

记录 Managed Agent 的功能更新、优化和问题修复。

* * *

## 2026-09-18

### 新功能

-   内置工具新增 `web_search` 与 `web_fetch`：`web_search` 搜索互联网信息，返回相关网页的标题、链接和内容摘要（0.03 元/次）；`web_fetch` 读取指定网页地址的正文内容并转换为文本（限时免费）。详见[Agent 工具配置](raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 2026-09-17

### 新功能

-   记忆库（Memory Store）上线：跨会话持久化的挂载资源，记忆库—记忆—版本三层模型，创建会话时挂载（只读/读写），智能体通过文件工具读写，历史版本自动记录并支持查询与擦除。控制台**记忆库**页面与 Memory Store API 同步开放。详见[记忆库](raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)与 [Memory Store API](raw/application-api-reference/managed-agents-api/memory-store-api.md)。

## 2026-09-07

### 新功能

-   发送 Event 接口（`POST /sessions/{session_id}/events`）的用户消息 `content` 新增多模态内容块：`image`（`image_url` / `file_id`）、`video`（`video_url` / `file_id`）、`file`（`file_id` + `filename`）。图片与视频进入模型多模态视觉通道；文件由平台物化到会话沙箱文件系统，模型通过工具按需读取。详见[发送 Event](raw/application-api-reference/managed-agents-api/session-api/event-post.md)。

## 2026-09-04

### 新功能

-   密钥库新增**密钥替换生效域名**和**替换位置**配置。密钥以占位符 `${变量名}` 形式供智能体引用，请求出网时由网关在指定域名的 Authorization 头中替换为真实密钥，未匹配域名只收到占位符。详见[密钥库认证](raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。

## 2026-08-26

### 新功能

-   Webhook 通知上线，支持将会话、智能体、定时任务等资源的状态变更事件推送到指定回调地址。接入方式见 [Webhook 通知](raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)，接口契约见 [Webhook API](raw/application-api-reference/managed-agents-api/webhook-api.md)。

## 2026-08-17

-   Managed Agents 正式商业化计费，自 2026-08-17 09:00:00（UTC+8）起生效。计费项、免费额度与示例详见 [计费说明](raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 2026-07-21

### 新功能

-   Managed Agent 文档上线
