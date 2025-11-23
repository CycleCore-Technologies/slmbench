#!/usr/bin/env python3
"""
Generate DARK MODE publication-quality figures for Maaza paper.

Copyright 2025 CycleCore Technologies
Licensed under the Apache License, Version 2.0
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set publication style for DARK MODE
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.facecolor'] = '#1a1a1a'
plt.rcParams['axes.facecolor'] = '#1a1a1a'
plt.rcParams['savefig.facecolor'] = '#1a1a1a'
plt.rcParams['text.color'] = '#f0f0f0'
plt.rcParams['axes.labelcolor'] = '#f0f0f0'
plt.rcParams['xtick.color'] = '#f0f0f0'
plt.rcParams['ytick.color'] = '#f0f0f0'
plt.rcParams['grid.color'] = '#404040'

# Dark mode color scheme (vibrant but not harsh)
COLOR_MAAZA = '#4FC3F7'  # Bright cyan-blue for fine-tuned models
COLOR_BASE = '#CE93D8'   # Bright purple for base/zero-shot models
COLOR_QWEN = '#FFB74D'   # Bright orange for Qwen baseline

# Data
models = {
    'SmolLM2-135M (base)': {'params': 135, 'json_exact': 1.9, 'type': 'base'},
    'Maaza-MLM-135M': {'params': 135, 'json_exact': 24.7, 'type': 'maaza'},
    'SmolLM2-360M (base)': {'params': 360, 'json_exact': 11.4, 'type': 'base'},
    'Maaza-SLM-360M': {'params': 360, 'json_exact': 55.1, 'type': 'maaza'},
    'Qwen2.5-0.5B': {'params': 500, 'json_exact': 14.6, 'type': 'qwen'},
}

# Complexity data
complexity_data = {
    'Simple': {
        'SmolLM2-135M': 4.0,
        'Maaza-MLM-135M': 44.7,
        'SmolLM2-360M': 23.7,
        'Maaza-SLM-360M': 78.9,
        'Qwen2.5-0.5B': 28.9,
    },
    'Medium': {
        'SmolLM2-135M': 0.0,
        'Maaza-MLM-135M': 13.5,
        'SmolLM2-360M': 0.0,
        'Maaza-SLM-360M': 51.4,
        'Qwen2.5-0.5B': 2.7,
    },
    'Complex': {
        'SmolLM2-135M': 0.0,
        'Maaza-MLM-135M': 0.0,
        'SmolLM2-360M': 0.0,
        'Maaza-SLM-360M': 4.0,
        'Qwen2.5-0.5B': 0.0,
    },
}


def figure1_performance_vs_size_dark():
    """Figure 1 DARK: JSONExact vs Model Size."""
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    # Separate by model type
    base_models = [(k, v) for k, v in models.items() if v['type'] == 'base']
    maaza_models = [(k, v) for k, v in models.items() if v['type'] == 'maaza']
    qwen_models = [(k, v) for k, v in models.items() if v['type'] == 'qwen']
    
    # Plot base models
    for name, data in base_models:
        ax.scatter(data['params'], data['json_exact'], 
                  s=150, marker='D', color=COLOR_BASE, 
                  edgecolors='white', linewidths=1.5, alpha=0.8,
                  zorder=3)
        ax.annotate(name.replace(' (base)', ''), 
                   (data['params'], data['json_exact']),
                   xytext=(10, -15), textcoords='offset points',
                   fontsize=8, ha='left', color='#f0f0f0')
    
    # Plot Maaza models
    for name, data in maaza_models:
        ax.scatter(data['params'], data['json_exact'], 
                  s=200, marker='o', color=COLOR_MAAZA, 
                  edgecolors='white', linewidths=1.5,
                  zorder=4)
        ax.annotate(name, 
                   (data['params'], data['json_exact']),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=8, ha='left', fontweight='bold', color='#ffffff')
    
    # Plot Qwen
    for name, data in qwen_models:
        ax.scatter(data['params'], data['json_exact'], 
                  s=150, marker='s', color=COLOR_QWEN, 
                  edgecolors='white', linewidths=1.5, alpha=0.8,
                  zorder=3)
        ax.annotate(name, 
                   (data['params'], data['json_exact']),
                   xytext=(-10, 10), textcoords='offset points',
                   fontsize=8, ha='right', color='#f0f0f0')
    
    # Draw connection lines
    ax.plot([135, 135], [1.9, 24.7], 'w--', alpha=0.4, linewidth=1.5, zorder=1)
    ax.plot([360, 360], [11.4, 55.1], 'w--', alpha=0.4, linewidth=1.5, zorder=1)
    
    # Add gain annotations
    ax.annotate('13× gain', (135, 13), fontsize=9, ha='center', 
               style='italic', color='#aaaaaa')
    ax.annotate('4.8× gain', (360, 33), fontsize=9, ha='center',
               style='italic', color='#aaaaaa')
    
    ax.set_xlabel('Model Parameters (millions)', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax.set_ylabel('JSONExact Score (%)', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax.set_title('Figure 1: Performance vs Model Size\nTask Specialization Outperforms Parameter Scaling', 
                fontsize=12, fontweight='bold', pad=15, color='#ffffff')
    
    ax.set_xlim(100, 550)
    ax.set_ylim(-2, 60)
    ax.grid(True, alpha=0.2, linestyle='--', color='#505050')
    
    # Legend
    legend_elements = [
        mpatches.Patch(color=COLOR_MAAZA, label='Fine-tuned (Maaza)'),
        mpatches.Patch(color=COLOR_BASE, label='Base (Zero-shot)'),
        mpatches.Patch(color=COLOR_QWEN, label='Qwen2.5-0.5B (Baseline)'),
    ]
    legend = ax.legend(handles=legend_elements, loc='upper left', fontsize=9,
                      facecolor='#2a2a2a', edgecolor='#505050')
    plt.setp(legend.get_texts(), color='#f0f0f0')
    
    plt.tight_layout()
    plt.savefig('/home/rain/SLMBench/papers/figures/figure1_performance_vs_size_DARK.png', 
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.savefig('/home/rain/SLMBench/papers/figures/figure1_performance_vs_size_DARK.pdf', 
                bbox_inches='tight', facecolor='#1a1a1a')
    print("✅ Figure 1 DARK saved")
    plt.close()


def figure2_performance_by_complexity_dark():
    """Figure 2 DARK: Performance breakdown by schema complexity."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    complexity_levels = ['Simple', 'Medium', 'Complex']
    model_names = ['SmolLM2-135M', 'Maaza-MLM-135M', 'SmolLM2-360M', 
                   'Maaza-SLM-360M', 'Qwen2.5-0.5B']
    
    x = np.arange(len(complexity_levels))
    width = 0.15
    
    colors = {
        'SmolLM2-135M': COLOR_BASE,
        'Maaza-MLM-135M': COLOR_MAAZA,
        'SmolLM2-360M': COLOR_BASE,
        'Maaza-SLM-360M': COLOR_MAAZA,
        'Qwen2.5-0.5B': COLOR_QWEN,
    }
    
    hatches = {
        'SmolLM2-135M': '///',
        'Maaza-MLM-135M': '',
        'SmolLM2-360M': '...',
        'Maaza-SLM-360M': '',
        'Qwen2.5-0.5B': 'xxx',
    }
    
    # Plot bars
    for i, model in enumerate(model_names):
        values = [complexity_data[comp][model] for comp in complexity_levels]
        offset = (i - 2) * width
        bars = ax.bar(x + offset, values, width, 
                     label=model,
                     color=colors[model],
                     edgecolor='white',
                     linewidth=0.8,
                     hatch=hatches[model],
                     alpha=0.75 if 'base' in model.lower() or 'Qwen' in model else 0.95)
    
    ax.set_xlabel('Schema Complexity', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax.set_ylabel('JSONExact Score (%)', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax.set_title('Figure 2: Performance by Schema Complexity\nCapacity Threshold Emerges at ~300M Parameters',
                fontsize=12, fontweight='bold', pad=15, color='#ffffff')
    ax.set_xticks(x)
    ax.set_xticklabels(complexity_levels)
    legend = ax.legend(fontsize=8, loc='upper right', ncol=1,
                      facecolor='#2a2a2a', edgecolor='#505050')
    plt.setp(legend.get_texts(), color='#f0f0f0')
    ax.grid(True, alpha=0.2, linestyle='--', axis='y', color='#505050')
    
    # Add horizontal line at 0%
    ax.axhline(y=0, color='#808080', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('/home/rain/SLMBench/papers/figures/figure2_performance_by_complexity_DARK.png',
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.savefig('/home/rain/SLMBench/papers/figures/figure2_performance_by_complexity_DARK.pdf',
                bbox_inches='tight', facecolor='#1a1a1a')
    print("✅ Figure 2 DARK saved")
    plt.close()


def figure3_disk_size_vs_performance_dark():
    """Figure 3 DARK: Disk size vs performance."""
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    disk_data = {
        'SmolLM2-135M (base)': {'size': 270, 'perf': 1.9, 'type': 'base'},
        'Maaza-MLM-135M': {'size': 270, 'perf': 24.7, 'type': 'maaza'},
        'SmolLM2-360M (base)': {'size': 720, 'perf': 11.4, 'type': 'base'},
        'Maaza-SLM-360M': {'size': 720, 'perf': 55.1, 'type': 'maaza'},
        'Qwen2.5-0.5B': {'size': 954, 'perf': 14.6, 'type': 'qwen'},
    }
    
    for name, data in disk_data.items():
        if data['type'] == 'base':
            color, marker, size = COLOR_BASE, 'D', 150
        elif data['type'] == 'maaza':
            color, marker, size = COLOR_MAAZA, 'o', 200
        else:
            color, marker, size = COLOR_QWEN, 's', 150
        
        ax.scatter(data['size'], data['perf'], 
                  s=size, marker=marker, color=color,
                  edgecolors='white', linewidths=1.5,
                  alpha=0.75 if data['type'] != 'maaza' else 0.95,
                  zorder=3)
        
        # Annotations
        if 'Maaza' in name:
            ax.annotate(name, (data['size'], data['perf']),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=8, ha='left', fontweight='bold', color='#ffffff')
        else:
            ax.annotate(name.replace(' (base)', ''), (data['size'], data['perf']),
                       xytext=(10, -15), textcoords='offset points',
                       fontsize=8, ha='left', color='#f0f0f0')
    
    ax.set_xlabel('Disk Size (MB)', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax.set_ylabel('JSONExact Score (%)', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax.set_title('Figure 3: Model Size vs Performance\nEdge Deployment Efficiency',
                fontsize=12, fontweight='bold', pad=15, color='#ffffff')
    
    ax.grid(True, alpha=0.2, linestyle='--', color='#505050')
    ax.set_xlim(200, 1000)
    ax.set_ylim(-2, 60)
    
    # Legend
    legend_elements = [
        mpatches.Patch(color=COLOR_MAAZA, label='Fine-tuned (Maaza)'),
        mpatches.Patch(color=COLOR_BASE, label='Base (Zero-shot)'),
        mpatches.Patch(color=COLOR_QWEN, label='Qwen2.5-0.5B'),
    ]
    legend = ax.legend(handles=legend_elements, loc='upper left', fontsize=9,
                      facecolor='#2a2a2a', edgecolor='#505050')
    plt.setp(legend.get_texts(), color='#f0f0f0')
    
    plt.tight_layout()
    plt.savefig('/home/rain/SLMBench/papers/figures/figure3_disk_size_vs_performance_DARK.png',
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.savefig('/home/rain/SLMBench/papers/figures/figure3_disk_size_vs_performance_DARK.pdf',
                bbox_inches='tight', facecolor='#1a1a1a')
    print("✅ Figure 3 DARK saved")
    plt.close()


def figure4_fine_tuning_comparison_dark():
    """Figure 4 DARK: Before/after fine-tuning comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#1a1a1a')
    ax1.set_facecolor('#1a1a1a')
    ax2.set_facecolor('#1a1a1a')
    
    models_ft = ['SmolLM2-135M', 'SmolLM2-360M']
    base_scores = [1.9, 11.4]
    ft_scores = [24.7, 55.1]
    gains = ['13×', '4.8×']
    
    x = np.arange(len(models_ft))
    width = 0.35
    
    # Left plot
    bars1 = ax1.bar(x - width/2, base_scores, width, label='Base (Zero-shot)',
                    color=COLOR_BASE, edgecolor='white', linewidth=1, alpha=0.8)
    bars2 = ax1.bar(x + width/2, ft_scores, width, label='Fine-tuned (Maaza)',
                    color=COLOR_MAAZA, edgecolor='white', linewidth=1, alpha=0.95)
    
    ax1.set_xlabel('Model', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax1.set_ylabel('JSONExact Score (%)', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax1.set_title('(A) Base vs Fine-tuned Performance', fontsize=11, fontweight='bold', color='#ffffff')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models_ft)
    legend1 = ax1.legend(fontsize=9, facecolor='#2a2a2a', edgecolor='#505050')
    plt.setp(legend1.get_texts(), color='#f0f0f0')
    ax1.grid(True, alpha=0.2, linestyle='--', axis='y', color='#505050')
    
    # Add gain labels with better positioning and dark mode styling
    for i, gain in enumerate(gains):
        y_pos = ft_scores[i] + 5  # Place above fine-tuned bar
        # Add dark background box with bright green border
        bbox_props = dict(boxstyle='round,pad=0.3', facecolor='#2a2a2a', 
                         edgecolor='#66FF66', linewidth=2, alpha=0.95)
        ax1.text(i, y_pos, gain,
                ha='center', va='bottom', fontsize=10, fontweight='bold', 
                color='#66FF66', bbox=bbox_props)
    
    # Right plot
    improvement_pct = [(ft - base) / base * 100 for base, ft in zip(base_scores, ft_scores)]
    bars3 = ax2.bar(x, improvement_pct, width*2,
                    color=['#66BB6A', '#4FC3F7'], edgecolor='white', linewidth=1, alpha=0.9)
    
    ax2.set_xlabel('Model', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax2.set_ylabel('Improvement (%)', fontsize=11, fontweight='bold', color='#f0f0f0')
    ax2.set_title('(B) Fine-tuning Improvement', fontsize=11, fontweight='bold', color='#ffffff')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models_ft)
    ax2.grid(True, alpha=0.2, linestyle='--', axis='y', color='#505050')
    
    # Add value labels with better dark mode styling
    for i, (bar, val) in enumerate(zip(bars3, improvement_pct)):
        height = bar.get_height()
        # Add dark semi-transparent background with border
        bbox_props = dict(boxstyle='round,pad=0.4', facecolor='#2a2a2a', 
                         edgecolor='#808080', linewidth=1.5, alpha=0.9)
        ax2.text(bar.get_x() + bar.get_width()/2., height + 15,
                f'+{val:.0f}%', ha='center', va='bottom',
                fontsize=10, fontweight='bold', color='#ffffff', bbox=bbox_props)
    
    plt.suptitle('Figure 4: Fine-tuning Impact on Small Language Models',
                fontsize=13, fontweight='bold', y=1.02, color='#ffffff')
    plt.tight_layout()
    plt.savefig('/home/rain/SLMBench/papers/figures/figure4_fine_tuning_comparison_DARK.png',
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.savefig('/home/rain/SLMBench/papers/figures/figure4_fine_tuning_comparison_DARK.pdf',
                bbox_inches='tight', facecolor='#1a1a1a')
    print("✅ Figure 4 DARK saved")
    plt.close()


def main():
    """Generate all DARK MODE figures."""
    print("\n" + "="*70)
    print("🌙 Generating DARK MODE Figures for Maaza Paper")
    print("="*70 + "\n")
    
    figure1_performance_vs_size_dark()
    figure2_performance_by_complexity_dark()
    figure3_disk_size_vs_performance_dark()
    figure4_fine_tuning_comparison_dark()
    
    print("\n" + "="*70)
    print("✅ All DARK MODE figures generated successfully!")
    print("="*70)
    print("\n📁 Output directory: /home/rain/SLMBench/papers/figures/")
    print("\n📄 Files created:")
    print("  • figure1_performance_vs_size_DARK.png/.pdf")
    print("  • figure2_performance_by_complexity_DARK.png/.pdf")
    print("  • figure3_disk_size_vs_performance_DARK.png/.pdf")
    print("  • figure4_fine_tuning_comparison_DARK.png/.pdf")
    print("\n🌙 Dark mode: Perfect for late-night paper reviews!")
    print("💡 Vibrant colors pop against dark background")
    print("👁️  Easier on the eyes, professional aesthetics")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()

