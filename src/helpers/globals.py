BLOCK_SIZE_RATE = 1.0 / 20  # BLOCK_SIZE_RATE * window.with gives block size

SPEED_RATE = 7.5 #1.0 / 8  # should be multiplied by block_width to get standard speed

GRAVITY_RATE = -25 #-0.0098  # should be multiplied by block width to get gravity

MAX_LOAD_PER_DER = 12


class Direction:
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"
    OVERLAP = "overlap"
