# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖终端用户触达（如钉钉、微信、H5/APP）、能力复用（组件化）和低代码集成（UI 设计器）三大场景。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离及权限模型约束。本文档面向开发者，聚焦可操作的核心能力、参数含义与关键限制。

## 支持的模型/功能

- **Agent 版本限定**：魔笔分享渠道、钉钉、微信、UI 应用、音视频实时互动等发布方式**仅支持 Agent 1.0 智能体应用**；Agent 2.0 仅支持 API 调用，不支持上述任何分享渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **应用类型支持**：
  - 智能体应用（Agent 1.0）：支持全部四类发布方式（魔笔/UI、钉钉、微信、组件、音视频）；
  - 工作流应用：支持发布为组件、接入 UI 应用、音视频实时互动（图文类）；
  - UI 应用：由 UI 设计器构建，可独立发布为 H5/APP 页面，亦可嵌入企业门户 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化能力**：智能体或工作流应用均可发布为可复用组件，供其他智能体或工作流引用，实现功能模块解耦与复用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 1 中称“音视频实时互动仅支持图文对话类应用（含智能体应用和工作流应用）”，而文档 3 的 UI 设计器章节未提及音视频能力；二者无直接冲突，但需明确音视频发布入口位于智能体/工作流的 **AI实时互动** 页签，而非 UI 设计器内。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用认证** | API Key | 所有对外发布渠道（钉钉、微信、UI、音视频）均需绑定有效的 API Key；必须与目标应用同属一个业务空间 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) | 不可跨业务空间复用；需提前在[我的API-KEY](https://bailian.console.aliyun.com/?tab=app#/api-key)中创建 |
| **钉钉配置** | 钉钉 Client ID / Client Secret / 模板 ID | 用于对接钉钉开放平台；模板 ID 必须关联已申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限的应用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) | 模板 ID 需在钉钉卡片平台创建并发布后获取；权限需手动申请 |
| **微信配置** | 开发者ID（AppID） | 微信公众号后台获取的基本凭证；授权后用于生成客服二维码 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) | 仅支持服务号/订阅号，不支持小程序 |
| **组件参数** | `query`, `imageList` | 预设系统参数，不可删除；`query` 为必填 String 类型，`imageList` 为非必填 Array<String> 类型 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) | 若组件无需图像输入，应将 `imageList` 的“是否可见”设为否 |
| **传参方式** | `业务透传` / `模型识别` | 决定参数值来源：`业务透传` 由调用方显式提供；`模型识别` 仅在智能体中生效（大模型自动填充），**在工作流中无效**，必须显式传入 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) | 此处存在关键逻辑差异：工作流中无论配置为何种传参方式，均需上游节点明确赋值 |

## 使用方式

1. **UI 应用发布**  
   进入应用「发布渠道」页签 → 选择「UI应用」→ 创建 → 自动填充基础信息（API Key、智能体、图标等）→ 发布至开发环境（24小时有效）或生产环境（需订阅套餐）→ 获取应用地址分享 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **钉钉/微信发布**  
   在「发布平台」页签 → 授权计算巢 AppFlow（首次需 SLR + API-KEY 加密传输）→ 选择对应渠道卡片 → 配置凭证（Client ID/Secret/模板 ID 或 AppID）→ 获取回调地址（钉钉）或二维码（微信）→ 完成外部平台配置（如钉钉机器人 HTTP 回调、微信公众号客服绑定）。

3. **发布为组件**  
   在「发布渠道」页签 → 「组件」区域点击「+ 创建」→ 填写组件名称、描述 → 配置输入参数（别名、描述、是否必填/可见、传参方式、默认值）→ 确定发布 → 在其他智能体（技能中选择）或工作流（拖入组件节点）中引用。

4. **音视频实时互动**  
   在「AI实时互动」页签 → 选择语音/视频 → 配置 API Key → 生成临时体验二维码（24小时）→ 测试通过后发布 → 开通智能媒体服务并授权 SLR → 选择 H5/APP 分享或 SDK 集成（WEB/IOS/安卓）。

## 限制和注意事项

- **Agent 版本强约束**：Agent 2.0 应用完全不支持魔笔、钉钉、微信、UI、音视频等发布方式，仅可通过 API 调用；此限制在多个文档中一致强调，是首要兼容性检查项 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），会导致无限循环；  
  - 多级调用（A→B→C）易触发超时（因应用有最长运行时间限制）；  
  - 组件发布后自动随源应用更新，需注意版本一致性 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境与权限隔离**：UI 应用、API Key、智能体/工作流必须归属同一业务空间，否则无法在 UI 设计器中下拉选择 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **开发环境时效性**：UI 应用开发环境链接有效期为 24 小时，过期需重新发布；生产环境需订阅付费套餐并配置自定义域名。
- **计费责任归属**：所有通过分享链接产生的模型调用费用，均由应用创建者 UID 账号承担，与访问者身份无关 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


