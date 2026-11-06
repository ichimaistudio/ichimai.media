import numpy as np, wave, sys
sr=44100; dur=float(sys.argv[2]); out=sys.argv[1]
pops=[float(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else []
t=np.arange(int(sr*dur))/sr; y=np.zeros_like(t)
def note(f,st,ln,amp):
    i0=int(st*sr); n=int(ln*sr); tt=np.arange(n)/sr
    env=np.exp(-tt*3.2)*(1-np.exp(-tt*200))
    w=(np.sin(2*np.pi*f*tt)+.35*np.sin(4*np.pi*f*tt)+.12*np.sin(6*np.pi*f*tt))*env*amp
    e=min(len(y),i0+n); y[i0:e]+=w[:e-i0]
m=lambda k:440*2**((k-69)/12)
chords=[[60,64,67,71],[57,60,64,67],[53,57,60,64],[55,59,62,65]]  # Cmaj7 Am7 Fmaj7 G7
beat=60/92
b=0
while b*beat<dur:
    ch=chords[(b//8)%4]
    if b%8==0: note(m(ch[0]-12),b*beat,beat*8,.22)
    note(m(ch[[0,1,2,3,2,1,2,3][b%8]]+12),b*beat,beat*2,.10)
    b+=1
for p in pops: note(1320,p,.25,.08); note(1980,p+.03,.2,.04)
d=int(.23*sr); yy=y.copy(); yy[d:]+=.35*y[:-d]; d2=int(.41*sr); yy[d2:]+=.2*y[:-d2]
fade=np.ones_like(t); fi=int(.4*sr); fo=int(1.5*sr); fade[:fi]=np.linspace(0,1,fi); fade[-fo:]=np.linspace(1,0,fo)
yy*=fade; yy=yy/np.max(np.abs(yy))*.6
s=(np.stack([yy,yy],1)*32767).astype(np.int16)
w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(s.tobytes()); w.close()
