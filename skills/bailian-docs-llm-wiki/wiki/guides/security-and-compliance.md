# security and compliance

阿里云百炼围绕"权限控制—内容安全—传输加密—私网接入—合规备案"构建了多层安全体系。开发者可以在[业务空间](../concepts/workspace.md)粒度上做模型调用、训练、部署的精细化授权；在数据链路层通过 AI 安全护栏、AES+RSA 混合加密和 PrivateLink 私网终端节点保护输入输出内容；在合规层面，平台已公示接入模型的算法备案号与大模型备案号，方便应用上架与监管审查。

## 权限管理

百炼以**[业务空间](../concepts/workspace.md)**为最小管理单元，支持跨地域的多空间架构（单个[业务空间](../concepts/workspace.md)不能跨地域存在）。权限体系基于三种角色：

| 角色 | 关键能力 |
| --- | --- |
| 超级管理员（主账号 / 拥有 `AliyunBailianFullAccess` 的 RAM 用户） | 跨空间管理用户、模型调用/训练/部署授权、限流、API Key |
| 业务空间管理员 | 管理本空间的用户、页面权限、API Key |
| 普通用户 | 按授权访问空间、页面和资源 |

要点：

- **API Key 权限**：单个 API Key 只能归属一个地域内的一个业务空间和一个用户，不可转移。API Key 的可调用模型和限流与归属空间保持一致，不受用户控制台页面权限影响。自 2026 年 3 月 25 日起，华北2（北京）地域新建的 API Key 均归属主账号。华北2（北京）的 API Key 支持设置 IP 访问白名单。
- **OpenAPI 接口权限**：RAM 用户默认无权调用百炼应用、知识库、Prompt 工程等 Open API，需要主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 系统策略。
- **生产环境建议**：按环境（dev / test / prod）或按业务线划分空间，把主账号总配额按比例分配到各空间并预留缓冲。详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

## 内容安全：AI 安全护栏

大模型自带的合规检查通常已足够，百炼额外支持接入 **AI 安全护栏服务** 对输入输出做二次审核（目前覆盖文本和图片类型模型）。

接入步骤：

1. 在 AI 安全护栏购买页开通内容审核服务，并创建服务关联角色。
2. 在百炼 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成授权。
3. 调用时在请求头设置 `X-DashScope-DataInspection`：

```json
{
  "X-DashScope-DataInspection": {
    "input": "cip",
    "output": "cip"
  }
}
```

触发拦截时返回 HTTP 400，错误码 `data_inspection_failed`（DashScope 协议为 `DataInspectionFailed`）。详见 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 数据传输安全

### 加密接入模型推理

对 `input` 字段做 AES 对称加密，AES 密钥再用百炼托管的 RSA 公钥加密后通过 `X-DashScope-EncryptionKey` 请求头传入，推理链路全程加密，响应也用同一 AES 密钥加密返回。

- **DashScope SDK（Java / Python）**：设置 `enableEncrypt(true)` 或 `enable_encryption=True` 即可开箱即用，SDK 自动处理加解密。
- **HTTP 手动接入**：先调用 `GET /api/v1/public-keys/latest` 获取最新公钥 ID 与值，再生成 128/192/256 位 AES 密钥与 IV，完成加密请求与解密响应。
- **限制**：加密机制仅适用于 DashScope Endpoint，OpenAI 兼容（Chat Completions / Responses API）Endpoint 不支持。

详见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 与 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 私网访问（PrivateLink）

通过 VPC 内的接口终端节点私网调用百炼 API，流量不经公网。连接为**单向**设计：仅 VPC 内资源可主动访问百炼，百炼无法反向访问 VPC。

- **支持地域**：华北2（北京）、新加坡。美国（弗吉尼亚）暂不支持私网访问。
- **终端节点服务**：选择阿里云服务 `com.aliyuncs.dashscope`，建议开启自定义服务域名以获得 HTTPS 支持（默认域名仅 HTTP）。
- **域名替换**：调用时把 `dashscope.aliyuncs.com` 替换为终端节点服务域名，例如 `vpc-cn-beijing.dashscope.aliyuncs.com` 或 `ep-{实例ID}.privatelink.aliyuncs.com`。
- **跨地域**：同境内/同境外推荐启用跨地域端点；跨境（如北京 VPC 调新加坡百炼）需通过 CEN 互通。

详见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

## 合规资质与隐私

- 百炼已通过 **SOC 2** 审计（无保留意见），在安全、可用性、保密性方面符合国际标准。
- 阿里云承诺**不会将用户数据用于模型训练**。构建应用或训练过程中传输的数据采用 **AES-256** 加密。
- 平台会存储模型与应用调用产生的数据，具体条款见《阿里云百炼服务协议》。

