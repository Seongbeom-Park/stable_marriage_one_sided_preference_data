# Stable Marriage with One Sided Preference Dataset

## Input Data
- `input/student{n}_school{m}`: n students and m schools
- `students_seed{k}.csv`: generated preference list of students with seed k
- `schools.csv`: capacity of each schools

## Output Data
- `output/student{n}_school{m}`: n students and m schools
- `result_optimal_seed{k}.csv`: student-optimal matching with `students_seed{k}.csv`
- `result_tb_seed{k}.csv`: student-oriented matching by tie-breaking algorithm with `students_seed{k}.csv`
- `summary.csv`: utilization and execution time

