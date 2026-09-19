# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖终端用户触达（如钉钉、微信、H5/APP）、能力复用（组件化）、实时音视频交互等场景。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离、权限与计费策略约束。本文档面向开发者，聚焦可操作的核心能力与关键限制。

## 支持的模型/功能

- **Agent 版本兼容性**：仅 **Agent 1.0** 智能体应用支持魔笔分享渠道、钉钉、微信、UI 应用、音视频实时互动及组件发布；**Agent 2.0 应用不支持上述任何分享渠道，仅可通过 API 调用** [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **支持的应用类型**：
  - 智能体应用（Agent 1.0）
  - 工作流应用（任务型/对话型）
  - UI 应用（基于魔笔低代码平台构建）
- **核心共享能力**：
  - **渠道分发**：魔笔分享链接、钉钉机器人、微信公众号客服、H5/APP 扫码体验、SDK 集成（音视频实时互动）；
  - **能力复用**：发布为可被其他智能体或工作流引用的模块化组件；
  - **界面交付**：通过 UI 设计器生成网页应用，支持开发/生产环境部署与自定义域名绑定 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：文档 1 明确限定“分享渠道均为 Agent 1.0 功能”，而文档 2 和文档 3 均未提及 Agent 2.0 的共享能力，与文档 1 一致。但文档 2 中“步骤一：创建应用”示例使用了 `千问-Max-Latest` 模型，该模型通常关联 Agent 2.0，此处存在潜在矛盾——实际发布组件前必须确保底层应用为 Agent 1.0，否则组件创建将失败。请以[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)中 Agent 版本说明为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用认证** | API Key | 用于调用百炼服务的身份凭证，必须与应用、UI 设计器处于同一业务空间 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) | 必填；需提前在控制台创建并授权 |
| **钉钉集成** | 钉钉 Client ID / Client Secret / 模板 ID | 用于配置钉钉机器人及卡片消息流式返回 | 需在钉钉开放平台创建应用并申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限 |
| **微信集成** | 微信 AppID（开发者ID） | 用于绑定微信公众号凭据 | 需在微信公众号后台「设置与开发 > 开发接口管理」获取 |
| **组件参数** | `query`, `imageList` | 系统预设参数，不可删除；`query` 为必填 String 类型，`imageList` 为非必填 Array<String> 类型 | `imageList` 仅在组件使用视觉模型时生效；隐藏参数需设 `是否可见 = 否` |
| **UI 应用** | 自定义域名、数据库表映射 | 生产环境需绑定域名；部分模板自动创建数据库表，结构必须严格匹配 | 使用已有表时若结构不一致将导致运行时错误 |

## 使用方式

1. **前提条件**：目标应用（智能体或工作流）必须已完成构建并**已发布**；API Key 与应用须归属同一业务空间。
2. **入口统一**：所有发布操作均从百炼控制台 **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** 页面进入，点击目标应用卡片的 **发布** 按钮。
3. **按渠道操作**：
   - **魔笔/UI 应用**：在“UI 应用”页签创建 → 编辑 UI → 发布至开发/生产环境 → 获取应用地址分享；
   - **钉钉/微信**：在“发布平台”页签完成授权 → 配置凭证（Client ID/Secret、AppID、模板 ID）→ 获取回调地址或二维码；
   - **组件**：在“发布渠道”页签 → “组件”区域点击 **+ 创建** → 配置名称、描述、参数（别名、传参方式、是否可见等）→ 确定发布；
   - **音视频实时互动**：在“AI 实时互动”页签 → 配置 API Key → 生成临时二维码或发布至 H5/APP/SDK；
4. **组件接入**：
   - **智能体中引用**：在技能配置中选择已发布组件；大模型根据组件描述与上下文自动触发（`模型识别`传参）或由用户/调用方提供输入（`业务透传`）；
   - **工作流中引用**：拖入“组件节点” → 选择组件 → 手动连接上游节点并指定输入变量（工作流**不支持** `模型识别` 自动填充，必须显式传参） [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用无法使用除 API 外的任何发布渠道，尝试操作将无响应或报错。
- **组件调用风险**：
  - **禁止嵌套调用**（A→B→A）：导致无限循环，服务不可用；
  - **慎用多级调用**（A→B→C）：受最长运行时间限制，易超时失败；
  - **组件自动更新**：源应用重新发布后，所有引用该组件的实例将同步更新，需充分测试兼容性。
- **环境与有效期**：
  - UI 应用开发环境链接**24 小时失效**，生产环境需订阅付费套餐并配置域名；
  - 音视频实时互动临时二维码有效期为 **24 小时**；
  - 所有分享链接默认仅对**持有链接的阿里云用户**开放，费用由创建者 UID 账号承担。
- **权限与配额**：
  - 钉钉/微信首次授权需同意 SLR 关联及 API-Key 加密传输；
  - UI 设计器使用文件存储（1GB 免费）和数据库（0.3GB 免费），超额按量计费；
  - 工作流中使用 `imageList` 参数时，必须确保组件底层模型支持视觉理解能力，否则参数被忽略。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


