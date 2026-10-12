"""Redraw the lecture-board diagrams as standalone PNGs; no LaTeX renderer."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

OUT = Path(__file__).resolve().parents[1] / 'tex' / 'figures' / 'dynamical-systems'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'text.usetex': False, 'font.family': 'DejaVu Serif',
                     'font.size': 13, 'mathtext.fontset': 'dejavuserif'})
INK, CURVE, GUIDE, POINT = '#242b34', '#ad673a', '#397ea4', '#8866ac'

def arrow(ax, xy, end, color=CURVE, lw=1.3):
    ax.annotate('', xy=end, xytext=xy,
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                mutation_scale=14))

def path(ax, x, y, color=CURVE, at=(.55,), lw=1.5):
    ax.plot(x, y, color=color, lw=lw)
    for f in at:
        i = int(f * (len(x)-1))
        j = min(i + max(2, len(x)//28), len(x)-1)
        arrow(ax, (x[i], y[i]), (x[j], y[j]), color, lw)

def save(fig, name):
    fig.savefig(OUT / name, dpi=260, bbox_inches='tight', pad_inches=.14,
                facecolor='white')
    plt.close(fig)

def axes(ax, xmax, ymax, xlabel, ylabel):
    ax.set(xlim=(-.35, xmax+.35), ylim=(-.42, ymax+.35))
    ax.axis('off')
    arrow(ax, (0,0), (xmax,0), INK)
    arrow(ax, (0,0), (0,ymax), INK)
    ax.text(xmax+.1, -.07, xlabel, fontsize=16)
    ax.text(-.1, ymax+.12, ylabel, fontsize=16)

def one_dimensional():
    fig, ax = plt.subplots(figsize=(8,3.25))
    ax.set(xlim=(-1.12,5.6), ylim=(-1.9,1.9))
    ax.axis('off')
    arrow(ax, (0,-1.8), (0,1.72), INK)
    arrow(ax, (0,0), (5.25,0), INK)
    ax.text(5.35,-.13,'$t$',fontsize=16)
    ax.text(-.22,1.75,'$x$',fontsize=16)
    for value in (-1,1):
        ax.plot([0,5.05],[value,value], '--', color=GUIDE, lw=1, dashes=(7,6))
        ax.text(-.2,value-.06,f'${value}$',ha='right')
    ax.text(-.22,.06,'$0$',ha='right')
    ax.text(-.75,1.75,'$x(1-x^2)$',ha='center',color=CURVE)
    for y,s in [(1.42,'-'),(1,'0'),(.5,'+'),(0,'0'),(-.5,'-'),(-1,'0'),(-1.48,'+')]:
        ax.text(-.75,y,f'${s}$',ha='center',va='center',color=CURVE,fontsize=16)
    for start in (0.12,1.75):
        t=np.linspace(0,3.3,400)
        for initial in (.18,1.75,-.18,-1.75):
            y=solve_ivp(lambda t,z:z*(1-z*z), (0,t[-1]), [initial], t_eval=t,
                        rtol=1e-9, atol=1e-11).y[0]
            path(ax,t+start,y,at=(.73,),color=INK)
    save(fig,'one-dimensional.png')

def competition():
    fig,ax=plt.subplots(figsize=(5.2,4.2))
    axes(ax,4.7,4.2,'$r$','$s$')
    for k in (2,3):
        ax.plot([0,k],[k,0],'--',color=GUIDE,lw=1,dashes=(4,6))
        ax.text(-.17,k,f'$(0,{k})$',ha='right',va='center',fontsize=12)
        ax.text(k,-.22,f'$({k},0)$',ha='center',va='top',fontsize=12)
    ax.text(3.28,.7,'$3=r+s$',color=GUIDE,fontsize=12)
    ax.text(.45,-.39,'$2=r+s$',color=GUIDE,fontsize=12)
    def rhs(t,z):
        r,s=z
        return [r*(3-r-s),s*(2-r-s)]
    for p in ((.07,.12),(.15,.7),(.18,1.4),(.3,4.1),(1.3,4.1),(2.3,4.1),(4.5,1.7)):
        sol=solve_ivp(rhs,(0,12),p,t_eval=np.linspace(0,12,1000),rtol=1e-8,atol=1e-10)
        path(ax,*sol.y,at=(.04,.15))
    for a,b in [((0,4),(0,3.3)),((0,.5),(0,1.1)),((.4,0),(1,0)),((4.5,0),(3.85,0))]:
        arrow(ax,a,b)
    for r,s in ((.35,2.9),(.5,1.7),(1.2,2.3),(1.4,1.3),(2.2,.7)):
        v=np.array(rhs(0,(r,s)));v=v/np.linalg.norm(v)*.35
        arrow(ax,(r,s),(r+v[0],s+v[1]),'#558a78')
    ax.scatter([0,0,3],[0,2,0],color=POINT,s=45,zorder=5)
    save(fig,'lotka-volterra.png')

def predator_prey():
    fig,ax=plt.subplots(figsize=(5.1,4.2))
    axes(ax,4.6,4.25,'$s$','$w$')
    # Nondimensional coordinates are used only to reproduce the schematic.
    eq=1.6
    ax.plot([eq,eq],[0,4.05],'--',color=GUIDE,lw=1,dashes=(5,8))
    ax.plot([0,4.25],[eq,eq],'--',color=GUIDE,lw=1,dashes=(5,8))
    for initial in ((1.6,2.05),(1.6,2.8),(1.6,3.8)):
        def rhs(t,z):
            s,w=z
            return [s*(eq-w),w*(s-eq)]
        sol=solve_ivp(rhs,(0,8),initial,max_step=.015,rtol=1e-9,atol=1e-11,
                      events=lambda t,z:z[0]-eq)
        # Stop at the first full return from the upper half of the vertical ray.
        ends=[t for t,z in zip(sol.t_events[0],sol.y_events[0]) if t>1 and z[1]>eq]
        stop=ends[0] if ends else sol.t[-1]
        data=solve_ivp(rhs,(0,stop),initial,t_eval=np.linspace(0,stop,600),rtol=1e-9,atol=1e-11).y
        path(ax,*data,at=(.12,.4,.65,.87))
    ax.scatter([0,eq],[0,eq],color=POINT,s=45,zorder=5)
    ax.text(-.12,eq,'$(0,c/d)$',ha='right',va='center',fontsize=12)
    ax.text(eq,-.23,'$(a/b,0)$',ha='center',va='top',fontsize=12)
    for a,b in [((0,3.7),(0,3.05)),((0,1.1),(0,.4)),((.35,0),(1,0)),((2.5,0),(3.2,0))]:
        arrow(ax,a,b)
    save(fig,'predator-prey.png')

def polar_cases():
    fig=plt.figure(figsize=(9,5.7))
    positions=[(.035,.54,.28,.39),(.36,.54,.28,.39),(.685,.54,.28,.39),
               (.12,.045,.33,.4),(.55,.045,.33,.4)]
    titles=[r'$\varepsilon=0$',r'$\varepsilon>0,\ \mu\leq0$',r'$\varepsilon<0,\ \mu\leq0$',
            r'$\varepsilon>0,\ \mu>0$',r'$\varepsilon<0,\ \mu>0$']
    for k,(pos,title) in enumerate(zip(positions,titles)):
        ax=fig.add_axes(pos);ax.axis('off');ax.set_aspect('equal')
        ax.set(xlim=(-2.1,2.1),ylim=(-2.05,2.05))
        ax.set_title(title,fontsize=15,pad=5)
        ax.scatter([0],[0],s=25,color=POINT if k else INK,zorder=5)
        if k==0:
            th=np.linspace(0,2*np.pi,500)
            for r in (.7,1.55): path(ax,r*np.cos(th),r*np.sin(th),at=(.05,.45))
        elif k in (1,2):
            th=np.linspace(0,4.6*np.pi,700)
            rr=1.8*np.exp(-.17*th) if k==1 else .15*np.exp(.17*th)
            path(ax,rr*np.cos(th),rr*np.sin(th),at=(.18,.5,.82))
        else:
            th=np.linspace(0,2*np.pi,500)
            ax.plot(np.cos(th),np.sin(th),color=POINT,lw=1.7)
            if k==3:
                theta=np.linspace(0,4.7*np.pi,700)
                for r,phase in [(1+.9*np.exp(-.23*theta),.2),
                                (1-.86*np.exp(-.17*theta),2.0)]:
                    path(ax,r*np.cos(theta+phase),r*np.sin(theta+phase),at=(.13,.42,.78))
                ax.annotate(r'$r=\sqrt{\mu}$',xy=(-.75,.66),xytext=(-2,1.5),
                            color=POINT,fontsize=12,arrowprops=dict(arrowstyle='-',color=POINT))
            else:
                theta=np.linspace(0,4.5*np.pi,700)
                r=.88*np.exp(-.16*theta)
                path(ax,r*np.cos(theta+1.2),r*np.sin(theta+1.2),at=(.15,.45,.8))
                theta=np.linspace(0,1.4*np.pi,400);r=1.06+.12*theta**1.25
                path(ax,r*np.cos(theta+1.7),r*np.sin(theta+1.7),at=(.18,.63,.9))
    save(fig,'polar-cases.png')

if __name__=='__main__':
    one_dimensional();competition();predator_prey();polar_cases()
    print(f'Created four diagrams in {OUT}')
