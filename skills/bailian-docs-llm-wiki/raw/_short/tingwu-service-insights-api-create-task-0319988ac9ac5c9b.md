# CreateTask - 创建通用服务洞察任务

创建通用服务洞察任务，包括创建离线转写任务和服务质检任务。

## 接入地址

```
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

## 请求方式

post方法

## 请求头

```
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Content-Type: application/json
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

model

string

是

定义业务类型，固定为`tingwu-service-insights`

tingwu-service-insights

input

object

是

传入相关业务参数

input.fileUrl

string

以下三个参数互斥且必选其一：fileUrl（音频文件OSS地址）、text（待分析文本）、dataId（已解析任务ID）

待分析文件oss URL地址

https://_**.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=YOUR\_ACCESS\_KEY\_ID&Expires=**_&Signature=YOUR\_SIGNATURE

input.text

string

待分析文本

每行必须按照如下格式：

${发言人名称}: ${发言人内容}

例子比如：

```
张3: 我想买一个SUV汽车
李4: 想要什么价位的？
```

input.dataId

string

关联已上传并解析完成的任务

input.appId

string

是

应用id，可在控制台的应用配置页面获取

input.task

string

是

定义任务类型，固定为`createTask`，表示创建任务

createTask

parameters

object

否

通用服务洞察控制参数（若传入空对象则复用已发布上线的配置项）

parameters.serviceInsights

object

否

通用服务洞察参数对象

parameters.serviceInsights.insightsContents

list\[\]

是

通用服务洞察的维度列表，包含洞察维度名称和定义，即需要大模型以什么样的标准判断该维度是否命中

**个数不超过150个**

parameters.serviceInsights.insightsContents\[i\].title

string

是

通用服务洞察项的标题

开场白

parameters.serviceInsights.insightsContents\[i\].content

string

是

通用服务洞察项的内容

客户代表在接听电话时没有使用开场白，例如 您好，很高兴为您服务

serviceInsights.insightsContents\[i\].score

string

否

汽车销售洞察项分值，用来表示该洞察项命中后，增加或扣减的分值，若未命中则为0

**范围是\[-100, 100\]**

50

## 返回参数

**名称**

**类型**

**描述**

**示例值**

output

object

output.dataId

string

任务id

output.status

string

-   0：成功
    
-   1：进行中
    
-   2：失败
    

0

usage

object

用量，目前为空object

{}

code

string

错误码

InvalidParameter

message

string

错误信息

Agent Input text format error.

request\_id

string

请求id

f97ee37d-0f9c-9b93-b6bf-bd263a232bf9

## 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-******e181c' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tingwu-service-insights",
    "input": {
        "task": "createTask",
        "text": "张*:我想买一个SUV\n李*:想要什么价位的？",
        "appId": "tw_***"
    },
    "parameters": {
        "serviceInsights": {
            "insightsContents": [
                {
                    "title": "到店迎接-欢迎语",
                    "content": "销售在开场白的时候主动向客户打招呼进行欢迎",
                    "score": "20"
                },
                {
                    "title": "离店送别-客户留资",
                    "content": "销售邀请客户留下微信、电话号码、名片等联系方式",
                    "score": "30"
                },
                {
                    "title": "到店迎接-饮品提供",
                    "content": "销售在接待客户的时候主动询问是否需要饮料（如咖啡、橙汁、水、茶等）、点心、零食、水果等",
                    "score": "50"
                }
            ]
        }
    }
}'
```

## 返回示例

```
{
    "output": {
        "dataId": "dj***"
    },
    "usage": {},
    "request_id": "8313c0bc-ff3f-98e8-b87a-0118f6fe3049"
}
```
