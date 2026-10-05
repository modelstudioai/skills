# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地调用大模型服务。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段 AES 加密 + RSA 公钥封装的混合加密机制，适用于敏感数据场景；[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 提供 SDK 自动化支持（Java/Python）。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内网直连百炼 API，流量全程不经过公网；同时支持为「安全存储业务空间」配置反向终端节点，对接客户私有网络中的 ElasticSearch、ADB、OSS 等资源；[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 是该模式的起点。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection` 启用输入/输出内容安全检测（如涉黄、涉政、广告等），由独立服务拦截高风险内容；[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 文档详细说明了开通、授权与调用方式。
- **模型备案信息**：所有上架模型均完成国家网信办算法备案及大模型备案，备案号实时公示于控制台与文档；[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 和 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 提供完整备案主体、编号及查询指引。

> **注意**：文档 6（`secure-storage.md`）标题为“私网访问配置”，但其子文档（如 `configure-an-endpoint-and-initiate-a-connection.md`）实际描述的是「安全存储业务空间」的反向终端节点方案，与文档 5 中面向通用 API 调用的 PrivateLink 方案属不同架构层级——前者用于客户私有资源被百炼反向访问，后者用于客户 VPC 主动访问百炼 API。二者不可混用，需根据业务角色（服务提供方 vs. 服务调用方）严格区分。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密时携带的 AES 密钥（经 RSA 公钥加密后） | `-----BEGIN RSA PRIVATE KEY-----...` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | DashScope SDK 启用自动加解密的开关 | `True` / `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id`, `public_key` | 通过 `/api/v1/public-keys/latest` 接口获取的 RSA 公钥元数据 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

- **启用传输加密**：  
  - SDK 方式（推荐）：安装 `dashscope>=1.14.0`（Python）或 `>=2.12.0`（Java），调用时设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动完成公钥获取、AES 密钥生成、加解密。  
  - HTTP 手动方式：先调用 `GET /api/v1/public-keys/latest` 获取公钥，再用该公钥加密 AES 密钥，并将加密后的密钥放入 `X-DashScope-EncryptionKey` 请求头，`input` 字段使用对应 AES 密钥加密。

- **配置私网访问**：  
  - **通用 API 私网调用**：在百炼控制台「管理 > 网络配置」添加 PrivateLink，关联业务空间后获取私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），替换 SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)的 `base_url`。  
  - **安全存储业务空间私网集成**：需依次完成「配置终端节点并发起连接」→「配置可用区IP」→「配置私有网络中的资源（OSS/ADB/ES）」→「配置MSE云原生网关」→「激活业务空间」；整个流程依赖华北2（北京）地域的专有网络与可用区约束。

- **启用 AI 安全护栏**：  
  1. 在 AI 安全护栏购买页开通服务并完成 RAM 授权；  
  2. 在百炼控制台「安全管理」页面完成服务关联角色授权；  
  3. 在模型调用请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`（注意：值为 JSON 字符串，非对象）。

- **获取合规材料**：  
  - 模型备案号：直接查阅 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)；  
  - 算法备案截图：使用备案编号（如 `网信算备330110507206401230035号`）在 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index) 查询并截图；  
  - 合作协议：联系商务经理申请《大模型服务/合作协议》，协议签署主体为阿里云百炼。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储业务空间的反向终端节点方案仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中的至少两个。
- **权限继承规则**：API Key 的模型调用权限、限流策略完全继承自其归属的**业务空间**，与创建该 Key 的用户（RAM 用户）的控制台页面权限无关；用户被移出业务空间后，其名下 API Key 将失效（重新加入可恢复）。
- **安全存储业务空间强依赖**：OSS Bucket 或 ES 实例若被释放，将导致该安全存储业务空间**永久不可用且无法恢复**，必须重建新空间；ADB/OSS 停服则导致知识库、审计日志等模块不可用。
- **加密与私网不互斥**：可在私网域名调用基础上叠加传输加密（即 `base_url` 替换为私网域名 + `enable_encryption=True`），双重保障数据安全。
- **合规责任主体**：阿里云百炼作为「服务技术支持者」提供已备案模型及基础设施，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的「服务提供者」，须独立承担内容审核、用户保护、算法评估等全部法定义务；[千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 明确强调此责任边界。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)


