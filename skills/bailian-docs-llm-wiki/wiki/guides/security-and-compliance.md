# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足监管要求（如《生成式人工智能服务管理暂行办法》）的前提下，安全、可控地构建和部署AI应用。

## 支持的模型/功能

- **传输加密**：支持对请求体 `input` 字段（含 `messages` 等核心内容）进行 AES-RSA 混合加密，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`, `qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了加解密流程与 SDK 集成方式。
- **私网访问**：支持通过阿里云 PrivateLink（终端节点）建立 VPC 到百炼服务的内网直连，流量全程不经过公网。该能力适用于华北2（北京）、中国香港地域的模型与应用 API 调用，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 提供了完整的配置与调用指南。
- **AI 安全护栏**：支持在请求头中启用输入/输出双路内容安全检测（`X-DashScope-DataInspection`），识别涉黄、涉政、广告等高风险内容。该能力目前覆盖文本和图片类模型，[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 文档包含开通、授权与请求示例。
- **安全存储业务空间**：提供独立的“安全存储空间”类型业务空间，支持通过反向终端节点、MSE 云原生网关等组件，将知识库、审计日志等数据完全隔离存储于客户私有网络内的 OSS、ADB、ES 等资源中，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `enable_encryption` (Python SDK) / `enableEncrypt` (Java SDK) | Boolean | 启用传输加密的开关，SDK 自动完成公钥获取、AES 密钥生成与加解密 | `True` |
| `X-DashScope-EncryptionKey` | Header String | 仅 HTTP 手动调用时使用，封装经 RSA 公钥加密后的 AES 密钥 | `"-----BEGIN RSA PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB\n-----END RSA PUBLIC KEY-----"` |
| `X-DashScope-DataInspection` | Header String | 启用 AI 安全护栏的开关，值为 JSON 字符串，指定 input/output 检测策略 | `'{"input":"cip","output":"cip"}'` |
| `public_key_id` | Response Field | 从 `/api/v1/public-keys/latest` 接口返回，用于标识当前使用的 RSA 公钥版本 | `"1"` |

> **注意**：文档 5 的文件名 `secure-storage.md` 与实际内容（私网访问配置索引）严重不符，且其子文档（如文档 6、8、9、14）均属于“安全存储业务空间”的完整私网架构方案，而非泛指“安全存储”。该命名易引发歧义，应以子文档路径为准。

## 使用方式

1. **传输加密（推荐 SDK 方式）**：
   - 安装最新版 DashScope SDK（Java ≥ 2.12.0，Python ≥ 1.14.0）。
   - 在 `Generation.call()` 或 `GenerationParam.builder()` 中设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）。
   - SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加密 `input` 并注入 `X-DashScope-EncryptionKey` 头，响应自动解密。

2. **私网访问（PrivateLink）**：
   - 在百炼控制台 **管理 > 网络配置** 开通私网连接，关联目标 VPC 与可用区交换机。
   - 在 **业务空间管理** 中编辑目标业务空间，在高级配置中绑定该私网连接。
   - 将 API 请求的 `base_url` 替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。

3. **AI 安全护栏**：
   - 访问 **[安全管理](https://bailian.console.aliyun.com/settings/security?globalset=1)** 页面，完成服务开通与角色授权。
   - 在模型调用请求头中添加 `X-DashScope-DataInspection: '{"input":"cip","output":"cip"}'`。

4. **安全存储业务空间**：
   - 创建业务空间时选择 **空间类型 = 安全存储空间**。
   - 依次完成：[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) → [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md) → [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) → [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md) → 最终激活。

## 限制和注意事项

- **地域限制**：私网访问（PrivateLink）仅支持华北2（北京）、中国香港地域；安全存储业务空间的专有网络必须为“华北2（北京）”，且可用区需为 G/H/L 中的至少两个。
- **API Key 归属**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key 均归属主账号，不可转移至 RAM 用户。RAM 用户的 API Key 在被移出业务空间后会失效（重新加入可恢复），但在 RAM 控制台删除该用户后则永久失效。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用应用、知识库、[Prompt 工程](../concepts/prompt.md)等 OpenAPI，必须由阿里云主账号在 RAM 控制台为其单独授予 `AliyunBailianDataFullAccess` 等系统策略。
- **模型备案责任**：百炼公示的算法备案号（如 `网信算备330110507206401230035号`）由模型提供方（如达摩院）持有，开发者作为服务提供者，仍需根据《生成式人工智能服务管理暂行办法》独立履行内容审核、用户保护、算法备案（如适用）等法定义务，[千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 文档明确强调了此主体责任。
- **数据隐私承诺**：阿里云百炼承诺绝不将客户数据用于模型训练，并对传输数据采用 AES-256 加密，[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md) 文档确认其已通过 SOC 2 审计。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


