# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 对称加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`、`qwen-flash`）[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持通过 PrivateLink 建立 VPC 到百炼网关的内网通道，流量全程不经过公网；同时支持为安全存储业务空间配置专属私有网络资源（OSS/ADB/ES），实现数据存储层的网络隔离 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection`，启用输入输出双路内容安全检测（涉黄、涉政、广告等），适用于所有已接入护栏服务的文本与图像模型 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案**：平台所接入的千问、万相、DeepSeek、Moonshot 等主流模型均已取得国家网信办算法备案号及大模型备案号，相关信息实时公示并可于[互联网信息服务算法备案系统](https://beian.cac.gov.cn)核验 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 13 中提及“万相”对应两个不同备案主体（达摩院与通义云启）及两个备案号，与文档 12 表格中“万相”仅列示一个算法备案号存在不一致。实际备案应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn)实时查询结果为准，开发者需按具体调用的模型版本（如图像生成 vs 视频生成）分别引用对应备案号。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | bool | 否（默认 `false`） | SDK 层启用传输加密的开关，启用后自动获取公钥、生成 AES 密钥并加解密 | `True`（Python） / `true`（Java） |
| `X-DashScope-EncryptionKey` | string | 是（HTTP 手动调用时） | Base64 编码的 RSA 加密后的 AES 密钥，随请求头发送 | `"LS0t...LUVORCBQUklWQVRFIEtFWS0tLS0t"` |
| `X-DashScope-DataInspection` | string | 否 | 启用 AI 安全护栏的请求头，值为 JSON 字符串（非对象），指定 input/output 检测策略 | `'{"input":"cip","output":"cip"}'` |
| `public_key_id` | string | — | 从 `/api/v1/public-keys/latest` 接口返回，用于标识当前生效的 RSA 公钥版本 | `"1"` |

## 使用方式

### 1. 传输加密（推荐使用 SDK）
- **前提**：已配置有效 API Key（建议设为环境变量 `DASHSCOPE_API_KEY`）。
- **SDK 调用**（Python/Java）：仅需在 `Generation.call()` 或 `GenerationParam.builder()` 中设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，其余参数与普通调用完全一致。SDK 自动完成公钥获取、AES 密钥生成、加解密全流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **HTTP 手动调用**：需先调用 `GET /api/v1/public-keys/latest` 获取 `public_key` 和 `public_key_id`，再用该公钥加密自生成的 AES 密钥，并将加密密钥放入 `X-DashScope-EncryptionKey` 请求头 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 2. 私网访问
- **API 域名替换**：将默认公网域名（如 `https://{WorkspaceId}.{RegionId}.maas.aliyuncs.com/api/v1`）替换为私网域名（格式：`https://{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com/api/v1`），该域名仅在关联 VPC 内可解析 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储空间配置**：需依次完成「创建反向终端节点」→「配置可用区 IP」→「配置 OSS/ADB/ES 资源」→「配置 MSE 网关」四步，全部完成后方可激活业务空间 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

### 3. AI 安全护栏
- **开通与授权**：需主账号在[安全管理](https://bailian.console.aliyun.com/settings/security?globalset=1)页面完成服务开通与角色授权。
- **调用启用**：在任意 SDK 或 HTTP 请求中添加 `X-DashScope-DataInspection` 请求头，值为 `{"input":"cip","output":"cip"}` 的字符串形式（注意外层为单引号或转义双引号） [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 限制和注意事项

- **权限粒度**：业务空间是权限管理的最小单元，**默认业务空间无法设置模型调用/训练/部署的细粒度限流与授权**；所有限制必须在显式创建的业务空间中配置 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 归属**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key **强制归属主账号**，不再支持归属 RAM 用户；且单个 API Key 仅绑定一个业务空间，不可跨空间复用 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限隔离**：RAM 用户默认**无权调用应用层 OpenAPI**（知识库、Prompt 工程等），必须由主账号在 RAM 控制台为其授予 `AliyunBailianDataFullAccess` 等特定策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储依赖强耦合**：OSS/ADB/ES 任一组件停止服务或被释放，将导致整个安全存储业务空间不可用且**无法恢复**，必须重建 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **合规责任主体**：即使使用百炼平台提供的已备案模型，**应用/小程序开发者自身仍是《生成式人工智能服务管理暂行办法》定义的“服务提供者”**，须独立承担内容审核、用户权益保障、算法备案（如适用）等全部法定义务 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


