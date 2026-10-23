# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别、规划和调用的标准化组件，弥补模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件支持官方预置、三方市场接入及完全自定义三种形态，适用于智能体（Agent 1.0）、工作流及 Assistant API 等多种调用路径。

## 支持的模型/功能

当前插件能力已在以下模型上验证可用：  
- `qwen-plus`（通义千问-Plus）  
- `qwen-max`（通义千问-Max）  

> **注意**：文档中明确指出“各模型对插件的兼容性可能有差异，最新的兼容性状态，请以控制台实际执行结果为准”[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)，因此生产环境务必以控制台实测为准，不可仅依赖文档列表。

插件按来源分为三类，均提供开箱即用或低代码集成能力：  
- **官方插件**：组件广场预置，免配置即可调用，包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **三方插件**：来自云市场，覆盖商业服务、图像视频、教育等领域，开通后可直接使用 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **自定义插件**：用户自主创建，支持对接任意 HTTP API，需定义插件 URL、工具路径、输入/输出参数及鉴权方式 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 关键参数

插件调用的核心参数由两层结构定义：**插件级**与**工具级**。

- **插件级参数**（仅自定义插件）：  
  - `plugin_url`：插件根域名，如 `https://example.com`；所有工具路径将拼接于此。  
  - `is_auth_enabled`：是否启用鉴权，支持 `Header` 或 `Query` 位置，类型含 `basic`/`bearer`/`appcode`，Token 值需按规范填写 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  

- **工具级参数**（所有插件共用）：  
  - `tool_name`：语义化名称（≤20 字符），影响大模型调用决策。  
  - `tool_description`：自然语言描述，建议包含使用示例，直接影响工具召回准确率 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  
  - `tool_path`：相对路径，必须以 `/` 开头（如 `/query`）。  
  - `input_parameters`：定义入参，关键字段包括：  
    - `parameter_name`（如 `city`）、`description`（如 `城市名称，中文`）、`type`（`String`/`Number`/`Object`）、`passing_method`（`大模型识别` 或 `业务透传`）。  
    - `Object` 类型子属性**不能为空**，否则发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  
  - `output_parameters`：定义出参，大模型据此解析 API 返回并构造最终响应，要求层级精简、描述准确。  
  - `advanced_config`（可选）：提供 `user_query → expected_payload` 示例对，显著提升复杂参数场景下的调用准确率 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 使用方式

插件需先发布为 MCP 服务，再通过以下任一方式集成：

- **控制台集成（推荐调试）**：  
  1. 在插件列表中，对目标插件单击 **发布为MCP服务**；  
  2. 进入智能体应用编排页，在 **MCP 区块** 单击 `+` → 切换至 **自定义MCP** 页签 → 添加该服务；  
  3. 若含鉴权或 `业务透传` 参数，需在对话前点击配置图标填入 `biz_params` 或 Token [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  

- **API 集成（生产部署）**：  
  - 通过 [Assistant API](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api) 的 `tools` 字段传入工具 ID（如 `"id": "calculator"`）及配置；  
  - 若含 `业务透传` 或用户级鉴权，需在请求体中通过 `biz_params` 传递对应参数 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  

- **工作流应用**：将插件作为独立节点拖入画布，手动编排执行顺序，不依赖大模型自动规划 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 限制和注意事项

- **权限限制**：首次访问插件市场需主账号或已授权 RAM 子账号创建服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需额外授予 `ram:CreateServiceLinkedRole` 权限，否则无法进入插件页面 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **参数限制**：  
  - GET 请求**不支持 `Object` 类型输入参数**，否则发布报错 `130022` [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；  
  - 工具名称超长（>20 字符）会导致发布失败，需手动截断 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  
- **功能限制**：  
  - `code_interpreter` 插件**禁止网络访问与本地文件上传**，仅支持白名单依赖（如 `pandas`, `matplotlib`, `requests` 等）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；  
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、摘要、链接，**不支持抓取详情页内容** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)；  
  - 官方插件**仅能与同业务空间内的智能体应用关联**，跨空间需先授权 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **安全与运维**：删除插件或工具将导致所有关联应用失效且**不可恢复**，操作前须确认 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


