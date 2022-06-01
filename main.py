import numpy as np
import pandas as pd
from algorithm import Matching, Group
import sys

# Group size is 4
groupSize = 4

#Student Groups list
studentGroups = []

# Check if there is a CSV file with the list of students and their preferences
if len(sys.argv) < 2:
    print("Please input a CSV file with students and their preferences.")
    sys.exit()
else:
    # Import the list of students as a Pandas dataframe
    studentsDf = pd.read_csv(sys.argv[1], header=0)


dfUnderClassmenBoys = studentsDf[
    (studentsDf["Grade"] < 11) & (studentsDf["Gender"] == "Male")
].reset_index()
dfUnderClassmenBoys.name = "Underclassmen Boys"

dfUnderClassmenGirls = studentsDf[
    (studentsDf["Grade"] < 11) & (studentsDf["Gender"] == "Female")
].reset_index()
dfUnderClassmenGirls.name = "Underclassmen Girls"

dfUpperClassmenBoys = studentsDf[
    (studentsDf["Grade"] >= 11) & (studentsDf["Gender"] == "Male")
].reset_index()
dfUpperClassmenBoys.name = "Upperclassmen Boys"

dfUpperClassmenGirls = studentsDf[
    (studentsDf["Grade"] >= 11) & (studentsDf["Gender"] == "Female")
].reset_index()
dfUpperClassmenGirls.name = "Upperclassmen Girls"

gradeGenderDfs = [
    dfUnderClassmenBoys,
    dfUnderClassmenGirls,
    dfUpperClassmenBoys,
    dfUpperClassmenGirls,
]

for df in gradeGenderDfs:
    if df.shape[0] <= 0:
        continue

    # Initialize a matrix of student preferences with the default value of 0 (no preference)
    studentPrefMatrix = np.zeros((df.shape[0], df.shape[0]), dtype=float)

    for idx in df.index:
        row = df.loc[idx]
        student = row["Email Address"]
        prefs = [
            row["Roommate Preference #1 Email"],
            row["Roommate Preference #2 Email"],
            row["Roommate Preference #3 Email"],
        ]

        for pref in prefs:
            # if the prefrence is in the dataset and student is not the same as the prefrence
            if (
                df[df["Email Address"] == pref].index.values.size > 0
                and pref != student
            ):

                studentPrefMatrix.itemset(
                    (
                        df[df["Email Address"] == pref].index[0],
                        df[df["Email Address"] == student].index[0],
                    ),
                    (10 - (prefs.index(pref) * 3)),
                )
            else:
                print(f"{student} has no preference {prefs.index(pref)+1} or is the same as the prefrence: {pref}")

    # Running Irving's algorithm
    matching = Matching(
        studentPrefMatrix, group_size=groupSize, iter_count=2, final_iter_count=2
    )
    score, studentIdxs = matching.solve()
    print(f"Irving's Algorithm Score for {df.name}: {score}")

    # Converting list of student indexes to list of student names
    for group in studentIdxs:
        studentGroup = []
        for studentIdx in group:
            studentGroup.append("Full Name: %s, Gender: %s, Grade: %s" % (df.iloc[studentIdx]["Full Name"], df.iloc[studentIdx]["Gender"], df.iloc[studentIdx]["Grade"]))
        studentGroups.append(studentGroup)

df = pd.DataFrame(data=studentGroups)
df.to_csv('rooms.csv',index=True, header=False)
