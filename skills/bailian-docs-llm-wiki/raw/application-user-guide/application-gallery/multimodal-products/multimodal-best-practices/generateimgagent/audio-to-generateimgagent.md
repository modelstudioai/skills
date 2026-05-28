# 语音请求直通图像生成Agent(websocket)

本文介绍基于WebSocket协议实现将语音请求直通图像生成Agent，实现文生图功能。

## 名词解释

直通链路：直通Agent是指不经过意图识别，将语音请求直接传递到Agent的方式。

本文介绍的流程如下：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3487352771/p1056325.png)

## **适用场景**

适用于AI打印机，拍学机等文字生成图像场景。

## **前提条件**

必须先阅读 [开始会话](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#78ee2ceb84tl9) ，了解实时多模态交互的整体WebSocket协议。

### **开通阿里云百炼模型服务并获取API KEY**

请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，API KEY作为百炼模型服务的鉴权凭证。

## **管控台配置**

1.  在[多模态开发套件](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.394f1b92MoDMrb&tab=app#/app/app-market/multi-modal-app)中创建多模态交互应用，选择全能版（不要选择视觉版），打开语音识别，关闭语音合成。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3487352771/p1056324.png)

2.  保持意图识别、文本模型开启。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3487352771/p1056326.png)

**重要**

意图识别配置、文本模型配置均需打开（按照本文配置方式下，使用图像生成不产生意图识别和文本模型的费用）。

3.  关闭对话承接语、知识库、联网搜索、长期记忆。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3487352771/p1056323.png)

4.  技能、MCP服务全部清空，Agent只保留图像生成Agent。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3487352771/p1056329.png)

5.  配置图像生成Agent，**目前语音请求直通生图Agent只支持文生图模式，不支持涂鸦生图、生图助手**。
    
6.  每种功能支持模型选择、提示词、正向提示词智能优化，反向提示词等选项。提示词可以添加变量，用于动态传入不同提示词。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3487352771/p1056328.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3487352771/p1056327.png)

**重要**

语音直通生图Agent必须在提示词中自定义 query 变量 ，用户只负责定义此变量，不需设置此变量值，系统会使用此变量将语音请求的ASR结果注入到生图的prompt中。如果用户没有在自定义变量中定义 query 变量，语音请求的query将无法注入到prompt。

比如用户设置的文生图提示词如图为：${query}，二次元风格。用户语音请求的ASR结果为：一只可爱小狗，则生图模型收到的完整提示词为：一只可爱的小狗，二次元风格。

7.  配置完成后请点击右上角发布按键进行发布（必须发布后才能测试）。
    

## **websocket协议接入**

## **开始会话**

