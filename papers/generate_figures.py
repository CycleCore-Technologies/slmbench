#!/usr/bin/env python3
"""
Generate publication-quality figures for Maaza paper.

Copyright 2025 CycleCore Technologies
Licensed under the Apache License, Version 2.0
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set publication style
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

# Color scheme
COLOR_MAAZA = '#2E86AB'  # Blue for fine-tuned models
COLOR_BASE = '#A23B72'   # Purple for base/zero-shot models
COLOR_QWEN = '#F18F01'   # Orange for Qwen baseline

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


def figure1_performance_vs_size():
    """Figure 1: JSONExact vs Model Size - showing fine-tuning advantage."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Separate by model type
    base_models = [(k, v) for k, v in models.items() if v['type'] == 'base']
    maaza_models = [(k, v) for k, v in models.items() if v['type'] == 'maaza']
    qwen_models = [(k, v) for k, v in models.items() if v['type'] == 'qwen']
    
    # Plot base models
    for name, data in base_models:
        ax.scatter(data['params'], data['json_exact'], 
                  s=150, marker='D', color=COLOR_BASE, 
                  edgecolors='black', linewidths=1.5, alpha=0.7,
                  zorder=3)
        ax.annotate(name.replace(' (base)', ''), 
                   (data['params'], data['json_exact']),
                   xytext=(10, -15), textcoords='offset points',
                   fontsize=8, ha='left')
    
    # Plot Maaza models
    for name, data in maaza_models:
        ax.scatter(data['params'], data['json_exact'], 
                  s=200, marker='o', color=COLOR_MAAZA, 
                  edgecolors='black', linewidths=1.5,
                  zorder=4)
        ax.annotate(name, 
                   (data['params'], data['json_exact']),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=8, ha='left', fontweight='bold')
    
    # Plot Qwen
    for name, data in qwen_models:
        ax.scatter(data['params'], data['json_exact'], 
                  s=150, marker='s', color=COLOR_QWEN, 
                  edgecolors='black', linewidths=1.5, alpha=0.7,
                  zorder=3)
        ax.annotate(name, 
                   (data['params'], data['json_exact']),
                   xytext=(-10, 10), textcoords='offset points',
                   fontsize=8, ha='right')
    
    # Draw connection lines to show fine-tuning gains
    ax.plot([135, 135], [1.9, 24.7], 'k--', alpha=0.3, linewidth=1, zorder=1)
    ax.plot([360, 360], [11.4, 55.1], 'k--', alpha=0.3, linewidth=1, zorder=1)
    
    # Add gain annotations
    ax.annotate('13× gain', (135, 13), fontsize=9, ha='center', 
               style='italic', color='gray')
    ax.annotate('4.8× gain', (360, 33), fontsize=9, ha='center',
               style='italic', color='gray')
    
    ax.set_xlabel('Model Parameters (millions)', fontsize=11, fontweight='bold')
    ax.set_ylabel('JSONExact Score (%)', fontsize=11, fontweight='bold')
    ax.set_title('Figure 1: Performance vs Model Size\nTask Specialization Outperforms Parameter Scaling', 
                fontsize=12, fontweight='bold', pad=15)
    
    ax.set_xlim(100, 550)
    ax.set_ylim(-2, 60)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Legend
    legend_elements = [
        mpatches.Patch(color=COLOR_MAAZA, label='Fine-tuned (Maaza)'),
        mpatches.Patch(color=COLOR_BASE, label='Base (Zero-shot)'),
        mpatches.Patch(color=COLOR_QWEN, label='Qwen2.5-0.5B (Baseline)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('/home/rain/SLMBench/papers/figures/figure1_performance_vs_size.png', 
                dpi=300, bbox_inches='tight')
    plt.savefig('/home/rain/SLMBench/papers/figures/figure1_performance_vs_size.pdf', 
                bbox_inches='tight')
    print("✅ Figure 1 saved")
    plt.close()


def figure2_performance_by_complexity():
    """Figure 2: Performance breakdown by schema complexity."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data
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
                     edgecolor='black',
                     linewidth=0.8,
                     hatch=hatches[model],
                     alpha=0.85 if 'base' in model.lower() or 'Qwen' in model else 1.0)
    
    ax.set_xlabel('Schema Complexity', fontsize=11, fontweight='bold')
    ax.set_ylabel('JSONExact Score (%)', fontsize=11, fontweight='bold')
    ax.set_title('Figure 2: Performance by Schema Complexity\nCapacity Threshold Emerges at ~300M Parameters',
                fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(complexity_levels)
    ax.legend(fontsize=8, loc='upper right', ncol=1)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Add horizontal line at 0% for reference
    ax.axhline(y=0, color='black', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('/home/rain/SLMBench/papers/figures/figure2_performance_by_complexity.png',
                dpi=300, bbox_inches='tight')
    plt.savefig('/home/rain/SLMBench/papers/figures/figure2_performance_by_complexity.pdf',
                bbox_inches='tight')
    print("✅ Figure 2 saved")
    plt.close()


def figure3_disk_size_vs_performance():
    """Figure 3: Disk size vs performance - efficiency comparison."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
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
                  edgecolors='black', linewidths=1.5,
                  alpha=0.7 if data['type'] != 'maaza' else 1.0,
                  zorder=3)
        
        # Annotations
        if 'Maaza' in name:
            ax.annotate(name, (data['size'], data['perf']),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=8, ha='left', fontweight='bold')
        else:
            ax.annotate(name.replace(' (base)', ''), (data['size'], data['perf']),
                       xytext=(10, -15), textcoords='offset points',
                       fontsize=8, ha='left')
    
    ax.set_xlabel('Disk Size (MB)', fontsize=11, fontweight='bold')
    ax.set_ylabel('JSONExact Score (%)', fontsize=11, fontweight='bold')
    ax.set_title('Figure 3: Model Size vs Performance\nEdge Deployment Efficiency',
                fontsize=12, fontweight='bold', pad=15)
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(200, 1000)
    ax.set_ylim(-2, 60)
    
    # Legend
    legend_elements = [
        mpatches.Patch(color=COLOR_MAAZA, label='Fine-tuned (Maaza)'),
        mpatches.Patch(color=COLOR_BASE, label='Base (Zero-shot)'),
        mpatches.Patch(color=COLOR_QWEN, label='Qwen2.5-0.5B'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('/home/rain/SLMBench/papers/figures/figure3_disk_size_vs_performance.png',
                dpi=300, bbox_inches='tight')
    plt.savefig('/home/rain/SLMBench/papers/figures/figure3_disk_size_vs_performance.pdf',
                bbox_inches='tight')
    print("✅ Figure 3 saved")
    plt.close()


def figure4_fine_tuning_comparison():
    """Figure 4: Before/after fine-tuning comparison bars."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Data
    models_ft = ['SmolLM2-135M', 'SmolLM2-360M']
    base_scores = [1.9, 11.4]
    ft_scores = [24.7, 55.1]
    gains = ['13×', '4.8×']
    
    x = np.arange(len(models_ft))
    width = 0.35
    
    # Left plot: Side-by-side comparison
    bars1 = ax1.bar(x - width/2, base_scores, width, label='Base (Zero-shot)',
                    color=COLOR_BASE, edgecolor='black', linewidth=1)
    bars2 = ax1.bar(x + width/2, ft_scores, width, label='Fine-tuned (Maaza)',
                    color=COLOR_MAAZA, edgecolor='black', linewidth=1)
    
    ax1.set_xlabel('Model', fontsize=11, fontweight='bold')
    ax1.set_ylabel('JSONExact Score (%)', fontsize=11, fontweight='bold')
    ax1.set_title('(A) Base vs Fine-tuned Performance', fontsize=11, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models_ft)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Add gain labels with better positioning and styling
    for i, gain in enumerate(gains):
        y_pos = ft_scores[i] + 5  # Place above fine-tuned bar
        # Add white background box for better readability
        bbox_props = dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='#27AE60', linewidth=1.5, alpha=0.9)
        ax1.text(i, y_pos, gain,
                ha='center', va='bottom', fontsize=10, fontweight='bold', 
                color='#27AE60', bbox=bbox_props)
    
    # Right plot: Improvement ratios
    improvement_pct = [(ft - base) / base * 100 for base, ft in zip(base_scores, ft_scores)]
    bars3 = ax2.bar(x, improvement_pct, width*2,
                    color=['#27AE60', '#16A085'], edgecolor='black', linewidth=1)
    
    ax2.set_xlabel('Model', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Improvement (%)', fontsize=11, fontweight='bold')
    ax2.set_title('(B) Fine-tuning Improvement', fontsize=11, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models_ft)
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Add value labels on bars with better styling
    for i, (bar, val) in enumerate(zip(bars3, improvement_pct)):
        height = bar.get_height()
        # Add semi-transparent background for readability
        bbox_props = dict(boxstyle='round,pad=0.4', facecolor='white', 
                         edgecolor='gray', linewidth=1, alpha=0.85)
        ax2.text(bar.get_x() + bar.get_width()/2., height + 15,
                f'+{val:.0f}%', ha='center', va='bottom',
                fontsize=10, fontweight='bold', bbox=bbox_props)
    
    plt.suptitle('Figure 4: Fine-tuning Impact on Small Language Models',
                fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('/home/rain/SLMBench/papers/figures/figure4_fine_tuning_comparison.png',
                dpi=300, bbox_inches='tight')
    plt.savefig('/home/rain/SLMBench/papers/figures/figure4_fine_tuning_comparison.pdf',
                bbox_inches='tight')
    print("✅ Figure 4 saved")
    plt.close()


def main():
    """Generate all figures."""
    import os
    os.makedirs('/home/rain/SLMBench/papers/figures', exist_ok=True)
    
    print("\n" + "="*70)
    print("📊 Generating Publication Figures for Maaza Paper")
    print("="*70 + "\n")
    
    figure1_performance_vs_size()
    figure2_performance_by_complexity()
    figure3_disk_size_vs_performance()
    figure4_fine_tuning_comparison()
    
    print("\n" + "="*70)
    print("✅ All figures generated successfully!")
    print("="*70)
    print("\n📁 Output directory: /home/rain/SLMBench/papers/figures/")
    print("\n📄 Files created:")
    print("  • figure1_performance_vs_size.png/.pdf")
    print("  • figure2_performance_by_complexity.png/.pdf")
    print("  • figure3_disk_size_vs_performance.png/.pdf")
    print("  • figure4_fine_tuning_comparison.png/.pdf")
    print("\n💡 Figures saved in both PNG (300 DPI) and PDF (vector) formats")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()

