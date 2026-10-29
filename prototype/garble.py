import numpy as np, subprocess
sr=22050
def seg(t0,t1):
    b=subprocess.run(["ffmpeg","-v","error","-ss",str(t0),"-t",str(t1-t0),"-i","mystery.mp3","-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b,np.float32)
def stats(t0,t1,lo=200,hi=1200):
    x=seg(t0,t1); n=2048; hop=int(sr*0.02); w=np.hanning(n)
    f=np.fft.rfftfreq(n,1/sr); band=(f>lo)&(f<hi)
    S=np.array([20*np.log10(np.abs(np.fft.rfft(x[i:i+n]*w))[band]+1e-9) for i in range(0,len(x)-n,hop)])
    W=S-np.median(S,axis=0)              # whiten each frequency row over the window
    k=W.argmax(1); prom=W.max(1); fr=f[band][k]
    voiced=prom>12                        # a clear line stands out of the bed
    st=12*np.log2(fr/440)
    # continuous runs: voiced frames whose pitch moves < 1 semitone from the previous frame
    runs=[];r=0
    for i in range(1,len(st)):
        if voiced[i] and voiced[i-1] and abs(st[i]-st[i-1])<1: r+=1
        else:
            if r: runs.append(r)
            r=0
    if r: runs.append(r)
    runs=np.array(runs)*0.02
    jumps=np.abs(np.diff(st))[voiced[1:]&voiced[:-1]]
    return dict(voiced=voiced.mean(), prom=np.median(prom[voiced]) if voiced.any() else 0,
                run_med=np.median(runs) if len(runs) else 0, run_p90=np.percentile(runs,90) if len(runs) else 0,
                long_runs=(runs>=0.3).sum()/((t1-t0)/10), jump_frac=(jumps>2).mean())
for name,(a,b) in {"bridge (garbled) 1:55-2:13":(115,133),"verse sung 2:30-2:37":(150,157),"sung 1:43-1:53":(103,113),"sung 2:40-2:49":(160,169)}.items():
    s=stats(a,b); print(f"{name:28s} voiced {s['voiced']:.2f} | line prominence {s['prom']:.1f} dB | run median {s['run_med']:.2f}s p90 {s['run_p90']:.2f}s | runs>=0.3s per 10s {s['long_runs']:.1f} | pitch jumps>2st {s['jump_frac']:.2f}")
