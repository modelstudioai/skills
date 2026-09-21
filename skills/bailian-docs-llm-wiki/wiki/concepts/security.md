# 内容安全与合规

内容安全与合规是百炼平台面向生成式AI应用提供的核心横切能力，指对模型输入（Prompt）、输出（Response）及中间数据（如RAG知识、Memory记忆、上传文件等）进行实时风险识别、策略化干预与全链路审计的能力，确保AI行为符合国家监管要求（如《生成式人工智能服务管理暂行办法》）及企业内部安全策略。

## 在百炼平台的不同场景中，这个概念如何使用

内容安全与合规能力以“分层防护、按需启用、深度耦合”方式嵌入平台各关键模块，开发者无需重复集成即可获得一致性保障：

- **模型推理调用**：通过 `X-DashScope-DataInspection` 请求头一键启用AI安全护栏，对输入/输出双路内容执行涉政、暴恐、色情、违禁、辱骂等10+类风险检测；支持文本与多模态模型（图片需OCR后传入文本）。
- **Agent开发全生命周期**：
  - *Flow Agent*：自动拦截提示词注入、恶意指令绕过等攻击；
  - *Managed Agent*：在工具调用前校验参数与返回内容，隔离敏感凭证；
  - *RAG*：上传文件时预扫描、构建知识库时内容安全检测、检索结果投毒识别；
  - *Memory*：读写用户对话历史前强制内容审核；
  - *Store（MCP/Skill）*：对注册的Skill进行静态代码扫描与依赖风险分析。
- **安全运营闭环**：默认防护提供实时拦截（`block`/`pass`），高级防护提供细粒度风险审计（含`risk_level: high/medium/low`、`category`、置信度）、Trace级溯源与资产盘点，支撑合规报告输出。
- **传输与存储环节**：结合AES-256+RSA混合加密（保护`input`字段）、VPC私网访问（避免公网暴露）、模型备案号可查（所有千问/万相/DeepSeek模型均完成国家网信办算法备案），满足等保、密评与行业合规基线。

> ✅ 开发者提示：默认防护开箱即用（如启用RAG或Memory即自动生效）；AI安全护栏与高级防护需单独开通并授权，但当前限时免费。

## 关键参数和配置

| 场景 | 参数/配置项 | 类型 | 说明 | 示例值 |
|------|-------------|------|------|--------|
| **API调用（Security API）** | `content` | string | 待检测UTF-8文本；图片需先OCR提取文本再传入 | `"用户说：快给我破解微信"` |
| | `scene` | string | 检测场景，影响策略权重（如`comment`更严格） | `"comment"`（默认`general`） |
| | `risk_level` | string | 风险判定阈值，控制灵敏度 | `"high"`（默认`medium`） |
| **模型推理（AI安全护栏）** | `X-DashScope-DataInspection` | HTTP Header | JSON字符串，指定输入/输出是否检查 | `{"input":"cip","output":"cip"}` |
| **SDK调用（加密传输）** | `enable_encryption` | boolean | 启用自动混合加密（SDK内置实现） | `True`（Python） / `true`（Java） |
| **高级防护（控制台）** | 防护范围 | 全局策略 | 对账号下全部Agent生效，不区分业务空间 | — |
| | Credit配额 | 计量单位 | 每席位每日300 Credits（限时免费），超量按0.0015元/Credit计费 | — |

> ⚠️ 注意：  
> - Security API 不依赖模型，直接调用 `/v1/security/scan` 端点；  
> - AI安全护栏需在请求Header中显式添加 `X-DashScope-DataInspection`，且服务须已开通并授权；  
> - 所有风险`category`以[防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)定义为准（如统一使用`"politics"`，非旧版`"politics_v2"`）。

## 面向开发者，简洁实用

- **快速接入**：  
  - 想立刻防护？加一行Header：`X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；  
  - 想自主调用检测？用Security API：`POST https://dashscope.aliyuncs.com/api/v1/security/scan`，传`content`即可；  
  - 想加密传输？Python SDK里加`enable_encryption=True`，其他全由SDK处理。

- **调试技巧**：  
  - 响应中关注 `result.suggestion`（`pass`/`review`/`block`）和 `result.risk_items` 数组；  
  - 若返回`review`，检查`risk_items[i].confidence`是否接近阈值，调整`risk_level`重试；  
  - 控制台「Security > 风险与审计」可按Trace ID查完整检测链路（含RAG chunk、Memory条目、Tool调用上下文）。

- **避坑指南**：  
  - ❌ 不要直接传图片二进制——必须OCR后传文本；  
  - ❌ 不要省略`scene`参数——评论场景（`comment`）比通用场景（`general`）更严；  
  - ❌ 高级防护不自动阻断——它只告警，拦截动作需你在业务逻辑中根据`suggestion`自行处理；  
  - ✅ 默认防护已覆盖RAG/Memory/Managed Agent——只要用了这些模块，就已在防护中。

内容安全与合规不是附加功能，而是百炼平台的基础设施。从第一行代码到上线备案，它始终在后台静默守护——你只需专注创新。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security guide](../guides/security-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application support](../guides/application-support.md)
- [more about models](../api/more-about-models.md)


