# security and compliance

阿里云百炼围绕"身份权限、内容安全、合规备案、传输加密、私网与安全存储"五个维度构建安全合规体系，覆盖从控制台到 API 调用、从公网到 VPC 私网的完整链路。本文面向开发者，按"权限与身份—内容安全—合规备案—传输加密—[私网访问](../concepts/vpc-private-access.md)—安全存储"的顺序梳理关键能力、参数与注意事项。

## 身份与权限管理

百炼的权限管理基于[业务空间](../concepts/workspace.md)（workspace）这一最小管理单元，支持控制台页面级与模型级的多维度权限控制，满足多地域、多用户的复杂组织架构需求，详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### 三种角色

- **超级管理员**：阿里云主账号，或拥有 `AliyunBailianFullAccess` 系统策略的 RAM 用户，可跨空间统一管理用户权限、空间可用模型、模型限流和 [API Key](../concepts/api-key.md)。建议 AI 安全护栏、模型监控、应用观测等功能使用主账号一次性开通。
- **[业务空间](../concepts/workspace.md)管理员**：拥有访问某个[业务空间](../concepts/workspace.md)"权限管理"页面的 RAM 用户，可管理该空间内的用户与资源，"管理员"权限包含该空间所有页面的访问权限。
- **普通用户**：根据分配的权限使用资源，不能管理用户或模型授权。

[业务空间](../concepts/workspace.md)按地理区域划分，**单个[业务空间](../concepts/workspace.md)不能跨地域存在**，各地域的默认[业务空间](../concepts/workspace.md)也是不同的空间。

### 模型与 [API Key](../concepts/api-key.md) 权限

[业务空间](../concepts/workspace.md)内可对模型进行三类精细化授权，**默认[业务空间](../concepts/workspace.md)无法设置这些限制**（所有模型均可调用、调优、部署）：

| 权限项 | 控制范围 | 配置入口 |
| --- | --- | --- |
| 限制模型调用 | 是否可调用（控制台 & API）+ 请求数限流 + [Token](../concepts/token.md) 限流 | 模型列表 → 模型调用列开关 + 当前空间限流列 |
| 限制模型训练 | 是否可调优（控制台 & API）及调优后部署 | 模型列表 → 模型授权 → 模型训练列 |
| 限制[模型部署](../concepts/model-deployment.md) | 是否可直接部署 | 模型列表 → 模型授权 → [模型部署](../concepts/model-deployment.md)列 |

单个 [API Key](../concepts/api-key.md) 只能归属一个地域内的一个[业务空间](../concepts/workspace.md)和一个用户，且不能转移。[API Key](../concepts/api-key.md) 的可调用功能与模型限流与**归属[业务空间](../concepts/workspace.md)**的权限保持一致，不受用户控制台权限影响，也无需为不同模型（文生文、文生图、语音合成）创建不同 [API Key](../concepts/api-key.md)。自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 [API Key](../concepts/api-key.md) 均归属主账号，并支持设置 IP 访问白名单。

> **注意**：[API Key](../concepts/api-key.md) 的有效性受账号操作影响——将 RAM 账号移出[业务空间](../concepts/workspace.md)会使其 [API Key](../concepts/api-key.md) 失效（重新加入后恢复），而在 RAM 控制台删除账号/角色则会使 [API Key](../concepts/api-key.md) 永久失效、不可恢复。

### OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的数据、[知识库](../concepts/knowledge-base.md)、Prompt 工程、长期记忆等 Open API。需阿里云主账号在 RAM 控制台添加以下系统策略之一：

- `AliyunBailianDataFullAccess`：可调用应用 API 目录下的所有 API。
- `AliyunBailianDataReadOnlyAccess`：仅可调用只读类 API（如 `DescribeFile`、`GetIndexJobStatus`）。

### 生产环境实践

- **空间规划**：推荐按环境（dev/test/prod）划分[业务空间](../concepts/workspace.md)实现隔离，或按业务线划分便于权限与成本管理。
- **限流策略**：将主账号总配额按比例分配给各[业务空间](../concepts/workspace.md)并预留缓冲。例如总配额 1000 QPM，可分配 prod 600 / test 200 / dev 100，预留 100。

