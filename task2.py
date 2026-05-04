import matplotlib.pyplot as plt
import numpy as np


def koch_curve(p1: np.ndarray, p2: np.ndarray, level: int) -> list[np.ndarray]:
    """
    Recursively generates points of a Koch curve between two points p1 and p2.
    Returns a list of points forming the curve.
    """
    if level == 0:
        return [p1, p2]

    # Divide segment into three equal parts
    a = p1 + (p2 - p1) / 3
    b = p1 + 2 * (p2 - p1) / 3

    # Calculate the apex of the equilateral triangle
    angle = np.pi / 3  # 60 degrees
    direction = b - a
    rotation = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)],
    ])
    apex = a + rotation @ direction

    # Recurse on each of the 4 new segments
    points = []
    for seg_start, seg_end in [(p1, a), (a, apex), (apex, b), (b, p2)]:
        segment_points = koch_curve(seg_start, seg_end, level - 1)
        # Avoid duplicating junction points
        points.extend(segment_points[:-1])

    points.append(p2)
    return points


def koch_snowflake(level: int) -> tuple[list, list]:
    """
    Generates the full Koch snowflake (3 Koch curves forming a triangle).
    Returns (x_coords, y_coords).
    """
    # Equilateral triangle vertices
    size = 1.0
    p1 = np.array([0.0, 0.0])
    p2 = np.array([size, 0.0])
    p3 = np.array([size / 2, size * np.sqrt(3) / 2])

    all_points = []
    for seg_start, seg_end in [(p1, p2), (p2, p3), (p3, p1)]:
        segment_points = koch_curve(seg_start, seg_end, level)
        all_points.extend(segment_points[:-1])

    # Close the snowflake
    all_points.append(all_points[0])

    x = [pt[0] for pt in all_points]
    y = [pt[1] for pt in all_points]
    return x, y


def main():
    try:
        level = int(input("Enter recursion level (0–7 recommended): "))
        if level < 0:
            print("Level must be a non-negative integer.")
            return
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    x, y = koch_snowflake(level)

    _, ax = plt.subplots(figsize=(8, 7))
    ax.plot(x, y, color="royalblue", linewidth=0.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Koch Snowflake — level {level}", fontsize=14)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

