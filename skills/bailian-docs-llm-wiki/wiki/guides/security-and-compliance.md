# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、数据隐私及监管备案等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等法规要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，并通过 RSA 公钥安全分发 AES 密钥，适用于敏感数据场景。该能力已集成至 DashScope SDK（Java/Python），调用时仅需设置 `enable_encryption=True` 即可启用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持通过 PrivateLink 在 VPC 内直连百炼 API，流量全程不经过公网。当前仅华北2（北京）、中国香港地域支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **AI 安全护栏**：支持输入/输出双路内容安全检测（CIP），可识别涉黄、涉政、广告等高风险内容。需在请求头中显式设置 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储业务空间**：专为高合规要求客户设计，支持将知识库、审计日志等数据完全托管于客户私有网络内，依赖 MSE 网关、OSS/ADB/ES 等资源隔离部署 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已取得国家网信办算法备案号及大模型备案号，详情见公示列表 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 11 中提及“上架及合规备案前，请开发者仔细阅读《生成式人工智能服务管理暂行办法》原文”，而文档 10 的免责声明明确指出“第三方模型的备案信息由提供方负责，阿里云百炼不作额外承诺”。二者逻辑一致——百炼提供备案号查询入口与主体信息，但最终备案责任主体为应用开发者自身，且第三方模型（如 DeepSeek、MiniMax）的备案状态需以 [互联网信息服务算法备案系统](https://beian.cac.gov.cn) 实时结果为准。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `X-DashScope-EncryptionKey` | Header | 用于传输加密后的 AES 密钥（Base64 编码） | `"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."` |
| `X-DashScope-DataInspection` | Header | 启用 AI 安全护栏，JSON 字符串格式 | `'{"input":"cip","output":"cip"}'` |
| `Authorization` | Header | API Key 认证凭证，必须为 `Bearer <api_key>` 格式 | `"Bearer sk-xxx"` |
| `public_key_id` | Response field | 从 `/api/v1/public-keys/latest` 接口返回，标识当前有效公钥版本 | `"1"` |

## 使用方式

1. **启用传输加密**  
   - HTTP 调用：先调用 `GET /api/v1/public-keys/latest` 获取公钥，再手动完成 AES 加密 + RSA 加密密钥流程；  
   - SDK 调用（推荐）：Python 中设置 `enable_encryption=True`，Java 中设置 `.enableEncrypt(true)`，SDK 自动处理全流程 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

2. **配置私网访问**  
   - 在百炼控制台 **管理 > 网络配置 > VPC私网访问** 添加私网连接；  
   - 在 **业务空间管理** 中将目标业务空间与私网连接关联；  
   - 替换 API 请求域名：将 `{WorkspaceId}.{RegionId}.maas.aliyuncs.com` 替换为 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`。

3. **启用 AI 安全护栏**  
   - 首先在 **安全管理 > 全局设置** 页面完成服务开通与授权；  
   - 所有模型调用请求必须携带 `X-DashScope-DataInspection` Header，否则不触发检测。

4. **使用安全存储业务空间**  
   - 仅限商务开通的专属空间类型；  
   - 必须按顺序完成：创建反向终端节点 → 配置可用区 VIP → 配置 OSS/ADB/ES → 配置 MSE 网关 → 激活空间；  
   - 全程依赖 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 文档指引。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港；安全存储业务空间当前仅支持华北2（北京）地域。
- **API Key 权限继承**：API Key 的模型调用权限、限流策略完全继承自其归属的**业务空间**，与用户账号的控制台页面权限无关；删除 RAM 用户会导致其 API Key 失效（重新加入可恢复）。
- **安全存储依赖强耦合**：OSS Bucket 若被释放，将导致整个安全存储业务空间不可用且**无法恢复**；ADB/ES 停服或释放亦会导致知识库、审计日志等功能中断。
- **加密功能约束**：DashScope SDK 的自动加密仅支持 Java 和 Python；其他语言需自行实现混合加密逻辑；不支持自定义 AES 密钥。
- **超级管理员权限边界**：超级管理员可跨空间管理模型、用户、API Key，但 **OpenAPI 接口权限（如知识库、[Prompt 工程](../concepts/prompt.md)）必须由阿里云主账号在 RAM 控制台单独授权**，RAM 用户默认无权调用 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)


