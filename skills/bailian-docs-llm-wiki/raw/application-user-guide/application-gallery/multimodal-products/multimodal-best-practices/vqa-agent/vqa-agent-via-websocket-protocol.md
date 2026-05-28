# 通过WebSocket协议接入拍照问答Agent和语音合成

本文介绍基于WebSocket协议实现将请求直通拍照问答Agent，并将结果进行TTS语音合成返回。

直通Agent是指不经过语音识别（ASR）、意图识别，将请求直接传递到Agent的方式。

实时多模态交互的标准流程通常如下：如果需要在该完整链路中使用拍照问答Agent（例如智能眼镜场景，直接问“帮我看看这是什么”），请阅读[拍照问答](https://help.aliyun.com/zh/model-studio/official-agent#d7b29ce94950f)和[RTOS SDK (License模式) 视觉模块接入](https://help.aliyun.com/zh/model-studio/rtos-sdk-license-mode-vision-module)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5088379671/p1049999.png)

如果只需要直通Agent，并不需要语音合成TTS，请阅读[通过HTTP协议接入拍照问答Agent](https://help.aliyun.com/zh/model-studio/vqa-agent-through-the-http-protocol)，即如下流程。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5088379671/p1049998.png)

本文介绍的流程如下：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5088379671/p1049994.png)

## **前提条件**

必须先阅读[实时多模态交互协议（WebSocket）](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol) ，了解实时多模态交互的整体WebSocket协议。

### **开通阿里云百炼模型服务并获取API KEY**

请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，API KEY作为百炼模型服务的鉴权凭证。

### **管控台开通拍照问答直通链路**

1.  在[多模态开发套件](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.394f1b92MoDMrb&tab=app#/app/app-market/multi-modal-app)中创建多模态交互应用，模板选择全能版本（不要选择视觉版），关闭语音识别，打开语音合成。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5088379671/p1049995.png)

**重要**

意图识别配置、文本模型配置均需打开（按照本文配置方式下，使用拍照问答不产生意图识别和文本模型的费用）。

2.  关闭 对话承接语、知识库、联网搜索、长期记忆配置。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5088379671/p1050000.png)

3.  技能配置全部清空、Agent配置只保留拍照问答。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5088379671/p1049997.png)

4.  配置拍照问答Agent，启动指令置空，模型推荐选择“视觉理解均衡版”，请按需要配置提示词。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5088379671/p1049996.png)

测试图片描述场景，提示词可使用如下（仅做演示支持，用户可按场景编辑）：

```
你是一个专业的图像分析与描述助手，请基于图片内容生成简洁、准确且信息丰富的文字描述。请确保描述涵盖以下要点：
主要物体和场景：明确指出画面中的核心元素及其位置、颜色、形状、数量，并说明场景类型（如室内、室外、城市、自然等）。
人物特征与动作（如有）：描述人物的衣着、表情、姿势、动作，互动关系，以及可能的身份或角色。
文字信息（如有）：描述图片中出现的文字、字体样式，以及文字的含义或用途（如标牌、广告、标题）。
环境与氛围：说明背景细节（如天气、光线、季节）、整体色调，以及画面传递的情绪或故事感。
视角与构图：可补充拍摄角度（俯视、平视、仰视）、景深效果、焦点位置等。
不进行主观评价，只提供客观、可观察的事实。
描述要求：
使用简洁清晰的中文，避免冗长和模糊词汇。
确保突出关键信息，同时覆盖细节。
如果画面元素之间存在明显关系（如因果、动作链），请在描述中说明。
不加入个人主观猜测或情绪判断（除非氛围明显）。
```

5.  配置完成后请点击右上角发布按键进行发布（必须发布后才能测试）。
    

## **时序图**

\[**关键流程**\] 服务端返回`Started`消息表示会话创建成功，但客户端禁止立即发送音频。客户端必须等待并接收到`DialogStateChanged`事件且`state`为`Listening`后，方可开始发送音频流。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5088379671/p1050108.png)

**重要**

1.  服务端返回`Started`消息表示会话创建成功，但客户端禁止立即发送请求。客户端必须等待并接收到`DialogStateChanged`事件且`state`为`Listening`后，方可开始发送请求。
    
2.  本文与标准语音对话在流程上的区别是，标准语音对话是在服务端处于`Listening`后开始上行语音，要监听VAD相关事件如SpeechStarted、SpeechEnded等事件，而本文是通过RequestToRespond 直接发送请求到服务端。
    

## **通过**RequestToRespond发送请求

### **RequestToRespond**

在Listening状态时，通知服务端与用户主动交互，可以上传文本调用agent，返回的结果再转换为语音下发

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

input

directive

string

是

指令名称：RequestToRespond

dialog\_id

string

是

对话id，标识对话上下文，**应与服务端返回的Listening状态时携带的dialog\_id相同**

type

string

是

服务应该采取的交互类型：

transcript 表示直接把文本转语音

prompt 表示把文本送大模型回答

**本文指定为prompt**

text

string

是

要处理的文本，可以为""空字符，也可以为明确的文本请求

parameters

images

list\[\]

否

需要分析的图片信息，目前仅支持上传单张图片

biz\_params

object

否

与Start消息中biz\_params相同，传递对话系统自定义参数。RequestToRespond的biz\_params参数只在本次请求中生效。

##### parameters.images的参数说明

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

-   当type为base64时，这里是图片的base64字符串，**且大小不能超过180KB**。
    
-   当type为url时，这里是图片的url地址。
    

##### parameters.biz\_params的参数说明

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

##### **commands.exec\_params参数说明**

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

exec\_params

app\_id

string

是

表示指定的agent，本实践固定为"visual\_qa",请复制使用

intent

string

是

表示指定agent的动作，本实践固定为"open\_visual\_qa",请复制使用

示例：

```
{
    "header": {
        "action":"continue-task",
        "task_id": "xxx",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "RequestToRespond",
          "dialog_id": "xxx",
          "type": "prompt",
          "text": ""
        },
        "parameters":{
          "images":[{
              "type": "url",
              "value": "img_url"
          }],
          "biz_params":{
            "commands": [
                {
                    "name": "agent_command",
                    "exec_params": {
                        "app_id": "visual_qa",
                        "intent": "open_visual_qa"
                    }
                }
            ]
          }
        }
    }
}
```

**重要**

1.  header中的参数定义见[实时多模态交互协议（WebSocket）](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol)相关说明
    
2.  时序图中的其他流程见[实时多模态交互协议（WebSocket）](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol)相关说明
