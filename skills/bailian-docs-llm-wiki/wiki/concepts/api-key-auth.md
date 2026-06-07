# API Key 与鉴权

API Key 是调用阿里云百炼平台模型和应用服务的唯一鉴权凭证，用于标识调用者身份并控制访问权限。百炼提供永久 API Key、临时 API Key 和订阅制专属 API Key 三类凭证，适用于不同安全级别和业务场景。

## API Key 的类型

百炼平台存在三种 API Key，前缀和用途各不相同：

| 类型 | 前缀 | 获取方式 | 适用场景 |
|------|------|---------|---------|
| 百炼通用 API Key | `sk-` | 百炼控制台 API Key 页面创建 | 标准模型 API 调用 |
| 临时 API Key | `st-` | 通过永久 Key 调用接口换取 | 浏览器、移动端等不可信环境 |
| 订阅制专属 API Key | `sk-sp-` | Token Plan 管理后台或 Coding Plan 控制台 | AI 编程工具（Cursor、Claude Code 等） |

三类 Key 互不相通，混用会导致 `401 Invalid API-key` 错误。

## 获取与管理

### 通用 API Key

在百炼控制台的 API Key 页面创建，需使用主账号或具备相应权限的 RAM 子账号操作。每个主账号在每个地域最多可创建 50 个 API Key（美国弗吉尼亚地域为 20 个）。API Key 无失效日期，删除后立即失效且不可恢复。

### 临时 API Key

适用于浏览器、移动 App 等不可信前端环境。由后端服务通过永久 Key 调用接口换取：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

关键特性：

- 默认有效期 60 秒，可通过 `expire_in_seconds` 参数指定 1-1800 秒
- 完全继承生成它的永久 Key 的权限（含模型、知识库访问限制）
- 到期自动失效，不支持手动删除或提前撤销
- 各地域独立，永久 Key 与临时 Key 必须在同一地域使用

## 权限模型

API Key 的权限由其**归属业务空间**决定：

- 默认业务空间下的 API Key 可调用所有标准模型，且无法限流
- 非默认业务空间的 API Key 仅限已授权的模型，并受请求数和 Token 限流约束
- 单个 API Key 只能归属一个地域内的一个业务空间和一个用户，不可转移
- API Key 的可调用范围与业务空间一致，不受用户控制台权限的影响

自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号。

## 多地域支持

百炼在多个地域提供服务，每个地域有独立的 API Key 体系和 Base URL：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

新加坡和德国地域需将 `{WorkspaceId}` 替换为实际的业务空间 ID。订阅制套餐使用专属 Base URL（如 Token Plan 团队版使用 `token-plan.cn-beijing.maas.aliyuncs.com`），与通用 API 端点不同。

## 安全配置

### 环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码导致泄露：

```bash
# Linux / macOS
echo "export DASHSCOPE_API_KEY='your-api-key'" >> ~/.bashrc
source ~/.bashrc
```

### IP 白名单

华北2（北京）地域支持为 API Key 配置 IP 访问白名单（IPv4/IPv6，最多 20 条），限制 Key 只能从指定 IP 地址调用。

### 传输加密

百炼支持对请求体中的 `input` 字段进行 AES+RSA 混合加密传输。DashScope Java/Python SDK 内置了自动加密功能，只需设置 `enableEncrypt(true)` 或 `enable_encryption=True`。

### 最小权限原则

生产环境建议：

- 按环境划分业务空间（dev/test/prod），为每个空间创建独立 API Key
- 为临时 Key 配置最小权限的永久 Key 作为生成源
- RAM 用户调用 OpenAPI 需主账号在 RAM 控制台单独授权 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`

## 常见错误

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| `InvalidApiKey` | API Key 无效或已删除 | 检查 Key 是否正确、是否已被删除 |
| `401 Invalid API-key` | Key 类型与端点不匹配 | 确认通用 Key 用通用端点、订阅制 Key 用专属端点 |
| `401 invalid access token` | 临时 Key 已过期或端点错误 | 重新生成临时 Key 或检查地域匹配 |
| `400 url error` / `404` | Base URL 与套餐类型不匹配 | 按套餐选择正确的 Base URL |

## 关联主题页

- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [more](../api/more.md)
- [security and compliance](../guides/security-and-compliance.md)
- [token plan guide](../guides/token-plan-guide.md)
- [application permission management](../guides/application-permission-management.md)


