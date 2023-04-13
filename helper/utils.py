def clamp(v, b_thresh, t_thresh):
    return max(min(v, t_thresh), b_thresh)
