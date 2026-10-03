# security and compliance

百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储、内容安全及监管备案等关键环节，帮助开发者满足国内外主流合规要求（如 GDPR、中国《生成式人工智能服务管理暂行办法》）。所有能力均通过统一 API 接口或控制台配置生效，无需额外部署安全中间件。具体实现细节请参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 文档。

## 支持的模型/功能

以下安全与合规能力适用于所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型），但部分功能需模型版本 ≥ v2.3.0 才完全支持：
- 输入/输出内容安全过滤（基于关键词、语义与多模态风险识别）
- 私网 VPC 访问通道（仅限企业版实例）
- 模型调用级 RBAC 权限控制（支持细粒度 API Key 策略）
- 自动化模型备案信息公示（仅限已通过国家网信办备案的模型）

> **注意**：[私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) 文档标题存在误导——该文件实际描述的是**私网访问配置**，而非“安全存储”；正确的能力说明见 [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md) 中关于 TLS 1.3 和私有 endpoint 的章节。

## 关键参数

调用模型 API 时，可通过请求头或 query 参数启用对应安全能力：
- `X-Qwen-Security-Level: high`：启用增强内容过滤（默认为 `medium`）
- `X-Qwen-Private-Endpoint: true`：强制走私网通道（需实例已绑定 VPC）
- `X-Qwen-Compliance-Mode: cn-gov`：激活中国境内合规策略集（含敏感词库、备案字段校验等）

所有参数均为可选，未显式指定时采用租户级默认策略。完整参数定义见 [输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 使用方式

1. **控制台配置**：在「安全中心」→「合规策略」中设置全局默认安全等级与备案模式；
2. **API 调用**：在 `POST /v1/chat/completions` 等接口请求头中传入上述关键参数；
3. **权限隔离**：通过 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) 配置不同角色对「合规策略配置」、「备案信息查看」等操作的访问权限；
4. **备案集成**：应用上线前，须在「AI 应用管理」中完成 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，否则生产环境调用将被拦截。

## 限制和注意事项

- 私网访问仅支持华东 1（杭州）、华北 2（北京）和华南 1（深圳）地域，其他地域暂不支持；
- 内容安全过滤不支持自定义规则引擎，仅可切换预置策略等级（`low`/`medium`/`high`）；
- 模型备案信息公示页面由平台自动同步国家网信办数据，开发者不可编辑，但需确保所用模型版本已在公示列表中；
- 免费试用账号无法开启私网访问与高安全等级过滤，需升级至企业版；
- 所有安全策略变更（如修改默认 `Security-Level`）将在 5 分钟内全量生效，无热更新延迟。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


