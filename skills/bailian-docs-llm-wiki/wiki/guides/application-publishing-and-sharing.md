# application publishing and sharing

百炼平台提供多种方式将智能体或工作流应用发布与共享，支持以组件形式复用、生成网页 UI 应用、集成至钉钉/微信等第三方平台，以及启用音视频实时互动能力。所有发布行为均基于已创建并发布的 Agent 1.0 应用（Agent 2.0 不支持除 API 外的任何分享渠道），且需确保应用、API Key 与 UI 设计器处于同一业务空间。核心能力围绕模块化、低代码和多端分发展开，面向开发者提供可组合、可配置、可灰度的交付路径。

## 支持的模型/功能

- **组件化复用**：智能体或工作流应用可发布为标准化组件，供其他智能体（作为工具）或工作流（作为节点）接入，实现跨应用能力复用。组件预设 `query`（String，必填）和 `imageList`（Array<String>，非必填）两个系统参数，分别用于文本指令与图像输入 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 应用发布**：通过可视化 UI 设计器，将智能体/工作流封装为网页应用，支持拖放式页面搭建、数据库映射、权限配置及一键发布至开发/生产环境 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **第三方平台集成**：支持发布至钉钉机器人、微信公众号、魔笔分享渠道（即 UI 应用）、以及音视频实时互动（H5/APP/SDK）四类渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **模型兼容性**：组件本身不绑定特定模型，但其底层智能体或工作流节点所用模型（如千问-Max-Latest、千问-Max）决定实际推理能力；UI 应用调用时，模型费用按实际 Token 消耗计费。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 传参方式约束 |
|--------|------|------|------|--------------|
| `query` | String | 是 | 用户自然语言输入，如“查询杭州天气” | 智能体中支持 `模型识别` 或 `业务透传`；工作流中仅支持 `业务透传`（即使配置为 `模型识别`，也必须显式传入） |
| `imageList` | Array<String> | 否 | 图像公网 URL 列表，仅当组件内部使用视觉模型时生效 | 同上，且需在参数配置中设为“是否可见=否”以隐藏（若组件不支持图像） |
| `biz_param` | Object | 否（按需） | API 调用时传递业务透传参数的顶层字段，结构为 `{ "param_name": "value" }` | 仅适用于 API 场景，不可用于 UI 或组件节点内联配置 |

> **注意**：文档 1 与文档 3 均明确指出，工作流中配置 `传参方式=模型识别` 对 `query` 等参数**无效**，必须由上游节点显式提供值；而文档 1 的“步骤四：接入组件到工作流应用”示例中未体现该强制传参逻辑，易引发误解。请以文档 3 的说明为准：工作流场景下，`模型识别` 仅为占位标识，无自动填充能力。

## 使用方式

1. **发布为组件**  
   - 进入智能体/工作流编辑页 → 点击「发布应用」→ 勾选「发布应用组件」→ 在弹窗中点击「立即发布」；或前往[组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) → 「+ 创建」→ 选择已有应用。  
   - 配置组件名称、描述、参数别名、是否可见、是否必填及传参方式（`业务透传` 或 `模型识别`）→ 确认发布。

2. **接入组件**  
   - **智能体中**：创建新智能体 → 在「技能」区域点击「+」→ 选择已发布组件 → 测试时若含 `业务透传` 参数，需在「入参变量配置」手动填写，或 API 调用时通过 `biz_param` 传入。  
   - **工作流中**：拖入「组件节点」→ 选择组件 → 在「输入」配置中，从变量菜单（如 `/系统变量/query`）显式绑定参数 → 连接上下游节点。

3. **发布为 UI 应用**  
   - 方式一（从已有应用）：应用发布页 → 「UI 应用」→ 「创建」→ 自动填充基础信息 → 编辑 UI → 发布至开发/生产环境。  
   - 方式二（从零设计）：进入[UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) → 「创建UI」→ 选模板 → 填写应用名、API Key、智能体 → 配置数据库映射 → 拖放组件编辑 → 右上角「发布」→ 获取访问链接。

4. **第三方渠道发布**  
   - **钉钉/微信**：应用发布页 → 「发布平台」页签 → 选择对应卡片 → 授权（首次需 SLR + API Key 加密传输）→ 配置凭据（Client ID/Secret、模板 ID、AppID）→ 获取回调地址或二维码 → 完成外部平台配置。  
   - **音视频互动**：应用「AI实时互动」页签 → 配置 API Key → 生成临时体验码（24 小时）→ 正式发布后开通智能媒体服务并完成 SLR 授权。

## 限制和注意事项

- **Agent 版本限制**：所有分享渠道（魔笔、钉钉、微信、组件、音视频）**仅支持 Agent 1.0**；Agent 2.0 应用仅可通过 API 调用，无法使用上述任何发布功能 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **业务空间一致性**：UI 设计器、API Key、智能体/工作流应用**必须归属同一业务空间**，否则无法关联或发布 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件调用风险**：  
  - 禁止 A 调用 B、B 再调用 A 的嵌套循环，会导致无限递归与服务不可用；  
  - 避免 A→B→C 的三级及以上调用链，因总运行时间受限，易触发超时错误 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境时效性**：开发环境发布的 UI 应用链接**24 小时后失效**，需重新发布；生产环境需订阅付费套餐并配置自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限与计费**：分享链接默认仅限阿里云用户访问，费用由应用创建者 UID 承担；匿名访问需在 UI 设计器中显式开启并配置权限组；模型调用、文件存储、数据库容量超出免费额度后按量计费。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)


