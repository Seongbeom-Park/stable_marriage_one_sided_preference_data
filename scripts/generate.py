#!/usr/bin/env python3
import argparse
import csv
import os
import sys
import random

def generate_students(student_count, school_count):
    students = []
    school_ids = list(range(school_count))
    for student_id in range(student_count):
        random.shuffle(school_ids)
        row = {'pref_' + str(pref): school_id for pref, school_id in enumerate(school_ids)}
        row['student_id'] = student_id
        students += [row]
    return students

def generate_schools(student_count, school_count):
    schools = []
    for school_id in range(school_count):
        capacity = student_count // school_count
        row = {
                'school_id': school_id,
                'capacity': capacity,
                }
        schools += [row]
    return schools

def save(path, fieldnames, data):
    with open(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate dataset')
    parser.add_argument('student_count', type=int, help='the number of students')
    parser.add_argument('school_count', type=int, help='the number of schools. NOTE: student_count should be devided by school_count')
    parser.add_argument('path', help='saving generated dataset to the path')
    parser.add_argument('seed', nargs='+', type=int, help='random seed for shuffle student\'s preference list')
    args = parser.parse_args()

    dataset_filepath = os.path.join(args.path,
            'student' + str(args.student_count) + '_school' + str(args.school_count))
    if not os.path.exists(dataset_filepath):
        os.makedirs(dataset_filepath)

    # students
    if args.seed != None:
        for seed in args.seed:
            random.seed(seed)
            students = generate_students(args.student_count, args.school_count)
            students_filename = os.path.join(dataset_filepath,
                    'student' + str(args.student_count) + '_school' + str(args.school_count) + '_students_seed' + str(seed) + '.csv')
            save(students_filename,
                    ['student_id'] + ['pref_' + str(pref) for pref in range(args.school_count)],
                    students)

    # schools
    schools = generate_schools(args.student_count, args.school_count)
    schools_filepath = os.path.join(dataset_filepath,
            'student' + str(args.student_count) + '_school' + str(args.school_count) + '_schools.csv')
    save(schools_filepath,
            ['school_id', 'capacity'],
            schools)

