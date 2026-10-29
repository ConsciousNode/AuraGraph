import sys, numpy as np, subprocess
sys.path.insert(0, "/home/claude/claude-persistant-1/tools/auragraph")
import proto as P
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.ndimage import median_filter
L, R = P.decode(sys.argv[1]); t0, t1 = float(sys.argv[2]), float(sys.argv[3])
mid = (L + R) / 2
f, t, M = P.spec(mid); c, idx = P.logbands(f); B = P.tobands(M, idx); ref = np.percentile(B, 99.5)
H = median_filter(B, size=(1, 17)); Pp = median_filter(B, size=(17, 1)); mh = H**2/(H**2+Pp**2+1e-20)
sel = (t >= t0) & (t < t1)
fig, ax = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
for a_, D, lab in ((ax[0], B, "full"), (ax[1], B*mh, "sustained"), (ax[2], B*(1-mh), "transient")):
    a_.imshow(np.clip(P.db(D[:, sel], ref), -80, 0), origin="lower", aspect="auto", extent=[t0, t1, 0, P.NBANDS], cmap="magma", vmin=-80, vmax=0)
    a_.set_ylabel(lab)
ax[2].set_xticks(np.arange(t0, t1 + 0.01, 0.25)); ax[2].tick_params(labelsize=6)
fig.savefig(sys.argv[4], bbox_inches="tight")
