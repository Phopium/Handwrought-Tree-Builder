import ui.config as uicfg
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
            for conn_id in talent["connections"]:
                end_x, end_y = self.talent_buttons[tree["name"]][conn_id][1]
                s_offset_x, s_offset_y = get_line_offsets(start_x, uicfg.initial_tile_posx, uicfg.btn_width, uicfg.btn_height)
                e_offset_x, e_offset_y = get_line_offsets(end_x, uicfg.initial_tile_posx, uicfg.btn_width, uicfg.btn_height)
                
                line_id = canvas.create_line(start_x + s_offset_x, start_y + s_offset_y, end_x + e_offset_x, end_y + e_offset_y, fill="#76d8ff", width=2)
                canvas.lines.append(line_id)


def modify_connection(self, tree_name, from_id, to_id):
    tree = next(t for t in self.data["trees"] if t["name"] == tree_name)
    from_talent = next(t for t in tree["talents"] if t["id"] == from_id)
    to_talent = next(t for t in tree["talents"] if t["id"] == to_id)
    if to_id in from_talent["connections"]:
        from_talent["connections"].remove(to_id)
    elif from_id in to_talent["connections"]:
        to_talent["connections"].remove(from_id)
    else:
        from_talent["connections"].append(to_id)

def modify_position(self, tree_name, from_id, to_id):
    #tree = next(t for t in self.data["trees"] if t["name"] == tree_name)
    from_talent = next(t for t in self.data if t["id"] == from_id)
    to_talent = next(t for t in self.data if t["id"] == to_id)

    # Copy the position values
    from_x_pos, from_y_pos = from_talent["x_pos"], from_talent["y_pos"]
    to_x_pos, to_y_pos = to_talent["x_pos"], to_talent["y_pos"]

    # Swap position values
    from_talent["x_pos"], to_talent["x_pos"] = to_x_pos, from_x_pos
    from_talent["y_pos"], to_talent["y_pos"] = to_y_pos, from_y_pos