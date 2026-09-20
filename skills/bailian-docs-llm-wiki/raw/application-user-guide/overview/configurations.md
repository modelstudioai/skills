# 配置

使用真实样本验证 Parse 或 Extract 设置，将其保存为可复用的配置。

配置用于保存可以重复使用的解析或抽取设置。例如，你可以为产品手册保存一套解析设置，为采购订单保存一套抽取字段，后续处理同类文件时继续使用。

## 前提与入口

先登录 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)。首次保存前，在解析或抽取工作台准备需要复用的设置；查看和编辑已有配置前，应已创建对应配置。

首次保存从工作台的「保存配置」进入；日常管理从左侧「配置」进入。首次体验可先阅读[快速开始](raw/application-user-guide/overview/quickstart.md)。

![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9dcf.jpg)

_通过类型筛选和配置 ID 查找配置，点击卡片查看可用操作。_

## 操作步骤

### 首次保存配置

1.  在文档解析或字段抽取工作台中，准备要重复使用的设置。
2.  点击「保存配置」。
3.  在配置创建弹窗中填写「配置名称」，最多 200 个字符。名称为空时，「创建配置」按钮不可用。
4.  点击「创建配置」，并查看页面反馈；暂时不创建时点击「取消」。
5.  从左侧进入「配置」，找到刚保存的配置，核对名称、类型和设置。

![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f9db6.png)

_在配置创建弹窗中填写名称，再点击「创建配置」。_

### 查找、编辑和测试

**操作**

**步骤**

**完成后检查**

查找

选择「全部」「文档解析」或「字段抽取」；有配置 ID 时输入搜索框

名称、类型和 ID 与目标配置一致

编辑

点击「编辑」，调整名称或选项，点击「保存配置」

重新打开配置，核对保存后的设置

测试

点击「测试」，使用有代表性的文件检查处理效果

结果符合后续应用的使用要求

引用

复制配置 ID，在应用的任务请求中指定该配置

引用的能力与配置类型一致

![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9dc1.png)

_在编辑侧栏中修改配置名称与设置。_

设置的含义分别见[配置文档解析](raw/application-user-guide/overview/overview/configuration.md)和[配置信息抽取](raw/application-user-guide/overview/overview/configuration.md)。在应用中引用配置的方法见[REST API 接入](raw/application-user-guide/overview/overview/rest-api.md)。

## 使用配置

创建成功后，配置列表中可以找到对应名称和 ID；编辑保存后，重新打开可核对当前设置。配置可用于后续复用，历史任务仍以当次快照为准。

## 当前配置与历史任务的关系

![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f9ddb.png)

_编辑配置用于后续任务，历史任务保留各自运行时的设置。_

历史任务使用的设置可在任务详情的「配置快照」中查看，操作方法见[任务记录](raw/application-user-guide/overview/configurations/tasks.md)
