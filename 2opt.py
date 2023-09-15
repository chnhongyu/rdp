# Solving Traveling Salesman Problem by applying Discrete Improving Search (local search)
# Neighborhood structure/Move: 2-exchange
# - remove two arcs, not sharing a node -> three paths
# - reconnect the three paths and form a new dicycle, by inserting two arcs

import random

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def total_distance(tour, points):
    distance = 0
    for i in range(len(tour)):
        distance += euclidean_distance(points[tour[i]], points[tour[(i + 1) % len(tour)]])
    return distance

def two_opt(tour, points):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue  # No need to reverse two consecutive edges
                new_tour = tour[:]
                new_tour[i:j] = reversed(tour[i:j])
                if total_distance(new_tour, points) < total_distance(tour, points):
                    tour = new_tour
                    improved = True
        return tour

def main():
    # Define a list of points (coordinates) for the TSP
    points = [(0, 0), (1, 2), (2, 4), (3, 1), (4, 3)]

    # Create an initial tour (random permutation of points)
    tour = list(range(len(points)))
    random.shuffle(tour)

    # Apply the 2-opt heuristic to improve the tour
    tour = two_opt(tour, points)

    # Calculate and print the total distance of the optimized tour
    distance = total_distance(tour, points)
    print("Optimized tour:", tour)
    print("Total distance:", distance)

if __name__ == "__main__":
    main()
