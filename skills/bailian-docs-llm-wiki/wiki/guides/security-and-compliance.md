# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限管控、内容安全、模型备案及数据隐私保护等关键维度。所有能力均面向开发者提供可编程接口和控制台配置，支持企业级安全治理要求。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，并通过 RSA 公钥安全分发 AES 密钥，适用于敏感数据场景。该能力已集成至 DashScope SDK（Java/Python），调用时启用 `enable_encryption=True` 即可自动完成加解密流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持两种私网方案：
  - **PrivateLink 终端节点**：适用于标准业务空间，通过 VPC 内网直连百炼 API，流量全程不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - **安全存储业务空间**：专为高合规要求场景设计，需配置反向终端节点 + MSE 网关 + 专属 OSS/ADB/ES 资源，实现数据不出客户 VPC 的全链路隔离 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection` 启用输入/输出内容检测，拦截涉政、涉黄、广告等高风险内容，适用于所有文本与图片类模型 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：提供所接入大模型的算法备案号与大模型备案号（如千问：`网信算备330110507206401230035号`；DeepSeek：`网信算备110108970550101240011号`），满足《生成式人工智能服务管理暂行办法》上架合规要求 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 6（`secure-storage.md`）标题为“私网访问配置”，但其子文档（如 `configure-an-endpoint-and-initiate-a-connection.md`）实际描述的是**安全存储业务空间**的专用私网架构，与文档 5 中面向通用业务空间的 PrivateLink 方案属不同产品形态，不可混用。开发者应根据业务安全等级选择：标准隔离选 PrivateLink；金融/政务等强监管场景必须选用安全存储业务空间。

## 关键参数

| 参数名 | 说明 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-EncryptionKey` | HTTP 请求头，携带 RSA 加密后的 AES 密钥（Base64 编码） | `"AQAB..."` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | HTTP 请求头，启用内容安全检测，值为 JSON 字符串 | `'{"input":"cip","output":"cip"}'` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `enable_encryption` / `enableEncrypt` | SDK 参数，启用自动加解密 | `True` (Python), `true` (Java) | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` & `public_key` | 从 `/api/v1/public-keys/latest` 接口获取，用于手动加密流程 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

1. **传输加密（推荐 SDK 自动模式）**  
   - Python：`Generation.call(..., enable_encryption=True)`；Java：`.enableEncrypt(true)`  
   - SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加密 `input` 并注入请求头，响应自动解密返回明文。

2. **私网访问（二选一）**  
   - **PrivateLink（通用业务空间）**：在控制台「管理 > 网络配置」添加私网连接 → 关联业务空间 → 替换 API 域名为 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com` [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。  
   - **安全存储业务空间（高合规场景）**：需依次完成「配置终端节点」→「配置可用区IP」→「配置OSS/ADB/ES资源」→「配置MSE网关」→「激活空间」全流程 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

3. **AI 安全护栏**  
   - 开通服务并授权后，在请求头添加 `X-DashScope-DataInspection: '{"input":"cip","output":"cip"}'`；若任一字段检测失败，API 返回 `400 DataInspectionFailed` 错误。

4. **合规备案材料准备**  
   - 直接引用文档 10 和文档 11 中公示的备案号（如 `网信算备330110507206401230035号`），登录 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index) 搜索截图即可；合作协议需联系商务经理获取 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储业务空间当前仅支持华北2（北京）[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **API Key 归属**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key 默认归属主账号，不可转移至 RAM 用户 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用应用、知识库、Prompt 工程等 OpenAPI，必须由阿里云主账号在 RAM 控制台为其授予 `AliyunBailianDataFullAccess` 等策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储业务空间依赖强耦合**：OSS Bucket 或 ADB/ES 实例被释放后，该业务空间将**永久不可恢复**，必须重建 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **加密与私网不互斥**：可在私网域名上调用加密接口（即同时启用 `enable_encryption=True` 并使用私网 base_url），二者叠加可实现「传输加密 + 网络隔离」双重防护。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)


