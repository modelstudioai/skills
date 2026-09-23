# 文字纹理生成API详情

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 文字纹理生成

**说明**支持的领域 / 任务：aigc /创意文字生成

WordArt锦书-文字纹理生成可以对输入的文字内容或文字图片进行创意设计，根据提示词内容对文字添加材质和纹理，实现立体材质、场景融合、光影特效等效果，生成效果精美、风格多样的艺术字，结合背景可以直接作为文字海报使用。

输入内容&效果示意：

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792613.jpeg) ![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792610.jpeg)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2352807371/p861786.png)

风格说明：目前支持“自定义”、“预设风格”和“风格参考图”三大类，“自定义”大类提供3种风格，用户可基于提供的风格通过提示词进行纹理效果自定义，支持输入提示词和字体类型 ；“预设风格”大类提供20种风格，此类别为预设的风格效果，不支持用户自定义输入提示词和字体类型；“风格参考图”基于用户提供的参考图进行相似纹理效果生成，支持输入提示词和字体类型。每一种风格具体的示例图如下：

-   “自定义”大类：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792612.png)

-   “预设风格”大类：

瀑布流水（waterfall）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792593.png)

雪域高原（snow\_plateau）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792594.png)

原始森林（forest）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792598.png)

天空遨游（sky）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792596.png)

国风建筑（chinese\_building）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792597.png)

奇幻卡通（cartoon）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792595.png)

乐高积木（lego）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792602.png)

繁花盛开（flower）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792599.png)

亚克力（acrylic）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792600.png)

大理石（marble）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792601.png)

绒线毛毡（felt）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792604.png)

复古油画（oil\_painting）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792603.png)

水彩（watercolor\_painting）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792605.png)

中国画（chinese\_painting）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792608.png)

工笔画（claborate\_style\_painting）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792606.png)

城市夜景（city\_night）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792607.png)

湖光山色（mountain\_lake）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792609.png)

秋日落叶（autumn\_leaves）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0600533171/p792611.png)

青龙献瑞（green\_dragon）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0484356171/p803679.png)

赤龙呈祥（red\_dragon）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0484356171/p803680.png)

-   “风格参考图”大类：

风格参考图（ref\_image\_url）

生成结果

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2352807371/p861793.jpeg)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2352807371/p861789.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2352807371/p861791.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2352807371/p861792.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2352807371/p861788.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2352807371/p861790.png)

## 应用场景

-   海报文字制作：围绕海报文字设计场景，通过简单的提示词描述即可实现创意字形、艺术纹理和个性字体的智能生成，批量生成丰富有趣的具有特效艺术字内容的个性化海报。
-   文档艺术字创作：办公文档艺术字创作设计场景，批量生成丰具有特效艺术字内容的个性化字体嵌入到文档中，实现内容多样性创作。
-   文字配图创意营销：电商、互动娱乐、视频制作等泛娱乐场景，可根据场景主题风格通过特定的提示词描述生成智能配图的艺术纹理和个性字体。

## 特色优势

-   灵活创意字体打造：通过简单灵活的提示词描述即可实现创意字形、艺术纹理和个性字体的智能打造。
-   文字边缘风格多变：文字变形可以对输入的文字边缘轮廓进行风格创意变形，根据提示词内容进行边缘变化。
-   批量稳定特效生成：批量生成丰富有趣的特效艺术字内容，在文字的辨识度、创意感、艺术性实现精准可控。
-   透明文字极速生成：支持生成带透明通道的艺术字图片，实现艺术字精细化分割并作为独立素材输出使用。
-   相似风格轻松生成：支持输入风格参考图，轻松生成与参考图具有相似风格的艺术字效果图。

## 模型概览

模型名

模型简介

wordart-texture

WordArt锦书-文字纹理生成可以对输入的文字内容或文字图片进行创意设计，根据提示词内容对文字添加材质和纹理，实现立体材质、场景融合、光影特效等效果，生成效果精美、风格多样的艺术字，结合背景可以直接作为文字海报使用。

## 输入限制

-   文字纹理服务支持两种输入模式，图像输入和文本输入，图像输入相关的字段为：input.image，文本输入相关的字段为input.text，两种输入方式需要二选一。
    
-   图像输入要求：黑底白字，图片大小小于5M，图像格式推荐jpg/png/jpeg/bmp，宽高比不超过2:1，图像的长边不超过2048。
    
-   文本输入要求：
    
-   小于6个字符，且不能为空字符串""。支持中文、阿拉伯数字、英文字母。
    
