import numpy as np, subprocess, sys
from scipy.signal import butter, sosfilt, find_peaks
def load(p,t0,t1,sr=22050):
    b=subprocess.run(["ffmpeg","-v","error","-ss",str(t0),"-t",str(t1-t0),"-i",p,"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b,np.float32),sr
p=sys.argv[1]
for t0,t1 in [(52,58),(92,98),(140,146),(165,171)]:
    x,sr=load(p,t0,t1)
    hop=int(sr*0.01)
    def env(lo,hi):
        sos=butter(4,[lo,hi],btype='band',fs=sr,output='sos'); y=sosfilt(sos,x)
        e=np.sqrt(np.convolve(y**2,np.ones(hop)/hop,'same'))[::hop]
        d=np.maximum(np.diff(e,prepend=e[0]),0); return d/(d.max()+1e-9)
    lo=env(35,110); sn=env(1500,5000); hh=env(7000,10500)
    print(f"--- {t0}-{t1}s")
    for name,e in [("kick 35-110",lo),("snare 1.5-5k",sn),("hat 7-10.5k",hh)]:
        pk,_=find_peaks(e,height=0.35,distance=8)
        print(f"{name}: "+" ".join(f"{t0+i*0.01:.2f}" for i in pk))
