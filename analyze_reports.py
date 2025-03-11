#!/usr/bin/env python3
"""
Analyze Locust CSV reports and generate a performance comparison.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def analyze_stats(stats_file):
    """Analyze the stats CSV file and return a summary."""
    if not os.path.exists(stats_file):
        print(f"Error: File {stats_file} not found.")
        return None
    
    try:
        df = pd.read_csv(stats_file)
        # Filter out the aggregated row
        df = df[df['Name'] != 'Aggregated']
        
        summary = {
            'endpoint': df['Name'].iloc[0],
            'requests': df['Request Count'].iloc[0],
            'failures': df['Failure Count'].iloc[0],
            'failure_rate': (df['Failure Count'].iloc[0] / df['Request Count'].iloc[0]) * 100 if df['Request Count'].iloc[0] > 0 else 0,
            'avg_response_time': df['Average Response Time'].iloc[0],
            'median_response_time': df['Median Response Time'].iloc[0],
            'min_response_time': df['Min Response Time'].iloc[0],
            'max_response_time': df['Max Response Time'].iloc[0],
            'requests_per_second': df['Requests/s'].iloc[0],
            'percentile_90': df['90%'].iloc[0],
            'percentile_95': df['95%'].iloc[0],
            'percentile_99': df['99%'].iloc[0],
        }
        return summary
    except Exception as e:
        print(f"Error analyzing {stats_file}: {str(e)}")
        return None

def analyze_history(history_file):
    """Analyze the history CSV file and return time-series data."""
    if not os.path.exists(history_file):
        print(f"Error: File {history_file} not found.")
        return None
    
    try:
        df = pd.read_csv(history_file)
        # Convert timestamp to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
        # Filter out rows with no requests
        df = df[df['Total Request Count'] > 0]
        
        return df
    except Exception as e:
        print(f"Error analyzing {history_file}: {str(e)}")
        return None

def generate_comparison_report(openai_summary, huggingface_summary):
    """Generate a comparison report between OpenAI and Hugging Face."""
    if not openai_summary or not huggingface_summary:
        print("Error: Missing summary data.")
        return
    
    print("\n=== Performance Comparison Report ===\n")
    print(f"{'Metric':<25} {'OpenAI':<15} {'Hugging Face':<15}")
    print("-" * 60)
    print(f"{'Endpoint':<25} {openai_summary['endpoint']:<15} {huggingface_summary['endpoint']:<15}")
    print(f"{'Total Requests':<25} {openai_summary['requests']:<15} {huggingface_summary['requests']:<15}")
    print(f"{'Failures':<25} {openai_summary['failures']:<15} {huggingface_summary['failures']:<15}")
    print(f"{'Failure Rate (%)':<25} {openai_summary['failure_rate']:.2f}%{'':<10} {huggingface_summary['failure_rate']:.2f}%")
    print(f"{'Avg Response Time (ms)':<25} {openai_summary['avg_response_time']:.2f}{'':<10} {huggingface_summary['avg_response_time']:.2f}")
    print(f"{'Median Response Time (ms)':<25} {openai_summary['median_response_time']:.2f}{'':<10} {huggingface_summary['median_response_time']:.2f}")
    print(f"{'Min Response Time (ms)':<25} {openai_summary['min_response_time']:.2f}{'':<10} {huggingface_summary['min_response_time']:.2f}")
    print(f"{'Max Response Time (ms)':<25} {openai_summary['max_response_time']:.2f}{'':<10} {huggingface_summary['max_response_time']:.2f}")
    print(f"{'Requests/s':<25} {openai_summary['requests_per_second']:.2f}{'':<10} {huggingface_summary['requests_per_second']:.2f}")
    print(f"{'90% Response Time (ms)':<25} {openai_summary['percentile_90']:.2f}{'':<10} {huggingface_summary['percentile_90']:.2f}")
    print(f"{'95% Response Time (ms)':<25} {openai_summary['percentile_95']:.2f}{'':<10} {huggingface_summary['percentile_95']:.2f}")
    print(f"{'99% Response Time (ms)':<25} {openai_summary['percentile_99']:.2f}{'':<10} {huggingface_summary['percentile_99']:.2f}")
    
    print("\n=== Performance Insights ===\n")
    
    # Compare response times
    if openai_summary['avg_response_time'] < huggingface_summary['avg_response_time']:
        print("- OpenAI API has lower average response times than Hugging Face.")
    else:
        print("- Hugging Face has lower average response times than OpenAI API.")
    
    # Compare throughput
    if openai_summary['requests_per_second'] > huggingface_summary['requests_per_second']:
        print("- OpenAI API has higher throughput (requests/second) than Hugging Face.")
    else:
        print("- Hugging Face has higher throughput (requests/second) than OpenAI API.")
    
    # Compare stability (using 95th percentile vs median ratio as a measure)
    openai_stability = openai_summary['percentile_95'] / openai_summary['median_response_time']
    hf_stability = huggingface_summary['percentile_95'] / huggingface_summary['median_response_time']
    
    if openai_stability < hf_stability:
        print("- OpenAI API shows more consistent response times (less variation).")
    else:
        print("- Hugging Face shows more consistent response times (less variation).")
    
    print("\n=== Recommendations ===\n")
    
    if openai_summary['failure_rate'] > 0:
        print(f"- Investigate OpenAI API failures ({openai_summary['failure_rate']:.2f}%).")
    
    if huggingface_summary['failure_rate'] > 0:
        print(f"- Investigate Hugging Face API failures ({huggingface_summary['failure_rate']:.2f}%).")
    
    if openai_summary['max_response_time'] > 1000:
        print("- Consider implementing timeouts for OpenAI API calls to handle slow responses.")
    
    if huggingface_summary['max_response_time'] > 1000:
        print("- Consider implementing timeouts for Hugging Face API calls to handle slow responses.")
    
    print("- For production use, implement retry logic with exponential backoff for both APIs.")
    print("- Consider caching responses for common queries to reduce API load and improve response times.")

def plot_comparison(openai_history, huggingface_history):
    """Generate comparison plots."""
    if not openai_history is None and not huggingface_history is None:
        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # Plot response times
        ax1.plot(openai_history['Timestamp'], openai_history['Total Average Response Time'], 'b-', label='OpenAI')
        ax1.plot(huggingface_history['Timestamp'], huggingface_history['Total Average Response Time'], 'r-', label='Hugging Face')
        ax1.set_title('Average Response Time Over Time')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Response Time (ms)')
        ax1.legend()
        ax1.grid(True)
        
        # Plot requests per second
        ax2.plot(openai_history['Timestamp'], openai_history['Requests/s'], 'b-', label='OpenAI')
        ax2.plot(huggingface_history['Timestamp'], huggingface_history['Requests/s'], 'r-', label='Hugging Face')
        ax2.set_title('Requests per Second Over Time')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Requests/s')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('reports/performance_comparison.png')
        print("\nPlot saved to reports/performance_comparison.png")
    else:
        print("Error: Missing history data for plotting.")

def main():
    """Main function."""
    # Check if reports directory exists
    if not os.path.exists('reports'):
        print("Error: Reports directory not found.")
        sys.exit(1)
    
    # Analyze OpenAI stats
    openai_summary = analyze_stats('reports/openai_stats.csv')
    
    # Analyze Hugging Face stats
    huggingface_summary = analyze_stats('reports/huggingface_stats.csv')
    
    # Generate comparison report
    if openai_summary and huggingface_summary:
        generate_comparison_report(openai_summary, huggingface_summary)
    
    # Analyze history data
    openai_history = analyze_history('reports/openai_stats_history.csv')
    huggingface_history = analyze_history('reports/huggingface_stats_history.csv')
    
    # Plot comparison
    plot_comparison(openai_history, huggingface_history)

if __name__ == "__main__":
    main() 