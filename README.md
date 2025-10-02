# LTW_Nhom02_BookSale
## Chạy dự án
1. Clone dự án về máy
2. Thực hiện tải dự án lên với PyChamr dựa theo hướng dẫn của thầy
3. Nhớ thiết lập trình biên dịch cho dự án
4. Tạo 1 app được phân công cho việc coding 
## Cấu trúc dự án
1. booksale: là phần cấu hình
2. app: ví dụ product, cart, profile,.... --> dùng để thêm, sửa, xóa...
3. folder template chung: base.html
4. folder static: chứa các image, js, css chung cho dự án
5. trong mỗi app sẽ có management để thực hiện dump dữ liệu từ file excel cho model cua từng app
6. Trong mỗi app sẽ có template riêng, và các template này sẽ kế thừa từ base.html vì base nó thiết lập ra navbar và footer
7. Mỗi app sẽ có model riêng --> ai làm app nào thì tạo model cho app đó
