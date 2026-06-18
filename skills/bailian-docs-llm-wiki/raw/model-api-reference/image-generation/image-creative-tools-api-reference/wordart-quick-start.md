# 创意文字WordArt锦书

WordArt锦书，围绕文字、特别是汉字的使用场景，通过简单的提示词描述即可实现创意字形、艺术纹理和个性字体的智能打造，批量生成丰富有趣的特效艺术字内容，在文字的辨识度、创意感、艺术性上均能实现精准可控和艺术加工，在文档、海报、配图等场景均可以方便快捷的使用。

如果你希望方便快捷地测试和体验功能效果，可以到魔搭社区-[WordArt锦书空间进行试用](https://www.modelscope.cn/studios/WordArt/WordArt/summary)。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **模型调用**

1.  WordArt锦书-文字变形：[文字变形API详情](https://help.aliyun.com/zh/model-studio/word-transformer)
    
2.  WordArt锦书-文字纹理生成：[文字纹理生成API详情](https://help.aliyun.com/zh/model-studio/fill-texture-effect-api)
    

## **功能介绍**

### **文字变形**

WordArt锦书-文字变形可以对输入的文字边缘轮廓进行创意变形，根据提示词内容进行边缘变化，实现一种字体的更多种创意用法，返回带有文字内容的黑底白色蒙版图。

输入文字：桂林山水

描述提示词：山峦叠嶂、漓江蜿蜒、岩石奇秀

返回结果：

![20231117173455.jpg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2179320071/p739205.jpg)

### **文字纹理生成**

WordArt锦书-文字纹理生成可以对输入的文字内容或文字图片进行创意设计，根据提示词内容对文字添加材质和纹理，实现立体材质、场景融合、光影特效等效果，生成效果精美、风格多样的艺术字，结合背景可以直接作为文字海报使用。

目前支持“自定义”和“预设风格”两大类，“自定义”大类提供3种风格，用户可基于提供的风格通过提示词进行纹理效果自定义，支持输入提示词和字体类型 ；“预设风格”大类提供18种风格，此类别为预设的风格效果，不支持用户自定义输入提示词和字体类型。每一种风格具体的示例图如下：

-   “自定义”大类：
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792572.png)

-   “预设风格”大类：
    

瀑布流水（waterfall）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792579.png)

雪域高原（snow\_plateau）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792591.png)

原始森林（forest）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792578.png)

天空遨游（sky）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792586.png)

国风建筑（chinese\_building）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792581.png)

奇幻卡通（cartoon）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792585.png)

乐高积木（lego）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792574.png)

繁花盛开（flower）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792587.png)

亚克力（acrylic）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792589.png)

大理石（marble）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792575.png)

绒线毛毡（felt）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792588.png)

复古油画（oil\_painting）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792576.png)

水彩（watercolor\_painting）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792582.png)

中国画（chinese\_painting）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792590.png)

工笔画（claborate\_style\_painting）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792584.png)

城市夜景（city\_night）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792577.png)

湖光山色（mountain\_lake）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792583.png)

秋日落叶（autumn\_leaves）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7951143171/p792580.png)

## 示例代码

### **前提条件**

-   已开通服务并获得API-KEY：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    

**说明**

以下代码演示了如何使用文字纹理生成API。需要使用您的API-KEY替换示例中的 _your-bailian-api-key_ ，代码才能正常运行。

### **依赖及代码**

Shell

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/wordart/texture' \
--header 'X-DashScope-Async: enable' \
--header 'Authorization: Bearer <YOUR-DASHSCOPE-API-KEY>' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'X-DashScope-DataInspection: enable' \
--data '{
    "model": "wordart-texture",
    "input": {
        "text": 
        {
            "text_content": "文字创意",
            "font_name": "dongfangdakai",
            "output_image_ratio": "1:1"
        },
        "prompt": "水果，蔬菜，温暖的色彩空间",
        "texture_style": "material"
    },
    "parameters": 
    {
        "image_short_size": 704,
        "n": 2,
        "alpha_channel": false
    }
}'
```

## **常见问题**

### **调用模型生成的创意文字WordArt锦书文字可以免费商用吗？**

通常情况下，若您对您上传的内容拥有合法知识产权，则合成内容的知识产权仍归属于您。更多相关信息，请参见[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)。

## **API参考**

有关WordArt锦书API的详细调用请参见[文字纹理生成API详情](https://help.aliyun.com/zh/model-studio/fill-texture-effect-api)、[文字变形API详情](https://help.aliyun.com/zh/model-studio/word-transformer)。
