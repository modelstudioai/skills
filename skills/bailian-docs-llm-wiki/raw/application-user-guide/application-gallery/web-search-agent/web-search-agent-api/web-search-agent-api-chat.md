# 生成对话

基于千问联网检索Agent提供的 agent\_id 与 agent\_version 信息，提供联网知识检索、场景化对话等能力。

## **请求语法**

```
POST /web-search-agent/chat/completions HTTP/1.1
```

## **请求参数**

-   注意：请求提供动态参数后，将会直接覆盖应用配置中的状态值。
    

**参数名**

**类型**

**是否必须**

**说明**

stream

bool

是

必须填 true，当前版本仅支持流式响应。若提供false或不提供，请求将失败

input

object

是

输入字段

input.request\_id

str

否

请求ID（业务自定义）

input.messages

array\[object\]

是

对话消息

input.messages.\[\].role

str

是

角色，枚举值为：user、assistant

input.messages.\[\].content

str

是

消息内容

parameters

object

是

配置参数字段

parameters.agent\_options

object

是

智能体专用参数

parameters.agent\_options.agent\_id

string

是

应用ID

parameters.agent\_options.agent\_version

string

是

应用版本

parameters.agent\_options.session\_knowledge

string

否

session 会话级别知识

parameters.agent\_options.system\_prompt

string

否

系统提示词

parameters.agent\_options.agent\_policy

string

否

执行策略

-   standard: 默认策略（推荐）
    
-   agentic: 强制边想边搜
    
-   turbo: 极速模式
    

parameters.agent\_options.forced\_search

bool

否

是否强制搜索

-   开启时， agent\_policy默认为 standard
    

parameters.agent\_options.enable\_citation

bool

否

是否透出引用信息

parameters.agent\_options.enable\_text\_image\_mixed

bool

否

是否图文并茂生成

parameters.agent\_options.enable\_lemma

bool

否

是否透出百科词条

parameters.agent\_options.related\_video

bool

否

是否透出相关视频

parameters.agent\_options.enable\_rec\_question

bool

否

是否透出相关问题

parameters.agent\_options.show\_step\_info

bool

否

是否展示工具调用状态信息，默认为 false

parameters.agent\_options.location

object

否

请求位置信息

parameters.agent\_options.location.address

string

否

具体地址

parameters.agent\_options.location.province

string

否

省份

parameters.agent\_options.location.city

string

否

城市

parameters.agent\_options.location.district

string

否

区/县

parameters.agent\_options.location.longitude

string

否

经度（小数点6位）

parameters.agent\_options.location.latitude

string

否

维度（小数点6位）

## **返回参数**

**参数名**

**类型**

**是否必须**

**说明**

request\_id

str

是

请求ID（dashscope 平台）

code

str

是

状态码（成功：200）

message

str

是

状态信息

output

object

是

输出字段

output.request\_id

str

否

请求ID（业务自定义）

output.choices

array\[object\]

是

模型输出信息

output.choices.\[\].finish\_reason

str

是

生成结束原因，仅尾包输出stop

output.choices.\[\].message

object

是

对话消息

output.choices.\[\].message.role

str

是

角色，枚举值为：user、assistant、tool

output.choices.\[\].message.content

str | array\[object\]

是

生成内容/工具返回内容

output.choices.\[\].message.reasoning\_content

str

否

思考内容

output.choices.\[\].message.tool\_calls

array\[object\]

否

工具调用信息

output.choices.\[\].message.tool\_calls\[0\].arguments

dcit\[str,object\]

否

工具调用参数

output.choices.\[\].message.tool\_calls\[0\].name

str

否

工具调用名称

output.choices.\[\].message.additional\_kwargs.extra\_json

Any

否

工具调用返回时，携带结构化输出信息

output.choices.\[\].message.extra

dict

否

步骤状态信息

output.choices.\[\].message.extra.group

str

否

执行阶段

output.choices.\[\].message.extra.step\_change

str

否

步骤变化事件

output.choices.\[\].message.extra.step

str

否

当前步骤

output.choices.\[\].message.response\_metadata

dict

否

请求模型调用详细信息

output.usage

object

否

用量统计

output.usage.input\_tokens

int

否

输入 tokens

output.usage.output\_tokens

int

否

输出 tokens

output.usage.total\_tokens

int

否

总 tokens

## **执行阶段枚举**

执行阶段（`group`）

描述

