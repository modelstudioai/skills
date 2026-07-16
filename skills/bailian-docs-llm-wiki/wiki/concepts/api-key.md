# API Key 鉴权

API Key 是调用阿里云百炼平台模型与应用的核心鉴权凭证，以 `Authorization: Bearer <API-Key>` 的形式随请求携带，用于标识调用者身份并界定其可访问的模型、应用与业务空间范围。

## 在百炼平台的使用场景

API Key 贯穿百炼的各类调用入口，不同场景下的获取与使用方式略有差异：

- **模型 API 直连**：调用文本、图像、视频、语音、向量等模型前，先在控制台对应地域的 **API Key** 页面创建 Key，配合服务端点 `base_url` 发起请求。
- **应用与知识库调用**：智能体应用、工作流应用、知识检索/问答接口（DashScope 应用网关）均通过 API Key Bearer 鉴权，Base URL 常需拼接业务空间 ID，如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`。
- **框架集成**：LlamaIndex（RAG）、Spring AI Alibaba（智能体/工作流/知识库检索）均以 API Key 鉴权复用百炼能力，通常通过环境变量注入。
- **百炼 CLI（`bl`）**：支持控制台登录、`--api-key`、环境变量、配置文件、临时传入等多种认证方式，可组合使用。
- **不可信环境（浏览器/移动端）**：应由后端生成临时 API Key，避免永久 Key 泄露。
- **子业务空间**：需使用该空间自身的 API Key，并预先为其授予相应模型的调用权限。

## Key 的类型与前缀

百炼的 API Key 因计费方式不同而彼此隔离，前缀是重要区分标识：

| 类型 | 前缀 | 说明 |
| --- | --- | --- |
| 按量付费（安全升级后） | `sk-ws` | 仅创建时展示一次明文，关闭弹窗后无法再查看，务必立即保存 |
| 按量付费（升级前旧 Key） | `sk-` | 仍可正常使用 |
| Token Plan / Coding Plan 专属 | `sk-sp-` | 套餐专属，与通用 Key 不可混用 |
| 临时 API Key | `st-` | 由后端接口生成、限时有效 |

> API Key 与其配套的 Base URL 必须成对使用。按量付费、Token Plan、Coding Plan 三者的 Key 与 Base URL 混用会导致意外扣费或返回 401/403 鉴权失败。

## 创建时的关键选项

- **归属业务空间**：决定 Key 的调用权限。默认空间的 Key 可调用所有标准模型及默认空间应用；子空间的 Key 仅能调用已授权模型及本空间应用。同一空间内的 Key 权限相同，无需按模态分别创建。
- **权限**：可选「全部」或「自定义」。自定义可配置 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）及可访问的模型/应用范围。
- **创建主体**：需主账号，或具备「管理员」/「API-Key」页面权限的子账号。RAM 子账号在订阅套餐前需主账号授予 `AliyunBailianFullAccess` 等权限。

## 配置与使用

推荐将 API Key 写入环境变量，避免硬编码泄漏：

- 通用约定使用 `DASHSCOPE_API_KEY`。
- Spring AI Alibaba 应用集成用 `DASHSCOPE_API_KEY`，知识库检索用 `AI_DASHSCOPE_API_KEY`（约定不一致，关键是 `application.yml` 中占位符与实际变量名匹配）。

调用时除 API Key 外，还需指定与地域、协议匹配的 `base_url`（OpenAI 兼容协议与 Anthropic 兼容协议不同）。

## 临时 API Key

面向浏览器、移动端等不可信环境，通过后端接口用永久 Key 换取限时凭证：

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

关键参数与特性：

- `expire_in_seconds`：有效期（TTL），单位秒，范围 `[1, 1800]`，默认 60 秒。
- 返回体中 `token`（`st-` 前缀）为临时 Key，`expires_at` 为过期 UNIX 时间戳。
- 临时 Key 继承永久 Key 的全部权限（含模型/知识库访问限制），到期自动失效，无法提前删除。
- 各地域（北京 / 新加坡 / 弗吉尼亚）的 Key 与 Endpoint 不互通，需配套使用。

## 编程化管理

除控制台外，百炼提供 OpenAPI（`CreateApiKey` / `GetApiKey` / `ListApiKeys` / `UpdateApiKey` / `DeleteApiKey` / `EnableApiKey` / `DisableApiKey` / `ResetApiKey`）以编程方式管理 Key。这些接口使用阿里云账号 AccessKey 签名认证，并需具备相应 RAM 权限，与业务调用所用的 API Key Bearer 鉴权不同。

## 开发者要点

- 优先用环境变量注入，切勿硬编码或提交到代码仓库。
- 升级后的 `sk-ws` Key 只显示一次，创建后立即保存。
- 明确当前场景使用的是按量付费、Token Plan、Coding Plan 中的哪种 Key，并搭配对应 Base URL。
- 不可信环境一律走临时 API Key，生产环境的文件存储不要依赖临时 URL。

## 关联主题页

- [preparations](../api/preparations.md)
- [more](../api/more.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)
- [token plan guide](../guides/token-plan-guide.md)
- [knowledge](../api/knowledge.md)


