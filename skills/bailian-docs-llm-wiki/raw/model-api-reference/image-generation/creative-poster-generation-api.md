# 创意海报生成API参考

本文介绍创意海报生成模型的输入输出参数。根据要求自动生成海报的背景和文字排版，支持多种海报风格。无需设计基础，轻松制作出彩作品，让创意触手可及。

**相关指南**：[创意海报生成](https://help.aliyun.com/zh/model-studio/creative-poster-generation-overview)

**重要**

-   本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。
    
-   wanx-poster-generation-v1 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)获取替代方案。
    

## **模型概览**

**模型名**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**计费单价**

**限流（含主账号与RAM子账号）**

**任务下发接口QPS限制**

**同时处理中任务数量**

wanx-poster-generation-v1

500张

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)获取替代方案。

2

1

## **前提条件**

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **创建任务**：首先发送一个请求创建文生图任务，该请求会返回任务ID。
    
-   **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。
    

### **步骤1：创建任务获取任务ID**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

#### **请求头（Headers）**

## 春节快乐海报

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data-raw '{
    "model":"wanx-poster-generation-v1",
    "input": {
        "title":"春节快乐",
        "sub_title":"家庭团聚，共享天伦之乐",
        "body_text":"春节是中国最重要的传统节日之一，它象征着新的开始和希望",
        "prompt_text_zh":"灯笼，小猫，梅花",
        "wh_ratios":"竖版",
        "lora_name":"童话油画",
        "lora_weight":0.8,
        "ctrl_ratio":0.7,
        "ctrl_step":0.7,
        "generate_mode":"generate",
        "generate_num":1
    },
    "auxiliary_parameters": "WMq4SC4......",
    "parameters":{}
}'
```

**Authorization** _string_ **必选**

推荐您使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。

**X-DashScope-Async** _string_ **必选**

是否使用DashScope异步调用。HTTP只支持异步调用，设置为`enable`。

**Content-Type** _string_ **必选**

请求内容类型。固定为`application/json`。

#### **请求体（Request Body）**

**model** _string_ **必选**

调用模型。创意海报生成模型为`wanx-poster-generation-v1`。

**parameters** _object_ **必选**

其他模型调用参数，只需要输入一个空对象即可。示例：`{}`

**input** _object_ **必选**

输入图像的基本信息，比如图像URL地址。

**属性**

**generate\_mode** _string_ **必选**

海报生成模式。

-   generate：默认模式。
    
-   sr：高分辨率模式。
    
-   hrf：高清修复模式。
    
-   只能从\["generate","sr","hrf"\]中选择。海报生成的基础模式为"generate"，选择此模式会返回海报图片的url（render\_urls）和与其一一对应的辅助参数（auxiliary\_parameters）。用户可从返回的结果中，选择需要进行分辨率提升（或者高清修复）的海报，通过二次调用，输入选中的海报对应的辅助参数，将generate\_mode设置为"sr"（或者"hrf"），得到对应的高分辨率（高清修复）结果。
    

**generate\_num** _Int_ 可选

生成的海报数。该参数只在`generate_mode=generate`时有效。

取值范围：\[1,4\]，默认为1。如果设置的值大于4，则默认生成4张图。

**auxiliary\_parameters** _string_ 可选

当generate\_mode为"sr"或"hrf"时为必选项。需要提升分辨率或者高清修复的海报图片对应的辅助参数，数量限制为1。

**注**

该字段必须为海报生成服务的"generate"模式所返回的辅助参数。

**title** _string_ **必选**

主标题。最多30个字符。例如，"春节快乐"。

**sub\_title** _string_ 可选

副标题。最多30个字符。例如，“家庭团聚，共享天伦之乐"。

**body\_text** _string_ 可选

正文。最多50个字符。例如："春节是中国最重要的传统节日之一，它象征着新的开始和希望"

**prompt\_text\_zh** _string_ 可选

中文提示词。例如，“小朋友画的可爱的龙，白色背景"

> 中文和英文提示词至少二选一设置，支持两个参数同时设置。两个字段字符数加起来最多50个字/单词。

**prompt\_text\_en** _string_ 可选

的英文提示词。例如："Children draw a lovely dragon, white background"。

> 中文和英文提示词至少二选一设置，支持两个参数同时设置。两个字段字符数加起来最多50个字/单词。

**wh\_ratios** _string_ 可选

生成海报的版式。

-   横版：默认值。
    
-   竖版
    

**lora\_name** _string_ 可选

海报风格名称。默认值为""。

**海报风格枚举值及图示**

-   2D插画1
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817373.jpeg)

-   2D插画2
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817371.jpeg)

-   浩瀚星云
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817370.jpeg)

-   浓郁色彩
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817378.jpeg)

-   光线粒子
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817368.jpeg)

-   透明玻璃
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817374.jpeg)

-   剪纸工艺
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817376.jpeg)

-   折纸工艺
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817380.jpeg)

-   中国水墨
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817377.jpeg)

-   中国刺绣
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817372.jpeg)

-   真实场景
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817382.jpeg)

-   2D卡通
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817384.png)

-   儿童水彩
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817383.jpeg)

-   赛博背景
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817375.jpeg)

-   浅蓝抽象
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817381.jpeg)

-   深蓝抽象
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817379.jpeg)

-   抽象点线
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817385.jpeg)

-   童话油画
    

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817369.jpeg)

**lora\_weight** _float_ 可选

海报风格权重，需要与lora\_name参数配合使用。

取值范围：\[0, 1\]，默认值为0.8。取值越接近1，海报风格越明显。

**ctrl\_ratio** _float_ 可选

留白效果权重，用于控制海报留白效果。

取值范围：\[0, 1\]，默认值为0.7。取值越接近1，留白效果越好，但海报背景生成效果可能会受到负面影响。

**ctrl\_step** _float_ 可选

留白步数比例，用于控制海报留白效果。

取值范围：(0, 1\]，默认值为0.7。取值越接近1，留白效果越好，但是海报背景生成效果可能会受到负面影响。

**creative\_title\_layout** _bool_ 可选

标题是否启用创意排版。默认值为false。

#### **响应**

## 成功响应

```
{
    "output": {
	"task_id": "d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx", 
        "task_status": "PENDING"
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
```

## 异常响应

```
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1"
}
```

**output** _object_

任务输出信息。

**属性**

**task\_id** _string_

任务id。

**task\_status** _string_

任务状态。

-   PENDING：排队中
    
-   RUNNING：处理中
    
-   SUSPENDED：挂起
    
-   SUCCEEDED：执行成功
    
-   FAILED：执行失败
    

**code** _string_

接口错误码。接口成功请求不会返回该参数。

**message** _string_

接口错误信息。接口成功请求不会返回该参数。

**request\_id** _string_

请求唯一标识。可用于请求明细溯源和问题排查。

### **步骤2：根据任务ID查询结果**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

#### **请求头（Headers）**

## 获取任务结果

```
curl --location --request GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** _string_ **必选**

推荐使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。

#### **URL路径参数（Path parameters）**

**task\_id** _string_ **必选**

任务id。

#### **响应**

## 任务执行成功

```
{
    "request_id": "b67df059-ca6a-9d51-afcd-9b3c4456b1e2",
    "output": {
        "task_id": "d76ec1e8-ea27-4038-8913-235c88ef0f70",
        "task_status": "SUCCEEDED",
        "submit_time": "2024-05-16 13:50:01.247",
        "scheduled_time": "2024-05-16 13:50:01.354",
        "end_time": "2024-05-16 13:50:27.795",
        "render_urls": ["http://vision-poster.oss-cn-shanghai.aliyuncs.com/xxxxxx"],
        "auxiliary_parameters": ["xxxxxx"],
        "bg_urls":["http://vision-poster.oss-cn-shanghai.aliyuncs.com/xxxxxx"]
    },
    "usage":{
      "image_count":1
    }
}
```

## 任务执行中

```
{
    "request_id":"e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output":{
        "task_id":"86ecf553-d340-4e21-af6e-a0c6a421c010",
        "task_status":"RUNNING",
        "task_metrics":{
            "TOTAL":1,
            "SUCCEEDED":1,
            "FAILED":0
        }
    }
}
```

## 任务执行失败

```
{
    "request_id": "dccfdf23-b38e-97a6-a07b-f35118c1ada6",
    "output": {
        "task_id": "4cbabbdf-2c1f-43f4-b983-c2cc47f4c115",
        "task_status": "FAILED",
        "submit_time": "2024-05-16 14:15:14.103",
        "scheduled_time": "2024-05-16 14:15:14.154",
        "end_time": "2024-05-16 14:15:14.694",
        "code": "InvalidParameter",
        "message": "check input data style"
    }
}
```

**output** _object_

任务输出信息。

**属性**

**task\_id** _string_

任务id。

**task\_status** _string_

任务状态。

-   PENDING：排队中
    
-   RUNNING：处理中
    
-   SUSPENDED：挂起
    
-   SUCCEEDED：执行成功
    
-   FAILED：执行失败
    

**render\_urls** _list\[string\]_

海报图像URL列表。海报图像URL有效时限为24小时。

-   当`generate_mode=generate`时，返回1～4张海报图像的URL列表。
    
-   当`generate_mode=sr`或者`generate_mode=hrf`时，返回1张海报图像的URL。
    

在返回海报图像URL之前，会进行敏感信息检测。如发现敏感内容，将拦截该图像，并替换为`output data may contain inappropriate content`。

**auxiliary\_parameters** _List\[String\]_

高清修复和提升分辨率的辅助参数，与render\_urls列表的URL一一对应。有效时限为24小时。

接口返回的auxiliary\_parameters可用于二次调用，将其作为入参，对海报进行分辨率提升或者高清修复。

在返回海报图像URL之前，会进行敏感信息检测。如发现敏感内容，将拦截该图像，并替换为`output data may contain inappropriate content`。

**bg\_urls** _List\[String\]_

不含文字的海报背景图URL。有效时限为24小时。

-   当`generate_mode=generate`时，返回1～4张海报图像的URL列表。
    
-   当`generate_mode=sr`或者`generate_mode=hrf`时，返回1张海报图像的URL。
    

在返回海报图像URL之前，会进行敏感信息检测。如发现敏感内容，将拦截该图像，并替换为`output data may contain inappropriate content`。

**task\_metrics** _object_

任务信息统计指标。

**属性**

**TOTAL** _integer_

总的任务数。

**SUCCEEDED** _integer_

任务状态为成功的任务数。

**FAILED** _integer_

任务状态为失败的任务数。

**submit\_time** _string_

任务提交时间。

**scheduled\_time** _string_

任务排期执行时间。

**end\_time** _string_

任务完成时间。

**code** _string_

接口错误码。接口成功请求不会返回该参数。

**message** _string_

接口错误信息。接口成功请求不会返回该参数。

**usage** _object_

输出信息统计。

**属性**

**image\_count** _integer_

生成图像的数量。

**request\_id** _string_

请求唯一标识。可用于请求明细溯源和问题排查。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

同时本模型还有如下特定错误码：

**HTTP状态码**

**接口错误码（code）**

**接口错误信息（message）**

**含义说明**

400

InvalidParameter

check input data style

输入参数不满足入参要求

500

InternalError

inference error

算法内部错误

## 常见问题

-   **如何查询已经提交的所有异步任务？**
    
    具体操作请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#3092aa5c70jmd)。
    
-   **创意海报生成API是否支持对已经生成的海报进行二次编辑？**
    
    不支持对已生成海报的内容（如标题、正文、风格等）进行二次编辑。仅能通过再次调用本API来提升已生成海报的分辨率。如需调整海报的内容，请重新设计并生成新的海报。
    
    提升已生成海报分辨率的方法为：将上次生成海报时的输入参数`"generate_mode"`的值修改为`sr`或`hrf`，并在输入参数中新增`"auxiliary_parameters"`，其值为上次生成海报时返回的完整参数集，其它参数保持不变。
    
    ```
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header 'Content-Type: application/json' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --data-raw '{
        "model":"wanx-poster-generation-v1",
        "input": {
            "title":"春节快乐",
            "sub_title":"家庭团聚，共享天伦之乐",
            "body_text":"春节是中国最重要的传统节日之一，它象征着新的开始和希望",
            "prompt_text_zh":"灯笼，小猫，梅花",
            "wh_ratios":"竖版",
            "lora_name":"童话油画",
            "lora_weight":0.8,
            "ctrl_ratio":0.7,
            "ctrl_step":0.7,
            "generate_mode":"hrf",
            "auxiliary_parameters": "WMq4SC4......",
            "generate_num":1
        },
        "parameters":{}
    }'
    ```
