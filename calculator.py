
def get_t(step_per_minute, period):
    return 30*period/step_per_minute

def get_step_per_minute(step_per_revolution):
    return  int(step_per_revolution/60)
