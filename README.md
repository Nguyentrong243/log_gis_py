# LOG_GIS_PY

## Quy ước nhánh (Branch Convention)

### main

- Nhánh chính
- KHÔNG làm việc trực tiếp
- Chỉ **Admin** được merge & push code hoàn chỉnh

### dev

- Nhánh phát triển chung
- Tất cả thành viên push code lên nhánh này
- Code trên dev có thể chưa hoàn chỉnh

### feature/

- Nhánh chức năng
- Tạo từ nhánh `dev`
- Ví dụ:
  - feature/read-file
  - feature/map-visualization

---

## Quy trình làm việc cho thành viên

```bash
git checkout dev
git pull
git checkout -b feature/ten-chuc-nang
```
