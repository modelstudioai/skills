# 查询模型列表

查询百炼平台上可用的模型列表，支持按模型作者、模态类型、模型能力、部署模式等条件筛选，并获取模型的定价和上下文长度等信息。

#### 华北2（北京）

GET`https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/models`

#### 新加坡

GET`https://WorkspaceId.ap-southeast-1.maas.aliyuncs.com/api/v1/models`

#### 中国香港

GET`https://WorkspaceId.cn-hongkong.maas.aliyuncs.com/api/v1/models`

#### 日本（东京）

GET`https://WorkspaceId.ap-northeast-1.maas.aliyuncs.com/api/v1/models`

#### 德国（法兰克福）

GET`https://WorkspaceId.eu-central-1.maas.aliyuncs.com/api/v1/models`

#### 美国（弗吉尼亚）

GET`https://dashscope-us.aliyuncs.com/api/v1/models`

## 请求头

`Authorization`String必填

格式为 `Bearer <API Key>`。在所选地域的 [API Key 管理](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)页面选择业务空间并获取 API Key。

## 查询参数

`name`String可选

按模型名称进行模糊搜索。示例：`qwen`

`model`String可选

按模型 ID 进行精确查询。示例：`qwen3.8-max`

`language`String可选

返回结果的语言。

-   `zh-CN`：中文
-   `en-US`：英文

`page_no`Integer可选

页码，从 1 开始。默认值：`1`。查询后续页时递增 `page_no`，根据响应中 `output` 下的 `total` 字段判断是否读完。

`page_size`Integer可选

每页返回的模型数量。默认值：`20`。

`providers`Array\[String\]可选

按模型作者筛选。DashScope Python SDK 2.x 的 `provider` 参数只在客户端筛选当前页，返回对象的 `total_count` 仍为筛选前的总数。

点击查看可选值

-   `qwen`：阿里巴巴-千问
-   `zhipu-ai`：智谱AI
-   `wan`：阿里巴巴-万相
-   `qwen-domain-model`：阿里巴巴-领域模型
-   `mini-max`：MiniMax
-   `moonshot-ai`：月之暗面
-   `deepseek`：DeepSeek
-   `happyhorse`：阿里巴巴-HappyHorse
-   `kling`：可灵AI
-   `pixverse`：PixVerse
-   `vidu`：Vidu
-   `tripo`：Tripo
-   `xiaomi`：小米MiMo

`inference_providers`Array\[String\]可选

按推理服务供应商筛选。

点击查看可选值

-   `aliyun-bailian`：阿里云百炼
-   `alibaba-cloud-modelstudio`：Alibaba Cloud Model Studio
-   `siliconflow`：硅基流动
-   `moonshot`：Kimi
-   `mini-max`：MiniMax
-   `kling`：Kling AI
-   `vidu`：Vidu
-   `pixverse`：PixVerse
-   `vanchin`：快手万擎
-   `xiaomi`：小米MiMo
-   `zhipu-ai`：Zhipu AI
-   `tripo`：Tripo

`capabilities`Array\[String\]可选

按文本生成、深度思考等模型能力筛选。此参数需通过 HTTP API 使用。

点击查看可选值

-   `Reasoning`：深度思考
-   `VU`：视觉理解
-   `IG`：图片生成
-   `VG`：视频生成
-   `ASR`：语音识别
-   `TTS`：语音合成
-   `ME`：多模态向量
-   `Realtime-Omni`：实时全模态
-   `Multimodal-Omni`：全模态
-   `Realtime-Text-to-Speech`：实时语音合成
-   `TG`：文本生成
-   `TR`：文本向量
-   `Realtime-ASR`：实时语音识别
-   `Realtime-Audio-Translate`：实时语音翻译
-   `3D-generation`：3D 生成
-   `Realtime-Chatting`：实时语音对话

传入多个值时重复参数名，例如 `capabilities=TG&capabilities=Reasoning`，返回支持文本生成或深度思考的模型。

`features`Array\[String\]可选

按模型特性筛选，如 function calling 和结构化输出。 此参数需通过 HTTP API 使用。