请参考 [开始会话](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#92d1f462e5xrm)消息的说明，本文需要在开始会话消息中进行如下配置。

### **开启文本流式返回**

-   parameters.downstream.intermediate\_text字段置为dialog
    
-   parameters.downstream.incremental\_response字段置为true
    

### **设置直通生图Agent和自定义透传参数**

parameters.biz\_params.commands\[ \]字段用于设置直通的Agent。

parameters.biz\_params.user\_defined\_params字段用户设置需要透传给agent的参数。

bizParams

参数

一级参数

类型

说明

commands\[\]

name

String

固定为“agent\_command”

exec\_params

Object

app\_id

String

管控台应用列表中的 agent，本文固定为"image\_to\_image"，表示图像生成Agent

intent

String

本文固定为"open\_image\_to\_image"

slots

Array

agent需要的槽位信息

user\_defined\_params

Object

透传给 Agent 的参数

image\_to\_image

Object

表示传递给生图Agent的参数

user\_prompt\_params

Object

用于传递生图Agent中的提示词自定义变量

##### **parameters.biz\_params.commands.exec\_params.slots参数说明**

name

string

是

表示槽位名

norm\_value

string

是

表示槽位值

在生图Agent中，需填充如下function、size两种槽位信息。

```
{
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
```

function用来指定具体的生图功能，支持三种配置，**本文只支持文生图**。

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

##### **parameters.biz\_params.user\_defined\_params.image\_to\_image.user\_prompt\_params参数说明**

**重要**

传递生图Agent内的提示词自定义变量时需要。本文要求必须在提示词中定义自定义变量query，所以必填。注意本文中query必须为空字符串，将由系统将语音请求的结果填充到query变量中。

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

user\_prompt\_params

positive

object

是

提示词中的自定义变量，本文中必填

negative

object

否

反向提示词的自定义变量

```
{
    "biz_params": {
        "commands": [
            {
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
                },
                "name": "agent_command"
            }
        ],
        "user_defined_params": {
            "image_to_image": {
                "user_prompt_params": {
                    "positive": {
                        "query": ""
                    }
                }
            }
        }
    }
}
```

**重要**

parameters.downstream.intermediate\_text字段、parameters.downstream.incremental\_response字段只能在创建WSS连接的开始消息中设置，在整轮对话中生效。

而parameters.biz\_params.commands\[ \]、parameters.biz\_params.user\_defined\_params字段可在开始消息中设置，创建连接后也可以通过[UpdateInfo - Input Message](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#649c4ce759ep7)消息动态更新。

### **开始会话消息示例**

```
{
    "header": {
        "action": "run-task",
        "streaming": "duplex",
        "task_id": "b96c2068b*****"
    },
    "payload": {
        "function": "generation",
        "input": {
            "app_id": "mm_***********",
            "directive": "Start",
            "workspace_id": "llm-***********"
        },
        "model": "multimodal-dialog",
        "parameters": {
            "biz_params": {
                "commands": [
                    {
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
                        },
                        "name": "agent_command"
                    }
                ],
                "user_defined_params": {
                    "image_to_image": {
                        "user_prompt_params": {
                            "positive": {
                                "query": ""
                            }
                        }
                    }
                }
            },
            "client_info": {
                "device": {
                    "uuid": "uuid_12345"
                },
                "location": {
                    "city_name": "杭州",
                    "latitude": "120.121",
                    "longitude": "30.221"
                },
                "user_id": "test_12345"
            },
            "downstream": {
                "audio_format": "pcm",
                "debug": false,
                "incremental_response": "true",
                "intermediate_text": "dialog",
                "pitch_rate": 100,
                "sample_rate": 48000,
                "speech_rate": 100,
                "type": "Audio",
                "voice": "longanhuan",
                "volume": 50
            },
            "upstream": {
                "mode": "duplex",
                "type": "AudioAndVideo"
            }
        },
        "task": "multimodal-generation",
        "task_group": "aigc"
    }
}
```

## **关于对话状态的说明**

接入语音请求直通生图Agent模式后，对话状态将由listening→thinking→responding→listening循环转为listening→thinking→listening循环，因为语音请求直通生图Agent模式不会合成TTS，所以没有responding状态。

## **返回事件说明**

解析生图返回的消息请监听 RespondingContent 事件。如果生图耗时较长（比如分辨率较高），会先返回心跳包，最后返回生成的图像链接。

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
    

### **output.extra\_info.agent\_info的参数说明**

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

### **返回心跳包示例**

```
{
    "header": {
        "task_id": "b96c206****",
        "event": "result-generated",
        "attributes": {

        }
    },
    "payload": {
        "output": {
            "event": "RespondingContent",
            "text": "RUNNINGRUNNING",
            "spoken": "RUNNINGRUNNING",
            "finished": false,
            "extra_info": {
                "tool_infos": [
                    {
                        "output": "",
                        "tool_name": "image_to_image",
                        "success": true,
                        "arguments": {

                        },
                        "type": "agent"
                    }
                ],
                "agent_info": {
                    "intent_infos": [
                        {
                            "domain": "image_to_image",
                            "intent": "open_image_to_image"
                        }
                    ],
                    "location": {
                        "city": "杭州",
                        "latitude": "120.121",
                        "longitude": "30.221"
                    },
                    "device": {
                        "device_id": "uuid_12345"
                    },
                    "round": 2
                },
                "query": "生成一只小羊的图片。"
            },
            "dialog_id": "48b2f122-****",
            "round_id": "0dc854c6c****",
            "llm_request_id": "0614e****"
        }
    }
}
```

**返回生成的图像链接示例**

```
{
    "header": {
        "task_id": "b96c20****",
        "event": "result-generated",
        "attributes": {

        }
    },
    "payload": {
        "output": {
            "event": "RespondingContent",
            "text": "img_url",
            "spoken": "img_url",
            "finished": true,
            "finish_reason": "stop",
            "extra_info": {
                "tool_infos": [
                    {
                        "output": "",
                        "tool_name": "image_to_image",
                        "success": true,
                        "arguments": {

                        },
                        "type": "agent"
                    }
                ],
                "agent_info": {
                    "intent_infos": [
                        {
                            "domain": "image_to_image",
                            "intent": "open_image_to_image"
                        }
                    ],
                    "location": {
                        "city": "杭州",
                        "latitude": "120.121",
                        "longitude": "30.221"
                    },
                    "device": {
                        "device_id": "uuid_12345"
                    },
                    "round": 2
                },
                "query": "生成一只小羊的图片。"
            },
            "dialog_id": "48b2f122-****",
            "round_id": "0dc854c6c****",
            "llm_request_id": "0614e****"
        }
    }
}
```

## **通过RTOS** C SDK(license)接入示例

初始化配置

```
mmi_user_config_t mmi_config = C_MMI_CONFIG_DEFAULT();

mmi_config.text_mode = C_MMI_TEXT_MODE_BOTH;    // 也可以配置成C_MMI_TEXT_MODE_LLM_ONLY
mmi_config.incremental_response = 1;
...    // 其他配置

c_mmi_config(&mmi_config);
```

在需要开启生图能力时，执行下列代码

```
cJSON *biz = cJSON_CreateObject();
cJSON *commands = cJSON_AddArrayToObject(biz, "commands");
cJSON *command = cJSON_CreateObject();
cJSON *exec_params = cJSON_AddObjectToObject(command, "exec_params");
cJSON_AddStringToObject(exec_params, "app_id", "image_to_image");
cJSON_AddStringToObject(exec_params, "intent", "open_image_to_image");
cJSON *slots = cJSON_AddArrayToObject(exec_params, "slots");
cJSON *s_function = cJSON_CreateObject();
cJSON *s_size = cJSON_CreateObject();
cJSON_AddStringToObject(s_function, "name", "function");
cJSON_AddStringToObject(s_function, "norm_value", "textToImage");
cJSON_AddStringToObject(s_size, "name", "size");
cJSON_AddStringToObject(s_size, "norm_value", "768*768");
cJSON_AddItemToArray(slots, s_function);
cJSON_AddItemToArray(slots, s_size);
cJSON_AddStringToObject(command, "name", "agent_command");
cJSON_AddItemToArray(commands, command);
cJSON *user_defined_params = cJSON_AddObjectToObject(biz, "user_defined_params");
cJSON *image_to_image = cJSON_AddObjectToObject(user_defined_params, "image_to_image");
cJSON *user_prompt_params = cJSON_AddObjectToObject(image_to_image, "user_prompt_params");
cJSON *positive = cJSON_AddObjectToObject(user_prompt_params, "positive");
cJSON_AddStringToObject(positive, "query", "");
c_mmi_update_biz_params(biz);
```

之后语音输入需要生成的图片内容即可获得图片链接
