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
                end_x_pos, end_y_pos = conn_id
                x_offset = 275
                y_offset = 30
                x_spacing = 200
                y_spacing =  170

                end_x, end_y = x_offset + end_x_pos * x_spacing, y_offset + end_y_pos * y_spacing
                s_offset_x, s_offset_y = get_line_offsets(start_x, uicfg.initial_tile_posx, uicfg.btn_width, uicfg.btn_height)
                e_offset_x, e_offset_y = get_line_offsets(end_x, uicfg.initial_tile_posx, uicfg.btn_width, uicfg.btn_height)
                
                line_id = canvas.create_line((start_x + s_offset_x), (start_y + s_offset_y), (end_x + e_offset_x), (end_y + e_offset_y), fill="#76d8ff", width=2)
                canvas.lines.append(line_id)


def modify_connection(self, tree_name, from_id, to_id):
    from_talent = next(t for t in self.data if t["id"] == from_id)
    from_talent_pos_table = from_talent["talent_positions"]
    from_talent_pos = [from_talent_pos_table["x_pos"], from_talent_pos_table["y_pos"]]
    to_talent = next(t for t in self.data if t["id"] == to_id)
    to_talent_pos_table = to_talent["talent_positions"]
    to_talent_pos = [to_talent_pos_table["x_pos"], to_talent_pos_table["y_pos"]]

    if to_talent_pos in from_talent_pos_table["connections"]:
        from_talent_pos_table["connections"].remove(to_talent_pos)
        id = from_talent["pos_id"]
        value = from_talent_pos_table["connections"]
    elif from_talent_pos in to_talent_pos_table["connections"]:
        to_talent_pos_table["connections"].remove(from_talent_pos)
        id = to_talent["pos_id"]
        value = to_talent_pos_table["connections"]
    else:
        from_talent_pos_table["connections"].append(to_talent_pos)
        id = from_talent["pos_id"]
        value = from_talent_pos_table["connections"]
        print(from_talent["name"])
        print(from_talent_pos)
        print(to_talent["name"])
        print(to_talent_pos)

    supa.update_database(table="talent_positions", id=id, column="connections", value=value)