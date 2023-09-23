## General

Using ideas from existing code to create the relics from Slay the Spire. This will help explore wider range of ideas to inform the future code.

- Events like "on_combat_start" are realistically probably something more like "on_state_change" with a validator `EventDataValidator("state_to", "combat")`, or some ENUM value.
- `on_player_` events will have a default validator of AttachedPlayerValidator() for simplicity unless kwarg `use_defaults=False`

## Relics

### Starter

**Burning Blood** - At the end of combat, heal 6 HP

```python
Relic("Burning Blood")
.add_effect(
	StatUpdate("health", 6)
	.set_trigger(EventTrigger("on_combat_end"))
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
		EventDataUpdate("number_cards", 2)
		.set_trigger(
			Toggle()
            .set_toggle_on(EventTrigger("on_combat_start"))
            .set_toggle_off(EventTrigger("on_player_post_draw_cards"))
			.set_trigger(EventTrigger"on_player_pre_draw_cards"))
        )
	)
)
```

**Cracked Core** - At the start of each combat, channel 1 Lightning orb

Try to utilize the Command design pattern to encapsulate instructions within an object for some yet unspecified target.

```python
Relic("Cracked Core")
.add_effect(
	CommandEffect(PlayerChannel(1, "lightning"))
	.set_trigger(EventTrigger("on_combat_start"))
	.add_targeter(AttachedPlayerTargeter())
)
```

**Pure Water** - At the start of combat, add 1 Miracle to your hand

```python
Relic("Pure Water")
.add_effect(
	CommandEffect(PlayerAddToHand(1, CardMiracle()))
	.set_trigger(EventTrigger("on_combat_start"))
	.add_targeter(AttachedPlayerTargeter())
)
```

### Common

**Akabeko** - Your first attack each combat deals 8 additional damage

```python
Relic("Akabako")
.add_effect(
    EventDataUpdate("damage", 8)
    .set_trigger(
        Toggle()
        .set_toggle_on(EventTrigger("on_combat_start"))
	    .set_toggle_off(EventTrigger("on_player_post_attack"))
        .set_trigger(EventTrigger("on_player_pre_attack"))
    )
)
```

**Anchor** - Start each combat with 10 block

```python
Relic("Anchor")
.add_effect(
	StatUpdate("block", 10)
	.set_trigger(EventTrigger("on_combat_start"))
	.add_targeter(AttachedPlayerTargeter())
)
```

**Ancient Tea Set** - Whenever you enter a rest site, start the next combat with 2 extra energy

```python
Relic("Ancient Tea Set")
.add_effect(
	StatUpdate("energy", 2)
    .set_trigger(
        Sequence()
        .add_seq(EventTrigger("on_player_enter_rest_site"))
        .add_seq(EventTrigger("on_combat_start"))
    )
	.add_targeter(AttachedPlayerTargeter())
)
```

**Art of War** - If you do not play any Attacks during your turn, gain an extra energy next turn

```python
Relic("Art of War")
.add_effect(
	StatUpdate("energy", 1)
	.set_trigger(
		Sequence()
		.add_seq(EventTrigger("on_player_start_turn"))
		.add_seq(EventTrigger("on_player_end_turn"))
		.add_reset(
            EventTrigger(
                "on_player_play_card",
                 PropertyEquals("type", "attack")
            )
        )
	)
	.add_targeter(AttachedPlayerTargeter())
)
```

**Bag of Marbles** - At the start of each combat, apply 1 Vulnerable to ALL enemies

```python
Relic("Bag of Marbles")
.add_effect(
	AddStatus(Vulnerable, 1)
	.set_trigger(EventTrigger("on_combat_start"))
	.add_targeter(AttachedPlayerEnemiesTargeter())
)

'''
The status class needs to encapsulate the idea of temporary
effects on a player that can change in intensity over time,
i.e. decrease by 1 every turn or clear after attacking

.add_change automatically targets itself
'''

Status("Vulnerable")
.add_effect(
	EventDataUpdate("damage", MultOp(1.5))
	.set_trigger(EventTrigger("on_player_take_damage"))
)
.add_change(
	StatUpdate("amount", -1)
	.set_trigger(EventTrigger("on_player_end_turn"))
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
Relic("Bronze Scales")
.add_effect(
	CommandEffect(PlayerTakeDamage(self, 3)) # source, amount
	.set_trigger(
        EventTrigger(
            "on_player_post_attack",
		    PropertyEquals("target", AttachedPlayerTargeter())
            use_default=False
    	)
    )
	.add_targeter(EventDataTargeter("player"))
)
```

