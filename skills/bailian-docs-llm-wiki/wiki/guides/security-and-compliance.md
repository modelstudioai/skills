# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖权限管理、内容安全审核、传输加密、私网访问和安全存储等场景。本文汇总了百炼在安全合规方面的核心机制和配置方法，帮助开发者构建符合生产要求的 AI 应用。

## 权限管理体系

百炼基于**业务空间**进行精细化权限管理，单个业务空间是权限控制和账单分账的最小管理单元。权限体系包含三种角色：

| 角色 | 核心能力 |
|------|----------|
| **超级管理员**（主账号或拥有 AliyunBailianFullAccess 策略的 RAM 用户） | 跨空间管理用户权限、模型授权、模型限流、API Key |
| **业务空间管理员** | 管理特定空间内的用户权限和 API Key |
| **普通用户** | 使用被授权的空间、页面和资源 |

超级管理员可以通过全局管理菜单对各业务空间进行模型调用授权（含限流）、模型训练授权、模型部署授权和用户管理。详细的角色权限矩阵和生产环境空间规划策略，请参见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### API Key 权限

单个 API Key 归属一个地域内的一个业务空间和一个用户，不可跨空间或跨用户转移。API Key 的可调用功能和模型限流与归属业务空间保持一致，不受用户控制台权限的影响。华北2（北京）地域的 API Key 支持设置 IP 访问白名单。

> **注意**：自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 均归属主账号。

### OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的数据、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI。需要主账号在 RAM 控制台为 RAM 用户添加 `AliyunBailianDataFullAccess`（完整权限）或 `AliyunBailianDataReadOnlyAccess`（只读权限）策略。

## 内容安全：AI 安全护栏

百炼支持接入 AI 安全护栏服务，对模型输入输出进行违规内容检测（涉黄、涉政、广告等）。配置流程：

1. 开通内容审核服务（通过购买页完成）。
2. 在百炼控制台的安全管理页面完成授权。
3. 在 API 调用时添加请求头 `X-DashScope-DataInspection`：

```json
{
  "X-DashScope-DataInspection": {
    "input": "cip",
    "output": "cip"
  }
}
```

当检测到违规内容时，API 将返回 `data_inspection_failed` 错误码（HTTP 400）。OpenAI 兼容模式和 [DashScope SDK](../concepts/dashscope-sdk.md) 均支持该请求头。完整的接入示例和多语言代码，请参见 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 传输安全

### 加密调用模型推理

百炼支持对请求体中的 `input` 字段进行加密传输，采用 AES + RSA 混合加密机制：

- **AES 对称加密**：加密 `input` 内容（支持 128/192/256 位密钥）
- **RSA 非对称加密**：对 AES 密钥进行加密传输

**[DashScope SDK](../concepts/dashscope-sdk.md) 方式（推荐）**：仅需设置 `enableEncrypt=true`（Java）或 `enable_encryption=True`（Python），SDK 自动完成加解密，响应内容为明文。

**HTTP 手动方式**：需自行生成 AES 密钥和 IV，通过 `/api/v1/public-keys/latest` 接口获取 RSA 公钥，将加密后的密钥信息放入 `X-DashScope-EncryptionKey` 请求头，并对 `input` 内容加密。此方式仅适用于 DashScope Endpoint，不支持 OpenAI 兼容 Endpoint。

> **注意**：获取 RSA 公钥的接口详情见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)，完整加密流程见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

### 私网访问（PrivateLink）

通过创建接口终端节点，可以在 VPC 内通过私网直接调用百炼 API，流量不经公网。核心步骤：

1. 在终端节点控制台创建接口终端节点，选择服务 `com.aliyuncs.dashscope`，并开启自定义服务域名。
2. 获取终端节点服务域名（默认域名仅支持 HTTP，自定义域名支持 HTTPS）。
3. 将 API 调用的 `base_url` 域名替换为终端节点服务域名。

支持的地域：华北2（北京）、新加坡。跨地域私网访问可通过启用跨地域端点（同境内/同境外推荐）或 CEN 跨地域 VPC 互通（跨境场景）实现。详细配置步骤见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

## 安全存储业务空间

安全存储业务空间为百炼提供专属的隔离环境，将数据存储到用户自有的 VPC 资源中（OSS、AnalyticDB、ElasticSearch），避免与平台其他租户共享存储。配置流程包含以下关键步骤：

1. **创建安全存储业务空间**并配置反向终端节点（通过 PrivateLink 建立私网连接）。
2. **配置可用区 IP**：创建 MSE 云原生网关，获取可用区 VIP 并填入百炼配置。
3. **配置私有网络资源**：分别配置 OSS Bucket（需设置 `bailian-safe-workspace-oss-access` 标签和跨域规则）、ADB 实例（需开启向量引擎优化）和 ES 实例（需添加交换机网段到白名单）。
4. **配置 MSE 路由**：创建服务和路由规则，将请求转发至 ES 实例。
5. **激活安全存储空间**：确认所有资源配置无误后激活。

> **注意**：OSS Bucket 被释放或 ES 停止计费将导致安全存储空间不可用，且部分情况下无法恢复，需重新创建。

详细的操作步骤请参见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)、[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) 和 [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)。

## 合规资质与备案

### 平台合规

百炼已通过 SOC 2 审计（无保留意见），覆盖安全、可用性和保密性控制。阿里云承诺不会将用户数据用于模型训练，传输数据采用 AES-256 加密。详见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

### 模型算法备案

百炼接入的大模型均已完成算法备案。主要备案信息包括：

- **千问**（达摩院交互式多能型合成算法）：网信算备 330110507206401230035 号
- **万相**（达摩院图像合成算法 / 通义万相视频生成算法）：网信算备 330110507206401230027 号 / 330106003156001240091 号
- **DeepSeek**：网信算备 110108970550101240011 号
- **智谱 AI / Moonshot / MiniMax / 阶跃星辰** 等第三方模型也均已完成备案。

完整备案号列表见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

### 应用上架与合规备案

基于百炼大模型开发的应用/小程序上架应用市场前，需根据《生成式人工智能服务管理暂行办法》完成合规手续。不同场景所需材料不同：

- **面向 C 端（无舆论属性）**：需提供大模型算法备案信息和与阿里云的合作协议。
- **面向 C 端（有舆论属性）**：额外需要安全评估报告和企业自主算法备案。
- **企业内部使用**：虽可能不直接适用公开服务的监管要求，但仍需关注数据安全等内部合规。

详细的备案查询步骤和合作协议申请方式见 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


