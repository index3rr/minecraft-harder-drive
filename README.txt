What is this?
Its a Fat12 Filesystem entirely within minecraft.
anyways more importantly, its not just a fat12 filesystem i built, but a program that connects it to a network drive on my computer, so when i place files on it, baritone automatically builds them here. Essentially im leeching off public mc servers data storage because I feel like it.

Why is this?
Well, I watched a video called "Minecraft is a web server" where this guy makes minecraft into a data storage medium, and connected it in my head to this other video called "Harder drives: Hard drives we didnt want or need" where this guy makes some essoterric storage devices, one of which uses a fat12 filesystem to store data using pings. its a really REALLY good video, go check it out if youre nerdy enough to care about this

Who is this?
Who are you?
Whats going on?
I'm Scared.

When is this?
If you read the project.txt file itll give you a log of me writing about what problems i had on this journey and when.

Where is this?
?? i get that it makes sense to ask all of the W questions but like obviously thats a stupid question bro stfu

How is this?
Basically, I'm using NBDkit with python, connected to a minescript python file using a socket, which handles all the reading/writing using baritone, and creation of schematic files for baritone to read. For a full guide on setup, you can look at "INSTRUCTIONS.txt"
