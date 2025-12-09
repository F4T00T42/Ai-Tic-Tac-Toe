import math

def project_3d_to_2d(x, y, z, cx, cy):
  distance = 800
  scale = distance / (distance + z)
  return cx + x * scale, cy + y * scale, scale, z


def rotate_point_3d(x, y, z, rx, ry):
  cos_y = math.cos(ry)
  sin_y = math.sin(ry)
  x1 = x * cos_y - z * sin_y
  z1 = x * sin_y + z * cos_y
  cos_x = math.cos(rx)
  sin_x = math.sin(rx)
  y1 = y * cos_x - z1 * sin_x
  z2 = y * sin_x + z1 * cos_x
  return x1, y1, z2


def point_in_polygon(point, poly):
  x, y = point
  inside = False
  n = len(poly)
  for i in range(n):
    x1, y1 = poly[i]
    x2, y2 = poly[(i + 1) % n]
    if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-6) + x1):
      inside = not inside
  return inside


def scale_polygon(poly, factor):
  cx = sum(x for x, _ in poly) / len(poly)
  cy = sum(y for _, y in poly) / len(poly)
  return [((x - cx) * factor + cx, (y - cy) * factor + cy) for x, y in poly]