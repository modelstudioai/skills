# security and compliance

阿里云百炼的安全与合规能力覆盖身份权限、内容安全、备案材料、数据隐私、传输加密、私网访问和安全存储等环节。开发者应先按地域和[业务空间](../concepts/workspace.md)规划权限边界，再根据应用形态选择 AI 安全护栏、加密调用、PrivateLink 或安全存储空间等能力，最后结合上架平台要求准备备案与合规材料。

## 能力范围与适用场景

### 权限与[业务空间](../concepts/workspace.md)隔离

百炼以[业务空间](../concepts/workspace.md)作为精细化权限管理和账单分账的最小单元，单个[业务空间](../concepts/workspace.md)不能跨地域存在；不同地域的默认[业务空间](../concepts/workspace.md)也是不同空间。权限体系主要包括超级管理员、[业务空间](../concepts/workspace.md)管理员和普通用户三类角色，详见[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

核心控制点包括：

- **模型调用授权与[限流](../concepts/rate-limit.md)**：超级管理员可控制某个模型是否允许在指定[业务空间](../concepts/workspace.md)通过控制台或 API 调用，并可设置请求数[限流](../concepts/rate-limit.md)和 [Token](../concepts/token.md) [限流](../concepts/rate-limit.md)。
- **模型训练与部署权限**：可限制[业务空间](../concepts/workspace.md)是否允许调优或部署特定模型。
- **控制台页面权限**：控制 RAM 用户可访问哪些[业务空间](../concepts/workspace.md)页面；该权限不影响其通过 [API Key](../concepts/api-key.md) 调用模型。
- **[API Key](../concepts/api-key.md) 管理**：[API Key](../concepts/api-key.md) 归属一个地域内的一个[业务空间](../concepts/workspace.md)和一个用户，其可调用功能和限流继承所属[业务空间](../concepts/workspace.md)权限。
- **OpenAPI 权限**：RAM 用户调用百炼应用的数据、[知识库](../concepts/[knowledge](../api/knowledge.md)-base.md)、Prompt 工程、长期记忆等 OpenAPI 时，需要主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`。

生产环境建议按开发、测试、预发、生产划分独立[业务空间](../concepts/workspace.md)，并为生产空间预留更高限流配额和更严格的用户权限。

> **注意**：默认[业务空间](../concepts/workspace.md)无法设置模型调用、训练、部署限制，也无法设置空间级限流；如果需要精细化隔离，应创建独立[业务空间](../concepts/workspace.md)。

### 输入输出内容安全

调用大模型时，百炼会根据模型自动匹配对应的 AI 安全护栏服务，目前文档说明支持文本和图片类型模型。接入方式是在请求头中增加 `X-DashScope-DataInspection`，指定对输入和输出进行内容检查，具体配置见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

关键请求头示例：

```json
{
  "X-DashScope-DataInspection": {
    "input": "cip",
    "output": "cip"
  }
}
```

OpenAI 兼容 SDK、[DashScope SDK](../concepts/dashscope-sdk.md)、Java、Node.js 等调用方式都可以通过额外请求头接入。命中高风险内容时，接口通常返回 `data_inspection_failed`、`DataInspectionFailed` 或 400 错误，调用方应将其作为业务可预期异常处理，而不是重试绕过。

### 备案与应用上架材料

如果应用、小程序通过百炼接入千问、万相等模型并计划上架到应用市场或小程序平台，开发者需要根据自身是否面向 C 端、是否具有舆论属性或社会动员能力等因素准备备案材料。备案号和算法备案信息可参考[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)与[千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

常见材料包括：

- 大模型算法备案信息或算法备案系统截图。
- 应用主体与阿里云主体的合作协议。
- 对具有舆论属性或社会动员能力的场景，可能还需要安全评估报告和企业自主算法备案。

备案信息页面公示了千问、万相、智谱 AI、DeepSeek、Moonshot、Xiaomi MiMo、可灵 AI、MiniMax、阶跃星辰、Vidu、Tripo、PixVerse 等模型或算法的备案编号；第三方模型备案信息由提供方负责。

> **注意**：备案信息、监管政策和平台审核要求可能变化。文档中的备案编号可作为材料准备入口，但实际提交前应以监管系统实时查询结果和应用平台最新要求为准。

### 合规资质与隐私保护

百炼通过 SOC 2 审计，在安全、可用性和保密性方面建立控制体系。隐私说明中明确：阿里云不会将用户数据用于模型训练；构建应用或训练大模型过程中传输的数据会经过 AES-256 加密。更多说明见[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

同时，百炼会根据法律法规和服务协议存储模型与应用调用时产生的数据。开发者在设计系统时，应将调用日志、审计、数据保留和用户告知纳入自身合规方案。

## 传输安全：加密调用与私网访问

### DashScope 推理请求加密

当请求内容涉及敏感信息或经公网传输时，可以对请求体中的 `input` 字段加密。百炼采用混合加密机制：使用 AES 加密 `input` 内容，使用 RSA 公钥加密 AES 密钥，并通过 `X-DashScope-EncryptionKey` 请求头传输密钥信息，完整流程见[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

接入方式有两类：

- **[DashScope SDK](../concepts/dashscope-sdk.md) 自动加密**：Java SDK 设置 `enableEncrypt(true)`，Python SDK 设置 `enable_encryption=True`。SDK 自动完成加解密，响应内容为明文。
- **HTTP 手动密钥管理**：调用方自行生成 AES 密钥和 IV，加密 `input`，再通过 RSA 公钥加密 AES 密钥，并在响应后自行解密。

手动模式需要先通过 `GET /api/v1/public-keys/latest` 获取 `public_key_id` 和 `public_key`，接口说明见[获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

关键参数包括：

- `input`：加密前为模型请求核心对象；手动加密后变为密文字符串。
- `X-DashScope-EncryptionKey`：JSON 字符串，包含 `public_key_id`、`encrypt_key`、`iv`。
- `Authorization`：获取 RSA 公钥与调用模型时均需使用 [API Key 鉴权](../concepts/api-key.md)。

> **注意**：文档明确说明 HTTP 手动加密机制适用于 DashScope Endpoint；OpenAI 兼容的 Chat Completions API 和 Responses API 不支持该加密机制。

### PrivateLink 私网访问模型或应用 API

如果需要在 VPC 内调用百炼模型或应用 API，并确保流量不经过公网，可创建接口终端节点，通过 PrivateLink 建立从 VPC 到百炼的单向私网连接。该能力详见[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

基本步骤：

1. 在百炼服务所在地域创建接口终端节点，终端节点服务选择 `com.aliyuncs.dashscope`。
2. 选择访问百炼服务的 VPC、交换机和安全组，安全组入方向需允许 80/443。
3. 获取默认服务域名或自定义服务域名。
4. 将 API 调用中的 `base_url` 从公网域名替换为终端节点服务域名。

地域限制与访问方式：

- 公共云百炼服务地域包括华北2（北京）和新加坡。
- 美国（弗吉尼亚）地域文档标注暂不支持私网访问。
- 同境内或同境外跨地域访问可使用跨地域端点；跨境跨地域访问可通过 CEN 做 VPC 互通。

> **注意**：默认服务域名仅支持 HTTP；如需 HTTPS，应使用自定义服务域名。

## 安全存储[业务空间](../concepts/workspace.md)

安全存储业务空间适用于需要将百炼应用程序的数据读写限制在特定私有网络资源中的场景，例如使用私网内的 OSS、AnalyticDB PostgreSQL、Elasticsearch 等组件，避免通过公网访问外部服务。相关配置由一组文档串联完成，包括[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)、[配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)、[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)和[配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)。

### 配置流程

1. **创建安全存储业务空间**：在业务空间管理中新增空间，空间类型选择安全存储空间。
2. **创建反向终端节点**：在华北2（北京）等支持地域创建反向终端节点，并在百炼侧确认连接。
3. **配置可用区 IP**：创建或复用 MSE 云原生网关，获取 NLB 的可用区 VIP 与交换机网段，并将 VIP 配置到百炼安全存储空间。
4. **配置私有网络资源**：按需配置 OSS、ADB、ES，并完成百炼访问授权、标签、白名单、账号密码等配置。
5. **配置 MSE 云原生网关**：将私网资源登记为网关服务，创建路由并发布。
6. **激活安全存储业务空间**：确认 Elasticsearch、ADB、OSS 都配置无误后激活空间。

### 资源配置要点

- **OSS**：Bucket 需要设置特定标签 `bailian-safe-workspace-oss-access=ReadAndWrite`，并配置允许百炼控制台来源的 CORS 规则。
- **ADB**：首次配置需要授权服务角色 `AliyunServiceRoleForSFMAccessADB`。
- **ES**：需要将交换机网段加入 VPC 私网访问白名单，并在百炼配置实例 ID、账号和密码。
- **MSE**：服务来源选择 DNS 域名，路由路径通常为 `/`，后端服务指向已创建的私网资源服务。

> **注意**：OSS Bucket 停止服务会导致安全存储空间、[知识库](../concepts/[knowledge](../api/knowledge.md)-base.md)、审计日志、历史记录等模块不可用；Bucket 释放或 ES 释放可能导致安全存储空间不可恢复，需要重新创建。

## 开发者落地建议

- **最小权限优先**：为不同环境创建独立业务空间，只向 RAM 用户授予必要页面权限、[API Key](../concepts/api-key.md) 权限和 OpenAPI 权限。
- **[API Key](../concepts/api-key.md) 安全**：优先使用环境变量保存 [API Key](../concepts/api-key.md)，不要硬编码到代码仓库；根据地域能力设置 IP 访问白名单。
- **内容安全前置**：面向外部用户的应用建议默认接入 AI 安全护栏，并把安全拦截错误纳入前端提示和审计日志。
- **敏感输入加密**：对包含个人信息、商业秘密或内部数据的 `input` 启用 [DashScope SDK](../concepts/dashscope-sdk.md) 加密或 HTTP 手动加密。
- **网络隔离**：生产环境优先使用 PrivateLink 或安全存储空间，将公网暴露面降到最低。
- **合规材料留痕**：保存备案系统查询截图、合作协议、模型备案编号、内容审核策略和用户协议版本，便于上架审核和后续审计。

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