## 内容安全：AI 安全护栏

大模型输入输出可能包含涉黄、涉政、广告等敏感内容。除模型自有合规检查外，百炼支持接入 AI 安全护栏服务，进一步识别违规信息，保障安全合规，详见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

### 开通步骤

1. **开通内容审核服务**：访问 AI 安全护栏购买页面，创建服务关联角色并购买。
2. **授权内容安全设置**：在百炼"安全管理"页面单击"去授权"开启内容安全设置。若已显示"已开通（不可取消）"及《自建安全机制承诺函》全文，可跳过此步。
3. **设置请求头**：调用百炼时在请求头设置 `X-DashScope-DataInspection`，开启输入输出检测：

```json
{"X-DashScope-DataInspection": {"input": "cip", "output": "cip"}}
```

目前支持文本和图片类型的模型，模型与护栏服务的对应关系及[计费](../concepts/billing.md)请参见官方说明。命中护栏时返回 `data_inspection_failed`（DashScope 为 `DataInspectionFailed`，HTTP 400），提示输入可能包含不当内容。

## 合规资质与备案

### 资质与隐私

百炼以无保留意见通过 SOC 2 审计，安全、可用性、保密性控制符合国际标准。阿里云承诺**不会将您的数据用于模型训练**，应用构建与模型训练过程中的传输数据均经过 AES-256 加密。根据法律法规，百炼会存储模型与应用调用产生的数据，详见《阿里云百炼服务协议》中的数据处理、隐私和安全条款，参考 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

### 模型备案信息公示

百炼公示所接入大模型的算法备案号与大模型备案号，详见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。部分示例如下：

| 模型 | 算法名称 | 算法备案号 |
| --- | --- | --- |
| 千问 | 达摩院交互式多能型合成算法 | 网信算备330110507206401230035号 |
| 万相 | 达摩院图像合成算法 | 网信算备330110507206401230027号 |
| 万相 | 通义万相视频生成算法 | 网信算备330106003156001240091号 |
| DeepSeek | DeepSeek 大语言模型算法 | 网信算备110108970550101240011号 |
| 智谱 AI | 智谱交互式内容生成算法 | 网信算备110108105858001230027号 |

大模型备案号（如通义千问 `ZheJiang-TongYiQianWen-20230901`、DeepSeek `Beijing-DeepseekChat-202404280016` 等）同样公示。第三方模型备案信息由提供方负责，阿里云百炼不作额外承诺。

### 应用上架及合规备案

接入千问、万相等模型的应用/小程序上架前，需依《生成式人工智能服务管理暂行办法》完成合规备案，详见 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

典型场景与所需材料：

| 场景 | 是否面向 C 端 | 舆论/动员能力 | 主要材料 |
| --- | --- | --- | --- |
| 场景 1 | 是 | 不具有 | 大模型算法备案信息 + 应用主体与阿里云的合作协议 |
| 场景 2 | 是 | 具有 | 场景 1 全部材料 + 企业自主安全评估报告 + 企业自主算法备案 |
| 场景 3 | 企业内部 | — | 关注数据安全、保密等内部合规要求 |

算法备案信息查询步骤：打开互联网信息服务算法备案系统（beian.cac.gov.cn），以"备案编号"为搜索类别输入对应备案号（如千问 `网信算备330110507206401230035号`），截图保存查询页面完整内容。合作协议（需含算法名称、应用产品或备案编号）请联系商务经理获取。

> **注意**：即使使用阿里云提供的模型及备案信息，应用/小程序开发者仍是法规定义的"服务提供者"，需独立履行内容审核、用户保护、数据安全、标识规范等全部法定义务。备案号应以算法备案系统实时查询结果为准，建议定期核验。

## 传输加密：以加密方式接入模型推理

当请求涉及敏感信息或经公网传输时，可对请求体 `input` 字段值加密，防止传输过程中被窃听或篡改，详见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

### 加解密机制

