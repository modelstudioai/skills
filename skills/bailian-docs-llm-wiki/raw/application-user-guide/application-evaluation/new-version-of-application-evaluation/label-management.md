# 标签管理

标签是用于应用评测和应用观测的核心组件，支持对评测数据和应用观测数据进行自定义标注。通过创建不同类型的标签，您可以构建适合业务场景的评测维度体系，对应用的输出效果进行多维度分析和评估。

> 在[标签管理](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=annotation&pageNum=1&valueType=all&name=)页面左上角单击**返回旧版**，可返回[旧版应用评测](https://help.aliyun.com/zh/model-studio/application-auto-evaluation)。

## 创建标签

访问[标签管理](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=annotation&pageNum=1&valueType=all&name=)页面，点击**创建标签**，进入标签创建页面，配置以下信息：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1050583.png)

**配置项**

**说明**

标签名称

必填，1-50字。用于标识和区分不同的标签，建议使用清晰易懂的名称。

描述

非必填，0-200字。描述标签的用途、评判标准或使用说明。

类型

选择标签类型，支持分类、布尔值、数字、文本四种类型。详见下文"标签类型"。

### **标签类型**

系统支持以下四种标签类型，适用于不同的标注场景：

#### **分类标签**

分类标签用于从预定义的选项中选择一个或多个值，适用于枚举类型的评测维度。

**配置项**

**说明**

筛选项

支持自定义筛选选项，最多可添加20个选项。

标注方式

标注时以下拉多选的方式进行选择，可选择一个或多个选项。

筛选条件

支持的筛选条件：属于、不属于。

**适用场景示例**：回答质量（较差/一般/较好）、错误类型（事实错误/逻辑错误/格式错误）、情感倾向（正面/中性/负面）。

#### **布尔值标签**

布尔值标签用于是/否类型的判断，适用于二元评测维度。

**配置项**

**说明**

选项

固定为两个选项，True和False。

标注方式

标注时以二选一的方式进行选择。

筛选条件

支持的筛选条件：属于、不属于。

**适用场景示例**：是否正确、是否存在幻觉、是否符合规范、是否完整。

#### **数字标签**

数字标签用于数值评分，适用于需要精确打分的评测维度。

**配置项**

**说明**

数据类型

支持Double类型数值输入，可以输入整数或小数。

标注方式

标注时通过数字输入框填写具体数值。

筛选条件

支持的筛选条件：等于、不等于、大于、大于等于、小于、小于等于。

**适用场景示例**：评分（1-5分）、相关性得分（0-1）、完整度百分比（0-100）。

#### **文本标签**

文本标签用于自由文本输入，适用于需要详细描述或备注的评测维度。

**配置项**

**说明**

数据类型

支持String类型文本输入，可以输入任意文本内容。

标注方式

标注时通过文本输入框填写具体内容。

筛选条件

支持的筛选条件：包含、不包含。

**适用场景示例**：错误原因说明、改进建议、标注备注、具体问题描述。

## 管理标签

访问[标签管理](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=annotation&pageNum=1&valueType=all&name=)页面，您可以查看和管理所有已创建的标签。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1050580.png)

点击**编辑**进入页面，可以修改标签配置。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1050581.png)

## 在评测任务中使用标签

### **数据明细**

访问[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task&pageNum=1&statuses=%5B%22all%22%5D&name=)页面，点击指定任务右侧的**详情**，您可以通过标签对评测数据进行标注和筛选。

#### **添加标签**

1.  在评测任务的详情页，点击**标签配置**。
    
2.  在弹出的侧边栏中，通过下拉列表选择当前业务空间下的标签。
    
3.  已添加的标签会显示在评测任务列表中，包括标签名、标签类型，以及标注状态。
    

#### **标注模式**

评测任务支持两种标注模式：

**模式**

**说明**

**普通模式**

页面为平铺展示，字段横向排列。点击操作列的**标注**可查看单条数据的完整信息，逐条进行标注。

**快速标注**

自定义标签为可编辑状态。分类标签和布尔值标签显示为下拉选择，数字和文本标签显示为输入框。选择或输入数据后会立即保存。

#### **标注视图**

点击操作列的**标注**，可查看单条数据的完整信息：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1051695.png)

-   **标题**：显示"标注#ID"，支持上一条/下一条切换，方便连续标注。
    
-   **评测集数据**：按行平铺展示评测集的字段名和内容，包括输入、输出等字段。
    
-   **应用输出**：应用的思维链内容（如有）和输出数据。
    
-   **人工标注**：展示所有已添加的标签，选择或修改数据后立即保存。
    

#### **数据筛选**

-   **根据筛选类型进行关键词搜索**：支持搜索评测集内容、应用输出、状态、评测结果类型对应的字段的值，进行模糊匹配。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1051702.png)
    
-   **根据标签进行数据筛选**：点击**过滤器****添加筛选条件**后，然后点击**应用**即可筛选指定内容。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1051697.png)
    

### **指标统计**

在[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task&pageNum=1&statuses=%5B%22all%22%5D&name=)页面点击指定任务右侧的**详情**，然后选择**指标统计**页面，可以查看基于标签的统计分析结果：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1051676.png)

## 在应用观测中使用标签

在应用观测模块中，您可以对每个Span数据进行标签标注，实现对线上真实数据的质量评估。详情请参考[应用评测-数据标注](https://help.aliyun.com/zh/model-studio/application-observation#h2-data-label)。

### 添加标注

1.  在指定应用右侧点击**查看详情**，点击**数据标注**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1051663.png)
    
2.  在弹出的侧边栏中，选择要添加的标签。点击**新建标签**可跳转到标签管理页面创建新标签。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1051671.png)
    
3.  标注内容会立即自动保存，无需手动提交。标注完成后，可在Span列表数据的**标签**列查看。
    

### 基于标签筛选

在应用观测页面的过滤器中，用户手动添加过的标签会自动出现在筛选项中。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1442430771/p1051666.png)
