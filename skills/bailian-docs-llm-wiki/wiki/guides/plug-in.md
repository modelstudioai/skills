# plug in

插件是扩展大模型能力的关键机制，用于弥补其在实时信息获取、精确计算、外部系统交互等方面的固有局限。百炼平台支持官方插件、三方插件和自定义插件三类，覆盖从开箱即用到深度定制的全场景需求。所有插件均以“工具”为最小可调用单元，通过标准化接口与大模型协同完成复杂任务。

## 支持的模型/功能

当前明确支持插件调用的模型为：**通义千问-Plus（`qwen-plus`）** 和 **通义千问-Max（`qwen-max`）**。其他模型的兼容性未在文档中确认，实际使用请以控制台执行结果为准 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：预置于组件广场，免配置即用，包括 `code_interpreter`（Python代码解释器）、`calculator`（计算器）、`text_to_image`（图片生成）、`quark_search`（夸克搜索）、`generate_qrcode`（生成二维码）、`github_search`（GitHub搜索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用。
- **自定义插件**：用户自主创建或从云市场导入，支持完全自定义 API 路径、鉴权方式、输入/输出参数及高级调用示例 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 3 中对官方插件列表的描述完全一致，但文档 3 明确指出“各模型对插件的兼容性可能有差异”，而文档 1 未提及其他模型支持情况；文档 2 未列出任何模型支持范围。因此，`qwen-plus` 和 `qwen-max` 是当前唯一经文档交叉验证的支持模型。

## 关键参数

- **工具 ID（tool_id）**：全局唯一标识符，用于 API 调用时指定目标工具。可在插件详情页的“插件工具”区域或工具卡片悬停图标处获取 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数（input parameters）**：
  - `传参方式`：分为 **大模型识别**（从用户输入中抽取）和 **业务透传**（由外部系统通过 `biz_params` 或 `user_defined_params` 传入）；
  - `类型`：支持 `String`、`Number`、`Object` 等，`Object` 类型下子属性不可为空；
  - `必填`：必须显式声明，否则发布失败。
- **输出参数（output parameters）**：所有参数均为必填项，大模型依据其定义对 API 响应进行结构化提取与重组。
- **鉴权配置**（仅自定义插件）：支持 `Header` 或 `Query` 位置，`Type` 可选 `basic`/`bearer`/`appcode`，`Token` 为服务级凭据；用户级鉴权需在对话前手动配置 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 使用方式

1. **控制台集成（推荐入门）**：
   - 官方/三方插件：访问 [插件市场](https://bailian.console.aliyun.com/#/plugin-market)，单击 **添加至智能体** → 选择目标智能体 → 确认添加。最多支持 10 个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页面的 **MCP 区块** 中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

2. **API 集成**：
   - Assistant API：在请求体 `tools` 字段中传入工具定义（含 `function.name`、`description`、`parameters`），并确保 `model` 指定为 `qwen-plus` 或 `qwen-max`；
   - 工作流应用：将插件作为独立节点拖入画布，配置输入/输出映射；
   - DashScope SDK：通过 `tools` 参数传递工具列表，业务透传参数需置于 `biz_params`。

3. **权限准备（必需前置步骤）**：
   - 主账号：首次访问插件市场时，需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；
   - RAM 子账号：须由主账号授予 `ram:CreateServiceLinkedRole` 权限（带 `cloundapi-access.sfm.aliyuncs.com` 服务名限制），否则无法完成授权 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 限制和注意事项

- **权限限制**：RAM 用户无默认 SLR 创建权限，必须由主账号预先授予策略（见文档 1 和文档 2 中完全一致的 JSON 策略），否则插件市场与云市场导入均会失败。
- **功能边界**：
  - `code_interpreter` 插件**不支持网络访问**与**本地文件上传**，依赖库版本固定（如 `requests~=2.31.0`、`pandas` 等）；
  - `quark_search` 和 `github_search` 仅返回网页标题、关键词、摘要，**不支持访问原始网页内容或项目源码**；
  - 自定义插件的 `Object` 类型参数子属性不能为空，且工具名称长度上限为 20 字符，超长将导致发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **调用逻辑**：智能体应用中插件调用由大模型主动决策（基于工具名+描述+用户输入），而工作流应用中插件为显式编排节点，二者触发机制不同 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
- **计费说明**：`code_interpreter`、`calculator`、`generate_qrcode`、`github_search` 为免费；`text_to_image` 与 `quark_search` 为“限时免费，需申请开通”，具体开通路径未在文档中说明。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)


