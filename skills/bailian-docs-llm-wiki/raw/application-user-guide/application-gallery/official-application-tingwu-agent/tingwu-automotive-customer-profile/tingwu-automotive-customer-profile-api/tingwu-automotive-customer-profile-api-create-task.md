# CreateTask - 创建购车客户画像任务

创建购车客户画像任务的API参考。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

## 接入地址

```
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

## 请求方式

post方法请求

## 请求头

```
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Content-Type: application/json
```

## 创建任务

创建购车客户画像分析任务。

### 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

model

string

是

定义业务类型，固定为tingwu-automotive-customer-profile

tingwu-automotive-customer-profile

input

object

是

传入相关业务参数

input.fileUrl

string

3选1

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

关联已经上传并解析完成的任务

input.appId

string

是

应用id

input.task

string

是

定义任务类型，固定为createTask，表示创建任务

createTask

parameters

object

否

客户画像控制参数

parameters.identityRecognition

object

否

角色设定

parameters.identityRecognition.identityContents

list\[\]

是

角色设定列表，包含身份名称和描述，列表最大长度为5

parameters.identityRecognition.identityContents\[i\].Name

string

是

角色身份名称

客户

parameters.identityRecognition.identityContents\[i\].Description

string

是

角色身份描述

对车辆提出疑问，表达使用感受

parameters.contentExtraction

object

否

客户详细关注点提取参数对象

parameters.contentExtraction.extractionContents

list\[\]

是

客户详细关注点提取的提取维度列表，包含提取项的名称和定义

个数不超过150

parameters.contentExtraction.extractionContents\[i\].title

string

是

客户详细关注点提取的提取维度名称

订车相关

parameters.contentExtraction.extractionContents\[i\].content

string

是

客户详细关注点提取的维度定义

定制颜色要多久？

parameters.contentExtraction.extractionContents\[i\].identity

string

是

客户的角色名称

客户

### 返回参数

**名称**

**类型**

**描述**

**示例值**

output

object

output.dataId

string

任务id

lsA\*\*\*

output.status

string

任务状态：

-   0：成功
    
-   1：进行中
    
-   2：失败
    

0

usage

object

用量

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

### 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-***' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tingwu-automotive-customer-profile",
    "input": {
        "task": "createTask",
        "text": "张3:我想买一个SUV\n李4：想要什么价位的？",
        "appId": "tw_***"
    },
    "parameters": {
        "identityRecognition": {
            "identityContents": [
                {
                    "name": "***",
                    "description": "介绍车辆的不同配置、性能与技术、舒适性与便利性等"
                },
                {
                    "name": "***",
                    "description": "对车辆提出疑问，表达使用感受等"
                }
            ]
        },
        "contentExtraction": {
            "extractionContents": [
                {
                    "title": "***",
                    "content": "车辆基础信息",
                    "identity": "客户询问车型参数、技术配置，销售详细介绍参数信息"
                }
            ]
        }
    }
}'
```

### 返回示例

```
{
    "output": {
        "dataId": "Foi***"
    },
    "usage": {},
    "request_id": "95edfcc7-0481-90aa-884b-3ebf3603b6f8"
}
```