说明

planning

计划中

对应plan模型，即系统处于任务规划阶段，该阶段包含 start 和 end 事件

generating

生成中

对应生成模型，表示系统正处于结果生成阶段，此阶段包含 start 和 end 事件。

当前步骤（`step`）

描述和说明

planning

计划中

generating

生成中

tool\_calling

工具调用中

tool\_calling\_{工具名称}

工具调用中，附带工具名称

-   由于模型原因 step\_change 值可能为不存在，请尽可能使用持久化的标志step
    
-   空包情况下 step、step\_change、group 字段的值可能不存在
    
-   plan、generation 均由 xxx\_start 事件 和 xxx\_end 事件两个事件组成
    
-   tool\_call 由 tool\_call\_start、tool\_calling、tool\_return 三个事件组成
    
-   tool\_call\_start 表示工具调用开始、tool\_calling 表示获取到完整工具调用的参数并会抛出完整的工具调用参数、tool\_return 表示工具调用返回结果，同时会携带结构化的工具返回信息。
    

事件发生时 `step` 的值

步骤变化事件 (`step_change`)

事件名称

解释说明

`planning`

plan\_start

开始规划

`step` 状态变为 `planning`, 表示对应状态的开头（包含当前包）。

`planning`

空

规划中

表示正在思考和工具调用

`planning`

plan\_end

结束规划

`step` 开始变成其他状态，事件发生时 `step` 仍为 `planning`，表示对应状态的结尾（包含当前包）。

`generating`

generation\_start

开始生成

与 `plan` 事件同理

`generating`

空

生成中

表示正在生成

`generating`

generation\_end

结束生成

与 `plan` 事件同理

`tool_calling_{工具名称}`

tool\_call\_start

开始工具调用

表示工具调用开始

`tool_calling_{工具名称}`

tool\_calling

工具调用中

会输出tool\_call的具体参数和工具名称，`tool_calling`状态变为`tool_calling_{工具名称}`。

`tool_calling_{工具名称}`

tool\_return

工具返回

会携带工具返回信息， `step` 开始变成其他状态，事件发生时 `step` 仍为 `tool_calling_{工具名称}`。

## Agent tool call message和工具名映射

当有工具调用时，在消息中的\["extra"\]\["step"\]字段中，会显示“tool\_calling\_xx”，显示正在调用的工具是什么。具体消息中的工具调用消息和实际的工具名的映射关系如下表所示。

### **文本问答**

**工具调用的 step 消息**

**工具名**

tool\_calling\_search

联网搜索

tool\_calling\_visit

网页阅读

tool\_calling\_video\_search

视频搜索

tool\_calling\_lemma\_search

百度词条

tool\_calling\_query\_suggesting

追问

### **多模态问答**

相比于文本问答，新增了 2 个工具图搜图，文搜图。

**工具调用的 step 消息**

**工具名**

tool\_calling\_image\_search

文搜图

tool\_calling\_image\_to\_image\_search

图搜图

### **本地生活 POI 工具**

**工具调用的 step 消息**

**工具名**

tool\_calling\_poi\_search

关键字搜索

tool\_calling\_around\_search

周边搜索

## 工具调用状态信息

### **参数**

工具调用的状态在消息中的\["extra"\]\["step\_change"\]字段中，工具调用的信息在\["extra"\]\["step\_info"\]中，工具调用状态和工具调用信息的映射如下：

工具调用的 step 状态

状态含义

工具调用状态信息 step\_info

tool\_call\_start

开始工具调用

开始调用 xxx 工具

tool\_calling

正在调用工具

正在调用 xxx 工具

tool\_calling\_return

工具调用完成

xxx 工具调用完成，xxx

以联网搜索工具为例，其工具调用的状态信息会经历如下这个状态：

```
"step_change": "tool_call_start", "step": "tool_calling_search","step_info": "开始调用联网检索工具"
"step_change": "tool_calling", "step": "tool_calling_search","step_info": "正在调用联网检索工具"
"step_change": "tool_return", "step": "tool_calling_search",  "step_info": "联网检索工具调用完成，检索到10个网页"
```

## 图文并茂消息协议

在开启图文并茂后，模型输出的消息中，会穿插图片，图片在消息正文中的为 html 标准图片格式，示例如下：

```
<img src=\"xxx\" data-type=\"image\" data-url=\"xxx\" data-title=\"台风后的杭州:蓝天白云如漫画般清新️\" alt=\"杭州 晴天 蓝天\" width=\"1080\" height=\"1410\">
```

