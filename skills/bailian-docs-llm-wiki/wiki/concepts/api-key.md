# API Key 鉴权

API Key 是调用阿里云百炼平台模型服务和应用接口的唯一鉴权凭证，用于标识调用者身份并控制访问权限。开发者在调用任何百炼 API 之前，必须先在控制台创建 API Key 并妥善保管。

## API Key 的类型

百炼目前存在三类 API Key，它们的格式、Base URL 和计费方式互不相通：

| 类型 | 格式 | Base URL | 计费方式 |
| --- | --- | --- | --- |
| 按量计费 API Key | `sk-xxx` | `dashscope.aliyuncs.com` | 按 Token 用量计费 |
| Token Plan 团队版 | `sk-sp-xxx` | `token-plan.cn-beijing.maas.aliyuncs.com` | 预付费 Credits 抵扣 |
| Coding Plan | `sk-sp-xxx` | `coding.dashscope.aliyuncs.com` | 按模型调用次数 |

误用不同类型的 API Key 与 Base URL 会导致意外扣费或 401/403 报错。

## 创建与获取

在百炼控制台的 API Key 管理页面创建，操作权限要求：

- 使用主账号，或具备"管理员"或"API-Key"页面权限的子账号。
- 不同地域的控制台入口不同（华北2/新加坡/日本/德国使用 `bailian.console.aliyun.com`，美国使用 `modelstudio.console.aliyun.com`）。

创建时可选择归属[业务空间](workspace.md)并配置权限（全部模型或自定义 IP 白名单 + 模型范围）。升级后新创建的 API Key 以 `sk-ws` 开头，**仅在创建时展示一次明文**，关闭弹窗后无法再次查看，请立即复制保存。

自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号，并支持设置 IP 访问白名单。

## 权限模型

单个 API Key 只能归属一个地域内的一个[业务空间](workspace.md)和一个用户，且不能转移。其核心权限规则：

- API Key 的可调用模型和限流与**归属[业务空间](workspace.md)**的权限保持一致，不受用户控制台权限影响。
- 默认业务空间的 API Key 可调用所有标准模型；子业务空间的 API Key 仅可调用已授权的模型。
- 无需为不同模型类型（文生文、文生图、语音合成）分别创建 API Key。
- API Key 没有失效日期，手动删除后即失效。

### API Key 状态变化

| 触发操作 | 影响 |
| --- | --- |
| 主动删除 API Key | 失效，不可恢复 |
| 将 RAM 账号移出业务空间 | 该账号的 API Key 失效（重新加入后恢复） |
| 在 RAM 控制台删除账号/角色 | API Key 永久失效，不可恢复 |

## 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

- **Linux/macOS**：追加 `export DASHSCOPE_API_KEY="your-key"` 到 `~/.bashrc`（Linux）或 `~/.zshrc`（macOS），然后 `source` 使其生效。
- **Windows**：通过系统属性设置系统变量，或在 CMD 中用 `setx`、PowerShell 中用 `[Environment]::SetEnvironmentVariable` 设置。

设置后已打开的 IDE 或终端不会自动加载新变量，需重启相关程序。使用 `sudo` 运行脚本时默认不继承用户环境变量，需加 `-E` 参数。

## 临时 API Key

在浏览器、移动端等不可信环境中，直接暴露永久 API Key 存在安全风险。百炼支持通过后端服务生成有限时效的临时 API Key：

```
POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=<TTL>
```

- `expire_in_seconds`：有效期，范围 [1, 1800] 秒，默认 60 秒。
- 临时 API Key 继承生成它的永久 API Key 的全部权限，到期后自动失效，无法手动删除。
- 各地域的 API Key 不互通，请求时需使用对应地域的 Endpoint。

## 在框架中使用

百炼支持的主流框架均以 API Key 进行鉴权：

- **OpenAI 兼容 SDK**（Python/Java/Node.js/Go）：通过 `api_key` 参数或 `DASHSCOPE_API_KEY` 环境变量传入。
- **[DashScope SDK](dashscope-sdk.md)**（Python/Java）：同样通过环境变量或初始化参数传入。
- **LlamaIndex**：构建 RAG 应用时通过 API Key 访问百炼云端知识库。
- **Spring AI Alibaba**：集成百炼智能体/工作流应用时通过 `application.yml` 配置 API Key。

不同框架对环境变量名的约定可能不一致（如 `DASHSCOPE_API_KEY` 与 `AI_DASHSCOPE_API_KEY`），需确保配置文件中的占位符与实际变量名一致。

## 安全建议

- 不要在客户端代码中硬编码永久 API Key，前端场景使用临时 API Key。
- 按环境（dev/test/prod）划分业务空间，实现 API Key 权限隔离。
- 定期审计 API Key 使用情况，及时删除不再使用的 Key。
- 华北2（北京）地域可为 API Key 设置 IP 访问白名单，进一步收缩访问范围。

## 关联主题页

- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [security and compliance](../guides/security-and-compliance.md)
- [token plan guide](../guides/token-plan-guide.md)
- [get started with models](../guides/get-started-with-models.md)
- [application permission management](../guides/application-permission-management.md)
- [frameworks](../api/frameworks.md)
- [more](../api/more.md)


