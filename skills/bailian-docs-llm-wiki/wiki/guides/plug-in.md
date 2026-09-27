# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调用的标准化单元，解决模型在实时信息获取、精确计算、多模态生成等场景下的固有局限。插件支持官方预置、三方集成与自定义开发三种形态，可在智能体应用、工作流应用及 Assistant API 中统一调用。其设计目标是让开发者以最小认知成本接入可信、可控、可审计的外部能力。

## 支持的模型/功能

当前插件能力仅在以下模型上可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的规划能力与响应稳定性存在差异，实际兼容性请以控制台运行结果为准。详细模型能力对比见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

官方插件提供开箱即用的 6 类基础能力：  
- `code_interpreter`：执行 Python 代码（数学计算、数据分析、可视化），依赖固定环境（含 `pandas`、`matplotlib`、`sympy` 等），**不支持网络访问与本地文件上传**；  
- `calculator`：高精度数值计算；  
- `text_to_image`：文生图（限时免费，需申请开通）；  
- `quark_search`：实时网页搜索（返回标题、关键词、摘要，**不支持访问网页详情页**）；  
- `generate_qrcode`：URL 转二维码；  
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，**不支持访问项目详情页**）。  

三方插件覆盖商业服务、图像视频、教育等领域，需在插件市场开通后使用；自定义插件则允许开发者接入任意 HTTP API，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 和 `github_search` 的能力边界（仅返回摘要类信息），但文档 2 在“常见问题”中额外说明“夸克搜索和联网搜索（`enable_search`）的区别”，指出后者是“基于夸克搜索”的轻量模式，且不保证返回搜索结果——该差异未在文档 1 中体现，开发者应以文档 2 的说明为准。

## 关键参数

插件调用依赖两类核心参数：  
- **工具 ID（`tool_id`）**：全局唯一标识符，如 `calculator`、`code_interpreter`，用于 API 请求中指定目标工具；可通过插件详情页悬浮图标复制，见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **输入参数（`input`）**：由大模型从用户 Query 中提取，或通过 `biz_params` 业务透传。配置时需明确定义参数名、类型（String/Number/Object）、描述、传参方式（“大模型识别”或“业务透传”）及是否必填。Object 类型子属性**不能为空**，否则发布失败（错误码 `130022`）。  
- **鉴权参数**：若插件启用鉴权，支持 `Header`（如 `Authorization: Bearer <token>`）或 `Query`（如 `?api_key=xxx`）方式，鉴权类型包括 `basic`/`bearer`/`appcode`。用户级鉴权需在对话前通过控制台配置 [Token](../concepts/token.md)，或通过 `biz_params` 透传。

## 使用方式

插件可通过三种路径集成：  
1. **控制台智能体应用**：在插件市场选择工具 → 单击“添加至智能体” → 选择目标智能体 → 发布应用。注意：官方插件仅支持与**同业务空间**内的智能体关联；自定义插件需先发布为 MCP 服务，再在智能体编排页的“MCP”区块中添加。  
2. **工作流应用**：将插件作为独立节点拖入画布，按需配置输入/输出映射，不依赖大模型自动规划。具体操作见 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
3. **API 调用**：  
   - Assistant API：在请求体 `tools` 字段中声明工具列表，模型自动选择并调用；  
   - DashScope SDK / HTTP 接口：通过 `tool_choice` 指定工具，`tool_input` 传入参数；含业务透传或用户级鉴权时，须通过 `biz_params` 传递对应字段。  

所有方式均要求插件/工具状态为“已发布”且“已启用”。调试阶段务必使用插件详情页的“测试工具”功能验证连通性。

## 限制和注意事项

- **权限前提**：首次使用插件需主账号或具备 `ram:CreateServiceLinkedRole` 权限的 RAM 用户授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`，否则无法访问插件市场，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **数量限制**：单个智能体应用最多关联 10 个工具；自定义插件的工具路径必须以 `/` 开头，且同一插件下所有工具共享插件 URL 域名。  
- **安全约束**：`code_interpreter` 插件明确禁止网络访问与文件上传；自定义插件若配置 `GET` 方法，则输入参数**不支持 Object 类型**（错误码 `130022`）。  
- **发布强校验**：自定义工具发布时，缺失参数描述（错误码 `130040`）、Object 子属性为空、GET 含 Object 参数等均会导致失败，必须修正后重新发布。  
- **失效风险**：删除插件或工具将导致所有关联应用调用失败，且操作不可逆。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


