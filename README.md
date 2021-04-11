# Lời mở đầu

## Chức năng 
Dự án này là phiên bản tiếp theo của dự án [flask-celery-hr-noti](https://github.com/quangvinh1986/flask-celery-hr-noti) cho phép thực hiện:
- Thực hiện đặt cache các dữ liệu của các bảng thường xuyên truy xuất.
- Cho phép reload lại cache tự động hàng ngày/hàng giờ bằng các cron-task
- Hoặc chủ động reload lại cache từ end-point



## Công nghệ sử dụng

- Python 3.8
- Flask 1.1.1
- Celery 5.0.5
- Redis: Sử dụng như message queue của celery và là nơi lưu trữ cache của hệ thống.
- PostgreSQL (Để đảm bảo việc có thể phình to về mặt chức năng, database của bài toán thay đổi thành RDBMS)

# Về dự án:
Phiên bản demo (DONE): 
- Thực hiện lưu trữ thông tin từ bảng dữ liệu vào redis.
  
  ex: http://0.0.0.0:5001/myApi/hrApi/departments?isReloadCache=true
  
```JSON
{
  "data": [
    {
      "LOCATION_ID": 1700,
      "MANAGER_ID": 200,
      "DEPARTMENT_NAME": "Administration",
      "DEPARTMENT_ID": 10
    },
    {
      "LOCATION_ID": 1800,
      "MANAGER_ID": 201,
      "DEPARTMENT_NAME": "Marketing",
      "DEPARTMENT_ID": 20
    }
  ],
  "dateReceived": "2021-04-12 00:10:49",
  "isCache": false
}      
  ```
  
- Dùng API lấy ra được dữ liệu trong redis.

ex: http://0.0.0.0:5001/myApi/hrApi/departments?isReloadCache=false

http://0.0.0.0:5001/myApi/hrApi/departments

```JSON
{
  "data": [
    {
      "LOCATION_ID": 1700,
      "MANAGER_ID": 200,
      "DEPARTMENT_NAME": "Administration",
      "DEPARTMENT_ID": 10
    },
    {
      "LOCATION_ID": 1800,
      "MANAGER_ID": 201,
      "DEPARTMENT_NAME": "Marketing",
      "DEPARTMENT_ID": 20
    }
  ],
  "dateReceived": "2021-04-12 00:10:49",
  "isCache": true
}      
  ```


Phiên bản nâng c:ao (TO_DO)
- Cho phép reload cache từ cron-job, các action dùng trong background-task
