# 通过HTTP协议接入图像生成Agent

## **功能介绍**

通过HTTP协议接入图像生成Agent，实现文生图、图生图、涂鸦生图功能。目前仅支持直通链路。

适用于壁纸生成、涂鸦作画、照片美化、图像风格化等各类图像生成场景。

直通链路是指不经过语音识别（ASR）、意图识别、语音合成（TTS）等节点，将请求直接送入图像生成Agent，并直接返回图片生成结果。

## **接入说明**

### **前提条件**

首先需要开通阿里云百炼模型服务，并获取API KEY。

请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，API KEY作为百炼模型服务的鉴权凭证。

### **管控台配置**

1.  在[多模态开发套件](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.394f1b92MoDMrb&tab=app#/app/app-market/multi-modal-app)中创建多模态交互应用，选择全能版（不要选择视觉版），关闭语音交互。保持意图识别、文本模型开启。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1307419671/p1048442.png)

2.  关闭对话承接语、知识库、联网搜索、长期记忆。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1307419671/p1048441.png)

3.  技能、MCP服务全部清空，Agent只保留生图玩法Agent。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0778149671/p1049190.png)

4.  配置图像生成Agent，支持涂鸦生图、生图助手、文生图3种玩法。
    
    1.  涂鸦生图：基于手绘的涂鸦线稿生成图片。
        
    2.  生图助手：基于上传的图片生成新图片。
        
    3.  文生图：基于输入的文本指令生成图片。
        
5.  每种功能支持模型选择、提示词、正向提示词智能优化，反向提示词等选项。提示词可以添加变量，用于动态传入不同提示词。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1307419671/p1048445.png)

6.  配置完成后请点击右上角发布按键进行发布（必须发布后才能测试）。
    

## **HTTP协议接入**

### **请求参数说明**

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

model

string

是

阿里云百炼模型名称，固定为"multimodal-dialog"，请直接复制使用

input

directive

string

是

指令名称：**Request**

app\_id

string

是

客户创建的应用ID（[获取APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)），可在**多模态交互开发套件**控制台的“我的应用”页面查看

dialog\_id

string

否

对话id，默认不填时是新对话，服务端会自动生成并在返回结果中下发，格式示例："12345678-1234-1234-1234-1234567890ab"，共36个字符。当希望继续之前的对话时，把当时服务端下发的dialog\_id在这里传入。生图玩法不考虑上下文，不填即可。

text

string

是

要处理的文本。注意，在本实践中没有文本请置为""空字符串。

parameters

client\_info

object

是

参数说明参考下方 parameters.client\_info的参数说明表格

images

list\[\]

否

需要参考的图片，在图生图场景需要，文生图不需要，parameters.images的参数说明表格

biz\_params

object

否

按需配置，参数说明参考下方parameters.biz\_params的参数说明表格

#### **parameters.client\_info的参数说明**

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

user\_id

string

是

终端用户ID，客户根据自己业务规则生成，用来针对不同终端用户实现定制化功能。最大长度36个字符。

device

uuid

string

否

客户端全局唯一的ID，需要用户自己生成并传入SDK，最大长度40个字符。一个终端用户可以有多个设备，那么每一个设备的uuid都不同，但user\_id相同。

#### **parameters.images的参数说明**

**一级参数**

**类型**

**是否必选**

**说明**

type

string

是

图片类型，支持两种：base64/url

value

string

是

图片内容。

-   当type为base64时，这里是图片的base64字符串。
    
-   当type为url时，这里是图片的url地址。
    

#### **parameters.biz\_params的参数说明**

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

commands\[i\]

name

string

是

表示直通到agent，本实践中固定为“agent\_command”，请直接复制使用

exec\_params

object

是

表示指定的agent，本实践固定，具体请参考commands.exec\_params参数说明

user\_defined\_params

image\_to\_image

object

否

表示用户自定义的agent参数，image\_to\_image表示传递给生图agent的参数，本实践仅在当需要传递生图agent内的提示词自定义变量时需要填充

