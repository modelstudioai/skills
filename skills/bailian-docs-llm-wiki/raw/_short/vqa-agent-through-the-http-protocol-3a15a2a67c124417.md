# 通过HTTP协议接入拍照问答Agent

<a id="名词解释"></a>

<a id="0381d10609pkf"></a>

## 名词解释

直通链路：是指不通过语音识别(ASR)、意图识别、语音合成(TTS)等节点，直接将请求送入Agent，并将Agent的回答直接返回的链路。

<a id="适用场景"></a>

<a id="2209ccf25ah0i"></a>

## 适用场景

将图片直接送入Agent进行识别，无需意图检测及语音链路，适用于带摄像头产品的图片理解、拍学机或学习机内的拍照识图等功能。

<a id="前提条件"></a>

<a id="282230ae9fhvf"></a>

## 前提条件

<a id="开通阿里云百炼模型服务并获取api-key"></a>

<a id="590096efccq0s"></a>

### 开通阿里云百炼模型服务并获取API KEY

请参考[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，API KEY作为百炼模型服务的鉴权凭证。

<a id="管控台开通拍照问答直通链路"></a>

<a id="f84460d1fal12"></a>

## 管控台开通拍照问答直通链路

1.  在[多模态开发套件](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.394f1b92MoDMrb&tab=app#/app/app-market/multi-modal-app)中创建多模态交互应用，模版选择全能版本(不要选择视觉版)，关闭语音交互。

⚠️注意：关闭语音交互配置即可，意图识别配置、文本模型配置均需打开。

1.  关闭 对话承接语、知识库、联网搜索、长期记忆配置。
    
2.  技能配置全部清空、Agent配置只保留拍照问答。
    
3.  配置拍照问答Agent，启动指令置空，模型推荐选择“视觉理解均衡版”，请按需要配置提示词。
    

测试图片描述场景，提示词可使用如下(仅做演示支持，用户可按场景编辑)

<a id="code-block"></a>

```text
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

1.  配置完成后请点击右上角发布按键进行发布(必须发布后才能测试)。

<a id="http协议接入"></a>

<a id="4a8f042f86trq"></a>

## HTTP协议接入

<a id="请求参数说明"></a>

<a id="bf9ecdc3d294g"></a>

### 请求参数说明

<table><tbody><tr><td><p><strong>一级参数</strong></p></td><td><p><strong>二级参数</strong></p></td><td><p><strong>类型</strong></p></td><td><p><strong>是否必选</strong></p></td><td><p><strong>说明</strong></p></td></tr><tr><td><p>model</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>阿里云百炼模型名称，固定为&quot;multimodal-dialog&quot;，请直接复制使用</p></td></tr><tr><td rowspan="4"><p>input</p></td><td><p>directive</p></td><td><p>string</p></td><td><p>是</p></td><td><p>指令名称：<strong>Request</strong></p></td></tr><tr><td><p>app_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>客户创建的应用ID（<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz">获取APP ID</a>），可在<strong>多模态交互开发套件</strong>控制台的“我的应用”页面查看</p></td></tr><tr><td><p>dialog_id</p></td><td><p>string</p></td><td><p>否</p></td><td><p>对话id，默认不填时是新对话，服务端会自动生成并在返回结果中下发，格式示例：&quot;12345678-1234-1234-1234-1234567890ab&quot;，共36个字符。当希望继续之前的对话时，把当时服务端下发的dialog_id在这里传入</p></td></tr><tr><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>要处理的文本。注意，在本实践中没有文本请置为&quot;&quot;空字符串。</p></td></tr><tr><td rowspan="3"><p>parameters</p></td><td><p>client_info</p></td><td><p>object</p></td><td><p>是</p></td><td><p>参数说明参考下方 parameters.client_info的参数说明表格</p></td></tr><tr><td><p>images</p></td><td><p>list[]</p></td><td><p>否</p></td><td><p>需要分析的图片数据，仅多模态应用可支持图片问答，参数说明参考下方parameters.images的参数说明表格</p></td></tr><tr><td><p>biz_params</p></td><td><p>object</p></td><td><p>否</p></td><td><p>按需配置，参数说明参考下方parameters.biz_params的参数说明表格</p></td></tr></tbody></table>

<a id="3646e02aaard7"></a>

##### parameters.client\_info的参数说明

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| user\_id |  | string | 是 | 终端用户ID，客户根据自己业务规则生成，用来针对不同终端用户实现定制化功能。最大长度36个字符。 |
| device | uuid | string | 否 | 客户端全局唯一的ID，需要用户自己生成并传入SDK，最大长度40个字符。一个终端用户可以有多个设备，那么每一个设备的uuid都不同，但user\_id相同。 |

<a id="b959f3af03nhz"></a>

##### parameters.images的参数说明

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>是</p></td><td><p>图片类型，支持两种：base64/url</p></td></tr><tr><td><p>value</p></td><td><p>string</p></td><td><p>是</p></td><td><p>图片内容。</p><ul><li><p>当type为base64时，这里是图片的base64字符串。</p></li><li><p>当type为url时，这里是图片的url地址。</p></li></ul></td></tr></tbody></table>

<a id="a71da25aabztk"></a>

##### parameters.biz\_params的参数说明

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>commands[i]</p></td><td><p>name</p></td><td><p>string</p></td><td><p>是</p></td><td><p>表示直通到agent，本实践中固定为“agent_command”，请直接复制使用</p></td></tr><tr><td><p>exec_params</p></td><td><p>object</p></td><td><p>是</p></td><td><p>表示指定的agent，本实践固定，具体请参考commands.exec_params参数说明</p></td></tr></tbody></table>

commands.exec\_params参数说明

<table><tbody><tr><td rowspan="2"><p>exec_params</p></td><td><p>app_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>表示指定的agent，本实践固定为&quot;visual_qa&quot;,请复制使用</p></td></tr><tr><td><p>intent</p></td><td><p>string</p></td><td><p>是</p></td><td><p>表示指定agent的动作，本实践固定为&quot;open_visual_qa&quot;,请复制使用</p></td></tr></tbody></table>

<a id="请求示例如下"></a>

<a id="fffee5d445bir"></a>

### 请求示例如下

<a id="code-block-2"></a>

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
                        "app_id": "visual_qa",
                        "intent": "open_visual_qa"
                    }
                }
            ]
        }
    }
}
```

<a id="curl请求示例"></a>

<a id="7cbe02f5bckzo"></a>

### curl请求示例

<a id="code-block-3"></a>

```json
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
              "app_id": "visual_qa",
              "intent": "open_visual_qa"
            }
          }
        ]
      }
    }
  }'
```

> **重要**
>
> 1.  请替换请求中的your\_api\_key(API\_KEY)，app\_id，img\_url。
> 2.  text字段请置为""空字符串，否则会进入意图

<a id="文本返回事件说明"></a>

<a id="bff43da05cy83"></a>

### 文本返回事件说明

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>event</p></td><td><p>string</p></td><td><p>是</p></td><td><p>事件名称：<strong>RespondingContent</strong></p></td></tr><tr><td></td><td><p>dialog_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>对话ID</p></td></tr><tr><td></td><td><p>round_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>本轮交互的ID</p></td></tr><tr><td></td><td><p>llm_request_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>调用llm的request_id</p></td></tr><tr><td></td><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>系统对外输出的文本，流式<strong>增量</strong>输出</p></td></tr><tr><td></td><td><p>spoken</p></td><td><p>string</p></td><td><p>是</p></td><td><p>合成语音时使用的文本，流式<strong>增量</strong>输出</p></td></tr><tr><td></td><td><p>finished</p></td><td><p>bool</p></td><td><p>是</p></td><td><p>输出是否结束</p></td></tr><tr><td></td><td><p>finish_reason</p></td><td><p>string</p></td><td><p>否</p></td><td><p>结束原因，目前只有一种：</p><ul><li><p>stop 表示正常结束</p></li></ul></td></tr><tr><td></td><td><p>extra_info</p></td><td><p>object</p></td><td><p>否</p></td><td><p>其他扩展信息，目前支持：</p><ul><li><p>agent_info: 智能体信息，见</p></li></ul></td></tr></tbody></table>

<a id="982f05df61x5h"></a>

##### extra\_info.agent\_info的参数说明

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| round |  | string | 是 | 对话轮次 |
| device | device\_id | string | 是 | 请求时使用的device.uuid |
| intent\_infos | intent | string | 是 | 使用的agent，本实践固定为"visual\_qa" |
|  | domain | string | 是 | 使用的agent，本实践固定为"visual\_qa" |

<a id="返回示例如下"></a>

<a id="f05ff4a4f9qcz"></a>

### 返回示例如下

<a id="code-block-4"></a>

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
                        "intent": "visual_qa",
                        "domain": "visual_qa"
                    }
                ]
            },
            "query": ""
        },
        "dialog_id": "6c4340eb-xxx-4055-8d66-0794df7986e0",
        "spoken": "你好",
        "finished": false,
        "text": "你好",
        "event": "RespondingContent"
    },
    "request_id": "xxx"
}
```
