# 影视传媒视频理解计费

全妙产品矩阵包含4个SaaS产品妙笔/妙策/妙搜/妙读和若干个AI Agent（场景化能力），本文档主要介绍AI Agent中影视传媒视频理解应用的计费。

## **计费说明**

我们提供**实时**和**异步**两种模式，推荐优先使用**异步模式**离线调用：

-   **实时模式>在线调用**：
    
    -   每个阿里云主账号提供1个免费并发，暂不支持增加并发配额；
        
    -   支持处理的单个视频时长最多不超过30分钟，且单个视频大小小于200MB，分辨率不超过1080P。
        
-   **异步模式>离线调用**：
    
    -   每个阿里云主账号提供2个免费并发，且支持增加并发配额，最多支持扩展到30并发；
        
    -   支持处理的单个视频时长最多不超过1小时，且单个视频大小小于450MB，分辨率不超过1080P，队列中的任务不超过10万个视频文件。
        

**说明**

千问系列模型的[免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)不适用于影视传媒视频理解功能。

## **计费详情**

**模式**

**套餐组合**

**计费**

实时模式

大模型推理（必选）

-   Qwen-VL-Post
    
    -   输入：0.0015元/千Token
        
    -   输出：0.0045元/千Token
        
-   全妙VL-turbo
    
    -   输入：0.0008元/千Token
        
    -   输出：0.002元/千Token
        
-   全妙VL-plus
    
    -   输入：0.0016元/千Token
        
    -   输出：0.004元/千Token
        
-   全妙VL-max（思考与非思考模式）
    
    -   输入：0.004元/千Token
        
    -   输出：0.01元/千Token
        
-   全妙LLM-turbo
    
    -   输入：0.0008元/千Token
        
    -   输出：0.002元/千Token
        
-   全妙LLM-plus
    
    -   输入：0.0024元/千Token
        
    -   输出：0.0096元/千Token
        
-   全妙LLM-max（思考与非思考模式）
    
    -   输入：0.0048元/千Token
        
    -   输出：0.0192元/千Token
        

多模态信息处理（必选）

2.8元/小时（按照实际成功处理的视频总时长计费）

角色识别（可选）

0.03元/分钟视频

异步模式

大模型推理（必选）

-   Qwen-VL-Post
    
    -   输入：0.0015元/千Token
        
    -   输出：0.0045元/千Token
        
-   全妙VL-turbo
    
    -   输入：0.0008元/千Token
        
    -   输出：0.002元/千Token
        
-   全妙VL-plus
    
    -   输入：0.0016元/千Token
        
    -   输出：0.004元/千Token
        
-   全妙VL-max（思考与非思考模式）
    
    -   输入：0.004元/千Token
        
    -   输出：0.01元/千Token
        
-   全妙LLM-turbo
    
    -   输入：0.0008元/千Token
        
    -   输出：0.002元/千Token
        
-   全妙LLM-plus
    
    -   输入：0.0024元/千Token
        
    -   输出：0.0096元/千Token
        
-   全妙LLM-max（思考与非思考模式）
    
    -   输入：0.0048元/千Token
        
    -   输出：0.0192元/千Token
        

多模态信息处理（必选）

2.8元/小时（按照实际成功处理的视频总时长计费）

角色识别（可选）

0.03元/分钟视频

（按照实际成功处理的视频总时长计费）

增加并发配额（可选）

1元/小时\*并发数

（例如用10并发处理共30小时视频，那就是1\*30\*10=300元）

-   上传任务优先使用免费并发，如果免费并发已全部占用，则使用付费并发，并按照当前任务实际处理时长计费。
    
-   可以通过GetVideoAnalysisConfig、UpdateVideoAnalysisConfig这两个接口查看和扩缩并发
    

## **开通与账单地址**

开通地址：[视频理解开通地址](https://common-buy.aliyun.com/?commodityCode=sfm_videoanalysis_public_cn)；

账单查询地址：[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail?spm=a2c4g.11186623.0.0.619355efACwmfT)。

## **节省计划**

节省计划是一种针对影视传媒视频理解API产品的折扣权益计划，可抵扣全妙-影视传媒视频理解API的所有按量付费项，包括多模态信息处理、角色识别、增加并发配额。(大模型推理无折扣)

您只需要承诺在一定期限内消费一定金额，即可享受影视传媒视频理解节省计划带来的优惠。对比按量付费，可降低5%到50%的费用。

详情可查看阿里云[节省计划](https://help.aliyun.com/zh/user-center/savings-plan-overview/)

### **购买方式**

[点击此处](https://common-buy.aliyun.com/?commodityCode=sfm_videoanalysis_spn_cn)购买通用型节省计划。您只需填写承诺消费金额并付款，即可完成购买并立即生效。

-   付款类型：全预付，购买时一次性付清所有费用。
    
-   购买时长：1年，1年期满后，未使用的费用将不会返还。
    
-   开通时间：下单后立即生效
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5451358571/p1007256.png)

### **折扣力度**

节省计划生效后，以折扣后单价抵扣按量付费账单，消费金额越高，折扣力度越大。

节省计划折扣力度如下表：

**承诺消费金额**

**多模态信息处理**

**角色识别**

**扩并发**

10000

0.7

0.85

0.95

20000

0.65

0.8

0.9

50000

0.6

0.75

0.8

100000

0.5

0.7

0.7

200000

0.4

0.6

0.65

## **产品地址**

可点击[产品地址](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)进行产品体验。

## **产品相关文档**

-   技术文档
    
    可点击[影视传媒视频理解接口文档](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-dir-film-and-television-media-video-understanding/)进行查看；
    
-   视频理解与内容提取的解决方案
    
    可点击[解决方案地址](https://www.aliyun.com/solution/tech-solution-deploy/2860032)进行查看体验。
    

## **常见问题**

#### **1\. 离线调用怎么增加并发配额？**

可以通过[GetVideoAnalysisConfig - 视频理解-获取配置](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideoanalysisconfig)、[UpdateVideoAnalysisConfig - 视频理解-更新配置](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideoanalysisconfig)接口查看和扩缩并发。

#### **2\. 一并发收费是1元/小时，这个时间是怎么定义的？**

收费的时间计算范围是从客户提交任务的时间点开始算到任务执行结束为止。

#### **3\. 任务运行到中途失败了，怎么计费？**

当任务运行到中途失败时，主要是看最后一个事件消息的event，如果是task-failed，就不计费；其他运行成功部分计费，失败部分不计费。在产品客户端页面立即中断并展示状态。

#### **4.新增的预付费模式对现有业务及现有付费模式有影响吗？**

节省计划对现有付费模式无影响。

#### **5.购买影视传媒视频理解API节省计划后能退订吗？**

支持退订。

#### **6.上传格式为**SRT（SubRip 字幕）**的ASR数据时解析错误怎么办？**

请将文件转为标准的utf-8格式编码。
