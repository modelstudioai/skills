# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全护栏、模型备案、权限管控及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持通过控制台、API 和 SDK 灵活启用，满足金融、政务、医疗等强监管行业的合规要求。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持文本输入的模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了加解密流程与兼容性。
- **私网访问**：提供两种私网方案：  
  - 面向通用模型/API 调用的 **PrivateLink 终端节点**（适用于标准业务空间），通过 VPC 内网直连百炼网关，流量不经过公网；  
  - 面向高安全等级场景的 **安全存储业务空间**（需商务开通），基于反向终端节点 + MSE 云原生网关 + 专属云资源（OSS/ADB/ES）构建全链路私有网络，[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 是其核心前置步骤。
- **AI 安全护栏**：默认对输入输出内容进行基础合规检查；高级能力需开通并显式启用，支持 `input` 和 `output` 双向内容审核（如涉政、涉黄、广告等），适用于文本和图片类模型，详见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案**：所有上架模型均完成国家网信办算法备案及大模型备案，备案信息实时公示，开发者可直接用于应用上架合规申报，参考 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 6（`raw/model-user-guide/security-and-compliance/secure-storage.md`）标题为“私网访问配置”，但其子文档实际描述的是**安全存储业务空间**（一种独立于标准 PrivateLink 的、更高安全等级的私有化部署方案）。该方案与文档 5 中的通用 PrivateLink 私网访问在架构、开通方式、适用地域和管理路径上均不同，不可混用。开发者应根据安全等级要求选择对应方案。

## 关键参数

| 参数名 | 作用 | 说明 |
|--------|------|------|
| `enable_encryption=True` (Python SDK) / `enableEncrypt=true` (Java SDK) | 启用传输加密 | SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥并完成加解密，无需手动管理密钥。 |
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用 AI 安全护栏 | 必须作为 HTTP 请求头传递，值为 JSON 字符串（非嵌套对象），`cip` 表示启用内容安全检查。 |
| `X-DashScope-EncryptionKey` | 手动加密时的 AES 密钥密文 | 仅在 HTTP 手动调用模式下使用，由客户端用 RSA 公钥加密后填入请求头。 |
| `X-DashScope-Endpoint-ID` | （PrivateLink 场景）指定私网域名 | 非必需，当业务空间关联多个私网连接时，可通过此 Header 指定目标 Endpoint。 |

## 使用方式

1. **传输加密（推荐 SDK 方式）**  
   安装最新版 DashScope SDK（Python ≥ 2.0.0，Java ≥ 2.12.0），在 `Generation.call()` 或 `chat.completions.create()` 中设置 `enable_encryption=True` 即可。SDK 自动处理公钥获取、AES 密钥生成、加解密全流程。

2. **私网访问（标准 PrivateLink）**  
   - 在百炼控制台 **设置 > 网络配置 > VPC私网访问** 中添加私网连接（需授权 `AliyunServiceRoleForBackrouterAccessNet` 角色）；  
   - 在 **业务空间管理** 中将目标业务空间与私网连接关联；  
   - 替换 API 调用的 `base_url` 为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。

3. **AI 安全护栏**  
   - 开通服务：访问 [AI 安全护栏购买页](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn) 并创建服务关联角色；  
   - 授权：在百炼控制台 **设置 > 安全管理** 页面单击“去授权”；  
   - 调用：在请求 Header 中添加 `X-DashScope-DataInspection` 参数（值为 `{"input":"cip","output":"cip"}`）。

4. **合规备案材料获取**  
   - 算法备案号与主体信息见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)；  
   - 实际上架时，需登录 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)，用备案号（如 `网信算备330110507206401230035号`）查询并截图完整备案页；  
   - 合作协议需联系商务经理获取。

## 限制和注意事项

- **权限粒度**：超级管理员可跨地域、跨空间管理，但 **OpenAPI 接口权限（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)）仅主账号可开通**，RAM 用户需主账号在 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 等策略，详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **地域约束**：PrivateLink 私网访问仅支持华北2（北京）、华东2（上海）等 6 个地域；安全存储业务空间当前仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中的至少两个。
- **API Key 生命周期**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key 均归属主账号；RAM 用户的 API Key 在被移出业务空间后会失效（重新加入可恢复），但在 RAM 控制台删除该用户后将永久失效。
- **数据隐私承诺**：阿里云明确承诺**绝不会将客户数据用于模型训练**，所有传输数据默认使用 AES-256 加密，符合 SOC 2 审计要求（[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)）。
- **安全存储业务空间依赖**：OSS Bucket 若被释放，将导致整个安全存储空间不可用且无法恢复；ADB/ES 若停止计费或释放，同样会导致知识库、审计日志等功能中断。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


