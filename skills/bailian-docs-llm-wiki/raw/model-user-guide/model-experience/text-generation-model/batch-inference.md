# 批量推理

对于无需实时响应的推理场景，批量推理能异步处理大批量的数据请求，成本仅为实时推理的 50% ，且接口兼容 OpenAI，适合执行模型评测、数据标注等批量作业。

## 工作原理

1.  提交任务：上传包含多个请求的 JSONL 文件，创建批量推理任务。
2.  异步处理：系统在后台队列中处理任务。可通过控制台或API查询任务进度和状态。
3.  下载结果：任务完成后，系统生成结果文件（记录成功响应）和错误文件（记录失败详情，如有）。

## 适用范围

#### 华北2（北京）

**支持的模型：**

-   **文本生成模型**
    -   千问 Max：qwen3.8-max、qwen3.7-max、qwen3-max
    -   千问 Plus：qwen3.7-plus、qwen3.6-plus、qwen3.5-plus、qwen-plus、qwen-plus-latest
    -   千问 Flash：qwen3.8-flash、qwen3.7-flash、qwen3.6-flash、qwen3.5-flash、qwen-flash
    -   千问 Long：qwen-long、qwen-long-latest
    -   第三方模型：deepseek-r1、deepseek-v3.2、deepseek-v3
-   **多模态模型**
    -   [图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)：qwen3.8-max、qwen3.8-flash、qwen3.7-plus、qwen3.6-plus、qwen3.7-flash、qwen3.6-flash、qwen3.5-plus、qwen3.5-flash、qwen3-vl-plus、qwen3-vl-flash
    -   [文字提取](raw/model-user-guide/model-experience/vision-model/qwen-vl-ocr.md)：qwen-vl-ocr、qwen-vl-ocr-latest
    -   [全模态](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)：qwen3.5-omni-plus、qwen3.5-omni-flash
-   [向量模型](raw/model-user-guide/model-experience/embedding-rerank-model/embedding.md)**：**text-embedding-v1、text-embedding-v2、text-embedding-v3、text-embedding-v4、qwen3.7-text-embedding、qwen3.7-text-embedding-flash
    

**重要**

-   在Batch 场景下，`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.7-flash`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash`、`qwen3.5-omni-flash`和`qwen3.5-omni-plus`单次请求的上下文 Token 数最大支持 256K，`qwen3.5-omni-plus`、`qwen3.5-omni-flash`不支持语音输出。
-   部分模型支持思考模式，开启后会产生思考`tokens`导致成本增加。
-   `qwen3.8`、`qwen3.7`、`qwen3.6`和`qwen3.5` 系列模型默认开启思考模式。建议使用混合思考模型时，显式设置`enable_thinking`参数（`true`开启/`false`关闭）。
-   在 JSONL 请求体中，`enable_thinking` 为 `body` 的顶层参数，须与 `model` 同级传入，不能放在 `extra_body` 中。
-   批量推理结果文件不包含 `reasoning_content` 字段。即使设置 `enable_thinking=true`，结果文件中 `choices[0].message` 也仅包含 `content` 和 `role` 字段。如需获取思考过程内容，请使用实时 API 调用（流式、非流式均可，设置 `enable_thinking=true` 即可），详情请参见[深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)。

#### 新加坡

**支持的模型**：qwen-max、qwen-plus、qwen-turbo。

## 使用批量推理

### 步骤一：准备输入文件

创建任务前，准备一个符合以下规范的 JSONL 文件：

-   **格式**：UTF-8 编码的 JSONL（每行一个独立JSON对象）。
    
-   **规模限制**：单文件 ≤ 50,000 个请求，且 ≤ 500 MB。
    
    > 数据量超出此限制时，拆分为多个任务分别提交。
    
-   **单行限制**：每个JSON对象 ≤ 1 MB，且不超过模型上下文长度。
    
-   **一致性要求**：同一文件内所有请求须使用相同模型及思考模式（如适用）。
    
-   **唯一标识**：每个请求必须包含文件内唯一的 custom\_id 字段，用于结果匹配。`custom_id` 最大支持 256 个字符，超过此限制将导致任务校验失败。如需回传更长的标识信息，可在创建任务时通过 `metadata` 的自定义字段实现，详见[使用 metadata 回传自定义标识](https://help.aliyun.com/zh/model-studio/batch-inference#f5a3d8e2b7y6x)。
    
-   **媒体文件地址**：多模态请求的 `body` 中通过 `image_url`、`video_url` 等字段引用的媒体文件，必须使用公网可访问的 URL。不支持本地文件路径（如 `file:///home/user/test.mp4`）和内网地址；使用此类地址创建的任务虽可提交成功，但不会被处理完成，请先将文件上传至公网可访问的存储再引用其 URL。
    

