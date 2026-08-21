# 传媒/零售文章风格与格式学习

百炼轻应用传媒/零售文章风格与格式学习为您提供零代码训练新文本的能力，即其可以帮助您分析文章的文风得到对应的文体大模型，方便您后续创作自定义文体的文章。

**重要**

传媒/零售文章风格与格式学习应用限时免费，额度用完后再按实际调用模型对应的输入、输出Token以后付费方式来计费。

-   更多关于新用户限时免费福利信息，请参见[新用户限时免费福利](https://help.aliyun.com/zh/document_detail/2793370.html)。
    
-   关于Token的计算方法和模型的计费详情，请参见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。
    

## **功能入口**

访问**[应用广场](https://bailian.console.aliyun.com/#/app-market)**页面，单击**全妙-传媒/零售文章风格与格式学习**卡片区域的**查看详情**，即可进入该轻应用控制台。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0922853471/p935613.png)

## **功能介绍**

### 应用详情

在**传媒/零售文章风格与格式学习**应用的**应用详情**页签，您可以查看功能描述、最佳实践、计费规则。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7724413371/p881513.png)

### **效果调试**

在**效果调试**页签，您可以参考以下步骤设置配置项，完成后单击**创作**。

1.  **模型**：默认使用**通义千问-Max**模型，不支持修改。
    
2.  输入需要学习的文章**。**
    
    在**文章样例**文本框中输入需要学习的文章，供大模型分析。您最多可添加10篇（单击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7319034271/p838228.png)增加一篇**，在新增的**文章样例**文本框中输入需要学习的文章），总字数不超过4000字。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7724413371/p881514.png)
    
3.  测试学习效果。
    
    1.  在**写作主题**文本框中，输入写作的主题、内容或相关信息和要求，描述详细具体。
        
    2.  根据写作主题，您可以添加写作参考素材，为大模型写作指引创作方向。您最多可添加10篇（单击**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7319034271/p838228.png)增加一篇**，在新增的**参考素材**文本框中输入需要学习的文章），总字数不超过4000字。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7724413371/p881515.png)
        
    
4.  单击**创作**。
    
    大模型根据上传的素材文章，分析文章特点，分析完成后，在右侧窗口展示文章特点的分析结果和学习效果测试结果。
    
    -   如果对分析结果和学习结果满意，您可直接采用。
        
    -   如果分析结果和学习结果与预期出入很大，您可点击**重新分析特点并学习**，模型会对内容进行重新分析特点和学习。
        
    -   如果仅对学习结果感觉不符合预期，您可将文章特点分析结果复制到**已有分析结果**文本框中，单击**创作**，进行文章学习（仅执行[测试学习效果](#b7c6b34b9di07)）。
        
    
    **重要**
    
    -   文章特点分析结果和学习效果测试结果均需消耗Token。
        
    -   当单击**重新分析特点并学习**时，右侧窗口中生成的文章特点分析结果和学习效果测试结果均需消耗Token。
        
    -   当仅执行**第2步：测试学习结果**时，右侧窗口中生成的**文章特点分析结果**不消耗Token，**学习效果测试结果**消耗Token。
        
    
    下图为学习文章示例。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7724413371/p881523.png)
    

### **查看API示例**

效果调试完成后，单击**API**页签，您可以查看对应生成的API示例。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7724413371/p881519.png)
