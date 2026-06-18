# 图生播报视频-灵动人像LivePortrait

灵动人像LivePortrait可基于人物肖像图片和人声音频文件，快速、轻量地生成人物肖像动态视频。其中，包含2个独立的模型“灵动人像LivePortrait-detect”和“灵动人像LivePortrait”，分别提供人物图片合规检测与人物视频生成能力。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

### **模型概览**

#### **模型简介**

-   灵动人像LivePortrait-detect是一个图像检测模型，用于检测输入的图片是否满足LivePortrait模型所需的人物肖像图片规范。
    
-   灵动人像LivePortrait是一个人物视频生成模型，可基于人物肖像图片和人声音频文件，快速、轻量地生成人物肖像动态视频。
    

#### **模型效果示例**

**输入物：人物肖像图片+人声音频文件**

**输出物：人物肖像动态视频**

人物肖像：

![素描男孩](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8083702371/p874909.png)

人声音频：参见右侧视频

人物视频：

人物肖像：

![古风美女](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8083702371/p874905.png)

人声音频：参见右侧视频

人物视频：

人物肖像：

![Emoji男孩](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9239161571/p874897.png)

人声音频：参见右侧视频

人物视频：

**说明**

以上示例所用素材均由AI生成。

### 资费与限流

**模型名称**

**单价**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**任务下发接口QPS限制**

**同时处理中任务数量**

liveportrait-detect

模型调用，后付费：

0.004元/张

200张

5

同步接口无限制

liveportrait

模型调用，后付费：

0.02元/秒

1800秒

1

（在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态）

### 前提条件

已开通阿里云百炼服务并获得API-KEY：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### **模型调用**

-   灵动人像LivePortrait系列模型支持后付费调用。
    
-   模型调用时，参照以下顺序：
    
    1.  调用“灵动人像LivePortrait-detect”模型确认输入的人物图像符合规范（可参考文档：[LivePortrait 图像检测](https://help.aliyun.com/zh/model-studio/liveportrait-detect-api)）；
        
    2.  调用“灵动人像LivePortrait”模型，输入经检测通过的人物图像以及包含清晰人声的音频文件，生成人物肖像动态视频（可参考文档：[LivePortrait 视频生成](https://help.aliyun.com/zh/model-studio/liveportrait-api)）。
