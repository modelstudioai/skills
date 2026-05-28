# 长期记忆开放接口

本文档介绍长期记忆的开放接口，用户可以通过接口干预记忆挖掘策略，管理记忆结果。

## 使用说明

1\. 如需使用长期记忆能力，请先在应用配置界面开启长期记忆开关。

2\. 开启长期记忆后，默认启用通用记忆配置，记忆用户的个人信息、兴趣爱好、近期行为等，并在后续对话中自动召回，无需额外操作。以userid维度进行记忆的存储。

3\. 如需根据业务场景自定义记忆策略，可使用本文档提供的接口。API配置后即时生效，并自动覆盖系统默认的记忆策略。

4\. 如需对记忆结果进行查询和修改，可使用本文档提供的接口。

Endpoint: sfmmultimodalapp.cn-beijing.aliyuncs.com

Region: cn-beijing

## 接入示例

### java

第一步：引入sdk

```
<dependency>
    <groupId>com.aliyun</groupId>
    <artifactId>sfmmultimodalapp20250909</artifactId>
    <version>1.1.2</version>
</dependency>
```

第二步：代码示例

```
Config config = new Config();
        config.setAccessKeyId("*");
        config.setAccessKeySecret("*");

        config.setEndpoint("********");  
        config.setRegionId("********"); 
        Client client = new Client(config);

        QueryMemoryConfigRequest request = new QueryMemoryConfigRequest();
        request.setWorkspaceId("llm-*"); //百炼的工作空间ID
        request.setAppId("*");  //百炼多模态交互套件APPID
        request.setUserDefinedId("*");

        QueryMemoryConfigResponse queryProfileResponse = client.queryMemoryConfig(request);
        System.out.println(JsonUtils.toJson(queryProfileResponse.getBody()));
```

### python

第一步：安装sdk

