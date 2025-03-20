
def get_t(step_per_revolution, period):
    return float((30*period))/step_per_revolution

def get_step_per_minute(step_per_revolution):
    return  int(step_per_revolution/60)
