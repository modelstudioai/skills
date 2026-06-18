# API Key 鉴权与安全

API Key 是调用阿里云百炼平台模型和应用的核心鉴权凭证，用于标识调用者身份并控制资源访问权限。每个 API Key 归属于特定地域内的一个[业务空间](workspace.md)和一个用户，其调用范围由所属[业务空间](workspace.md)的权限配置决定。

## 获取与管理

在百炼控制台的 **API Key** 页面创建 API Key，需使用主账号或具备相应权限的子账号操作。关键规则：

- API Key 创建后永久有效，手动删除即失效，不可恢复。
- 华北2（北京）和新加坡地域已完成安全升级，新建 API Key 仅在创建时展示一次明文，关闭弹窗后无法再次查看。
- 每个主账号在华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域最多可创建 50 个 API Key；美国（弗吉尼亚）地域每个归属账号最多 20 个。
- 自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 均归属主账号。

## 权限与[业务空间](workspace.md)

API Key 的权限体系以业务空间为最小管理单元：

| 场景 | 权限范围 |
|------|---------|
| 默认业务空间 | 可调用所有标准模型，无法设置模型级限流 |
| 子业务空间 | 仅可调用已授权的模型，支持 QPM 和 Token 限流 |

- 同一业务空间内的 API Key 权限相同，无需为不同模型类型（文生文、文生图、语音合成等）分别创建。
- API Key 的可调用功能和模型限流与归属业务空间一致，不受用户控制台权限影响。
- 华北2（北京）地域的 API Key 支持设置 IP 访问白名单。

### API Key 状态与账号操作

| 操作 | 影响 |
|------|------|
| 删除 API Key | 永久失效，不可恢复 |
| 将账号移出业务空间 | 对应 RAM 账号的 API Key 失效，重新加入后恢复 |
| 在 RAM 控制台删除账号/角色 | 对应 API Key 永久失效，不可恢复 |

## 环境变量配置

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码导致泄漏风险：

- **Linux / macOS**：将 `export DASHSCOPE_API_KEY="YOUR_KEY"` 追加到 Shell 配置文件（`~/.bashrc` 或 `~/.zshrc`），然后 `source` 使其生效。
- **Windows**：通过系统属性或 `setx` 命令设置永久环境变量，需重启命令行窗口生效。

> **提示**：如果环境变量已设置但代码仍提示找不到 API Key，常见原因包括：仅设置了临时变量、未重启 IDE/应用、使用 `sudo` 时未加 `-E` 参数。

## 临时 API Key

在浏览器、移动 App 等不可信环境中，直接暴露永久 API Key 存在安全风险。百炼支持通过后端服务生成临时 API Key：

- 有效期可自定义（1 至 1800 秒，默认 60 秒），到期后自动失效，无法手动删除。
- 临时 API Key（以 `st-` 开头）继承生成它的永久 API Key 的全部权限。
- 各地域的 API Key 不通用，需使用对应地域的 Endpoint。

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 多地域支持

不同地域使用不同的 Base URL：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |

> **注意**：新加坡、日本（东京）、德国（法兰克福）地域的 Base URL 中需要将 `{WorkspaceId}` 替换为实际的业务空间 ID。

## 套餐场景下的 API Key

百炼的 Token Plan 团队版和 Coding Plan 使用专属 API Key 和 Base URL，与标准 API Key 独立：

- **Token Plan 团队版**：在管理后台创建成员并分配席位后，系统自动生成 API Key，Base URL 为 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。
- **Coding Plan**：面向个人开发者，Base URL 为 `https://coding.dashscope.aliyuncs.com/v1`。

## 安全最佳实践

1. **避免硬编码**：始终通过环境变量或密钥管理服务传递 API Key，不要将其写入代码或配置文件。
2. **最小权限原则**：为不同环境（开发、测试、生产）创建独立的子业务空间，各自使用独立的 API Key。
3. **前端场景用临时 Key**：浏览器和移动端不要使用永久 API Key，改用临时 API Key 并控制有效期。
4. **定期轮换**：定期删除旧 API Key 并创建新的，降低泄漏后的影响范围。
5. **IP 白名单**：在华北2（北京）地域为生产环境的 API Key 设置 IP 访问白名单。
6. **加密传输**：对包含敏感信息的请求启用加密调用（[DashScope SDK](dashscope-sdk.md) 的 `enable_encryption=True`），或通过 PrivateLink 实现私网访问。

## 关联主题页

- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)
- [token plan guide](../guides/token-plan-guide.md)
- [more](../api/more.md)


