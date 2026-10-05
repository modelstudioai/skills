# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可调用的标准化组件，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件支持官方预置、三方市场及自定义开发三种类型，可被智能体应用、工作流应用或 Assistant API 主动或编排式调用。其设计目标是让开发者以最小集成成本获得可验证、可组合、可管理的增强能力。

## 支持的模型/功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性存在差异，实际可用性请以控制台运行结果为准。插件本身按来源分为三类：

- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等。详情见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
- **三方插件**：来自阿里云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用，无需额外配置。具体接入方式和权限要求详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **自定义插件**：支持开发者基于自有 API 创建，支持 HTTP(S) 协议、灵活鉴权（Header/Query、Bearer/AppCode/Basic）、JSON 或 form-urlencoded 提交方式，并可导入云市场 API。完整流程参见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 2 在“常见问题”中补充说明“联网搜索（enable_search）也是基于夸克搜索”，但未明确二者是否为同一能力的不同调用路径。实践中应以控制台插件市场实际提供的 `quark_search` 工具 ID 为准，`enable_search` 并非独立插件，而是部分模型内置的搜索开关，与插件调用机制不同。

## 关键参数

插件调用依赖以下关键参数，尤其在自定义插件和 API 集成场景中必须准确配置：

- **工具 ID（tool_id）**：唯一标识一个工具，例如 `calculator`、`text_to_image`；通过插件详情页悬浮图标复制获取（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **输入参数（input parameters）**：
  - `传参方式`：必须明确设为 `大模型识别`（由 LLM 从用户输入中抽取）或 `业务透传`（由外部系统传入，需通过 `biz_params` 或 `user_defined_params` 指定）；
  - `参数名称` 与 `参数描述` 需语义清晰，直接影响 LLM 参数提取准确率；
  - `类型` 支持 String/Number/Boolean/Object，Object 类型子属性**不能为空**（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 错误码 130022）。
- **输出参数（output parameters）**：所有字段必填，定义 LLM 如何解析 API 响应并组织最终回复；建议层级扁平、命名精准。
- **鉴权配置**：若开启鉴权，需指定 `鉴权类型`（bearer/basic/appcode）、`位置`（Header/Query）、`参数名`（如 `Authorization` 或 `api_key`）及 `Token` 值。

## 使用方式

插件可通过三种方式集成到应用中：

1. **控制台可视化集成（推荐用于快速验证）**：
   - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面单击“添加至智能体”，选择目标智能体应用即可关联（最多 10 个工具）；
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页面的 **MCP 区块** 中添加（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）；
   - 所有插件均支持在工作流应用中作为独立节点编排调用（见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)）。

2. **API 集成**：
   - 通过 DashScope SDK 或 HTTP 接口调用已绑定插件的应用时，若含 `业务透传` 参数或 `用户级鉴权`，必须通过 `biz_params` 字段传递对应值；
   - Assistant API 用户需在 `tools` 数组中声明工具 ID 及函数定义，详见 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)（引用见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。

3. **权限前提**：
   - 主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`（策略 `AliyunServiceRolePolicyForSFMAccessCloudAPI`），否则无法访问插件市场或调用云市场 API（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 限制和注意事项

- **业务空间隔离**：官方插件仅能与**同业务空间内的智能体应用**关联；跨空间调用需通过 MCP 服务或 API 方式实现。
- **调用上限与计费**：`code_interpreter`、`calculator`、`generate_qrcode`、`github_search` 免费；`text_to_image` 和 `quark_search` 为限时免费，需单独申请开通；三方插件按所选套餐计费（见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)）。
- **安全限制**：
  - `code_interpreter` 插件**禁止网络访问**（无法 `requests.get` 外部 URL）且**不支持上传本地文件**，可用依赖列表严格限定（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；
  - 自定义插件的 `插件URL` 必须为 HTTPS 协议，且域名需在白名单范围内（控制台提示为准）。
- **调试与发布强约束**：
  - 自定义插件的工具必须**发布后**才可在应用中调用；
  - 工具发布失败常见原因为：参数描述缺失（错误码 130040）、Object 类型子属性为空或 GET 请求下误配 Object 输入参数（错误码 130022），须按 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 的错误码说明修复。
- **RAM 子账号特殊要求**：若无 `ram:CreateServiceLinkedRole` 权限，需主账号预先授予自定义策略（策略脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)），否则无法完成 SLR 授权。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


