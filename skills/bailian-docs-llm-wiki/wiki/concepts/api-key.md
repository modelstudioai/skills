# API Key 鉴权

API Key 是调用阿里云百炼模型与应用服务的核心鉴权凭证，所有 API 请求（OpenAI 兼容、Anthropic 兼容、DashScope 原生协议）均通过它验证调用者身份并确定权限范围。API Key 的调用权限由其归属的[业务空间](workspace.md)决定，并与地域、计费方案严格绑定。

## 类型与前缀

百炼平台存在三套相互隔离的 API Key 体系，必须与对应的 Base URL 配套使用，混用会导致 401/403 鉴权失败或意外扣费：

| 类型 | 前缀 | 配套 Base URL | 适用场景 |
| --- | --- | --- | --- |
| 按量付费 Key | `sk-ws`（新建）/ `sk-`（存量） | `dashscope.aliyuncs.com` 或 `{WorkspaceId}.{region}.maas.aliyuncs.com` | 常规模型与应用调用、后端服务 |
| Token Plan 专属 Key | `sk-sp-` | `token-plan.cn-beijing.maas.aliyuncs.com` | Claude Code、Cursor 等 AI 工具订阅式使用 |
| 临时 API Key | `st-` | 与生成它的永久 Key 相同 | 浏览器、移动端等不可信环境 |

## 获取与管理

- **创建入口**：百炼控制台右上角选择地域（华北2（北京）、新加坡、日本（东京）、德国（法兰克福）；美国（弗吉尼亚）走独立控制台），进入 API Key 页面创建。需主账号或具备 `管理员` / `API-Key` 页面权限的子账号。
- **仅展示一次**：新 Key 明文仅在创建时展示一次，关闭弹窗后无法再次查看，丢失需重置或重建。
- **地域隔离**：各地域的 API Key 相互独立，不能跨地域使用，请求时需搭配对应地域的 Endpoint。
- **控制台操作**：支持编辑、删除、禁用、重置（禁用/重置在美国（弗吉尼亚）地域不可用）。
- **编程管理**：可通过 OpenAPI（CreateApiKey / ListApiKeys / ResetApiKey 等）管理，这类管控接口使用阿里云 AccessKey 签名鉴权，而非 API Key 本身。

## 权限模型

- **归属[业务空间](workspace.md)**：Key 的调用权限完全由归属[业务空间](workspace.md)决定，同一空间内权限相同，无需按模型类型创建多个 Key。
- **子空间隔离**：子业务空间的 Key 只能调用已授权模型和该空间内的应用；在百炼上调优后的模型仅能用其所在空间的 Key 调用。
- **自定义权限**：创建时可选 `全部` 或 `自定义`——支持 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）与可访问模型范围限制（美国（弗吉尼亚）地域不支持自定义配置）。

## 典型使用场景

### 模型 / 应用 API 调用

推荐将 Key 配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露：

```bash
export DASHSCOPE_API_KEY='YOUR_KEY'   # Linux / macOS
setx DASHSCOPE_API_KEY "YOUR_KEY"     # Windows CMD
```

SDK 调用时从环境变量读取，并搭配正确的 `base_url`：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
```

HTTP 直调时通过请求头 `Authorization: Bearer $DASHSCOPE_API_KEY` 传递。向量化、排序、图像视频生成等所有模型 API 均使用同一鉴权方式。

### 不可信环境：临时 API Key

浏览器、移动 App 中不应暴露永久 Key，应由后端调用 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=<TTL>` 生成临时 Key：

- `expire_in_seconds` 范围 `[1, 1800]` 秒，默认 60 秒。
- 临时 Key 继承永久 Key 的全部权限（含模型/知识库访问限制），到期自动失效，无法手动删除。

### 百炼 CLI

`bl` CLI 支持多种认证方式：`bl auth login --console`（浏览器登录，推荐）、`bl auth login --api-key sk-xxx`、环境变量、`bl config set --key api_key`，或单次 `--api-key` 临时传入。可用 `bl auth status --output json` 验证。

## 安全最佳实践

- 使用环境变量或密钥管理服务注入，切勿将真实 Key 写入代码仓库、日志或公开渠道。
- 面向前端的场景一律使用临时 API Key。
- 按业务线划分子业务空间，用各自空间的 Key 实现权限隔离与分账。
- 需要更细粒度控制时启用自定义权限（IP 白名单 + 模型范围）。
- Key 疑似泄露时立即在控制台重置或禁用。

## 关联主题页

- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)
- [more about models](../api/more-about-models.md)
- [more](../api/more.md)
- [vector and sort](../api/vector-and-sort.md)
- [token plan guide](../guides/token-plan-guide.md)


