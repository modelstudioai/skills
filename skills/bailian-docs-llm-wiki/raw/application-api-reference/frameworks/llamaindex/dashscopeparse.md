# DashScopeParse

DashScopeParse是专门用于高效地解析和表示文件的解析器，以便通过LlamaIndex框架进行高效检索和上下文增强。目前使用的解析服务来自于阿里云 “文档智能（Document Mind）” 。

## 开始

### 前提条件

首先，登录[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)，获取你的API-KEY，当需要指定业务空间时也要获取指定“业务空间id”。

-   已创建API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   已创建业务空间：[业务空间管理](https://help.aliyun.com/zh/model-studio/use-workspace)。

然后，安装DashScopeParse的安装包（python>=3.9,<=3.12）

```
pip install llama-index-core
pip install llama-index-readers-dashscope
```

### 示例代码

现在你可以使用下面的代码获取PDF文件的解析结果了：

```
import os

os.environ['DASHSCOPE_API_KEY'] = "<Your API Key>"
os.environ['DASHSCOPE_WORKSPACE_ID'] = "<Your Workspace id, Default workspace is empty.>"

from llama_index.readers.dashscope.base import DashScopeParse
from llama_index.readers.dashscope.utils import ResultType

file = ['aiayn.pdf', 'not_exist.pdf']
parse = DashScopeParse(result_type=ResultType.DASHSCOPE_DOCMIND, category_id="<category id>")
documents = parse.load_data(file_path=file)
```
**Note：**

-   目前只支持.doc、.docx、.pdf，大小在100M以内且文件页数在1000以内的文件上传、解析。

**Note：**

-   DASHSCOPE\_API\_KEY：是必须指定的API-KEY。
-   DASHSCOPE\_WORKSPACE\_ID：如果使用默认业务空间，可以不指定。如果需要指定业务空间，请指定“业务空间id”。

### 返回结果

结果为Documents对象，json化内容为：（只示例重点字段，其中text字段由于长度过长，所以做了省略显示）

```
[
    {
        "id_": "doc_ab3d344971084f288248d69ba9bada1310022601",
        "metadata": {
            "parse_fmt_type": "DASHSCOPE_DOCMIND"
        },
        "text": "\"{\\\"logics\\\":{\\\"docTree\\\":[{\\\"backlink\\\":{\\\"\u4e0a\u7ea7\\\":[\\\"ROOT\\\"]},\\\"level\\\":0,\\\"link\\\":{\\\"\u4e0b\u7ea7\\\":[],\\\"\u5305\u542b\\\":[]},\\\"uniqueId\\\":\\\"171c391e5e7c68a253eb0adf59fa476d\\\"},{\\\"backlink\\\":{\\\"\u4e0a\u7ea7\\\":[\\\"171c391e5e7c68a253eb0adf59fa476d\\\"]},\\\"level\\\":1,\\\"link\\\":{\\\"\u4e0b\u7ea7\\\":[],\\\"\u5305\u542b\\\":[]},\\\"uniqueId\\\":\\\"397257823ee2878fc4b4a5759fe9afe9\\\"},{\\\"backlink\\\":{\\\"\u4e0a\u7ea7\\\":[\\\"ROOT\\\"]},\\\"level\\\":0,\\\"link\\\":{\\\"\u4e0b\u7ea7\\\":[],\\\"\u5305\u542b\\\":[]},\\\"uniqueId\\\":\\\"08ab57d41ea73966c49191292e1abb5b\\\"},{\\\"backlink\\\":{\\\"\u4e0a\u7ea7\\\":[\\\"08ab57d41ea73966c49191292e1abb5b\\\"]},\\\"level\\\":1,\\\"link\\\":{\\\"\u4e0b\u7ea7\\\":[],\\\"\u5305\u542b\\\":[]},\\\"uniqueId\\\":\\\"2f5ac27b37e3cb65f14799d4811bb633\\\"},......",
    }
]
```

## 参数说明

### 输入参数

参数

类型

默认值

说明

result\_type

_Enum_

ResultType.DASHSCOPE\_DOCMIND

Parser解析结果的类型

num\_workers

int

4

处理多个文件时发起API请求的worker数量

check\_interval

int

5

查询解析状态是的间隔，单位：秒

max\_timeout

int

3600

解析超时时间，单位：秒

workspace

str

None

DashScope workspace id

api\_key

str

None

DashScope api key，可以通过环境变量等方法设置。

category\_id

str

default

指定上传的类目ID

### 输出Document对象字段说明

字段名

字段类型

字段描述

id\_

str

系统生成的文档id

metadata.parse\_fmt\_type

str

解析结果格式化类型

text

str

解析结果字符串，为JSON转义的结果，如果是python语言可以使用json.loads(text)
