# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖终端用户触达（如微信、钉钉、H5）、能力复用（组件化）、实时音视频交互等场景。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离、权限与计费策略约束。开发者应根据目标集成方式选择对应发布路径，并严格遵循参数配置规范与调用限制。

## 支持的模型/功能

- **适用应用类型**：  
  - ✅ 智能体应用（**仅 Agent 1.0**）：支持全部发布渠道（魔笔 UI、钉钉、微信、组件、音视频实时互动）；  
  - ❌ 智能体应用（Agent 2.0）：**仅支持 API 调用**，不支持 UI、钉钉、微信、组件、音视频等任何分享渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)；  
  - ✅ 工作流应用：支持发布为组件、接入 UI 设计器、音视频实时互动（图文类）；  
  - ✅ UI 应用：基于魔笔低代码平台构建，可独立发布至开发/生产环境，支持匿名访问与权限组控制 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

- **核心发布能力**：  
  - **UI 应用**：通过可视化拖拽构建网页界面，绑定智能体或工作流，一键发布至开发环境（24 小时有效期）或生产环境（需订阅套餐）；  
  - **第三方平台集成**：钉钉机器人（需配置 Client ID/Secret、模板 ID 及 `Card.Streaming.Write` 权限）、微信公众号（需 AppID 授权）；  
  - **组件化复用**：将智能体或工作流发布为可被其他智能体/工作流引用的模块，预设 `query` 和 `imageList` 系统参数；  
  - **音视频实时互动**：支持 H5/APP 扫码体验与 SDK 集成（WEB/iOS/Android），适用于语音/视频对话类应用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

> **注意**：文档 1 明确限定“魔笔分享渠道、钉钉、微信、组件、音视频实时互动”均为 Agent 1.0 功能；而文档 2 在“步骤一：创建应用”中未强调版本限制，且示例中混用“千问-Max-Latest”（属 Agent 2.0 常用模型），易引发混淆。实际开发中，**必须使用 Agent 1.0 应用才能完成组件发布与第三方平台发布**，Agent 2.0 应用仅可通过 API 调用，不可发布为组件或接入钉钉/微信。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用认证** | API Key | 调用百炼服务的凭证，必须与应用、UI 同属一个业务空间 | 必填；需提前在[API Key 管理页](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 |
| **钉钉配置** | Client ID / Client Secret / 模板 ID | 从钉钉开放平台获取，用于身份认证与卡片消息渲染 | 模板 ID 必须关联已申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限的应用 |
| **微信配置** | AppID（开发者 ID） | 微信公众号后台「设置与开发 > 开发接口管理」中获取 | 必填；需完成微信公众号授权流程 |
| **组件参数** | `query`（String, 必填）<br>`imageList`（Array<String>, 非必填） | 预设系统参数，分别传递文本输入与图像 URL 列表 | 不可删除；可通过“是否可见”隐藏；`imageList` 仅在启用多模态模型时生效 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| **组件传参** | 传参方式（业务透传 / 模型识别） | 决定参数由调用方显式提供，还是由大模型从上下文推断 | 工作流中**不支持模型识别**，必须通过上游节点显式传入 |

## 使用方式

1. **前置条件**：  
   - 应用已完成构建并**已发布**（非草稿状态）；  
   - 所有资源（应用、API Key、UI）必须位于**同一业务空间**；  
   - 钉钉/微信首次集成需完成 SLR 角色授权与 API Key 加密传输授权。

2. **操作路径**（统一入口）：  
   - 进入百炼控制台 → **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** → 找到目标应用 → 点击卡片右上角 **发布** 按钮 → 切换至对应页签（如“发布平台”、“AI实时互动”、“UI应用”、“组件”）。

3. **典型流程**：  
   - **UI 应用**：选择“UI应用” → 创建 → 编辑界面 → 发布至开发环境（即时可用）或生产环境（需绑定域名+付费套餐）；  
   - **钉钉/微信**：在“发布平台”页签 → 授权 → 选择/创建 API Key → 填写平台凭证 → 获取回调地址（钉钉）或二维码（微信）→ 在对应平台完成机器人/公众号配置；  
   - **组件**：在“发布渠道”页签 → “组件”区域点击“+ 创建” → 填写名称/描述 → 配置 `query`/`imageList` 等参数（含别名、是否必填、传参方式）→ 确定发布 → 在其他智能体（技能区）或工作流（组件节点）中引用；  
   - **音视频互动**：在“AI实时互动”页签 → 配置 API Key → 生成临时二维码测试 → 发布 → 完成智能媒体服务开通与 SLR 授权 → 选择 H5/APP 分享或 SDK 集成。

## 限制和注意事项

- **Agent 版本硬性限制**：Agent 2.0 应用**完全不支持**除 API 调用外的任何发布方式，该限制贯穿所有渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)；  
- **组件调用风险**：  
  - ❌ 禁止嵌套调用（A → B → A），将导致无限循环与功能失效；  
  - ⚠️ 多级调用（A → B → C）易触发超时（默认最长运行时间限制），建议控制在 2 层以内；  
- **工作流中组件参数**：即使配置为“模型识别”，工作流也**不会自动推断参数值**，必须由上游节点显式传入，此行为与智能体场景不同 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)；  
- **UI 环境时效性**：开发环境发布的 UI 地址**24 小时后自动失效**，需重新发布；生产环境需订阅付费套餐并配置自定义域名；  
- **计费归属**：所有通过分享链接产生的模型调用费用，均由**应用创建者 UID 账号承担**，与访问者身份无关；  
- **权限隔离**：UI 应用默认仅限阿里云用户访问；如需开放给匿名用户，须在 UI 设计器中显式开启“允许匿名访问”并配置权限组 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


