# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节，帮助开发者满足《生成式人工智能服务管理暂行办法》等国内法规要求。所有能力均通过 API 参数、控制台配置和策略中心统一管理，无需修改业务代码即可启用。具体实现细节请参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 文档。

## 支持的模型/功能

以下安全与合规能力适用于所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及自定义微调模型：
- 输入/输出内容安全过滤（基于关键词、语义与多模态识别的 AI 安全护栏）
- TLS 1.2+ 传输加密与私网 VPC 访问支持
- 细粒度 RBAC 权限管理（含模型调用、日志查看、策略配置等权限项）
- 模型备案信息自动同步与应用级合规备案引导  
- 隐私数据处理说明与 GDPR/PIPL 兼容性声明  

> **注意**：私网访问配置仅支持华东1（杭州）、华北2（北京）、华南1（深圳）三地，其他地域暂未开放，详见 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) —— 注意该文档标题中“secure-storage”为历史命名错误，实际指代私网接入能力，与存储加密无关。

## 关键参数

调用模型 API 时，可通过以下请求头或参数启用对应能力：

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `x-bailian-security-level` | string | 安全等级：`basic`（基础过滤）、`strict`（强语义拦截）、`none`（关闭） | `basic` |
| `x-bailian-audit-log` | boolean | 是否强制记录输入/输出至审计日志（需开通日志服务） | `false` |
| `x-bailian-vpc-only` | boolean | 强制仅允许私网 VPC 内调用（需提前配置 VPC 白名单） | `false` |

完整参数说明见 [输入输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 使用方式

1. **启用内容安全过滤**：在 API 请求头中设置 `x-bailian-security-level: strict`，无需额外鉴权；  
2. **配置私网访问**：在控制台「安全设置 → 网络访问」中绑定 VPC 并开启 `x-bailian-vpc-only`；  
3. **完成应用备案**：首次发布生产环境 AI 应用前，须通过控制台「合规中心 → 应用备案」提交材料，流程说明见 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)；  
4. **查看模型备案信息**：所有已上线模型的备案编号、算法类型、训练数据范围等均实时公示于控制台「合规中心 → 模型备案信息」。

## 限制和注意事项

- 审计日志（`x-bailian-audit-log=true`）将额外产生日志存储费用，且日志保留期最长为 180 天；
- `strict` 安全等级可能误拦截低风险但语义模糊的合法输入（如技术术语缩写、方言表达），建议灰度验证；
- 权限策略变更后最长 5 分钟生效，期间可能出现策略延迟（参见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）；
- 模型备案信息公示依赖国家网信办备案系统同步，若控制台显示“待同步”，通常为 1–3 个工作日延迟，非平台故障。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


