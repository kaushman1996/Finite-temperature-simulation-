import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as patches

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 20
})

LX = 24
LY = 24

# triangular lattice vectors
a1 = np.array([1, 0])
a2 = np.array([0.5, np.sqrt(3)/2])

points = []
index_pos = {}
index = 0

for i in range(LY):
    for j in range(LX):
        r = j*a1 + i*a2
        index_pos[index] = r
        index += 1

# sites where we place blue dots

blue_sites = {0, 3, 6, 9, 12, 15, 18, 21, 25, 28, 31, 34, 37, 40, 43, 46, 50, 53, 
56, 59, 62, 65, 68, 71, 72, 75, 78, 81, 84, 87, 90, 93, 97, 100, 103, 
106, 109, 112, 115, 118, 122, 125, 128, 131, 134, 137, 140, 143, 144, 
147, 150, 153, 156, 159, 162, 165, 169, 172, 175, 178, 181, 184, 187, 
190, 194, 197, 200, 203, 206, 209, 212, 215, 216, 219, 222, 225, 228, 
231, 234, 237, 241, 244, 247, 250, 253, 256, 259, 262, 266, 269, 272, 
275, 278, 281, 284, 287}
red_sites = {289, 292, 295, 298, 301, 304, 307, 310, 314, 317, 320, 323, 326, 329, 
332, 335, 339, 342, 345, 348, 351, 354, 357, 336, 361, 364, 367, 370, 
373, 376, 379, 382, 386, 389, 392, 395, 398, 401, 404, 407, 411, 414, 
417, 420, 423, 426, 429, 408, 433, 436, 439, 442, 445, 448, 451, 454, 
458, 461, 464, 467, 470, 473, 476, 479, 483, 486, 489, 492, 495, 498, 
501, 480, 505, 508, 511, 514, 517, 520, 523, 526, 530, 533, 536, 539, 
542, 545, 548, 551, 555, 558, 561, 564, 567, 570, 573,552
} 
fig, ax = plt.subplots(figsize=(8,8))

for idx, pos in index_pos.items():

    if idx in blue_sites:
        ax.plot(pos[0], pos[1],
                marker='o',
                color='dodgerblue',
                markersize=14)

    elif idx in red_sites:
        ax.plot(pos[0], pos[1],
                marker='o',
                color='red',
                markersize=14)

    else:
        ax.plot(pos[0], pos[1],
                marker='*',
                color='black',
                markersize=8)

# -------- draw red bond between sites 28 and 29 --------
dimers = [(266, 266+23), (269,269+23), (272,272+23),(275,275+23),(278,278+23),(281,281+23),(284,284+23),(287,287+23)]#,(290,290+23)]92,287,

for i,j in dimers:
    p1 = index_pos[i]
    p2 = index_pos[j]
    ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color='green',lw=3)
# ------------------------------------------------------
# --------------------------------------------------
# -------- draw arrows from site 245 to given sites --------
arrow_targets = [252, 227, 251, 229, 204,205]

start = index_pos[228]

for t in arrow_targets:
    end = index_pos[t]
    ax.annotate(
        '',
        xy=(end[0], end[1]),
        xytext=(start[0], start[1]),
        arrowprops=dict(
            arrowstyle='->',
            color='purple',
            lw=2
        )
    )

arrow_targets = [319, 318,296,271]

start = index_pos[295]

for t in arrow_targets:
    end = index_pos[t]
    ax.annotate(
        '',
        xy=(end[0], end[1]),
        xytext=(start[0], start[1]),
        arrowprops=dict(
            arrowstyle='->',
            color='magenta',
            lw=2
        )
    )

arrow_targets = [294]

start = index_pos[295]

for t in arrow_targets:
    end = index_pos[t]
    ax.annotate(
        '',
        xy=(end[0], end[1]),
        xytext=(start[0], start[1]),
        arrowprops=dict(
            arrowstyle='->',
            color='orange',
            lw=2
        )
    )


# ---------------------------------------------------------
ax.set_aspect('equal')
ax.axis('off')
ax.set_aspect('equal')
ax.axis('off')

# zoom region
ax.set_xlim(9.5,20.3)
ax.set_ylim(6,14.2)

"""x1, x2 = 9.5, 20
y1, y2 = 6, 14

# Draw rectangle on the FULL plot (before zooming)
rect = patches.Rectangle(
    (x1, y1),            # bottom-left corner
    x2 - x1,             # width
    y2 - y1,             # height
    linewidth=2,
    edgecolor='green',
    facecolor='none'
)
ax.add_patch(rect)

# Now apply zoom
ax.set_xlim(x1, x2)
ax.set_ylim(y1, y2)
"""
ax.set_aspect('equal')
ax.axis('off')
# -------- labels on top of box --------
y_top = 14.2  # slightly above the box

#ax.text(20.2, 10, r'$X_0$', fontsize=22, ha='center')
#ax.text(20, y_top, r'$X_1$', fontsize=22, ha='center')
#ax.text(18.5, y_top, r'$X_2$', fontsize=22, ha='center')




ax.annotate(
    r'$X_0$',
    xy=(12.5, 14.2),       # target
    xytext=(11.0, 14.2),   # text to the right
    ha='center',
    va='center',
    fontsize=22,
    color='orange',
    arrowprops=dict(arrowstyle='->', color='orange', lw=2),
    zorder=10
)

ax.annotate(
    r'$X_1$',
    xy=(15.5, 14.2),       # target
    xytext=(14.0, 14.2),   # text to the right
    ha='center',
    va='center',
    fontsize=22,
    color='magenta',
    arrowprops=dict(arrowstyle='->', color='magenta', lw=2),
    zorder=10
)

ax.annotate(
    r'$X_2$',
    xy=(18.5, 14.2),       # target
    xytext=(17.0, 14.2),   # text to the right
    ha='center',
    va='center',
    fontsize=22,
    color='purple',
    arrowprops=dict(arrowstyle='->', color='purple', lw=2),
    zorder=10
)
# --- small transparent shaded rectangle ---
rect = patches.Rectangle(
    (8.5, 9.1),   # bottom-left corner (adjust as needed)
    12.5,           # width
    1.5,           # height
    linewidth=1.5,
    edgecolor='black',
    facecolor='gray',   # fill color
    alpha=0.3           # transparency (0 = fully transparent, 1 = solid)
)

ax.add_patch(rect)

plt.savefig("domain_wall_zoom.pdf", bbox_inches='tight')
plt.show()
#plt.savefig("domain_wall.pdf")
#plt.show()
