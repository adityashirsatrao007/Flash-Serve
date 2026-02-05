import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_naive_batching():
    fig, ax = plt.subplots(figsize=(8, 3))
    
    # Data: (start, duration)
    # User A: 0-10
    # User B: 0-4
    
    # Bars
    ax.broken_barh([(0, 10)], (10, 8), facecolors='#3b82f6') # User A (Blue)
    ax.broken_barh([(0, 4)], (20, 8), facecolors='#3b82f6')  # User B (Blue)
    
    # Wasted Space
    ax.broken_barh([(4, 6)], (20, 8), facecolors='#ef4444', hatch='///') # Waste (Red)
    
    # Labels
    ax.text(5, 14, "User A (Long Request)", color='white', ha='center', va='center', fontweight='bold')
    ax.text(2, 24, "User B", color='white', ha='center', va='center', fontweight='bold')
    ax.text(7, 24, "GPU IDLE (WASTED)", color='white', ha='center', va='center', fontweight='bold')
    
    # Settings
    ax.set_ylim(5, 35)
    ax.set_xlim(0, 11)
    ax.set_xlabel('Time (seconds)')
    ax.set_yticks([14, 24])
    ax.set_yticklabels(['Slot 1', 'Slot 2'])
    ax.set_title("Standard Approach: Static Batching", pad=20)
    
    plt.tight_layout()
    plt.savefig('naive_batching.png', dpi=300)
    plt.close()

def draw_flash_batching():
    fig, ax = plt.subplots(figsize=(8, 3))
    
    # Bars
    ax.broken_barh([(0, 10)], (10, 8), facecolors='#3b82f6') # User A
    ax.broken_barh([(0, 4)], (20, 8), facecolors='#3b82f6')  # User B
    ax.broken_barh([(4, 6)], (20, 8), facecolors='#10b981')  # User C (Green)
    
    # Labels
    ax.text(5, 14, "User A (Long Request)", color='white', ha='center', va='center', fontweight='bold')
    ax.text(2, 24, "User B", color='white', ha='center', va='center', fontweight='bold')
    ax.text(7, 24, "User C (Injected!)", color='white', ha='center', va='center', fontweight='bold')
    
    # Settings
    ax.set_ylim(5, 35)
    ax.set_xlim(0, 11)
    ax.set_xlabel('Time (seconds)')
    ax.set_yticks([14, 24])
    ax.set_yticklabels(['Slot 1', 'Slot 2'])
    ax.set_title("Flash-Serve: Continuous Batching", pad=20)
    
    plt.tight_layout()
    plt.savefig('flash_serve_batching.png', dpi=300)
    plt.close()

def draw_architecture():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Helper to draw box
    def draw_box(x, y, w, h, text, color='#eff6ff', edge='#2563eb'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", 
                                    linewidth=2, edgecolor=edge, facecolor=color)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=10, fontweight='bold', color='#1e3a8a')

    # Helper to draw arrow
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#64748b', lw=2))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2, label, ha='center', va='center', backgroundcolor='white', fontsize=8)

    # Settings
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Boxes
    draw_box(4, 8.5, 2, 1, "User Request", color='#f0fdf4', edge='#16a34a')
    draw_box(4, 6.5, 2, 1, "API Server\n(FastAPI)", color='#fff7ed', edge='#ea580c')
    
    # Engine Box (Container)
    # Using simple Rectangle to avoid bounds issues with FancyBboxPatch
    rect = patches.Rectangle((1, 1), 8, 4.5, linewidth=2, edgecolor='#9333ea', facecolor='#faf5ff', alpha=0.5)
    ax.add_patch(rect)
    ax.text(5, 5.8, "Inference Engine", ha='center', fontweight='bold', color='#9333ea')
    
    draw_box(4, 4, 2, 0.8, "Scheduler", color='#eff6ff', edge='#2563eb')
    draw_box(2, 2, 2, 1, "Model Executor\n(GPU)", color='#fee2e2', edge='#dc2626')
    draw_box(6, 2, 2, 1, "Block Manager\n(PagedAttention)", color='#f0f9ff', edge='#0ea5e9')

    # Arrows
    draw_arrow(5, 8.5, 5, 7.6) # User -> API
    draw_arrow(5, 6.5, 5, 4.9, "Prompt") # API -> Scheduler
    draw_arrow(4, 4.4, 3, 3.1, "Batch") # Scheduler -> Model
    draw_arrow(6, 4.4, 7, 3.1, "Alloc/Free") # Scheduler -> BlockMgr
    draw_arrow(4, 2.5, 5.9, 2.5) # Model -> Memory
    ax.text(5, 2.7, "KV Cache", ha='center', fontsize=8)

    # Save with full figure and explicit white background
    fig.patch.set_facecolor('white')
    plt.savefig('architecture_diagram_v2.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    draw_naive_batching()
    draw_flash_batching()
    draw_architecture()
