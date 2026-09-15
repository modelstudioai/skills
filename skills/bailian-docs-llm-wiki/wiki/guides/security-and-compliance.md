# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全护栏、模型备案、权限管控及数据隐私保护等关键维度。所有能力均面向企业级开发者设计，支持通过控制台、OpenAPI 和 SDK 三种方式集成，满足金融、政务、医疗等强监管行业的落地要求。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段 AES 加密 + RSA 公钥封装，适用于敏感数据场景；[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 提供完整加解密流程与 SDK 封装。
- **私网访问**：支持两种私网方案：
  - **PrivateLink 终端节点**：用于公网模型/API 的内网直连（如 `dashscope.aliyuncs.com`），流量全程走阿里云内网；
  - **安全存储业务空间反向终端节点**：专为高安全等级客户设计，需配合 MSE 网关、OSS/ADB/ES 等 VPC 内资源使用，实现数据不出私有云；该方案详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持在请求头中启用 `X-DashScope-DataInspection`，对输入输出进行涉黄、涉政、广告等违规内容识别；目前覆盖文本与图片类模型，调用时需显式配置 header。
- **模型备案**：所有上架模型均完成国家网信办算法备案与大模型备案，备案信息实时公示于 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)，开发者可直接引用用于应用上架合规申报。
- **权限与审计**：基于阿里云 RAM 实现三级权限体系（超级管理员 / 业务空间管理员 / 普通用户），支持模型调用、训练、部署的细粒度授权与限流，并与账单分账联动。

> **注意**：文档 6（`secure-storage.md`）将“私网访问配置”列为一级标题，但其实际内容全部指向子文档（如 `configure-an-endpoint-and-initiate-a-connection.md`），未提供独立逻辑说明；而文档 2（`transmission-security.md`）明确将 PrivateLink 归类为传输安全能力。因此，“私网访问”应按网络层（PrivateLink）与数据层（安全存储空间）分属两类能力，而非统一归入“传输安全”。

## 关键参数

| 参数名 | 位置 | 类型 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | SDK 调用参数 | bool | 启用 AES+RSA 混合加密 | `True`（Python）、`true`（Java） |
| `X-DashScope-EncryptionKey` | HTTP Header | string | RSA 加密后的 AES 密钥（Base64） | `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `X-DashScope-DataInspection` | HTTP Header | string（JSON string） | 启用安全护栏，必须为 JSON 字符串（非对象） | `'{"input":"cip","output":"cip"}'` |
| `public_key_id` & `public_key` | `/api/v1/public-keys/latest` 响应体 | string | 用于手动加密的 RSA 公钥元数据 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8..."` |
| IP 白名单 | API Key 管理页 | list | 限制 API Key 仅允许指定 IP 段调用 | `192.168.1.0/24,203.0.113.5` |

## 使用方式

### 1. 传输加密（推荐 SDK 自动模式）
- 安装 DashScope SDK ≥ v1.14.0（Python）或 ≥ v2.12.0（Java）；
- 在 `Generation.call()` 或 `GenerationParam.builder()` 中设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）；
- SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加密 `input` 并注入 header，响应自动解密。

### 2. 私网访问（二选一）
- **PrivateLink（通用模型 API）**：
  1. 在 VPC 控制台创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
  2. 替换 SDK 或 OpenAI 兼容模式的 `base_url` 为终端节点域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/compatible-mode/v1`）；
- **安全存储空间（高安全数据场景）**：
  1. 创建类型为“安全存储空间”的业务空间；
  2. 配置反向终端节点 → 可用区 VIP → OSS/ADB/ES 资源 → MSE 网关路由 → 最终激活空间；
  3. 所有数据读写均经由 MSE 网关转发至 VPC 内资源，不经过百炼公共服务层。

### 3. AI 安全护栏
- 在请求 header 中添加 `X-DashScope-DataInspection: '{"input":"cip","output":"cip"}'`；
- `input` 表示检查用户输入，`output` 表示检查模型输出；两者可独立开关（如 `"input":"off","output":"cip"`）；
- 触发拦截时返回 `400` 与 `data_inspection_failed` 错误码，无响应体内容。

### 4. 权限管理
- **超级管理员**（主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户）：通过全局管理菜单（如 [北京](https://bailian.console.aliyun.com/settings/workspace)）跨空间管理模型授权、限流、API Key；
- **业务空间管理员**：在空间内管理用户权限、页面可见性、模型调用/训练/部署开关；
- **普通用户**：仅能使用被授权的模型与页面，API Key 权限继承自所属空间的模型授权策略。

## 限制和注意事项

- **地域限制**：
  - PrivateLink 私网访问仅支持华北2（北京）、新加坡地域；美国（弗吉尼亚）暂不支持；
  - 安全存储业务空间仅支持华北2（北京），且 VPC 必须包含可用区 G/H/L 中至少两个；
- **API Key 约束**：
  - 单个 API Key 仅归属一个地域、一个业务空间、一个用户，不可迁移；
  - 自 2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号（文档 1 明确）；
- **加密限制**：
  - DashScope SDK 加密仅支持 Java/Python，其他语言需手动实现 HTTP 调用；
  - 不支持自定义 AES 密钥，密钥由 SDK 生成；
- **安全护栏限制**：
  - 仅对模型原始输入/输出生效，不检查中间步骤（如 RAG 检索结果）；
  - 若未配置 header，不触发护栏，无默认防护；
- **数据隐私承诺**：
  - 阿里云**绝不会将您的输入数据用于模型训练**（见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)）；
  - 所有传输数据默认 AES-256 加密，静态数据按服务协议约定存储。

> **注意**：文档 1 中关于“OpenAPI 接口权限”的描述存在过时风险——其末尾截断为 `AliyunBailianDataFullAccess`，未给出完整策略名及链接，且未说明该策略是否仍为最新推荐权限。开发者应以 RAM 控制台中实际可选的 `AliyunBailian*` 系统策略为准，优先选用 `AliyunBailianFullAccess`（超级管理员）或最小化自定义策略。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)


