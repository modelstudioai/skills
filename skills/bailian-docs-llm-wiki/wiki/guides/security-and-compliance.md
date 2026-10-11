# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段的 AES-256 对称加密 + RSA 公钥封装密钥的混合加密机制，适用于敏感数据场景。该能力已集成至 DashScope SDK（Java/Python），开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内流量全程走阿里云内网，避免公网暴露；同时支持“安全存储业务空间”模式，将知识库、审计日志等数据完全托管于客户私有网络内的 OSS/ADB/ES 资源中 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection`，启用输入/输出双路内容安全检测（涉黄、涉政、广告等），由独立服务提供实时拦截 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已取得国家网信办算法备案号及大模型备案号，信息持续公示并可溯源验证 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

## 关键参数

| 参数名 | 说明 | 示例值 | 来源 |
|--------|------|--------|------|
| `enable_encryption` / `enableEncrypt` | SDK 启用传输加密的布尔开关 | `True` / `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 | `'{"input":"cip","output":"cip"}'` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密时，用于传递 RSA 加密后的 AES 密钥 | Base64 编码字符串 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-IP-Whitelist` | API Key 级 IP 白名单（仅限 IPv4，美国弗吉尼亚地域不支持 IPv6） | `"192.168.1.0/24,203.0.113.5"` | [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) |

> **注意**：文档 1 中明确指出“API Key 的状态随归属用户（账号）操作的变化”，但未说明白名单变更是否实时生效；实际行为以控制台操作后立即生效为准，建议在生产环境变更后进行调用验证。

## 使用方式

1. **传输加密（SDK 方式）**  
   - 安装最新版 DashScope SDK（Java ≥ 2.12.0，Python ≥ 1.14.0）；  
   - 在 `Generation.call()` 或 `GenerationParam.builder()` 中设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）；  
   - SDK 自动完成公钥获取、AES 密钥生成、加解密全流程，响应体为明文。

2. **私网访问（PrivateLink）**  
   - 在百炼控制台 **管理 > 网络配置** 开通私网连接，绑定目标 VPC 与可用区交换机；  
   - 在 **业务空间管理** 中将目标业务空间关联该私网连接；  
   - 替换 API 请求域名：将 `{WorkspaceId}.{RegionId}.maas.aliyuncs.com` 替换为生成的私网域名 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`。

3. **AI 安全护栏**  
   - 开通服务并完成授权（需主账号在 **安全管理** 页面操作）；  
   - 在任意模型调用请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；  
   - 违规内容将触发 `400 DataInspectionFailed` 错误，不返回模型输出。

4. **安全存储业务空间（私有网络数据托管）**  
   - 申请开通“安全存储空间”类型业务空间；  
   - 依次完成：创建反向终端节点 → 配置可用区 VIP → 授权 OSS/ADB/ES → 配置 MSE 网关路由 → 激活空间；  
   - 所有知识库、历史记录、审计日志等数据均落盘至客户指定的私有云资源，百炼平台无权直接访问原始数据。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储业务空间当前仅支持华北2（北京）[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **权限继承规则**：API Key 的模型调用权限、限流策略完全继承自其归属的**业务空间**，与用户（RAM 账号）的控制台页面权限无关；删除用户或将其移出业务空间将导致其所有 API Key 失效 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储依赖强耦合**：OSS Bucket 若被释放，将导致整个安全存储业务空间不可用且**无法恢复**；ADB/ES 停服或释放亦会导致知识库等功能中断，需提前规划续费与灾备 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案责任主体**：使用百炼接入千问等模型的应用/小程序，其开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户权益保障、算法备案（如适用）等全部法定义务，阿里云仅作为“服务技术支持者”提供备案信息与协议支持 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。
- **加密兼容性**：传输加密仅支持 `input` 字段（含 `messages`），不支持对 `parameters`（如 `temperature`）或 `tools` 等其他字段加密；HTTP 手动加密方式需自行管理密钥生命周期，不推荐生产环境长期使用。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


