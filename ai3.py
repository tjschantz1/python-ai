# Constraint Satisfaction AI - Class Scheduling for Soonest Graduation

'''
This CSP program considers the following constraints:
1. Student will take one and only one course per term
2. Course that has prerequisites must be taken in a term that follows the term
    in which all prerequisites are done
3. Some terms may be skipped as long as the student finishes in Year 3 Fall 2
4. Student needs to take 3 out of the 8 elective courses. It doesn’t matter
    which ones are included in the degree plan. Those courses which are not
    taken will be labeled as “Not Taken” (see sample output)
5. Student must take all foundation and core courses
'''

# Import packages
import numpy as np
import pandas as pd
from constraint import *

# Import Course Rotations worksheet as dataframe & encode for numeric domain
dfRotations = pd.read_excel('csp_course_rotations.xlsx', sheet_name='course_rotations')

# Import Prerequisites worksheet as dataframe & encode for numeric domain
dfPrereqs = pd.read_excel('csp_course_rotations.xlsx', sheet_name='prereqs')
dfPrereqs = dfPrereqs.drop_duplicates(subset=['prereq','course']).reset_index(drop=True) # remove duplicate entries

# Initalize Variables, Lists, & Dictionaries
startTerm = 1
years = [1,2,3]
termNums = [1,2,3,4,5,6]
termNames = ['Fall 1', 'Fall 2', 'Spring 1', 'Spring 2', 'Summer 1', 'Summer 2']

yearTermList = []
for i in years:
    for j in termNames:
        yearTermList.append('Year ' + str(i) + ' ' + str(j))
del yearTermList[-4:] # remove Year/Term entries in list >Year 3 Fall 2
yearTermList += ['Not Taken'] # for print mapper

courses = list(dfRotations['Course']) # variables
allTerms = list(range(1,15)) + [90,91,92,93,94] # domains; >90 = Not Taken
mapDict = {k: v for k, v in zip(allTerms,yearTermList)} # for print mapper

prereqDict = dfPrereqs.groupby('course').agg({'prereq': lambda x: x.tolist()})['prereq'].to_dict()

mustTake = list(dfRotations['Course'][(dfRotations['Type'] == 'foundation') | 
        (dfRotations['Type'] == 'core')])

# Obtain domains for each course variable
def getCourseTerms(dfi, canSkipBool):
    df = dfi[termNums] # create df of term availabilty by course
    df = df * termNums # set each 1-value to associate term number
    df.set_index(dfi['Course'], inplace=True)
    df = df.replace({0:np.nan})
    
    for i in range(7,15): # extend width of df to # of terms required
        df[i] = df[i-6] + 6
    
    if canSkipBool is True:
        for i in range(90,95): # add values for 5 out of 8 skipped terms
            df[i] = i
    return df
dfMustTakeTerms = dfRotations[(dfRotations['Type'] == 'foundation') | 
        (dfRotations['Type'] == 'core') | 
        (dfRotations['Type'] == 'capstone')]
dfMustTakeTerms = getCourseTerms(dfMustTakeTerms, False)
dfElectiveTerms = dfRotations[(dfRotations['Type'] == 'elective')]
dfElectiveTerms = getCourseTerms(dfElectiveTerms, True)

# Create dictionaries for must-take & elective classes
mustTakeTermDict = {}
for i in range(len(dfMustTakeTerms)):
    key = dfMustTakeTerms.index[i]
    values = list(dfMustTakeTerms.iloc[i].dropna(axis=0))
    mustTakeTermDict.update({key:values})
    
electiveTermDict = {}
for i in range(len(dfElectiveTerms)):
    key = dfElectiveTerms.index[i]
    values = list(dfElectiveTerms.iloc[i].dropna(axis=0))
    electiveTermDict.update({key:values})

# Instantiate problem class
problem = Problem()

# Add Variables 
for k,v in mustTakeTermDict.items():
    problem.addVariable(k, v)
for k,v in electiveTermDict.items():
    problem.addVariable(k, v)

# Define function for checking prerequisites
def prereqCheck(a, b):
    return a < b

# Build constraints
problem.addConstraint(AllDifferentConstraint()) # ensure no retaking of courses
problem.addConstraint(NotInSetConstraint([startTerm]), list(dfPrereqs['course']))

# Ensure all foundational, core, & capstone classes are taken
# as well as allowing any 3 electives to be taken in addition
problem.addConstraint(InSetConstraint(list(range(1,14))), mustTake)

# Ensure no courses are taken before or without satisfying associated prereq's
for k,v in prereqDict.items():
    for a in v:
        problem.addConstraint(prereqCheck, [a, k])

# Solve CSP
sols = problem.getSolutions()
firstSol = sols[0]

# Remove duplicate solutions
for solution in sols:
    for k,v in solution.items():
        if v > 90:
            solution[k] = 90
sols = [dict(s) for s in set(frozenset(d.items()) for d in sols)]

# Format 1st solution for printing
def formatSol(sol):
    df = pd.DataFrame.from_dict(sol, orient='index') # convert dict to df
    df[0] = df[0].map(mapDict)
    df.reset_index(inplace=True)
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df.sort_values([0,'index'], ascending=[True, False], inplace=True)
    df = df[cols]
    df.set_index(df[0], inplace=True, drop=True)
    df.drop(0, 1, inplace=True) # remove column
    df.index.name = None
    return df
dfFirstSol = formatSol(firstSol)

# Print info
print('START TERM =', yearTermList[0])
print('Number of Possible Degree Plans is', len(sols))
print('\nSample Degree Plan:')
print (dfFirstSol.to_string(header=None))