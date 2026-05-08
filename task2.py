import turtle


def koch_curve(t: turtle.Turtle, order: int, size: float) -> None:
    """
    Recursively draws one segment of the Koch curve.

    Args:
        t: Turtle object used for drawing.
        order: Recursion depth. Higher value = more spikes.
        size: Length of the current segment.
    """
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)


def draw_koch_snowflake(order: int, size: float = 300) -> None:
    """
    Draws a full Koch snowflake consisting of 3 Koch curves.

    Args:
        order: Recursion depth.
        size: Side length of the initial equilateral triangle.
    """
    window = turtle.Screen()
    window.title(f"Koch Snowflake — level {order}")
    window.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.pencolor("royalblue")
    t.pensize(1)

    # Position the turtle so the snowflake is centered
    t.penup()
    t.goto(-size / 2, -size * (3 ** 0.5) / 6)
    t.pendown()

    # Draw 3 sides of the snowflake
    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)

    window.mainloop()


def main() -> None:
    try:
        order = int(input("Enter recursion level (0–6 recommended): "))
        if order < 0:
            print("Level must be a non-negative integer.")
            return
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    draw_koch_snowflake(order)


if __name__ == "__main__":
    main()
