# CutQuestions - 试卷切题

切题及题目结构化接口，客户输入试卷或整页题目图片，算法返回每个题目的位置信息以及结构化（题干、选项、答案等）信息。

## 接口说明

开通 EduTutor 服务。本接口在公测阶段，每个账号每天可以免费调用 1000 次。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/EduTutor/2025-07-07/CutQuestions)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/EduTutor/2025-07-07/CutQuestions)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

edututor:CutQuestions

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /service/cutApi HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

当前请求所使用的百炼业务空间 id。

llm-1ijrzuv3v0ivvls7

body

object

否

请求 body。

image

string

是

试卷、题目图片链接。

https://oss.xxx.com/xx.png

parameters

object

是

参数配置。

struct

boolean

是

是否返回结构化信息。

true

extract\_images

boolean

是

是否返回子题临时 oss 链接，便于后续答题直接使用。

true

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

请求 id，每次请求都是唯一值，便于后续排查问题。

1CE2851D-96D6-51D0-8ADA-EB7ACAF374BB

success

boolean

调用是否成功。

True

code

string

响应状态码。

SUCCESS

httpStatusCode

integer

http 状态码。

200

message

string

返回码描述。

success

data

string

算法返回结果。

'{ "questions": \[ { "pos\_list": \[ \[ 21, 0, 364, 0, 364, 82, 21, 82 \] \], "sub\_images": \[ "http://duguang-mld.oss-accelerate.aliyuncs.com/ocr\_edu/1CE2851D-96D6-51D0-8ADA-EB7ACAF374BB\_0\_0.png?OSSAccessKeyId=LTAI5tPtEwpyT4JR9Gym\*\*\*\*&Expires=1755593474&Signature=SnqwepQVvZ51PnUGtpH0fWV50JI%3D" \], "merged\_image": "http://duguang-mld.oss-accelerate.aliyuncs.com/ocr\_edu/1CE2851D-96D6-51D0-8ADA-EB7ACAF374BB\_0\_0.png?OSSAccessKeyId=LTAI5tPtEwpyT4JR9Gy\*\*\*\*&Expires=1755593474&Signature=SnqwepQVvZ51PnUGtpH0fWV50JI%3D", "info": { "stem": { "text": "8. 若 \\\\\\\\(a + b = -1\\\\\\\\), \\\\\\\\(ab = 4\\\\\\\\), 则 \\\\\\\\((4a - 5b - 3ab) - (3a - 6b + ab)\\\\\\\\) 的值为 \_ 。", "pos\_list": \[ \[ 21, 4, 364, 4, 364, 78, 21, 78 \] \] }, "option": \[\], "figure": \[\], "answer": \[ { "text": "-17", "pos\_list": \[ \[ 225, 51, 262, 51, 262, 70, 225, 70 \] \] } \], "type": "填空题", "subquestion": \[\] } } \] }'

input\_tokens

integer

此次调用输入消耗的 token 数。

80

output\_tokens

integer

此次调用输出消耗的 token 数。

38

#### [](#算法结果字段-data)算法结果字段 data

-   需要序列化，字段说明如下：

字段

类型

描述

示例值

questions

array

模型切出来的题目数组。

questions\[i\].pos\_list

array

第 i 道题目的坐标框（可能含有多个）。

\[\[21,0,364,0,364,82,21,82\]\]

questions\[i\].sub\_images

array

根据坐标框提取出来的子图图片链接（7 天有效）。

questions\[i\].merged\_image

string

所有子图合并之后的题目完整图片链接（7 天有效）。

questions\[i\].info

object

题目结构化信息。

questions\[i\].info.type

string

题目类型：选择题/填空题/判断题/问答题/作文题/其他。

填空题

questions\[i\].info.stem

array

题干信息。

questions\[i\].info.stem.text

string

题干文本信息。

questions\[i\].info.stem.pos\_list

array

题干坐标框信息。

questions\[i\].info.option

array

选项信息。

questions\[i\].info.option\[j\].text

string

选项文本信息。

questions\[i\].info.option\[j\].pos\_list

array

选项位置信息。

