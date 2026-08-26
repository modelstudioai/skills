# 查询模型列表

调用 GET /api/v1/models 接口查询百炼平台上可用的模型列表，支持按模型作者、模态类型、模型能力、部署模式等条件筛选，并获取模型的定价和上下文长度等信息。

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    > 调用时请将 `{WorkspaceId}` 替换为您的业务空间 ID。
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models`
    
    新加坡
    
    `[https://dashscope-intl.aliyuncs.com/api/v1/models](https://dashscope-intl.aliyuncs.com/api/v1/models)`
    
    中国香港
    
    `[https://cn-hongkong.dashscope.aliyuncs.com/api/v1/models](https://cn-hongkong.dashscope.aliyuncs.com/api/v1/models)`
    
    日本（东京）
    
    `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/models`
    
    德国（法兰克福）
    
    `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/models`
    
    美国（弗吉尼亚）
    
    `https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/models`
    
-   **认证方式**
    
    在请求 Header 中设置 `Authorization: Bearer {API_KEY}`。
    

## 请求参数

所有参数均通过 Query String 传递。

**参数**

**类型**

**必选**

**描述**

name

String

否

按模型名称进行模糊搜索。示例：`qwen`

model

String

否

按模型 ID 进行精确查询。示例：`qwen3-max`

language

String

否

返回结果的语言。可选值：`zh-CN`（中文）、`en-US`（英文）。

page\_no

Integer

否

页码，从 1 开始。默认值：`1`。

page\_size

Integer

否

每页返回的模型数量。默认值：`20`。

providers

Array\[String\]

否

供应商，可选值

-   qwen：阿里巴巴-千问
    
-   zhipu-ai：智谱AI
    
-   wan：阿里巴巴-万相
    
-   qwen-domain-model：阿里巴巴-领域模型
    
-   mini-max：MiniMax
    
-   moonshot-ai：月之暗面
    
-   deepseek：DeepSeek
    
-   happyhorse：阿里巴巴-HappyHorse
    
-   kling：可灵AI
    
-   pixverse：PixVerse
    
-   vidu：Vidu
    
-   tripo：Tripo
    
-   xiaomi：小米MiMo
    

inference\_providers

Array\[String\]

否

按推理服务供应商筛选。可选值：

-   aliyun-bailian：阿里云百炼
    
-   alibaba-cloud-modelstudio：Alibaba Cloud Model Studio
    
-   siliconflow：硅基流动
    
-   moonshot：Kimi
    
-   mini-max：MiniMax
    
-   kling：Kling AI
    
-   vidu：Vidu
    
-   pixverse：PixVerse
    
-   vanchin：快手万擎
    
-   xiaomi：小米MiMo
    
-   zhipu-ai：Zhipu AI
    
-   tripo：Tripo
    

capabilities

Array\[String\]

否

模型类型，可选值

-   Reasoning :深度思考
    
-   VU :视觉理解
    
-   IG :图片生成
    
-   VG :视频生成
    
-   ASR :语音识别
    
-   TTS :语音合成
    
-   ME :多模态向量
    
-   Realtime-Omni :实时全模态
    
-   Multimodal-Omni :全模态
    
-   Realtime-Text-to-Speech :实时语音合成
    
-   TG :文本生成
    
-   TR :文本向量
    
-   Realtime-ASR :实时语音识别
    
-   Realtime-Audio-Translate :实时语音翻译
    
-   3D-generation :3D 生成
    
-   Realtime-Chatting :实时语音对话
    

features

Array\[String\]

否

模型能力，可选值

-   model-experience :模型体验
    
-   function-calling :function calling
    
-   structured-outputs :结构化输出
    
-   web-search :联网搜索
    
-   prefix-completion :前缀续写
    
-   cache :cache缓存
    
-   batch :批量推理
    
-   fine-tuning :模型调优
    

context\_window

Integer

否

按上下文长度筛选，返回上下文长度大于等于该值的模型。示例：`20000`

service\_site

String

否

按部署模式筛选。不传时返回所有部署模式的模型。可选值：

-   global：全球
    
-   international：国际
    
-   asia-pacific-china：中国
    
-   cn-hongkong：中国香港
    
-   european-union：欧盟
    
-   united-states：美国
    
-   japan：日本
    

supports

Array\[String\]

否

按模型支持的应用场景筛选。默认值：`inference`。可选值：

-   `inference`：支持推理的模型
    
-   `deploy`：支持部署的模型
    

deployment\_methods

Array\[String\]

否

按部署方式筛选。可选值：

-   `ptu`：预置吞吐量（Provisioned Throughput Unit）
    

deployment\_ptu\_service\_tiers

Array\[String\]

否

按 PTU 类型筛选，使用时需同时设置 `deployment_methods` 包含 `ptu`。

## 返回参数

**参数**

**类型**

**描述**

request\_id

String

请求 ID，用于问题排查。

output.total

Number

符合条件的模型总数。

output.page\_no

Number

当前页码。

output.page\_size

Number

每页条数。

output.models\[\].model

String

模型 ID，用于 API 调用时指定模型。

output.models\[\].name

String

模型的名称。

output.models\[\].description

String

模型的功能描述。

output.models\[\].provider

String

模型作者，如 `qwen`。

output.models\[\].inference\_provider

String

推理服务供应商，如 `aliyun-bailian`。

output.models\[\].capabilities

Array\[String\]

模型支持的模态类型，取值与请求参数 `capabilities` 一致。

output.models\[\].features

Array\[String\]

模型支持的能力列表，取值与请求参数 `features` 一致。

output.models\[\].published\_time

String

模型发布时间，格式：`yyyy-MM-dd HH:mm:ss`。可能为 `null`。

output.models\[\].inference\_metadata

Object

模型的输入输出模态信息，包含以下字段：

-   `request_modality`（Array\[String\]）：输入模态，可选值为 `Text`、`Image`、`Audio`、`Video`。
    
-   `response_modality`（Array\[String\]）：输出模态，可选值同上。
    

output.models\[\].model\_info

Object

模型的上下文长度信息，包含以下字段（值为 `null` 表示无限制或不适用）：

-   `context_window`（Integer）：上下文窗口总长度
    
-   `max_input_tokens`（Integer）：最大输入 Token 数
    
-   `max_output_tokens`（Integer）：最大输出 Token 数
    
-   `max_reasoning_tokens`（Integer）：最大推理 Token 数
    
-   `reasoning_max_input_tokens`（Integer）：最大输入（思考）
    
-   `reasoning_max_output_tokens`（Integer）：最大输出（思考）
    

output.models\[\].prices

Array\[Object\]

模型定价信息。每个元素包含：

-   `range_name`（String）：分段名称。如无分段计费则为 `Default`，如有分段则为具体区间（如 `32k<Input<=128k`）。
    
-   `prices`（Array\[Object\]）：价格列表，每项包含 `type`（计费项）、`price`（单价）、`price_unit`（单位，如"每百万tokens"）、`price_name`（价格描述，如"输入"）。
    

output.models\[\].equivalent\_snapshot

String

对应的快照模型

## 请求示例

**示例一：查询所有文本生成模型**
```
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models?capabilities=TG&page_no=1&page_size=20" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```
**示例二：查询 Qwen 系列的推理模型**
```
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models?providers=qwen&capabilities=TG&capabilities=Reasoning&page_no=1&page_size=100" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```

## 返回示例

```
{
    "code": null,
    "message": null,
    "success": true,
    "output": {
        "total": 168,
        "page_no": 1,
        "page_size": 10,
        "models": [
            {
                "model": "qwen3-max",
                "name": "通义千问3-Max",
                "description": "通义千问3系列Max模型，适配场景更加复杂的智能体需求。",
                "features": [
                    "function-calling",
                    "structured-outputs",
                    "web-search"
                ],
                "prices": [
                    {
                        "prices": [
                            {
                                "type": "input_token",
                                "price": "2",
                                "price_unit": "每百万tokens",
                                "price_name": "输入"
                            },
                            {
                                "type": "output_token",
                                "price": "8",
                                "price_unit": "每百万tokens",
                                "price_name": "输出"
                            }
                        ],
                        "range_name": "Default"
                    }
                ],
                "published_time": "2025-11-11 12:00:00",
                "inference_metadata": {
                    "response_modality": ["Text"],
                    "request_modality": ["Text"]
                },
                "model_info": {
                    "context_window": 131072,
                    "max_input_tokens": 130048,
                    "max_output_tokens": 16384,
                    "max_reasoning_tokens": null
                }
            },
            {
                "model": "qwen-image-max",
                "name": "Qwen-Image-Max",
                "description": "通义千问图像生成模型Max系列。",
                "features": ["model-experience"],
                "prices": [
                    {
                        "prices": [
                            {
                                "type": "image_number",
                                "price": "0.075",
                                "price_unit": "每张",
                                "price_name": "图像生成"
                            }
                        ],
                        "range_name": "Default"
                    }
                ],
                "published_time": null,
                "inference_metadata": {
                    "response_modality": ["Image"],
                    "request_modality": ["Text"]
                },
                "model_info": {
                    "context_window": null,
                    "max_input_tokens": null,
                    "max_output_tokens": null,
                    "max_reasoning_tokens": null
                }
            }
        ]
    },
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
