# 安全与加密传输

安全与加密传输是百炼平台保障数据在客户端与服务端之间传输过程机密性、完整性与抗篡改能力的核心机制，通过 TLS 1.2+ 全链路加密、可选的端到端内容加密（AES-RSA 混合加密）及私网隔离等多层防护，确保敏感输入（如 PII、业务指令、凭证片段）不被中间人窃听或篡改。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用（通用文本/多模态接口）**：  
  所有 `/v1/chat/completions` 等模型 API 默认强制启用 HTTPS（TLS 1.2+），所有请求头、请求体、响应体均经传输层加密。对高敏数据（如身份证号、银行卡号、内部指令），开发者可主动启用**端到端内容加密**：先调用 `/api/v1/public-keys/latest` 获取 RSA 公钥，用其加密 AES 会话密钥，并将密钥通过 `X-DashScope-EncryptionKey` 请求头传递；原始 `input` 内容则使用该 AES 密钥加密后传入 `messages[].content`。服务端自动解密并执行推理，响应内容默认不加密（如需加密响应，需自行实现客户端侧加解密逻辑）。

- **Security API（安全治理数据面）**：  
  所有安全类接口（如 `/overview`、`/agent_logs`）同样运行于 HTTPS 协议之上，且强制要求 `Authorization: Bearer <API-Key>` 鉴权。API Key 本身即为传输敏感凭证，因此必须通过 TLS 保护——任何 HTTP 直连或明文日志打印均视为严重安全违规。平台不提供 Security API 的额外内容加密选项，因其返回数据（如告警摘要、策略状态）已属脱敏后的治理元数据，非原始业务载荷。

- **Agent 运行时治理（Agent Governance）**：  
  Agent 模式下的 `governance_config` 参数（含规则配置、工具白名单等）随请求体一同经 TLS 加密传输。治理引擎在服务端解密后解析策略，不涉及额外内容加密流程。但若 `messages[].content` 中包含需加密的敏感上下文（如用户上传的合同原文），仍需叠加使用前述 AES-RSA 加密流程，治理模块将在解密后对明文内容执行 PII 识别、越界拦截等策略。

- **私网访问（PrivateLink / 安全存储空间）**：  
  此为传输加密的增强形态：在 TLS 基础上，将流量从公网剥离，全程走阿里云内网（VPC → PrivateLink 终端节点 → 百炼网关）。适用于金融、政务等对“数据不出域”有强要求的场景。此时 TLS 仍生效，但网络层已无公网暴露面，显著降低中间人攻击与 DDoS 风险。注意：私网访问不替代内容加密，二者可叠加使用（例如：私网 + TLS + AES 加密 input）。

## 关键参数和配置

| 参数名 | 位置 | 类型 | 说明 | 是否必需 |
|--------|------|------|------|----------|
| `X-DashScope-EncryptionKey` | 请求头 | string | 经 RSA 公钥加密后的 AES 密钥（PEM 格式 Base64 字符串） | 启用端到端加密时必需 |
| `public_key_id` / `public_key` | 来自 `/api/v1/public-keys/latest` 响应 | string | 用于加密 AES 密钥的 RSA 公钥信息，每次调用可能轮换 | 加密前必需获取 |
| `Authorization: Bearer <API-Key>` | 请求头 | string | 所有 API 的基础鉴权凭证，必须通过 TLS 传输 | 全局必需 |
| `BASE_URL`（含 workspace_id + 地域） | 请求 URL | string | 如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1`，决定 TLS 终止点与路由路径 | 全局必需，且必须与 API Key 地域一致 |

> ⚠️ 注意：  
> - 不支持在客户端（浏览器/移动端）硬编码或透传 `X-DashScope-EncryptionKey` 或 API Key；密钥管理应交由后端服务完成。  
> - `X-DashScope-EncryptionKey` 仅作用于 `input` 内容（即 `messages[].content`），不影响 `tools`、`governance_config` 等结构化参数字段。  
> - 私网访问无需额外参数，只需将 `BASE_URL` 替换为 PrivateLink 终端节点地址（控制台可查），其余调用方式完全一致。

## 面向开发者，简洁实用

- ✅ **推荐组合（生产环境）**：  
  `HTTPS + API Key 鉴权 + （可选）AES-RSA 加密 input + （高合规场景）PrivateLink`  
  ——覆盖传输层、应用层、网络层三重防护。

- ✅ **快速验证加密是否生效**：  
  使用 `curl -v` 查看响应头 `x-request-id` 和 TLS 版本（`* ALPN, server accepted to use http/1.1` + `* SSL connection using TLSv1.3`）；若启用 `X-DashScope-EncryptionKey`，服务端解密失败会返回 `400 InvalidEncryptionKey` 错误码。

- ❌ **禁止行为**：  
  - 将 `X-DashScope-EncryptionKey` 或 API Key 写入前端代码、Git 仓库或日志；  
  - 使用 HTTP 协议调用任何百炼 API；  
  - 对 `X-DashScope-EncryptionKey` 做缓存超过 5 分钟（公钥可能轮换）；  
  - 在未校验 `public_key_id` 匹配的情况下复用旧公钥加密。

- 🛠️ **SDK 提示**：  
  DashScope Python SDK v2.0+ 支持 `enable_encryption=True` 自动处理密钥获取、AES 生成、RSA 加密与请求头注入，一行代码启用：  
  ```python
  from dashscope import Generation
  response = Generation.call(
      model='qwen-plus',
      messages=[{'role': 'user', 'content': '我的身份证号是110...'}],
      enable_encryption=True  # 自动完成公钥拉取与内容加密
  )
  ```

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [agent governance](../guides/agent-governance.md)
- [preparations](../api/preparations.md)


