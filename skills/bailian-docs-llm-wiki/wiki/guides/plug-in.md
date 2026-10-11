# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式接入，弥补大模型在精确计算、实时信息获取、多模态输出等方面的固有局限。开发者可直接调用官方插件、开通三方插件，或基于自有 API 创建自定义插件，所有插件均通过统一的工具 ID 和参数契约被智能体或工作流调度。插件调用由大模型自主规划（Agent 模式）或按流程编排（Workflow 模式）触发，无需手动编写集成逻辑。

## 支持的模型/功能

当前插件能力仅在以下通义千问系列模型中正式支持：  
- `qwen-plus`（通义千问-Plus）  
- `qwen-max`（通义千问-Max）  

> **注意**：文档 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中明确指出“各模型对插件的兼容性可能有差异，最新的兼容性状态，请以控制台实际执行结果为准”，而 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 未提及其模型限制，此处以更严谨的概述文档为准。

官方插件提供开箱即用的六类基础能力，无需配置输入/输出参数：  
- `code_interpreter`：执行 Python 代码（支持 pandas、matplotlib、sympy 等依赖，但**不支持网络访问与本地文件上传**）  
- `calculator`：高精度数学计算  
- `text_to_image`：文生图（限时免费，需申请开通）  
- `quark_search`：实时网页搜索（返回标题、关键词、摘要，**不支持访问网页详情页**）  
- `generate_qrcode`：URL 转二维码  
- `github_search`：GitHub 项目检索（返回项目标题、链接、摘要，**不支持访问项目详情**）  

三方插件覆盖商业服务、图像视频、教育等领域，需在插件市场开通后使用；自定义插件支持通过 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 文档指引创建，可对接任意 HTTP API。

## 关键参数

插件调用依赖两类关键参数：

1. **工具 ID（tool_id）**：全局唯一标识符，用于 API 请求中指定目标工具。例如 `calculator`、`quark_search`。获取路径：插件详情页 → 工具卡片 → 悬停并点击复制图标（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中“获取工具 ID”说明）。

2. **工具参数（input/output parameters）**：  
   - **输入参数**：需明确定义名称、类型（String/Number/Object）、描述、传参方式（`大模型识别` 或 `业务透传`）。Object 类型子属性**不能为空**，否则发布失败（错误码 130022）。  
   - **输出参数**：必须全部配置，大模型据此从 API 响应中提取并结构化最终答案。嵌套层级应尽量扁平。  
   - **高级配置（示例 Query）**：推荐为复杂入参提供 `Value` 示例（如 `{"city": "杭州", "date": "2025-04-25"}`），显著提升大模型参数提取准确率。

## 使用方式

插件可通过三种方式集成：

- **控制台可视化集成**：  
  1. 在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 开通/授权插件；  
  2. 进入智能体应用编排页 → **MCP 区块** → 添加已发布的 MCP 服务（官方/三方插件自动注册为 MCP；自定义插件需先点击“发布为 MCP 服务”）；  
  3. 最多支持单个应用关联 **10 个工具**，大模型根据输入自主选择调用（Agent 模式）或按节点顺序执行（Workflow 模式）。

- **Assistant API 集成**：  
  在请求 `messages` 中声明 `tools` 数组，每个元素包含 `type: "function"` 及对应 `function` 定义（含 `name` 即 tool_id、`description`、`parameters` JSON Schema）。详见 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api) 中 `tools` 关键字章节。

- **DashScope SDK / HTTP API 集成**：  
  对于含 `业务透传` 参数或开启用户级鉴权的插件，需通过 `biz_params` 字段传递参数或 Token（参考 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。

## 限制和注意事项

- **权限要求**：首次使用插件前，主账号或 RAM 子账号必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需额外授予 `ram:CreateServiceLinkedRole` 权限（策略脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)），否则无法进入插件市场或导入云市场 API。

- **功能限制**：  
  - `code_interpreter` 插件禁止网络访问及文件上传，依赖库版本固定（如 `requests~=2.31.0`, `pandas` 等），不可自定义安装；  
  - `quark_search` 与 `github_search` 均**仅返回摘要信息，不支持跳转或解析原始网页/仓库内容**；  
  - 自定义插件的 `Object` 类型输入参数在 `GET` 请求下不被支持（错误码 130022），须改用 `POST`。

- **发布与调试**：所有自定义工具必须完成 **在线调试成功 → 保存草稿 → 发布** 流程才可被调用；发布失败常见原因为参数描述缺失（错误码 130040）或 Object 子属性为空（错误码 130022），需严格按 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 文档修正。

- **计费说明**：官方插件中 `code_interpreter`、`calculator`、`generate_qrcode`、`github_search` 为免费；`text_to_image` 与 `quark_search` 为限时免费，需单独申请开通。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


