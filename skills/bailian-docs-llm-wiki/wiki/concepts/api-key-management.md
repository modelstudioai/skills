# API Key 管理与安全

API Key 是调用阿里云百炼平台模型和应用的鉴权凭证，贯穿开发、测试到生产环境的全生命周期。合理管理 API Key 的创建、分发、权限控制和安全防护，是保障业务稳定运行的基础。

## 核心概念

API Key 在百炼平台中具有以下关键属性：

- **归属关系**：每个 API Key 归属于特定地域内的一个[业务空间](workspace.md)和一个用户，不可转移。
- **权限继承**：API Key 的可调用功能和模型限流与其归属[业务空间](workspace.md)的权限一致，不受用户控制台权限影响。
- **统一凭证**：无需为不同模型类型（文生文、文生图、语音合成等）分别创建 API Key。

## 创建与获取

在百炼控制台的 **API Key** 页面创建，需使用主账号或具备相应权限的子账号操作。各地域的 API Key 数量上限：

| 地域 | 上限 |
|------|------|
| 华北2（北京）、新加坡、日本（东京）、德国（法兰克福） | 每个主账号 50 个 |
| 美国（弗吉尼亚） | 每个归属账号 20 个 |

创建后永久有效，手动删除即失效。华北2（北京）和新加坡地域已完成安全升级，新建 API Key 仅在创建时展示一次明文，关闭弹窗后无法再次查看，请务必妥善保存。

## 环境变量配置

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码导致泄漏风险：

- **Linux / macOS**：将 `export DASHSCOPE_API_KEY="YOUR_KEY"` 追加到 Shell 配置文件（`.bashrc` 或 `.zshrc`），然后 `source` 使其生效。
- **Windows**：通过系统属性、`setx` 命令或 PowerShell 的 `[Environment]::SetEnvironmentVariable` 设置永久变量。

## 权限控制场景

### 默认[业务空间](workspace.md)

默认业务空间的 API Key 可调用所有标准模型，权限较大，适合快速开发和原型验证。

### 子业务空间隔离

通过创建子业务空间实现精细化管控：

- **权限管控**：限制 RAM 用户只能通过指定子空间的 API Key 调用已授权的模型。
- **费用分账**：每个子空间独立生成账单，便于多业务场景的费用拆分。
- 调用标准模型前需由超级管理员为该空间设置模型调用权限。

### Token Plan / Coding Plan 专属 Key

Token Plan 团队版和 Coding Plan 使用各自专属的 API Key 和 Base URL，与百炼按量计费的 API Key 互不相通，请勿混用。

| 计费方式 | API Key 格式 | Base URL 前缀 |
|----------|-------------|--------------|
| 按量计费 | 标准格式 | `dashscope.aliyuncs.com` |
| Token Plan 团队版 | 标准格式 | `token-plan.cn-beijing.maas.aliyuncs.com` |
| Coding Plan | `sk-sp-xxx` | `coding.dashscope.aliyuncs.com` |

## 临时 API Key

在浏览器、移动 App 等不可信环境中，直接暴露永久 API Key 存在安全风险。可通过后端服务生成临时 API Key：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

- 有效期可自定义（1~1800 秒，默认 60 秒），到期后自动失效。
- 临时 API Key 继承生成它的永久 API Key 的全部权限。
- 以 `st-` 开头，无法手动删除。

## 安全最佳实践

1. **避免硬编码**：始终通过环境变量或密钥管理服务注入 API Key，不要写入代码或配置文件。
2. **最小权限**：生产环境使用子业务空间的 API Key，仅授权必要的模型和功能。
3. **前端防泄漏**：面向用户的客户端一律使用临时 API Key，有效期尽量缩短。
4. **IP 白名单**：华北2（北京）地域的 API Key 支持设置 IP 访问白名单，限制调用来源。
5. **定期轮换**：定期删除旧 Key 并创建新 Key，降低泄漏后的影响面。
6. **空间规划**：按环境（dev/test/prod）或业务线划分业务空间，结合限流策略分配配额。

## 常见问题

- **API Key 权限不足**：检查 API Key 归属的业务空间是否已授权对应模型。子业务空间需超级管理员手动开通模型权限。
- **401/403 错误**：确认 API Key 与 Base URL 匹配（按量计费、Token Plan、Coding Plan 三者不通用）。
- **环境变量不生效**：确认已 `source` 配置文件或重启 IDE；使用 `sudo` 时需加 `-E` 参数保留环境变量。
- **API Key 失效**：可能因手动删除、RAM 账号被删除、或账号被移出业务空间导致。

## 关联主题页

- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [more](../api/more.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)
- [token plan guide](../guides/token-plan-guide.md)


