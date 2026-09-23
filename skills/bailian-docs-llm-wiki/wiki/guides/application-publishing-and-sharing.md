# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖嵌入式集成（组件）、多端触达（钉钉/微信/H5/APP）、实时音视频交互等场景。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离、权限与计费策略约束。开发者应根据目标集成方式选择对应发布路径，并严格遵循参数配置与调用规范。

## 支持的模型/功能

- **适用应用类型**：  
  - ✅ 智能体应用（**仅 Agent 1.0**）：支持全部发布渠道（魔笔 UI、钉钉、微信、组件、音视频实时互动）；  
  - ❌ 智能体应用（Agent 2.0）：**仅支持 API 调用**，不支持任何 UI 或渠道类分享功能 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)；  
  - ✅ 工作流应用：支持发布为组件、UI 应用、音视频实时互动（图文类），但**不支持钉钉/微信机器人发布**；  
  - ✅ UI 应用：仅支持通过魔笔 UI 设计器发布，可集成智能体或工作流作为后端能力 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

- **核心发布能力**：  
  - **UI 应用**：基于魔笔低代码平台生成 H5/PC 网页，支持自定义界面、数据库绑定与匿名访问控制；  
  - **渠道集成**：钉钉机器人（需配置卡片模板与 `Card.Streaming.Write` 权限）、微信公众号（需 AppID 授权）；  
  - **组件化复用**：将智能体或工作流发布为可被其他智能体/工作流引用的模块化组件，支持 `model recognition` 与 `biz param` 两种传参模式 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)；  
  - **音视频实时互动**：仅限图文对话类应用（智能体/工作流），提供 H5/APP 扫码体验与 SDK 集成两种接入方式。

> **注意**：文档 1 中称“音视频实时互动仅支持百炼的图文对话类应用（含智能体应用和工作流应用）”，而文档 3 的 UI 设计器章节未提及音视频能力；二者无冲突，因 UI 应用本身是独立前端容器，其后端可对接任意百炼应用（含音视频互动后端），但 UI 设计器**不直接提供音视频交互控件**，需通过 SDK 集成实现。

## 关键参数

| 参数 | 说明 | 约束与注意事项 |
|------|------|----------------|
| `API Key` | 调用百炼服务的身份凭证，必须与应用、UI 设计器处于**同一业务空间** | 未授权时 UI/钉钉/微信/音视频配置均失败；创建前需确认业务空间一致性 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |
| `query` / `imageList` | 组件预设系统参数，不可删除；`query` 为必填 String 类型，`imageList` 为可选 Array<String> 类型 | 若组件不处理图像，须将 `imageList` 的 **是否可见** 设为 `否`；否则可能引发空数组解析异常 |
| `传参方式`（业务透传 / 模型识别） | 决定参数值由调用方显式传入，还是由大模型从上下文自动推断 | **工作流中模型识别无效**：即使配置为“模型识别”，也必须由上游节点显式传值；仅智能体在 `model recognition` 模式下支持自动填充 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `回调地址`（钉钉） / `二维码`（微信） / `分享链接`（UI/音视频） | 渠道级访问入口，用于终端用户接入 | UI 开发环境链接**24 小时失效**；生产环境需订阅付费套餐并绑定域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |

## 使用方式

1. **前置检查**：确保目标应用已**发布成功**，且所属业务空间与 API Key、UI 设计器一致；  
2. **进入发布入口**：  
   - 智能体/工作流：在控制台应用详情页 → **发布渠道** 页签；  
   - UI 应用：在 [UI 设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) → **创建UI** 或 **环境部署**；  
3. **按渠道配置**：  
   - **UI 应用**：选择模板 → 绑定 API Key 与智能体/工作流 → 编辑界面 → 发布至开发/生产环境；  
   - **钉钉/微信**：完成第三方平台授权（SLR + API Key 传输）→ 获取并填写 `Client ID/Secret`、`模板 ID`（钉钉）或 `AppID`（微信）→ 复制回调地址或二维码；  
   - **组件**：在发布渠道页签点击 **+ 创建** → 填写组件名称/描述 → 配置 `query` 等参数的别名、可见性、传参方式 → **确定发布**；  
   - **音视频**：在 **AI实时互动** 页签 → 选择 API Key → 生成临时二维码测试 → 发布后开通智能媒体服务并授权 SLR；  
4. **验证与引用**：  
   - UI/渠道：扫码或访问链接测试交互；  
   - 组件：在新智能体的 **技能** 中选择，或在工作流画布中拖入 **组件节点** 并配置输入变量。

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用**完全不支持**魔笔 UI、钉钉、微信、组件、音视频等所有非 API 发布方式，该限制在 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中明确强调；  
- **嵌套与多级调用禁止**：组件 A 调用 B、B 又调用 A 将导致死循环；A→B→C 的三级调用易触发超时（百炼有全局最长运行时间限制），建议单层组件调用；  
- **工作流中模型识别失效**：文档 2 明确指出：“在工作流中引用该组件时，即使参数的传参方式设置为模型识别，应用也不会自动推断参数值”，必须显式传参；  
- **UI 开发环境时效性**：所有开发环境发布的 UI 地址**24 小时后自动失效**，生产环境需付费订阅；  
- **权限与计费隔离**：分享链接默认仅限阿里云用户访问；费用由应用创建者 UID 承担，包括模型调用、文件存储（1GB 免费）、数据库（0.3GB 免费）及生产环境订阅费 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；  
- **数据库表结构强校验**：UI 模板映射的数据库表若已存在，其字段类型、长度、主键等**必须与模板内置结构完全一致**，否则运行时报错。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