-   `model-experience`：模型体验
-   `function-calling`：function calling
-   `structured-outputs`：结构化输出
-   `web-search`：联网搜索
-   `prefix-completion`：前缀续写
-   `cache`：cache缓存
-   `batch`：批量推理
-   `fine-tuning`：模型调优

`context_window`Integer可选

按上下文长度筛选，返回上下文长度严格小于该值的模型。示例：`20000`。

`service_site`String可选

按部署模式筛选。不传时返回所有部署模式的模型。

-   `global`：全球
-   `international`：国际
-   `asia-pacific-china`：中国
-   `cn-hongkong`：中国香港
-   `european-union`：欧盟
-   `united-states`：美国
-   `japan`：日本

`supports`Array\[String\]可选

按模型支持的应用场景筛选。默认值：`inference`。

-   `inference`：支持推理的模型
-   `deploy`：支持部署的模型

`deployment_methods`Array\[String\]可选

按部署方式筛选。

-   `ptu`：预置吞吐量（Provisioned Throughput Unit）

`deployment_ptu_service_tiers`Array\[String\]可选

按 PTU 类型筛选，使用时需同时设置 `deployment_methods` 包含 `ptu`。

## 返回参数

`code`String | null

错误码。查询成功时为 `null`。

`message`String | null

错误信息。查询成功时为 `null`。

`success`Boolean

查询是否成功。

`output`Object

模型列表及分页信息。

查看子字段

`total`Number

符合条件的模型总数。DashScope Python SDK 2.x 在返回对象的 `total_count` 字段中提供该值。

`page_no`Number

当前页码。

`page_size`Number

每页条数。

`models`Array\[Object\]

模型列表，每个元素为一个模型对象。分页响应示例仅保留一条模型记录。

查看子字段

`model`String

模型 ID，用于 API 调用时指定模型。

`name`String

模型的名称。

`description`String

模型的功能描述。

`provider`String

模型作者，如 `qwen`。

`capabilities`Array\[String\]

模型支持的能力，取值与查询参数 `capabilities` 一致。

`inference_provider`String

推理服务供应商，如 `aliyun-bailian`。

`features`Array\[String\]

模型支持的特性，取值与查询参数 `features` 一致。

`prices`Array\[Object\]

模型定价信息，按计费区间返回。

查看子字段

`prices`Array\[Object\]

该计费区间的价格列表。

查看子字段

-   `type`：计费项。
-   `price`：单价。
-   `price_unit`：单位，如“每百万tokens”。
-   `price_name`：价格描述，如“输入”。
-   `time_band`（String）：该价格条目的时段标识。示例值为 `standard`。

`range_name`String

分段名称。无分段计费时为 `Default`，有分段计费时为具体区间，如 `32k<Input<=128k`。

`published_time`String

模型发布时间，格式：`yyyy-MM-dd HH:mm:ss`。可能为 `null`。

`inference_metadata`Object

模型的输入输出模态信息。

查看子字段

-   `response_modality`（Array\[String\]）：输出模态。
-   `request_modality`（Array\[String\]）：输入模态。

输入和输出模态的可选值：

-   `Text`
-   `Image`
-   `Audio`
-   `Video`

`model_info`Object

模型的上下文长度信息。字段值为 `null` 表示无限制或不适用。

查看子字段

-   `context_window`（Integer）：上下文窗口总长度
-   `max_input_tokens`（Integer）：最大输入 Token 数
-   `max_output_tokens`（Integer）：最大输出 Token 数
-   `max_reasoning_tokens`（Integer）：最大推理 Token 数
-   `reasoning_max_input_tokens`（Integer）：最大输入（思考）
-   `reasoning_max_output_tokens`（Integer）：最大输出（思考）

`equivalent_snapshot`String

对应的快照模型

`inference_offline_info`Object

推理场景下线信息。

查看子字段

下线信息条目（`$`）包含以下字段。

`offline_time`Date

预计下线时间。

`request_id`String

请求 ID，用于问题排查。

#### 默认查询

curl

```
curl --get "https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/models" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d "page_no=1" \
    -d "page_size=20"
```

