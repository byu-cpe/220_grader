# Running the Assignment Grading Script
This script helps with streamlining TA grading of assignments.  For full automation, the student work must either be gathered from Learning Suite or github.

1. If from LearningSuite it must be a normal homework assignment where the students attach a ZIP file of their work.  LearningSuite Exams don't currently work.
2. If from github, each student has to have a github repo where their work is.  They must use the right directory structure so the scripts can navigate and find it.

# Installation and Running Sample Dataset
You likely have already cloned this repo but here is the whole set of steps:

```
git clone https://github.com/byu-cpe/220_grader
cd 220_grader
make install
make sample
```

If you look in `Makefile` you will see how `make sample` actually just runs `python3 run_passoff.py Lab9`.  This does the following:

- Creates a Lab9_passoff directory and unzips the `Lab9.zip` into it.  That should result in a file for each student of the form: FirstName_LastName_netid_Lab9.zip
- Then unzips each student zip into its own directory
- Then checks the `Labs.csv` file for students who need scores 
- For each such student, it will first call the `run_on_lab` routine if that callback is defined. 
    - For instance you could have it open up VS Code with all the source code files in the student's directory so you can view it.  
- After running the callback, you are asked for a score and that is entered into the `Labs.csv` file.

## Re-Running It
Every time you run it, if there are new students' work in the .zip file, then you can grade those and it will just add their scores to the .csv file.  It will not ask you to regrade work for students who already have a grade.

What to do if you later want to re-grade something?  You could remove that student's score from `Labs.csv` and simply re-run.

Eventually you can import the .csv file information back into the LearningSuite Gradebook.

**TODO: document how to re-import scores into LearningSuite.**


The Goeders `byu-cpe/ecen427_grader` repo's `sample run_passoff.py` program is more complex than this (I simplified it).  It has at least the following features I didn't use:
- It assumes that there is a separate csv file for each lab rather than putting them all in one csv file.  
- It also assumes those are off in a sub-directory and it uses a function call to get the path for those given a lab name from the command line.
- It uses function names to map the Lab name you specify on the command line to whatever name really exists in the csv file column headers. 
- It has provisions for groups of students to work together and have them get a group score.
- It has provisions for milestone passoffs as well as lab passoffs.
- It uses more complicated callbacks to actually compile and run the students' code.
- It has 2 grading scripts - one for the coding standard and one for passoffs.  

Any of the above features could be adopted if desired. 

# The `Labs.csv` File
As you can see from the sample file, the first row lists the column names for the rest of the file.

The first 3 columns are required to be there and in that order (Last name, first name, BYU ID).   The others are the names of the labs.  If you create it by hand, don't put in spaces after the commas, do it as shown in this sample:

``` csv
"Last Name","First Name","Net ID","Course Homework ID","Section Number","Lab0","Lab1","Lab3","Lab4","Lab5","LabSim","Lab6","Lab7","Lab8","Lab9","Lab10","Lab11"
"Smith","John","js","509BC75","001",
"Wilson","Steve","sw","22067AE", "002",
```

## Obtaining a `Labs.csv` File for a Class
You can get such a file for your class from LearningSuite by going to BYU Grades->Export. Then, select the lab passoff assignments you want included (doing then one at a time makes a lot of sense).  Then, down below under student information select "Last name, preferred name" as well as "Section Number" and "Course Homework ID".  The defaults are OK for everything else.  The result will be a csv file with the needed information.  Rename it and place it into a directory and then add the path to run_passoff.py.

# Making the .zip File of Student Work
To create a test ZIP file representing student work, let's assume you have a directory with files `top.sv` and `decode.sv` in it.  To create the needed zip file you would do this:
```
cd directoryWithFiles
zip ../John_Smith_js223_Lab9.zip *.sv
cd ..
```
You do this for each student's directory and now will have a set of ZIP files you have created.
Then, create a ZIP file of those with something like:

```
zip Lab9.zip John_Smith_js223_Lab9.zip Steve_Wilson_sw12_Lab9.zip
``` 
where you include all the desired student ZIP files.   

Or, you could do: `zip Lab9.zip *.zip`.  Either way the result is a ZIP file of ZIP files in the format the tool wants.  Note: do not use a GUI-based 'Compress' tool (like on the Mac) to create this - it puts in extra directory layers that makes it not work.

## Obtaining a .zip File of Student Work for a Specific Lab
When you get ready to actually do it for real student work, you can extract such a ZIP file from LearningSuite via the following steps (remember that this only works for Homework assignments where the student have been asked to attach a ZIP of their work, it does not work for Exam assignments):

TODO: document how to do this.
    
# Changing Things Up With a New .csv and .zip File
1. Put the .csv file wherever you want.
2. Add its path to the run_passoff.py program where you are creating the Grader object.
3. Put the ZIP file of ZIP files you have wherever you want.
4. Add its path to the run_passoff.py program where you are creating the Grader object.
5. Modify the callback if you want it to do something.  Or, you could replace its body with a `return`.  Or, you could not define it at all when creating the Grader object (remove it from the Grader object creation call - it will default to `None`).
6. Run things as `python3 labName`.  You should see that a `labName_passoff` directory gets created and the student ZIP files get placed there.  You should then be asked for student grades for the ones that don't have scores.  You will see that the student zip file has been expanded in `labName_passoff` and you can do anything you want with those files to decide on a grade.  

# Obvious Enhancements
1. Use a separate CSV file for each lab.  In this case it need not have columns for all labs, just the one of interest.  
2. Put those CSV files into a directory to keep things clean.  Goeders' original 427 system does that - look at that code for ideas on how the code finds them.
3. Since you have to have a separate ZIP file for each lab, create a directory to hold them and modify the code to go look for them.
4. The Goeders 427 example maps lab names you type when you run on the command line to actual column names in the CSV file.  Compare to the 427 example to see how that was done.
5. Add more labs to the various data structures.
6. Make it so each lab has a different # of points possible (it is in the run_passoff.py code).
7. Create a real callback to help with grading.  The obvious thing to do would be to have the python code automatically fire up VS Code in the directory where the student's .sv files are so the TA could just look through them quickly and come up with a grade.  Should be straightforward.
8. Figure out a way that a TA can provide feedback to students.  One idea: if each student had a unique homework ID (which they do), you could publish the entire class's feedback where each student's feedback was associated with his/her homework ID.  This would let the student see it but it would be confidential.  To do this the TA could manage a big text file with all the feeeback in it for a lab.  Or, you could modify the grader to actually ask the TA for feedback to add into the file.   