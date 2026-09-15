# 析言权限管理

本文档介绍了如何在析言GBI中进行权限管理，以控制用户对数据表、列与值的查询权限。

## 流程简介

1.  [新增权限](https://help.aliyun.com/zh/model-studio/xiyan-gbi-permission-management#42843e554bygi)：为数据表或数据表的列与值设置权限，通过权限来约束用户可查询的数据表、列和值的范围。
2.  [为角色关联权限](https://help.aliyun.com/zh/model-studio/xiyan-gbi-permission-management#a7b50faed0zk8)：您可以通过设置角色并为其关联权限，来约束使用析言的用户可访问的数据范围。
3.  [验证权限是否生效](https://help.aliyun.com/zh/model-studio/xiyan-gbi-permission-management#c3dbec64a9ky5)：析言GBI会根据角色权限验证并处理提交的问题，确保只有符合权限范围的查询才能被执行并展示查询结果。
4.  [实现权限隔离](https://help.aliyun.com/zh/model-studio/xiyan-gbi-permission-management#e4be989fbas4c)：通过[API](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-intelligent-asking-number/api-dataanalysisgbi-2024-08-23-dir-cloud-sql-execution-mode/api-dataanalysisgbi-2024-08-23-rundataanalysis.md)进行问答和数据分析时，可以为不同用户分配业务空间和角色，以实现权限隔离。请注意，控制台上不支持此功能。

## 前提条件

已在[数据表管理](https://bailian.console.aliyun.com/xiyan#/dataManagement/dataSourceM)授权联接数据库。具体操作请参见[数据库连接](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#8e5d17697392b)。

## 授权操作

### 步骤一：新增权限

析言提供了系统预置权限**全表查询权限**。该权限默认开启，用于查询全部数据表。

如果您需要对特定的数据表或数据表的列与值设置查询权限，请在[权限管理](https://bailian.console.aliyun.com/xiyan#/systemSettings/authority)页面点击**新增权限**，配置以下信息：

**参数名称**

**参数说明**

**权限名称**

自定义。建议对权限名称进行规范，以便准确识别权限的用途。

**权限使用状态**

-   开启：权限生效。
-   关闭：权限不生效。

**授权数据范围**

-   **表级别：**表示对选中的数据表设置查询权限，拥有该权限的角色方能查询该数据表的内容。
-   **列与值级别：**表示对选中的列与值设置查询权限，拥有该权限的角色方能查询该列与值的内容。

**选择数据表**

**授权数据范围**选择**表级别**时显示该参数。候选范围为在数据表管理时授权访问的表范围。

> 同一权限内可设置多张数据表，多张数据表间是“或”关系。

**选择列与值**

**授权数据范围**选择**列与值级别**时显示该参数。

点击**新增一组列与值**，先选择数据表，再选择该表内的列与值。

> 一个权限内可设置多组列与值，每组列与值仅能选择单张数据表，数据表候选范围为在数据表管理时授权访问的表范围。

析言可添加应用场景：

-   **全部值：**表示可查询该列的全部值。
-   **固定值：**表示可查询该列在已设置的固定值范围内的值。
-   **变量值：**表示该列的值为动态参数，可在每次问答时动态传入，此处仅需填写该变量的自定义变量名称。通过API使用本功能时，请确保传入的变量名称与此处填写的名称保持一致。

### 步骤二：为角色关联权限

析言提供了系统预置角色**超级管理员**角色，并为该角色关联了全表查询权限。

如果您需要自定义角色并关联权限，请在[角色管理](https://bailian.console.aliyun.com/xiyan#/systemSettings/authority)页面点击**新增角色**，配置以下信息：

**参数名称**

**参数说明**

**角色名称**

自定义。建议对角色名称进行规范，以便准确识别角色的用途。

**关联权限**

选择需要关联的权限。

> 一个角色至多可拥有20个权限。

### 步骤三：验证权限是否生效

1.  **在提问时选择合适的角色。**
    
    在析言GBI[首页](https://bailian.console.aliyun.com/xiyan#/home)的问题输入框上方选择角色，再进行提问。
    
    > 超级管理员和其他角色不能同时选择。
    
    如果选中的角色关联的权限中包含变量值类型，则需要输入相应的变量值，再提问。问题提交时，析言会核实变量值是否符合用户角色可查询的权限范围，若不符合权限范围，则会拒绝提问请求，并提示错误信息：“您当前角色为xxxx，该角色需要传入【变量名】的变量值，请完善信息后重新提交，当次问题不计入析言调用额度”。
    
    单击问题输入框上方的**角色**下拉框，弹出角色选择对话框，以复选框形式列出可选角色（如**超级管理员（选择后自动拥有所有角色）**和**客户信息权限**），勾选后单击**确定**即可应用对应权限进行提问。
    
2.  **展示SQL内容。**
    
    问题提交通过，在SQL生成之后，析言将对SQL内容和数据权限范围进行检查，展示最终的SQL内容。分为以下2种情况：
    
    -   若本次SQL生成**符合**数据权限的查询范围：则继续执行SQL查询和后续的图表展示。
        
    -   若本次SQL生成**不符合**数据权限的查询范围：则不执行SQL查询，同时提示信息“很抱歉，您没有对该问题的查询权限，table.col1、table.col2不在您的可查询范围内”。
        
        **重要**不论本次SQL生成是否符合数据权限的查询范围，都会消耗析言调用额度。
        

### 步骤四：实现权限隔离

目前仅支持通过[Chat对话接口](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-intelligent-asking-number/api-dataanalysisgbi-2024-08-23-dir-cloud-sql-execution-mode/api-dataanalysisgbi-2024-08-23-rundataanalysis.md)调用析言GBI时实现权限隔离。
