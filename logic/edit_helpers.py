import ui.config as uicfg
import logic.supa_tables as supa
#import logic.supa_tables as supa

def get_line_offsets(x_pos, initial_x, btn_width, btn_height):
    """Helper function to calculate offsets based on x-position."""
    # Exception for initial tree tile
    if x_pos == initial_x:
        offset_x = btn_width * 0
        offset_y = btn_height * 1.35
    else:
        offset_x = btn_width / 2
        offset_y = btn_height / 1.5
    return offset_x, offset_y


def draw_connections(self, tree, canvas):
    for talent in self.data:
        if talent["tree_id"] == tree["id"]:
            start_x, start_y = self.talent_buttons[tree["name"]][talent["id"]][1]
            talent_pos = talent["talent_positions"]
            for conn_id in talent_pos["connections"]:
                end_x, end_y = conn_id
                s_offset_x, s_offset_y = get_line_offsets(start_x, uicfg.initial_tile_posx, uicfg.btn_width, uicfg.btn_height)
                e_offset_x, e_offset_y = get_line_offsets(end_x, uicfg.initial_tile_posx, uicfg.btn_width, uicfg.btn_height)
                
                line_id = canvas.create_line((start_x + s_offset_x), (start_y + s_offset_y), (end_x + e_offset_x), (end_y + e_offset_y), fill="#76d8ff", width=2)
                canvas.lines.append(line_id)


def modify_connection(self, tree_name, from_id, to_id):
    from_talent = next(t for t in self.data if t["id"] == from_id)
    from_talent_pos = from_talent["talent_positions"]
    to_talent = next(t for t in self.data if t["id"] == to_id)
    to_talent_pos = to_talent["talent_positions"]

    if to_id in from_talent_pos["connections"]:
        from_talent_pos["connections"].remove(to_id)
    elif from_id in to_talent_pos["connections"]:
        to_talent_pos["connections"].remove(from_id)
    else:
        from_talent_pos["connections"].append(to_id)
