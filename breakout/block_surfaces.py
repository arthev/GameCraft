#Warning! Lazy hack: These get reassigned at the bottom so that the B_versions take on the DB_values.
BLOCK = (SCREEN_SIZE[0]//10, SCREEN_SIZE[1]//30)
BH = BLOCK[1]
BW = BLOCK[0]
DBL = BW//64
DBH = BLOCK[1] - 2*DBL
DBW = BLOCK[0] - 2*DBL
DBLOCK = (DBW, DBH)

def generate_blocks():
    dblock = pygame.Surface(BLOCK) #Copy these
    dblock.fill(BLACK)
    block = pygame.Surface(DBLOCK)
    block.fill(BLACK)

    def dblockify(b):
        db = dblock.copy()
        db.blit(b, (DBL, DBL))
        return db.convert()

    block_1 = block.copy()
    block_1.fill(COLOUR)
    block_1 = dblockify(block_1)

    block_2 = block.copy()
    pygame.draw.rect(block_2, COLOUR, 
            (0, 0, DBW, DBH), 4)
    block_2 = dblockify(block_2)

    block_3 = block.copy()
    pygame.draw.rect(block_3, COLOUR, 
            (0, 0, DBW, DBH), 4)
#    pygame.draw.lines(block_3, COLOUR, False, 
#            ((8, 0), (8, DBH), (16, DBH), (16, 0), (24, 0), (24, DBH), (32, DBH), (32, 0), (40, 0), (40, DBH), (48, DBH), (48, 0), (56, 0), (56, DBH)), 4)
    for i in range(DBW):
        if (i-1) % 6 == 0:
            pygame.draw.line(block_3, COLOUR,
                    (i, 0), (i, DBH), 3)
    block_3 = dblockify(block_3)

    block_4 = block.copy()
    pygame.draw.rect(block_4, COLOUR, (0, 0, DBLOCK[0], DBLOCK[1]), 1)
    for i in range(DBH):
        if i % 2 == 0:
            pygame.draw.line(block_4, COLOUR,
                    (0, i), (DBW, i), 1)
    block_4 = dblockify(block_4)

    block_5 = block.copy()
    pygame.draw.rect(block_5, COLOUR, (0, 0, DBW, DBH), 1)
    for i in range(DBW):
        if i % 2 == 0:
            pygame.draw.line(block_5, COLOUR,
                    (i, 0), (i, DBH), 1)
    block_5 = dblockify(block_5)

    block_6 = block.copy()
    pygame.draw.rect(block_6, COLOUR, (0, 0, DBW, DBH), 1)
    for i in range(-16, DBW):
        if i % 4 == 0:
            pygame.draw.line(block_6, COLOUR,
                    (i, 0), (i + 16, DBH), 1)
    block_6 = dblockify(block_6)

    return {1:block_1, 2:block_2, 3:block_3, 4:block_4, 5:block_5, 6:block_6}

block_surfaces = generate_blocks()
