# 析言GBI反向网络访问VPC打通

## 简介

本文针对用户使用阿里云VPC内数据库时如何使用析言GBI产品进行操作指导。析言通过反向网络访问技术与用户VPC环境打通，通过私网访问用户VPC数据库，进而为用户提供析言产品服务。

析言采用**PrivateLink**网络方案，解决用户数据库不能通过公网被析言生产环境访问的问题。析言VPC所属地域为cn-beijing。

网络联通示意图如下：

-   **用户VPC与析言VPC在相同地域（均为cn-beijing）。** ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7702891271/p825734.png)
-   **用户VPC与析言VPC在不同地域时，需跨地域连接（用户数据库VPC所属地域不为beijing）。** ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7702891271/p825735.png)

关于**PrivateLink**的介绍和基本使用，请参见[跨账号共享用户自建服务NLB](https://help.aliyun.com/zh/privatelink/share-your-service/)文档。

关于**对等连接**的介绍和基本使用，请参见[VPC对等连接](https://help.aliyun.com/zh/vpc/vpc-peer-to-peer-connection)文档。

## 操作流程

### 用户准备工作

-   析言生产环境部署在cn-beijing地域，若用户的数据库同在cn-beijing，VPC间联通方案较便捷；若用户的数据库在其他地域（比如cn-shanghai），则需要在cn-beijing新建一份VPC，而后使用CEN或者[对等连接](https://help.aliyun.com/zh/vpc/vpc-peer-to-peer-connection)等方式将cn-beijing和cn-shanghai的两个VPC进行打通，最后再与析言cn-beijing的VPC进行打通。
-   用户需登录阿里云控制台，并具有PrivateLink相关权限。
-   用户需提供阿里云主账号ID，用于后续进行网络白名单登记。
-   用户可以访问主账号下待关联的数据库，并且创建好只读账号，并对该账号的权限进行设置，后续要使用该账号在析言控制台进行数据授权配置。
-   用户可以查询到主账号下待关联的数据库的内网域名和内网IP，后续需要提供给析言，进行NAT规则的配置。

### 配置步骤

#### 步骤一：提供用户信息，由析言添加服务白名单

您可以在[阿里云官网](https://www.aliyun.com/)右上角点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2458891271/p826032.png)图标（下图位置①），选择**售后在线**（下图位置②），通过工单将以下信息反馈给析言的技术支持人员申请添加服务白名单。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6979331471/p924093.png)

工单中需要提供的信息包括：

-   **问题描述：**反向网络访问VPC打通，申请添加析言GBI白名单
-   **主账号ID**：在[阿里云官网](https://www.aliyun.com/)右上角点击头像（上图位置③）获取**账号ID**。例如，196xxx。
-   **可用区**：例如，可用区B。
-   **数据库实例内网地址**：例如，rm-xxxx.mysql.rds.aliyuncs.com。
-   **数据库实例内网IP**：例如，172.x.x.x。

#### 步骤二：创建终端节点

用户需在其cn-beijing的VPC内创建[终端节点](https://vpc.console.aliyun.com/endpoint/cn-beijing/reverseEndpoints)。终端节点可以与终端节点服务相关联，以建立通过VPC私网访问外部服务的网络连接。

**注意**：用户创建终端节点时，节点类型需选择**反向**类型，点击“选择可用服务”，下方列表区域将会出现析言终端节点服务（析言真实ID为：epsrv-2zeczobsytmn6nv9actr），并选择。

由于析言生产环境的网络资源在H区，所以这里相应的也要选择H区；后续析言可能会增加其他可用区来加强服务可用性，所以建议用户预留其他网段。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5523247371/p907692.png)

终端节点创建完毕后，用户可在终端节点详情页查看生成的终端节点域名、终端节点可用区的域名和IP，且连接状态为已连接。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5523247371/p907554.png)

#### 步骤三：用户提供待关联数据库的内网域名和IP，由析言配置NAT规则

用户登录数据库控制台，查看内网地址，以RDS举例：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7702891271/p825742.png)

在同VPC内的ECS上，查询数据库对应的IP，可以通过ping命令：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5523247371/p907562.png)

#### 步骤四：开放白名单

-   终端节点开放白名单
    
    终端节点的安全组，可以管控VPC到终端节点网卡的数据通信，本场景中，需要开放**入方向**的**任意端口**。具体操作可以参考[加入和管理安全组](https://help.aliyun.com/zh/privatelink/create-and-manage-endpoints/)。
    
-   数据库开放白名单
    
    本场景中，需要在数据库侧对**终端节点**开放访问权限。不同类型的数据库，有不同的白名单功能，以下以常见的RDS和Hologress等来举例。
    
    -   RDS开放白名单的操作请参见[设置白名单](https://help.aliyun.com/zh/rds/apsaradb-rds-for-sql-server/configure-an-ip-address-whitelist-for-an-apsaradb-rds-for-sql-server-instance)。
    -   Hologres开放白名单的操作请参见[IP白名单](https://help.aliyun.com/zh/hologres/security-and-compliance/configure-an-ip-address-whitelist)、[析言GBI](https://help.aliyun.com/zh/hologres/user-guide/xiyan-gbi)。
    -   AnalyticDB PostgreSQL 版开放白名单的操作请参见[设置白名单](https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/user-guide/configure-an-ip-address-whitelist-user-guide)。

#### 步骤五：在析言控制台配置数据源

登录析言控制台，填入用户VPC内的内网域名等数据库信息。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7702891271/p825755.png) ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7702891271/p825745.png)

## 附录

### 跨VPC互联

本方案中，主要是指同账号跨地域的VPC对等连接，是析言推荐用户的同一账号在不同VPC间进行打通的方式，客户也可以根据自身情况选择其他互访方案。关于VPC对等连接的更多内容，请参见：

-   [VPC互连](https://help.aliyun.com/zh/vpc/cross-vpc-interconnection-overview/#section-fz7-c87-cna)
-   [使用VPC对等连接实现VPC私网互通](https://help.aliyun.com/zh/vpc/vpc-peer-to-peer-connection)
-   [VPC对等连接配置示例](https://help.aliyun.com/zh/vpc/vpc-peer-to-peer-connection)
