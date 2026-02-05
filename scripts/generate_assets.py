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
    # Use 1:1 aspect ratio to prevent squashing
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Settings
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Helper to draw box
    def draw_box(x, y, w, h, text, color='#eff6ff', edge='#2563eb', text_color='#1e3a8a', fontsize=10):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", 
                                    linewidth=2, edgecolor=edge, facecolor=color)
        ax.add_patch(rect)
        ax.text(x + w/2 + 0.2, y + h/2 + 0.2, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=text_color)

    # Helper to draw arrow
    def draw_arrow(x1, y1, x2, y2, label="", ha='center'):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#64748b', lw=2))
        if label:
            # Place label on a white background box
            t = ax.text((x1+x2)/2, (y1+y2)/2, label, ha=ha, va='center', fontsize=9, color='#475569', backgroundcolor='white')
            t.set_bbox(dict(facecolor='white', edgecolor='none', alpha=0.8, pad=0))

    # --- Layout ---
    
    # 1. User Request (Top) - Centered at X=6
    draw_box(4.5, 10.0, 3, 1.0, "User Request", color='#f0fdf4', edge='#16a34a', text_color='#14532d', fontsize=11)
    
    # 2. API Server
    draw_box(4.5, 8.0, 3, 1.0, "API Server\n(FastAPI)", color='#fff7ed', edge='#ea580c', text_color='#7c2d12', fontsize=11)
    
    # 3. Inference Engine (Big Container)
    # Spans X=1 to 11, Y=1 to 6.5
    rect = patches.Rectangle((1, 1), 10, 5.5, linewidth=2, edgecolor='#9333ea', facecolor='#faf5ff', alpha=0.5, linestyle='--')
    ax.add_patch(rect)
    ax.text(6, 6.0, "Inference Engine", ha='center', fontweight='bold', fontsize=12, color='#9333ea')
    
    # 4. Engine Internal Components
    # Scheduler (Top of Engine)
    draw_box(4.5, 4.5, 3, 1.0, "Scheduler", color='#eff6ff', edge='#2563eb', text_color='#1e3a8a', fontsize=11)
    
    # Model Executor (Bottom Left)
    draw_box(1.5, 2.0, 3, 1.0, "Model Executor\n(GPU)", color='#fee2e2', edge='#dc2626', text_color='#7f1d1d', fontsize=10)
    
    # Block Manager (Bottom Right)
    draw_box(7.5, 2.0, 3, 1.0, "Block Manager\n(PagedAttention)", color='#f0f9ff', edge='#0ea5e9', text_color='#0c4a6e', fontsize=10)

    # --- Connections ---
    
    # User -> API
    draw_arrow(6, 10.0, 6, 9.4)
    
    # API -> Scheduler (Enters Engine)
    draw_arrow(6, 8.0, 6, 6.0, "Prompt Queue", ha='center')
    draw_arrow(6, 6.0, 6, 5.9) # Continue into container
    
    # Scheduler -> Model
    draw_arrow(5, 4.5, 3, 3.4, "Schedule Batch", ha='right')
    
    # Scheduler -> Block Manager
    draw_arrow(7, 4.5, 9, 3.4, "Alloc/Free Blocks", ha='left')
    
    # Model -> RAM (Conceptual)
    draw_arrow(4.5, 2.5, 7.5, 2.5, "KV Cache Updates")

    # Save
    fig.patch.set_facecolor('white')
    plt.savefig('architecture_diagram_v3.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    draw_naive_batching()
    draw_flash_batching()
    draw_architecture()