标签中：

-   data-type：数据类型，image 为图片数据
    
-   src ：图片的 url 地址
    
-   data-url ：图片的来源网址
    
-   data-tile ：图片标题
    
-   width/height ：图片的尺寸宽和高
    

在包含图片的模型消息中，additional\_kwargs 字段中包含了如下两个字段：

-   data\_type，如果为图文并茂的图片消息，则值为 image
    
-   data\_json，包含当前内容相关的所有图片，正文中只显示一张。这里是所有相关图片的集合，数据类型为 json。
    
    -   在 data\_json 中，每张图片的消息体如下所示：
        
        -   idx：图片编号 id
            
        -   url：图片来源网址
            
        -   title：图片标题
            
        -   published：网址发布日期
            
        -   image\_info\["url"\]：图片网址
            
        -   image\_info\["width"\]：图片宽
            
        -   image\_info\["height"\]：图片高
            

```
{"idx": 15, "query": "杭州 晴天 蓝天", "url": "xxx", "title": "xx", "published": "2024-11-04 03:04:04", "image_info": {"url": "xxx", "width": 1080, "height": 1410}}
```

以下展示了图文并茂消息完整的 3 个消息包示例：

```
data: {
    "status_code": 200,
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "",
                "message": {
                    "content": "游玩。\n\n",
                    "additional_kwargs": {},
                    "response_metadata": {},
                    "type": "ai",
                    "name": null,
                    "id": "run--019e63e4-e728-7421-b3e5-57b408d6d4b0",
                    "example": false,
                    "tool_calls": [],
                    "invalid_tool_calls": [],
                    "usage_metadata": null,
                    "tool_call_chunks": [],
                    "reasoning_content": "",
                    "role": "assistant",
                    "extra": {
                        "group": "generating",
                        "step_change": "",
                        "step": "generating"
                    }
                }
            }
        ]
    },
    "usage": null,
    "request_id": "chenwen-test-web-search-01"
}

data: {
    "status_code": 200,
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "",
                "message": {
                    "content": "<img src=\"http://miaobi-lite.bj.bcebos.com/miaobi/5mao/b%275Y%2Bw6aOO6L%2BH5ZCO55qE5Zu%2B54mHXzE3MzA2NTY4MTMuMTQ0MDA1NQ%3D%3D%27/0.png\" data-type=\"image\" data-url=\"http://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_4158884509151638702\" data-title=\"台风后的杭州:蓝天白云如漫画般清新\" alt=\"杭州 晴天 蓝天\" width=\"1080\" height=\"1410\">\n\n\n",
                    "additional_kwargs": {
                        "data_type": "image",
                        "data_json": [
                            {
                                "idx": 15,
                                "query": "杭州 晴天 蓝天",
                                "url": "http://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_4158884509151638702",
                                "title": "台风后的杭州:蓝天白云如漫画般清新",
                                "published": "2024-11-04 03:04:04",
                                "image_info": {
                                    "url": "http://miaobi-lite.bj.bcebos.com/miaobi/5mao/b%275Y%2Bw6aOO6L%2BH5ZCO55qE5Zu%2B54mHXzE3MzA2NTY4MTMuMTQ0MDA1NQ%3D%3D%27/0.png",
                                    "width": 1080,
                                    "height": 1410
                                }
                            },
                            {
                                "idx": 16,
                                "query": "杭州 晴天 蓝天",
                                "url": "http://m.dianping.com/ugcdetail/175828244?sceneType=0&bizType=29&msource=baiduappugc",
                                "title": "杭州的天空也太美了吧!",
                                "published": "2023-07-26 00:00:00",
                                "image_info": {
                                    "url": "http://qcloud.dpfile.com/pc/VWohABccM5j2sRMTT4YdH7qapT46U8bLlM3Wp-xKeMm3OVoihIkmurvV3052Y9Xt.jpg",
                                    "width": 2048,
                                    "height": 2731
                                }
                            },
                            {
                                "idx": 17,
                                "query": "杭州 晴天 蓝天",
                                "url": "http://m.dianping.com/ugcdetail/175964222?sceneType=0&bizType=29&msource=baiduappugc",
                                "title": "杭州蓝天白云很美,只是每次去人都要晒黑两",
                                "published": "2023-07-27 00:00:00",
                                "image_info": {
                                    "url": "http://qcloud.dpfile.com/pc/6ScKLghe1ZcE15OpzbomPigY1VkO6o_UTx9z6UB_BoNtf5OGAsnbF-AFIAJjozRl.jpg",
                                    "width": 2048,
                                    "height": 2731
                                }
                            }
                        ]
                    },
                    "response_metadata": {},
                    "type": "ai",
                    "name": null,
                    "id": "run--019e63e4-e728-7421-b3e5-57b408d6d4b0",
                    "example": false,
                    "tool_calls": [],
                    "invalid_tool_calls": [],
                    "usage_metadata": null,
                    "tool_call_chunks": [],
                    "reasoning_content": "",
                    "role": "assistant",
                    "extra": {
                        "group": "generating",
                        "step_change": "",
                        "step": "generating"
                    }
                }
            }
        ]
    },
    "usage": null,
    "request_id": "chenwen-test-web-search-01"
}

data: {
    "status_code": 200,
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "",
                "message": {
                    "content": "**总结**：",
                    "additional_kwargs": {},
                    "response_metadata": {},
                    "type": "ai",
                    "name": null,
                    "id": "run--019e63e4-e728-7421-b3e5-57b408d6d4b0",
                    "example": false,
                    "tool_calls": [],
                    "invalid_tool_calls": [],
                    "usage_metadata": null,
                    "tool_call_chunks": [],
                    "reasoning_content": "",
                    "role": "assistant",
                    "extra": {
                        "group": "generating",
                        "step_change": "",
                        "step": "generating"
                    }
                }
            }
        ]
    },
    "usage": null,
    "request_id": "chenwen-test-web-search-01"
}
```

