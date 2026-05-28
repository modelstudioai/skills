# 图生舞蹈视频-舞动人像AnimateAnyone

舞动人像AnimateAnyone可基于人物图片和人物动作模板，生成人物动作视频。其中，包含3个独立的模型“舞动人像AnimateAnyone-detect”、“舞动人像AnimateAnyone-template”和“舞动人像AnimateAnyone”，分别提供人物图片合规检测、人物动作模板生成与人物视频生成能力。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

### **模型概览**

#### **模型简介**

-   舞动人像AnimateAnyone-detect，是一个图像检测模型，用于检测输入的图片是否满足AnimateAnyone模型所需的人物图片规范。
    
-   舞动人像AnimateAnyone-template，是一个动作模板生成模型，用于从人物运动视频中提取人物动作并生成满足AnimateAnyone模型所需的动作模板。
    
-   舞动人像AnimateAnyone，是一个人物视频生成模型，可基于人物图片和动作模板生成人物动作视频。
    

#### **模型效果示例**

**输入：人物图片**

**输入：动作视频**

**输出（按图片背景生成）**

**输出（按视频背景生成）**

![05-9\_16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5770383371/p885845.png)

![04-9\_16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9239161571/p885846.png)

**说明**

-   以上示例，由集成了“舞动人像AnimateAnyone”的千问APP生成。
    
-   舞动人像AnimateAnyone模型的生成内容为视频画面，不包含音频。
    

### **资费与限流**

**模式**

**模型名称**

**单价**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**任务下发接口QPS限制**

**同时处理中任务数量**

模型调用

animate-anyone-detect-gen2

模型调用，后付费：

0.004元/张

200张

5

同步接口无限制

animate-anyone-template-gen2

模型调用，后付费：

0.08元/秒

1800秒

1

（在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态）

animate-anyone-gen2

模型调用，后付费：

0.08元/秒

1800秒

模型部署

animate-anyone-detect

模型独立部署，预付费：

-   10000元/算力单元/月
    
-   20元/算力单元/小时
    

需部署成功后调用，仅收取部署费用。

无

5

1算力单元支持2并发

animate-anyone

1算力单元支持1并发

### 前提条件

已开通服务并获得API-KEY：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### 模型调用

-   舞动人像AnimateAnyone系列模型支持后付费调用。
    
-   调用时，需按模型名称调用对应模型，并请参照以下调用顺序：
    
    a. 调用“舞动人像AnimateAnyone-detect”模型确认输入的人物图像符合规范（可参考文档：[AnimateAnyone 图像检测](https://help.aliyun.com/zh/model-studio/animate-anyone-detect-api)）；
    
    b. 调用“舞动人像AnimateAnyone-template”模型输入人物运动视频以生成人物动作模板（可参考文档：[AnimateAnyone 动作模板生成](https://help.aliyun.com/zh/model-studio/animate-anyone-template-api)）。
    
    c. 调用“舞动人像AnimateAnyone”模型输入通过检测的人物图像和人物动作模板ID以生成视频（可参考文档：[AnimateAnyone 视频生成](https://help.aliyun.com/zh/model-studio/animateanyone-video-generation-api)）。
    

### 模型部署与调用

-   舞动人像AnimateAnyone系列模型还支持模型独立部署。
    
-   模型部署时，需要在[模型部署](https://bailian.console.aliyun.com/home#/efm/model_deploy)页面购买独占实例资源并分别部署**“舞动人像AnimateAnyone-detect-deployment”**模型和**“舞动人像AnimateAnyone-deployment”**模型。
    
-   模型部署成功后，可查看到**部署成功的模型名称**显示在已部署模型列表的 **Model** 列中。
    
-   模型调用时，需在入参的“model”字段中填入**部署成功的模型名称**，并参照以下调用顺序：
    
    a. 调用“舞动人像AnimateAnyone-detect”模型确认输入的人物图像符合规范（可参考文档：[AnimateAnyone 图像检测](https://help.aliyun.com/zh/model-studio/animate-anyone-detect-api)）；
    
    b. 调用“舞动人像AnimateAnyone”模型输入通过检测的人物图像和预设动作模板文件以生成视频（可参考文档：[AnimateAnyone 视频生成](https://help.aliyun.com/zh/model-studio/animateanyone-video-generation-api)）。
    

**说明**

-   animate-anyone-detect、animate-anyone仅为模型能力代称，独立部署的模型将在部署成功后生成唯一的模型名称，如“animate-anyone-detect-xxx”，模型调用时需指明调用的是该独立部署模型。
    
-   由于图像检测的调用耗时较短，而视频生成算法的调用耗时较长。使用时，可结合实际需要调整图像检测模型与视频生成模型的部署比例。通常，当图像以有序的队列输入时，1路图像检测并发应可支撑5路视频生成并发任务。
