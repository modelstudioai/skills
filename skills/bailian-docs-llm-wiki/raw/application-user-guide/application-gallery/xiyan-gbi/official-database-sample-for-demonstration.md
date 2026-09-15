# 官方提供演示用的数据库样例

本文主要提供了用于演示的测试数据，旨在帮助您快速构建测试数据，并在实际项目中灵活运用API进行后续的集成开发。

## 前提条件

-   已开通阿里云百炼。
-   已[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。
-   已[获取AccessKey ID和AccessKey Secret](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
-   RAM用户已添加`AliyunDataAnalysisGBIFullAccess`权限策略：[管理RAM用户的权限](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)。
-   已在析言GBI的**[数据表管理](https://bailian.console.aliyun.com/xiyan#/dataManagement/dataSourceM)**中授权联接了数据库。具体操作，请参见[数据库连接](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#8e5d17697392b)。

## 操作步骤

### 步骤一：准备数据

为方便演示基本功能，您可以将以下样例数据导入到自己的数据库中。

```
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '产品ID',
    product_name VARCHAR(255) NOT NULL COMMENT '产品名称',
    price DECIMAL(10, 2) NOT NULL COMMENT '产品价格',
    category VARCHAR(255) NOT NULL COMMENT '产品类别',
    in_stock_quantity INT NOT NULL COMMENT '库存数量',
    create_date DATE NOT NULL COMMENT '创建日期,格式为YYYY-MM-DD',
    INDEX category_idx (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT '存储产品信息的表';
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT COMMENT '客户ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '客户名',
  `email` varchar(255) NOT NULL COMMENT '客户电子邮箱',
  `join_date` date NOT NULL COMMENT '加入日期，格式为YYYY-MM-DD',
  PRIMARY KEY (`customer_id`),
  KEY `name_idx` (`name`) COMMENT '按姓名索引用于优化查询',
  KEY `email_idx` (`email`) COMMENT '按电子邮箱索引用于优化查询'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存储客户信息的表';
CREATE TABLE orders (
	order_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
	customer_id INT NOT NULL COMMENT '下单客户的ID',
	product_id INT NOT NULL COMMENT '所订购产品的ID',
	order_date DATE NOT NULL COMMENT '下单日期，格式为YYYY-MM-DD',
	quantity INT NOT NULL COMMENT '订购产品的数量',
	order_status VARCHAR(50) NOT NULL COMMENT '订单状态（例如：待发货、已发货、已送达）',
	INDEX order_date_idx (order_date) COMMENT '按下单日期索引用于优化查询',
	INDEX customer_product_idx (customer_id, product_id),
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
	FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT '存储订单信息的表';
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (1, '苏斌', 'jiehao@example.com', '2024-03-01');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (2, '陈建国', 'qinjuan@example.net', '2023-12-05');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (3, '叶桂芝', 'chaoyin@example.net', '2024-05-24');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (4, '赵飞', 'yinxiulan@example.net', '2023-05-14');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (5, '张强', 'juansu@example.org', '2023-07-04');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (6, '毛淑珍', 'leibai@example.com', '2023-07-29');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (7, '邓瑞', 'tianli@example.com', '2022-11-26');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (8, '章红', 'huangyong@example.org', '2024-07-02');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (9, '胡玉兰', 'lizheng@example.org', '2024-04-10');
INSERT INTO `customers` (`customer_id`, `name`, `email`, `join_date`) VALUES (10, '厉坤', 'ping59@example.com', '2024-01-14');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (1, '护眼台灯', 1837.00, '数码产品', 16, '2023-12-31');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (2, '便携式榨汁机', 584.82, '数码产品', 98, '2024-04-15');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (3, '耳机无线蓝牙', 1368.97, '数码产品', 26, '2024-05-01');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (4, '空气炸锅', 760.15, '数码产品', 76, '2024-05-19');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (5, '华为P30手机', 886.24, '数码产品', 1, '2024-10-20');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (6, '智能手表', 1217.32, '数码产品', 52, '2024-01-21');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (7, '全自动豆浆机', 1162.19, '数码产品', 61, '2023-10-31');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (8, '小米手环', 91.26, '数码产品', 2, '2024-02-24');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (9, '化妆刷套装', 1410.57, '数码产品', 90, '2024-08-27');
INSERT INTO `products` (`product_id`, `product_name`, `price`, `category`, `in_stock_quantity`, `create_date`) VALUES (10, '电热水壶', 823.79, '数码产品', 61, '2023-11-04');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (1, 2, 8, '2023-12-12', 7, '已送达');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (2, 1, 7, '2024-03-05', 5, '已送达');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (3, 3, 9, '2024-06-11', 1, '已发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (4, 5, 10, '2024-01-20', 6, '待发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (5, 10, 1, '2024-04-25', 10, '待发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (6, 4, 8, '2024-06-11', 7, '已发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (7, 9, 6, '2024-01-05', 6, '已发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (8, 2, 5, '2024-07-13', 2, '待发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (9, 8, 7, '2024-01-18', 2, '已发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (10, 5, 10, '2024-09-23', 2, '已送达');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (11, 7, 7, '2024-07-06', 3, '已送达');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (12, 1, 2, '2024-08-02', 5, '已发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (13, 2, 7, '2024-07-12', 4, '待发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (14, 3, 9, '2024-03-18', 3, '待发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (15, 9, 8, '2024-06-19', 8, '已送达');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (16, 9, 8, '2023-12-18', 4, '已发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (17, 4, 8, '2024-01-18', 2, '已送达');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (18, 4, 3, '2024-08-10', 6, '待发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (19, 1, 9, '2023-11-17', 6, '已发货');
INSERT INTO `orders` (`order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `order_status`) VALUES (20, 2, 2, '2024-08-25', 2, '已发货');
```

完成数据的导入后，您需要在析言控制台中将这些数据表进行关联。

### 步骤二：在控制台验证问答功能

在对话式查询界面输入自然语言问题`最畅销的3个商品的名称`，系统依次执行问题改写、数据表选取（products、orders、customers）、SQL生成及执行SQL四个步骤，显示**执行完成**状态。查询结果表格的product\_name列返回三行数据：小米手环、全自动豆浆机、护眼台灯。底部自然语言总结为"最畅销的3个商品名称分别是：小米手环、全自动豆浆机和护眼台灯"。
