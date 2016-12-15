# StarfleetChallenge
Code and information for a programming challenge from CognitiveScale

### Design decisions
My first decision upon reading the problem was how to represent the field while running the simulation.
Given the output requirement of printing the field relative to the ship's location, the idea of maintaining an array of the relevant part of the field was unattractive, as this would result in constant resizing and moving of elements.

Instead, I noticed the similarity between the technically infinite field and a sparse array, an array with relatively very few non-zero elements.
Sparse arrays are often represented by only keeping the locations and values of non-zero elements, for convenience and efficiency.
Going beyond this, since the firing patterns and field printing are considered relative to the ship's location, it made sense to only maintain the relative positions of the mines as well.

When thought of in this way, there is no need to even maintain the absolute position of the ship, everything I need to do is relative to the ship's location.

I then decided to create a simple class for the simulation that could be instantiated with the field, and then fed commands while it keeps track of these locations, score, number of mines left, etc.


### Implementation
I chose Python for this challenge because at the moment it is my most frequently used language, and the problem doesn't seem to benefit from the advantages of any of the other languages I am comfortable with.
Of course, a purely object oriented language would maybe make more sense, but with the simplicity of this problem, I think Python offers enough structure.

I had a few choices to make during implementation.
The main one was how to actually store the relative locations of the mines.
For readability, I chose to make a simple Mine structure/object, which contains a NumPy array for the [x, y], and an int for the depth.
I used NumPy arrays for the relative locations and movement vectors to facilitate simple element-wise addition and comparison.

Due to the representation of the problem I chose, movement can be performed by subtracting the movement vector from each mine's relative location, and checking if a torpedo hit a mine can be performed by comparing the relative locations of the torpedoes to the relative locations of the mines.
Descending into the cuboid is performed by decreasing the relative depth of each mine by 1 each step.

### Notes
- I used Python 3 for this, but tested it with Python 2.7.5 as well, so it should work with either, provided NumPy is installed.

- As defined, the program, challenge.py, takes 2 command line arguments: the field file and script file names in order, so simply run:

 python challenge.py fieldfile scriptfile

- The line that converts the depth as a character into an integer is strange because in ASCII lowercase letters have higher values than capital letters. I could have just as easily calculated the value procedurally, but I thought it would be more fun to use 1 equation that worked over both ranges using modulus division.

- Not to nitpick, and I hope this doesn't come across as rude, but the definitions of north and south as incrementing and decrementing y, respectively, are backwards with respect to the examples given. I think it's clear what you were looking for by the examples and example I/O, but I just thought you might want to know!

- Overall, I found this problem very interesting to think about, particularly how to represent the problem while solving it. Thank you for the opportunity to share some code and thoughts with you all.
