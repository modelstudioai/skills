# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖终端用户触达（如微信、钉钉、H5）、能力复用（组件化）、实时音视频交互等场景。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离、权限与计费策略约束。开发者应根据目标集成方式选择对应发布路径，并严格遵循参数配置规范与调用限制。

## 支持的模型/功能

- **适用应用类型**：  
  - ✅ 智能体应用（**仅 Agent 1.0**）：支持全部发布渠道（魔笔 UI、钉钉、微信、组件、音视频实时互动）；  
  - ❌ 智能体应用（Agent 2.0）：**仅支持 API 调用**，不支持 UI、钉钉、微信、组件、音视频等任何分享渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)；  
  - ✅ 工作流应用：支持发布为组件、接入 UI 设计器、音视频实时互动（图文类），但**不支持钉钉/微信机器人发布**；  
  - ✅ UI 应用：基于魔笔低代码平台构建，可集成智能体或工作流作为后端能力 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

- **核心发布能力**：  
  - **UI 应用**：通过魔笔生成 H5 页面，支持开发/生产环境部署、匿名访问控制；  
  - **钉钉/微信机器人**：需完成开放平台授权（SLR + API-KEY）、模板 ID 与凭证配置；  
  - **组件化**：智能体或工作流可发布为可复用组件，供其他智能体（模型识别调用）或工作流（显式节点调用）引用；  
  - **音视频实时互动**：仅限图文对话类应用（智能体/工作流），提供 H5/APP 扫码体验与 SDK 集成两种模式 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

> **注意**：文档 1 明确限定“分享渠道均为 Agent 1.0 功能”，而文档 2 和文档 3 均未提及 Agent 2.0 的兼容性，但文档 1 的版本约束具有最高优先级。若尝试对 Agent 2.0 应用执行 UI/钉钉/微信/组件发布操作，控制台将不可见对应入口或报错。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用认证** | `API-KEY` | 调用百炼服务的密钥，必须与应用、UI 同属一个业务空间 | 必填；需提前在[同一业务空间](../../raw/model-api-reference/preparations/get-api-key.md)创建 |
| **钉钉配置** | `Client ID` / `Client Secret` / `模板 ID` | 从钉钉开放平台获取，用于机器人身份认证与消息卡片渲染 | `Card.Streaming.Write` 和 `Card.Instance.Write` 权限必须申请并生效 |
| **微信配置** | `AppID`（开发者ID） | 微信公众号后台「基本配置」中获取 | 仅支持服务号/企业微信（文档未明确，但流程依赖公众号后台） |
| **组件参数** | `query` / `imageList` | 预设系统参数，`query` 为必填 String 类型，`imageList` 为可选 Array<String> 类型 | 不可删除；可通过“是否可见”隐藏非必需参数 |
| **UI 配置** | `数据库表映射` | 模板自带表（如 `kb_chat_list`）需结构完全一致，否则运行时报错 | 使用已有表前必须校验字段类型与数量 |

## 使用方式

1. **前置条件**：  
   - 应用已完成构建并**已发布**（非草稿状态）；  
   - 所有资源（API-KEY、智能体、UI）必须位于**同一业务空间** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；  
   - 钉钉/微信首次使用需完成计算巢 AppFlow 授权（SLR + API-KEY 加密传输）。

2. **操作路径**：  
   - **UI 应用**：应用管理 → 目标应用 → **发布渠道** → **UI应用** → 创建 → 编辑 → 发布至开发/生产环境；  
   - **钉钉/微信**：应用管理 → 目标应用 → **发布平台** → 选择渠道 → 完成授权与凭证配置 → 获取回调地址/二维码；  
   - **组件**：应用管理 → 目标应用 → **发布渠道** → **组件** → 填写名称/描述/参数（含别名、传参方式、是否必填）→ 确定发布；  
   - **音视频互动**：应用管理 → 目标应用 → **AI实时互动** → 选择语音/视频 → 配置 API-KEY → 生成体验链接 → 发布并开通智能媒体服务。

3. **组件接入**：  
   - **智能体中引用**：在技能配置中选择已发布组件；大模型依据组件描述与上下文自动触发（`模型识别`传参方式）；  
   - **工作流中引用**：拖入“组件节点”，手动连接上游节点并指定输入变量（如 `系统变量/query`）；`模型识别`在此场景下**无效**，必须显式传参。

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用**完全不支持**除 API 外的任何发布方式，该限制优先于所有其他文档描述 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **组件调用风险**：  
  - ❌ 禁止嵌套调用（A→B→A），将导致无限循环；  
  - ⚠️ 多级调用（A→B→C）易超时，建议单跳深度 ≤2；  
  - ✅ 组件更新自动同步：原应用重新发布后，所有引用该组件的智能体/工作流将立即使用新逻辑。  
- **环境与有效期**：  
  - UI 开发环境链接**24 小时失效**，生产环境需订阅付费套餐；  
  - 音视频临时体验二维码**24 小时失效**；  
  - 钉钉/微信机器人回调地址长期有效，但需确保钉钉应用版本已发布且机器人已启用。  
- **权限与计费**：  
  - 分享链接默认仅限阿里云用户访问，可通过 UI 设计器配置匿名访问权限；  
  - 所有调用产生的模型费用由应用创建者 UID 承担；  
  - UI 生产环境发布、数据库/文件存储超出免费额度需额外付费 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


