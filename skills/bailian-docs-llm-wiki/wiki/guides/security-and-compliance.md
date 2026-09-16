# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私等关键维度。所有能力均面向开发者可编程、可配置、可审计，满足金融、政务、医疗等强监管场景的落地要求。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段 AES 加密 + RSA 公钥封装的混合加密机制，适用于敏感数据公网传输场景；[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)  
- **私网访问**：支持两种私网路径：  
  - *应用/API 层*：通过 PrivateLink 创建接口终端节点，直连 `dashscope.aliyuncs.com`（北京/新加坡地域），流量全程内网；[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)  
  - *安全存储业务空间层*：需创建反向终端节点 + MSE 网关 + 配置 VIP + 接入 OSS/ADB/ES，实现完全隔离的数据存储环境；[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)  
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection` 启用输入/输出内容合规检测（如涉政、涉黄、广告等），默认按模型自动匹配策略；[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)  
- **模型备案**：所有预置模型（千问、万相、DeepSeek、Moonshot 等）均完成国家网信办算法备案及大模型备案，备案号实时公示；[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)  

> **注意**：文档 6 和文档 14 均指向“安全存储业务空间”的私网方案，但文档 6 明确限定适用范围为“已开通安全存储业务空间的用户”，而文档 14 仅作为目录页未说明前提条件。实际使用必须以文档 6 的前提条件为准——该能力为专属服务，非默认开通，需商务侧单独申请。

## 关键参数

| 参数名 | 位置 | 说明 | 示例值 |
|--------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | SDK 调用参数 | 启用传输加密开关 | `True` (Python), `true` (Java) |
| `X-DashScope-EncryptionKey` | HTTP 请求头 | 封装 RSA 加密后的 AES 密钥（SDK 自动注入，手动调用时需填入） | `"-----BEGIN RSA PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB\n-----END RSA PUBLIC KEY-----"` |
| `X-DashScope-DataInspection` | HTTP 请求头 | 启用 AI 安全护栏，JSON 字符串格式 | `'{"input":"cip","output":"cip"}'` |
| `public_key_id` | `/api/v1/public-keys/latest` 响应体 | 当前生效的 RSA 公钥 ID（用于密钥轮换追踪） | `"1"` |

## 使用方式

### 1. 传输加密（推荐 SDK 方式）
- 安装 DashScope SDK ≥1.14.0（Python）或 ≥2.12.0（Java）  
- 设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）  
- SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加解密 input/output，**无需手动管理密钥或公钥**；[获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)  

### 2. 私网访问（二选一）
- **通用 API 私网**：在 VPC 中创建接口终端节点（服务名 `com.aliyuncs.dashscope`），替换 SDK 或 OpenAI 兼容模式的 `base_url` 为终端节点域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/compatible-mode/v1`）  
- **安全存储业务空间私网**：仅限已开通该服务的客户，需按顺序完成：创建反向终端节点 → 配置 MSE 网关 VIP → 授权 OSS/ADB/ES → 激活空间；完整流程见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)  

### 3. AI 安全护栏
- 开通服务并授权后，在请求头添加 `X-DashScope-DataInspection`  
- 值为 JSON 字符串（非对象），`"input":"cip"` 表示检查输入，`"output":"cip"` 表示检查输出；违规时返回 `400` 及 `data_inspection_failed` 错误码  

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问**不支持美国（弗吉尼亚）地域**；安全存储业务空间仅支持**华北2（北京）** 地域；[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)  
- **API Key 权限继承**：API Key 的模型调用权限、限流策略完全继承自其归属的**业务空间**，与用户（RAM 账号）的控制台页面权限无关；[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)  
- **加密限制**：DashScope SDK 的自动加密仅支持 Java/Python；HTTP 手动调用需自行实现 AES/RSA 加解密逻辑；[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)  
- **安全存储依赖强耦合**：OSS/ADB/ES 任一组件停止服务或被释放，将导致整个安全存储业务空间不可用且**无法恢复**，必须重建；[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)  
- **备案责任主体**：阿里云提供模型备案号及合作协议模板，但应用/小程序上架的最终合规责任主体是**开发者自身**，需独立完成安全评估、算法备案及内容审核义务；[千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)