## **本地生活 POI 卡片渲染**

**开启本地生活后**模型会输出基于位置检索POI的结果信息。同时**开启图文并茂**后，在POI 检索结果信息中会穿插图片，图片在消息正文中的为 html 标准图片格式，示例如下：

```
<img src=\"https://aos-comment.amap.com/B0FFGD1PB5/comment/content_media_external_file_9739_ss__1749454867961_64014666.jpg\" data-type=\"poi\" data-url=\"https://www.amap.com/detail/B0FFGD1PB5\" data-title=\"吴山景区吴山广场-吴山文化公园\" alt=\"吴山景区吴山广场-吴山文化公园\" width=\"400\" height=\"auto\"/>\n
```

标签中：

-   data-type：数据类型，poi 为地图卡片
    
-   src ：第一个卡片图片的链接
    
-   data-url ：卡片对应高德链接
    
-   data-tile ：卡片标题
    
-   width/height ：图片的尺寸宽和高
    

在包含图片的模型消息中，additional\_kwargs 字段中包含了如下两个字段：

-   data\_type，如果为地图卡片的图片消息，则值为 poi
    
-   data\_json，包含当前内容相关的所有地图卡片，正文中只显示一个。这里是所有相关卡片的集合，数据类型为 json。
    

在 data\_json 中，每个地图卡片的消息体如下所示：

**字段**

**类型**

**说明**

name

string

地点名称

id

string

地点唯一标识

distance

string

离中心点距离，单位米；仅在周边搜索的时候有值返回

location

string

poi 经纬度

type

string

poi 所属类型

typecode

string

poi 分类编码

pname

string

poi 所属省份

cityname

string

poi 所属城市

adname

string

poi 所属区县

address

string

poi 详细地址

photos

object

返回 poi 图片相关信息

photos\[\].title

string

poi 的图片介绍

photos\[\].url

string

poi 图片的下载链接

business

object

设置后返回 poi 商业信息

business 个性化字段

**字段**

**类型**

**说明**

business\_area

string

poi 所属商圈

opentime\_today

string

poi 今日营业时间，如 08:30-17:30 08:30-09:00 12:00-13:30 09:00-13:00

opentime\_week

string

poi 营业时间描述，如 周一至周五:08:30-17:30(延时服务时间:08:30-09:00；12:00-13:30)；周六延时服务时间:09:00-13:00(法定节假日除外)

tel

string

poi 的联系电话

tag

string

poi 特色内容，目前仅在美食poi下返回

rating

string

poi 评分，目前仅在餐饮、酒店、景点、影院类 POI 下返回

cost

string

poi 人均消费，目前仅在餐饮、酒店、景点、影院类 POI 下返回

parking\_type

