# Overview

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

# Implementation

The main player here is the `Effect` class, which is an implementation of the command pattern used to define a certain action that should be taken as part or whole of an ability.
An `Effect` has a `Trigger`, which comes along with a number of `Validator`s, and some `Targeters`. For Slay the Spire, effects can be added to relics and Statuses. 

As an example, here is the definition for Slay the Spire's relic "Bronze Scales" with the ability "Whenever you take damage, deal 3 damage back". My implementation understands the ability a little differently, but I think still technically correct, "Whenever you take damage from an enemy, deal 3 damage back". Hopefully the code reads fairly straightforwardly. 

```python
bronze_scales = Relic("Bronze Scales").add_effect(
    TakeDamage(3)
    .set_trigger(
        EventTrigger(
            "on_player_post_take_damage",
            PropertyOneOf("source", GameManager().enemies),
        )
    )
    .add_targeter(EventDataPropertyTargeter("source"))
)
```

Here an instance of a Relic is defined. A relic is pretty much just a container for effects, with some interaction with the player when getting equipped. An effect is added with `.add_effect()`, in this case the `TakeDamage` effect. To the effect are added a trigger and a targeter with their respective functions. 

A `Trigger` works with the event system (observer pattern) to determine whether or not its parent effect should activate. A trigger will listen for a certain event, here `on_player_post_take_damage`, 
and when notified, will pass the event data to each of its `Validators`, in this case just one, `PropertyOneOf`. A validator contains a method to determine whether or not the passed in event data matches the certain criteria required for this `Trigger` to activate the parent effect. For Bronze Scales we make sure that the source of the damage was one of the enemies (by pulling the enemy list off of the GameManager singleton).

If all the validators are green, then the effect activates on all the targets found by the `Targeter`. The targeter defines instructions for collecting the correct entities or data to act on. Here, `TakeDamage` will apply to whatever is stored under the "source" property of the event data from the `on_player_post_take_damage` event.

Since this is unique effect, everything is defined with the creation of the relic, but it could very easily be extracted into a keyword.

```python
thorns_keyword = (
    TakeDamage(3)
    .set_trigger(
        EventTrigger(
            "on_player_post_take_damage",
            PropertyOneOf("source", GameManager().enemies),
        )
    )
    .add_targeter(EventDataPropertyTargeter("source"))
)

bronze_scales = Relic("Bronze Scales").add_effect(thorns_keyword)
```
