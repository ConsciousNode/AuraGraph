#!/usr/bin/env python3
"""AuraGraph inversion sweep (Kehai, 2026-10-29): render a tile at a given resolution,
rebuild audio from it with Griffin-Lim, and score how much melody and rhythm come back.
usage: invert_sweep.py TRACK [TRACK...]  (first 15 s of each)"""
import sys,subprocess,numpy as np,itertools,json
from scipy.signal import stft,istft
SR,NFFT,HOP=22050,2048,512; FMIN,FMAX=30.0,11000.0
def load(p):
    b=subprocess.run(["ffmpeg","-v","error","-t","15","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b,np.float32).copy()
def chroma(s):
    ff,tt,S=stft(s,fs=SR,nperseg=4096,noverlap=4096-HOP); S=np.abs(S); ok=(ff>60)&(ff<4000)
    pc=np.round(12*np.log2(ff[ok]/440)).astype(int)%12; C=np.zeros((12,S.shape[1]))
    for p in range(12): C[p]=S[ok][pc==p].sum(0)
    return C/(C.sum(0)+1e-9)
def onset(s):
    _,_,S=stft(s,fs=SR,nperseg=1024,noverlap=1024-HOP); L=np.log(np.abs(S)+1e-6)
    return np.maximum(np.diff(L,axis=1),0).sum(0)
def rebuild(x,nb,W,bits,iters=60):
    f,t,Z=stft(x,fs=SR,nperseg=NFFT,noverlap=NFFT-HOP); M=np.abs(Z)
    edges=np.geomspace(FMIN,FMAX,nb+1); centers=np.sqrt(edges[:-1]*edges[1:])
    bi=np.clip(np.searchsorted(edges,f)-1,0,nb-1)
    B=np.stack([M[bi==k].mean(0) if (bi==k).any() else M[np.argmin(abs(f-centers[k]))] for k in range(nb)])
    ref=np.percentile(B,99.5); D=20*np.log10(np.maximum(B,1e-10)/ref)
    L=2**bits-1; q=np.round((np.clip(D,-80,0)+80)/80*L)/L*80-80
    T=q.shape[1]; W=min(W,T)
    # downsample time by averaging into W columns, then hold
    seg=np.linspace(0,T,W+1).astype(int); qs=np.stack([q[:,a:b].mean(1) for a,b in zip(seg[:-1],seg[1:])],1)
    col=np.minimum(np.searchsorted(seg[1:],np.arange(T),side='right'),W-1); q=qs[:,col]
    mag=10**(q[bi]/20)*ref
    ph=np.exp(2j*np.pi*np.random.default_rng(0).random(mag.shape))
    for _ in range(iters):
        _,y=istft(mag*ph,fs=SR,nperseg=NFFT,noverlap=NFFT-HOP)
        _,_,Z2=stft(y,fs=SR,nperseg=NFFT,noverlap=NFFT-HOP); ph=np.exp(1j*np.angle(Z2[:,:T]))
    _,y=istft(mag*ph,fs=SR,nperseg=NFFT,noverlap=NFFT-HOP); return y/np.abs(y).max()*0.9
def score(x,y):
    n=min(len(x),len(y)); x,y=x[:n],y[:n]; cx,cy=chroma(x),chroma(y)
    pc=np.mean(cx.argmax(0)==cy.argmax(0))
    sh=np.roll(cy,cy.shape[1]//2,axis=1); base=np.mean(cx.argmax(0)==sh.argmax(0))
    ox,oy=onset(x),onset(y); m=min(len(ox),len(oy)); oc=np.corrcoef(ox[:m],oy[:m])[0,1]
    return pc,base,oc
if __name__=="__main__":
    tracks=sys.argv[1:]; X={t.split('/')[-1][:12]:load(t) for t in tracks}
    res=[]
    for nb,W,bits in [(160,1000,8),(160,1000,3),(80,1000,8),(40,1000,8),(24,1000,8),(12,1000,8),(160,250,8),(160,100,8),(160,50,8),(160,25,8),(40,100,8),(24,100,4),(12,50,4)]:
        r=[score(x,rebuild(x,nb,W,bits)) for x in X.values()]
        a=np.mean(r,0); res.append((nb,W,bits,*a)); print("bands %3d  px %4d  bits %d | melody %.2f (chance %.2f)  rhythm %.2f"%(nb,W,bits,*a),flush=True)
    json.dump(res,open('/tmp/sweep/res.json','w'))
