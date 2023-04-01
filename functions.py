import block

def shift_blocks_down(placed_blocks_ar : list[list[block.block]],playable_field,cleared_row: int) -> None:
    for row in range(cleared_row-1,-1,-1):
        for col in range(playable_field):
            block = placed_blocks_ar[row][col]
            if block:
                block.map_pos[1] += 1
                placed_blocks_ar[row+1][col] = block
                placed_blocks_ar[row][col] = None



def check_line(placed_blocks_ar:list[list[block.block]],playable_field:int)->None:
    for row, lines in enumerate(placed_blocks_ar):
        if all(item for item in lines):
            for item in lines:
                item.tetromino.blocks.remove(item)
                placed_blocks_ar[row][int(item.map_pos[0])] = None
            shift_blocks_down(placed_blocks_ar,playable_field,row)
            
            