每个JSON对象须遵循以下字段规范：

字段

类型

是否必填

说明

`custom_id`

string

是

请求的唯一标识符

`method`

string

是

HTTP 方法，仅支持 `POST`

`url`

string

是

请求端点。文本生成与多模态模型填写 `/v1/chat/completions`，向量模型填写 `/v1/embeddings`

`body`

object

是

请求体，格式与所填 `url` 对应接口（/v1/chat/completions 或 /v1/embeddings）一致

#### 示例文件

可下载示例文件[test\_model.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250926/wrheek/test_model.jsonl)，内容为：

```
{"custom_id":"1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-max","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"你好！有什么可以帮助你的吗？"}]}}
{"custom_id":"2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-max","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is 2+2?"}]}}
```
**Batch 推理 JSONL 文件生成工具**

Batch 推理需要构造 JSONL 文件，每行为一个独立请求。以下 Python 脚本可直接运行生成符合格式的 JSONL 文件。

#### 使用方式

1.  将以下代码保存为 `generate_batch_jsonl.py`
2.  修改脚本中 `TASKS` 列表的请求内容
3.  运行 `python generate_batch_jsonl.py`
4.  生成的 `batch_input.jsonl` 文件可直接用于 Batch 推理任务

##### 文本生成模型 JSONL 生成脚本

```
#!/usr/bin/env python3
"""
Batch 推理 JSONL 文件生成工具

支持的地域与模型请参见上方“适用范围”。

文件大小限制：单行 ≤6MB，总文件 ≤500MB，建议 ≤10000 行

使用方式：
  1. 修改下方 TASKS 列表
  2. 运行: python generate_batch_jsonl.py
  3. 输出: batch_input.jsonl
"""
import json

# ═══════════════════════════════════════════════════════
# 配置区：修改以下内容来生成您需要的 JSONL
# ═══════════════════════════════════════════════════════

MODEL = "qwen-max"          # 选择模型（参见上方“适用范围”）
ENABLE_THINKING = False     # 是否开启思考模式（仅部分模型支持）
THINKING_BUDGET = 50        # 思考 token 预算（思考模式下生效）

# 任务列表：每个 dict 代表一条用户消息
TASKS = [
    {"role": "user", "content": "你好！请介绍一下自己。"},
    {"role": "user", "content": "What is 2+2?"},
    {"role": "user", "content": "请用Python写一个快速排序算法"},
]

# ═══════════════════════════════════════════════════════
# 以下为生成逻辑，一般无需修改
# ═══════════════════════════════════════════════════════

def build_request(custom_id: str, model: str, messages: list,
                  enable_thinking: bool = False, thinking_budget: int = 50) -> dict:
    """构造单条 Batch 请求"""
    body = {"model": model, "messages": messages}
    if enable_thinking:
        body["enable_thinking"] = True
        body["thinking_budget"] = thinking_budget
        body["stream"] = True  # 思考模式需开启 stream
    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": body
    }

def main():
    output_file = "batch_input.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for i, task in enumerate(TASKS, 1):
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                task
            ]
            req = build_request(
                custom_id=f"request-{i}",
                model=MODEL,
                messages=messages,
                enable_thinking=ENABLE_THINKING,
                thinking_budget=THINKING_BUDGET
            )
            f.write(json.dumps(req, ensure_ascii=False) + "\n")
    print(f"已生成 {output_file}，共 {len(TASKS)} 条请求")

if __name__ == "__main__":
    main()
```