Python

```
import os
import dashscope

client = dashscope.Client(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1",
)

resp = client.models.list(
    page_no=1,
    page_size=20,
)
# 返回分页对象：resp.models 为当前页模型列表，resp.total_count 为符合条件的模型总数
print(resp.models)
```

```
{
    "code": null,
    "message": null,
    "success": true,
    "output": {
        "total": 373,
        "page_no": 1,
        "page_size": 20,
        "models": [
            {
                "model": "qwen3.8-max",
                "name": "Qwen3.8-Max",
                "description": "2.4万亿参数MoE旗舰，编程与办公能力全面跃升，可自主编程十数天交付完整项目。胜任法律、金融、设计等数百种专业任务，一次对话端到端交付生产级成果。原生视觉理解贯穿规划、执行与验证全流程，支持超长文档与长视频的深度语义解析。长程任务中自主规划与闭环迭代，持续进化。",
                "provider": "qwen",
                "capabilities": ["Reasoning", "VU", "TG"],
                "inference_provider": "aliyun-bailian",
                "features": ["cache", "function-calling"],
                "prices": [
                    {
                        "prices": [
                            {
                                "type": "input_token",
                                "price": "12",
                                "price_unit": "每百万tokens",
                                "price_name": "输入",
                                "time_band": "standard"
                            },
                            {
                                "type": "output_token",
                                "price": "36",
                                "price_unit": "每百万tokens",
                                "price_name": "输出",
                                "time_band": "standard"
                            }
                        ],
                        "range_name": "Default"
                    }
                ],
                "published_time": "2026-08-02 12:14:32",
                "inference_metadata": {
                    "response_modality": ["Text"],
                    "request_modality": ["Image", "Text", "Video"]
                },
                "model_info": {
                    "context_window": 1000000,
                    "max_input_tokens": 991808,
                    "max_output_tokens": 131072,
                    "max_reasoning_tokens": 262144,
                    "reasoning_max_input_tokens": 983616,
                    "reasoning_max_output_tokens": 131072
                }
            }
        ]
    },
    "request_id": "实际请求 ID"
}
```

#### 按模型 ID 查询

curl

```
curl --get "https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/models" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d "model=qwen3.8-max" \
    -d "page_no=1" \
    -d "page_size=20"
```

Python

```
import os
import dashscope

client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1",
)

model = client.models.get("qwen3.8-max")
print(model)
```

```
{
    "code": null,
    "message": null,
    "success": true,
    "output": {
        "total": 1,
        "page_no": 1,
        "page_size": 20,
        "models": [
            {
                "model": "qwen3.8-max",
                "name": "Qwen3.8-Max",
                "description": "2.4万亿参数MoE旗舰，编程与办公能力全面跃升，可自主编程十数天交付完整项目。胜任法律、金融、设计等数百种专业任务，一次对话端到端交付生产级成果。原生视觉理解贯穿规划、执行与验证全流程，支持超长文档与长视频的深度语义解析。长程任务中自主规划与闭环迭代，持续进化。",
                "provider": "qwen",
                "capabilities": ["Reasoning", "VU", "TG"],
                "inference_provider": "aliyun-bailian",
                "features": ["cache", "function-calling"],
                "prices": [
                    {
                        "prices": [
                            {
                                "type": "input_token",
                                "price": "12",
                                "price_unit": "每百万tokens",
                                "price_name": "输入",
                                "time_band": "standard"
                            },
                            {
                                "type": "output_token",
                                "price": "36",
                                "price_unit": "每百万tokens",
                                "price_name": "输出",
                                "time_band": "standard"
                            }
                        ],
                        "range_name": "Default"
                    }
                ],
                "published_time": "2026-08-02 12:14:32",
                "inference_metadata": {
                    "response_modality": ["Text"],
                    "request_modality": ["Image", "Text", "Video"]
                },
                "model_info": {
                    "context_window": 1000000,
                    "max_input_tokens": 991808,
                    "max_output_tokens": 131072,
                    "max_reasoning_tokens": 262144,
                    "reasoning_max_input_tokens": 983616,
                    "reasoning_max_output_tokens": 131072
                }
            }
        ]
    },
    "request_id": "实际请求 ID"
}
```

