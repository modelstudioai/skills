# API Key

API Key 是调用阿里云百炼大模型服务的鉴权凭证，用于在 API 请求中标识调用者身份并控制访问权限。每个 API Key 归属于特定地域的特定[业务空间](workspace.md)，其权限范围由归属空间的配置决定。

## 创建与获取

在百炼控制台的 API Key 管理页面创建，需使用主账号或具备相应权限的 RAM 子账号：

1. 选择目标地域（华北2北京、新加坡、日本东京、德国法兰克福、美国弗吉尼亚）
2. 点击"创建 API Key"，选择归属[业务空间](workspace.md)和权限配置
3. 创建成功后立即复制保存明文密钥——关闭弹窗后无法再次查看

每个主账号在每个地域最多可创建 50 个 API Key（美国地域每个归属账号最多 20 个）。升级后新创建的 Key 以 `sk-ws` 开头。

## 格式与类型

| 类型 | 前缀 | 用途 |
|------|------|------|
| 永久 API Key | `sk-` 或 `sk-ws` | 通用百炼按量[计费](billing.md)调用 |
| [Token](token.md) Plan 专属 Key | `sk-sp-` | [Token](token.md) Plan / Coding Plan 订阅服务 |
| 临时 API Key | `st-` | 前端等不可信环境的短期授权 |

不同类型的 API Key 对应不同的 Base URL，不可混用。

## 环境变量配置

建议将 API Key 配置到环境变量，避免在代码中硬编码：

```bash
# Linux / macOS
export DASHSCOPE_API_KEY='your-api-key'

# Windows PowerShell（永久）
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-api-key", [EnvironmentVariableTarget]::User)
```

设置后需重启终端或 IDE 才能生效。使用 `sudo` 运行脚本时需加 `-E` 参数继承环境变量。

## 权限与安全

- API Key 权限由归属[业务空间](workspace.md)决定，同一空间内的 Key 权限相同
- 支持自定义 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）和可访问模型范围
- API Key 无过期时间，手动删除后即失效
- 将 RAM 账号移出业务空间会使其 API Key 失效（重新加入后恢复）；在 RAM 控制台删除账号则使 Key 永久失效
- 各地域的 API Key 不互通，调用时必须使用对应地域的 Endpoint

## 临时 API Key

在浏览器、移动端等不可信环境中，应通过后端生成临时 API Key 下发到客户端：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

- 有效期范围 1~1800 秒，默认 60 秒
- 继承生成它的永久 Key 的全部权限，无法进一步收窄
- 到期自动失效，不能提前删除

## 在不同场景中的使用

| 场景 | 说明 |
|------|------|
| 模型 API 调用 | 通过 HTTP Header `Authorization: Bearer <key>` 或 SDK 配置传入 |
| 应用调用 | 调用百炼智能体/工作流应用时作为鉴权凭证 |
| 框架集成 | LlamaIndex、Spring AI Alibaba 等框架通过环境变量读取 |
| Managed Agents API | 一个 Key 可访问其归属工作空间下的全部资源 |
| AI 工具接入 | Cursor、Claude Code、Cline 等工具中配置使用 |
| MCP 服务 | 百炼 MCP 广场服务使用通用 API Key（`sk-`），与套餐专属 Key 分开 |

## 注意事项

- 不要在客户端代码或版本控制中硬编码 API Key
- 不同地域的 Key 和 Endpoint 必须配套使用
- [Token](token.md) Plan 专属 Key（`sk-sp-`）与按量[计费](billing.md) Key（`sk-`）的 Base URL 不同，混用会导致额外扣费或 403 错误
- 单个 API Key 只能归属一个地域内的一个业务空间，不能转移

## 关联主题页

- [preparations](../api/preparations.md)
- [application call](../api/application-call.md)
- [more](../api/more.md)
- [more about models](../api/more-about-models.md)
- [frameworks](../api/frameworks.md)
- [security and compliance](../guides/security-and-compliance.md)
- [token plan guide](../guides/token-plan-guide.md)
- [managed agents api](../api/managed-agents-api.md)


