# Amazon Order History
Parses your Amazon Order history.

Run the python file with your Amazon email and password as the first and second parameters, respectively.

```sh
> python amazon_order_history.py name@email.com Password1
```

Outputs a .csv file:

|OrderDate |OrderTotal|OrderNumber|Status|DeliveredDate|
|----------|----------|-----------|------|-------------|
|2018-07-25|33.02|000-0000000-0000001|Delivered|2018-07-26|
|2018-07-19|19.9|000-0000000-0000002|Delivered|2018-07-25|
|2018-07-18|33.89|000-0000000-0000003|Delivered|2018-07-21|


Note: I've only tested this on Amazon.ca
