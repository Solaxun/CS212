"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

mon,tue,wed,thur,fri =  range(5)
people   =  list(itertools.permutations(range(5)))
jobs     =  list(itertools.permutations(range(5))) #didn't understand why this and things
things   =  list(itertools.permutations(range(5))) #had to be set to range(5) and blanks 
                                                   #added below on 40/41.
def logic_puzzle():
    for Hamming,Knuth,Minsky,Wilkes,Simon in people:
        for Laptop,Droid,Tablet,Iphone,_ in things:
            for Programmer,Writer,Designer,Manager,_ in jobs:
                if (Wilkes != Programmer #2
                    and Hamming == Programmer #3
                    and Wilkes == Droid #3
                    and wed == Laptop #1
                    and Writer != Minsky #4
                    and Knuth != Manager #5
                    and Tablet != Manager  #5
                    and Knuth == Simon + 1 #6
                    and Designer != thur  #7 
                    and fri != Tablet #8
                    and Designer != Droid #9
                    and Knuth == Manager + 1
                    and Laptop == Writer #11/1
                    and Wilkes == mon #11/1 
                    and (Iphone == tue or Tablet == tue)
                    ): #12
                    ans = {'Hamming':Hamming,
                            'Knuth':Knuth,
                            'Minsky':Minsky,
                            'Wilkes':Wilkes,
                            'Simon':Simon}
                    return sorted(ans,key=lambda x: ans[x])
print(logic_puzzle())