##### 多模态模型请求格式

多模态模型的 `content` 字段为数组格式，包含媒体对象和文本提问。每行请求中的媒体URL需为同一类型（图片、视频或音频）。将上方脚本中的 `TASKS` 替换为以下格式即可：

```
# 多模态模型配置示例
MODEL = "qwen-vl-max"       # 多模态模型

# 多模态任务：content 为数组格式
TASKS = [
    {"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": "https://example.com/image1.jpg"}},
        {"type": "image_url", "image_url": {"url": "https://example.com/image2.jpg"}},
        {"type": "text", "text": "这些图描绘了什么内容？"}
    ]},
]

# qwen-omni-turbo 音频/视频格式：
# {"type": "input_audio", "input_audio": {"data": "https://example.com/audio.wav", "format": "wav"}}
# {"type": "video_url", "video_url": "https://example.com/video.mp4"}

# 注意：
# - qwen3-vl-plus 和 qwen3-vl-flash 不使用 system 角色，thinking_budget 设置为 500
# - 其他多模态模型包含 system 角色，thinking_budget 设置为 50
# - 思考模式需额外设置 ENABLE_THINKING = True
```

##### 向量模型请求格式

向量模型使用 `/v1/embeddings` 接口，请求格式不同于文本生成模型。可使用以下独立脚本生成：

```
#!/usr/bin/env python3
"""向量模型 Batch JSONL 生成（使用 /v1/embeddings 接口）"""
import json

MODEL = "text-embedding-v3"  # 向量模型，可选型号参见上方“适用范围”

TEXTS = [
    "衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买。",
    "风急天高猿啸哀",
    "The quick brown fox jumps over the lazy dog",
]

output_file = "batch_embedding.jsonl"
with open(output_file, "w", encoding="utf-8") as f:
    for i, text in enumerate(TEXTS, 1):
        req = {
            "custom_id": f"emb-{i}",
            "method": "POST",
            "url": "/v1/embeddings",
            "body": {"model": MODEL, "input": text, "encoding_format": "float"}
        }
        f.write(json.dumps(req, ensure_ascii=False) + "\n")
print(f"已生成 {output_file}，共 {len(TEXTS)} 条请求")
```

#### 在批量推理中配置思考模式

部分模型（如 qwen3.7-plus、qwen3.7-max 及 qwen3.6、qwen3.5 系列）默认开启思考模式，会产生额外的思考 Token。如需在批量推理中配置思考模式，请在 JSONL 文件每行请求的 `body` 中设置 `enable_thinking` 参数，与 `model` 同级放置。可选参数 `thinking_budget` 用于限制思考 Token 数量上限。

**重要**`enable_thinking` 和 `thinking_budget` 必须直接放在 `body` 最外层（与 `model` 同级）。请勿将其放入 `extra_body` 中——`extra_body` 是 OpenAI Python SDK 用于透传非标准参数的机制，仅在实时推理的 SDK 调用中有效，在批量推理的 JSONL 文件中不适用。

示例：关闭思考模式

```
{"custom_id":"request-1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen3.5-plus","enable_thinking":false,"messages":[{"role":"user","content":"你好"}]}}
```

示例：开启思考模式并限制思考 Token 预算

```
{"custom_id":"request-2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen3.5-plus","enable_thinking":true,"thinking_budget":50,"messages":[{"role":"user","content":"请分析以下问题"}]}}
```

### 步骤二：创建批量推理任务