**Centennial Puzzle** - The first time you lose HP each combat, draw 3 cards.

```python
Relic("Centennial Puzzle")
.add_effect(
    CommandEffect(PlayerDrawCards(3))
    .set_trigger(
        Toggle()
        .add_toggle_on(EventTrigger("on_combat_start"))
        .add_toggle_off(
            EventTrigger(
                "on_player_post_take_damage",
                PropertyInRange("damage", min=1)
            )
        )
        .set_trigger(EventTrigger("on_player_post_take_damage"))
    )
)
```

**Ceramic Fish** - Whenever you add a card to your deck, gain 9 gold.

```python
Relic("Ceramic Fish")
.add_effect(
	StatUpdate("gold", 9)
	.set_trigger(EventTrigger("on_player_add_card"))
	.add_targeter(AttachedPlayerTargeter())
)
```

**Dream Catcher** - Whenever you rest, you may add a card to your deck.

```python
Relic("Dream Catcher")
.add_effect(
	CommandEffect(PlayerAddCard(1))
	.set_trigger(EventTrigger("on_player_rest"))
	.add_targeter(AttachedPlayerTargeter())
)
```

**Happy Flower** - Every 3 turns, gain 1 Energy.

```python
Relic("Happy Flower")
.add_effect(
	Counter(3, StatUpdate("energy", 1))
	.set_trigger(EventTrigger("on_player_turn_start"))
	.add_targeter(AttachedPlayerTargeter())
)
```

**Juzu Bracelet** - Regular enemy combats are no longer encountered in ? rooms.

_Requires some interaction with the game systems. See **Tiny Chest** for some ideas?_

**Lantern** - Gain 1 Energy on the first turn of each combat.

_See **Ancient Tea Set**_

**Maw Bank** - Whenever you climb a floor, gain 12 Gold. No longer works when you spend and Gold at the shop.

```python
Relic("Maw Bank")
.add_effect(
    StatUpdate("gold", 12)
    .set_trigger(
	    Toggle()
	    .set_toggle(True)
	    .set_toggle_off(EventTrigger("on_player_shop_purchase"))
        .set_trigger(EventTrigger("on_player_climb_floor")))
	)
    .add_targeter(AttachedPlayerTargeter())
)
```

**Meal Ticket** - Whenever you enter a shop, heal 15 HP.

```python
Relic("Meal Ticket")
.add_effect(
	Heal(15)
	.set_trigger(
        EventTrigger(
		    "on_player_climb_floor",
		    PropertyEquals("dest", "shop")
        )
	)
	.add_targeter(AttachedPlayerTargeter())
)
```

**Nunchaku** - Every time you play 10 Attacks, gain 1 Energy

```python
Relic("Nunchaku")
.add_effect(
	Counter(10, StatUpdate("energy", 1))
	.set_trigger(
        EventTrigger(
		    "on_player_play_card",
		    PropertyEquals("type", "attack")
        )
	)
	.add_targeter(AttachedPlayerTargeter())
)
```

**Oddly Smooth Stone** - At the start of each combat, gain 1 Dexterity

```python
Relic("Oddly Smooth Stone")
.add_effect(
	AddStatus(Dexterity, 1)
	.set_trigger(EventTrigger("on_combat_start"))
	.add_targeter(AttachedPlayerTargeter())
)

'''
Need a way of referencing a status's current value
'''
Status("Dexterity")
.add_effect(
	EventDataUpdate("block", AddOp(AttachedStatusValue()))
	.set_trigger(EventTrigger("on_player_pre_gain_block"))
)
```

**Omamori** - Negate the next 2 Curses you obtain.

