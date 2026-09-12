# application permission management

应用权限管理用于控制不同用户或角色对百炼平台中模型应用的访问与操作权限，包括查看、调用、编辑和删除等能力。该机制基于阿里云RAM（资源访问管理）体系实现，支持细粒度的策略配置。开发者需结合应用部署模式（如API调用、Web UI嵌入）合理分配权限，避免越权访问或功能受限。

## 支持的模型/功能

- 支持所有在百炼平台托管的模型应用（含自定义微调模型、RAG应用、Agent工作流等）  
- 权限粒度覆盖：应用级读写、推理调用（`InvokeApplication`）、配置修改（`UpdateApplication`）、日志查看（`ListApplicationLogs`）及版本管理（`PublishApplicationVersion`）  
- 支持通过RAM角色、用户组或直接为RAM用户附加自定义策略，详见 [权限管理](../../raw/application-user-guide/application-permission-management.md) 中的策略模板说明  

## 关键参数

- `Resource`: 必须指定具体应用ARN，格式为 `acs:baichuan:cn-shanghai:<account-id>:application/<app-id>`；通配符 `*` 仅在全局管理员策略中允许使用  
- `Action`: 常用动作包括 `baichuan:InvokeApplication`、`baichuan:UpdateApplication`、`baichuan:ListApplications` 等，完整列表见 [权限管理](../../raw/application-user-guide/application-permission-management.md) 的“支持的Action”章节  
- `Condition`: 可选，支持基于请求上下文（如`acs:SourceIp`、`acs:SecureTransport`）添加限制条件，但不支持对`applicationId`做字符串匹配类条件判断  

## 使用方式

1. 登录[RAM控制台](https://ram.console.aliyun.com/) → 创建自定义策略（JSON格式）  
2. 将策略授权给目标RAM用户/用户组/角色  
3. 应用调用时，SDK或API请求自动携带对应身份凭证，权限校验由百炼服务端完成  
4. 推荐优先使用最小权限原则，例如仅授予`baichuan:InvokeApplication`而非`baichuan:*`；调试阶段可参考 [权限管理](../../raw/application-user-guide/application-permission-management.md) 提供的示例策略快速验证  

## 限制和注意事项

- 单个应用最多绑定100个RAM主体（用户/角色/用户组），超出需清理冗余授权  
- 权限变更后最长5分钟内生效（受RAM策略缓存影响）  
- **注意**：文档中提及的`baichuan:DeleteApplication`动作在v2.3.0+版本中已废弃，实际应使用`baichuan:ArchiveApplication`替代，该差异已在最新版 [权限管理](../../raw/application-user-guide/application-permission-management.md) 中修正，旧文档未同步更新  
- 不支持跨地域权限复用：华东1（杭州）创建的应用ARN无法在华北2（北京）直接授权，需分别配置  
- Web UI中“共享链接”生成的临时[Token](../concepts/token.md)不经过RAM权限系统，其访问控制独立于本机制，详见相关分享功能文档

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


