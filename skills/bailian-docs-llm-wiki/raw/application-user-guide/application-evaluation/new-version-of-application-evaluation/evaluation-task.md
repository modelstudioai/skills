# 评测任务

评测任务是应用评测的核心功能，用于对应用的输出质量进行系统化评估。支持智能体应用和工作流应用的评测，可结合自动评估器和人工标签进行多维度评价。

> 在[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task&pageNum=1&statuses=%5B%22all%22%5D&name=)页面左上角单击**返回旧版**，可返回[旧版应用评测](https://help.aliyun.com/zh/model-studio/application-auto-evaluation)。

## **创建评测任务**

1.  访问[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task&pageNum=1&statuses=%5B%22all%22%5D&name=)页面，单击**创建评测任务**，配置以下基本信息：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7744803771/p1048186.png)
    
    **字段**
    
    **说明**
    
    任务名称
    
    自定义任务名称，最多50个字符。
    
    任务描述
    
    描述任务的目的或用途，最多200个字符。
    
    选择评测集
    
    从已发布的评测集列表中选择评测集和对应版本。
    
    选择应用
    
    选择应用关联方式，支持三种选项：
    
    -   **不关联应用**（默认）：不关联任何应用，适用于纯人工标注场景。
        
    -   **工作流**：关联工作流应用，系统将使用评测集数据调用工作流进行评测。
        
    -   **智能体**：关联智能体应用，系统将使用评测集数据调用智能体进行评测。
        
    
    评估器
    
    可添加评估器进行自动评分。选择评估器后，需要配置参数映射，将评估器的变量参数映射到实际数据源。详见[评估器](https://help.aliyun.com/zh/model-studio/grader)。
    
    **配置要求**：
    
    -   所有变量都必须完成映射后，才能保存配置
        
    -   确保映射关系正确，避免评分结果不准确
        
    
    **说明**
    
    建议为评测任务添加3-5个评估器，从不同维度评估应用质量。常见组合：
    
    -   相关性评估器（LLM）+ 格式校验评估器（Code）
        
    -   正确性评估器（LLM）+ 字符串匹配评估器（Code）
        
    -   智能体工具调用评估器（LLM）+ 参数检查评估器（Code）
        
    
    每个评测任务最多支持添加10个评估器。
    
    标签
    
    为评测任务添加标签，用于人工标注（可选）：
    
    -   点击**添加标签**按钮，从标签列表中选择需要的标签。
        
    -   标签将用于任务详情页的人工标注功能。
        
    -   创建任务后也可以在任务详情页中单击**标签配置**添加标签。
        
    
2.  确认所有配置后，点击**完成创建**按钮创建评测任务。
    

**说明**

注意：评测任务发起后将无法修改配置。

## 管理任务

评测任务创建后，可单击评测任务右侧的**详情**进入任务详情页。

在任务详情页可查看数据明细和指标统计：

-   **数据明细**：展示每条评测数据的详细结果，可进行数据标注、标签配置等操作。
    
    -   **评估器评分结果**：自动评分列，显示指定评估器对每条数据的评分（0-1之间或自定义范围）。
        
    -   **标签配置：**可为评测任务添加标签。
        
    -   **标注模式：**
        
        -   **普通模式**：页面平铺展示，字段横向排列。
            
        -   **快速标注**：点击后，自定义标签变为可编辑状态。分类标签显示为下拉选择，输入类型显示为输入框，修改后立即保存。
            
        
        两种模式下均可点击**标注**查看单条数据的完整信息，进行逐条标注。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0642430771/p1050528.png)
        

-   **指标统计：**展示综合得分和评测进度等信息。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1845933771/p1057903.png)
    

## **计费说明**

评测任务调用大模型产生的Token费用正常计费。消耗的Token量可访问[评测任务](https://bailian.console.aliyun.com/cn-beijing?tab=app#/efm/app_evaluate/tabs?pageNum=1&statuses=%5B%22all%22%5D&name=)页面查看，价格详情请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。

## 常见问题

1.  **评测任务创建后可以修改吗？**
    
    评测任务创建后，任务配置（应用、评测集）不可修改，但您可以随时添加人工标签进行标注。如需使用不同配置，请创建新的评测任务。
    
2.  **"不关联应用"选项的作用？**
    
    “不关联应用”适用于纯人工标注场景。选择此选项后，系统不会自动调用任何应用进行评测，您需要完全依靠人工标签进行数据标注和评价。
    
3.  **评估器和标签如何配合使用？**
    
    评估器用于自动评分，适合有明确规则或标准答案的评测维度。标签用于人工标注，适合需要主观判断的评测维度。在同一个评测任务中，您可以同时使用评估器进行自动评分，并添加标签进行人工补充标注，实现全面的评测覆盖。
    
4.  **如何返回旧版应用评测？**
    
    访问[应用评测](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task&pageNum=1&statuses=%5B%22all%22%5D&name=)页面，在左上角单击**返回旧版**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0642430771/p1052985.png)
