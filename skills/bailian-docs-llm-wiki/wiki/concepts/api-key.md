# API Key 鉴权

API Key 是调用阿里云百炼平台模型与应用的核心鉴权凭证，几乎所有 HTTP 接口、SDK 与 CLI 都通过它来标识调用者身份并确定调用权限。

## 概念定义

API Key 是一串以 `sk-`（新版为 `sk-ws` 开头）标识的密钥字符串，用于百炼平台的身份认证与权限控制。它在控制台创建，其调用权限由归属的业务空间决定：同一业务空间内的所有 Key 权限相同，默认业务空间的 Key 可调用所有标准模型，子业务空间的 Key 仅能调用已授权的模型。

## 在不同场景中的使用

### 模型 API / 应用调用鉴权

调用模型 API（DashScope 或 OpenAI 兼容）或智能体/工作流应用时，API Key 通过 HTTP 请求头传递：

```
Authorization: Bearer <API-Key>
```

调用应用时还需额外提供 APP ID；子业务空间场景下需再提供 Workspace ID。

### 环境变量配置（推荐）

为避免在代码中硬编码，建议将 API Key 配置为环境变量 `DASHSCOPE_API_KEY`：

```bash
# Linux / macOS (Bash)
echo "export DASHSCOPE_API_KEY='your-api-key'" >> ~/.bashrc
source ~/.bashrc

# Windows PowerShell（永久）
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-api-key", [EnvironmentVariableTarget]::User)
```

> 设置后，已打开的 IDE、终端需重启才能加载新值；使用 `sudo` 运行脚本时需加 `-E` 参数继承环境变量。

### 临时 API Key（不可信环境）

在浏览器、移动 App 等不可信环境中，应由后端服务生成临时 API Key，避免永久 Key 泄露：

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

- `expire_in_seconds`：有效期（TTL），范围 `[1, 1800]` 秒，默认 60 秒。
- 返回体中 `token`（`st-` 开头）即临时 Key，`expires_at` 为过期 UNIX 时间戳。
- 临时 Key **继承生成它的永久 Key 的全部权限**（含模型/知识库访问限制），到期自动失效，无法提前删除。

### CLI 认证

百炼 CLI（`bl`）支持多种认证方式：

| 方式 | 命令 | 适用场景 |
|------|------|----------|
| 控制台登录（推荐） | `bl auth login --console` | 交互式，模型调用 + 应用管理 |
| API Key | `bl auth login --api-key sk-xxx` | 模型调用 |
| 环境变量 | 配置 API Key 环境变量 | CI/CD、无界面环境 |

### 框架集成

LlamaIndex、Spring AI Alibaba 等框架均以 API Key 鉴权复用百炼能力。注意变量名约定可能不一致（Spring AI Alibaba 应用集成用 `DASHSCOPE_API_KEY`，知识库检索用 `AI_DASHSCOPE_API_KEY`），关键是保证 `application.yml` 中 `${...}` 占位符与实际变量名一致。

### 订阅套餐专属 Key

Token Plan 团队版与 Coding Plan 使用独立的 API Key（均以 `sk-sp-` 开头）和专属 Base URL，与百炼按量付费（`sk-` 通用 Key + `dashscope.aliyuncs.com`）三者完全隔离，必须配套使用，混用会导致意外扣费或 401/403 鉴权失败。

## 关键参数与配置

- **创建入口**：百炼控制台 API Key 页面，使用主账号或有权限的子账号创建。
- **明文展示**：新版 Key 仅在创建时展示一次，关闭弹窗后不可再查看，请立即复制保存。
- **权限配置**：华北2（北京）、新加坡、日本（东京）、德国（法兰克福）支持配置归属业务空间、描述及权限（全部/自定义）；自定义权限可设 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）和可访问模型范围。美国（弗吉尼亚）需选择归属账号，不支持禁用、重置和自定义权限。
- **数量限制**：华北2（北京）等地域每个主账号每地域最多 50 个；美国（弗吉尼亚）每个归属账号最多 20 个。
- **地域隔离**：各地域的 API Key 不互通，请求时须使用对应地域的 Endpoint 与 Key。

## 使用建议

- 生产环境优先使用环境变量注入，切勿硬编码或提交到代码仓库。
- 面向前端/移动端时使用后端签发的临时 Key，缩短暴露时间窗口。
- 按业务线隔离权限或分账时，使用子业务空间的专属 API Key，并预先为该空间授予模型调用权限。

## 关联主题页

- [preparations](../api/preparations.md)
- [more](../api/more.md)
- [more about models](../api/more-about-models.md)
- [frameworks](../api/frameworks.md)
- [application call](../api/application-call.md)
- [knowledge](../api/knowledge.md)
- [token plan guide](../guides/token-plan-guide.md)



