# 调优数据上传规则

## 概述

本文档阐述文本生成模型调优数据的格式规格、打包要求、大小与数量限制及 API 上传配额。适用范畴为文本生成模型调优（text/image/video → text），涵盖纯文本 SFT/DPO/CPT、千问 VL 图片与视频理解、视频抽帧、工具调用（function calling）与深度思考（thinking）。视频生成模型调优（image → video）不属于本范畴。

数据集类型（训练集或评测集）创建后不可变更。各训练方式与元素的支持情况详见[训练方式与元素支持矩阵](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-support-matrix)，各组合的格式构造规则见下文对应章节。

**警告**发布与删除操作不可逆：已发布版本不可再编辑，仅草稿版本可删除或在线编辑；数据集类型创建后不可变更。切换类型、场景或训练方式会清空已上传文件。

管理类操作（创建参数、版本管理、评测集管理规则、导入方式选型、数据清洗、安全合规）引导到同级文档，详见[训练集与评测集](raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)、[模型调优简介](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)等。建议在创建数据集页面下载对应场景的数据模板，按模板结构准备数据可避免导入失败。

数据集构建建议（推荐数据规模、多样性与均衡、数据扩充策略）详见[模型调优简介-数据集构建技巧](https://help.aliyun.com/zh/model-studio/model-training-overview#aebd25a7f1g2v)。

强化学习（RL）训练数据格式（jsonl + messages + rollout\_extra，通过 SDK 上传）详见[RL 训练数据格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-rl)。

## 训练方式与元素支持矩阵

训练集支持 SFT、DPO、CPT 三种训练方法，各训练方式与元素的支持情况见下文矩阵表。调优推荐顺序为 CPT（可选）→ SFT → DPO（可选），三者递进非互斥。

地域可用性：

-   SFT、本地上传、日志回流、API 上传、多模态数据格式全地域支持。
-   DPO、CPT、OSS 导入、云存储挂载仅支持北京地域。

训练方式与元素的支持矩阵如下：

**训练方式**

**文本生成**

**视觉理解-图片输入**

**视觉理解-视频输入（qwen3.5+）**

**视觉理解-工具调用（qwen3.5+）**

**深度思考**

[SFT](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-sft-text)

✓

✓

✓

✓

✓

[DPO](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-dpo-text)

✓

✗

✗

✗

✓

[CPT](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-cpt-text)

✓

✗

✗

✗

✗

[评测集](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-eval-set)

✓

✗

✗

✗

✗

各训练方式版本新增时的数据继承策略如下（CPT 不支持继承已有数据，每次新增版本均需新建）：

**数据继承策略**

**SFT**

**DPO**

**CPT**

继承已有数据

✓

✓

✗

创建新数据

✓

✓

支持（强制新建）

训练方法 SFT/DPO/CPT 字段定义详见[模型调优简介](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 文本生成 - SFT 格式

SFT 文本生成训练数据采用 jsonl 文件格式，基于 ChatML messages 多轮结构。

-   支持 system、user、assistant 三种角色，content 字段为字符串（多模态场景的 content 数组结构见对应多模态格式章节）。
-   单文件大小上限 200 MB。
-   一个数据集可混合不同格式行——每条记录独立选格式，无需统一为单一格式。
-   可选格式：普通对话、深度思考、工具调用、工具与思考组合（见下方标签页样例）。

SFT 文本生成支持以下样例格式，各样例的完整 JSON 结构见对应标签页：

#### 普通 ChatML

普通 ChatML 格式样例（system/user/assistant 多轮对话）：

```
{
  "messages": [
    {"role": "system", "content": "系统输入1"},
    {"role": "user", "content": "用户输入1"},
    {"role": "assistant", "content": "期望的模型输出1"},
    {"role": "user", "content": "用户输入2"},
    {"role": "assistant", "content": "期望的模型输出2"}
  ]
}
```

#### 进阶用法

1.  支持`loss_weight`参数，取值范围 `(0.0, 1.0]`，数值越大代表训练时该条数据的重要性越高。
    
    > 默认支持 Qwen3.5 及以上版本模型；如需支持 Qwen3、Qwen2.5 系列模型，请联系商务经理。
    

```
{"role": "assistant", "content": "期望的模型输出", "loss_weight": "1.0"}
```

#### 深度思考（thinking）

深度思考（thinking）格式样例（思考标签放最后一条 assistant，前后换行必须保留）：

```
{
  "messages": [
    {"role": "system", "content": "系统输入1"},
    {"role": "user", "content": "用户输入1"},
    {"role": "assistant", "content": "模型输出1"},
    {"role": "user", "content": "用户输入2"},
    {"role": "assistant", "content": "<think>\n期望的思考内容2\n</think>\n\n期望的输出2"}
  ]
}
```

#### 工具调用（function calling）

请使用[视觉理解-SFT 格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#yz71e49hgo000)。

### 思考模式格式说明

深度思考内容用 `<think>\n…\n</think>\n\n` 标签包裹，置于 assistant 输出文本内（与最终答复同属最后一条 assistant 的 content）。规则：

-   只能放在最后一条 assistant 输出中；中间的 assistant 输出不加思考标签。
-   思考标签前后的换行符必须保留。
-   若训练样本设置模型不输出思考标签，训练完成后不建议再开启思考模式调用。

### 评测集格式

评测集仅服务文本生成场景，与 SFT/DPO/CPT 训练方式无关——DPO/CPT 训练后的模型同样使用文本生成评测集进行评测，不区分训练方式。

评测集规格：

-   文件格式 xlsx，列结构见控制台下载模板。
-   入库方式：本地上传、日志回流；不支持对象存储（OSS）导入与云存储挂载。
-   仅草稿版本支持在线编辑（Prompt/Completion），已发布版本不可编辑。

本地上传文件格式为 xlsx（列结构见控制台下载模板），每条评测数据为一组 Prompt/Completion 内容，示例如下：

```
{"prompt": "谁在文艺复兴时期绘制人体?", "completion": "文艺复兴时期是一个关于艺术、文化和学术的复兴运动,在这个时期,许多艺术家都绘制了人体。"}
{"prompt": "为什么太阳会发光发热?", "completion": "太阳是由氢原子核在高温高压下聚变而产生的巨大能量。这种聚变反应释放出大量的光和热能。"}
{"prompt": "为什么天空是蓝色的?", "completion": "阳光照射到地球大气层中时,波长较短的蓝光会被大气中的气体分子散射开来,形成我们看到的蓝天。"}
```

日志回流入库限制：

-   支持日志范围为最近 30 天内。
-   单次导入上限 10 万条。
-   需授权服务关联角色并指定 API Key 与模型筛选条件。
-   训练集仅 SFT 文本生成场景可用（评测集文本生成亦支持）。

日志回流导入方式详情见[日志回流](raw/model-user-guide/model-data-overview/model-log-backflow.md)。

评测集应准备数据不重叠的独立集合，用于客观评估模型泛化能力。评测集管理规则详见[训练集与评测集](raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 文本生成 - DPO 格式

DPO 文本生成训练数据采用 jsonl 格式，基于 ChatML messages 多轮结构，额外含 chosen 与 rejected 两条对比的 assistant 输出，用于偏好对齐训练。messages 内的所有内容均作为输入，DPO 用于训练模型对最后一条 user 输入的正负反馈。messages 多轮结构规则见[文本生成 - SFT 格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-sft-text)。

针对深度思考内容，chosen 或 rejected 的 assistant 输出可使用思考标签包裹，思考标签只能放最后一条 assistant 行，规则见[文本生成 - SFT 格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-sft-text)。

loss\_weight （邀测）参数支持 chosen 模块，取值范围 0.0 至 1.0，数值越大训练重要性越高，详见[文本生成 - SFT 格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-sft-text)。

DPO 训练数据单文件大小上限为 200 MB，与 SFT 文本生成一致。DPO 定义详见[模型调优简介](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)，草稿与发布操作见[训练集与评测集](raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

DPO 文本生成训练数据样例见下文代码块：

#### 普通 ChatML

普通 chosen/rejected 对比格式样例（两条对比的 assistant 输出）：

```
{
  "messages": [
    {"role": "system", "content": "系统输入"},
    {"role": "user", "content": "用户输入1"},
    {"role": "assistant", "content": "模型输出1"},
    {"role": "user", "content": "用户输入2"},
    {"role": "assistant", "content": "模型输出2"},
    {"role": "user", "content": "用户输入3"}
  ],
  "chosen": {"role": "assistant", "content": "赞同的模型期望输出3"},
  "rejected": {"role": "assistant", "content": "反对的模型期望输出3"}
}
```

#### 深度思考（thinking）

思考标签格式样例（深度思考内容用思考标签包裹，放最后 assistant）：

```
{
  "messages": [
    {"role": "system", "content": "系统输入"},
    {"role": "user", "content": "用户输入1"},
    {"role": "assistant", "content": "模型输出1"},
    {"role": "user", "content": "用户输入2"}
  ],
  "chosen": {"role": "assistant", "content": "<think>\n期望的思考内容\n</think>\n\n期望的模型输出"},
  "rejected": {"role": "assistant", "content": "反对的模型期望输出2"}
}
```

## 文本生成 - CPT 格式

CPT 文本生成训练数据采用 jsonl 纯文本格式，每行一个 jsonl 对象，结构为 {text}，text 字段为纯文本内容。messages 多轮结构规则见[文本生成 - SFT 格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-sft-text)。

CPT 训练数据约束：

-   建议至少 5000 万 Token，单文件大小上限 300 MB。
-   不支持草稿状态与数据继承，每次新增版本均需新建数据并立即发布。

CPT 定义详见[模型调优简介](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)，版本管理与数据继承操作见[训练集与评测集](raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。CPT 纯文本样例完整 JSON 结构见下文代码块。

{text} 纯文本格式样例（每行一个 jsonl 纯文本对象）：

```
{
  "text": "文本内容"
}
```

## 视觉理解-SFT 格式

SFT 图片训练数据用于千问 VL 多模态理解（控制台 UI 选项为「图片理解」）场景，采用 zip 压缩包格式，包含 data.jsonl 训练文本数据文件与图片文件。data.jsonl 须置于压缩包根目录，data.jsonl 中每条训练数据的 messages 采用 content 数组结构，数组项含图片字段（image）与文本字段（text）。推荐使用单层目录结构，打包规则详见[多模态压缩包打包规则](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-zip-package)。

#### 图片输入限制

图片准入限制如下：

-   单张图片宽度和高度均不超过 1024 px。
-   单张图片不超过 10 MB。
-   支持格式：bmp、jpeg、jpg、png、tif、tiff、webp。

resized\_width 与 resized\_height 为可选的目标缩放控制参数，用于指定图片目标缩放尺寸，非图片准入上限。图片准入上限为宽高不超过 1024 px、单张不超过 10 MB。图片准入具体数值以控制台实际展示为准。

图片消耗 token 计算详见[图像与视频理解-计费与限流](https://help.aliyun.com/zh/model-studio/vision#10c14b25cdhuh)。

#### 视频输入限制

仅 qwen3.5 及以后的多模态模型支持。支持两种视频输入模式：

-   **视频文件路径模式**：video 字段为字符串（如 "video1.mp4"），由平台处理抽帧。适用于使用完整视频文件的场景。
-   **图片帧列表模式**：video 字段为图片文件名列表（如 \["0.jpg","1.jpg"\]），用户自行准备帧序列。适用于已有抽帧图片的场景。

**说明**训练数据中的图片与视频须同时满足模型调用的输入限制（如图像分辨率、视频时长、帧率等），调用限制详见[视频限制](https://help.aliyun.com/zh/model-studio/vision)。

视频消耗 token 计算详见[图像与视频理解-计费与限流](https://help.aliyun.com/zh/model-studio/vision#10c14b25cdhuh)。

两种模式的字段对比与样例见下文：

**字段/参数**

**视频文件路径模式**

**图片帧列表模式**

video

str（视频文件路径，必填）

List\[str\]（图片帧列表，必填）

sample\_fps

不适用

float（\[0.1, 10\]，默认 2.0，可选）

fps

float（\[0.1, 10\]，默认 2.0，可选）

不适用

resized\_width

int（缩放宽度，可选）

int（缩放宽度，可选）

resized\_height

int（缩放高度，可选）

int（缩放高度，可选）

video\_start

float（截取起始时间，可选）

不适用

video\_end

float（截取结束时间，可选）

不适用

SFT 图片训练样例见下文标签页：

#### 普通 ChatML

普通 ChatML 格式样例（system/user/assistant 多轮对话）：

```
{
  "messages": [
    {"role": "system", "content": [{"text": "系统输入1"}]},
    {"role": "user", "content": [{"text": "用户输入1"}]},
    {"role": "assistant", "content": [{"text": "期望的模型输出1"}]},
    {"role": "user", "content": [{"text": "用户输入2"}]},
    {"role": "assistant", "content": [{"text": "期望的模型输出2"}]}
  ]
}
```

#### 深度思考（thinking）

深度思考（thinking）格式样例（思考标签放最后一条 assistant，前后换行必须保留）：

```
{
  "messages": [
    {"role": "system", "content": [{"text": "系统输入1"}]},
    {"role": "user", "content": [{"text": "用户输入1"}]},
    {"role": "assistant", "content": [{"text": "模型输出1"}]},
    {"role": "user", "content": [{"text": "用户输入2"}]},
    {"role": "assistant", "content": [{"text": "<think>\n期望的思考内容2\n</think>\n\n期望的输出2"}]}
  ]
}
```

#### 工具调用（function calling）

**说明****qwen3.5+**的模式支持使用工具调用数据格式。

工具调用（function calling）格式样例（tools 定义 + messages 多轮含 tool 角色，tool\_call\_id 一一对应）：

```
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "查询指定城市的实时天气",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {"type": "string", "description": "城市名称，例如：北京"}
          },
          "required": ["city"]
        }
      }
    }
  ],
  "messages": [
    {"role": "user", "content": [{"text": "帮我查一下北京的天气"}]},
    {
      "role": "assistant",
      "content": [{"text": "好的，我来帮您查询北京的天气。"}],
      "tool_calls": [
        {
          "id": "call_3a11c1ba883b41b6a4e0cb",
          "type": "function",
          "function": {
            "name": "get_weather",
            "arguments": "{\"city\": \"北京\"}"
          }
        }
      ]
    },
    {"role": "tool", "tool_call_id": "call_3a11c1ba883b41b6a4e0cb", "content": [{"text": "{\"city\": \"北京\", \"weather\": \"晴\", \"temperature\": \"25℃\"}"}]},
    {"role": "assistant", "content": [{"text": "北京今天天气晴朗，气温 25℃，适合出行。"}]}
  ]
}
```

#### 图片输入

图片加文本格式样例（content 数组含图片项与文本项）：

```
{
  "messages": [
    {"role": "system", "content": [{"text": "系统输入"}]},
    {
      "role": "user",
      "content": [
        {"text": "用户输入1"},
        {"image": "图像文件名1.jpg", "resized_width": 200, "resized_height": 200}
      ]
    },
    {"role": "assistant", "content": [{"text": "期望的模型输出1"}]}
  ]
}
```

#### 视频文件路径模式

视频文件路径模式格式样例（video 字段为视频文件路径字符串）：

```
{
  "messages": [
    {"role": "system", "content": [{"text": "系统输入"}]},
    {
      "role": "user",
      "content": [
        {"text": "用户输入1"},
        {"video": "视频文件名1.mp4", "fps": 3.0, "resized_width": 200, "resized_height": 200, "video_start": 0.0, "video_end": 3.0}
      ]
    },
    {"role": "assistant", "content": [{"text": "期望的模型输出1"}]}
  ]
}
```

#### 图片帧列表模式

图片帧列表模式格式样例（video 为帧列表，含 sample\_fps）：

```
{
  "messages": [
    {"role": "system", "content": [{"text": "系统输入"}]},
    {
      "role": "user",
      "content": [
        {"text": "用户输入2"},
        {"video": ["0.jpg", "1.jpg", "2.jpg", "3.jpg"], "sample_fps": 5.0, "resized_width": 200, "resized_height": 200}
      ]
    },
    {"role": "assistant", "content": [{"text": "期望的模型输出2"}]}
  ]
}
```

多模态理解定义详见[模型调优简介](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

### 工具调用格式说明

工具调用（function calling）模式在 messages 多轮结构基础上增加 tools 定义与 tool\_calls/role:tool 机制，字段约束如下：

-   tools：工具定义数组，每项含 type:"function" 与 function{name, description, parameters}；parameters 为 JSON Schema（含 type/properties/required）。
-   messages：多轮对话数组，角色含 user、assistant、tool。
-   content：多模态内容数组，可含 image、text、video 等项（与多模态理解格式一致）。
-   assistant.tool\_calls：模型生成的工具调用数组，含 id、type:"function"、function{name, arguments}；arguments 为 JSON 字符串。
-   role:"tool"：工具返回，tool\_call\_id 必须与对应 tool\_calls\[\].id 一一对应，content 内为工具返回结果。

多轮对话最后一条通常为 assistant 基于工具返回的最终答复。

百炼不支持 OpenAI 的 name、weight 参数，所有 assistant 输出都会被训练。从 OpenAI/Azure 迁移的训练数据不可携带 name/weight 字段。

数据多样性与均衡性建议：各场景数据数量应相对均衡，数据比例符合实际场景比例，避免某一类数据过多导致模型偏向于学习该类特征，影响泛化能力。

### 思考模式格式说明

深度思考内容用 `<think>\n…\n</think>\n\n` 标签包裹，置于 assistant 输出文本内（与最终答复同属最后一条 assistant 的 content）。规则：

-   只能放在最后一条 assistant 输出中；中间的 assistant 输出不加思考标签。
-   思考标签前后的换行符必须保留。
-   若训练样本设置模型不输出思考标签，训练完成后不建议再开启思考模式调用。

## RL 训练数据格式

强化学习（RL）训练数据采用 jsonl 格式，每行一个 JSON 对象，含 `messages` 与 `rollout_extra` 两个字段。RL 通过 SDK 上传（`AgenticRL.run()`），非控制台打包通道；计费按 MTU 模型训练单元，非 Token。RL 数据格式、SDK 上传与 Rollout/Reward 函数开发详见[强化学习训练概述](raw/model-user-guide/fine-tuning/rl-training/rl-training-overview.md)。

字段说明：

-   `messages`：用户问题，ChatML 结构（`[{role, content}]`）。只含 prompt（`user`，可前置 `system`），**不含**`assistant`**回答**——回答由模型在 Rollout 阶段自主生成。`content` 为字符串。
-   `rollout_extra`：参考答案或业务数据，dict 类型，透传给 Reward 函数用于评分。支持自定义 key（不限于 `solution`）；框架自动提取 `ground_truth`（参考答案），自定义 key 通过 `rollout_extra["key"]` 读取。

RL 数据**不含**`reward`**字段**——reward 由 Reward 函数在训练运行时计算（对比 `rollout_extra` 参考答案评分，输出 0~1 分），不预置在 jsonl 中。与 SFT（messages 含完整 assistant 答案）、DPO（chosen/rejected 对）不同，RL 的 messages 只有 prompt。

数学推理样例（`rollout_extra.solution` 标准答案）：

```
{"messages": [{"role": "user", "content": "Output the answer when you are ready. The answer should be surrounded by three sharps (###), in the form of ### ANSWER: <answer> ###. 6.6 minus x (3/2) times equals 5.6."}], "rollout_extra": {"solution": "2/3"}}
```

代码生成样例（`entry_point`/`tests`/`timeout_sec`/`language`）：

```
{"messages": [{"role": "user", "content": "Write a function add(a, b) that returns the sum of two integers."}], "rollout_extra": {"entry_point": "add", "tests": "def test_add():\n    assert add(1,2)==3\n    assert add(-1,1)==0\n", "timeout_sec": 10, "language": "python"}}
```

Agent 工具调用样例（`expected_tools`/`success_check`/`max_steps`）：

```
{"messages": [{"role": "user", "content": "查询订单 ORD-123 的物流状态并告知预计送达日期。"}], "rollout_extra": {"expected_tools": ["query_order", "get_logistics"], "success_check": "SELECT status FROM orders WHERE id='ORD-123'", "max_steps": 6}}
```

`rollout_extra` 常用 key（按场景）：

-   数学推理：`solution`（标准答案）、`solution_steps`（过程，可选）、`difficulty`（难度，可选）。
-   Agent 工具调用：`expected_tools`（期望工具集）、`success_check`（成功判定）、`max_steps`（调用效率参考）。
-   代码生成：`entry_point`（入口函数）、`tests`（单测代码）、`timeout_sec`（执行超时）、`language`（沙盒选型）。

RL 数据约束：

-   数据量需大于 `batch_size`（默认 64）。几十至几百条可验证方案；正式训练数学推理 500~2000 条、Agent ≥1000 条、代码 ≥1000 题，数据量越大效果越优。
-   训练集与验证集为两个独立 jsonl 文件，分别通过 `TrainingDataset`/`ValidationDataset` 上传（验证集可选）。
-   RL 通过 SDK 上传（`AgenticRL.run()`），非控制台打包通道；计费按 MTU 模型训练单元，非 Token。SDK 字段与提交方式详见[强化学习训练配置](raw/model-user-guide/fine-tuning/rl-training/rl-training-config-monitoring.md)。

## 多模态压缩包打包规则

多模态理解训练数据以 zip 压缩包形式通过**新增数据集**页面上传，打包须满足以下约束：

-   压缩包最大支持 2 GB。
-   包内文件夹与文件名允许的字符集为 ASCII 字母（a-z、A-Z）、数字（0-9）、下划线（\_）、连字符（-）。
-   训练文本数据文件固定为 data.jsonl，必须位于压缩包根目录——确保压缩后打开 zip 文件直接看到 data.jsonl，外层不能再包裹文件夹。

图片或视频文件名应在压缩包内全局唯一，即使分布在不同文件夹中。data.jsonl 内只需声明文件名而非文件路径——正确示例：image1.jpg；错误示例：jpg\_folder/image1.jpg。

云存储挂载不支持 zip 压缩包。使用云存储挂载加载数据集时，须将未经压缩的数据集文件夹整体上传到 OSS Bucket，通过 MountStorage 的 file\_path 指定 data.jsonl 文件路径；包含多文件时只需指定 data.jsonl 路径，其余同目录文件自动挂载。云存储挂载详见[使用 API 进行模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

命名示例与目录结构见下文代码块。云存储挂载授权操作见[在控制台进行模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)，OSS 导入 Bucket 标签打标操作见[训练集与评测集](raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

```
# 单层目录（推荐）
Trainingdata_vl.zip
  |--- data.jsonl        # 必须在根目录，外层不再包裹文件夹
  |--- image1.png
  |--- video1.mp4

# data.jsonl 内声明文件名（非路径）
# 正确：image1.jpg
# 错误：jpg_folder/image1.jpg
```

前往控制台[新增数据集](https://bailian.console.aliyun.com/#/efm/model_data/createDataAss)页面上传多模态压缩包并完成打包校验。

## 文件大小与数量限制

本地上传文件大小与数量上限按训练方式分场景设定，详见下文分场景表。图片准入限制见[视觉理解-SFT 格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-sft-image)，评测集格式限制见[评测集格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-eval-set)，日志回流入库限制见[评测集格式](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-eval-set)。

max\_length 取值区间 500 至 131072 为训练序列长度配置参数，非上传准入上限。单条训练数据上传准入大小上限以控制台页面展示为准。

本地上传文件大小与数量上限按训练方式分场景设定，推荐数据量为最低建议值：

**训练方式/场景**

**单文件大小上限**

**文件数量上限(maxCount)**

**推荐数据量**

文本生成 - SFT 格式

200 MB

10（默认）

至少上千条

文本生成 - DPO 格式

200 MB

10（默认）

至少上百条

文本生成 - CPT 格式

300 MB

1

至少 5000 万 Token

多模态（zip）

2 GB

1

根据实际场景准备充足样本

文件名（不含后缀）

≤120 字符且不重名

—

—

扩展名

须在 [新增数据集](https://bailian.console.aliyun.com/#/efm/model_data/createDataAss) 列表中

—

—

## API 上传配额

通过 DashScope API 上传调优文件（用途标记为模型调优）的配额见下文配额表。控制台创建数据集时，File API 列表最多支持 10 个文件合并注册；通过 API 上传的调优文件在控制台模型调优页面与 API 调用中均可见可用。

云存储挂载加载数据集的约束：

-   通过 MountStorage 的 file\_path 指定 data.jsonl 根目录清单路径，不支持 zip 压缩包。
-   选择云存储挂载存储位置时强制立即发布，不支持草稿状态。
-   挂载前需授权百炼服务访问 OSS 数据。

超限承接与加密：

-   单文件超过 300 MB：通过云存储挂载或多模态 ZIP 2 GB 通道上传。
-   总配额超额：删除历史文件释放空间。
-   导入数据自动启用 OSS 服务端加密（SSE-OSS，AES256）。

API 调用、认证、SDK、错误码、MountStorage 字段细节见[使用 API 进行模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

API 上传调优文件配额如下：

**配额项**

**限制值**

**说明**

单文件大小

不超过 300 MB

调优文件（模型调优用途）

有效文件总空间

100 GB

未删除文件累计

有效文件总数量

10000 个

未删除文件累计

文件存储时长

无时间限制

不自动过期

File API 列表上限

10 个

控制台创建数据集时合并注册

OSS 导入与云存储挂载的差异对比如下：

**维度**

**OSS 导入**

**云存储挂载**

前置条件

百炼数据访问授权标签

授权百炼服务访问 OSS 数据

数据形态

单个或批量文件

未经压缩的数据集文件夹整体（不支持 zip）

入口

数据管理 > 新增数据集 > OSS 导入

模型调优 > 创建训练任务 > 数据配置 > 数据集挂载

版本草稿

支持草稿与立即发布

强制立即发布（不支持草稿）

评测集

✗

✗

## 上传校验与常见错误

在**新增数据集**页面本地上传文件时，前端校验会拒绝不符合准入规则的文件并弹出提示。常见校验拒绝与上传出错场景见下文折叠项：

问题：上传文件时前端提示文件数量超过上限，文件被拒绝上传。

**定位：**maxCount 按训练方式设定——SFT/DPO 文本默认 10，多模态 zip 与 CPT 为 1。上传文件数超过对应训练方式的上限即被前端拒绝。

**处置：**按以下方式调整后重传：

1.  核对当前训练方式对应的 maxCount 上限，详见[文件大小与数量限制](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-size-limits)。
2.  减少文件数至上限内；多模态数据合并为单个 zip，CPT 数据合并为单个 jsonl。
3.  文件数仍超限时拆分为多个数据集分批上传。

问题：文件名（不含后缀）长度超过 120 字符，前端拒绝上传。

**定位：**文件名不含后缀上限 120 字符，且须仅含 ASCII 字母、数字、下划线、连字符。

**处置：**按以下方式调整后重传：

1.  重命名文件，使文件名（不含后缀）缩短至 120 字符以内。
2.  仅使用 a-z/A-Z/0-9/\_/- 字符，去除中文及其他非 ASCII 字符。
3.  多模态压缩包内文件名还须全局唯一。

问题：文件名（不含后缀比对）重复，前端拒绝上传。

**定位：**同一数据集内文件名不含后缀须唯一，比对时忽略扩展名。

**处置：**按以下方式调整后重传：

1.  排查重名文件，重命名使其不含后缀部分唯一。
2.  同名不同扩展名的文件（如 image.jpg 与 image.png）也会被判重名，须同时区分。
3.  多模态 zip 内文件名须全局唯一，即使分布在不同文件夹。

问题：单文件大小超过对应训练方式上限，前端拒绝上传。

**定位：**单文件大小上限按训练方式分场景——SFT/DPO 文本 200 MB、多模态 zip 2 GB、CPT 300 MB。

**处置：**按以下方式调整后重传：

1.  核对文件大小是否超过对应训练方式上限。
2.  拆分 jsonl 为多个文件分批上传（SFT/DPO）；CPT 数据拆分需新建多个数据集。
3.  单文件超 300 MB 的承接方式见[API 上传配额](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-api-quota)。

问题：文件扩展名不在 supportedExtension 列表，前端弹出 warning 并拒绝上传。

**定位：**扩展名须在支持列表内——文本训练用 jsonl，评测集用 xlsx，多模态图片支持 bmp/jpeg/jpg/png/tif/tiff/webp，多模态视频支持 mp4 等格式。

**处置：**按以下方式调整后重传：

1.  核对文件扩展名是否在对应场景的支持列表内。
2.  将文件转换为支持的扩展名后重新打包上传。
3.  多模态 zip 内图片与视频扩展名须逐一符合，否则整包导入失败。

问题：OSS 上传过程中文件被置为 error 状态，上传未完成。

**定位：**常见原因为 Bucket 标签缺失、百炼服务访问 OSS 授权异常或文件格式不符。

**处置：**按以下方式排查后重试：

1.  核对 OSS Bucket 已添加百炼数据访问授权标签。
2.  确认已授权百炼服务访问 OSS 数据。
3.  检查 data.jsonl 与文件格式符合打包规则后重试上传，详见[多模态压缩包打包规则](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-zip-package)。

不可逆操作风险提示：

-   发布与删除操作均不可逆；已发布版本不可再编辑，仅草稿版本可删除或在线编辑。
-   数据集类型（训练集/评测集）创建后不可变更、不可互换，选错需新建数据集重新导入全部数据。
-   切换数据集类型、训练场景、训练方式时会清空已上传文件并重置存储位置与导入方式。

验证集自动切分会从训练集中随机抽取 10% 数据作为验证集，减少实际训练数据量。小数据集建议选择独立验证集，验证集配置操作见[在控制台进行模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

建议先下载对应场景的数据模板，按模板结构准备数据可避免导入失败，数据模板下载建议见[概述](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-overview)。常见问题排障详见下文折叠项。草稿数据清洗与增强操作见[数据清洗或增强](raw/model-user-guide/model-data-overview/data-processing.md)，安全合规数据领域见[0 代码强化大模型安全合规能力](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

上传校验失败时，可前往控制台[新增数据集](https://bailian.console.aliyun.com/#/efm/model_data/createDataAss)页面核对文件格式与准入规则。
