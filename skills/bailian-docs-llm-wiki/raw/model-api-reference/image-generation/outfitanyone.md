# AI试衣OutfitAnyone

AI试衣包含**试衣模型**和**辅助模型**。通过灵活组合，可以满足从快速出图到精修细节、再到局部替换等多样化的业务需求。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

**快速入口：**[在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/vision?currentTab=imageGenerate) **｜** [计费与限流](https://help.aliyun.com/zh/model-studio/billing-for-outfitanyone) **｜** [免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)

**相关API：**![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-基础版](https://help.aliyun.com/zh/model-studio/outfitanyone-api)**｜**![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-Plus版](https://help.aliyun.com/zh/model-studio/aitryon-plus-api)**｜**![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-图片精修](https://help.aliyun.com/zh/model-studio/ai-fitting-picture-finishing-api-details)**｜**![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-图片分割](https://help.aliyun.com/zh/model-studio/aitryon-parsing-api)

## **模型概览**

**模型分类**

**模型服务**

**模型名称**

**核心功能**

**适用场景**

**试衣模型**

[AI试衣-基础版](https://help.aliyun.com/zh/model-studio/outfitanyone-api)

aitryon

快速生成试衣效果图。

对生成速度要求高，质感要求一般的场景。

[AI试衣-Plus版](https://help.aliyun.com/zh/model-studio/aitryon-plus-api)

（推荐）

aitryon-plus 

提升图片清晰度、服饰纹理细节和logo还原效果。

生成耗时较长，适用于对时效性要求不高的场景。

**辅助模型**

[AI试衣-图片精修](https://help.aliyun.com/zh/model-studio/ai-fitting-picture-finishing-api-details)

aitryon-refiner

提升试衣图的质感、清晰度和真实感。

在试衣模型的基础上，进一步追求高质量的图片效果。

[AI试衣-图片分割](https://help.aliyun.com/zh/model-studio/aitryon-parsing-api)

aitryon-parsing-v1

分割图片中的服饰区域。

用于实现局部试衣，或获取服装坐标用于商品热区交互等。

## **使用场景**

您可以根据业务需求组合调用这些 API， 以下是常见场景的调用流程：

### **场景一：基础试衣**

**适用场景：** 快速验证效果，或对出图速度要求高的业务。

**调用步骤**：

1.  准备输入：准备模特图片和服装图片。
    
2.  调用试衣模型：调用[AI试衣-基础版](https://help.aliyun.com/zh/model-studio/outfitanyone-api) 或[AI试衣-Plus版](https://help.aliyun.com/zh/model-studio/aitryon-plus-api)，将上述两张图片作为核心参数传入。
    
3.  获取结果：API 将直接返回试衣效果图。
    

### **场景二：精修**试衣

**适用场景：**对最终图片质量、细节和真实感有要求的场景。

**调用步骤**：

1.  调用试衣模型：按照[场景一：基础试衣](#fced826e3fojt)的步骤，调用试衣模型，获得一张试衣效果图。
    
2.  调用图片精修模型：调用[AI试衣-图片精修](https://help.aliyun.com/zh/model-studio/ai-fitting-picture-finishing-api-details)，将上一步生成的基础试衣效果图和原始的输入图（模特图和服装图）作为参数传入。
    
3.  获取结果：API 将返回精修后的试衣效果图。
    

### 场景三：局部试衣

**适用场景：**替换部分服饰，例如：保留模特原有的裤子，只替换上衣。

**调用步骤：**

1.  提取保留服饰：调用[AI试衣-图片分割](https://help.aliyun.com/zh/model-studio/aitryon-parsing-api)，输入原始模特图，获取要保留的服饰图片（例如裤子）。
    
2.  组合试衣：调用[AI试衣-基础版](https://help.aliyun.com/zh/model-studio/outfitanyone-api) 或[AI试衣-Plus版](https://help.aliyun.com/zh/model-studio/aitryon-plus-api)，同时传入原始模特图、新的上衣图和上一步得到的裤子图。
    
3.  获取结果：API 将返回一张组合了新上衣和原始裤子的试衣效果图。
    

### 场景四：获取服饰坐标

**适用场景：** 在生成的图片上添加商品标签，或实现商品热区交互功能。

**调用步骤：**

1.  调用图片分割模型：调用[AI试衣-图片分割](https://help.aliyun.com/zh/model-studio/aitryon-parsing-api)，输入任意模特图（真实照片或AI试衣图均可）。
    
2.  获取结果：API会返回服饰区域的坐标（bbox）和可视化效果。您可以利用此坐标实现前端交互功能（如商品热区）。
