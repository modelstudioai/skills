# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、网络搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态输出等方面的固有局限。开发者可直接调用官方插件、开通三方插件，或创建自定义插件，所有插件均通过统一的工具调用协议与智能体/工作流/Assistant API集成。插件能力需依赖服务关联角色授权方可启用，详见[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 支持的模型/功能

当前插件能力支持以下模型（按控制台实测兼容性为准）：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对工具调用的规划能力存在差异，建议在实际业务中以控制台调试结果为最终依据。  
插件按来源分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL转二维码）、`github_search`（GitHub项目检索）。详细说明见[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需在云市场开通后使用。
- **自定义插件**：支持通过API URL导入或手动创建，可对接任意HTTP服务，需配置工具路径、鉴权、输入/输出参数等。完整流程参见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档2中列出的模型兼容性表格未注明生效时间，而文档1和文档3均强调“以控制台实际执行结果为准”。实践中发现 `qwen-vl-plus` 在部分图像生成类插件调用中存在响应延迟或失败率升高现象，建议优先选用 `qwen-vl-max` 进行视觉相关任务。

## 关键参数

插件调用依赖以下核心参数：
- **工具ID（tool_id）**：唯一标识一个工具，用于API请求中指定目标。可在插件详情页的“插件工具”区域或自定义插件工具卡片上悬停复制（见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **输入参数（input parameters）**：由大模型从用户输入中提取（传参方式为“大模型识别”）或由业务系统透传（传参方式为“业务透传”）。自定义插件中需明确定义参数名、类型（String/Number/Object）、描述及是否必填。
- **鉴权配置**：适用于自定义插件及部分三方插件。支持 Header（如 `Authorization: Bearer <token>`）或 Query（如 `?api_key=xxx`）方式，鉴权类型包括 `basic`、`bearer`、`appcode`。
- **高级配置（示例Query）**：为提升大模型参数提取准确率，可在自定义插件中配置典型用户输入与期望入参的映射关系（如用户输入“查询杭州明天天气” → `{"city": "杭州", "date": "2025-04-25"}`）。

## 使用方式

插件可通过三种方式集成：
1. **控制台可视化集成**：在[插件市场](https://bailian.console.aliyun.com/#/plugin-market)页面，选择插件后单击“添加至智能体”，关联到同业务空间的智能体应用；或在智能体编排页的“MCP”区块中添加已发布的MCP服务（自定义插件需先发布为MCP服务）。
2. **工作流节点调用**：在工作流应用中将插件作为独立节点拖入画布，按需配置输入/输出映射（详见[工作流应用插件节点](raw/application-user-guide/llm-application/workflow-application.md)）。
3. **API调用**：
   - 通过 **Assistant API**：在 `tools` 字段中声明工具列表（含 `tool_id` 和 `function.description`），由模型自主决策调用（参考[Assistant API文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)）；
   - 通过 **DashScope SDK/HTTP接口**：在请求体中传递 `tool_id` 及 `biz_params`（用于透传参数或用户级鉴权[Token](../concepts/token.md)）。

## 限制和注意事项

- **权限前提**：首次使用插件必须完成服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI` 授权。主账号可一键授权；RAM子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 必须为 `cloundapi-access.sfm.aliyuncs.com`），否则无法进入插件页面或导入云市场API —— 此要求在[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)和[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)中均被明确强调。
- **业务空间隔离**：官方插件仅能与**相同业务空间**内的智能体应用关联；跨空间调用需通过API方式或MCP服务解耦。
- **工具数量上限**：单个智能体应用最多绑定10个工具（含官方、三方、自定义插件）。
- **安全限制**：`code_interpreter` 插件禁止网络访问及本地文件上传，仅预装指定依赖库（如 `pandas`, `matplotlib`, `requests` 等），详见[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **自定义插件发布要求**：工具必须处于“已发布”且“调试成功”状态才可被调用；Object类型输入参数在GET请求下不被支持，需改用POST（见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)错误码130022说明）。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


