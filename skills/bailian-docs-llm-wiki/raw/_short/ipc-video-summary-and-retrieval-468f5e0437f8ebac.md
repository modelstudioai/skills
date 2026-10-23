# IPC视频摘要&视频检索

面向 IPC 摄像头场景，通过 HTTP 协议接入物理世界感知 Agent，实现视频摘要、结构化标注和自然语言视频检索。

## 功能介绍

面向消费级摄像头（IPC）场景，提供监控采集数据的智能理解与语义检索能力。系统通过多模态大模型对视频画面进行自动摘要与结构化标注，并基于向量化存储与检索技术，实现对历史监控的自然语言查询，帮助用户快速定位关键时刻。

-   视频摘要：对监控画面自动生成场景描述与结构化标签，支持自定义标签，并以语义向量形式持久化存储。
-   视频检索：支持自然语言查询历史事件，结合向量相似度匹配与大模型语义精排，按相似度阈值或 Top-K 返回结果。

**重要**本文包含两种调用方式：`vector_mode=store` 生成摘要并入库，`vector_mode=retrieve` 检索历史视频。两者使用同一个 HTTP 接口，通过 `vector_mode` 区分。

## 前提条件

-   已开通阿里云百炼模型服务。
-   已获取 API Key，作为百炼模型服务的鉴权凭证。参见[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## 控制台配置

### 第一步：创建应用

1.  打开[多模态交互开发套件](https://bailian.console.aliyun.com/?tab=app#/app/app-market/multi-modal-app)并登录。点击右上角**免费开通**，完成[服务开通](https://common-buy.aliyun.com/?commodityCode=sfm_MultimodalByQuery_public_cn)。

![开通多模态交互服务](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/cb232b98-d722-425e-99fb-cbb479a4264f.png)

2.  点击**自定义创建**，进入应用配置页面。

![创建多模态交互应用](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/2d70afdf-9f1f-406f-b441-7696797b7762.png) ![自定义创建应用](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/73189229-b53c-45a2-9ad3-664e91797d48.png)

### 第二步：配置应用

1.  关闭**语音交互**，保持**意图识别**和**文本模型**开启。关闭**对话承接语**、**知识库**、**联网搜索**和**长期记忆**，删除全部指令、插件和 MCP 服务。

![关闭语音交互并保留意图识别和文本模型](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/e3a99c63-5d42-4dfa-88cb-5982e75c7c52.png) ![关闭对话承接语、知识库、联网搜索和长期记忆](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/9f2480ef-bde3-4434-ad2e-f29307d44bba.png) ![删除全部指令、插件和 MCP 服务](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/d4c9badc-c532-457e-bede-eb218a2a3eb1.png)

2.  点击百炼应用的添加按钮，添加**物理世界感知**应用。首次使用需[开通服务](https://common-buy.aliyun.com/?commodityCode=sfm_worldperception_public_cn)。

![添加物理世界感知应用](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/4d03ea63-e5fe-4c40-8914-5e7ceb5025c7.png) ![开通物理世界感知服务](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/76ab8e75-b976-40ef-9293-92abce7cda6b.png)

3.  开通成功后，刷新应用配置页面，勾选**物理世界感知**并确定。不要勾选其他应用。

![勾选物理世界感知应用](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/3204887a-1893-43c3-a1c6-96a2a4f4231c.png)

4.  应用默认提供 IPC 场景视觉分析能力，可以通过配置按钮切换。

![切换 IPC 场景视觉分析能力](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/abecf6ac-bd45-4eb2-80ce-f09dc5f4ca96.png)

**说明**应用配置只保留**物理世界感知**。不要勾选其他应用，避免影响本实践的调用链路。

### 第三步：发布应用

配置完成后，点击右上角**发布**。应用必须发布后才能测试。

![发布应用](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/8K4nyeZJ4xQ3onLb/img/6f8b7a45-d547-4215-b0ca-cffc08d0c778.png)

返回上级页面，点击复制并保存刚发布的应用 ID，用于后续调用。

![复制应用 ID](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/1GXn45K60bd9KqDQ/img/60ae4f4b-836c-4dba-bc4f-0e9589235c84.png)

## HTTP 协议接入

请求地址：`https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。请求头设置 `X-DashScope-SSE: enable`，返回以 SSE 事件流下发。

### 请求参数

参数

类型

必填

说明

`model`

string

是

百炼模型名称，固定为 `multimodal-dialog`。

`input.directive`

string

是

指令名称，固定为 `Request`。

`input.app_id`

string

是

控制台创建的应用 ID，可在**多模态交互开发套件**控制台的**我的应用**页面查看。参见[获取 App ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)。

`input.text`

string

是

要处理的文本。本实践中固定为空字符串 `""`。

`parameters.client_info`

object

是

终端信息，见下文。

`parameters.biz_params`

object

是

业务参数，见下文。

#### parameters.client\_info

参数

类型

必填

说明

`user_id`

string

是

终端用户 ID，由业务侧按自身规则生成，用于针对不同终端用户实现定制化功能。最大长度 36 个字符。  
**注意**，在摘要/检索场景此字段必填，且必须保证同一 `app_id` 下每个用户的 `user_id` 唯一。相同的 `user_id` 的视频放在同一检索空间；如果两个 C 端用户使用相同的 `user_id`，则会出现检索资源共享。

`device.uuid`

string

是

设备 ID，由业务侧生成并传入 SDK，最大长度 40 个字符。一个终端用户（`user_id`）可以有多个设备，每个设备的 `uuid` 都不同，但 `user_id` 相同。  
**注意**，在摘要/检索场景此字段必填，且必须保证同一 `app_id` 下同一 `user_id` 的不同设备的 `uuid` 必须不同，否则无法区分不同的设备。

#### parameters.biz\_params

参数

类型

必填

说明

`commands[].name`

string

是

固定为 `agent_command`。

`commands[].exec_params`

object

是

指定 Agent，见下文。

`user_defined_params.physical_sense`

object

是

传给物理世界感知模型的参数。

#### commands\[\].exec\_params

参数

类型

必填

说明

`app_id`

string

是

固定为 `physical_sense`。

`intent`

string

是

固定为 `open_physical_sense`。

`slots`

list\[\]

是

Agent 槽位信息。

##### slots

参数

类型

必填

说明

`name`

string

是

槽位名。

`norm_value`

string

是

槽位值。

接入物理世界感知 Agent 时，需要填充 `scene` 槽位。`scene` 为必填项，支持以下值：

-   `embodied`：具身智能
-   `ipc`：IPC 场景（本文使用）
-   `auto_driving`：自动驾驶

```
{
  "slots": [
    {
      "name": "scene",
      "norm_value": "ipc"
    }
  ]
}
```

#### parameters.biz\_params.user\_defined\_params.physical\_sense.user\_prompt\_params

参数

类型

必填

说明

`param.sub_scene`

string

是

本场景固定为 `vector`。

`param.vector_mode`

string

是

标识摘要或检索。`store`：摘要；`retrieve`：检索。其他值报错。

`param.vector_store_config`

object

否

`vector_mode=store` 时必填。摘要配置，见下文。

`param.vector_retrieve_config`

object

否

`vector_mode=retrieve` 时必填。检索配置，见下文。

`param.format`

string

是

资源模式，支持 `image` 或 `video`。

`param.prompt`

string

是

`vector_mode=store` 时为空字符串；`vector_mode=retrieve` 时为检索的自然语言。

`param.images`

array

条件必填

资源数组。摘要时必填，见下文。

`param.oss`

object

否

OSS 配置，见下文。

`param.frame_enabled`

boolean

否

是否使用图片序列。仅 `format=video` 时生效。

`param.high_resolution`

boolean

否

是否开启高精度。默认关闭。

`param.max_pixels`

integer

否

像素上限。`vector_mode=store` 时有效，使用示例值 `230400`。

`param.fps`

double

条件必填

抽帧频率，取值范围 `[0.1, 10.0]`。`vector_mode=store` 且 `format=video` 时必填，使用示例值 `0.2`。不建议修改，修改会增加成本。

`param.max_frames`

integer

否

抽取帧的上限。

`param.max_tokens`

integer

否

输出最大 Token 数。

`param.temperature`

float

否

温度，默认 `0.0`。

`param.version`

string

否

版本号。无特殊约定时为空。

##### param.images

参数

类型

必填

说明

`type`

string

是

资源类型，支持 `base64` 或 `url`。

`value`

string

是

`type=base64` 时为资源的 base64 字符串；`type=url` 时为资源 URL。

**说明**

-   推荐分辨率范围为 640×480 到 1920×1080。
-   `type=url` 时，URL 必须以 `https` 开头，不支持 `http`。

##### param.oss

参数

类型

必填

说明

`internal`

boolean

否

是否使用内网链接。内网链接仅同地域可下载。

`region`

string

否

`internal=true` 时有效，表示 OSS 地域。

#### vector\_store\_config

参数

类型

必填

说明

`tags`

object

否

自定义标签，会注入到 prompt。

`tags.tags_object`

`list<string>`

否

物体类标签。

`tags.tags_action`

`list<string>`

否

动作类标签。

`extra_data`

object

否

自定义数据，检索时随结果返回。

`pre_process`

object

否

预处理配置。

`pre_process.type`

string

否

当前仅支持 `dts_to_mp4`，其他值报错。

#### vector\_retrieve\_config

参数

类型

必填

说明

`pipeline`

string

是

向量检索使用的 pipeline，见下文。

`similarity_threshold`

string

条件必填

`pipeline=threshold` 时必填。可解析为 double 且 ∈ `(0,1]`，否则报错。

`similarity_top_size`

string

条件必填

`pipeline=top_size` 时必填。可解析为正整数且 ≤ 1000，否则报错。

`vector_retrieval_time`

object

否

检索的时间范围。为空时默认检索当天。

`vector_retrieval_time.start_time`

string

否

开始时间，格式 `yyyy-MM-dd HH:mm:ss`。

`vector_retrieval_time.end_time`

string

否

结束时间，格式 `yyyy-MM-dd HH:mm:ss`。

时间范围规则：

-   `start_time` 和 `end_time` 必须同时指定，只传一个会报错。
-   `end_time` 必须大于 `start_time`。
-   时区默认为 `Asia/Shanghai`。
-   数据默认保留 7 天。

#### pipeline

值

说明

`threshold`

按相似度阈值检索，返回相似度达到阈值的向量。

`top_size`

返回相似度排名前 size 个向量。

`default_topk`

默认链路，等价于 `top_size=10`。

`llm_rerank`

先取 Top 10，再通过大模型语义精排返回 Top 3。可以过滤语义矛盾的结果，仅返回 3 条。

### 请求示例

#### 视频摘要

```
curl --request POST \
  --url https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --header "X-DashScope-SSE: enable" \
  --data '{
  "model": "multimodal-dialog",
  "input": {
    "directive": "Request",
    "app_id": "mm_xxxxxxxx",
    "text": ""
  },
  "parameters": {
    "client_info": {
      "user_id": "user_001",
      "device": {
        "uuid": "device_001"
      }
    },
    "biz_params": {
      "commands": [
        {
          "name": "agent_command",
          "exec_params": {
            "app_id": "physical_sense",
            "intent": "open_physical_sense",
            "slots": [
              {
                "name": "scene",
                "norm_value": "ipc"
              }
            ]
          }
        }
      ],
      "user_defined_params": {
        "physical_sense": {
          "user_prompt_params": {
            "param": {
              "sub_scene": "vector",
              "format": "video",
              "prompt": "",
              "fps": 0.2,
              "max_pixels": 230400,
              "images": [
                {
                  "type": "url",
                  "value": "https://example-bucket.oss-cn-hangzhou.aliyuncs.com/ipc/camera-01.dts"
                }
              ],
              "oss": {
                "internal": false,
                "region": "hangzhou"
              },
              "vector_mode": "store",
              "vector_store_config": {
                "tags": {
                  "tags_object": ["车", "宠物", "火焰", "烟雾", "外卖", "快递", "人"],
                  "tags_action": ["跌倒", "坐着", "躺着"]
                },
                "extra_data": {
                  "oss_path": "/video/00"
                },
                "pre_process": {
                  "type": "dts_to_mp4"
                }
              }
            }
          }
        }
      }
    }
  }
}'
```

#### 视频检索（top\_size）

```
curl --request POST \
  --url https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --header "X-DashScope-SSE: enable" \
  --data '{
  "model": "multimodal-dialog",
  "input": {
    "directive": "Request",
    "app_id": "mm_xxxxxxxx",
    "text": ""
  },
  "parameters": {
    "client_info": {
      "user_id": "user_001",
      "device": {
        "uuid": "device_001"
      }
    },
    "biz_params": {
      "commands": [
        {
          "name": "agent_command",
          "exec_params": {
            "app_id": "physical_sense",
            "intent": "open_physical_sense",
            "slots": [
              {
                "name": "scene",
                "norm_value": "ipc"
              }
            ]
          }
        }
      ],
      "user_defined_params": {
        "physical_sense": {
          "user_prompt_params": {
            "param": {
              "sub_scene": "vector",
              "format": "image",
              "prompt": "几点钟有人打球",
              "vector_mode": "retrieve",
              "vector_retrieve_config": {
                "pipeline": "top_size",
                "similarity_top_size": "5",
                "vector_retrieval_time": {
                  "start_time": "2026-09-21 00:00:00",
                  "end_time": "2026-09-21 23:00:00"
                }
              }
            }
          }
        }
      }
    }
  }
}'
```

#### 视频检索（llm\_rerank）

```
curl --request POST \
  --url https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --header "X-DashScope-SSE: enable" \
  --data '{
  "model": "multimodal-dialog",
  "input": {
    "directive": "Request",
    "app_id": "mm_xxxxxxxx",
    "text": ""
  },
  "parameters": {
    "client_info": {
      "user_id": "user_001",
      "device": {
        "uuid": "device_001"
      }
    },
    "biz_params": {
      "commands": [
        {
          "name": "agent_command",
          "exec_params": {
            "app_id": "physical_sense",
            "intent": "open_physical_sense",
            "slots": [
              {
                "name": "scene",
                "norm_value": "ipc"
              }
            ]
          }
        }
      ],
      "user_defined_params": {
        "physical_sense": {
          "user_prompt_params": {
            "param": {
              "sub_scene": "vector",
              "format": "image",
              "prompt": "几点钟有人打球",
              "vector_mode": "retrieve",
              "vector_retrieve_config": {
                "pipeline": "llm_rerank",
                "vector_retrieval_time": {
                  "start_time": "2026-09-21 00:00:00",
                  "end_time": "2026-09-21 23:00:00"
                }
              }
            }
          }
        }
      }
    }
  }
}'
```

## 返回结果

接口以 SSE 事件流返回。等待过程中只需关注最后一个 `finished=true` 的数据包，该包对应最终结果。事件包含 `event: result` 和 `data` 字段，以下返回示例为 `data` 字段的 JSON 结构。

### 摘要返回示例

```
{
  "output": {
    "round_id": "385edc5b707b413faf6b399f0894a73c",
    "llm_request_id": "7ea9521fbb1a48d796588213ceb84900",
    "extra_info": {
      "tool_infos": [
        {
          "output": "",
          "tool_name": "physical_sense",
          "arguments": {},
          "type": "agent",
          "success": true
        }
      ],
      "agent_info": {
        "ext_params": {
          "vector_store_result": {
            "summary": "室内办公区域无人活动，环境安静",
            "tags_action": [],
            "tags_object": [],
            "is_success": true,
            "info": "stored 1 embedding successfully"
          },
          "usage": [
            {
              "inputTokens": 1340,
              "modelType": "type_ipc_flash",
              "outputTokens": 91,
              "totalTokens": 1431
            },
            {
              "inputTokens": 69,
              "modelType": "event_retrieval",
              "outputTokens": 0,
              "totalTokens": 69
            }
          ]
        },
        "round": 1,
        "device": {
          "device_id": "device_001"
        },
        "intent_infos": [
          {
            "intent": "open_physical_sense",
            "domain": "physical_sense"
          }
        ]
      },
      "query": ""
    },
    "finish_reason": "stop",
    "dialog_id": "2dd901ad-d061-449b-a6eb-8652fccf4f53",
    "spoken": "",
    "finished": true,
    "text": "summary and vector store",
    "event": "RespondingContent"
  },
  "request_id": "66207dc3-2b37-9ace-a5b8-b8df609ef4eb"
}
```

### 检索返回示例

```
{
  "output": {
    "round_id": "e582d5e2a59d4f889468027d18eca40f",
    "llm_request_id": "4d9ecf97e8b845e695ea66fb1aa30f73",
    "extra_info": {
      "tool_infos": [
        {
          "output": "",
          "tool_name": "physical_sense",
          "arguments": {},
          "type": "agent",
          "success": true
        }
      ],
      "agent_info": {
        "ext_params": {
          "vector_retrieve_result": {
            "pipeline": "top_size",
            "total_candidates": 1,
            "is_success": true,
            "matches": [
              {
                "capturedAt": "2026-09-21 19:45:14",
                "description": "监控画面显示为白天的室内办公区域，光线充足。左侧设有白色接待台，右侧摆放着一张长方形桌子及几把椅子，桌上放置有盆栽植物和烟灰缸。背景处有一盆高大的绿植。整个场景中没有任何人员、车辆或宠物出现，环境保持静止状态。",
                "extraData": "{\"oss_path\":\"/video/00\"}",
                "mediaUrls": [
                  "https://example-bucket.oss-cn-hangzhou.aliyuncs.com/ipc/camera-01.dts"
                ],
                "similarity": 0.4510287801329569
              }
            ],
            "info": "retrieved 1 matches"
          },
          "usage": [
            {
              "inputTokens": 5,
              "modelType": "event_retrieval",
              "outputTokens": 0,
              "totalTokens": 5
            }
          ]
        },
        "round": 1,
        "device": {
          "device_id": "device_001"
        },
        "intent_infos": [
          {
            "intent": "open_physical_sense",
            "domain": "physical_sense"
          }
        ]
      },
      "query": ""
    },
    "finish_reason": "stop",
    "dialog_id": "03874c54-e385-49b3-a534-7856cc4d3533",
    "spoken": "",
    "finished": true,
    "text": "vector retrieve",
    "event": "RespondingContent"
  },
  "request_id": "5c0858af-a642-9303-89a1-407338afe19e"
}
```

### 返回参数说明

参数

类型

说明

`request_id`

string

百炼网关的请求 ID。

`output.event`

string

事件名称，固定为 `RespondingContent`。

`output.dialog_id`

string

对话 ID。

`output.round_id`

string

本轮交互的 ID。

`output.llm_request_id`

string

调用大模型的请求 ID。

`output.text`

string

返回内容。本实践的业务结果通过 `output.extra_info.agent_info.ext_params` 返回。

`output.spoken`

string

用于 TTS 合成的内容。未开启语音合成时无需关注。

`output.finished`

boolean

输出是否结束。

`output.finish_reason`

string

结束原因。当前仅支持 `stop`，表示正常结束。

`output.extra_info`

object

扩展信息。

`output.extra_info.tool_infos`

array

工具调用信息，包含 `tool_name`、`type`、`success`、`arguments`、`output` 等字段。

`output.extra_info.agent_info`

object

Agent 信息。

`output.extra_info.query`

string

查询内容。

#### output.extra\_info.agent\_info.ext\_params

参数

类型

说明

`vector_store_result`

object

`vector_mode=store` 时返回，表示摘要入库结果。

`vector_store_result.summary`

string

视频摘要。

`vector_store_result.tags_object`

`list<string>`

命中的物体标签。

`vector_store_result.tags_action`

`list<string>`

命中的动作标签。

`vector_store_result.is_success`

boolean

是否成功。

`vector_store_result.info`

string

提示信息。

`vector_retrieve_result`

object

`vector_mode=retrieve` 时返回，表示检索结果。

`vector_retrieve_result.pipeline`

string

与请求中的 `pipeline` 一致。

`vector_retrieve_result.total_candidates`

integer

参与相似度比对的向量个数。

`vector_retrieve_result.is_success`

boolean

是否成功。

`vector_retrieve_result.matches`

array

返回的向量详情，size=实际返回的向量个数。

`vector_retrieve_result.matches[].mediaUrls`

array

存储时使用的资源 URL 数组。

`vector_retrieve_result.matches[].description`

string

资源的文字摘要。

`vector_retrieve_result.matches[].similarity`

double

相似度。

`vector_retrieve_result.matches[].capturedAt`

string

向量存储的时间。

`vector_retrieve_result.matches[].extraData`

string

与向量绑定的自定义信息，JSON 字符串。

`vector_retrieve_result.info`

string

提示信息。

`usage`

array

Token 消耗信息，包含调用的全部模型。

`usage[].modelType`

string

模型类型。

`usage[].inputTokens`

integer

输入 Token 数。

`usage[].outputTokens`

integer

输出 Token 数。

`usage[].totalTokens`

integer

总 Token 数。
