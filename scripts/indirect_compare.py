import math

def bucher_indirect(hr_ab: float, hr_bc: float):
    # A vs C through common comparator B
    log_hr_ac = math.log(hr_ab) - math.log(hr_bc)
    return math.exp(log_hr_ac)

if __name__ == "__main__":
    print("Demo indirect HR A vs C:", bucher_indirect(0.72, 0.88))