##### **parameters.biz\_params.commands.exec\_params参数说明**

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

exec\_params

app\_id

string

是

表示指定的agent，本实践固定为"image\_to\_image",请复制使用

intent

string

是

表示指定agent的动作，本实践固定为"open\_image\_to\_image",请复制使用

slots

list\[\]

是

agent需要的槽位信息

##### **parameters.biz\_params.commands.exec\_params.slots参数说明**

name

string

是

表示槽位名

norm\_value

string

是

表示槽位值

在生图agent中，需填充如下function、size两种槽位信息。

```
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

**生图模式**

**模型配置**

**支持分辨率**

文生图

轻量版

图像分辨率宽高范围在\[200, 2048\]，宽高比在\[1:4, 4:1\]。比如256x2048是不允许的，因为宽高比为1:8。

均衡版

高级版

图像分辨率：总像素在\[1280\*1280, 1440\*1440\]之间

图像宽高比：\[1:4, 4:1\]

生图助手/涂鸦生图

轻量版

图像分辨率：宽高均在\[512, 4096\]像素之间

均衡版

图像分辨率：宽高均在\[512\*512, 2048\*2048\]像素之间

高级版

图像分辨率：总像素在 \[768\*768, 2048\*2048\]像素之间

##### **parameters.biz\_params.user\_defined\_params.image\_to\_image.user\_prompt\_params参数说明**

**重要**

本实践仅在当需要传递生图agent内的提示词自定义变量时需要填充。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1307419671/p1048444.png)

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

user\_prompt\_params

positive

object

否

提示词中的自定义变量

negative

object

是

反向提示词的自定义变量

```
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

### **文生图请求示例**

```
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

#### **文生图curl请求示例**

```
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

**重要**

1.  请替换请求中的your\_api\_key（API\_KEY）、app\_id，img\_url。
    
2.  text字段请置为""空字符串，否则会进入意图
    
3.  user\_defined\_params仅需在传递生图玩法中Agent提示词自定义变量时才需传递。
    

### **生图助手请求示例**

```
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

#### **生图助手curl请求示例**

```
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

**重要**

1.  请替换请求中的your\_api\_key（API\_KEY）、app\_id，img\_url。
    
2.  text字段请置为""空字符串，否则会进入意图
    
3.  user\_defined\_params仅需在传递生图玩法中Agent提示词自定义变量时才需传递。
    

### **涂鸦生图请求示例**

参考生图助手请求示例，仅需将parameters.biz\_params.commands.exec\_params.slots内的function槽位从imageAssistant（表示生图助手）改为sketchToImage（表示涂鸦生图）。

### **文本返回事件说明**

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

output

event

string

是

事件名称：**RespondingContent**

dialog\_id

string

是

对话ID

round\_id

string

是

本轮交互的ID

llm\_request\_id

string

是

调用llm的request\_id

text

string

是

生成图像的url，在生成过程内容为RUNNING，生成结束后为图片的url

spoken

string

是

用于TTS合成的内容，在未开启语音合成功能时不用关注。本实践内容和text字段相同。

finished

bool

是

输出是否结束

finish\_reason

string

否

结束原因，目前只有一种：

-   stop 表示正常结束
    

extra\_info

object

否

其他扩展信息，目前支持：

-   agent\_info: 智能体信息，见
    

#### **output.extra\_info.agent\_info的参数说明**

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

round

string

是

对话轮次

device

device\_id

string

是

请求时使用的device.uuid

intent\_infos

intent

string

是

使用的agent，本实践固定为"open\_image\_to\_image"

domain

string

是

使用的agent，本实践固定为"image\_to\_image"

#### **返回示例如下**

```
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

**重要**

1.  在图像生成过程中，每3-5秒会返回一个心跳包，output.text="RUNNING"表示合成中，此时output.finished = false
    
2.  当图像合成结束，output.finished = true，此时output.text字段为img\_url
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1307419671/p1048446.png)