string

停车场类型（地下、地面、路边），目前仅在停车场类 POI 下返回

下方展示**开启本地生活和图文混出**后的示例

```
"additional_kwargs": {
  "data_type": "poi",
  "data_json": [
    {
      "address": "四宜亭吴山景区(吴山广场地铁站D口步行150米)",
      "distance": "352",
      "business": {
        "opentime_today": "24小时营业",
        "keytag": "城市公园",
        "rating": "3.8",
        "business_area": "吴山",
        "tel": "0571-8703****",
        "rectag": "城市公园",
        "opentime_week": "周一至周日 00:00-24:00"
      },
      "pcode": "330000",
      "adcode": "330102",
      "pname": "浙江省",
      "cityname": "杭州市",
      "type": "风景名胜;公园广场;公园",
      "photos": [
        {
          "title": "",
          "url": "https://aos-comment.amap.com/B0FFGD1PB5/comment/content_media_external_file_9739_ss__1749454867961_64014666.jpg"
        },
        {
          "title": "",
          "url": "https://aos-comment.amap.com/B0FFGD1PB5/comment/content_media_external_images_media_1000008441_ss__1751303656358_97699056.jpg"
        },
        {
          "title": "",
          "url": "https://aos-comment.amap.com/B0FFGD1PB5/comment/content_media_external_file_9746_ss__1749454867953_49866303.jpg"
        }
      ],
      "typecode": "110101",
      "adname": "上城区",
      "citycode": "0571",
      "navi": {
        "navi_poiid": "H51F022002_375744",
        "entr_location": "120.163399,30.239046",
        "gridcode": "4520218310"
      },
      "name": "吴山景区吴山广场-吴山文化公园",
      "indoor": {
        "indoor_map": "0"
      },
      "location": "120.163789,30.238795",
      "id": "B0FFGD1PB5",
      "distance_text": "距离紫阳街道吴山小普陀吴山景区352米",
      "from": "浙江省杭州市上城区紫阳街道吴山小普陀吴山景区"
    }
  ]
}
```

## **多模态图像理解问答**

联网搜索 Agent 多模态接口支持通过图片 + 文本的方式进行对话。用户可以上传图片 URL，并附加文本问题，Agent 将理解图片内容调用工具并给出回答。

### **请求参数**

**参数名**

**类型**

**是否必须**

**说明**

input

object

是

输入字段

input.messages

array

是

消息列表

input.messages\[\].role

string

是

角色，固定为 user

input.messages\[\].content

array

是

消息内容，支持图片和文本

input.messages\[\].content\[\].type

string

否

图片地址，支持两种格式：

