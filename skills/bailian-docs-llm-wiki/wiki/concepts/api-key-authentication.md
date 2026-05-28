# API Key 管理与鉴权

API Key 管理与鉴权是阿里云百炼平台用于验证调用方身份、隔离资源访问边界及支撑计量计费的核心安全机制。通过为不同业务空间、计费方案与运行环境生成独立的密钥凭证，实现大模型服务的安全接入、权限管控与成本分账。

## 在不同场景中的使用方式

* **SDK 与后端代码集成**：推荐通过 [[environment-variables]] 注入 `DASHSCOPE_API_KEY`，配合对应地域的 `base_url` 初始化 OpenAI 或 DashScope 兼容 SDK。系统自动基于 Key 校验模型开关、限流阈值与计费归属，无需额外传递空间标识。
* **第三方工具与客户端接入**：在 IDE、CLI 或低代码平台中配置时，需严格匹配协议路径与套餐类型。Coding Plan 专属 Key（`sk-sp-` 前缀）、按量付费 Key（`sk-` 前缀）与 Token Plan 团队版凭证**互不通用**，混用或跨场景滥用将触发 `401` 鉴权失败或订阅封禁。
* **企业级多环境/多团队协作**：API Key 的生效范围完全绑定至 [[workspace]]。管理员通过为 [[ram-user]] 创建 Key 即可实现模型调用授权与配额隔离，控制台页面权限与 API 调用权限解耦，适合 `dev/test/prod` 环境分治。
* **不可信客户端与高敏场景**：面向浏览器、移动端或临时调试环境，建议通过服务端接口动态生成短效临时 Key 替代永久密钥，继承父级权限但生命周期极短，有效降低凭证泄露风险。

## 关键参数与配置

| 参数 / 配置项 | 说明 | 约束与默认值 |
|:---|:---|:---|
| `api_key` / `Authorization` | 核心身份鉴权凭证 | 请求 Header 需格式化为 `Bearer <key>`；主账号可见全量 Key，子账号仅可见自身记录 |
| `Workspace ID` | 权限隔离与资源路由的最小单元 | 决定 Key 可用的模型列表、[[rate-limit-policy]] 阈值及账单归属，不可跨空间复用 |
| `base_url` (地域端点) | API 请求路由地址 | Key 签发地域必须与端点地域严格匹配，否则直接拦截；常见端点：北京(`dashscope`)、新加坡(`dashscope-intl`)、弗吉尼亚(`dashscope-us`) |
| `expire_in_seconds` | 临时 Key 有效时长 | 默认 `60s`，可配 `[1, 1800]s`；生成后不可提前撤销或查看明文 |
| `IP 白名单` | 限制 Key 的调用源 IP | 目前仅**华北2（北京）**地域支持创建时配置；非白名单请求将被丢弃 |
| 协议路径标识 | 路由与鉴权校验后缀 | OpenAI 兼容协议用 `/compatible-mode/v1` 或 `/v1`；Anthropic 兼容协议固定为 `/apps/anthropic` |

## 安全规范与生产最佳实践

* **密钥生命周期管理**：平台不设置 Key 自动过期时间。若所属 RAM 用户被移出业务空间，其名下 Key 立即失效；删除用户则 Key 永久失效。建议结合 [[permission-management]] 建立定期轮换机制。
* **跨域与跨空间强隔离**：API Key 不支持跨地域或跨工作空间迁移。各地域静态数据持久化于接入端，Key 与端点必须同属一域，跨域调用将产生非预期费用或鉴权失败。
* **临时凭证使用边界**：临时 Key 仅支持极短期或单次调用，不可缓存或用于生产常驻服务。若检测到临时 Key 泄露，需立即在控制台吊销其对应的永久主 Key。
* **合规演进提示**：自 2026年3月25日起，**华北2（北京）**地域新创建的 API Key 将强制归属阿里云主账号，原有 RAM 子账号绑定逻辑将逐步废弃。企业用户需提前规划服务账号与密钥托管体系。
* **限流与配额规划**：生产环境建议按业务线预留 10% QPM 缓冲应对突发流量。不同模型 RPM/TPM 额度独立计算，可通过 [[billing]] 与监控面板实时核对用量，避免全局限流触发。

> 详细接入步骤、环境变量配置及密钥获取路径，请参阅 [[preparations]]。如需了解模型调用配额、账单规则或临时凭证生成逻辑，可访问 [[openai-compatible-api]] 与 [[generate-temporary-api-key]]。

## 关联主题页

- [[get-started-with-models|get started with models]] — `../guides/get-started-with-models.md`
- [[use-chat-client-or-development-tool|use chat client or development tool]] — `../guides/use-chat-client-or-development-tool.md`
- [[application-permission-management|application permission management]] — `../guides/application-permission-management.md`
- [[preparations|preparations]] — `../api/[[preparations|preparations]].md`
- [[more-about-models|[[more|more]] about models]] — `../api/[[more|more]]-about-models.md`
- [[general-text-embedding|general text embedding]] — `../api/general-text-embedding.md`

