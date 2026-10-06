# 安全防护

安全防护是百炼平台内生、分层、可编排的防御能力体系，面向 Agent 全生命周期（开发、运行、数据、记忆、生态）提供默认启用的内容检测、行为隔离与风险审计能力，形成「量 → 挡 → 记」闭环：自动度量风险、实时拦截高危操作、完整记录事件链路，无需开发者手动集成即可获得基础防护。

## 在百炼平台的不同场景中，这个概念如何使用

安全防护不是单一功能模块，而是按防护对象与阶段深度融入各核心场景：

- **Flow Agent**：输入/输出内容自动触发默认内容安全检测（涉黄、涉政、广告等），拦截违规文本；高级防护可开启「提示词攻击」策略，识别 jailbreak、越狱指令等对抗性输入。
- **Managed Agent**：运行时默认启用沙箱隔离、工具调用拦截（如禁止 `rm -rf /`）、凭证隔离与 Session 生命周期治理；高级防护中「工具调用安全」策略可监测异常工具组合调用模式并告警。
- **RAG 应用**：知识库上传文件时默认预扫描（病毒、恶意宏、敏感信息），索引构建与检索过程默认检测内容投毒风险；高级防护「RAG 数据投毒」策略提供细粒度语义级投毒识别与溯源。
- **Memory 与 Store**：记忆读写、技能（Skill）包上传、MCP 组件注册均默认执行内容安全检测；高级防护「知识库与记忆窃取」「身份与安全凭证」策略可识别越权访问、凭证硬编码等风险行为。
- **模型调用与传输**：通过 `X-DashScope-DataInspection` 头启用 AI 安全护栏，对输入输出做合规检查；支持 AES+RSA 混合加密传输，保障敏感数据在公网链路中的机密性——此属传输层安全能力，与运行时防护协同构成纵深防御。

> ✅ 关键原则：**默认防护随模块使用自动生效，零配置；高级防护需授权开通，全局生效，仅监测告警，不自动阻断。**

## 关键参数和配置

| 参数 | 类型 | 说明 | 开启方式 |
|------|------|------|----------|
| `risk_level` | string | 风险等级（`high`/`medium`/`low`），由置信度与危害联合判定，用于告警筛选与处置优先级 | 所有告警接口返回字段（如 `/agent_logs`） |
| `Credit` | integer | 高级防护用量单位（1 Credit ≈ 对应 [Token](token.md) 量的内容检测），每日每席位默认 300 Credits | 控制台 **Security > 高级防护 > 配额管理** 查看与调整 |
| `seat`（席位） | — | 启用高级防护且处于运行状态的 Agent 实例数；停用或未启用不计费 | 自动统计，控制台 **Security > 高级防护 > 使用概况** 可见 |
| `X-DashScope-DataInspection` | HTTP Header | 启用 AI 安全护栏（如 `{"input":"cip","output":"cip"}`），独立于平台默认防护 | 调用模型 API 时显式传入 |
| `enable_encryption` | bool（SDK） | 启用端到端传输加密（AES+RSA），保护 `input` 字段 | SDK 中设置（如 Python `Generation.call(enable_encryption=True)`） |

> ⚠️ 注意：  
> - 高级防护策略（如「敏感数据外泄」「身份凭证」）**仅输出告警，不自动拦截请求或终止 Agent**；拦截动作由默认防护中的内容检测、沙箱机制等底层能力完成。  
> - `X-DashScope-DataInspection` 是模型服务层能力，与平台层安全防护正交，可叠加使用。  
> - 所有高级防护策略配置对**账号下全部 Agent 全局生效**，不区分业务空间。

## 面向开发者，简洁实用

- **快速验证防护是否生效**：  
  ```bash
  # 查看最近24小时拦截统计（含默认防护）
  bl agents security overview

  # 查询高风险告警（高级防护产出）
  bl agents security alerts --risk-level high
  ```

- **API 集成告警流**：  
  调用 `/api/v1/agentstudio/security/agent_logs?risk_level=high&order_by=check_time&order=desc` 获取实时告警列表，响应含 `alert_id`、`risk_domain`（如 `prompt_attack`）、`details`（风险上下文）等关键字段。

- **导出全量告警用于 SOC 分析**：  
  先 POST `/export_agent_logs` 提交任务（注意 `params` 字段需为 **PascalCase 字符串化 JSON**），再 GET `/export_status?export_id=xxx` 轮询下载链接。

- **生产环境必做三件事**：  
  1. **禁用默认业务空间**：新建独立业务空间，避免权限失控；  
  2. **开通高级防护并启用关键策略**：如「提示词攻击」「敏感数据外泄」，及时发现新型风险；  
  3. **为敏感 Agent 配置私网访问 + 传输加密**：双重保障数据链路安全（PrivateLink + `enable_encryption`）。

安全防护的目标不是增加复杂度，而是让安全成为平台的“空气”——你感知不到它的存在，但离开它就无法呼吸。

## 关联主题页

- [security guide](../guides/security-guide.md)
- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)
- [managed agents](../guides/managed-agents.md)


