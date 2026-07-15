# API Key 鉴权

API Key 是阿里云百炼平台调用模型与应用的核心鉴权凭证：请求通过在 HTTP 头 `Authorization: Bearer <API Key>` 中携带该密钥完成身份校验，无需为不同模态单独申请。

## 获取与配置

- **创建**：需主账号或具备 `管理员` / `API-Key` 页面权限的子账号，在[阿里云百炼控制台](https://bailian.console.aliyun.com/)对应地域的 **API Key** 页面创建。
- **归属业务空间**：决定 Key 的调用范围。默认业务空间的 Key 可调用所有标准模型及默认空间应用；子业务空间的 Key 只能调用已授权的模型及本空间应用，同一空间内 Key 权限相同。
- **权限**：可选 **全部**，或 **自定义**（配置 IP 白名单最多 20 个 IPv4/IPv6 地址/网段，并限定可访问的模型/应用范围）。
- **环境变量**：推荐配置到 `DASHSCOPE_API_KEY`，避免硬编码泄漏（各系统方式：`~/.bashrc`、`~/.zshrc`、`~/.bash_profile`，或 Windows 系统属性 / `setx` / PowerShell）。
- **服务端点**：调用时除 Key 外还需指定 `base_url`（即创建弹窗中的 API Host），OpenAI 兼容协议与 Anthropic 兼容协议的 `base_url` 不同，且随地域变化。

> 安全升级后新建的按量付费 Key 以 `sk-ws` 开头，**仅创建时明文展示一次**，务必立即复制保存；升级前 `sk-` 开头的旧 Key 仍可使用。

## Key 的类型（互不通用）

不同计费方案使用格式不同、完全隔离的 Key，混用会导致 401/403 或意外走按量计费扣费：

| 前缀 | 类型 | 说明 |
| --- | --- | --- |
| `sk-` | 按量付费通用 Key（旧） | 升级前创建，仍可用 |
| `sk-ws` | 按量付费通用 Key（新） | 安全升级后创建，明文仅展示一次 |
| `sk-sp-` | Token Plan / Coding Plan 专属 Key | 订阅套餐专用，与通用 Key 隔离 |
| `st-` | 临时 API Key | 由永久 Key 生成，有时效 |

各地域（北京 / 新加坡 / 弗吉尼亚）的 API Key 不互通，请求时须使用对应地域的 Endpoint 与 Key。

## 典型使用场景

### 1. SDK / 直接调用模型

配置好 `DASHSCOPE_API_KEY` 后，即可用官方 DashScope SDK（Python、Java）或 OpenAI 兼容 SDK（Python、Java、Node.js、Go）发起文本、图像、视频、语音、向量等调用。

### 2. 百炼 CLI（`bl` / `bailian`）

支持多种可组合的认证方式：

| 方式 | 命令 | 场景 |
| --- | --- | --- |
| 控制台登录（推荐） | `bl auth login --console` | 模型调用 + 应用管理 |
| API Key | `bl auth login --api-key sk-xxx` | 模型调用，会校验有效性 |
| 环境变量 | 配置 API Key 环境变量 | CI/CD、无界面环境 |
| 配置文件 | `bl config set --key api_key --value sk-xxx` | 持久化，**不校验** |
| 临时传入 | `bl text chat --api-key sk-xxx ...` | 单次调用，不落盘 |

### 3. 第三方 AI 工具接入

Claude Code、Cursor、Cline、Codex、Qoder、Dify 等工具统一以「Base URL + API Key + 模型 ID」接入，通过 OpenAI 兼容或 Anthropic 兼容协议访问百炼网关。务必保证 Key 与 Base URL 的计费方案、地域一致。

### 4. 开源框架集成

LlamaIndex（Python）、Spring AI Alibaba（Java）均以 API Key 鉴权。注意 Spring AI Alibaba 两篇文档约定的变量名不一致：应用集成用 `DASHSCOPE_API_KEY`，知识库检索用 `AI_DASHSCOPE_API_KEY`，关键是 `application.yml` 中 `${...}` 占位符与实际变量名匹配。

### 5. 子业务空间调用

按业务线隔离权限或分账时，必须使用子业务空间自身的 Key，并提前为该空间授予标准模型（如 `qwen-plus`）的调用权限；调优部署的模型仅能由所在空间的 Key 调用。

## 临时 API Key

在浏览器、移动端等不可信环境中，应由后端用永久 Key 生成时效性临时凭证，避免永久 Key 泄露。

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**关键要点**：

- `expire_in_seconds`：有效期（TTL），单位秒，范围 `[1, 1800]`，默认 60 秒。
- 响应返回 `token`（`st-` 开头的临时 Key）与 `expires_at`（过期 UNIX 时间戳）。
- 临时 Key 继承永久 Key 的全部权限（含模型/知识库访问限制），到期自动失效，无法提前删除。
- 各地域不互通；新加坡地域需将 Endpoint 中的 `WorkspaceId` 替换为实际值。

## 编程化管理

除控制台外，百炼提供 OpenAPI（`CreateApiKey` / `GetApiKey` / `ListApiKeys` / `UpdateApiKey` / `DeleteApiKey` / `EnableApiKey` / `DisableApiKey` / `ResetApiKey`）管理 Key，调用需使用阿里云账号 AccessKey 签名认证并具备相应 RAM 权限。

## 常见排错

- **401 / 403 鉴权失败**：多因误用了错误前缀的 Key，或 Key 与 Base URL 的地域 / 计费方案不匹配。
- **意外扣费**：套餐场景误用通用 `sk-` Key 会走按量计费通道。
- **`InvalidApiKey`**：临时 Key 接口常见错误码，检查永久 Key 是否有效、Endpoint 地域是否对应。

## 关联主题页

- [preparations](../api/preparations.md)
- [more](../api/more.md)
- [more about models](../api/more-about-models.md)
- [frameworks](../api/frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [token plan guide](../guides/token-plan-guide.md)


