import random, sys
random.seed(7)
W = H = 128
grid = [[None]*W for _ in range(H)]
PAL = {
 'B':'#070a06',  # background
 'd':'#1d3a16',  # dark green outline
 'g':'#3f8f2e',  # pepe green
 'h':'#5fb445',  # highlight green
 'G':'#2a6a20',  # mid green shade
 'w':'#f2f3e4',  # eye white
 'k':'#0a0a0a',  # black
 'l':'#b57a2b',  # lip gold-brown
 'L':'#7a4c17',  # lip dark
 'y':'#f0c232',  # gold
 'Y':'#a67f14',  # dark gold
 's':'#1a2416',  # scaffold dark
 'o':'#c9a227',  # gold dim (sparkle)
 't':'#132a12',  # subtle grid tone
}
def put(x,y,c):
    if 0<=x<W and 0<=y<H: grid[y][x]=c
def get(x,y):
    return grid[y][x] if 0<=x<W and 0<=y<H else None

# --- background subtle dither
for y in range(H):
    for x in range(W):
        grid[y][x]='B'
for _ in range(420):
    put(random.randrange(W),random.randrange(H),'t')
for _ in range(60):
    put(random.randrange(W),random.randrange(H),'o' if random.random()<0.4 else 'Y')

# --- Pepe head, procedural pixel art
cx,cy=64,62
def ell(cx,cy,rx,ry):
    s=set()
    for y in range(int(cy-ry)-1,int(cy+ry)+2):
        for x in range(int(cx-rx)-1,int(cx+rx)+2):
            if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1.0: s.add((x,y))
    return s
head=set()
head |= ell(cx,cy+2,24,22)
head |= ell(cx+2,cy-8,20,12)       # brow bulge
head |= ell(cx-14,cy+10,12,9)      # jaw left
head = {(x,y) for (x,y) in head if y<=cy+22}
for (x,y) in head: put(x,y,'g')
def outline(region,col):
    for (x,y) in region:
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            if (x+dx,y+dy) not in region: put(x,y,col)
outline(head,'d')
for (x,y) in head:
    if y>cy+14 and get(x,y)=='g' and (x+y)%2==0 and (x,y+4) not in head: put(x,y,'G')
for x in range(cx-14,cx-4): put(x,cy-14,'h')
for x in range(cx-18,cx-10): put(x,cy-11,'h')
for x in range(cx-20,cx-16): put(x,cy-7,'h')

# eyes: big whites with heavy lids, pepe style
def eye(ex,ey,rx,ry,px,py):
    e=ell(ex,ey,rx,ry)
    for (x,y) in e: put(x,y,'w')
    lid={(x,y) for (x,y) in e if y<=ey-1}
    for (x,y) in lid: put(x,y,'g')
    vis=e-lid
    for (x,y) in vis:
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            if (x+dx,y+dy) not in vis: put(x,y,'d')
    for (x,y) in lid:
        if (x,y+1) in vis: put(x,y,'d'); put(x,y-1,'d')
    for yy in range(py-1,py+2):
        for xx in range(px-2,px+2): put(xx,yy,'k')
    put(px-1,py-1,'w')
eye(cx-9,cy-5,10,6,cx-6,cy-2)
eye(cx+11,cy-7,10,6,cx+13,cy-4)

# mouth: thin upper lip, thick lower lip, frown at corners
mouth=set(); lower=set()
for x in range(cx-19,cx+15):
    t=(x-(cx-2))/17.0
    top=cy+8+int(2.2*t*t)
    for y in range(top,top+2): mouth.add((x,y))
    for y in range(top+2,top+6-(1 if abs(t)>0.8 else 0)): lower.add((x,y))
for (x,y) in mouth: put(x,y,'l')
for (x,y) in lower: put(x,y,'L')
for (x,y) in lower:
    if (x,y-1) in mouth: put(x,y,'l')
lips=mouth|lower
outline(lips,'L')
for (x,y) in lips:
    if (x,y-1) not in lips: put(x,y-1,'d')
for x in range(cx-13,cx+5):
    put(x,cy+17+int(((x-(cx-4))/9.0)**2),'d')
for x in range(cx-6,cx+2): put(x,cy+3,'d')
for x in range(cx+6,cx+16): put(x,cy+2,'d')

# --- "under construction": lower-right of pepe is still being assembled
unbuilt=set()
for (x,y) in head:
    if x>cx and y>cy+2:
        prob=min(1.0,((x-cx)+(y-(cy+2)))/22.0)
        if random.random()<prob: unbuilt.add((x,y))
for (x,y) in unbuilt:
    put(x,y,'s' if (x%2==0 and y%2==0) else 'B')