_I set card to None in the event, but there may be a better way to not interfere with other events that may want to know the card_

```python
Relic("Omamori")
.add_effect(
	NTimes(2, EventDataUpdate("card", None))
	.set_trigger(
        EventTrigger(
            "on_player_add_card",
            PropertyEquals("type", "curse")
        )
	)
)
```

**Oricalcum** - If you end your turn without Block, gain 6 Block

```python
Relic("Orichalcum")
.add_effect(
	StatUpdate("block", 6)
	.set_trigger(
		Sequence()
		.add_seq(EventTrigger("on_player_turn_start"))
		.add_seq(EventTrigger("on_player_turn_end"))
		.add_reset(
            EventTrigger(
                "on_player_post_gain_block"
                PropertyInRange("block", min=1)
            )
		)
	)
	.add_targeter(AttachedPlayerTargeter())
)
```

**Pen Nib** - Every 10th Attck you play deals double damage.

_See **Nunchaku**_

**Potion Belt** - Upon pickup, gain 2 Potion slots

```python
Relic("Potion Belt")
.add_effect(
	NTimes(1, StatUpgrade("potion_slots", 2))
	.set_trigger(
        EventTrigger(
            "on_player_add_relic",
            PropertyEquals("relic", AttachedRelicTargetter())
        )
	)
	.add_targeter(AttachedPlayerTargeter())
)
```

**Preserved Insect** - Enemies in Elite rooms have 25% less HP.

```python
Relice("Preserved Insect")
.add_effect(
	StatUpdate("health", MultOp(0.75))
	.set_trigger(
		Sequence()
		.add_seq(
            EventTrigger(
                "on_player_climb_floor",
                PropertyEquals("dest", "elite")
            )
		)
		.add_seq(EventTrigger("on_combat_start"))
	)
	.add_targeter(AttachedPlayerEnemyTargeter()) #  <-- ?
)
```

**Regal Pillow** - Heal and additional 15 HP when you Rest.

_ALT: Healing from Resting is increased by 15_

```python
Relic("Regal Pillow")
.add_effect(
	EventDataUpdate("amount", 15)
	.set_trigger(
        EventTrigger(
            "on_player_pre_heal",
            PropertyEquals("source", "rest")
        )
	)
)
```

**Smiling Mask** - The Merchant's card removal service now always costs 50 Gold.

- Option 1: Commands to interact with the shop removal prices now and after each purchase
- Option 2: Stratgey for how the shop prices are calculated.

**Strawberry** - Raise your Max HP by 7

```python
Relic("Strawberry")
.add_effect(
	NTimes(1, StatModifierEffect("max_health", 7))
	.set_trigger(
        EventTrigger(
            "on_player_add_relic",
            AttachedRelicValidator()
        )
	)
	.add_targeter(AttachedPlayerTargeter())
)
```

**The Boot** - Whenever you would deal 4 or less unblocked Attack damage, increase it to 5.

Raises the question of how best to define logical combinations of validators.
Here I assume that all validators passed in to `.add_event_validator` must result in True to apply the effect. The `Or()` validator would return True if at least one of its validators is True.

What about effects that trigger off of multiple events??

```python
Relic("The Boot")
.add_effect(
	EventDataUpdate("damage", MaxOp(5))
	.set_trigger(
        EventTrigger(
            "on_player_pre_take_damage",
            AttachedPlayerValidator().invert(),
            Or(
                PropertyEquals("source", AttachedPlayerTargeter()),
                PropertyEquals("source", AttachedPlayerRelicTargeter()),
            )
            use_default=False
        )
	)
)
```

**Tiny Chest** - Every 4th ? room is a Treasure room.

- Option 1: Command to load the type of room
- Option 2: Modify event that loads a room type

```python
Relic("Tiny Chest")
.add_effect(
	Counter(4, CommandEffect(SetNextQuestionRoom("treasure")))
	.set_trigger(
        EventTrigger(
            "on_player_climb_floor",
            PropertyEquals("dest", "?")
        )
	)
)

Relic("Tiny Chest")
.add_effect(
	EventDataUpdate("type", "treasure")
	.set_trigger(
		Sequence()
		.add_seq(
            EventTrigger(
                "on_player_climb_floor",
                PropertyEquals("dest", "?"),
                repeat=4
		    )
        )
		.add_seq(EventTrigger("on_pre_room_load"))
	)
)
```