pip install -i [http://yum.tbsite.net/aliyun-pypi/simple/](http://yum.tbsite.net/aliyun-pypi/simple/)\--extra-index-url [http://yum.tbsite.net/pypi/simple/](http://yum.tbsite.net/pypi/simple/)\--trusted-host=yum.tbsite.net alibabacloud-sfmmultimodalapp20250909==1.1.2

第二步：代码示例

```
import sys
from typing import List

from Tea.exceptions import UnretryableException, TeaException
from alibabacloud_sfmmultimodalapp20250909.client import Client as SfmMultiModalApp20250909Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sfmmultimodalapp20250909 import models as sfm_multi_modal_app_20250909_models

class PopRequest:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> SfmMultiModalApp20250909Client:
        config = open_api_models.Config(
            access_key_id='*',
            access_key_secret='*'
        )

        config.endpoint = f'*******'
        return SfmMultiModalApp20250909Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        client = PopRequest.create_client()
        memory_config_request = sfm_multi_modal_app_20250909_models.QueryMemoryConfigRequest(
            workspace_id='*',
            app_id='*',
            user_defined_id='*'
        )
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.query_memory_config(memory_config_request)
            print('body', res.body)
            if res.body.success:
                print('data', res.body.data)
        except UnretryableException as e:
            # 网络异常
            print(e)
        except TeaException as e:
            # 业务异常
            print(e)
        except Exception as e:
            # 其他异常
            print(e)

if __name__ == '__main__':
    PopRequest.main(sys.argv[1:])
```

**前置条件**

1.  需要首先登录阿里云，进入访问控制，为请求的ram账号分配权限：AliyunSFMMultiModalAppFullAcces，管理阿里云多模态交互开发套件（sfmmultimodalapp）的权限。
    
2.  ram账号同时必须在百炼有该工作空间id的权限。
    

## 接口列表

公共响应参数

参数

类型

必填

描述

requestId

String

是

请求Id

success

Boolean

是

是否成功

code

String

是

返回码

httpStatusCode

Integet

是

http状态码

message

String

否

返回消息

data

Object

否

返回数据

### **记忆策略配置**

#### **用户画像（profile）**

用户画像用于设定具体的记忆挖掘策略，例如个人信息、兴趣爱好、行为偏好等。

多模态交互开发套件提供默认的用户画像挖掘规则，基本覆盖个人用户的生活和工作场景。如需自定义，可参考以下接口。支持进行用户级别、应用级别的用户画像配置。

通过接口完成配置后，将覆盖默认的用户画像配置。

##### **1\. 创建profile\_schema(CreateProfile)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

否

用户id(用户唯一标识，在工作空间下保持唯一)

workspaceId

varchar

是

空间id

appId

String

是

应用id

name

String

是

profile名称

description

String

是

profile描述

attributes

Array

是

属性

\[0\].name

String

是

名称，应该尽可能保证在语义中唯一，不然会对抽取效果有一定影响，如\[“姓名”、“名称”、“名字”\]，\[“年龄”，“年纪”，“岁数”\] 不应该同时出现

\[0\].description

String

否

描述

\[0\].immutable

Boolean

否

是否不可修改，默认False

\[0\].defaultValue

String

否

初始值, 如果immutable为True则必填

出参：

参数

类型

必填

描述

requestId

String

是

请求Id

schemaId

String

是

用户画像Id

name

String

是

profile名称

description

String

是

profile描述

##### **2\. 更新profile\_schema(UpdateProfile)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

否

用户id(用户唯一标识，在工作空间下保持唯一)

workspaceId

varchar

是

百炼工作空间id

appId

String

是

多模态应用id

name

String

否

profile名称

description

String

否

profile描述

attributesOperations

Array

是

属性

\[0\].op

String

是

枚举值："add"表示新增, "update"表示更新, "delete"表示删除

\[0\].attributeId

String

否

attribute\_id, op为"update"或者"delete"为必填

\[0\].name

String

否

名称，add时必填,如果name变更，可能会造成之前的值有异常

\[0\].description

String

否

描述

\[0\].defaultValue

String

否

默认值

出参：

参数

类型

必填

描述

requestId

String

是

请求Id

name

String

是

profile名称

description

String

是

profile描述

##### **3\. 删除profile\_schema(DeleteProfile)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

否

用户id

workspaceId

varchar

是

空间id

appId

String

是

应用id

出参：

参数

类型

必填

描述

requestId

String

是

请求Id

##### **4\. 获取profile\_schema详情(QueryProfile)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

否

用户id

workspaceId

varchar

是

空间id

appId

String

是

应用id

出参：

**参数**

**类型**

**必填**

**描述**

name

String

是

profile名称

description

String

是

profile描述

attributes

Object

是

属性

\[0.\]attributeId

String

是

属性id

\[0.\]name

String

是

名称

\[0.\]description

String

否

描述

\[0.\]immutable

Boolean

否

不可修改，默认False

\[0.\]defaultValue

String

否

初始值, 如果immutable为True则必填

##### **5\. 获取用户画像数据(QueryUserProfile)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

是

用户id

workspaceId

varchar

是

工作空间id

appId

String

是

应用id

出参：

**参数**

**类型**

**必填**

**描述**

name

String

是

profile名称

description

String

是

profile描述

attributes

Object

是

属性

\[0.\]id

String

是

id

\[0.\]name

String

是

名称

\[0.\]value

String

否

值

#### 记忆片段配置（memory config）

记忆片段用于挖掘用户画像之外的零散记忆片段，例如近期行为等。可以通过prompt配置具体的记忆策略。

##### **1\. 更新记忆片段配置(PatchMemoryConfig)**

不存在就新增，存在就修改

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

否

用户id

workspaceId

String

是

空间id

appId

String

是

应用id

prompt

String

否

自定义指令，影响记忆抽取的效果

autoUpdate

Boolean

否

记忆合并更新，建议传true，避免数据膨胀

expirationTime

integer

否

记忆过期时间

topK

integer

否

最大召回数量

threshold

Double

否

最低阈值，建议值0.03

出参：

**参数**

**类型**

**必填**

**描述**

requestId

String

是

请求id

##### **2\. 查询记忆片段配置(QueryMemoryConfig)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

否

用户id

workspaceId

varchar

是

空间id

appId

String

是

应用id

出参：

**参数**

**类型**

**必填**

**描述**

requestId

String

是

请求id

prompt

String

否

自定义指令，影响记忆抽取的效果，对应新增记忆的customInstructions

autoUpdate

Boolean

否

记忆合并更新，建议传true，避免数据膨胀

expirationTime

integer

否

记忆过期时间

topK

integer

否

最大召回数量

threshold

Double

否

最低阈值，建议值0.03

### **记忆数据管理**

#### **记忆管理(memory)**

记忆管理接口，用于查询、编辑单个用户的记忆挖掘结果。

##### **1\. 新增记忆内容(CreateMemory)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

是

用户id

workspaceId

String

是

空间id

appId

String

是

应用id

content

String

否

自定义内容，固定会存入记忆数据content和messagesJson必填一个

projectId

String

是

用户画像：profile\_project

记忆片段：observation\_project

messagesJson

String

否

消息列表，Json字符串，messages\[0\].role String messages\[0\].content String｜Array 支持多模态，参考Omni入参

prompt

String

否

自定义指令，影响记忆抽取的效果，比如，”仅关注用户的职业信息，不要关注年龄，性别等隐私信息”

autoUpdate

Boolean

否

记忆合并更新，建议传true，避免数据膨胀

expirationTime

Integer

否

过期时间，值域\[1-180\]

\-1 表示不过期

metaData

Object

否

元信息,(建议传如下字段)

\[0\].dialog\_id

String

否

对话id，用于记录属于哪轮对话

\[0\].locationName

String

否

地理位置（语义）

\[0\].workspaceId

String

否

百炼工作空间id

\[0\].geoCoordinate

String

否

坐标，格式参考坐标转换 - 高德地图 API

\[0\].mediaDesc

Array

否

多模态信息表述

mediaDesc

**参数**

**类型**

**必填**

**描述**

url

String

否

多模态文件url

description

String

否

对应文本描述信息

出参：

**参数**

**类型**

**必填**

**描述**

requestId

String

是

请求Id

memoryNodes

Array

变更的记忆列表

\[0\].memoryNodeId

String

是

多模态文件url

\[0\].content

String

是

对应文本描述信息

\[0\].event

String

是

记忆事件，表示新增，更新，删除  
"ADD","UPDATE","DELETE"

\[0\].oldContent

String

否

过去的内容，仅当event为"UPDATE"时有效

##### **2\. 查询记忆列表(QueryMemoryList)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

是

用户id

workspaceId

varchar

是

空间id

appId

String

是

应用id

projectId

String

否

用户画像：profile\_project

记忆片段：observation\_project，

多模态应用为必填，语音应用可空

pageSize

Integer

否

每页大小，默认10

pageNum

Integer

否

页号，默认1

出参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

是

用户id

workspaceId

varchar

是

空间id

appId

String

是

应用id

memoryNodes

Array

是

记忆列表

\[0\].memoryNodeId

String

是

生成的记忆唯一Id

\[0\].content

String

是

生成的记忆内容

\[0\].timestamp

String

是

消息时间戳

\[0\].createdAt

String

是

创建时间

\[0\].updatedAt

String

是

更新时间

\[0\].projectId

String

是

在add/update时所指定的projectId，可能为空

\[0\].metaData

Obejct

否

元信息

total

Integer

是

总数

pageSize

Integer

是

每页大小

pageNum

Integer

是

页号

##### **3\. 删除记忆内容(DeleteMemory)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

是

用户id

workspaceId

varchar

是

空间id

appId

String

是

应用id

memoryNodeId

String

是

生成的记忆唯一Id

出参：

**参数**

**类型**

**必填**

**描述**

requestId

String

是

请求Id

##### **4\. 修改记忆内容(UpdateMemory)**

入参：

**参数**

**类型**

**必填**

**描述**

userDefinedId

String

是

用户id

workspaceId

varchar

是

空间id

appId

String

是

应用id

memoryNodeId

String

是

生成的记忆唯一Id

projectId

String

否

用户画像：profile\_project

记忆片段：observation\_project

metaData

Object

否

元信息，建议如下传

\[0\].dialog\_id

String

否

对话id，用于记录属于哪轮对话

\[0\].locationName

String

否

地理位置（语义）

\[0\].workspaceId

String

否

工作空间id

\[0\].geoCoordinate

String

否

坐标，格式参考坐标转换 - 高德地图 API

\[0\].mediaDesc

Array

否

多模态信息表述

mediaDesc

**参数**

**类型**

**必填**

**描述**

url

String

否

多模态文件url

description

String

否

对应文本描述信息

## 附录

目前，基于用户维度的长期记忆，可挖掘和召回以下内容：

**说明**

下面表格是默认的用户画像，如果通过接口定义用户画像，这些内容将会被覆盖掉。

profile模块

profile

举例

个人信息

姓名：包括姓名、昵称、英文名等

用户名字叫小白，英文名叫Mike

出生日期：出生年月日、年龄、年龄段、星座、属相等

用户生日是1月22日，属牛

性别

用户是女生

民族

用户是朝鲜族人，能听懂韩语但不太会讲

身高、体重、血型

用户身高160cm，是O型血

职业

用户之前在金融公司上班，现在自己创业开餐厅

教育背景

用户毕业于清华大学计算机系，毕业时间是2016年

重要日期：纪念日等

5月1日是用户的结婚纪念日

过敏史

用户对鸡蛋过敏，不能食用任何含鸡蛋的食物

用户对花粉过敏，春天尽量不去植物多的地方

地域：所在城市、家庭/公司/学校住址、籍贯等

用户是江苏人，在上海工作

用户的公司地点在陆家嘴

语言：母语、第二语言、方言等

用户会说英文和粤语，最近在学习日语

宗教信仰

用户没有宗教信仰，但偶尔会去寺庙走走

兴趣偏好

饮食偏好：口味、菜系、饮食文化、食物名称、餐厅名称、饮食禁忌、用餐习惯等

用户喜辣，爱吃四川火锅

用户不喜欢吃香菜

用户喜欢研究葡萄酒文化

用户对鸡蛋过敏

旅行偏好：目的地类型、目的地名称、旅行方式、季节偏好、住宿类型等

用户喜欢自然风光类景点

用户喜欢冬天去滑雪

用户偏向选择住民宿

购物偏好：购物方式、偏好品牌、价格敏感度、支付习惯等

用户喜欢双十一在淘宝囤货，喜欢研究各种打折活动

用户爱买xx品牌的衣服

阅读偏好：文学类型、书籍类型、书籍名称、作者名称、阅读习惯等

用户喜欢法国文学

用户喜欢读余华的书

用户倾向于阅读纸质书

收听偏好：音乐/播客/有声书等类型和名称、歌手/主播/创作者的风格和名字、收听平台、收听时段、收听时长等

用户喜欢早晨上班路上听科技播客

用户喜欢听周杰伦的歌

用户喜欢利用碎片时间听英语口语课

观影偏好：内容领域、电影/电视/综艺/纪录片/话剧等的类型和名称、演员/导演/博主等的类型和名字等

用户最近爱看短剧

用户喜欢喜剧片，最爱的演员是xxx

用户最喜欢的探店博主是xxx

运动偏好：运动项目、运动频率、运动场地等

用户最近每周至少晨跑三次

用户喜欢骑行，不擅长打篮球

出行偏好：常用交通工具、座位偏好等

用户短途出行倾向于高铁而不是飞机

用户喜欢靠窗的座位

衣着偏好：着装风格、配色风格、服装材质和图案、服装品牌等

用户喜欢棉质衣服，因为更透气舒适

用户喜欢休闲风格的穿着，尤其是牛仔裤

其他兴趣偏好，具体到细分的类别和名称

用户喜欢摄影，爱拍人像

用户最近对插花很感兴趣

生活习惯和状态

作息：睡眠习惯、生活规律等

用户每天要午睡30分钟

对话风格：喜欢的对话风格

用户希望助手用活泼的语气对话

思考方式：感性/理性，喜欢直接获得答案/通过对话引导思考等

用户希望引导思考而不是直接给出答案

技能水平：语言、运动等的技能水平

用户英语口语一般，希望通过练习快速提升

健康状况

基础指标：BMI、血压、心率等

用户BMI偏低，医生建议适当增重

身体异常状况：生病、感到身体不适等

用户最近有点感冒，喉咙不舒服

心理状况：焦虑、兴奋、疲惫等

用户最近心情不好，因为心爱的小狗去世了

人格特质：MBTI类型等

用户是ESTJ人格

医疗记录：手术/住院记录、长期用药清单、术后恢复计划等

用户刚刚做了阑尾手术，最近每天要服用三次xx药物

生活记录

购物历史：最近购入的商品

用户前两天买了很多清洁用品

浏览历史：影音、文章等浏览和阅读历史

用户今天把甄嬛传看到了30集

行程历史：最近去过的城市、地点

用户昨天去了故宫和天安门

设备密码

用户家里的Wi-Fi密码是29283238

个人计划

短期计划：会议安排、购物清单、医院就诊等

用户明天要去超市购买水果和水杯

用户下周一要去牙科复诊

长期计划：职业规划、健身计划、减重目标、学习计划、财务目标等，以及完成进展

用户计划今年内减肥10斤

家庭相关

家庭成员/朋友基础信息：名字、年龄、职业、生活偏好等

用户的女儿叫小浩，3岁，最近喜欢看绘本

用户最好的朋友是Lily，认识5年了，生日是10月15号

家庭成员/朋友生活状况：孩子的营养补充计划、喜欢的游戏和玩具、学校班级等，老人的健康状态、饮食习惯等

用户的妈妈有高血压，每天早上要吃降压药

用户的儿子现在三年级，每周要上美术班

宠物相关：品种、昵称、年龄、体重、饮食偏好、性格、身体状况等

用户家里有一只叫旺财的狗，喜欢吃鸡腿
