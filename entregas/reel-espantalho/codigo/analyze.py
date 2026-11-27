import cv2, numpy as np, sys, glob, os
S=sys.argv[1]
for f in sorted(glob.glob(S+'/src/*.png')):
    im=cv2.imread(f); lab=cv2.cvtColor(im,cv2.COLOR_BGR2LAB).astype(np.float32)
    h,w=im.shape[:2]
    # background estimate: median of mid-left strip region likely paper
    samp=lab[int(h*0.02):int(h*0.98), int(w*0.01):int(w*0.04)].reshape(-1,3)
    bg=np.median(samp,axis=0)
    d=np.linalg.norm(lab-bg,axis=2)
    m=(d>38).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    cv2.imwrite(S+'/work/mask_'+os.path.basename(f),m*255)
    rows=m[:, int(w*0.05):int(w*0.95)].sum(1)
    on=rows>w*0.01
    bands=[];start=None
    for y,v in enumerate(on):
        if v and start is None: start=y
        if not v and start is not None:
            if y-start>8: bands.append((start,y))
            start=None
    if start is not None: bands.append((start,h))
    print(os.path.basename(f), 'bg',bg.round(), bands)
