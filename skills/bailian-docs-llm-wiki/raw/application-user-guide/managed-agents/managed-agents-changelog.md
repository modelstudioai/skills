# 更新日志

Managed Agent 的版本更新记录。

记录 Managed Agent 的功能更新、优化和问题修复。

* * *

## 2026-09-07

### 新功能

-   发送 Event 接口（`POST /sessions/{session_id}/events`）的用户消息 `content` 新增多模态内容块：`image`（`image_url` / `file_id`）、`video`（`video_url` / `file_id`）、`file`（`file_id` + `filename`）。图片与视频进入模型多模态视觉通道；文件由平台物化到会话沙箱文件系统，模型通过工具按需读取。详见[发送 Event](raw/application-api-reference/managed-agents-api/session-api/event-post.md)。

## 2026-09-04

### 新功能

-   密钥库新增**密钥替换生效域名**和**替换位置**配置。密钥以占位符 `${变量名}` 形式供智能体引用，请求出网时由网关在指定域名的 Authorization 头中替换为真实密钥，未匹配域名只收到占位符。详见[密钥库认证](raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。

## 2026-08-26

### 新功能

-   Webhook 事件订阅上线，支持将会话、智能体、部署等资源的状态变更事件推送到指定回调地址。接入方式见 [Webhook 事件订阅](raw/application-user-guide/managed-agents/managed-agents-webhook.md)，接口契约见 [Webhook API](raw/application-api-reference/managed-agents-api/webhook-api.md)。

## 2026-08-17

-   Managed Agents 正式商业化计费，自 2026-08-17 09:00:00（UTC+8）起生效。计费项、免费额度与示例详见 [计费说明](raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 2026-07-21

### 新功能

-   Managed Agent 文档上线
