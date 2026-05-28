# WritingStyleTemplateField

名称

类型

描述

示例值

object

写作文体表单字段定义

MinItemLength

integer

数组内每个元素的最小长度

1000

Max

double

数值输入的最大值

2000

MinLength

integer

字符输入最小长度

20

MaxLength

integer

字符输入最大长度

2000

MaxItemLength

integer

数组内每个元素的最大长度

4000

Name

string

表单名称

字段名称

BuildIn

boolean

是否为内置字段

true

Enums

array<object>

表单的枚举值列表

object

枚举对象

CascadingFields

array

级联字段列表（详情参考 通知文体的定义）

string

级联字段

级联字段

Key

string

枚举的唯一 KEY

枚举KEY

Name

string

枚举的名称

枚举名称

Min

double

数值输入的最小值

1

Required

boolean

该表单是否必填

false

MaxItem

integer

数组的元素最大个数

10

InitialValue

string

初始化值

初始值

CascadingFields

array

级联字段列表定义（使用方式 参考 通知文体的定义）

[WritingStyleTemplateField](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-struct-writingstyletemplatefield)

级联字段

Style

object

前端样式定义

Placeholder

string

输入框占位符

清输入Prompt

Type

string

表单对应的前端组件样式，可选值：{"input", "textArea", "inputNumber", "datePicker", "segmented", "select", "inputWord", "inputTree"}

media

ShowTime

boolean

日期选择器是否支持时间

Suffix

string

输入框后缀（用来展示单位）

后缀

Description

string

输入框提示文案

输入框提示文案

Format

string

日期格式

yyyy-mm-dd

Key

string

表单字段的 KEY

topic
