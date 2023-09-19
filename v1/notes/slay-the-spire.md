## General

- Events like "on_combat_start" are realistically probably something more like "on_state_change" with a validator `EventDataValidator("state_to", "combat")`, or some ENUM value.
  - There will probably be some sort of "upkeep" step where things can happen after the game properly sets things up but before play starts.

## New Terms

- [ ] ToggleEffect
- [ ] SequenceEffect
- [ ] CommandEffect
- [ ] Status / AddStatus

## Relics

**Burning Blood** - At the end of combat, heal 6 HP

```python
Relic("Burning Blood")
.add_effect(
	"on_combat_end",
	StatUpdate("health", 6)
)
.add_targeter(AttachedPlayerTargeter())
```

**Ring of the Snake** - At the start of combat, draw 2 additional cards

_ALT: The first time you draw cards each combat, draw 2 additional cards._

- Option 1: Combine effects that add and remove an effect.
- Option 2: A toggle effect that enables and disables an effect.

```python
Relic("Ring of the Snake")
.add_effect(
	"on_player_pre_draw_cards",
	ToggleEffect(
		EventDataUpdate("number_cards", 2)
		.add_event_validator(AttachedPlayerValidator())
	)
	.add_toggle_on("on_combat_start")
	.add_toggle_off("on_player_post_draw_cards", AttachedPlayerValidator())
)
```

where toggle on and off are defined something like

```python
class ToggleEffect(EffectDecorator):
	def add_toggle_on(event_name, *validators):
		...
	def add_toggle_off(event_name, *validators):
		...
```

**Cracked Core** - At the start of each combat, channel 1 Lightning orb

_See **Bronze Scales** for first thougts on CommandEffect_

```python
Relic("Cracked Core")
.add_effect(
	"on_combat_start",
	CommandEffect(PlayerChannel(1, "lightning"))
	.add_targeter(AttachedPlayerTargeter())
)
```

**Pure Water** - At the start of combat, add 1 Miracle to your hand

```python
Relic("Pure Water")
.add_effect(
	"on_combat_start",
	CommandEffect(PlayerAddToHand(1, CardMiracle()))
	.add_targeter(AttachedPlayerTargeter())
)
```

**Akabeko** - Your first attack each combat deals 8 additional damage

```python
Relic("Akabako")
.add_effect(
	"on_player_pre_attack",
	ToggleEffect(
		EventDataUpdate("damage", 8)
		.add_validator(AttachedPlayerValidator())
	)
	.add_toggle_on("on_combat_start")
	.add_toggle_off("on_player_post_attack", AttachedPlayerValidator())
)
```

**Anchor** - Start each combat with 10 block

```python
Relic("Anchor")
.add_effect(
	"on_combat_start",
	StatUpdate("block", 10)
	.add_targeter(AttachedPlayerTargeter())
)
```

**Ancient Tea Set** - Whenever you enter a rest site, start the next combat with 2 extra energy

```python
Relic("Ancient Tea Set")
.add_effect(
	"on_player_enter_rest_site",
	StatUpdate("energy", 2)
	.add_targeter(AttachedPlayerTargeter())
)

# The sequence is interesting but may require a significaat rework
# Technically everything else is also a sequence of length 1
# There is no event to pass in to add_effect
# I do like the idea of adding events to the effects
Relic("Ancient Tea Set")
.add_effect(
	"",
	SequenceEffect(
		StatUpdate("energy", 2)
		.add_targeter(AttachedPlayerTargeter())
	)
	.add_seq("on_player_enter_rest_site")
	.add_seq("on_combat_start")
)
```

**Art of War** - If you do not play any Attacks during your turn, gain an extra energy next turn

```python
Relic("Art of War")
.add_effect(
	SequenceEffect(
		StatUpdate("energy", 1)
		.add_targeter(AttachedPlayerTargeter())
	)
	.add_seq("on_player_start_turn")
	.add_seq("on_player_end_turn")
	.add_reset("on_player_play_card", PropertyEquals("type", "attack"))
)
```

**Bag of Marbles** - At the start of each combaat, apply 1 💔 Vulnerable to ALL enemies

```python
Relic("Bag of Marbles")
.add_effect(
	"on_combat_start",
	AddStatus(Vulnerable, 1)
	.add_targeter(AttachedPlayerEnemiesTargeter())
)

'''
The status class needs to encapsulate the idea of temporary
effects on a player that can change in intensity over time,
i.e. decrease by 1 every turn or clear after attacking
'''

Status("Vulnerable")
.add_effect(
	"on_player_take_damage",
	EventDataUpdate("damage", MultOp(1.25))
)
.add_change(
	"on_player_end_turn",
	AddOp(-1),
	AttachedPlayerValidator()
)
```

