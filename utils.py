def clamp(v, b_thresh, t_thresh):
    return max(min(v, t_thresh), b_thresh)

def point_rect_col(point, rect):
    return (rect[0]<point[0] and point[0]<rect[0]+rect[2] and rect[1]<point[1] and point[1]<rect[1]+rect[3])

def update_and_remove(list_ref, dt):
    for i in range(len(list_ref)-1,-1,-1):
        item=list_ref[i]
        item.update(dt)
        if item.is_dead:list_ref.pop(i)
