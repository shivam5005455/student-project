import cv2
import numpy as np
import math

# Window
WIDTH, HEIGHT = 800, 600

# 3D cube vertices
cube = np.array([
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
], dtype=float)

# Cube edges
edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

def rotation_matrix(ax, ay, az):
    """Create 3D rotation matrix."""
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(ax), -math.sin(ax)],
        [0, math.sin(ax),  math.cos(ax)]
    ])

    Ry = np.array([
        [ math.cos(ay), 0, math.sin(ay)],
        [0, 1, 0],
        [-math.sin(ay), 0, math.cos(ay)]
    ])

    Rz = np.array([
        [math.cos(az), -math.sin(az), 0],
        [math.sin(az),  math.cos(az), 0],
        [0, 0, 1]
    ])

    return Rz @ Ry @ Rx


# Animation angles
angle_x = 0
angle_y = 0
angle_z = 0

while True:

    # Black background
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Rotate cube
    R = rotation_matrix(angle_x, angle_y, angle_z)
    rotated = cube @ R.T

    # Move cube away from camera
    rotated[:, 2] += 5

    # Perspective projection
    focal_length = 500

    points = []

    for x, y, z in rotated:
        px = int((x * focal_length / z) + WIDTH / 2)
        py = int((y * focal_length / z) + HEIGHT / 2)

        points.append((px, py))

    # Draw edges
    for a, b in edges:
        cv2.line(
            frame,
            points[a],
            points[b],
            (0, 255, 255),
            3,
            cv2.LINE_AA
        )

    # Draw vertices
    for p in points:
        cv2.circle(
            frame,
            p,
            7,
            (255, 100, 0),
            -1,
            cv2.LINE_AA
        )

    # Title
    cv2.putText(
        frame,
        "Python + OpenCV 3D Cube",
        (210, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press Q to exit",
        (300, 570),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (180, 180, 180),
        2
    )

    # Show
    cv2.imshow("3D Animation", frame)

    # Animation speed
    angle_x += 0.02
    angle_y += 0.03
    angle_z += 0.01

    # Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()