**Bag of Preparation** - At the start of each combat, draw 2 additional cards

_See **Ring of the Snake**_

**Blood Vial** - At the start of each combat, heal 2 HP

_See **Burning Blood**_

**Bronze Scales** - Whenever you take damage, deal 3 damage back.

_ALT: After you are attacked, deal 3 damage back_

This relic requires a way of invoking a method on the target.
COMMANAD PATTERN?

```python
Relic("Burning Blood")
.add_effect(
	"on_player_post_attack",
	CommandEffect(
		PlayerTakeDamage(self, 3) # source, amount
	)
	.add_event_validator(
		PropertyEquals("target", AttachedPlayerTargeter())
	)
	.add_targeter(EventDataTargeter("player"))
)
```

**Centennial Puzzle** - The first time you lose HP each combat, draw 3 cards.

```python
Relic("Centennial Puzzle")
.add_effect(
	"on_player_post_take_damage"
	ToggleEffect(
		CommandEffect(PlayerDrawCards(3))
		.add_event_validator(AttachedPlayerValidator())
	)
	.add_toggle_on("on_combat_start")
	.add_toggle_off(
		"on_player_post_take_damage",
		PropertyInRange("damage", min=1))
)
```

**Ceramic Fish** - Whenever you add a card to your deck, gain 9 gold.

```python
Relic("Ceramic Fish")
.add_effect(
	"on_player_add_card",
	StatUpdate("gold", 9)
	.add_targeter(AttachedPlayerTargeter())
	.add_event_validator(AttachedPlayerValidator())
)
```

**Dream Catcher** - Whenever you rest, you may add a card to your deck.

```python
Relic("Dream Catcher")
.add_effect(
	"on_player_rest",
	CommandEffect(PlayerAddCard(1))
	.add_targeter(AttachedPlayerTargeter())
	.add_event_validator(AttachedPlayerValidator())
)
```

**Happy Flower** - Every 3 turns, gain 1 Energy.

```python
Relic("Happy Flower")
.add_effect(
	"on_player_turn_start"
	Counter(3, StatUpdate("energy", 1))
	.attached_player()
)

'''
.attached_player()

shorthand for

.add_targeter(AttachedPlayerTargeter())
.add_event_validator(AttachedPlayerValidator())

'''
```

_SKIP_ **Juzu Bracelet** - Regular enemy combats aare no longer encountered in ? rooms.

_Requires some interaction with the game systems. Makes more sense for a single player game_

**Lantern** - Gain 1 Energy on the first turn of each combat.

_See **Ancient Tea Set**_

**Maw Bank** - Whenever you climb a floor, gain 12 Gold. No longer works when you spend and Gold at the shop.

```python
Relic("Maw Bank")
.add_effect(
	ToggleEffect(
		"on_player_climb_floor",
		StatUpdate("gold", 12)
		.attached_player()
	)
	.set_toggle(True)
	.add_toggle_off("on_player_shop_purchase")
)
```

**Meal Ticket** - Whenever you enter a shop, heal 15 HP.

```python
Relic("Meal Ticket")
.add_effect(
	"on_player_climb_floor",
	Heal(15)
	.attached_player()
	.add_event_validator(PropertyEquals("dest", "shop"))
)
```

**Nunchaku** - Every time you play 10 Attacks, gain 1 Energy

```python
Relic("Nunchaku")
.add_effect(
	"on_player_play_card"
	Counter(10, StatUpdate("energy", 1))
	.attached_player()
	.add_event_validator(PropertyEquals("type", "attack"))
)
```

**Oddly Smooth Stone** - Aat the start of each combat, gain 1 Dexterity

```python
Relic("Oddly Smooth Stone")
.add_effect(
	"on_combat_start",
	AddStatus(Dexterity, 1)
	.attached_player()
)

'''
Need a way of referencing a status's current value
'''
Status("Dexterity")
.add_effect(
	"on_player_gain_block"
	EventDataUpdate("block", AddOp(AttachedStatusValue()))
)
```

**Omamori** - Negate the next 2 Curses you obtain.

_I set card to None in the event, but there may be a better way to not interfere with other events that may want to know the card_

```python
Relic("Omamori")
.add_effect(
	"on_player_add_card"
	NTimes(2,
		EventDataUpdate("card", None)
		.add_event_validator(PropertyEquals("type", "curse"))
	)
)
```

**Oricalcum** - If you end your turn without Block, gain 6 Block

```python
Relic("Orichalcum")
.add_effect(
	"on_player_end_turn",
	StatUpdate("block", 6)
	.add_event_validator() # <------
)

'''
Need a way of validating using the attached players stats.
Probbly using the player data in the event
'''
```

**Pen Nib** - Every 10th Attck you play deals double damage.

_See **Nunchaku**_
