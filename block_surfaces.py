#Warning! Lazy hack: These get reassigned at the bottom so that the B_versions take on the DB_values.
DBLOCK = (SCREEN_SIZE[0]//10, SCREEN_SIZE[1]//30)
DBH = DBLOCK[1]
DBW = DBLOCK[0]
BL = DBW//64
BH = DBLOCK[1] - 2*BL
BW = DBLOCK[0] - 2*BL
BLOCK = (BW, BH)

def generate_blocks():
    dblock = pygame.Surface(DBLOCK) #Copy these
    dblock.fill(BLACK)
    block = pygame.Surface(BLOCK)
    block.fill(BLACK)

    def dblockify(b):
        db = dblock.copy()
        db.blit(b, (BL, BL))
        return db.convert()

    block_1 = block.copy()
    block_1.fill(COLOUR)
    block_1 = dblockify(block_1)

    block_2 = block.copy()
    pygame.draw.rect(block_2, COLOUR, 
            (0, 0, BW, BH), 4)
    block_2 = dblockify(block_2)

    block_3 = block.copy()
    pygame.draw.rect(block_3, COLOUR, 
            (0, 0, BW, BH), 4)
    pygame.draw.lines(block_3, COLOUR, False, 
            ((8, 0), (8, BH), (16, BH), (16, 0), (24, 0), (24, BH), (32, BH), (32, 0), (40, 0), (40, BH), (48, BH), (48, 0), (56, 0), (56, BH)), 4)
    block_3 = dblockify(block_3)

    block_4 = block.copy()
    pygame.draw.rect(block_4, COLOUR, (0, 0, BLOCK[0], BLOCK[1]), 1)
    for i in range(BH):
        if i % 2 == 0:
            pygame.draw.line(block_4, COLOUR,
                    (0, i), (BW, i), 1)
    block_4 = dblockify(block_4)

    block_5 = block.copy()
    pygame.draw.rect(block_5, COLOUR, (0, 0, BW, BH), 1)
    for i in range(BW):
        if i % 2 == 0:
            pygame.draw.line(block_5, COLOUR,
                    (i, 0), (i, BH), 1)
    block_5 = dblockify(block_5)

    block_6 = block.copy()
    pygame.draw.rect(block_6, COLOUR, (0, 0, BW, BH), 1)
    for i in range(-16, BW):
        if i % 4 == 0:
            pygame.draw.line(block_6, COLOUR,
                    (i, 0), (i + 16, BH), 1)
    block_6 = dblockify(block_6)

    return {1:block_1, 2:block_2, 3:block_3, 4:block_4, 5:block_5, 6:block_6}

block_surfaces = generate_blocks()
