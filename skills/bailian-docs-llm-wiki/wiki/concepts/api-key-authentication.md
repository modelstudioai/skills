# API Key 鉴权

API Key 是阿里云百炼平台的身份鉴权凭证，用于在调用大模型 API 和应用 API 时验证调用者身份并控制访问权限。所有通过 SDK 或 HTTP 接口发起的请求都必须携带有效的 API Key。

## 获取与创建

API Key 在百炼控制台的**密钥管理**页面创建，需使用主账号或具备相应权限的 RAM 子账号操作。创建后永久有效，手动删除后即失效。

> **注意**：华北2（北京）和新加坡地域已进行安全升级，新建的 API Key 仅在创建时展示一次明文，关闭弹窗后无法再查看，请务必立即保存。

## 使用方式

API Key 通过 HTTP 请求头 `Authorization: Bearer <API_KEY>` 传递。推荐将 API Key 配置到环境变量 `DASHSCOPE_API_KEY` 中，避免在代码里硬编码导致泄露。

**各平台环境变量配置：**

- **Linux/macOS**：`export DASHSCOPE_API_KEY="your-key"` 追加到 `~/.bashrc` 或 `~/.zshrc`
- **Windows CMD**：`setx DASHSCOPE_API_KEY "your-key"`
- **Windows PowerShell**：`[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-key", [EnvironmentVariableTarget]::User)`

配置后需重启 IDE 或终端使环境变量生效。使用 `sudo` 运行脚本时需加 `-E` 参数以继承环境变量。

## 权限与业务空间

API Key 的权限由其归属的**业务空间**决定：

- 单个 API Key 归属一个地域内的一个业务空间和一个用户，不可跨空间或跨用户转移。
- **默认业务空间**的 API Key 可调用所有标准模型及该空间内的应用。
- **子业务空间**的 API Key 仅可调用已授权的模型和该空间内的应用，适用于权限管控和费用分账场景。
- API Key 的可调用模型和限流配额与业务空间保持一致，不受用户控制台权限的影响。
- 无需为不同类型的模型（文生文、文生图、语音合成等）创建不同的 API Key。

### IP 访问白名单

华北2（北京）地域支持为 API Key 设置 IP 访问白名单，实现更精细的网络层访问控制。

### API Key 失效场景

| 触发操作 | 主账号的 API Key | RAM 账号的 API Key |
|---------|----------------|-------------------|
| 主动删除 API Key | 失效，不可恢复 | 失效，不可恢复 |
| 将账号移出业务空间 | -- | 失效（重新加入后恢复） |
| 在 RAM 控制台删除账号/角色 | -- | 失效，不可恢复 |

> **注意**：自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号。

## 临时 API Key

在浏览器、移动 App 等不可信环境中直接使用永久 API Key 存在泄露风险。百炼支持通过后端服务生成**临时 API Key**：

- **生成方式**：向 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 发送请求，Header 中携带永久 API Key
- **有效期**：默认 60 秒，可通过 `expire_in_seconds` 参数设置，范围 [1, 1800] 秒
- **权限继承**：临时 API Key 继承生成它的永久 API Key 的全部权限
- **自动失效**：到期后自动失效，无法手动删除

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 不同地域的 Base URL

使用 API Key 调用时需匹配正确地域的 Base URL：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |

各地域的 API Key 相互独立，不可跨地域使用。

## 在模型调用中使用

通过 [DashScope SDK](dashscope-sdk.md) 或 OpenAI 兼容 SDK 调用模型时，均需传入 API Key：

```python
import os
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你的问题')
```

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
```

## 管理权限

API Key 的管理涉及以下角色权限：

| 操作 | 超级管理员 | 业务空间管理员 | 普通用户 |
|------|-----------|-------------|---------|
| 创建/删除 API Key | 支持 | 支持 | 不支持 |
| 设置 IP 白名单 | 支持（北京地域） | 支持（北京地域） | 不支持 |

## 常见鉴权错误

| 错误码 | 说明 | 排查方向 |
|--------|------|---------|
| `401 Unauthorized` / `InvalidApiKey` | API Key 无效或已被删除 | 确认 API Key 是否正确、是否已过期或被删除 |
| `403 Forbidden` / `AccessDenied` | API Key 无权访问目标资源 | 确认 API Key 所属业务空间是否已授权该模型或应用 |
| `data_inspection_failed` | 内容安全检测未通过 | 检查输入输出是否触发了 AI 安全护栏规则 |

## 安全最佳实践

1. **不要硬编码**：始终通过环境变量或密钥管理服务传递 API Key，避免写入代码仓库。
2. **最小权限**：使用子业务空间的 API Key 限制可调用的模型范围，而非使用默认空间的全权限 Key。
3. **前端场景用临时 Key**：浏览器或移动端使用临时 API Key，有效期尽量设短。
4. **定期轮换**：定期删除旧 Key 并创建新 Key，降低泄露风险。
5. **启用 IP 白名单**：华北2（北京）地域建议配置 IP 访问白名单，限制 API Key 的来源 IP。

## 关联主题页

- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


