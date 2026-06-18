# 图生唱演视频-悦动人像EMO

悦动人像EMO可基于人物肖像图片和人声音频文件，生成高质量的人物肖像动态视频。其中，包含2个独立的模型“悦动人像EMO-detect”和“悦动人像EMO”，分别提供人物图片合规检测与人物视频生成能力。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

### **模型概览**

#### **模型简介**

-   悦动人像EMO-detect，是一个特定的图像检测模型，用于检测输入的图片是否满足emo模型所需的人物肖像图片规范。
    
-   悦动人像EMO，是一个人物视频生成模型，可基于人物肖像图片和人声音频文件生成人物肖像动态视频。
    

#### **模型效果示例**

**输入物：人物肖像图片+人声音频文件**

**输出物：人物肖像动态视频**

人物肖像：

![上春山](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9239161571/p872312.png)

人声音频：参见右侧视频

人物视频：

使用动作风格强度：活泼（"style\_level": "active"）

人物肖像：

![15\_原图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5438661371/p872922.png)

人声音频：参见右侧视频

人物视频：

使用动作风格强度：适中（"style\_level": "normal"）

人物肖像：

![娃哈哈](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5438661371/p872311.png)

人声音频：参见右侧视频

人物视频：

使用动作风格强度：平静（"style\_level": "calm"）

**说明**

以上示例，由集成了“悦动人像EMO”的千问APP生成。

### **资费与限流**

**模式**

**模型名称**

**单价**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**任务下发接口QPS限制**

**同时处理中任务数量**

模型调用

emo-detect-v1

模型调用，后付费：

0.004元/张

200张

5

同步接口无限制

emo-v1

模型调用，后付费：

-   生成1:1画幅视频：0.08元/秒
    
-   生成3:4画幅视频：0.16元/秒
    

1800秒

1

（在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态）

模型部署

emo-detect

模型独立部署，预付费：

-   10000元/算力单元/月
    
-   20元/算力单元/小时
    

需部署成功后调用，仅收取部署费用。

无

5

1算力单元支持5并发

emo

1算力单元支持1并发

### 前提条件

已开通服务并获得API-KEY：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### **模型调用**

-   悦动人像EMO系列模型支持后付费调用。
    
-   模型调用时，参照以下顺序：
    
    1.  调用“悦动人像EMO-detect”模型确认输入的人物图像符合规范（可参考文档：[EMO 图像检测](https://help.aliyun.com/zh/model-studio/emo-detect-api)）；
        
    2.  调用“悦动人像EMO”模型，输入人物图像原图、经检测通过后获得的相关图像区域参数、以及包含清晰人声的音频文件，生成人物肖像动态视频（可参考文档：[EMO 视频生成](https://help.aliyun.com/zh/model-studio/emo-api)）。
        

### **模型部署与调用**

-   悦动人像EMO系列模型还支持模型独立部署。
    
-   模型部署时，需要在[模型部署](https://bailian.console.aliyun.com/home#/efm/model_deploy)页面购买独占实例资源并分别部署**“悦动人像EMO-detect-deployment”**模型和**“悦动人像EMO-deployment”**模型。
    
-   模型部署成功后，可查看到**部署成功的模型名称**（如下图所示）。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4406435171/p798911.png)
    
-   模型调用时，需在入参的“model”字段中填入**部署成功的模型名称**，并参照以下调用顺序：
    
    1.  调用“悦动人像EMO-detect-deployment”模型确认输入的人物图像符合规范（可参考文档：[EMO 图像检测](https://help.aliyun.com/zh/model-studio/emo-detect-api)）；
        
    2.  调用“悦动人像EMO-deployment”模型，输入人物图像原图、经检测通过后获得的相关图像区域参数、以及包含清晰人声的音频文件，生成人物肖像动态视频（可参考文档：[EMO 视频生成](https://help.aliyun.com/zh/model-studio/emo-api)）。
        

**说明**

-   emo-detect、emo仅为模型能力代称，独立部署的模型将在部署成功后生成唯一的模型名称，如“emo-detect-xxx”，模型调用时需指明调用的是该独立部署模型。
    
-   由于图像检测的调用耗时较短，而视频生成算法的调用耗时较长。使用时，可结合实际需要调整图像检测模型与视频生成模型的部署比例。通常，当图像以有序的队列输入时，1路图像检测并发应可支撑10路以上的视频生成并发任务。