1\. URL 格式（[推荐](https://help.aliyun.com/zh/model-studio/web-search-agent-api-chat-multimodal-file)）：[https://example.com/image.jpg](https://example.com/image.jpg)

2\. Base64 格式：data:<content\_type>;base64,<base64\_data>，其中 content\_type 为图片 MIME 类型（如 image/jpeg）

input.messages\[\].content\[\].image\_url

object

条件必须

当 type为 image\_url 时必须

## **示例**

### **请求示例**

-   文本请求示例
    

```
{
    "input": {
        "messages": [
            {
                "role": "user", 
                "content": "现在日期"
            }
        ]
    },
    "stream": true,
    "parameters": {
        "agent_options": {
            "agent_id": "aid-xxx",
            "agent_version": "beta"
        }
    }
}
```

-   多模态请求示例
    

```
{
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "image_url": {
                            "url": "http://other-general-huabei2.oss-cn-beijing.aliyuncs.com/upload/36e553b350e98ba81f6b33b08833a784.png"
                        },
                        "type": "image_url"
                    },
                    {
                        "text": "这是什么动物，一般生活在哪些地域",
                        "type": "text"
                    }
                ]
            }
        ]
    },
    "stream": true,
    "parameters": {
        "agent_options": {
            "agent_version": "beta",
            "agent_id": "aid-xxx"
        }
    }
}
```

### **返回示例**

```
data: {
    "status_code": 200,
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "",
                "message": {
                    "content": "xxx",
                    "additional_kwargs": {},
                    "response_metadata": {
                        "headers": {
                            "vary": "Origin",
                            "x-request-id": "ca7a41ad-3994-9dcf-adf6-f7aa56bec62b",
                            "content-type": "text/event-stream;charset=UTF-8",
                            "x-dashscope-call-gateway": "true",
                            "req-cost-time": "508",
                            "req-arrive-time": "1773800485527",
                            "resp-start-time": "1773800486035",
                            "x-envoy-upstream-service-time": "506",
                            "date": "Wed, 18 Mar 2026 02:21:25 GMT",
                            "server": "istio-envoy",
                            "transfer-encoding": "chunked"
                        }
                    },
                    "type": "ai",
                    "name": null,
                    "id": "run--019cfebf-7194-78b3-ad12-c3df6b6423b1",
                    "example": false,
                    "tool_calls": [],
                    "invalid_tool_calls": [],
                    "usage_metadata": null,
                    "tool_call_chunks": [],
                    "reasoning_content": "",
                    "role": "assistant",
                    "extra": {
                        "group": "generating",
                        "step_change": "generation_start",
                        "step": "generating"
                    }
                }
            }
        ]
    },
    "usage": null,
    "request_id": "xxxx-xxxx"
}
```

### **调用示例**

Python

```
# coding=utf-8

import os
import json
import requests

chat_completions_url = 'https://dashscope.aliyuncs.com/api/v2/apps/web-search-agent/chat/completions'

headers = {
    'Authorization': f'Bearer {os.getenv("DASHSCOPE_API_KEY", "")}',  # 配置 API KEY
    'Content-Type': 'application/json'
}

if __name__ == "__main__":
    params = {
        "input": {
            "messages": [{"role": "user", "content": "目前国内主流多模态模型分别有哪些，根据性能和效果做下分析"}]  # 传入请求消息
        },
        "parameters": {
            "agent_options": {  # 设置 agent 选项
                "agent_id": "${agent_id}",  # 应用ID，可在应用管理页面获取到，例如：aid-8fd***e00
                "agent_version": "${agent_version}"  # 应用版本，beta 测试版本 / release 发布版本
            }
        },
        "stream": True
    }
    
    response = requests.post(chat_completions_url, headers=headers, json=params, stream=True)
    
    resultlist = []
    stage = ''
    action = ''
    content = ''
    reasoning_content = ''
    for chunk in response.iter_lines():
        if chunk:
            chunk_str = chunk.decode('utf-8').strip()
            if chunk_str.startswith('data:'):
                json_str = chunk_str[len('data:'):].strip()
                try:
                    obj = json.loads(json_str)
                    # 检查异常
                    if obj.get('code') != '200':
                        print("服务异常：", obj)
                    # 获取消息体
                    msg = obj.get('output', {}).get('choices', [{}])[0].get('message', {})
                    extra_flags = msg.get('extra', {})  # 获取模型状态标记字段
    
                    if stage != extra_flags.get('group', ''):  # 获取 模型当前阶段
                        print(f"agent stage: {extra_flags.get('group', '')}")
                    stage = extra_flags.get('group', '')
    
                    if action != extra_flags.get('step', '') and extra_flags.get('step', ''):  # 获取 模型当前阶段
                        print(f"agent action: {extra_flags.get('step', '')}")
                    action = extra_flags.get('step', '')
    
                    role = msg.get('role', '')  # 获取模型角色 assistant or role
                    content = msg.get('content')  # 获取生成内容
                    toolcalls = msg.get('tool_calls', [])  # 获取工具调用
                    if toolcalls:
                        print(f'{toolcalls}')
    
                    if role == "tool":
                        print("\\n" + content + "\\n", end='')  # 前后都换行
                    else:
                        print(content, end='')  # 流式输出
                    # 可按需保存
                    resultlist.append(obj)
                except Exception as e:
                    print("异常解析:", e)
```

Java

```
import java.io.*;
import java.net.*;
import java.util.*;
import com.alibaba.fastjson.*;
import java.nio.charset.StandardCharsets;

public class WebSearchStreamDemo {

    // 配置 API KEY
    public final static String CHAT_COMPLETIONS_URL = "https://dashscope.aliyuncs.com/api/v2/apps/web-search-agent/chat/completions";
    public final static String API_KEY = System.getenv("DASHSCOPE_API_KEY");

    public static void main(String[] args) throws Exception {
        // 构造参数
        Map<String, Object> params = new HashMap<>();
        // input.messages
        List<Map<String, Object>> messages = new ArrayList<>();
        Map<String, Object> msgObj = new HashMap<>();
        msgObj.put("role", "user");
        msgObj.put("content", "${prompt}");
        messages.add(msgObj);
        // input
        Map<String, Object> input = new HashMap<>();
        input.put("messages", messages);
        // parameters.agent_options
        Map<String, Object> agentOptions = new HashMap<>(); // 
        agentOptions.put("agent_id", "${agent_id}");// 应用ID，可在应用管理页面获取到，例如：aid-8fd***e00
        agentOptions.put("agent_version", "${agent_version}"); // 应用版本，beta 测试版本 / release 发布版本
        // parameters
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("agent_options", agentOptions);

        params.put("input", input);
        params.put("parameters", parameters);
        params.put("stream", true);

        String body = JSON.toJSONString(params);

        // HTTP 请求
        URL apiUrl = new URL(CHAT_COMPLETIONS_URL);
        HttpURLConnection conn = (HttpURLConnection) apiUrl.openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        conn.setRequestProperty("Authorization", "Bearer " + API_KEY);
        conn.setRequestProperty("Content-Type", "application/json");

        // 发送 body
        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.getBytes(StandardCharsets.UTF_8));
        }

        // 处理流式响应
        InputStream inputStream = conn.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
        String line;
        String stage = "";
        String action = "";
        List<JSONObject> resultList = new ArrayList<>();

        while ((line = reader.readLine()) != null) {
            if (!line.trim().isEmpty()) {
                String chunkStr = line.trim();
                if (chunkStr.startsWith("data:")) {
                    String jsonStr = chunkStr.substring(5).trim();
                    try {
                        JSONObject obj = JSON.parseObject(jsonStr);
                        // 检查异常
                        if (!"200".equals(obj.getString("code"))) {
                            System.out.print("服务异常: " + obj);
                        }
                        // 获取  output->choices[0]->message
                        JSONObject msg = null;
                        if (obj.containsKey("output")) {
                            JSONObject output = obj.getJSONObject("output");
                            if (output != null && output.containsKey("choices")) {
                                JSONArray choices = output.getJSONArray("choices");
                                if (choices != null && !choices.isEmpty()) {
                                    JSONObject firstChoice = choices.getJSONObject(0);
                                    if (firstChoice.containsKey("message")) {
                                        msg = firstChoice.getJSONObject("message");
                                    }
                                }
                            }
                        }
                        if (msg == null) {
                            continue;
                        }

                        // 获取 extra_flags 字段
                        JSONObject extraFlags = msg.containsKey("extra") && msg.get("extra") != null
                                ? msg.getJSONObject("extra") : new JSONObject();

                        // agent stage
                        String stageNew = extraFlags.containsKey("group") && extraFlags.get("group") != null
                                ? extraFlags.getString("group") : "";
                        if (!stage.equals(stageNew)) {
                            System.out.println("agent stage: " + stageNew);
                        }
                        stage = stageNew;

                        // agent action
                        String actionNew = extraFlags.containsKey("step") && extraFlags.get("step") != null
                                ? extraFlags.getString("step") : "";
                        if (!action.equals(actionNew) && !actionNew.isEmpty()) {
                            System.out.println("agent action: " + actionNew);
                        }
                        action = actionNew;

                        String role = msg.containsKey("role") && msg.get("role") != null
                                ? msg.getString("role") : "";

                        Object contentObj = msg.get("content");
                        String content = null;
                        boolean isContentString = false;
                        // content 是字符串类型
                        if (contentObj instanceof String) {
                            content = contentObj.toString();
                            isContentString = true;
                        }

                        // 字符串为空时补 reasoning_content
                        if (isContentString && content.isEmpty()) {
                            Object reasoningContentObj = msg.get("reasoning_content");
                            if (reasoningContentObj instanceof String) {
                                content = reasoningContentObj.toString();
                            }
                        }

                        // 工具调用
                        if (msg.containsKey("tool_calls") && msg.get("tool_calls") instanceof List) {
                            JSONArray toolCalls = msg.getJSONArray("tool_calls");
                            if (!toolCalls.isEmpty()) {
                                System.out.println(toolCalls);
                            }
                        }

                       if ("tool".equals(role)) {
                            System.out.print("\\n" + content + "\\n");
                        } else {
                            System.out.print(content);
                        }

                        // 可按需保存
                        resultList.add(obj);
                    } catch (Exception e) {
                        System.out.println("异常解析: " + e);
                    }
                }
            }
        }
        reader.close();
    }
}
```
