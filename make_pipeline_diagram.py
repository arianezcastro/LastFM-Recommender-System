"""Draw the methodology pipeline diagram (Figure 1) as pipeline.png.

Run from the project folder:  python make_pipeline_diagram.py
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

INK = '#0b0b0b'      # primary text
MUTED = '#52514e'    # arrows and secondary text
STAGES = {           # stage name: (fill, border)
    'Data preparation': ('#d6e6f9', '#2a78d6'),
    'Pattern mining': ('#fbe1d6', '#eb6834'),
    'Recommendation and evaluation': ('#d1f0e4', '#1baf7a'),
}

BOX_W, BOX_H = 3.35, 1.55
COLUMNS = [0.2, 4.1, 8.0, 11.9]  # left edge of each column
ROW_TOP, ROW_BOTTOM = 3.6, 0.4   # bottom edge of each row

# (title, detail lines, stage, column, row)
BOXES = [
    ('1  Load data',
     ['Last.fm HetRec 2011:', 'user_artists, artists, tags',
      '(Section 6)'],
     'Data preparation', 0, ROW_TOP),
    ('2  Explore and check',
     ['Nulls, duplicates, support', 'distribution, minsup range',
      '(Section 7)'],
     'Data preparation', 1, ROW_TOP),
    ('3  Build transactions',
     ['One set of top-50 artists per', 'user: N = 1,892, d = 17,632',
      '(Sections 8.1 and 8.2)'],
     'Data preparation', 2, ROW_TOP),
    ('4  Split users',
     ['70% train, 15% validation,', '15% test; hide 20% of each',
      "evaluation user's artists (8.3)"],
     'Data preparation', 3, ROW_TOP),
    ('5  Mine itemsets',
     ['Apriori vs FP-Growth on the', 'training users; choose minsup',
      '(Section 9)'],
     'Pattern mining', 0, ROW_BOTTOM),
    ('6  Generate rules',
     ['A → B with support,', 'confidence, and lift',
      '(Section 10)'],
     'Pattern mining', 1, ROW_BOTTOM),
    ('7  Recommend artists',
     ['Fire rules with A ⊆ visible', 'artists, rank top-k, popular',
      'fallback (Section 11)'],
     'Recommendation and evaluation', 2, ROW_BOTTOM),
    ('8  Tune, then test',
     ['Tune on validation users;', 'compare with popularity',
      'on test users (Section 12)'],
     'Recommendation and evaluation', 3, ROW_BOTTOM),
]


def draw_box(ax, title, detail, stage, column, bottom):
    """Draw one pipeline step as a rounded box with a title and detail."""
    fill, border = STAGES[stage]
    left = COLUMNS[column]
    ax.add_patch(FancyBboxPatch(
        (left, bottom), BOX_W, BOX_H,
        boxstyle='round,pad=0.02,rounding_size=0.12',
        facecolor=fill, edgecolor=border, linewidth=1.5))
    ax.text(left + 0.15, bottom + BOX_H - 0.18, title, ha='left', va='top',
            fontsize=10, fontweight='bold', color=INK)
    ax.text(left + 0.15, bottom + BOX_H - 0.52, '\n'.join(detail),
            ha='left', va='top', fontsize=8.2, color=INK, linespacing=1.35)


def arrow(ax, start, end, style='-'):
    """Draw an arrow from start to end."""
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle='-|>', mutation_scale=12, color=MUTED,
        linewidth=1.3, linestyle=style, shrinkA=0, shrinkB=0))


def main():
    """Build the figure and save it next to the notebook."""
    fig, ax = plt.subplots(figsize=(11.2, 4.4), dpi=200)
    ax.set_xlim(0, 15.5)
    ax.set_ylim(0.2, 5.75)
    ax.axis('off')

    for title, detail, stage, column, bottom in BOXES:
        draw_box(ax, title, detail, stage, column, bottom)

    # Left-to-right arrows within each row
    for row_bottom in (ROW_TOP, ROW_BOTTOM):
        middle = row_bottom + BOX_H / 2
        for column in range(3):
            arrow(ax, (COLUMNS[column] + BOX_W + 0.05, middle),
                  (COLUMNS[column + 1] - 0.05, middle))

    # Training transactions wrap from step 4 down to step 5
    gap_y = (ROW_TOP + ROW_BOTTOM + BOX_H) / 2
    split_x = COLUMNS[3] + 0.8
    mine_x = COLUMNS[0] + BOX_W / 2
    ax.plot([split_x, split_x, mine_x], [ROW_TOP - 0.05, gap_y, gap_y],
            color=MUTED, linewidth=1.3)
    arrow(ax, (mine_x, gap_y), (mine_x, ROW_BOTTOM + BOX_H + 0.05))
    ax.text((mine_x + split_x) / 2, gap_y + 0.17,
            '1,330 training transactions', fontsize=8.4, color=MUTED,
            ha='center', va='center', style='italic')

    # Validation and test users go straight to the evaluation step
    eval_x = COLUMNS[3] + 1.9
    arrow(ax, (eval_x, ROW_TOP - 0.05), (eval_x, ROW_BOTTOM + BOX_H + 0.05),
          style='--')
    ax.text(eval_x + 0.12, gap_y, 'validation and\ntest users',
            fontsize=8.4, color=MUTED, ha='left', va='center',
            style='italic')

    # Stage legend
    for i, (stage, (fill, border)) in enumerate(STAGES.items()):
        x = 0.2 + i * 4.6
        ax.add_patch(FancyBboxPatch(
            (x, 5.35), 0.32, 0.22,
            boxstyle='round,pad=0.01,rounding_size=0.05',
            facecolor=fill, edgecolor=border, linewidth=1.2))
        ax.text(x + 0.45, 5.46, stage, va='center', fontsize=9.5, color=INK)

    fig.savefig('pipeline.png', bbox_inches='tight', facecolor='white')
    print('Saved pipeline.png')


if __name__ == '__main__':
    main()
