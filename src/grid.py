import configuration
from vector import Vec2


class SpatialGrid:
    """
    Spatial grid partitioning class for faster collision detection between lines.

    Since lines are not straight, collisions are estimated by storing a series of positions that go on the line.
    Collision is checked right before each position is recorded in self.grid.
    """

    def __init__(self) -> None:
        self._grid: dict[tuple[int, int], set[Vec2]] = {}
        self._setup_partition()

    def _setup_partition(self) -> None:
        """
        Setup partition table
        """
        for row in range(configuration.NUM_PARTITION_ROW):
            for col in range(configuration.NUM_PARTITION_COL):
                self._grid[(row, col)] = set()

    def add_position(self, position: Vec2) -> None:
        self._grid[self._position_to_grid_indices(position)].add(position)

    def check_collision(self, position: Vec2) -> bool:
        grid_indices = self._position_to_grid_indices(position)

        for x in range(grid_indices[0] - 1, grid_indices[0] + 2):
            for y in range(grid_indices[1] - 1, grid_indices[1] + 2):
                if (
                    x < 0
                    or x >= configuration.NUM_PARTITION_COL
                    or y < 0
                    or y >= configuration.NUM_PARTITION_ROW
                ):
                    continue
                partition = self._grid[(x, y)]
                if self._check_collision_in_partition(position, partition):
                    return True
        return False

    def _check_collision_in_partition(
        self, position: Vec2, partition: set[Vec2]
    ) -> bool:
        for p in partition:
            if p is position:
                continue
            if (p - position).norm() < configuration.line.width / 2:
                # print(
                #     f"Collision with {p} and {position}, {(p - position).norm()} {configuration.line.width}"
                # )
                return True
        return False

    def _position_to_grid_indices(self, position: Vec2) -> tuple[int, int]:
        row = int(position.x * configuration.NUM_PARTITION_COL)
        col = int(position.y * configuration.NUM_PARTITION_ROW)
        return (row, col)