questions\[i\].info.figure

array

插图信息。

questions\[i\].info.figure\[k\].pos\_list

array

插图位置信息。

questions\[i\].info.answer

array

答案信息。

questions\[i\].info.answer\[m\].pos\_list

array

答案位置信息。

"-17"

questions\[i\].info.answer\[m\].text

string

答案文本信息。

questions\[i\].info.subquestion

array

子题信息（结构和 info 一致）。

举例：

```
{
    "questions": [
        {
            "pos_list": [
                [
                    21,
                    0,
                    364,
                    0,
                    364,
                    82,
                    21,
                    82
                ]
            ],
            "sub_images": [
                "http://xxxxx/sub_images/1CE2851D-96D6-51D0-8ADA-EB7ACAF374BB_0_0.png"
            ],
            "merged_image": "http://xxxxx/sub_images/1CE2851D-96D6-51D0-8ADA-EB7ACAF374BB.png",
            "info": {
                "stem": {
                    "text": "8. 若 \\\\(a + b = -1\\\\), \\\\(ab = 4\\\\), 则 \\\\((4a - 5b - 3ab) - (3a - 6b + ab)\\\\) 的值为 _ 。",
                    "pos_list": [
                        [
                            21,
                            4,
                            364,
                            4,
                            364,
                            78,
                            21,
                            78
                        ]
                    ]
                },
                "option": [],
                "figure": [],
                "answer": [
                    {
                        "text": "-17",
                        "pos_list": [
                            [
                                225,
                                51,
                                262,
                                51,
                                262,
                                70,
                                225,
                                70
                            ]
                        ]
                    }
                ],
                "type": "填空题",
                "subquestion": []
            }
        }
    ]
}
```

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "1CE2851D-96D6-51D0-8ADA-EB7ACAF374BB",
  "success": true,
  "code": "SUCCESS",
  "httpStatusCode": 200,
  "message": "success",
  "data": "'{\n    \"questions\": [\n        {\n            \"pos_list\": [\n                [\n                    21,\n                    0,\n                    364,\n                    0,\n                    364,\n                    82,\n                    21,\n                    82\n                ]\n            ],\n            \"sub_images\": [\n                \"http://duguang-mld.oss-accelerate.aliyuncs.com/ocr_edu/1CE2851D-96D6-51D0-8ADA-EB7ACAF374BB_0_0.png?OSSAccessKeyId=LTAI5tPtEwpyT4JR9Gym****&Expires=1755593474&Signature=SnqwepQVvZ51PnUGtpH0fWV50JI%3D\"\n            ],\n            \"merged_image\": \"http://duguang-mld.oss-accelerate.aliyuncs.com/ocr_edu/1CE2851D-96D6-51D0-8ADA-EB7ACAF374BB_0_0.png?OSSAccessKeyId=LTAI5tPtEwpyT4JR9Gy****&Expires=1755593474&Signature=SnqwepQVvZ51PnUGtpH0fWV50JI%3D\",\n            \"info\": {\n                \"stem\": {\n                    \"text\": \"8. 若 \\\\\\\\(a + b = -1\\\\\\\\), \\\\\\\\(ab = 4\\\\\\\\), 则 \\\\\\\\((4a - 5b - 3ab) - (3a - 6b + ab)\\\\\\\\) 的值为 _ 。\",\n                    \"pos_list\": [\n                        [\n                            21,\n                            4,\n                            364,\n                            4,\n                            364,\n                            78,\n                            21,\n                            78\n                        ]\n                    ]\n                },\n                \"option\": [],\n                \"figure\": [],\n                \"answer\": [\n                    {\n                        \"text\": \"-17\",\n                        \"pos_list\": [\n                            [\n                                225,\n                                51,\n                                262,\n                                51,\n                                262,\n                                70,\n                                225,\n                                70\n                            ]\n                        ]\n                    }\n                ],\n                \"type\": \"填空题\",\n                \"subquestion\": []\n            }\n        }\n    ]\n}'",
  "input_tokens": 80,
  "output_tokens": 38
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/EduTutor/2025-07-07/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
