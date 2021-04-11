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
Phiên bản demo: 
- Thực hiện lưu trữ thông tin từ bảng dữ liệu vào redis.
- Dùng API lấy ra được dữ liệu trong redis.

Phiên bản ứng dụng: (DONE)
- Cho phép reload cache từ API và cron-job.
- Xây dựng API trả về dữ liệu trong cache hoặc dữ liệu từ databse.