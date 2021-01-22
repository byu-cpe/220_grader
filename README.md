# Running the Goeders Assignment Grading Script
This script helps with streamlining TA grading of assignments.  For full automation, the student work must either be gathered from Learning Suite or github.

1. If from LearningSuite it must be a normal homework assignment where the students attach a ZIP file of their work.  LearningSuite exams don't work.
2. If from github, each student has to have a github repo where their work is.  They must use the right directory structure so the scripts can navigate and find it.

To set up to run, you will need to do a few things:

1. You need to install the python pandas package using `python3 -m pip install pandas`
2. You will need to create a Labs.csv file (like the one there).  See instructions below.  Once you have created it, you then code the path to this file into run_passoff.py so it can find it.
3. You also code the path to the ZIP file containing the student ZIP files into run_passoff.py.
4. You then run it as `python3 run_passoff.py Lab9` (or whatever lab name you want from the the columns of the csv file).  This will do the following:
    - Create a Lab9_passoff directory and unzip the Lab9.zip into it.  That should result in a file for each student of the form: FirstName_LastName_netid_Lab9.zip
    - It will then unzip each student zip into its own directory
    - It will then check the Labs.csv file for students who need scores 
    - For each such student it will first call the `run_on_lab` routine if that callback is defined. 
        - For instance you could have it open up VS Code with all the source code files in the student's directory so you can view it.  
    - After running the callback, you are asked for a score and that is entered into the Labs.csv file.

# Explanation

So, the big idea is that it unzips the student work, does the callback, and then asks for a score.  This is all done only for students without a score in the Labs.csv file.  So, you can call it as often as you like and if new student work shows up in the zip file, you will be asked for a score for it.  

Once you have the csv file with all the needed scores, you can re-import the scores into LearningSuite using the following steps:
- TBD

What to do if you later want to re-grade something?  I assume you would remove that student's score from Labs.csv and simply re-run.

The Goeders 427 sample run_passoff.py is more complex than this (I simplified it).  It has at least the following features I didn't use:
- It assumes that there is a separate csv file for each lab rather than putting them all in one csv file.  
- It also assumes those are off in a sub-directory and it uses a function call to get the path for those given a lab name from the command line.
- It uses function names to map the Lab name you specify on the command line to whatever name really exists in the csv file column headers.  This will allow you to have spaces in the LearningSuite lab names but just specify a single word when you run on the command line.
- It has provisions for groups of students to work together and have them get a group score.
- It has provisions for milestone passoffs as well as lab passoffs.
- It uses more complicated callbacks to actually compile and run the students' code.
- It has 2 grading scripts - one for coding standard and one for passoffs.  

Any of the above features could be adopted if desired.  Specifically, if a coding standard automated program were created it could be called in the coding standard program callback.

# Making the Labs.csv File
As you can see from the sample file, the first row lists the column names for the rest of the file.  It is best that the column headings don't have spaces in the names.

The first 3 columns are required to be there and in that order (Last name, first name, BYU ID).   The others are the names of the labs.  If you create it by hand, don't put in spaces after the commas, do it as shown in this sample:

``` csv
"Last Name","First Name","Net ID","Course Homework ID","Section Number","Lab0","Lab1","Lab3","Lab4","Lab5","LabSim","Lab6","Lab7","Lab8","Lab9","Lab10","Lab11"
"Smith","John","js","509BC75","001",
"Wilson","Steve","sw","22067AE", "002",
```

You can get such a file for your class from LearningSuite by going to BYU Grades->Export. Then, select the lab passoff assignments.  Then, down below under student information select "Last name, preferred name" as well as "Section Number" and "Course Homework ID".  The defaults are OK for everything else.  The result will be a csv file with the needed information.  Rename it and place it into a directory and then add the path to run_passoff.py.

# Making the .zip File of Student Work
To create a test file representing student work, let's assume you have a directory with files `top.sv` and `decode.sv` in it.  To create the needed zip file you would do this:
```
cd directoryWithFiles
zip ../John_Smith_js223_Lab9.zip *.sv
cd ..
```
You do this for each student's directory and now will have a set of ZIP files you have created.
Then, create a ZIP file of thos with something like:

```
zip Lab9.zip John_Smith_js223_Lab9.zip Steve_Wilson_sw12_Lab9.zip
``` 
where you include all the needed ZIP files.   Or, you could do: `zip Lab9.zip *.zip`.  The result is a ZIP file of ZIP files in the format the tool wants.  Note: do not use the Mac's 'Compress' tool to create this - it puts in extra directory layers that makes it not work.

When you get ready to actually do it for real student work, you can extract such a ZIP file from LearningSuite via the following steps (remember that this only works for Homework assignments where the student have been asked to attach a ZIP of their work, it does not work for Exam assignments):

Step 1. TBA
Step 2. TBA
    
# A Sample Setup
1. Put the .csv file in the main directory.
2. Add its name to the run_passoff.py where you are creating the Grader object (about line 85).
3. Put the ZIP file of ZIP files you created into the main directory.
4. Add its name to the run_passoff.py program where you are creating the Grader object (about line 92).
5. Modify the callback if you want it to do something.  Or, you could replace its body with a `return`.  Or, you could not define it when creating the Grader object (remove line 91 where it defines `run_on_lab`).
6. Run it as `python3 Lab9`.  You should see that a `Lab9_passoff` directory gets created and the student ZIP files get placed there.  You should then be asked for student grades for the ones that don't have scores.  You will see that the student zip file has been expanded in Lab9_passoff and you can do anything you want with those files to decide on a grade.  

## Obvious Enhancements
1. Use a separate CSV file for each lab.  In this case it need not have columns for all labs, just the one of interest.  
2. Put those CSV files into a directory to keep things clean.  Goeders' original 427 system does that - look at that code for ideas on how the code finds them.
3. Since you have to have a separate ZIP file for each lab, create a directory to hold them and modify the code to go look for them.
4. The Goeders 427 example maps lab names you type when you run on the command line to actual column names in the CSV file - this allows for column names with spaces in the titles.  Compare to the 427 example to see how that was done.
5. Add more labs to the various data structures.
6. Make it so each lab has a different # of points possible.
7. Create a real callback to help with grading.  The obvious thing to do would be to have the python code automatically fire up VS Code in the directory where the student's .sv files are so the TA could just look through them quickly and come up with a grade.
8. Figure out a way that a TA can provide feedback.  It could be manual in LearningSuite (it allows that for Homework assignments), but it could also be done some other way.  One idea: if each student had a unique homework ID, you could publish the entire class's feedback where each student's feedback was associated with his homework ID.  This would let the student see it but it would be confidential.  To do this you could have the TA manage a big text file with all the feeeback or modify the grader to actually add feedback the TA typed into the file.   Also, to do this you would want to include the student's homework ID in the CSV file (it is an option).