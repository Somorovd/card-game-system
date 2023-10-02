# README

For a long time I have been interesting in deck building and trading card games (real and digital) such as Magic: The Gathering, Dominion, Ascension, Slay the Spire, Inscryption, and many more,
as well as Rouge-like games such as Enter the Gungeon, Into the Breach, Risk of Rain, Peglin etc. etc. In the future I would love to design a similar style game. 

I started by doing some research into how one could go about implementing a card game with many cards and many keywords. There were many tutorials on how to set up a card game 
so that you could draw and play cards in turns, but very little about actually getting into the meat of the game itself. At the same time I was reading the Design Patterns book by
the Gang of Four, which I found thoroughly fascinating, so I decided to try and apply the newly learned patterns to make a little system for myself to help build a game. 

2 main concerns I wanted to address going in were:
1. How can I use effects without having to rely on large branching if statements to check for all possible keywords and status effects?
    * Use the observer pattern at strategic points to allow any effects to interupt and/or modify the flow
2. How can I define the behavior of a keyword in one place and add it to any card or relic I wanted without the need to repeat the code?    
    * Command and Strategy pattern for keywords. Builder (maybe?) pattern to construct different cards/relics with keywords.
  
For now, in this little playground, I am working in python since prototyping and iteration is quite quick, 
but in the future I would like to implement a similar system with a strongly typed language. 
