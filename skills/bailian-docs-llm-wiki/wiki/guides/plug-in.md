# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调用的标准化单元，解决模型在实时信息获取、精确计算、多模态生成等场景下的固有局限。插件支持官方预置、三方市场及自定义开发三种来源，可在智能体应用、工作流应用及 Assistant API 中统一调用。其设计目标是让开发者以最小认知成本集成确定性能力，而非替代模型推理。

## 支持的模型/功能

当前插件能力仅在以下模型上可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的规划能力与响应稳定性存在差异，**实际兼容性请以控制台运行结果为准**，不建议依赖文档中未明确标注的模型标识符。  
插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需配置参数。包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等。详情见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
- **三方插件**：来自阿里云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用。调用前须确保已授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色，具体流程参见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **自定义插件**：支持从零创建或从云市场导入，适用于私有 API 集成。需明确定义插件 URL、工具路径、输入/输出参数及鉴权方式，调试发布后方可使用。完整流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件，但文档 2 明确指出其“目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 1 仅简述为“搜索实时信息”。此处以文档 2 的限定说明为准，避免误判插件能力边界。

## 关键参数

插件调用依赖以下核心参数，均需在控制台或 API 中显式配置：
- **工具 ID（tool_id）**：唯一标识一个工具，如 `calculator`、`text_to_image`。必须与插件市场或自定义插件中发布的 ID 完全一致。获取方式见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数（input parameters）**：由大模型从用户 query 中提取，需在自定义插件中明确定义 `参数名称`、`参数描述`、`类型`（String/Number/Object 等）及 `传参方式`（“大模型识别”或“业务透传”）。Object 类型子属性不能为空，否则发布失败（错误码 130022）。
- **鉴权配置**：自定义插件若需鉴权，须设置 `是否鉴权`、`鉴权类型`（basic/bearer/appcode）、`位置`（Header/Query）及 `Token`。Header 鉴权默认字段为 `Authorization`；Query 鉴权需指定参数名（如 `api_key`）。
- **高级配置（可选）**：提供 `Value` 字段的调用示例（如 `{"city": "杭州", "date": "2025-04-25"}`），显著提升复杂入参的识别准确率，减少漏召/误召。

## 使用方式

插件可通过三种方式接入：
- **智能体应用（Agent 1.0）**：在应用编排页面的 **MCP 区块** 添加插件（或其转换的 MCP 服务）。官方插件仅支持与**同业务空间**内的智能体关联；自定义插件需先发布为 MCP 服务再添加。最多支持同时启用 10 个工具。
- **工作流应用**：将插件作为独立节点拖入画布，按需配置输入/输出映射，执行逻辑由人工编排而非模型自主决策。
- **Assistant API**：在 `tools` 数组中传入工具定义（含 `type`, `function.name`, `function.description`, `function.parameters`），并在 `messages` 中触发调用。详细格式见 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)。

> **注意**：文档 1 称插件可通过“智能体应用、工作流应用以及 Assistant API 调用”，而文档 2 的“调用插件”章节仅详述了智能体和工作流两种方式，并强调 Assistant API 需“搜索 `tools` 关键字”查阅。此处以文档 2 的指引为准——Assistant API 是正式支持方式，但需开发者主动查阅对应 API 文档，而非控制台图形化配置。

## 限制和注意事项

- **权限前提**：首次使用插件（无论官方、三方或自定义）前，主账号或 RAM 用户必须完成 `AliyunServiceRoleForSFMAccessCloudAPI` 服务关联角色授权。RAM 用户需额外获得 `ram:CreateServiceLinkedRole` 权限（策略脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **功能限制**：`code_interpreter` 插件**不支持网络访问及本地文件上传**，仅限沙箱内执行；`quark_search` 和 `github_search` 均仅返回摘要信息，无法抓取网页正文或项目代码仓库详情。
- **发布约束**：自定义插件的工具名称长度上限为 20 字符；Object 类型输入参数在 GET 请求下不被允许（错误码 130022）；所有输出参数均为必填项，且描述需精简准确，否则影响大模型结果解析。
- **运维风险**：删除插件或工具将导致所有关联应用失效，且操作不可逆；修改插件 URL 或鉴权配置后，必须重新测试并发布工具，否则调用将失败。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