详见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 应用上架与合规备案

根据《生成式人工智能服务管理暂行办法》（2023-08-15 生效），面向公众的 AIGC 应用必须完成合规手续，否则将被下架。是否需要备案、需要哪些材料，取决于应用形态：

| 场景 | 所需材料 |
| --- | --- |
| 面向 C 端，**不具**舆论属性/社会动员能力（个人助手、学习辅导等） | 大模型算法备案信息 + 与阿里云的合作协议 |
| 面向 C 端，**具有**舆论属性/社会动员能力（社交媒体内容生成、舆情分析等） | 上述材料 + 企业自主安全评估报告 + 企业自主算法备案 |
| 企业内部使用 | 一般不直接适用暂行办法，但仍需关注数据安全内部合规 |

**备案主体信息**（技术主体为"服务技术支持者"）：

| 模型 | 算法名称 | 备案主体 | 备案号 |
| --- | --- | --- | --- |
| 千问 | 达摩院交互式多能型合成算法 | 阿里巴巴达摩院(杭州)科技有限公司 | 网信算备330110507206401230035号 |
| 万相（图像） | 达摩院图像合成算法 | 阿里巴巴达摩院(杭州)科技有限公司 | 网信算备330110507206401230027号 |
| 万相（视频） | 通义万相视频生成算法 | 通义云启（杭州）信息技术有限公司 | 网信算备330106003156001240091号 |

合作协议需包含算法名称/产品/备案编号相关内容，请联系商务经理获取。备案号请以 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index) 实时查询结果为准，建议定期核验。详见 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

> **注意**：即使使用了阿里云提供的模型与备案信息，应用开发者仍是法规定义的"服务提供者"，需独立履行内容审核、用户保护、数据安全、标识规范等全部法定义务。

## 接入模型备案信息公示

除千问、万相外，百炼接入的第三方模型也已公示算法备案号与大模型备案号，覆盖智谱 AI、DeepSeek、Moonshot、小米 MiMo、可灵 AI、MiniMax、阶跃星辰、Vidu、Tripo、PixVerse 等。完整清单见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：第三方模型的备案信息由提供方负责，阿里云百炼不作额外承诺，相关权利义务以《阿里云百炼服务协议》第 5.1.1.2 条、第 5.1.2 条为准。

## 安全存储业务空间

面向有私有网络数据隔离需求的用户，百炼提供**安全存储业务空间**（需联系商务开通）。整体流程：

1. 在百炼控制台创建安全存储类型的业务空间。
2. 在 VPC（华北2（北京），至少两个可用区）内创建**反向终端节点**并连接百炼。
3. 创建 MSE 云原生网关（2 核 4G，启用 TLS 硬件加速，私网类型），获取可用区 VIP 与交换机网段。
4. 在百炼侧配置可用区 IP，并把 MSE NLB 的 IP 加入反向终端节点安全组入方向白名单（端口 1/65535）。
5. 在 VPC 内配置私有资源：
   - **OSS**：创建 Bucket `bailian-safe-workspace-oss-access`（北京），打标签 `bailian-safe-workspace-oss-access=ReadAndWrite`，配置 CORS 来源 `*bailian.console.aliyun.com`，授权百炼访问。
   - **ADB（AnalyticDB PostgreSQL）**：购买 6.0 标准版高可用实例，开启向量引擎优化，授权角色 `AliyunServiceRoleForSFMAccessADB`。
   - **Elasticsearch**：7.10 内核增强版，双可用区，把交换机网段加入 ES 的 VPC 私网访问白名单。
6. 在 MSE 网关中创建 DNS 域名类型的服务与路由，把 ES 域名路由到后端。
7. 回到百炼确认 OSS / ADB / ES 配置无误后点击**激活**，空间状态变为可用。

> **注意**：OSS Bucket 或 ES 停止计费/被释放会导致安全存储空间、知识库、审计日志、历史记录等模块不可用甚至无法恢复，需要重新创建空间。

详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)、[配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)、[配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)、[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

## 限制与注意事项

- 业务空间**不能跨地域**；各地域的默认业务空间互相独立。
- 默认业务空间**无法**设置模型调用/训练/部署限制，所有模型均可调用；如需限流或禁用，必须创建自定义空间。
- 加密接入仅支持 DashScope Endpoint，OpenAI 兼容模式不支持。
- 私网访问在华北2（北京）与新加坡可用；美国（弗吉尼亚）暂不支持。
- AI 安全护栏目前覆盖文本和图片类模型，具体对应关系参见护栏服务文档。
- 第三方模型备案信息由模型提供方负责，使用前建议自行在备案系统核验。

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


