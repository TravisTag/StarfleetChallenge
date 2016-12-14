# StarfleetChallenge
Code and information for a programming challenge from CognitiveScale

### Design decisions
My first decision upon reading the problem was how to represent the field while running the simulation.
Given the output requirement of printing the field relative to the ships location, the idea of maintaining an array similar to the way it is given was unattractive, as this would result in consant resizing and moving of elements.
Instead, I noticed the similarity between the technically infinite field and a sparse array, an array with relatively very few non-zero elements.
Sparse arrays are often represented by only keeping the locations and values of non-zero elements, for convenience and efficiency.
Going beyond this, since the firing patterns and field printing are considered relative to the ship's location, it made sense to only maintain the relative positions of the mines as well.

When thought of in this way, there is no need to even maintain the absolute position of the ship, everything I need to do is relative to the ships location.

I then decided to create a simple class for the simulation that could be instantiated with the field, and then fed commands while it keeps track of these locations, penalties, etc.


### Implementation
I chose Python for this challenge because I am comfortable with it, and the problem doesn't seem to benefit from the advantages of any of the other languages I am comfortable with.