-   若提供ttf文件，需为标准的ttf文件，文件大小小于30M，input.text.ttf\_url和input.text.font\_name字段需要二选一。
    
-   提示词长度小于200，且不能为""。
    
-   URL地址中不能包含中文字符。
    

## HTTP调用接口

### 功能描述

本模型需要相对较长的算法调用时间，所以在接口层面采用了异步调用的方式进行任务提交，在通过任务接口提交作业之后，系统会返回对应的作业ID，随后可以通过对应的异步作业查询接口获取任务的状态并且在作业到达最终完成态后取回对应的作业结果。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

**说明**接口限制：对单账户（含主账号与RAM子账号）任务下发接口限制QPS为2，并发任务数量限制为1。

### 作业提交接口调用

POST [https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture](https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture)

### 入参描述

传参方式

字段

类型

必选

描述

示例值

Header

Content-Type

_String_

是

请求类型：application/json

application/json

Authorization

_String_

是

API-Key，例如：Bearer d1\*\*2a

Bearer d1\*\*2a

X-DashScope-Async

_String_

是

固定使用 enable，表明使用异步方式提交作业。

enable

Body

model

_String_

是

指明需要调用的模型，固定值

wordart-texture

input.image

_Object_

否

图片输入的相关字段

input.image和input.text 需要二选一

input.image.image\_url

_String_

否

文字图像的地址；

图像要求：黑底白字，图片大小小于5M，图像格式推荐jpg/png/jpeg/bmp，长宽比不大于2，最大边长小于等2048；

若选择了input.image，此字段为必须字段

"image\_url":"[https://xxxxx](https://xxxxx)"

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1600533171/p792614.png)

input.text

_Object_

否

文字输入的相关字段

input.image和input.text 需要二选一

input.text.text\_content

_String_

否

用户输入的文字内容，小于6个字；

若选择了input.text，此字段为必须字段，且不能为空字符串""；

支持中文、阿拉伯数字、英文字母（字符的支持范围由ttf文件决定）

"text": "文字创意"

input.text.ttf\_url

_String_

否

用户传入的ttf文件；

标准的ttf文件，文件大小小于30M；

当使用input.text时，input.text.ttf\_url和input.text.font\_name 需要二选一

"ttf\_url":"[https://xxxxx](https://xxxxx)"

input.text.font\_name

_String_

否

使用预置字体的名称；

当使用input.text时，input.text.ttf\_url和input.text.font\_name 需要二选一；

默认为"dongfangdakai"

取值类型及说明：

'dongfangdakai'：阿里妈妈东方大楷

'puhuiti\_m'：阿里巴巴普惠体

'shuheiti'：阿里妈妈数黑体

'jinbuti'：钉钉进步体

'kuheiti'：站酷酷黑体

'kuaileti'：站酷快乐体

'wenyiti'：站酷文艺体

'logoti'：站酷小薇LOGO体

'cangeryuyangti\_m'：站酷仓耳渔阳体

'siyuansongti\_b'：思源宋体

'siyuanheiti\_m'：思源黑体

'fangzhengkaiti'：方正楷体

"font\_name": "dongfangdakai"

input.text.output\_image\_ratio

_String_

否

文字输入的图片的宽高比；

默认为"1:1"，可选的比例有："1:1", "16:9", "9:16"；

"output\_image\_ratio": "1:1"

input.prompt

_String_

是

期望文字纹理创意样式的描述提示词，长度小于200，不能为""

"prompt": "水果，蔬菜"

input.texture\_style

_String_

否

纹理风格的类型，包括“自定义”和“预设风格”两大类（注：如果使用“风格参考图”模式，则直接提供input. ref\_image\_url字段即可，本字段不起作用），两类风格具体取值和说明如下：

“自定义”大类提供3种风格，用户可基于提供的风格通过提示词进行纹理效果自定义，支持输入提示词（input.prompt）和字体类型（input.text.ttf\_url和input.text.font\_name），取值类型如下：

"material"：立体材质

"scene": 场景融合

"lighting"：光影特效

“预设风格”大类提供20种风格，此类别为预设的风格效果，不支持用户自定义输入提示词（input.prompt）和字体类型（input.text.ttf\_url和input.text.font\_name），取值类型如下：

"waterfall"：瀑布流水

"snow\_plateau"：雪域高原

"forest"：原始森林

"sky"：天空遨游

"chinese\_building"：国风建筑

"cartoon"：奇幻卡通

"lego"：乐高积木

"flower"：繁花盛开