**Toy Ornithopter** - Whenever you use potion, heal 5 HP.

```python
Relic("Toy Ornithopter")
.add_effect(
	Heal(5)
	.set_trigger(EventTrigger("on_player_pre_potion"))
)
```

**Vajra** - At the start of each combat, gain 1 Strength

_See **Bag of Marbles**_

**War Paint** - Upon pick up, Upgrade 2 random Skills

Again we see that more complicated targeters are required with logical combinations.
Not satisfied with this but will hve to see more examples.

```python
Relic("War Paint")
.add_effect(
	CommandEffect(UpgradeCard())
	.set_trigger(
        EventTrigger(
            "on_player_add_relic",
            AttachedRelicValidator()
        )
	)
	.add_targeter(
		Random(2,
			AttachedPlayerCardsTargeter()
			.where("type", "skill")
			.where("upgraded", False),
			unique=True
		)
	)
)
```

**Red Skull** - While your HP is at or below 50%, you have 3 additional Strength.

Seems like a toggle since it should only happnen once each way. Losing health while already below threshold doesnt give even more strength. But how to remove strength when toggles off?

- Option 1: 2 separate toggle effects that act in reverse, one adds Strength one removes
- Option 2: Optional on_enable, on_disable effects for a toggle.

**Sneko Skull** - Whenever you apply Poison, apply an additional 1 Poison.

**Data Disk** - Start each combat with 1 Focus

**Damaru** - At the start of your turn, gain 1 Mantra

### Uncommon

The ones interesting in terms of unique effects for this system.

**Eternal Feather** - For every 5 cards in your deck, heal 3 HP whenever you enter a Rest site.

Need a way of calculating properties on a target.

**Horn Cleat** - At the start of your 2nd turn, gain 14 block.

Turn start sequence with repeater, reset on combat start.

**Meat on the Bone** - If your HP is at or below 50% at the end of combat, heal 12 HP.

Requires some calculation off of player properties in validator.

**Strike Dummy** - Cards containing 'strike' deal 3 additional damage.

Filtered targeter

**Paper Phrog** - Enemies with Vulnerable take 75% more damage rather than 50%.

Stat modifier on a status?

**Self-Forming Clay** - Whenever you lose HP in combat, gain 3 Block next turn.

Gaining stats next turn is a mechanic that would have a command associated with it.
Combat HP is a toggle for combat then an effect on lose HP.

**Paper Krane** - Enemies with Weak deal 40% less damage rather than 25%.

_See **Paper Frog**_

**Duality** - Whenever you play an Attack, gain 1 temporary Dexterity

Some sort of temporary status mechanics. Perhaps a decorator.

### Rare

The ones interesting in terms of unique effects for this system.

**Du-Vu Doll** - For each Curse in your deck, start each combat with 1 additional Strength

_See **Eternal Feather**_

**Ginger** - You can no longer become Weakened.

Cancel out some sort of on_add_status event

**Pocketwatch** - Whenever you ply 3 or less cards during your turn, draw 3 additional cards at the start of your next turn.

Indeterminate number of events for a sequence.

**Unceasing Top** - Whenever you have no cards in hand during your turn, draw a card.

Is there an event for this? Perhaps a post play card event that triggers after everything is worked out.

**The Specimen** - Whenever an enemy dies, transfer any Poison it has to a random enemy.

**Tingsha** - Whenever you discard a card during your turn, deal 3 damage to a random enemy for each card discarded.

Im reading this as the first discard is 3, the second is 3 + 3, etc. so there needs to be a way of counting events and accessing that value.

In the wiki there is a patch for changing the target of the damage if the current target dies while taking damage.

### Shop

**Orange Pellets** - Whenever you play a Power, Attack, and Skill in the same turn, remove all of your debuffs.

Checklist of events, can be done in any order.
