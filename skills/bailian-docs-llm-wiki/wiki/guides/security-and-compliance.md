# security and compliance

阿里云百炼平台围绕权限管理、数据传输加密、内容安全审核、私网接入和合规备案五个维度，提供了完整的安全与合规体系。开发者可以根据业务场景按需启用对应能力，在满足监管要求的同时保护数据安全。本文汇总了百炼平台在安全与合规方面的核心功能和配置方式。

## 权限管理

百炼采用**业务空间**作为最小管理单元，支持基于角色的多维度权限控制，满足多地域、多用户的组织架构需求。详细的权限体系说明参见[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### 角色体系

平台定义了三种核心角色：

| 角色 | 职责范围 |
|------|---------|
| **超级管理员** | 跨空间统一管理用户权限、模型授权、模型限流和 API Key。包括阿里云主账号和拥有 `AliyunBailianFullAccess` 策略的 RAM 用户 |
| **业务空间管理员** | 管理特定业务空间内的用户权限和资源 |
| **普通用户** | 根据分配的权限使用资源 |

### 业务空间权限

单个业务空间不能跨地域存在。超级管理员可通过全局管理菜单对业务空间进行以下管理：

- **模型调用控制**：控制模型在空间内能否被调用，并设置请求数限流和 Token 限流
- **模型训练与部署控制**：管理模型的调优和部署权限
- **用户控制台权限**：管理 RAM 用户对控制台功能的访问

> **注意**：默认业务空间无法设置模型调用、训练和部署的限制，所有模型均可使用且无法限流。

### API Key 权限

单个 API Key 只能归属一个地域内的一个业务空间和一个用户，且不能转移。API Key 的可调用功能和模型限流与归属业务空间保持一致，不受用户控制台权限的影响。自 2026 年 3 月 25 日起，华北2（北京）地域的所有新创建 API Key 均归属主账号。华北2（北京）地域的 API Key 支持设置 IP 访问白名单。

### OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的数据、知识库、Prompt 工程及长期记忆等功能的 OpenAPI。若需调用，需要阿里云主账号在 RAM 控制台为 RAM 用户添加 `AliyunBailianDataFullAccess`（全部 API）或 `AliyunBailianDataReadOnlyAccess`（只读类 API）权限。

### 生产环境最佳实践

- **空间规划**：建议按环境划分（dev/test/prod），实现严格的环境隔离
- **限流策略**：将主账号总配额按比例分配给各业务空间，预留缓冲应对突发流量

## 内容安全

百炼支持接入 AI 安全护栏服务，在大模型自有合规检查之上进一步识别输入输出中的违规信息。详细配置方式参见[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

### 接入步骤

1. **开通内容审核服务**：访问 AI 安全护栏购买页面，创建服务关联角色并完成开通
2. **授权内容安全设置**：在百炼控制台的安全管理页面完成授权
3. **设置请求头**：在调用请求中添加 `X-DashScope-DataInspection` header

请求头格式：

```json
{
    "X-DashScope-DataInspection": {
       "input": "cip",
       "output": "cip"
    }
}
```

当输入内容触发安全审核时，API 将返回 `data_inspection_failed` 错误码（HTTP 400）。OpenAI 兼容模式和 DashScope 原生模式均支持该功能。

## 传输加密

百炼支持对请求体中的 `input` 字段进行加密传输，防止敏感数据在传输过程中被窃听或篡改。加密方案采用混合加密机制：数据由 AES 对称算法加密，AES 密钥通过 RSA 非对称加密传输。完整加密接入流程参见[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

### DashScope SDK 自动加密

DashScope SDK 封装了加解密逻辑，只需启用加密功能即可开箱使用：

- **Java SDK**：设置 `.enableEncrypt(true)`
- **Python SDK**：设置 `enable_encryption=True`

SDK 会自动完成加密和解密，返回明文结果，无需手动处理。

> **注意**：SDK 自动加密仅支持 Java 和 Python，不支持自定义密钥。其他语言需使用 HTTP 手动加密方式。

### HTTP 手动加密

手动加密适用于所有语言，但仅适用于 DashScope Endpoint，OpenAI 兼容模式不支持。核心步骤：

1. 生成 AES 密钥（128/192/256 位）和初始向量 IV
2. 通过 `GET /api/v1/public-keys/latest` 接口获取 RSA 公钥，用于加密 AES 密钥
3. 用 AES 密钥加密 `input` 内容，在 `X-DashScope-EncryptionKey` 请求头中传入加密后的密钥信息
4. 解密响应数据

RSA 公钥获取接口的详细说明参见[获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

## 私网访问

百炼支持通过阿里云 PrivateLink 建立 VPC 到百炼服务的私网连接，确保流量不经过公网。该连接为单向设计，仅允许 VPC 内资源主动访问百炼，百炼无法反向访问用户 VPC。详细操作参见[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

### 接入步骤

1. **创建接口终端节点**：在终端节点控制台选择 `com.aliyuncs.dashscope` 服务，绑定目标 VPC
2. **获取服务域名**：在终端节点详情页获取默认服务域名（HTTP）或自定义服务域名（HTTPS）
3. **替换 base_url**：将 API 调用中的公网域名替换为终端节点服务域名

支持的服务地域：华北2（北京）、新加坡。美国（弗吉尼亚）暂不支持私网访问。

### 跨地域私网访问

- **同境内/同境外**：推荐启用跨地域端点
- **跨境**：通过 CEN（云企业网）实现跨地域 VPC 互通

## 安全存储业务空间

百炼提供安全存储业务空间，通过反向终端节点将应用程序与用户私有网络中的云产品组件（ElasticSearch、AnalyticDB、OSS）关联，实现数据在用户自有资源中的隔离存储。

配置流程包括四个阶段：

1. **配置终端节点**：创建安全存储空间并建立反向终端节点连接，参见[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
2. **配置可用区 IP**：创建 MSE 云原生网关并获取可用区 VIP，参见[配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
3. **配置私有网络资源**：创建并配置 OSS Bucket、ADB 实例和 ES 实例，参见[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
4. **配置 MSE 网关并激活**：创建路由服务并激活安全存储空间，参见[配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)

> **注意**：安全存储业务空间需要申请开通，请咨询商务人员了解开通方式。如果 OSS Bucket 或 ES 实例被释放，安全存储空间将不可用且无法恢复，需重新创建。

## 合规备案

### 合规资质

百炼已通过 SOC 2 审计（无保留意见），在安全、可用性和保密性方面符合国际标准。详情参见[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

### 隐私保护

- 阿里云不会将用户数据用于模型训练
- 传输数据使用 AES-256 加密
- 根据法规要求，百炼将存储模型与应用调用时产生的数据

### 算法备案信息

百炼接入的主要模型备案信息，详见[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)：

| 模型 | 算法名称 | 备案编号 |
|------|---------|---------|
| 千问 | 达摩院交互式多能型合成算法 | 网信算备330110507206401230035号 |
| 万相（图像） | 达摩院图像合成算法 | 网信算备330110507206401230027号 |
| 万相（视频） | 通义万相视频生成算法 | 网信算备330106003156001240091号 |
| DeepSeek | DeepSeek 大语言模型算法 | 网信算备110108970550101240011号 |
| 智谱 AI | 智谱交互式内容生成算法 | 网信算备110108105858001230027号 |
| MiniMax | 应事文本信息合成算法-2 | 网信算备310104297296101230065号 |

### 应用上架合规

根据《生成式人工智能服务管理暂行办法》，使用百炼大模型的应用上架需要完成合规备案。不同场景所需材料不同，详细指南参见[千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)：

- **面向 C 端且不具有舆论属性**：需提供算法备案信息 + 合作协议
- **面向 C 端且具有舆论属性**：额外需要安全评估报告和算法备案
- **企业内部使用**：可能不直接适用，但需关注数据安全等内部合规要求

备案信息可在[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)中按备案编号查询验证。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)


