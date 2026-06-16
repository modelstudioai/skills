# API Key 管理

API Key 是调用阿里云百炼平台模型和应用的鉴权凭证，用于标识调用者身份并控制访问权限。所有通过 API 方式调用百炼模型、应用和数据服务的请求都必须携带有效的 API Key。

## 基本概念

每个 API Key 归属于一个**地域**内的一个**[业务空间](workspace.md)**和一个**用户**，不可转移。API Key 的可调用功能和模型限流由其归属的[业务空间](workspace.md)决定，同一空间内的 API Key 权限相同，无需为不同模型类型（文生文、文生图、语音合成等）分别创建。

百炼支持以下几种 API Key 格式：

| 格式 | 类型 | 用途 |
|------|------|------|
| `sk-xxxxx` | 百炼通用 API Key | 调用百炼标准模型和应用 |
| `sk-sp-xxxxx` | Token Plan 专属 API Key | Token Plan 团队版专用，不可与通用 Key 混用 |
| `st-xxxxx` | 临时 API Key | 有效期 1–1800 秒，适用于前端等不可信环境 |

## 创建与管理

### 创建权限

创建 API Key 需要使用主账号，或具备「管理员」或「API-Key」页面权限的子账号（RAM 用户）。超级管理员和[业务空间](workspace.md)管理员均可管理 API Key，普通用户无权操作。

### 数量限制

| 地域 | 每个主账号上限 |
|------|--------------|
| 华北2（北京） | 50 个 |
| 新加坡 | 50 个 |
| 德国（法兰克福） | 50 个 |
| 美国（弗吉尼亚） | 20 个 |

### 生命周期

- API Key 创建后**无失效日期**，手动删除后即失效且不可恢复。
- RAM 用户被禁用或删除后，其创建的所有 API Key 均将失效。
- RAM 用户被移出业务空间后，其 API Key 失效；重新加入后可恢复。
- 自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号。

## 不同场景的使用方式

### 模型 API 调用

调用百炼模型 API 时，需要将 API Key 配合对应地域的 Base URL 使用：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

### 第三方工具接入

Claude Code、Cursor、Cline、Cherry Studio 等第三方工具接入百炼时，核心配置均为填入 API Key 和对应计费方案的 Base URL。按量计费、Coding Plan 和 Token Plan 团队版三种方案的 API Key 和 Base URL 互不相通。

### 临时 API Key

在浏览器、移动 App 等不可信环境中，应由后端服务通过 `POST /api/v1/tokens` 接口换取临时 API Key，避免永久 Key 泄露。临时 Key 继承生成它的永久 Key 的全部权限，到期自动失效，不能手动删除。不同地域的永久 Key 互相独立，临时 Key 也必须在对应地域调用。

## 安全配置

### 环境变量配置

为避免在代码中硬编码 API Key 导致泄漏风险，建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`：

```bash
# Linux / macOS
export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'
```

设置后需重启 IDE 或终端才能生效。使用 `sudo` 运行时需加 `-E` 参数传递环境变量。

### IP 白名单

目前仅华北2（北京）地域支持为 API Key 配置 IP 访问白名单，实现更精细的访问控制。

### 数据传输加密

百炼支持对请求体中的 `input` 字段进行加密传输（仅限 DashScope Endpoint），使用 AES + RSA 混合加密机制。DashScope SDK 可一键开启，HTTP 调用需手动管理密钥。

## 权限与业务空间

- **默认业务空间**：API Key 可调用所有标准模型及该空间内的应用，无法设置模型调用限制。
- **子业务空间**：API Key 仅可调用已授权的模型，超级管理员可设置请求数限流和 Token 限流。
- API Key 的权限由归属空间决定，**不受用户控制台权限管理影响**。

## 常见问题

- **API Key 找不到**：确认已设置永久性环境变量并重启了 IDE 或终端。
- **Key 混用报错**：通用 API Key（`sk-`）、Token Plan Key（`sk-sp-`）和 Coding Plan Key 的 Base URL 各不相同，不可混用。
- **权限不足**：确认 API Key 归属的业务空间已开通目标模型的调用权限。
- **RAM 用户 Key 失效**：检查该 RAM 用户是否被禁用、删除或移出了业务空间。

## 关联主题页

- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [token plan guide](../guides/token-plan-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