采用混合加密：数据由 AES 对称算法加密，AES 密钥通过 RSA 非对称加密实现安全传输。流程为：生成 AES 密钥 → 用 AES 密钥加密 `input` → 用 RSA 公钥加密 AES 密钥 → 将加密后的 `input` 与密钥信息（封装在 `X-DashScope-EncryptionKey` 请求头）传入百炼 → 平台推理链路全程加密、解密数据并用相同 AES 密钥加密答案返回 → 用户侧用 AES 密钥解密响应。

### 两种接入方式

**1. [DashScope SDK](../concepts/dashscope-sdk.md)（自动加密·开箱即用）**

仅支持 Java 和 Python，不支持自定义密钥：

- Java SDK：`GenerationParam.builder().enableEncrypt(true)`
- Python SDK：`dashscope.Generation.call(..., enable_encryption=True)`

SDK 自动完成加解密，响应为明文，无需手动处理。

**2. HTTP 调用（手动密钥管理）**

需额外完成三步：添加 `X-DashScope-EncryptionKey` 请求头、对 `input` 内容加密、对响应数据解密。该请求头为 JSON 字符串，含 `public_key_id`（公钥 ID）、`encrypt_key`（RSA 公钥加密后的 AES 密钥）、`iv`（初始向量）三个字段。AES 密钥长度支持 128/192/256 位（32 字节），长度越长安全性越高但开销越大。

> **注意**：手动加密调用仅适用于 DashScope 的 Endpoint，OpenAI 兼容（Chat Completions API 和 Responses API）的 Endpoint **不支持**此加密机制。

### 获取 RSA 公钥

加密前需调用接口获取当前最新公钥 ID 及其值，详见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

- 接口：`GET /api/v1/public-keys/latest`
- 鉴权：`Authorization: Bearer <API-KEY>`
- 返回：`request_id`、`data.public_key`（RSA 公钥值）、`data.public_key_id`（公钥 ID）
- 前提：已开通百炼服务并获得 API-KEY，建议配置到环境变量以降低泄漏风险。

## [私网访问](../concepts/vpc-private-access.md)：通过 PrivateLink 终端节点访问 API

为在 VPC 内直接调用百炼模型/应用 API 且流量不经公网，可创建私网终端节点（PrivateLink），将通信限制在阿里云内网，详见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

### 工作原理与地域

终端节点连接为**单向设计**，仅允许 VPC 内资源主动访问百炼，百炼无法反向访问 VPC 内资源。百炼公共云服务所在地域：华北2（北京）、新加坡。**美国（弗吉尼亚）地域暂不支持[私网访问](../concepts/vpc-private-access.md)**。

### 配置步骤

1. **创建接口终端节点**：在终端节点控制台创建，终端节点服务选择"阿里云服务"并筛选 `com.aliyuncs.dashscope`，开启"自定义服务域名"。建议至少选择两个不同可用区的交换机以实现高可用；安全组入方向需允许 80（http）、443（https）。
2. **获取终端节点服务域名**：默认服务域名格式 `ep-{实例ID}.privatelink.aliyuncs.com`（仅 HTTP）；自定义服务域名格式 `vpc-{实例ID}.{地域ID}.dashscope.aliyuncs.com`（支持 HTTPS）。
3. **调用验证**：将 API base_url 中的域名替换为终端节点服务域名后在对应 VPC 发起调用。支持 HTTP/curl、OpenAI Python SDK、DashScope Python SDK（建议 ≥1.14.0）、DashScope Java SDK（建议 ≥2.12.0）。

### 跨地域访问

- **同境内或同境外跨地域**（如华东1杭州 VPC → 华北2北京百炼）：推荐启用跨地域端点。
- **跨境跨地域**（中国内地与境外之间，如华北2北京 VPC → 新加坡百炼）：通过 CEN 跨地域 VPC 互通。

## 安全存储[业务空间](../concepts/workspace.md)

安全存储[业务空间](../concepts/workspace.md)通过反向终端节点与 VPC 私网连接，让部署其中的应用访问同 VPC 下的 ElasticSearch、AnalyticDB（ADB）、OSS 等云组件，避免公网访问风险。该能力需联系商务人员申请开通。

