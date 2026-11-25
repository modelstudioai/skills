# 通过HTTP协议接入图像生成Agent

<a id="功能介绍"></a>

<a id="e59424465933w"></a>

## 功能介绍

通过HTTP协议接入图像生成Agent，实现文生图、图生图、涂鸦生图功能。目前仅支持直通链路。

适用于壁纸生成、涂鸦作画、照片美化、图像风格化等各类图像生成场景。

直通链路是指不经过语音识别（ASR）、意图识别、语音合成（TTS）等节点，将请求直接送入图像生成Agent，并直接返回图片生成结果。

<a id="接入说明"></a>

<a id="a62c98a19fedm"></a>

## 接入说明

<a id="前提条件"></a>

<a id="b59a750904toi"></a>

### 前提条件

首先需要开通阿里云百炼模型服务，并获取API KEY。

请参考[获取API Key](../model-api-reference/preparations/get-api-key.md)，API KEY作为百炼模型服务的鉴权凭证。

<a id="管控台配置"></a>

<a id="35b561dcffnpo"></a>

### 管控台配置

1.  在[多模态开发套件](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.394f1b92MoDMrb&tab=app#/app/app-market/multi-modal-app)中创建多模态交互应用，选择全能版（不要选择视觉版），关闭语音交互。保持意图识别、文本模型开启。
    
    文本模型选择**多模态交互专有模型-高速版**。
    
2.  关闭对话承接语、知识库、联网搜索、长期记忆。
    
    将**携带上下文轮数**设置为 `5`。
    
3.  技能、MCP服务全部清空，Agent只保留生图玩法Agent。
    
4.  配置图像生成Agent，支持涂鸦生图、生图助手、文生图3种玩法。
    
    1.  涂鸦生图：基于手绘的涂鸦线稿生成图片。
    2.  生图助手：基于上传的图片生成新图片。
    3.  文生图：基于输入的文本指令生成图片。
5.  每种功能支持模型选择、提示词、正向提示词智能优化，反向提示词等选项。提示词可以添加变量，用于动态传入不同提示词。
    
    涂鸦生图的**模型选择**提供三个选项：**图生图高级版**、**图生图均衡版**、**图生图轻量版**。
    
6.  配置完成后请点击右上角发布按键进行发布（必须发布后才能测试）。
    

<a id="http协议接入"></a>

<a id="03ca3f66073kl"></a>

## HTTP协议接入

<a id="请求参数说明"></a>

<a id="1f6e7ddb94j9t"></a>

### 请求参数说明

<table><tbody><tr><td><p><strong>一级参数</strong></p></td><td><p><strong>二级参数</strong></p></td><td><p><strong>类型</strong></p></td><td><p><strong>是否必选</strong></p></td><td><p><strong>说明</strong></p></td></tr><tr><td><p>model</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>阿里云百炼模型名称，固定为&quot;multimodal-dialog&quot;，请直接复制使用</p></td></tr><tr><td rowspan="4"><p>input</p></td><td><p>directive</p></td><td><p>string</p></td><td><p>是</p></td><td><p>指令名称：<strong>Request</strong></p></td></tr><tr><td><p>app_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>客户创建的应用ID（<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz">获取APP ID</a>），可在<strong>多模态交互开发套件</strong>控制台的“我的应用”页面查看</p></td></tr><tr><td><p>dialog_id</p></td><td><p>string</p></td><td><p>否</p></td><td><p>对话id，默认不填时是新对话，服务端会自动生成并在返回结果中下发，格式示例：&quot;12345678-1234-1234-1234-1234567890ab&quot;，共36个字符。当希望继续之前的对话时，把当时服务端下发的dialog_id在这里传入。生图玩法不考虑上下文，不填即可。</p></td></tr><tr><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>要处理的文本。注意，在本实践中没有文本请置为&quot;&quot;空字符串。</p></td></tr><tr><td rowspan="3"><p>parameters</p></td><td><p>client_info</p></td><td><p>object</p></td><td><p>是</p></td><td><p>参数说明参考下方 parameters.client_info的参数说明表格</p></td></tr><tr><td><p>images</p></td><td><p>list[]</p></td><td><p>否</p></td><td><p>需要参考的图片，在图生图场景需要，文生图不需要，parameters.images的参数说明表格</p></td></tr><tr><td><p>biz_params</p></td><td><p>object</p></td><td><p>否</p></td><td><p>按需配置，参数说明参考下方parameters.biz_params的参数说明表格</p></td></tr></tbody></table>

<a id="parameters-client-info的参数说明"></a>

<a id="c2956a4b2b284"></a>

#### parameters.client\_info的参数说明

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| user\_id |  | string | 是 | 终端用户ID，客户根据自己业务规则生成，用来针对不同终端用户实现定制化功能。最大长度36个字符。 |
| device | uuid | string | 否 | 客户端全局唯一的ID，需要用户自己生成并传入SDK，最大长度40个字符。一个终端用户可以有多个设备，那么每一个设备的uuid都不同，但user\_id相同。 |

<a id="parameters-images的参数说明"></a>

<a id="4b71e05ccfve9"></a>

#### parameters.images的参数说明

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>是</p></td><td><p>图片类型，支持两种：base64/url</p></td></tr><tr><td><p>value</p></td><td><p>string</p></td><td><p>是</p></td><td><p>图片内容。</p><ul><li><p>当type为base64时，这里是图片的base64字符串。</p></li><li><p>当type为url时，这里是图片的url地址。</p></li></ul></td></tr></tbody></table>

<a id="parameters-biz-params的参数说明"></a>

<a id="6aa1edff1c5uw"></a>

#### parameters.biz\_params的参数说明

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>commands[i]</p></td><td><p>name</p></td><td><p>string</p></td><td><p>是</p></td><td><p>表示直通到agent，本实践中固定为“agent_command”，请直接复制使用</p></td></tr><tr><td><p>exec_params</p></td><td><p>object</p></td><td><p>是</p></td><td><p>表示指定的agent，本实践固定，具体请参考commands.exec_params参数说明</p></td></tr><tr><td><p>user_defined_params</p></td><td><p>image_to_image</p></td><td><p>object</p></td><td><p>否</p></td><td><p>表示用户自定义的agent参数，image_to_image表示传递给生图agent的参数，本实践仅在当需要传递生图agent内的提示词自定义变量时需要填充</p></td></tr></tbody></table>

<a id="03fadc8c9apn5"></a>

##### parameters.biz\_params.commands.exec\_params参数说明

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>exec_params</p></td><td><p>app_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>表示指定的agent，本实践固定为&quot;image_to_image&quot;,请复制使用</p></td></tr><tr><td><p>intent</p></td><td><p>string</p></td><td><p>是</p></td><td><p>表示指定agent的动作，本实践固定为&quot;open_image_to_image&quot;,请复制使用</p></td></tr><tr><td><p>slots</p></td><td><p>list[]</p></td><td><p>是</p></td><td><p>agent需要的槽位信息</p></td></tr></tbody></table>

<a id="c1d64a7bbfhef"></a>

##### parameters.biz\_params.commands.exec\_params.slots参数说明

|  |  |  |  |
| --- | --- | --- | --- |
| name | string | 是 | 表示槽位名 |
| norm\_value | string | 是 | 表示槽位值 |

在生图agent中，需填充如下function、size两种槽位信息。

<a id="code-block"></a>

```json
{
      "slots": [
          {
            "name": "function",
            "norm_value" :"imageAssistant"
          },
          {
            "name":"size",
            "norm_value":"768*768"
          }
      ]
}
```

function用来指定具体的生图功能，支持三种配置：

-   textToImage：文生图
-   imageAssistant：生图助手
-   sketchToImage：涂鸦生图

size用来指定生成图片的分辨率，分辨率和选择的玩法及模型强相关，支持的分辨率范围见下表

<table><tbody><tr><td><p><strong>生图模式</strong></p></td><td><p><strong>模型配置</strong></p></td><td><p><strong>支持分辨率</strong></p></td></tr><tr><td rowspan="3"><p>文生图</p></td><td><p>轻量版</p></td><td rowspan="2"><p>图像分辨率宽高范围在[200, 2048]，宽高比在[1:4, 4:1]。比如256x2048是不允许的，因为宽高比为1:8。</p></td></tr><tr><td><p>均衡版</p></td></tr><tr><td><p>高级版</p></td><td><p>图像分辨率：总像素在[1280*1280, 1440*1440]之间</p><p>图像宽高比：[1:4, 4:1]</p></td></tr><tr><td rowspan="3"><p>生图助手/涂鸦生图</p></td><td><p>轻量版</p></td><td><p>图像分辨率：宽高均在[512, 4096]像素之间</p></td></tr><tr><td><p>均衡版</p></td><td><p>图像分辨率：宽高均在[512*512, 2048*2048]像素之间</p></td></tr><tr><td><p>高级版</p></td><td><p>图像分辨率：总像素在 [768*768, 2048*2048]像素之间</p></td></tr></tbody></table>

<a id="2d08d257e0e85"></a>

##### parameters.biz\_params.user\_defined\_params.image\_to\_image.user\_prompt\_params参数说明

> **重要**
>
> 本实践仅在当需要传递生图agent内的提示词自定义变量时需要填充。

在涂鸦生图配置面板的提示词区域，单击右上角的 **{x} 自定义变量** 按钮即可添加自定义变量，其中 `${style}` 为默认预置变量。

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>user_prompt_params</p></td><td><p>positive</p></td><td><p>object</p></td><td><p>否</p></td><td><p>提示词中的自定义变量</p></td></tr><tr><td><p>negative</p></td><td><p>object</p></td><td><p>是</p></td><td><p>反向提示词的自定义变量</p></td></tr></tbody></table>

<a id="code-block-2"></a>

```json
"user_defined_params": {
    "image_to_image": {
        "user_prompt_params": {
            "positive": {
                "hair": "长头发",
                "name": "张三"
            },
            "negative": {
                "style": "低分辨率"
            }
        }
    }
}
```

<a id="文生图请求示例"></a>

<a id="6c27b15d17wjd"></a>

### 文生图请求示例

<a id="code-block-3"></a>

```json
{
    "model": "multimodal-dialog",
    "input": {
        "directive": "Request",
        "app_id": "xxxxxx",
        "text": ""
    },
    "parameters": {
        "client_info": {
            "user_id": "test-251222",
            "device": {
                "uuid": "test-251222-123"
            }
        },
      "biz_params": {
        "commands": [
          {
            "name": "agent_command",
            "exec_params": {
              "app_id": "image_to_image",
              "intent": "open_image_to_image",
		"slots": [
		  {
		    "name": "function",
		    "norm_value" :"textToImage"
			},
		  {
		    "name":"size",
		    "norm_value":"768*768"
		        }
		]
            }
          }
        ],
	  "user_defined_params": {
		"image_to_image": {
                  "user_prompt_params":{
                    "positive":{
                       "hair": "长头发"，
                       "name": "张三"
                      },
                    "negative":{
                       "style": "低分辨率"
                      }
                    }
		}
	  }
      }
    }
}
```

<a id="文生图curl请求示例"></a>

<a id="a64b7f4e725qm"></a>

#### 文生图curl请求示例

<a id="code-block-4"></a>

```bash
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer your_api_key' \
  --header 'X-DashScope-SSE: enable' \
  --data '{
    "model": "multimodal-dialog",
    "input": {
        "directive": "Request",
        "app_id": "xxxxxx",
        "text": ""
    },
    "parameters": {
        "client_info": {
            "user_id": "test-251222",
            "device": {
                "uuid": "test-251222-123"
            }
        },
        "biz_params": {
            "commands": [
                {
                    "name": "agent_command",
                    "exec_params": {
                        "app_id": "image_to_image",
                        "intent": "open_image_to_image",
                        "slots": [
                            {
                                "name": "function",
                                "norm_value": "textToImage"
                            },
                            {
                                "name": "size",
                                "norm_value": "768*768"
                            }
                        ]
                    }
                }
            ],
            "user_defined_params": {
                "image_to_image": {
                    "user_prompt_params": {
                        "positive": {
                            "hair": "长头发",
                            "name": "张三"
                        },
                        "negative": {
                            "style": "低分辨率"
                        }
                    }
                }
            }
        }
    }
}'
```

> **重要**
>
> 1.  请替换请求中的your\_api\_key（API\_KEY）、app\_id，img\_url。
> 2.  text字段请置为""空字符串，否则会进入意图
> 3.  user\_defined\_params仅需在传递生图玩法中Agent提示词自定义变量时才需传递。

<a id="生图助手请求示例"></a>

<a id="2608f8a85d637"></a>

### 生图助手请求示例

<a id="code-block-5"></a>

```json
{
    "model": "multimodal-dialog",
    "input": {
        "directive": "Request",
        "app_id": "xxxxxx",
        "text": ""
    },
    "parameters": {
        "images": [
            {
                "type": "url",
                "value": "img_url"
            }
        ],
        "client_info": {
            "user_id": "test-251222",
            "device": {
                "uuid": "test-251222-123"
            }
        },
        "biz_params": {
            "commands": [
                {
                    "name": "agent_command",
                    "exec_params": {
                        "app_id": "image_to_image",
                        "intent": "open_image_to_image",
                        "slots": [
                            {
                                "name": "function",
                                "norm_value": "imageAssistant"
                            },
                            {
                                "name": "size",
                                "norm_value": "768*768"
                            }
                        ]
                    }
                }
            ],
            "user_defined_params": {
                "image_to_image": {
                    "user_prompt_params": {
                        "positive": {
                            "hair": "长头发",
                            "name": "张三"
                        },
                        "negative": {
                            "style": "低分辨率"
                        }
                    }
                }
            }
        }
    }
}
```

<a id="生图助手curl请求示例"></a>

<a id="b09a2027d6qgx"></a>

#### 生图助手curl请求示例

<a id="code-block-6"></a>

```bash
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer your_api_key' \
  --header 'X-DashScope-SSE: enable' \
  --data '{
    "model": "multimodal-dialog",
    "input": {
        "directive": "Request",
        "app_id": "xxxxxx",
        "text": ""
    },
    "parameters": {
        "images": [
            {
                "type": "url",
                "value": "img_url"
            }
        ],
        "client_info": {
            "user_id": "test-251222",
            "device": {
                "uuid": "test-251222-123"
            }
        },
        "biz_params": {
            "commands": [
                {
                    "name": "agent_command",
                    "exec_params": {
                        "app_id": "image_to_image",
                        "intent": "open_image_to_image",
                        "slots": [
                            {
                                "name": "function",
                                "norm_value": "imageAssistant"
                            },
                            {
                                "name": "size",
                                "norm_value": "768*768"
                            }
                        ]
                    }
                }
            ],
            "user_defined_params": {
                "image_to_image": {
                    "user_prompt_params": {
                        "positive": {
                            "hair": "长头发",
                            "name": "张三"
                        },
                        "negative": {
                            "style": "低分辨率"
                        }
                    }
                }
            }
        }
    }
}'
```

> **重要**
>
> 1.  请替换请求中的your\_api\_key（API\_KEY）、app\_id，img\_url。
> 2.  text字段请置为""空字符串，否则会进入意图
> 3.  user\_defined\_params仅需在传递生图玩法中Agent提示词自定义变量时才需传递。

<a id="涂鸦生图请求示例"></a>

<a id="06dffc66ebo4p"></a>

### 涂鸦生图请求示例

参考生图助手请求示例，仅需将parameters.biz\_params.commands.exec\_params.slots内的function槽位从imageAssistant（表示生图助手）改为sketchToImage（表示涂鸦生图）。

<a id="文本返回事件说明"></a>

<a id="be6fa2917amux"></a>

### 文本返回事件说明

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>event</p></td><td><p>string</p></td><td><p>是</p></td><td><p>事件名称：<strong>RespondingContent</strong></p></td></tr><tr><td></td><td><p>dialog_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>对话ID</p></td></tr><tr><td></td><td><p>round_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>本轮交互的ID</p></td></tr><tr><td></td><td><p>llm_request_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>调用llm的request_id</p></td></tr><tr><td></td><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>生成图像的url，在生成过程内容为RUNNING，生成结束后为图片的url</p></td></tr><tr><td></td><td><p>spoken</p></td><td><p>string</p></td><td><p>是</p></td><td><p>用于TTS合成的内容，在未开启语音合成功能时不用关注。本实践内容和text字段相同。</p></td></tr><tr><td></td><td><p>finished</p></td><td><p>bool</p></td><td><p>是</p></td><td><p>输出是否结束</p></td></tr><tr><td></td><td><p>finish_reason</p></td><td><p>string</p></td><td><p>否</p></td><td><p>结束原因，目前只有一种：</p><ul><li><p>stop 表示正常结束</p></li></ul></td></tr><tr><td></td><td><p>extra_info</p></td><td><p>object</p></td><td><p>否</p></td><td><p>其他扩展信息，目前支持：</p><ul><li><p>agent_info: 智能体信息，见</p></li></ul></td></tr></tbody></table>

<a id="output-extra-info-agent-info的参数说明"></a>

<a id="5ada954f91oco"></a>

#### output.extra\_info.agent\_info的参数说明

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| round |  | string | 是 | 对话轮次 |
| device | device\_id | string | 是 | 请求时使用的device.uuid |
| intent\_infos | intent | string | 是 | 使用的agent，本实践固定为"open\_image\_to\_image" |
|  | domain | string | 是 | 使用的agent，本实践固定为"image\_to\_image" |

<a id="返回示例如下"></a>

<a id="bdfde370777w9"></a>

#### 返回示例如下

<a id="code-block-7"></a>

```json
{
    "output": {
        "round_id": "xxx",
        "llm_request_id": "xxx",
        "extra_info": {
            "agent_info": {
                "round": 1,
                "device": {
                    "device_id": "test-251222-123"
                },
                "intent_infos": [
                    {
                        "intent": "open_image_to_image",
                        "domain": "image_to_image"
                    }
                ]
            },
            "query": ""
        },
        "dialog_id": "6c4340eb-xxx-4055-8d66-0794df7986e0",
        "spoken": "img_url",
        "finished": true,
        "text": "img_url",
        "event": "RespondingContent"
    },
    "request_id": "xxx"
}
```

> **重要**
>
> 1.  在图像生成过程中，每3-5秒会返回一个心跳包，output.text="RUNNING"表示合成中，此时output.finished = false
> 2.  当图像合成结束，output.finished = true，此时output.text字段为img\_url

<a id="code-block-8"></a>

```text
id:1 合成过程中
event:result
:HTTP_STATUS/200
data:{"output":{"round_id":"6633eccfd6a44090b49bbbfe84a8xxx","llm_request_id":"f22feed889994756b3787de8b08bxxx","extra_info":{"tool_infos":[{"output":"","tool_name":"image_to_image","arguments":{},"type":"agent","success":true}]},"dialog_id":"00cd961c-bf58-49f5-b3bb-7c5ca9xxx","spoken":"","finished":false,"text":"","event":"RespondingContent"},"request_id":"a162bf16-8156-4b13-88f6-fcb7xxx"}
id:2 合成过程中
event:result
:HTTP_STATUS/200
data:{"output":{"round_id":"6633eccfd6a44090b49bbbfe84xxx","llm_request_id":"f22feed889994756b3787de8b0xxx","extra_info":{"agent_info":{"round":1,"device":{"device_id":"xxx-test-251222-123"},"intent_infos":[{"intent":"open_image_to_image","domain":"image_to_image"}]},"query":""},"dialog_id":"00cd961c-bf58-49f5-b3bb-7c5xxx","spoken":"RUNNING","finished":false,"text":"RUNNING","event":"RespondingContent"},"request_id":"a162bf16-8156-4b13-88f6-fcb7xxx"}
id:3 合成过程中
event:result
:HTTP_STATUS/200
data:{"output":{"round_id":"6633eccfd6a44090b49bbbfe84xxx","llm_request_id":"f22feed889994756b3787de8bxxx","extra_info":{"agent_info":{"round":1,"device":{"device_id":"xxx-test-251222-123"},"intent_infos":[{"intent":"open_image_to_image","domain":"image_to_image"}]},"query":""},"dialog_id":"00cd961c-bf58-49f5-b3bb-7c5cxxx","spoken":"RUNNING","finished":false,"text":"RUNNING","event":"RespondingContent"},"request_id":"a162bf16-8156-4b13-88f6-fcb71xxx"}
id:4 合成过程中
event:result
:HTTP_STATUS/200
data:{"output":{"round_id":"6633eccfd6a44090b49bbb1xxx","llm_request_id":"f22feed889994756b3787xxx","extra_info":{"agent_info":{"round":1,"device":{"device_id":"xxx-test-251222-123"},"intent_infos":[{"intent":"open_image_to_image","domain":"image_to_image"}]},"query":""},"dialog_id":"00cd961c-bf58-49f5-b3bb-xxx","spoken":"RUNNING","finished":false,"text":"RUNNING","event":"RespondingContent"},"request_id":"a162bf16-8156-4b13-88f6-fclxxx"}
id:5 合成结束
event:result
:HTTP_STATUS/200
data:{"output":{"round_id":"6633eccfd6a44090b49bbbfxxx","llm_request_id":"f22feed889994756b3787de8xxx","extra_info":{"tool_infos":[{"output":"","tool_name":"image_to_image","arguments":{},"type":"agent","success":true}],"agent_info":{"round":1,"device":{"device_id":"xxx-test-251222-123"},"intent_infos":[{"intent":"open_image_to_image","domain":"image_to_image"}]},"query":""},"finish_reason":"stop","dialog_id":"00cd961c-bf58-49f5-b3bb-7cxxx","spoken":"https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/1d/03/20260107/c6e3cb4b/eb8e554d-66ff-44ca-ba0d-f05481405d2c-1-1.png?Expires=1767854752&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE","finished":true,"text":"https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/1d/03/20260107/c6e3cb4b/eb8e554d-66ff-44ca-ba0d-f05481405d2c-1-1.png?Expires=1767854752&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE","event":"RespondingContent"},"request_id":"a162bf16-8156-4b13-88f6-fcbxxx"}
```
