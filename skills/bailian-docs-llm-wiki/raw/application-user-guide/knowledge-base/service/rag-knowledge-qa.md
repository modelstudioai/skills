# 知识问答

知识问答服务基于大模型结合知识检索能力，支持绑定多个知识库，自动检索相关内容并生成自然语言回答。您可以通过控制台配置模型、检索参数和生成策略，也可以通过 API 集成到自有应用中。

## 创建问答服务

1.  登录控制台，进入 [**知识服务 → 知识问答**](https://bailian.console.aliyun.com/cn-beijing/rag/qa/list)。
    
2.  点击右上角 **创建**，在弹窗中填写 **服务名称**（必填，最多 40 个字符）和 **描述信息**（可选，最多 200 个字符），点击 **确认** 完成创建。
    
3.  创建成功后自动进入配置页面。选择生成回答的 **模型**（如 qwen3.6-plus），点击模型右侧的 **设置** 图标可配置 `temperature` 和 `enable_thinking` 参数；**提示词**（可选，最多 500 个字符）用于指导模型的回答风格和行为。
    
4.  选择检索策略，见下方[检索模式](https://help.aliyun.com/zh/model-studio/rag-knowledge-qa#h-ragqa-mode)。
    
5.  点击 **\+ 添加**，绑定一个或多个知识库（最多 15 个）。开启 **优先级** 开关后，每个知识库会显示优先级选项，可选择 **高/中/低** 设置该知识库的检索优先级。
    
    如需为单个知识库设置独立参数，点击知识库右侧的展开图标，展开该知识库的配置面板，见下方[知识库独立配置](https://help.aliyun.com/zh/model-studio/rag-knowledge-qa#h-ragqa-kb-config)。
    
6.  根据需要启用文件预解析、拒答、防泄漏等生成控制参数，见下方[生成控制参数](https://help.aliyun.com/zh/model-studio/rag-knowledge-qa#h-ragqa-gen)。
    
7.  在右侧的调试窗口中输入问题，查看模型生成的回答、引用来源和检索过程。支持上传附件（需开启文件预解析）。
    
8.  配置完成后，点击右上角 **发布**。发布后可通过 API 调用该问答服务。
    

**说明**

-   已创建至少一个知识库，且知识库中已有解析完成的文档。
-   如需使用多知识库联合问答，各知识库须位于同一业务空间下。

## 检索模式

模式

工作方式

适用场景

极速

单轮检索后直接生成回答，支持 Query 改写开关

简单明确的问题、对响应速度敏感的场景

多轮智能检索

基于大模型进行多轮规划搜索（Agentic），自动进行意图识别、Query 改写和知识库路由，可配置 ReAct 最大轮次

复杂问题、模糊问题、需要跨库综合回答的场景

点击检索模式下拉框右侧的 **设置** 图标可配置检索模式的高级参数。

## 知识库独立配置

点击知识库右侧的展开图标，可配置该知识库的独立检索参数：

参数

取值范围

说明

Query 改写

开/关

对用户输入进行优化改写，提升检索效果。极速模式下通过此开关控制；多轮智能检索模式下由 Agent 自动改写

初步向量检索 TopK

1~100

向量检索阶段初步召回的切片数量

初步关键词检索 TopK

1~100

关键词检索阶段初步召回的切片数量

排序模型

qwen3-rerank 等 / 不使用模型

对该知识库的召回结果独立排序。纯文本知识库可选 qwen3-rerank 系列；多模态知识库可选 qwen3-vl-rerank

排序模型模式

问答模式 / 相似模式

问答模式按 QA 匹配度排序；相似模式按语义相似度排序。仅在排序模型开启时可用

相似度阈值

0.01~1.0

过滤排序后分数低于阈值的切片。值越高结果越精确，但可能遗漏相关内容

最大召回数量

1~20

该知识库排序后返回的切片数量

标签过滤

—

根据文档标签过滤检索范围。输入标签后回车确认，或从下拉列表中选择已有标签

**说明**不同知识库类型展示的参数有所不同。文档搜索类型展示全部参数；图片问答等多模态类型不展示 Query 改写和 TopK 参数。

## 生成控制参数

参数

说明

文件预解析

开启后，可在调试窗口通过附件按钮上传文件（包括图片和文档）进行问答。提供两种解析模式：**全文引用**（解析完整内容作为上下文）和**切片检索**（将文件切片后结合知识库检索）

拒答

开启后，当检索结果不足以回答问题时，模型拒绝回答并返回自定义的拒答话术

防泄漏

开启后，防止知识库原文在回答中被直接泄漏，检测到可能泄漏时返回自定义的防护回复

多模态回复

开启后，模型回答中会包含知识库中的图片等多模态内容

引用

开启后，模型回答中展示引用来源，标注回答内容出自哪个文档

## API 调用

知识问答通过 [chat 接口](raw/application-api-reference/rag-api/knowledge/knowledgechat.md) 调用，返回 SSE 流式响应：

```
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "切片策略怎么选？"}
      ]
    },
    "parameters": {
      "agent_options": {
        "agent_id": "${YOUR_AGENT_ID}"
      }
    },
    "stream": true
  }'
```

**重要**也可通过阿里云百炼 CLI 发起知识问答：`bl knowledge chat --message "切片策略怎么选？" --agent-id <问答服务ID>`。详见[使用 CLI](raw/application-user-guide/knowledge-base/integration/cli.md)。

### SSE 事件类型

问答响应按以下顺序返回事件：

事件

说明

`plan_start` → `planning` → `plan_end`

规划阶段，模型规划检索与回答策略

`tool_calling` → `tool_return`

工具调用阶段，`tool_calling` 抛出检索请求，`tool_return` 返回命中切片

`generation_start` → `generating` → `generation_end`

生成阶段，流式输出最终回答，`generation_end` 时 `finish_reason` 为 `stop`

**说明**多轮智能检索模式下，`plan → tool_calling → tool_return` 整段可重复多次。事件完整说明见 [chat 接口](raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

## 多轮对话

平台不保存对话状态，每次请求需传入完整 `messages` 历史。建议：

-   限制历史长度（最近 10 轮），避免超出模型上下文窗口
-   检索时仅基于最新一条 user message，降低噪声

**重要**创建问答服务后，可以在[服务渠道](raw/application-user-guide/knowledge-base/integration/channels.md)中查看接入方式，通过 API / MCP / CLI 等方式集成到应用中。