for (x,y) in unbuilt:
    edge=any((x+dx,y+dy) not in head for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
    if edge and (x+y)%2==0: put(x,y,'Y')
    elif x%8==4 or y%8==4: put(x,y,'Y' if (x+y)%2==0 else 's')
for (x,y) in unbuilt:
    if random.random()<0.07: put(x,y,'y')

# --- gold frame border
for i in range(W):
    for c in (0,W-1):
        put(i,c,'Y'); put(c,i,'Y')
    if i%4<2:
        put(i,1,'y'); put(i,W-2,'y'); put(1,i,'y'); put(W-2,i,'y')

# --- tiny pixel font (3x5, W and M are 5 wide)
FONT={
'S':["111","100","111","001","111"],'W':["10001","10001","10101","10101","01010"],
'A':["010","101","111","101","101"],'R':["110","101","110","101","101"],
'M':["10001","11011","10101","10001","10001"],'P':["111","101","111","100","100"],
'E':["111","100","110","100","111"],' ':["000","000","000","000","000"],
'B':["110","101","110","101","110"],'U':["101","101","101","101","111"],
'I':["111","010","010","010","111"],'L':["100","100","100","100","111"],
'D':["110","101","101","101","110"],'N':["110","101","101","101","101"],
'G':["111","100","101","101","111"],'T':["111","010","010","010","010"],
'0':["111","101","101","101","111"],'1':["010","110","010","010","111"],
'2':["111","001","111","100","111"],'3':["111","001","111","001","111"],
'4':["101","101","111","001","001"],'5':["111","100","111","001","111"],
'6':["111","100","111","101","111"],'7':["111","001","001","001","001"],
'8':["111","101","111","101","111"],'9':["111","101","111","001","111"],
}
def textw(s,scale):
    return sum((len(FONT.get(ch,FONT[' '])[0])+1)*scale for ch in s)-scale
def text(s,x0,y0,scale,col,shadow='Y'):
    x=x0
    for ch in s:
        rows=FONT.get(ch,FONT[' '])
        for r,row in enumerate(rows):
            for c,bit in enumerate(row):
                if bit=='1':
                    for dy in range(scale):
                        for dx in range(scale):
                            if shadow: put(x+c*scale+dx+1,y0+r*scale+dy+1,shadow)
                            put(x+c*scale+dx,y0+r*scale+dy,col)
        x+=(len(rows[0])+1)*scale
title="SWARM PEPE"
text(title,(W-textw(title,2))//2,6,2,'y')

# --- agents: tiny 4x4 sprites
SPR = {
 0:[".yy.","ykky",".gg.","g..g"],
 1:[".yy.","ykky",".gg.",".g.g"],
 2:["yyy.","ykky",".gg.","g.g."],
 3:[".yy.","ykky","ygg.","g..g"],   # carrying gold block left
 4:[".yy.","ykky",".ggy","g..g"],   # carrying gold block right
 5:[".y..","ykky",".gg.","g..g"],
}
occupied=set()
built=set(head)-unbuilt
forbidden=set()
for (x,y) in built:
    for dx in range(-1,2):
        for dy in range(-1,2): forbidden.add((x+dx,y+dy))
forbidden-=unbuilt
for x in range(W):
    for y in range(0,20): forbidden.add((x,y))   # title band
    for y in range(H-7,H): forbidden.add((x,y))  # footer band
agents=[]
# a row of agents standing on top of the head
for x in range(cx-18,cx+19,6):
    ytop=min(y for (xx,y) in head if xx==x)
    cells=[(x+dx,ytop-4+dy) for dx in range(0,5) for dy in range(0,4)]
    if any(c in occupied or c in head for c in cells): continue
    for c in cells: occupied.add(c)
    agents.append((x,ytop-4,random.choice([0,1,2,5])))
tries=0
while len(agents)<340 and tries<200000:
    tries+=1
    x=random.randrange(2,W-6); y=random.randrange(2,H-6)
    cells=[(x+dx,y+dy) for dx in range(0,5) for dy in range(0,5)]
    if any(c in forbidden or c in occupied for c in cells): continue
    dist=((x-(cx+16))**2+(y-(cy+16))**2)**0.5
    if random.random()>max(0.6,1.0-dist/150.0): continue
    for c in cells: occupied.add(c)
    v=random.choice([3,4,3,4,0,1]) if dist<30 else random.choice([0,1,2,5,3,4])
    agents.append((x,y,v))
# gold "data stream" trails from some agents into the unbuilt zone
ub=sorted(unbuilt)
for (ax,ay,v) in agents:
    if random.random()<0.22 and ub:
        tx,ty=random.choice(ub)
        n=max(abs(tx-ax),abs(ty-ay))
        for i in range(0,n,3):
            px=ax+2+(tx-ax)*i//n; py=ay+2+(ty-ay)*i//n
            if get(px,py)=='B' and (px,py) not in occupied: put(px,py,'y' if i%6==0 else 'o')

for (ax,ay,v) in agents:
    for r,row in enumerate(SPR[v]):
        for c,ch in enumerate(row):
            if ch!='.': put(ax+c,ay+r,ch)
cap=f"{len(agents)} AGENTS BUILDING"
text(cap,(W-textw(cap,1))//2,H-7,1,'y',shadow=None)

# --- emit SVG: one path per color (run-length rows), <use> per agent
paths={}
for y in range(H):
    x=0
    while x<W:
        c=grid[y][x]
        if c=='B': x+=1; continue
        x0=x
        while x<W and grid[y][x]==c: x+=1
        paths.setdefault(c,[]).append(f"M{x0} {y}h{x-x0}")
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="1024" height="1024" shape-rendering="crispEdges">']
out.append(f'<rect width="{W}" height="{H}" fill="{PAL["B"]}"/>')
out.append('<g fill="none" stroke-width="1" transform="translate(0,.5)">')
for c,segs in paths.items():
    out.append(f'<path stroke="{PAL[c]}" d="{"".join(segs)}"/>')
out.append('</g></svg>')
svg="\n".join(out)
open(sys.argv[1],'w').write(svg)
print("agents",len(agents),"svg chars",len(svg),"unbuilt",len(unbuilt))
