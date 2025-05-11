import random
import math

def get_points(mu_x: float, mu_y: float, sigma: float, group: int, nbr_points: int) -> list:
    return [[(random.gauss(mu_x, sigma), random.gauss(mu_y, sigma)), group] for _ in range(nbr_points)]


def get_distances(new_element: tuple, elements: list) -> list:
    x1, y1 = new_element

    neighbors = []

    for element in elements:
        x2, y2 = element[0]
        group = element[1]
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        neighbors.append((dist, group))

    neighbors = list(sorted(neighbors, key=lambda x: x[0]))
    return neighbors

def get_nearest_neighbors_group(k: int, distances: list) -> tuple:
    neighbors_groups = {}
    for element in distances[0:k]:
        neighbor_group = element[1]
        if neighbors_groups.get(neighbor_group):
            neighbors_groups[neighbor_group] += 1
        else:
            neighbors_groups[neighbor_group] = 1

    return sorted(neighbors_groups.items(), key=lambda x:x[1], reverse=True)[0] # (group, nbr of neighbor)


if __name__ == '__main__':
    from CoordinateSystem import CoordinateSystem, Landmark, Landmarks
    sigma = 0.5

    n_points = 100

    mu_x_g1 = 3
    mu_y_g1 = 3

    mu_x_g2 = -3
    mu_y_g2 = -3

    mu_x_g3 = -3
    mu_y_g3 = 3

    mu_x_g4 = 3
    mu_y_g4 = -3

    k_nearest = 11

    group_1 = get_points(mu_x_g1, mu_y_g1, sigma, 1, n_points)
    group_2 = get_points(mu_x_g2, mu_y_g2, sigma, 2, n_points)
    group_3 = get_points(mu_x_g3, mu_y_g3, sigma, 3, n_points)
    group_4 = get_points(mu_x_g4, mu_y_g4, sigma, 4, n_points)
    groups = group_1 + group_2 + group_3 + group_4

    element = (random.uniform(-3, 3), random.uniform(-3, 3))

    distance = get_distances(element, groups)

    landmarks_g1 = Landmarks([])
    landmarks_g2 = Landmarks([])
    landmarks_g3 = Landmarks([])
    landmarks_g4 = Landmarks([])
    for i in group_1:
        landmarks_g1 += Landmark(i[0])
    for i in group_2:
        landmarks_g2 += Landmark(i[0])
    for i in group_3:
        landmarks_g3 += Landmark(i[0])
    for i in group_4:
        landmarks_g4 += Landmark(i[0])

    landmark_new_element = Landmark(element, text_color=(255, 255, 255), text="press esc to see of which groups i belong", text_placement="topright")

    points_color_list = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]

    system = CoordinateSystem([landmarks_g1, landmarks_g2, landmarks_g3, landmarks_g4, landmark_new_element], (800, 800), -6, 6, 2, -6, 6, 2)
    system.show(background_color=(0,0,0), points_color_list=points_color_list, axes_color=(255, 255, 255), graduation_color=(255, 255, 255), show_x_graduation_coordinate=True, show_y_graduation_coordinate=True)

    nearest_group = get_nearest_neighbors_group(k_nearest, distance)[0]
    if nearest_group == 1:
        points_color_list[4] = (255, 0, 0)

    elif nearest_group == 2:
        points_color_list[4] = (255, 255, 0)

    elif nearest_group == 3:
        points_color_list[4] = (0, 255, 0)

    elif nearest_group == 4:
        points_color_list[4] = (0, 0, 255)

    landmark_new_element.text = "i am here"

    system = CoordinateSystem([landmarks_g1, landmarks_g2, landmarks_g3, landmarks_g4, landmark_new_element], (800, 800), -6, 6, 2, -6, 6, 1)
    system.show(background_color=(0,0,0), points_color_list=points_color_list, axes_color=(255, 255, 255), graduation_color=(255, 255, 255), show_x_graduation_coordinate=True, show_y_graduation_coordinate=True)