"acrylic"：亚克力

"marble"：大理石

"felt"：绒线毛毡

"oil\_painting"：复古油画

"watercolor\_painting"：水彩

"chinese\_painting"：中国画

"claborate\_style\_painting"：工笔画

"city\_night"：城市夜景

"mountain\_lake"：湖光山色

"autumn\_leaves"：秋日落叶

"green\_dragon"：青龙献瑞

"red\_dragon"：赤龙呈祥

默认为"material"；

"style\_type": "material"

input. ref\_image\_url

_String_

否

风格参考图的地址，在提供了风格参考图的情况下，input.texture\_style字段将不起作用；

图像要求：图像格式推荐jpg/png/jpeg/bmp，长宽比不大于2，最大边长小于等2048；

若同时提供提示词和参考图，建议参考图侧重用于提供风格的参考，提示词侧重对生成图片的细节描述，提示词应与参考图提供的风格具有一致性，用户可以考虑使用[千问视觉理解大模型（Qwen-VL）](raw/model-user-guide/model-experience/vision-model/vision.md)基于参考图辅助生成提示词。

"ref\_image\_url ":"[https://xxxxx](https://xxxxx)"

parameters.image\_short\_size

_Integer_

否

生成的图片短边的长度，默认为704，取值范围为\[512, 1024\]， 若输入数值非64的倍数，则最终取值为不大于该数值的能被64整除的最大数；

"image\_short\_size": 512

parameters.n

_Integer_

是

生成的图片数量，默认为 1，取值范围为\[1, 4\]

"n": 1

parameters.alpha\_channel

_Bool_

否

是否返回带alpha通道的图片；

默认为 false；

"alpha\_channel": false

### 出参描述

```
{
    "request_id": "54766eb3-ce64-9082-a7f6-7025813d9482",
    "output": {
        "task_id": "91a5933d-6c49-4130-ae30-a14000e37649",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-08-15 10:46:20.054",
        "scheduled_time": "2025-08-15 10:46:20.087",
        "end_time": "2025-08-15 10:46:27.768",
        "results": [
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.jpg"
            },
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.jpg"
            }
        ],
        "task_metrics": {
            "TOTAL": 2,
            "SUCCEEDED": 2,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 2
    }
}
```

字段

类型

描述

示例值

output.task\_id

String

本次请求的异步任务的作业 id，实际作业结果需要通过异步任务查询接口获取。

13b1848b-5493-4c0e-8c44-68d038b492af

output.task\_status

String

提交异步任务后的作业状态。

PENDING

request\_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

### 请求示例

以下示例展示通过CURL命令来调用本模型的脚本

**说明**需要使用您的API-KEY替换示例中的_your-dashscope-api-key_，代码才能正常运行。

```
# 图片输入
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture' \
--header 'X-DashScope-Async: enable' \
--header 'Authorization: Bearer <YOUR_DASHSCOPE_API_KEY>' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
    "model": "wordart-texture",
    "input": {
        "image":
        {
            "image_url": "https://dmshared-new.oss-cn-hangzhou.aliyuncs.com/junyan.hjy/wordart/lcy/example.png"
        },
        "prompt": "水果，蔬菜，温暖的色彩空间",
        "texture_style": "material"
    },
    "parameters":
    {
        "image_short_size": 704,
        "n": 2,
        "alpha_channel": false
    }
}'

# 文字输入
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture' \
--header 'X-DashScope-Async: enable' \
--header 'Authorization: Bearer <YOUR_DASHSCOPE_API_KEY>' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
    "model": "wordart-texture",
    "input": {
        "text":
        {
            "text_content": "文字创意",
            "font_name": "dongfangdakai",
            "output_image_ratio": "1:1"
        },
        "prompt": "水果，蔬菜，温暖的色彩空间",
        "texture_style": "material"
    },
    "parameters":
    {
        "image_short_size": 704,
        "n": 2,
        "alpha_channel": false
    }
}'

# 输入风格参考图
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture' \
--header 'X-DashScope-Async: enable' \
--header 'Authorization: Bearer <YOUR_DASHSCOPE_API_KEY>' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
    "model": "wordart-texture",
    "input": {
        "text":
        {
            "text_content": "文字创意",
            "font_name": "dongfangdakai",
            "output_image_ratio": "16:9"
        },
        "prompt": "鲜花",
        "ref_image_url": "https://dmshared-new.oss-cn-hangzhou.aliyuncs.com/0ximian/transfer_20230801/new_design/tmp/wordposter/ref_images/flower2.png"
    },
    "parameters":
    {
        "image_short_size": 704,
        "n": 2,
        "alpha_channel": false
    }
}'
```

