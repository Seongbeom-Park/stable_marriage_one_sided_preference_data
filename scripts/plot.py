#!/usr/bin/env python3
import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np
import os

LABEL_TIE_BREAKING = 'Baseline'
LABEL_STUDENT_OPTIMAL = 'Student-Optimal'

def read(path):
    if not os.path.isfile(path):
        sys.exit('ERROR: file not exist: ' + path)
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def calculate_mean(data):
    sum_utility = {}
    sum_execution_time = 0.0
    for row in data:
        for k, v in row.items():
            if k.startswith('pref_'):
                if k in sum_utility:
                    sum_utility[k] += float(v)
                else:
                    sum_utility[k] = float(v)
            elif k == 'execution_time':
                sum_execution_time += float(v)

    mean_utility = {k: v / len(data) for k, v in sum_utility.items()}
    mean_execution_time = sum_execution_time / len(data)
    return mean_utility, mean_execution_time

def plot(x, data, path, xlabel=None, ylabel=None, precision='{:.1f}'):
    edge_color = 'black'
    edge_width = 0.5
    bar_width = 0.9 / len(data)
    x_axis = np.arange(len(x))

    plt.subplots()
    for index, (label, values) in enumerate(data):
        z = len(values)
        rects = plt.bar(x_axis + index * bar_width,
                values,
                bar_width,
                label=label,
                edgecolor=edge_color,
                linewidth=edge_width,
                )
        plt.bar_label(rects,
                fmt=precision,
                )

    plt.xticks(x_axis + bar_width / len(data), x)
    if xlabel == None:
        plt.tick_params(axis='x',
                which='both',
                bottom=False,
                top=False,
                labelbottom=False,
                )
    else:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    # plt.show()
    plt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot figures')
    parser.add_argument('student_count', type=int, help='ath for the students')
    parser.add_argument('school_count', type=int, help='path for the schools')
    parser.add_argument('input_path', help='loading allocation result from the path')
    parser.add_argument('output_path', help='saving figures to the path')
    parser.add_argument('--console', action=argparse.BooleanOptionalAction, help='print data to the stdout without saving figures')
    args = parser.parse_args()

    output_filepath = os.path.join(args.output_path,
            'student' + str(args.student_count) + '_school' + str(args.school_count))
    if not os.path.exists(output_filepath):
        os.makedirs(output_filepath)

    summary_filepath = os.path.join(args.input_path,
            'student' + str(args.student_count) + '_school' + str(args.school_count),
            'student' + str(args.student_count) + '_school' + str(args.school_count) + '_summary.csv')
    summary = read(summary_filepath)
    utility_optimal, execution_time_optimal = calculate_mean([row for row in summary if row['algorithm'] == 'student_optimal'])
    utility_tb, execution_time_tb = calculate_mean([row for row in summary if row['algorithm'] == 'tie_breaking'])
    time_multiplier, time_unit = (1000, 'ms') if execution_time_optimal < 1.0 else (1, 's')
    print(utility_optimal, execution_time_optimal * time_multiplier, time_unit)
    print(utility_tb, execution_time_tb * time_multiplier, time_unit)

    if args.console == False or args.console == None:
        figure_utility_filepath = os.path.join(output_filepath,
                'student' + str(args.student_count) + '_school' + str(args.school_count) + '_utility.png')
        z = len(utility_tb)
        plot(['Rank ' + str(pref + 1) for pref in range(z)],
                [
                    (
                        LABEL_TIE_BREAKING,
                        [utility_tb['pref_' + str(pref)] for pref in range(z)],
                        ),
                    (
                        LABEL_STUDENT_OPTIMAL,
                        [utility_optimal['pref_' + str(pref)] for pref in range(z)],
                        ),
                    ],
                figure_utility_filepath,
                xlabel='Preference Rank of Allocated School',
                ylabel='Number of Students',
                precision='{:.1f}',
                )
        figure_execution_time_filepath = os.path.join(output_filepath,
                'student' + str(args.student_count) + '_school' + str(args.school_count) + '_execution_time.png')
        plot(['Execution Time'],
                [
                    (
                        LABEL_TIE_BREAKING,
                        [execution_time_tb * time_multiplier],
                        ),
                    (
                        LABEL_STUDENT_OPTIMAL,
                        [execution_time_optimal * time_multiplier],
                        ),
                    ],
                figure_execution_time_filepath,
                xlabel=None,
                ylabel='Execution Time (' + time_unit + ')',
                precision='{:.2f}',
                )