1.  在\*\*[批量推理](https://bailian.console.aliyun.com/model/batch)\*\*页面，单击**创建批量推理任务**。
    
2.  在弹出的对话框中：填写**任务名称**和**任务描述**，设置**最长等待时间**（1–14 天），上传 JSONL 文件。
    
    > 可单击 **下载示例文件** 获取模板。
    
3.  填写完成后，单击**确认**。
    

### 步骤三：监控和管理任务

-   **查看**：
    
    -   在任务列表页，查看任务的**进度**（已处理请求数/总请求数）和**状态**。
    -   按任务名称或ID搜索，或按业务空间筛选，快速定位目标任务。
-   **管理**：
    
    -   取消："执行中"的任务可在**操作**列取消。
    -   排错："失败"的任务可悬停状态查看错误概要，下载错误文件查看详情。例如，若批次文件中混用了不同模型，任务将显示**失败**状态，错误信息示例：`The model 'qwen-turbo' for this request does not match the rest of the batch. Each batch must contain requests for a single model.`

### 步骤四：下载结果

**重要**任务结束超过 30 天将自动删除，请及时下载结果。

任务完成后，单击**查看结果**，下载产出文件：

-   **结果文件**：记录所有成功请求及其 `response` 结果。
-   **错误文件（如有）**：记录所有失败请求及其 `error` 详情。

两个文件均包含 `custom_id` 字段，用于与原始输入数据匹配，关联结果或定位错误。

### 步骤五：查看用量统计（可选）

在[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面，筛选并查看批量推理的用量统计。

-   **查看数据概览**：**选择时间**（最长 30 天），将**推理类型**选为**批量推理**，查看批量推理的模型调用概览。
    
-   **查看模型详情**：
    
    -   单击模型类别（如**大语言模型**）进入详情页，**选择时间**（最长 30 天），将**推理类型**选为**批量推理**，查看该类别模型的调用信息。
    -   单击目标模型右侧的**查看详情**，查看单模型的调用情况。

**重要**

-   批量推理的调用数据以**任务结束时间**为准进行统计。正在运行的任务，其调用信息在任务完成前无法查询到。
-   监控数据存在 1～2 小时延迟。

## 使用 metadata 回传自定义标识

`custom_id` 最大支持 256 个字符。如需在结果文件中回传更长的标识信息，可使用 `metadata` 的自定义字段实现。

### metadata 字段说明

`metadata` 是创建 Batch 任务时的可选参数，支持以下字段：

-   `ds_name`：任务名称，设置后将显示在控制台的**任务名称**列。
-   `ds_description`：任务描述，设置后将显示在控制台的**任务描述**列。
-   **自定义字段**：除上述官方字段外，`metadata` 还支持任意自定义字段，且自定义字段的值**不受 256 个字符的限制**。查询任务详情时，所有自定义字段会完整回传。

### 代码示例

以下示例展示如何通过 `metadata` 的自定义字段回传超过 256 个字符的标识信息：

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

batch = client.batches.create(
    input_file_id="file-batch-xxxxxxxxxxxxxxxxxxxx",
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "ds_name": "my_batch_task",
        "ds_description": "批量推理任务描述",
        "my_custom_field": "此字段的值可以超过256个字符，用于回传更长的标识信息..."
    }
)
print(batch)
```

任务创建成功后，通过查询任务详情接口（`GET /v1/batches/{batch_id}`）可获取完整的 `metadata` 信息，包括所有自定义字段及其完整内容。

## API 参考

在生产环境中，使用兼容 OpenAI 的API自动化创建和管理 Batch 任务。核心流程如下：

**重要**批量推理仅支持 OpenAI 兼容格式的 API 调用。使用 OpenAI Python SDK 时，需将 `base_url` 设置为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。DashScope Python SDK（`dashscope` 包）不提供批量推理接口，无法通过 `dashscope.BatchInference`、`dashscope.Batches` 等方式提交批量推理任务。

示例：

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
batch = client.batches.create(
    input_file_id=file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
)
```

1.  [上传文件](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
    
    调用 `POST /v1/files` 上传文件，记录返回的文件 ID。
    
2.  [创建任务](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)传入文件ID 或OSS路径，调用 `POST /v1/batches` 创建任务，记录返回的 `batch_id`。
    
3.  [轮询状态](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)使用 `batch_id` 轮询 `GET /v1/batches/{batch_id}`。当 `status` 变为 `completed` 时，记录 `output_file_id` 并停止轮询。
    
4.  [下载结果](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)使用 `output_file_id` 调用 `GET /v1/files/{output_file_id}/content`，下载结果文件。
    

完整的 Batch API接口定义和代码示例，请参见[OpenAI兼容-Batch（文件输入）](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 任务生命周期

状态

说明

**validating（验证中）**

系统正在校验文件格式（JSONL 规范）及每行请求的API格式合法性。

**in\_progress（执行中）**

文件验证通过，系统已开始逐行处理推理请求。

**finalizing（****执行中****）**

所有请求均已处理完毕，结果正在分别写入结果文件和错误文件。在控制台任务列表中，此阶段与 in\_progress 共用**执行中**状态标签，无独立展示文案。

**completed（已完成）**

结果文件和错误文件已写入完成，可下载。

**failed（失败）**

任务在 validating 阶段失败，通常由文件级错误（如 JSONL 格式错误、文件过大）导致。此状态下不会执行任何推理请求，也不会生成结果文件。

**expired（已终止）**

任务运行时间超过创建时设定的最长等待时间，被系统终止。创建新任务时，建议设置更长的等待时间。

**cancelled（已终止）**

用户取消任务，未开始处理的请求将被终止。

## 计费说明

-   **计费单价：** 所有成功请求的输入和输出 Token，单价均为对应模型实时推理价格的 **50%**，具体请参见[模型列表](raw/model-user-guide/get-started-with-models/models.md)。
    
-   **计费范围：**
    -   仅对任务中成功执行的请求计费。
    -   文件解析失败、任务执行失败、或行级错误请求均**不产生费用**。
    -   对于被取消的任务，在取消前已成功完成的请求仍正常计费。

**说明**

-   批量推理为独立计费项，支持[AI 通用型节省计划](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，但不支持[预付费](https://common-buy.aliyun.com/?commodityCode=sfm_llminference_spn_public_cn)（节省计划）、[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)等优惠，以及[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)等功能。
-   部分模型（如 qwen3.7-plus、qwen3.7-max 及 qwen3.6、qwen3.5 系列）默认开启思考模式，会产生额外的思考 Token，并按输出 Token 价格计费，导致成本增加。建议根据任务复杂度设置 enable\_thinking 参数以控制成本，具体请参考[深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)。

## 常见问题

1.  **使用批量推理需要额外购买或开通吗？**
    
    不需要。开通阿里云百炼服务后即可使用，费用按**后付费模式**从账户余额中扣除。
    
2.  **任务提交后为什么立即失败（状态变为 failed）？**
    
    这通常是文件级错误导致的，任务并未执行任何推理请求。按以下顺序排查：
    
    -   **文件格式**：是否为严格的 JSONL 格式，每行一个完整的JSON对象。
    -   **文件规模**：文件大小、行数等是否超出限制。详情请参见[准备输入文件](https://help.aliyun.com/zh/model-studio/batch-inference#cdb5ab7b74k2t)。
    -   **模型一致性**：检查文件中所有请求的 `body.model` 字段是否完全一致，且使用的是当前地域支持的模型。
3.  **任务处理需要多长时间？**
    
    处理时长主要取决于系统当时的负载。系统繁忙时任务可能需要排队，成功或失败都会在设定的最长等待时间内返回结果。
    

## 错误码

如果调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
