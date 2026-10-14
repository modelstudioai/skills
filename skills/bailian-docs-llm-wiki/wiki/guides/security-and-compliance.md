# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限管控、内容安全、算法备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足监管要求（如《生成式人工智能服务管理暂行办法》）的前提下，安全、可控地调用大模型服务。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES 加密，并通过 RSA 公钥安全分发 AES 密钥，适用于敏感数据场景。该能力已集成至 DashScope SDK（Python/Java），开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持两种私网方案：
  - **PrivateLink 模型/API 接入**：适用于标准业务空间，通过终端节点将 VPC 流量直连百炼网关，全程内网不走公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - **安全存储业务空间**：专为高合规要求场景设计，需配置反向终端节点、MSE 网关、可用区 VIP 及私有云资源（OSS/ADB/ES），实现全链路私有网络隔离 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持在请求头中启用输入/输出内容安全检查（`X-DashScope-DataInspection`），自动拦截涉黄、涉政、广告等违规内容，与模型强绑定 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **算法与模型备案**：公示所接入大模型的国家网信办算法备案号及大模型备案号，覆盖千问、万相、DeepSeek、Moonshot 等主流模型，供上架合规使用 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 6 和文档 5 描述的私网机制存在定位差异——文档 5 面向通用业务空间的 PrivateLink 接入（单向出向连接），而文档 6 描述的是“安全存储业务空间”所需的反向终端节点（需 MSE 网关编排），二者适用场景、控制台入口和配置流程完全不同，不可混用。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `enable_encryption=True` (Python) / `enableEncrypt=true` (Java) | 启用混合加密（AES+RSA）的 SDK 开关 | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密时携带的 AES 密钥密文（Base64 编码） | `...` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id`, `public_key` | 通过 `/api/v1/public-keys/latest` 接口获取的 RSA 公钥元数据 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

1. **启用传输加密**  
   - SDK 方式（推荐）：安装 `dashscope>=1.14.0`（Python）或 `dashscope-java>=2.12.0`（Java），调用时设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动完成公钥获取、AES 密钥生成、加解密全流程。  
   - HTTP 手动方式：先调用 `GET /api/v1/public-keys/latest` 获取最新 `public_key` 和 `public_key_id`，再用该公钥加密 AES 密钥，最后将加密后的 `input` 和密钥密文通过 `X-DashScope-EncryptionKey` 头传入。

2. **配置私网访问**  
   - **标准业务空间**：在百炼控制台 **管理 > 网络配置 > VPC私网访问** 添加 PrivateLink，关联业务空间后，将 API 域名替换为 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`。  
   - **安全存储业务空间**：需依次完成：① 创建反向终端节点；② 创建 MSE 云原生网关并配置可用区 VIP；③ 将 VIP 加入终端节点安全组；④ 配置 OSS/ADB/ES 等私有云资源白名单与授权 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

3. **启用 AI 安全护栏**  
   在请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`（注意：值是 JSON 字符串，非对象）。若输入/输出被判定为违规，API 返回 `400` 及 `data_inspection_failed` 错误码。

4. **获取合规材料**  
   - 算法备案号：直接引用 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中对应模型的备案编号。  
   - 合作协议：联系商务经理申请含【算法名称】与【备案编号】的正式合作协议。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储业务空间当前仅支持华北2（北京） [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **权限继承规则**：API Key 的模型调用权限完全继承自其归属的**业务空间**，与用户（RAM 账号）的控制台页面权限无关；但 OpenAPI 接口（如知识库、Prompt 工程）需主账号在 RAM 控制台单独授权策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储业务空间依赖强耦合**：OSS Bucket 若被释放，将导致整个安全存储空间**不可恢复**；ADB/ES 若停止计费或释放，相关模块（知识库、审计日志等）将不可用 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **加密能力约束**：DashScope SDK 的自动加密仅支持 Python 和 Java；其他语言需自行实现 HTTP 手动加密流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **数据隐私承诺**：阿里云明确声明**绝不会将您的输入数据用于模型训练**，所有传输数据默认经 AES-256 加密 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)


