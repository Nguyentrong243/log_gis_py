#!/usr/bin/env python
# coding: utf-8

# In[1]:


from geopy.distance import geodesic
import math

danh_sach_don_hang = {
    "DH01": {"ten": "Sang", "lat": 10.7840, "lon": 106.6960, "vung": "noi_thanh"},
    "DH02": {"ten": "An",   "lat": 10.7885, "lon": 106.7012, "vung": "noi_thanh"},
    "DH03": {"ten": "Hòa",  "lat": 10.7580, "lon": 106.6650, "vung": "noi_thanh"},
    "DH04": {"ten": "Bình", "lat": 10.8231, "lon": 106.6297, "vung": "noi_thanh"},
    "DH05": {"ten": "Yến",  "lat": 10.7200, "lon": 106.7250, "vung": "noi_thanh"},
    "DH06": {"ten": "Linh", "lat": 10.7721, "lon": 106.6983, "vung": "noi_thanh"},
    "DH07": {"ten": "Tuấn", "lat": 10.8010, "lon": 106.6825, "vung": "noi_thanh"},
    "DH08": {"ten": "Minh", "lat": 10.8500, "lon": 106.7700, "vung": "ngoai_thanh"},
    "DH09": {"ten": "Cường", "lat": 10.9500, "lon": 106.8200, "vung": "ngoai_thanh"},
    "DH10": {"ten": "Tuấn",  "lat": 10.8850, "lon": 106.6000, "vung": "ngoai_thanh"},
    "DH11": {"ten": "Lan",   "lat": 10.8900, "lon": 106.6100, "vung": "ngoai_thanh"},
    "DH12": {"ten": "Phước", "lat": 10.9500, "lon": 106.5000, "vung": "ngoai_thanh"},
    "DH13": {"ten": "Vy",    "lat": 10.7000, "lon": 106.5500, "vung": "ngoai_thanh"},
    "DH14": {"ten": "Sơn",   "lat": 10.8500, "lon": 106.8000, "vung": "ngoai_thanh"},
}

danh_sach_shipper = {
    "Tài":   {"lat": 10.7900, "lon": 106.7050, "don_dang_giao": []},
    "Hùng":  {"lat": 10.8100, "lon": 106.6800, "don_dang_giao": []}, 
    "Nam":   {"lat": 10.7850, "lon": 106.7000, "don_dang_giao": []}, 
    "Việt":  {"lat": 10.8200, "lon": 106.6300, "don_dang_giao": []}, 
    "Cường": {"lat": 10.8800, "lon": 106.6050, "don_dang_giao": []},
    "Dũng":  {"lat": 10.8550, "lon": 106.7900, "don_dang_giao": []}, 
    "Long":  {"lat": 10.7100, "lon": 106.5600, "don_dang_giao": []}, 
    "Thịnh": {"lat": 10.7700, "lon": 106.6800, "don_dang_giao": []}, 
    "Quốc":  {"lat": 10.9400, "lon": 106.5100, "don_dang_giao": []}, 
    "Kiệt":  {"lat": 10.6600, "lon": 106.7400, "don_dang_giao": []}, 
}



def tinh_thoi_gian(khoang_cach, vung):
    van_toc = 30 if vung == "noi_thanh" else 55 
    return math.ceil((khoang_cach / van_toc) * 60)

def tool_logistics_fix():
    print("\n" + "="*15 + " LỆNH ĐIỀU PHỐI ĐƠN HÀNG HÀNG LOẠT " + "="*15)

    ten_tx_input = input("Nhập tên tài xế: ").title().strip()
    if ten_tx_input not in danh_sach_shipper:
        print(f"❌ Lỗi: Không tìm thấy tài xế '{ten_tx_input}'!")
        return

    input_don = input("Nhập danh sách mã đơn (cách nhau bởi dấu phẩy): ").upper().strip()
    ds_ma_don = [d.strip() for d in input_don.split(",")]

    shipper = danh_sach_shipper[ten_tx_input]

    # [QUAN TRỌNG 1] Reset danh sách về 0 trước khi xử lý
    # Lệnh này đảm bảo bạn nhập bao nhiêu thì chỉ hiện bấy nhiêu, không bị cộng dồn đơn cũ
    shipper["don_dang_giao"] = [] 

    for ma_don_input in ds_ma_don:
        # [QUAN TRỌNG 2] Kiểm tra trùng lặp NGAY LẬP TỨC
        # Lệnh này chặn việc nhập "DH01, DH01". Cái đầu vào được, cái sau sẽ bị chặn.
        if ma_don_input in shipper["don_dang_giao"]:
            print(f"⚠️ Đơn hàng {ma_don_input} bị trùng! (Bỏ qua)")
            continue

        if ma_don_input not in danh_sach_don_hang:
            print(f"⚠️ Mã đơn {ma_don_input} không tồn tại!")
            continue

        don = danh_sach_don_hang[ma_don_input]
        vi_tri_khach = (don["lat"], don["lon"])
        vi_tri_shipper = (shipper["lat"], shipper["lon"])

        the_go_don = True

        # Logic kiểm tra khoảng cách gộp đơn (giữ nguyên logic cũ của bạn)
        if len(shipper["don_dang_giao"]) > 0:
            for ma_da_co in shipper["don_dang_giao"]:
                don_cu = danh_sach_don_hang[ma_da_co]
                kc_giua_don = geodesic((don_cu["lat"], don_cu["lon"]), vi_tri_khach).km

                if kc_giua_don > 9: 
                    print(f"❌ KHÔNG THỂ GỘP {ma_don_input}: Quá xa đơn {ma_da_co} ({kc_giua_don:.2f}km > 9km)")
                    the_go_don = False
                    break

        if the_go_don:
            # Chỉ khi nào thỏa mãn mọi điều kiện mới thêm vào danh sách
            shipper["don_dang_giao"].append(ma_don_input)

            kc_shipper_khach = geodesic(vi_tri_shipper, vi_tri_khach).km
            phut = tinh_thoi_gian(kc_shipper_khach, don["vung"])

            print(f"\n✅ XÁC NHẬN: {ten_tx_input} nhận đơn {ma_don_input}")
            print(f"- Khách hàng: {don.get('ten', 'Chưa rõ')}")
            print(f"- Khoảng cách: {kc_shipper_khach:.2f} km | Thời gian: {phut} phút")

    # In kết quả cuối cùng
    print(f"\n📍 {ten_tx_input} đang phụ trách: {', '.join(shipper['don_dang_giao'])}")


if __name__ == "__main__":
    while True:
        tool_logistics_fix()

        lua_chon = input("\nBạn có muốn tiếp tục kiểm tra đơn khác không? (y/n): ").lower().strip()

        if lua_chon == 'n':
            print("👋 Đã thoát hệ thống điều phối.")
            break
        elif lua_chon != 'y':
            print("⚠️ Lệnh không hợp lệ, mặc định thoát.")
            break



