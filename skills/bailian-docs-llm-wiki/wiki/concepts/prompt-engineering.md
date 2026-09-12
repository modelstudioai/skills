# Prompt 工程

Prompt 工程是系统性设计、验证与优化提示词（Prompt）以精准引导大模型生成高质量、稳定、可复用输出的技术实践。它不仅是文本输入的简单编写，更涵盖模板结构化、变量注入、上下文编排、输出约束、A/B 测试及自动化反馈调优等全生命周期方法。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**：通过 `prompt_template` 字段在 API 请求中内联 Jinja2 模板（如 `{{ input }}`、`{% for item in context %}...{% endfor %}`），实现动态内容注入与逻辑分支控制；所有托管模型均支持该能力，是提升输出一致性的基础手段。  
- **Skill 封装**：将 Prompt 模板作为独立 `type: "prompt"` 的 Skill 发布，配合 `output_schema` 强制结构化返回（如 JSON 格式），供工作流或外部系统标准化调用，避免重复开发与维护碎片化提示逻辑。  
- **资产中心管理**：Prompt 模板作为一类核心 AI 资产（`asset_type = "prompt_template"`），支持版本化（`version`）、权限隔离（`visibility: private/org/public`）与跨项目复用；可一键部署为 API 服务或导入 Notebook 进行实验验证。  
- **应用构建（LLM Application）**：在智能体（Agent 2.0）、工作流（Workflow）及高代码应用中，Prompt 工程是定义角色行为（`system_prompt`）、控制工具调用格式、约束多轮对话状态的关键配置项；RAG 场景下常与 `retrieval_config` 协同，将检索结果注入 Prompt 上下文。  
- **用例落地**：在文生文、客服问答、AI 解题等典型场景中，需严格遵循平台提供的 [Prompt 工程指南](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide)，例如使用角色标记（`<|system|>`/`<|user|>`）、权重语法（`[重要]`）、分隔符（`---`）等规范，否则生成质量显著下降。  
- **持续优化闭环**：对支持自动优化的模型（见 [Prompt 自动优化支持列表](https://help.aliyun.com/zh/model-studio/optimize-prompt)），启用 `enable_prompt_optimization: true` 后，平台基于真实调用反馈（如人工评分、规则校验）自动迭代模板版本，无需人工重写。

## 关键参数和配置

- `prompt_template`：字符串类型，Jinja2 语法模板，最大长度 8192 token（含变量展开后），超长将截断并返回 warning。  
- `variables`：JSON 对象，与模板中变量名一一对应，用于运行时替换（如 `{"input": "xxx", "context": ["a", "b"]}`）。  
- `enable_prompt_optimization`：布尔值，设为 `true` 时触发平台级自动优化（仅同步调用生效，流式响应不支持）。  
- `prompt_version`：字符串，指定模板版本号（如 `"v2.1"`），默认取 `latest`；历史版本可用于 A/B 测试或回滚。  
- `output_schema`：JSON Schema 对象（可选），定义期望输出结构，配合 `type: "prompt"` 的 Skill 使用，平台将自动校验并格式化返回结果。  
- `system_prompt`：字符串（部分应用类型支持），用于全局角色设定，优先级高于模板内硬编码的 system 指令，适用于多轮对话一致性保障。

## 面向开发者，简洁实用

- ✅ **起步建议**：从控制台「资产中心」→「Prompt 模板」创建首个模板，使用预置样例快速验证；调试阶段务必开启控制台「测试」功能，观察变量注入与 token 截断效果。  
- ✅ **生产最佳实践**：  
  - 所有线上 Prompt 模板必须绑定明确 `version` 并发布为 `published` 状态；  
  - RAG 场景下，用 `{{ retrieved_chunks | join('\n---\n') }}` 安全拼接检索结果，避免越界；  
  - 启用 `output_schema` 时，确保返回字段名与 Schema 中 `properties` 键完全一致（区分大小写）；  
  - 避免在模板中硬编码敏感信息，通过 `variables` 注入并配合 RAM 权限管控。  
- ⚠️ **避坑提醒**：  
  - `stream=true` 时 `enable_prompt_optimization` 无效；  
  - Qwen2/Qwen3 模型需手动验证旧版 Prompt 样例中的角色标记（如 `<|assistant|>`）兼容性；  
  - `prompt_template` 中禁止使用未声明的变量，否则渲染失败返回空字符串而非报错。

## 关联主题页

- [prompt](../guides/prompt.md)
- [skill](../guides/skill.md)
- [asset center page](../guides/asset-center-page.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [llm application](../guides/llm-application.md)


