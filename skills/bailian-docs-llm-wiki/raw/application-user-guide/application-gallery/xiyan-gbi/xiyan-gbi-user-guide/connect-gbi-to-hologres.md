# 通过析言GBI连接实时数仓Hologres

当析言GBI连接实时数仓Hologres后，Hologres实时查询并输出数据至析言GBI进行数据分析。本文为您介绍如何通过析言GBI连接实时数仓Hologres，并利用自然语言完成数据分析。

## 前置概念

阅读本文前，您可按需了解[什么是实时数仓Hologres](https://help.aliyun.com/zh/hologres/product-overview/what-is-hologres)。

## 操作步骤

### Hologres数据准备

以下示例使用MaxCompute提供的公开数据集TPC-H的ORDERS表。您无需进行任何额外准备，只需运行以下SQL语句，即可通过MaxCompute外部表将ORDERS表的数据导入Hologres。

```
-- 创建外部表
IMPORT FOREIGN SCHEMA public_data
LIMIT TO (ORDERS_10g)
FROM SERVER odps_server INTO public options (if_table_exist 'update');

-- 创建内部表
BEGIN;
CREATE TABLE ORDERS (
    O_ORDERKEY bigint NOT NULL PRIMARY KEY,
    O_CUSTKEY int NOT NULL,
    O_ORDERSTATUS text NOT NULL,
    O_TOTALPRICE DECIMAL(12, 2) NOT NULL,
    O_ORDERDATE timestamptz NOT NULL,
    O_ORDERPRIORITY text NOT NULL,
    O_CLERK text NOT NULL,
    O_SHIPPRIORITY int NOT NULL,
    O_COMMENT text NOT NULL
);

CALL set_table_property ('ORDERS', 'segment_key', 'O_ORDERDATE');
CALL set_table_property ('ORDERS', 'distribution_key', 'O_ORDERKEY');
CALL set_table_property ('ORDERS', 'bitmap_columns', 'O_ORDERKEY,O_CUSTKEY,O_ORDERSTATUS,O_ORDERPRIORITY,O_CLERK,O_SHIPPRIORITY,O_COMMENT');
CALL set_table_property ('ORDERS', 'dictionary_encoding_columns', 'O_ORDERSTATUS,O_ORDERPRIORITY,O_CLERK,O_COMMENT');

COMMENT ON COLUMN ORDERS.O_ORDERKEY IS '订单编号';
COMMENT ON COLUMN ORDERS.O_CUSTKEY IS '顾客序号';
COMMENT ON COLUMN ORDERS.O_ORDERSTATUS IS '订单状态';
COMMENT ON COLUMN ORDERS.O_TOTALPRICE IS '总价';
COMMENT ON COLUMN ORDERS.O_ORDERDATE IS '下单日期';
COMMENT ON COLUMN ORDERS.O_ORDERPRIORITY IS '订单优先级';
COMMENT ON COLUMN ORDERS.O_CLERK IS '收银员';
COMMENT ON COLUMN ORDERS.O_SHIPPRIORITY IS '发货优先级';
COMMENT ON COLUMN ORDERS.O_COMMENT IS '备注';

COMMIT;

-- 数据导入内表
INSERT INTO ORDERS SELECT * FROM ORDERS_10g;
```

### 连接Hologres

析言GBI支持通过公网的方式连接Hologres，详情请参见[实例详情](https://help.aliyun.com/zh/hologres/user-guide/instance-configurations)。具体操作模式如下：

1.  前往[应用广场](https://bailian.console.aliyun.com/?tab=app#/app-market/solution)解决方案页面，单击**析言GBI**下的**立即查看**。
    
2.  单击**数据表管理**，根据连接方式，选择**访问公网数据库**中的**PostgreSQL**，并单击**授权联接**。
    
    通过公网连接Hologres，请确保在[Hologres管理控制台](https://hologram.console.aliyun.com/#/instance)的**实例详情**页**网络信息**中已手动开启公网。
    
3.  填入数据库配置参数和登录信息，单击**授权联接**。
    
    相关配置说明如下：
    
    **参数名称**
    
    **说明**
    
    IP/域名
    
    Hologres实例的域名。您可以进入[Hologres管理控制台](https://hologram.console.aliyun.com/#/instance)的**实例列表**，选择对应实例，在**实例详情**的**网络信息**中，选择**公网**获取对应域名。
    
    端口号
    
    Hologres实例的网络端口。您可以进入[Hologres管理控制台](https://hologram.console.aliyun.com/#/instance)的**实例列表**，选择对应实例，在**实例详情**的**网络信息**中，选择**公网**获取对应域名的端口。
    
    数据库名称
    
    需要连接的数据库名。您可以进入[Hologres管理控制台](https://hologram.console.aliyun.com/#/instance)，**前往HoloWeb**，连接并登录对应实例，在**已登录实例**中查询对应数据库名。
    
    数据库Schema
    
    需要连接的数据库Schema。默认是`public`，您也可以填写其他Schema。
    
    数据库用户名
    
    当前账号的AccessKey ID。获取方式请参见[AccessKey 管理](https://usercenter.console.aliyun.com/?spm=5176.2020520153.nav-right.dak.3bcf415dCWGUBj#/manage/ak)。
    
    数据库密码
    
    当前账号的AccessKey Secret。获取方式请参见[创建访问密钥](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。
    
4.  单击右侧**关联数据表**，选择需要关联数据表的名称，单击**确认关联**。
    
    完成数据表关联，可对数据表进行管理。
    

## 自然语言问答

单击析言GBI**首页**，您可以通过自然语言问答形式完成数据分析，在输入框中输入与所关联的数据表相关问题。例如“每年有多少笔订单？有多少笔最高优订单？”。

系统将自动完成问题改写、数据表选取、查询SQL生成和SQL执行，最终以表格形式展示查询结果。您还可以单击**编辑SQL**修改系统生成的SQL语句。

## 更多功能与操作

您可以进一步参考[析言GBI使用指南](raw/application-user-guide/application-gallery/xiyan-gbi/xiyan-gbi-user-guide.md)，完成企业数据管理、模型优化案例管理、模型输出干预等高级操作。
