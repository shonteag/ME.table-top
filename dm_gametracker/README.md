

DOC

ClassHandler.py
    Object: ClassXmlHandler
      Reads in class details ('xml/class.xml') and generates a dictionary of searchable class information.
      Should only be accessed internally.

    Object: ClassHandler()
      Can be accessed externally to gather necessary class-related information.
      See 'xml/class.xml' for relevant CLASS_KEY and class details.

    print_class_details(class_key=CLASSKEY)
      Outputs to stdout. Prints all loaded classes and details for those classes. (Unlockable powers, weapon slots, etc.)

    get_class_details(class_key=CLASSKEY)
      Returns a dictionary with the relevant class-specific values. The dictionary is keyed based on the xml file, and the keys correspond to all keys within the "<class>" wrappers.
      Special Case: The value for the "powers" key is a list of strings. These strings are power_key's which can be used to access the PowerHandler for more details.


PowerHandler.py
    Object: PowerXmlHandler()
      Reads in powers from xml file ('xml/power.xml').
      Should only be accessed internally.

    Object: PowerHandler()
      Used externally to lookup power details based on power_key value(s).
      See 'xml/power.xml' for relevant POWER_KEY and power details.

      print_power_details()
        This prings all powers loaded by the handler. Output is to stdout.

      get_power_details(power_keys=[POWER_KEY, POWER_KEY, ...])
        This takes a list of POWER_KEYS as input and returns a dictionary populated with information keyed by the provided POWER_KEYs.
        NOTE: power_keys MUST BE A LIST!

      get_type_powers(power_type)
        Takes a string as argument. Must be either 'biotic' or 'tech'.
        Returns a dictionary populated with all powers of the specified type (and all their details).
 
      get_power_type(power_key)
        Takes a POWER_KEY as an argument, and returns 'biotic' or 'tech'.


!!!NOTE!!!
For ClassHandler and PowerHandler, if you add a key in the corresponding XML files, it will be loaded into the dictionary as a key-value pair.
So, for instance, to add and intelligence modifier to the Engineer class, open xml/class.xml, find the "class" entry corresponding to Engineer, and add the tag
"<\intelligence_modifier>5</\intelligence_modifier>"
Now when you load classes, the class dictionaries will include a new key "intelligence_modifier" and will have the value 5.



Enemy.py
    Object: Enemy(name=str,
                  class_key=CLASSKEY,
                  race=str,
                  role=str,
                  level=int,
                  difficulty=int,
                  max_health=int,
                  max_shield=int,
                  shield_recharge=int,
                  damage_reduction=int,
                  weapons=None, **Not implemented yet**
                  powers=list[power_key, power_key, ...],
                  description=str,
                  power_handler=PowerHandler(),
                  class_handler=ClassHandler(),
                  weapon_handler=WeaponHandler())
    This object has alot of arguments when intializing. They are relatively self-explanatory.
    power_handler, class_handler, weapon_handler must be pre-initialized instances of each of the necessary types.
    Object can be accessed externally.

    _setup_powers()
      Method initializes the cooldown tracker. When a power is used, it's value in the cooldown tracker is set to it's cd value (access via the PowerHandler), and is decremented by 1 every turn.
      Internal use only.

    use_power(power_key)
      Simulate power use by this enemy. Sets cooldown tracker for this power.

    enemy_cast_on_self(power_key)
      Simulates a player casting a power on this enemy. If the power is a dot, it is added to the negative effects tracker with a value of the power duration (decremented by 1 each turn).
      Similarly, if the power is a tech/biotic primer, this instance of Enemy is given a tech/biotic state.
      If power is a tech/biotic detonator, it will cause detonation and un-prime this Enemy for its specified power type.

    take_damage(amount, source=str)
      Simulates this Enemy instance taking damage: power, weapon, dot, etc.). Damages shielding first, and if shield breaks, bleeds over into health.
      NOTE: Still needs to use damage reduction.

    new_turn()
      Simulates a new turn. Several tasks completed:
        - DOTs tick for specified damage (accessed via PowerHandler)
        - DOT durations decreased by 1
        - Biotic/Tech primes decreased by 1
        - Cooldowns decreased by 1
        - Shield increased by this Enemy's 'shield_recharge' value.


Encounter.py
TODO



Dependancy Chart

           tracker.py
           /        \
          /          \
       Encounter     Scaler
               \
                \
                Enemy
                /  |\
               /   | \
   PowerHandler    | ClassHandler
                   |
             WeaponHandler