#### 按模型作者查询

```
curl --get "https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/models" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d "providers=qwen" \
    -d "page_no=1" \
    -d "page_size=100"
```

```
{
    "code": null,
    "message": null,
    "success": true,
    "output": {
        "total": 147,
        "page_no": 1,
        "page_size": 100,
        "models": [
            {
                "model": "qwen3.8-max",
                "name": "Qwen3.8-Max",
                "description": "2.4万亿参数MoE旗舰，编程与办公能力全面跃升，可自主编程十数天交付完整项目。胜任法律、金融、设计等数百种专业任务，一次对话端到端交付生产级成果。原生视觉理解贯穿规划、执行与验证全流程，支持超长文档与长视频的深度语义解析。长程任务中自主规划与闭环迭代，持续进化。",
                "provider": "qwen",
                "capabilities": ["Reasoning", "VU", "TG"],
                "inference_provider": "aliyun-bailian",
                "features": ["cache", "function-calling"],
                "prices": [
                    {
                        "prices": [
                            {
                                "type": "input_token",
                                "price": "12",
                                "price_unit": "每百万tokens",
                                "price_name": "输入",
                                "time_band": "standard"
                            },
                            {
                                "type": "output_token",
                                "price": "36",
                                "price_unit": "每百万tokens",
                                "price_name": "输出",
                                "time_band": "standard"
                            }
                        ],
                        "range_name": "Default"
                    }
                ],
                "published_time": "2026-08-02 12:14:32",
                "inference_metadata": {
                    "response_modality": ["Text"],
                    "request_modality": ["Image", "Text", "Video"]
                },
                "model_info": {
                    "context_window": 1000000,
                    "max_input_tokens": 991808,
                    "max_output_tokens": 131072,
                    "max_reasoning_tokens": 262144,
                    "reasoning_max_input_tokens": 983616,
                    "reasoning_max_output_tokens": 131072
                }
            }
        ]
    },
    "request_id": "实际请求 ID"
}
```

#### 按能力查询

```
curl --get "https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/models" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d "capabilities=TG" \
    -d "page_no=1" \
    -d "page_size=20"
```

```
{
    "code": null,
    "message": null,
    "success": true,
    "output": {
        "total": 108,
        "page_no": 1,
        "page_size": 20,
        "models": [
            {
                "model": "qwen3.8-max",
                "name": "Qwen3.8-Max",
                "description": "2.4万亿参数MoE旗舰，编程与办公能力全面跃升，可自主编程十数天交付完整项目。胜任法律、金融、设计等数百种专业任务，一次对话端到端交付生产级成果。原生视觉理解贯穿规划、执行与验证全流程，支持超长文档与长视频的深度语义解析。长程任务中自主规划与闭环迭代，持续进化。",
                "provider": "qwen",
                "capabilities": ["Reasoning", "VU", "TG"],
                "inference_provider": "aliyun-bailian",
                "features": ["cache", "function-calling"],
                "prices": [
                    {
                        "prices": [
                            {
                                "type": "input_token",
                                "price": "12",
                                "price_unit": "每百万tokens",
                                "price_name": "输入",
                                "time_band": "standard"
                            },
                            {
                                "type": "output_token",
                                "price": "36",
                                "price_unit": "每百万tokens",
                                "price_name": "输出",
                                "time_band": "standard"
                            }
                        ],
                        "range_name": "Default"
                    }
                ],
                "published_time": "2026-08-02 12:14:32",
                "inference_metadata": {
                    "response_modality": ["Text"],
                    "request_modality": ["Image", "Text", "Video"]
                },
                "model_info": {
                    "context_window": 1000000,
                    "max_input_tokens": 991808,
                    "max_output_tokens": 131072,
                    "max_reasoning_tokens": 262144,
                    "reasoning_max_input_tokens": 983616,
                    "reasoning_max_output_tokens": 131072
                }
            }
        ]
    },
    "request_id": "实际请求 ID"
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