### 响应示例

```
{
    "output": {
		"task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "PENDING"
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
```

### 异常响应示例

在提交作业请求出错的情况下，输出的结果中会通过 code 和 message 指明出错原因。

```
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1"
}
```

### 作业任务状态查询和结果获取接口

GET [](https://dashscope.aliyuncs.com/api/v1/tasks/)[https://dashscope.aliyuncs.com/api/v1/tasks/](https://dashscope.aliyuncs.com/api/v1/tasks/){task\_id}

### 入参描述

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Url Path

task\_id

String

是

需要查询作业的 task\_id

13b1848b-5493-4c0e-8c44-68d038b492af

Header

Authorization

String

是

API-Key，例如：Bearer d1\*\*2a

Bearer d1\*\*2a

### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

本次请求的异步任务的作业 id，实际作业结果需要通过异步任务查询接口获取。

13b1848b-5493-4c0e-8c44-68d038b492af

output.task\_status

String

被查询作业的作业状态

任务状态：

PENDING 排队中

RUNNING 处理中

SUCCEEDED 成功

FAILED 失败

UNKNOWN 作业不存在或状态未知

output.results

Array

如果作业成功，包含模型生成的结果 object，每个 object 中包含按照要求生成的结果地址

\[ {"url":"[https://xxx/1.jpg](https://xxx/1.jpg)"},

{"url":"[https://xxx/2.jpg](https://xxx/2.jpg)"} \]

usage.image\_count

Int

本次请求生成图像计量

"image\_count": 1

request\_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

### 请求示例

以下示例展示通过CURL命令来调用本模型的脚本。

**说明**需要使用您的API-KEY替换示例中的`YOUR-DASHSCOPE-API-KEY`，代码才能正常运行。

```
curl -X GET \
--header 'Authorization: Bearer <YOUR-DASHSCOPE-API-KEY>' \
https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-af6e-a0c6a421c010
```

### 响应示例（作业执行中）

作业提交后将处于排队状态，在得到调度之后将转为运行状态，此时作业的状态为RUNNING，task\_metrics将给出具体batch状态；

```
{
    "request_id":"e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output":{
        "task_id":"86ecf553-d340-4e21-af6e-a0c6a421c010",
        "task_status":"RUNNING",
        "submit_time": "2025-08-15 10:46:20.054",
        "scheduled_time": "2025-08-15 10:46:20.087",
        "end_time": "2025-08-15 10:46:27.768",
        "task_metrics":{
            "TOTAL":1,
            "SUCCEEDED":1,
            "FAILED":0
        }
    }
}
```

### 响应示例（作业成功执行完毕）

如果作业执行完成并成功之后，再次查询作业状态，接口将在告知作业状态的同时，一并将作业的结果返回。对于本模型，作业在结束之后的状态会持续保留24小时以备客户随时查询，24小时之后，作业将从系统中清除，相关的结果也将一并清除；对应的，作业生成的结果为图像的URL地址，出于安全考虑，该URL的下载有效期也是24小时，需要用户在获取作业结果后根据需要及时使用或者转存。

```
{

    "output":{
        "task_id":"a8532587-fa8c-4ef8-82be-0c46b17950d1",
		"task_status":"SUCCEEDED",
        "submit_time": "2025-08-15 10:46:20.054",
        "scheduled_time": "2025-08-15 10:46:20.087",
        "end_time": "2025-08-15 10:46:27.768",
        "results":[
            {
                "url":"https://xxx/1.jpg"
            },
            {
                "url":"https://xxx/2.jpg"
            },
            {
                "url":"https://xxx/3.jpg"
            },
            {
                "url":"https://xxx/4.jpg"
            }
        ]
    },
    "usage":{
        "image_count":4
    },
    "request_id":"7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
```

### 响应示例（作业失败）

如果因为某种原因作业失败，则作业状态会设置为FAILED，并且通过code和message字段指明错误原因。

```
{
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51",
    "output": {
      "task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "FAILED",
        "code": "xxx",
        "message": "xxxxxx"
    }
}
```

## 状态码说明

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)

同时本模型还有如下特定错误码：

http 返回码\*

错误码（code）

错误信息（message）

含义说明

**400**

**InvalidParameter**

The request is missing required parameters or the parameters are out of the specified range, please check the parameters that you send

缺少必要的接口调用参数或参数越界
