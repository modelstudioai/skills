# Agent 资产

盘点当前业务空间内由百炼纳管的 Agent 及其关联资源，帮助识别安全防护对象，了解 Agent 的潜在攻击面与风险影响范围。

## 页面入口

在控制台导航栏点击 **Security**，左侧菜单选择 **默认防护 > Agent 资产**，进入 Agent 资产页面。

## 功能说明

Agent 资产页面展示当前业务空间内由百炼纳管的原生或托管 Agent，以及与这些 Agent 关联的模型、工具、知识库、记忆等资源。通过资产关系可查看 Agent 的组成、防护状态和风险关联情况。目前安全纳管的 Agent 包括 Flow Agent 和 Managed Agent 两大类，更多详情参见本章[统计规则](#h-security-assets-rules)一节。

**说明**尚未接入百炼纳管范围的外部 Agent，不会被自动识别为页面资产。当前版本暂不支持点击下钻查看 Agent 列表与节点详情，后续版本将提供。

## 页面指标

指标

释义

**Agent 数**

当前业务空间内的 Agent 数量

**身份数**

当前业务空间内已登记身份的 Agent 数量

**模型数**

与 Agent 建立关联关系的模型数量

**工具数**

与 Agent 建立关联关系的工具数量，包括内置插件、自定义 API/connector、MCP tool

**技能数**

与 Agent 建立关联关系的 Skill 数量

**知识库数**

与 Agent 建立关联关系的知识库数量

**记忆数**

与 Agent 建立关联关系的记忆资源数量

**渠道数**

与 Agent 建立关联关系的渠道数量

## 统计规则

纳入统计的 Agent 及相关节点按以下逻辑盘点：

Agent 类型

统计范围

**Flow Agent**

草稿态 + 发布态下的 Agent 及 Agent 节点。同一 Agent 同时存在草稿态与发布态时，仅统计发布态

**Managed Agent**

发布态 + 归档态下的 Agent 及 Agent 节点

**说明**Agent 运行后，系统会对相关内容自动执行异步安全检测。

## 相关页面

-   [防护总览](raw/application-user-guide/security-guide/section-assets/overview.md)：查看防护全景与拦截统计
-   [安全策略](raw/application-user-guide/security-guide/section-adv/policy.md)：按需启用高级防护策略
