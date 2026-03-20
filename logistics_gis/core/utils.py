from math import radians, cos, sin, asin, sqrt

# tính khoảng cách giữa 2 điểm (km)
def distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return R * c


# tìm các store trong bán kính (km)
def find_nearby(lat, lon, stores, radius=5):
    result = []

    for s in stores:
        d = distance(lat, lon, s.lat, s.lng)
        if d <= radius:
            result.append(s)

    return result