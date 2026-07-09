# API Key 鉴权

API Key 是调用阿里云百炼平台模型服务和应用 API 的唯一鉴权凭证，通过 HTTP 请求头 `Authorization: Bearer <API-Key>` 传递，平台据此识别调用者身份并执行权限控制。

## 在百炼平台的使用场景

### 模型调用

所有模型 API（文本生成、图像生成、语音合成等）统一使用 API Key 鉴权。同一[业务空间](workspace.md)内的 API Key 权限相同，无需为不同模型类型分别创建。调用时将 API Key 配置为环境变量 `DASHSCOPE_API_KEY`，SDK 会自动读取。

### 应用调用

通过 Responses API 或 DashScope API 调用智能体和工作流应用时，同样需要 API Key 鉴权。子[业务空间](workspace.md)下的应用调用还需额外提供 Workspace ID。

### 知识检索与问答

知识检索和知识问答接口使用[业务空间](workspace.md) ID 拼接的专属 Base URL，配合 API Key Bearer 鉴权。

### [Token](token.md) Plan / Coding Plan

订阅型套餐使用专属 API Key（以 `sk-sp-` 开头）和专属 Base URL，与按量计费的普通 API Key 互不相通。

## 关键参数与配置

### API Key 类型

| 类型 | 前缀 | Base URL | 适用场景 |
|------|------|----------|----------|
| 普通 API Key | `sk-ws` | `dashscope.aliyuncs.com` | 按量计费模型调用 |
| [Token](token.md) Plan 专属 | `sk-sp-` | `token-plan.cn-beijing.maas.aliyuncs.com` | [Token](token.md) Plan 团队版 |
| Coding Plan 专属 | `sk-sp-` | `coding.dashscope.aliyuncs.com` | Coding Plan 个人开发 |
| 临时 API Key | `st-` | 同永久 Key | 浏览器/移动端等不可信环境 |

### 创建与权限

- 在百炼控制台 API Key 管理页面创建，需主账号或具备相应权限的子账号操作。
- 每个主账号每个地域最多 50 个 API Key（美国地域为 20 个）。
- API Key 归属于特定业务空间，调用权限由该空间的模型授权决定。
- 支持配置 IP 访问白名单和模型范围限制。
- 创建后仅展示一次明文，关闭弹窗后无法再次查看。

### 临时 API Key

在不可信环境中，通过后端服务生成临时 API Key 避免永久凭证泄露：

```
POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800
```

- `expire_in_seconds`：有效期范围 [1, 1800] 秒，默认 60 秒。
- 临时 Key 继承永久 Key 的全部权限，到期自动失效，无法手动删除。
- 各地域的 API Key 不互通，需使用对应地域的 Endpoint。

### 环境变量配置

推荐将 API Key 配置到环境变量，避免硬编码泄露：

```bash
# Linux/macOS
export DASHSCOPE_API_KEY="sk-xxx"

# 写入 shell 配置文件永久生效
echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.bashrc
```

## 安全注意事项

- 不要在客户端代码中硬编码 API Key，使用环境变量或密钥管理服务。
- 浏览器/移动端场景务必使用临时 API Key。
- 将 RAM 账号移出业务空间会使其 API Key 失效（重新加入后恢复）；在 RAM 控制台删除账号则 API Key 永久失效。
- 三类 API Key 与 Base URL 互不相通，误用会导致按量扣费或鉴权失败（401/403）。

## 关联主题页

- [preparations](../api/preparations.md)
- [application call](../api/application-call.md)
- [more](../api/more.md)
- [more about models](../api/more-about-models.md)
- [token plan guide](../guides/token-plan-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [knowledge](../api/knowledge.md)


