"""
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating 
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.
(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.
(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.
(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)
For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.

"""
#need accurate framecount bc 10th frame is diff for longer games (less strikes)
def bowling(balls):
    "Compute the total score for a player's game of bowling."
    ## bowling([int, ...]) -> int
    cur_pos = 0
    frame = 1
    points = 0
    bonus = {} #dict of index:lookforward
    while cur_pos < len(balls)-1:
        if balls[cur_pos] + balls[cur_pos+1] == 10:
            points += balls[cur_pos] + balls[cur_pos+1]
            bonus[cur_pos] = (cur_pos+2,1) #(start index of bonus, lookforward)
            cur_pos += 2
            frame += 1
        elif balls[cur_pos] + balls[cur_pos+1] < 10:
            points += balls[cur_pos] + balls[cur_pos+1]
            cur_pos += 2
            frame += 1
        else:
            points += balls[cur_pos]
            if frame < 10:
               bonus[cur_pos] = (cur_pos+1,2)
            if balls[cur_pos] + balls[cur_pos+1] == 20 and cur_pos == len(balls)-2:
                points+=10 #ugly hack to get last element since this branch doesn't compare next element
            cur_pos += 1
            frame += 1
    bonus_points = []
    for i in bonus:
        start,lookforward = bonus[i]
        bonus_points.append(sum(balls[start:lookforward+start]))
    return sum(bonus_points) + points

def test_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])
    print('tests pass!')
# test_bowling()

def better_bowling(balls,frame=1):
    if frame == 10: #10th frame don't accumulate bonusa
        return sum(balls)
    if len(balls) < 2: 
        return sum(balls)
    if balls[0] + balls[1] == 10:
        return (balls[0] + balls[1] 
                         + better_bowling(balls[2:3]) 
                         + better_bowling(balls[2:],frame+1))
    elif balls[0] + balls[1] < 10:
        return (balls[0] + balls[1] 
                         + better_bowling(balls[2:],frame+1))
    else:
        return (balls[0] + better_bowling(balls[1:2])
                         + better_bowling(balls[2:3]) 
                         + better_bowling(balls[1:],frame+1))

def test_better_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])
    print('tests pass!')
test_better_bowling()
# print(better_bowling([10] * 12))#300
# print(better_bowling([4] * 20))#80
# print(better_bowling([9,1] * 10 + [9]))#190
# print(better_bowling([0,0] * 9 + [10,1,0]))#11

def bowling(balls):
    "Compute the total score for a player's game of bowling."
    ## bowling([int, ...]) -> int
    total = 0
    for frame in range(10):
        score, balls = score_frame(balls)
        total += score
    return total

def score_frame(balls):
    "Return two values: (score_for_this_frame, remaining_balls)."
    n_used, n_scoring = ((1, 3) if balls[0] == 10 # strike
                    else (2, 3) if balls[0] + balls[1] == 10 # spare
                    else (2, 2)) # open frame
    return (sum(balls[:n_scoring]), balls[n_used:])



