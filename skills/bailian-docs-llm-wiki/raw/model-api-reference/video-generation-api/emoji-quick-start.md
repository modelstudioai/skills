# 图生表情包视频-表情包Emoji

表情包视频生成（Emoji）模型基于一张**人物肖像或半身头像**，结合**预设动态模板**，生成具有丰富表情的视频。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **模型效果**

**输入：人物肖像图片**

**输出：人物肖像动态视频**

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8567357371/p906296.png)

“嫌弃”表情的模板ID（driven\_id）：jingdian\_xianqi

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5821216571/p906298.png)

“开心”表情的模板ID（driven\_id）：mengwa\_kaixin

## **视频生成流程**

表情包视频生成主要由两个API协同工作：先检查人像图片是否合规，再生成表情包动态视频。

-   **步骤一：图像检测** 
    
    调用[Emoji 图像检测API](https://help.aliyun.com/zh/model-studio/emoji-detect-api)，确保人像图片合规，并获取人脸区域和表情包动态区域的坐标。
    
-   **步骤二：视频生成**
    
    调用[Emoji 视频生成API](https://help.aliyun.com/zh/model-studio/emoji-api)，传入通过检测的人像图片、上一步获取的坐标、在[表情包模板ID列表](https://help.aliyun.com/zh/model-studio/emoji-api#552aacbdadtaq)选择的模板ID，生成表情包视频。
    

## **计费与限流**

-   模型免费额度和计费单价请参见[模型列表与价格](https://help.aliyun.com/zh/model-studio/models#f62472e1b6m3b)。
    
-   模型限流请参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
