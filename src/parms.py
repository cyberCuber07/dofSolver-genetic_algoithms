from numpy import array, pi, zeros

LINKS = array([310, 170, 230, 147])
# ================================================
# angles
ANG_LIMITS = array([[30, 120],
                    [80, 270],
                    [80, 270],
                    [90, 270]])
tmp = zeros(ANG_LIMITS.shape)
for i in range(ANG_LIMITS.shape[0] - 1):
    tmp[i + 1, 0] = (ANG_LIMITS[i + 1, 0] - 180) * pi / 180
    tmp[i + 1, 1] = (ANG_LIMITS[i + 1, 1] - 180) * pi / 180
tmp[0, 0] = ANG_LIMITS[0, 0] * pi / 180
tmp[0, 1] = ANG_LIMITS[0, 1] * pi / 180
ANG_LIMITS = tmp
ANG_LIMITS[0, 0] = 10 * pi / 180
print(ANG_LIMITS)
# SS = [1, -1, -1, -1] # simpler version
SS = [1, 1, 1, 1]
# ================================================

N = LINKS.shape[0]
N_SETS = 1 * 10 ** 2
N_PARENTS = int(N_SETS * 0.2)
N_CROSSOVER = N_SETS - N_PARENTS
CROSSOVER_POINT = N // 2
N_MUTATIONS = 1

ITER = 2 * 10 ** 1
# MUTE_PER == 5 * 10 ** -1 resulted in fast convergence
MUTE_PER = 5 * 10 ** -1

SAVE_DIR = "data"
CSV_NAME = "history"

TARGET = array([500, 200, -50])
# TARGET = array([400, -400])

# robots cover boundaries
BOUND = [[-270, 650],       # OX
         [-380, 450],       # OY
         [60 - 420, 0]]    # OZ
BOUND = [[i - 50, j + 50] for (i, j) in BOUND]
BOUND = array(BOUND)
# =========================================
# NOTICE
# notice that height  on OZ is 60, so bound on OZ should be [60, -360],
# but then change the "check_bound"'s "check_one" methods for loop
# =========================================