### 配置流程总览

| 步骤 | 说明 | 参考 |
| --- | --- | --- |
| 1. 创建安全存储[业务空间](../concepts/workspace.md) | [业务空间](../concepts/workspace.md)管理 → 新增[业务空间](../concepts/workspace.md)，空间类型选"安全存储空间" | [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) |
| 2. 创建反向终端节点 | 终端节点控制台创建反向终端节点，终端节点服务选描述为"百炼公共云生产环境-北京站点-安全存储空间专网通道接入点"的服务（VPC NAT 网关、反向、IPv4），配置 VPC/安全组/可用区与交换机 | 同上 |
| 3. 在百炼确认连接 | [业务空间](../concepts/workspace.md)管理 → 管理安全存储空间 → 选择终端节点 → 连接，等待状态变为"已连接" | 同上 |
| 4. 配置可用区 IP | 创建 MSE 云原生网关（2核4G、2 节点、启用 TLS 硬件加速、私网、至少两可用区），获取 NLB 各可用区 VIP 与交换机网段，在百炼配置对应可用区 IP，并将 VIP 加入反向终端节点安全组入方向（全部端口） | [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md) |
| 5. 配置私有网络资源 | 配置 OSS（Bucket 名 `bailian-safe-workspace-oss-access`、特定标签、CORS 来源 `*bailian.console.aliyun.com`）、ADB（6.0 标准版、高可用版、开启向量引擎优化）、ElasticSearch（7.10、内核增强版、两可用区，交换机网段加入 VPC 私网访问白名单） | [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) |
| 6. 配置 MSE 云原生网关 | 在网关创建 DNS 域名服务（指向 ES 私网地址/端口，TLS 关闭）、创建路由（域名为 ES 域名、路径 `/`、单服务），然后回百炼"资源配置"页激活安全存储[业务空间](../concepts/workspace.md) | [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md) |

### 关键约束与注意事项

- 专有网络地域须为华北2（北京），可用区须在 G/H/L（或 ADB 的 G/H/I）中按要求选择，每个可用区至少一个交换机；反向终端节点的安全组不要放入其他云组件、无需配置出入网规则。
- 阿里云百炼只能访问客户授权过且带特定标签（标签名 `bailian-safe-workspace-oss-access`，标签值 `ReadAndWrite`）的 OSS Bucket。
- ADB 配置需授权服务关联角色 `AliyunServiceRoleForSFMAccessADB`（策略 `AliyunServiceRolePolicyForSFMAccessADB`）。
- **资源不可中断**：OSS Bucket 停止服务会导致安全存储空间、[知识库](../concepts/knowledge-base.md)、审计日志、历史记录等模块不可用，恢复 Bucket 后可恢复；但 Bucket 被释放会造成安全存储空间不可用且**无法恢复**，需重建。ES 停止[计费](../concepts/billing.md)/被释放的后果与 OSS 相同。
- 激活前安全存储空间不可用，激活成功后才可用。

## 限制与注意事项汇总

- 默认[业务空间](../concepts/workspace.md)无法设置模型调用/训练/部署限制，所有模型均可调用、调优、部署，且无法限流。
- [API Key](../concepts/api-key.md) 不可跨地域、跨业务空间、跨用户转移；账号移出空间会使其 [API Key](../concepts/api-key.md) 失效（重新加入恢复），删除账号/角色则永久失效。
- AI 安全护栏目前仅支持文本和图片类型模型。
- [DashScope SDK](../concepts/dashscope-sdk.md) 自动加密仅支持 Java/Python 且不支持自定义密钥；HTTP 手动加密仅适用于 DashScope Endpoint，OpenAI 兼容 Endpoint 不支持。
- PrivateLink 私网访问美国（弗吉尼亚）地域暂不支持；跨地域访问需区分同境内/同境外与跨境两种方式。
- 安全存储业务空间的 OSS/ES 等底层资源一旦释放，安全存储空间不可恢复，需重建。
- 模型与应用的合规备案信息应以算法备案系统实时查询结果为准，建议定期核验；开发者作为"服务提供者"需独立承担全部法律责任。

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

















