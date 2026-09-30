# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调度的标准化单元，弥补其在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件分为官方插件、三方插件和自定义插件三类，支持在智能体应用、工作流应用及 Assistant API 中调用。所有插件均需通过服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI` 授权后方可使用，详见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 支持的模型/功能

当前插件能力仅在以下模型上可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性可能存在差异，**实际执行效果以控制台运行结果为准**，不建议依赖文档中未明确标注的模型标识符。  
插件功能按来源分为三类：
- **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等。详情见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云市场，覆盖商业服务、图像视频、教育等领域，开通后即可调用。
- **自定义插件**：用户可基于自有 API 创建，支持完整生命周期管理（创建、调试、发布、MCP 服务转换），适用于官方/三方插件无法满足的业务场景，操作指南见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中“插件调用机制”部分称插件可通过“工作流应用”调用，但未说明是否支持工具自动规划；而文档 2 明确指出“在工作流应用中调用插件，是将插件作为工作流应用的一个节点，按照用户编排的方式执行特定任务，而非由大模型主动进行规划和调用”。二者逻辑一致，但文档 1 表述易引发歧义，应以文档 2 的说明为准。

## 关键参数

- **工具 ID**：唯一标识一个工具，用于 API 调用时指定目标。可在插件详情页的“插件工具”区域或工具名称旁的图标处复制（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **输入参数（入参）**：
  - `传参方式` 必须明确设为 `大模型识别`（从用户输入中抽取）或 `业务透传`（由外部传入，如 `biz_params`）；
  - `参数名称` 和 `参数描述` 需语义清晰，直接影响大模型参数提取准确率；
  - `类型` 支持 String/Number/Object 等，Object 类型下子属性**不能为空**（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **输出参数（出参）**：所有字段均为必填，定义应精简、扁平，避免深层嵌套，以便大模型高效解析并合成最终回复。
- **鉴权配置**（自定义插件）：支持 Header 或 Query 方式，鉴权类型包括 `basic`、`bearer`、`appcode`；Token 值需与 API 提供方一致。

## 使用方式

1. **权限准备**：首次使用前，主账号或 RAM 子账号必须完成 `AliyunServiceRoleForSFMAccessCloudAPI` 角色授权（[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
2. **插件接入**：
   - **官方/三方插件**：在插件市场页面单击“添加至智能体”，选择目标智能体应用（官方插件需同业务空间），最多支持添加 10 个工具；
   - **自定义插件**：需先发布为 MCP 服务，再在智能体应用的“MCP”区块中添加；
   - **工作流应用**：将插件作为独立节点拖入流程图，手动配置输入/输出映射；
   - **API 调用**：通过 Assistant API 的 `tools` 字段声明可用工具列表，或在 DashScope SDK 中传入 `tools` 参数。
3. **调用验证**：在智能体对话框中输入典型请求（如“12313×13232等于多少”），观察是否触发 `calculator` 工具并返回正确结果（[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)）。

## 限制和注意事项

- **模型限制**：插件不支持所有模型，仅限文档明确列出的 `qwen-*` 系列模型；其他模型调用将静默失败。
- **功能限制**：
  - `code_interpreter` 不支持网络访问、本地文件上传，依赖库版本固定（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；
  - `quark_search` 和 `github_search` 仅返回网页标题、关键词、摘要或项目链接，**不支持直接抓取网页正文或项目代码内容**；
  - 同一智能体应用最多绑定 10 个工具。
- **配置风险**：
  - 自定义插件中，若 `请求方法` 为 `GET`，则输入参数**不支持 Object 类型**（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）；
  - 删除插件或工具会导致已关联的应用失效，且操作不可逆；
  - 修改插件 URL 或鉴权配置后，必须重新测试并发布所有相关工具。
- **调试建议**：复杂入参场景务必使用“高级配置”提供调用示例（如 `{"city": "杭州", "date": "2025-04-25"}`），可显著降低漏召回与误召回率。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


