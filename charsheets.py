# This file contains the models for the document object, CharacterSheets for Dungeons & Dragons. It is kept separated in this file because of separations
# of concerns, as this is a complex data-object with multiple nested arrays and embedded dicts, not to mention subfields for rendering, it would quickly make app.py unreadable.

from flask_wtf import *
from user import User
from flask_mongoengine import MongoEngine, Document
from flask_mongoengine.wtf import model_form
from wtforms import *
from wtforms.widgets import ListWidget, CheckboxInput, TableWidget
from wtforms.validators import *
from wtforms import *
from flask_wtf.form import *
from wtforms.fields.html5 import *
from wtforms.widgets.html5 import *
db = MongoEngine()

# 'Attributes' are a dict of ints that can range from 1 to 20. All characters have a set of Attributes within this range. This will be passed
# to a jQuery script that will then calculate required values based on these database posts. As those values can be modified so frequently
# and are calculated from the base-attribute value, it is preferable to defer the modifier to the FrontEnd to save on r/w operations.


class CharAttributes(db.EmbeddedDocument):
    strength = db.IntField(min_value=1, max_value=20)
    dexterity = db.IntField(min_value=1, max_value=20)
    constitution = db.IntField(min_value=1, max_value=20)
    intelligence = db.IntField(min_value=1, max_value=20)
    wisdom = db.IntField(min_value=1, max_value=20)
    charisma = db.IntField(min_value=1, max_value=20)

# Saves is a list of booleans, represented in HTML as checkboxes. A save in the context of the rules is either true or false. If true, it adds a bonus based on
# proficiency modifier. As the modifier is calculated on the front-end, the database need only pass True or False to the front-end.


class Saves(db.EmbeddedDocument):
    StrSave = db.BooleanField()
    DexSave = db.BooleanField()
    ConSave = db.BooleanField()
    IntSave = db.BooleanField()
    WisSave = db.BooleanField()
    ChaSave = db.BooleanField()

# 'Skills' is a boolean list, represented in HTML as checkboxes. All characters use the list of skills, so it is a separate embedded document like attributes.
# The user will mark a number of skills as 'proficient' and when the data is passed to the front-end, values will be generated using jQuery
# to accurately calculate the exact numeric value based on proficiency. As this number can value based on modifiers, it is not worth writing exact
# numbers into the DB there, you can get accurate data for our purposes knowing just if it is proficient or not.


class Skills(db.EmbeddedDocument):
    Athletics = db.BooleanField()
    Acrobatics = db.BooleanField()
    Sleight = db.BooleanField()
    Stealth = db.BooleanField()
    Arcana = db.BooleanField()
    History = db.BooleanField()
    Investigation = db.BooleanField()
    Nature = db.BooleanField()
    Religion = db.BooleanField()
    AnimalHandling = db.BooleanField()
    Insight = db.BooleanField()
    Medicine = db.BooleanField()
    Perception = db.BooleanField()
    Survival = db.BooleanField()
    Deception = db.BooleanField()
    Intimidation = db.BooleanField()
    Performance = db.BooleanField()
    Persuasion = db.BooleanField()

# 'Armor' at its core represents an integer that theoretically has neither a maximum nor minimum value. However, numerous
# factors can alter armor-class and it is feasible for a user to want to save multiple 'Armor' objects to represent
# different equipment in a game. Therefore, Armor will be accessible through a EmbeddedDocument
# Field of multiple armor-items in
# the DB, which user can add, update or remove from at will. Some of the more basic rules are incorporated for ease-of-use
# in the form of the required boolean-fields.


class Armor(db.EmbeddedDocument):
    Name = db.StringField()
    CharDescription = db.StringField()
    ACValue = db.IntField()
    HeavyArmor = db.BooleanField()
    MediumArmor = db.BooleanField()
    LightArmor = db.BooleanField()
    Shield = db.BooleanField()


# 'Attacks', much like Armor, are a class of what is essentially a collection of ints. An attack roll is a randomized number
# adding the modifier, the modifier being calculated client-side on the front-end, the object needs only save name, description, dice-type
# and defer all other math operations to the JavaScript component.


class Attacks(db.EmbeddedDocument):
    Name = db.StringField()
    Description = db.StringField()
    DmgDie = db.IntField()


class AttackObjs(db.EmbeddedDocument):
    AttacksList = db.EmbeddedDocumentField(Attacks)

# The ClassObj contains name, description and level as well as an embedded list-item classes as "Ability", a catch-all term for character-abilities
# that the user must specify and keep updated themselves. Proficiency is a function of level/4 +1 (Rounded up) and is thus referred to the front-end which handles
# derived stats.


class Abilities(db.EmbeddedDocument):
    Name = db.StringField()
    Description = db.StringField()
    DieType = db.IntField()
    Attribute = FieldList(db.EmbeddedDocumentField(CharAttributes))


class AbilityObjs(db.EmbeddedDocument):
    AbilityList = db.EmbeddedDocumentField(Abilities)


class ClassObj(db.EmbeddedDocument):

    HitDie = db.IntField()
    Abilities = FieldList(db.EmbeddedDocumentField(AbilityObjs))
    AttacksPerRound = db.IntField()


# Finally, the char object contains StringFields for name, description, looks, an int-field for level and references to all other documents to embed.


class Char(db.DynamicDocument):

    Name = db.StringField()
    CharClass = db.StringField()
    Subclass = db.StringField()
    Appearance = db.StringField()
    CharDescription = db.StringField()
    ClassObj = FieldList(db.EmbeddedDocumentField(ClassObj))
    AttributeList = FieldList(db.EmbeddedDocumentField(CharAttributes))
    SavesList = FieldList(db.EmbeddedDocumentField(Saves))
    SkillsList = FieldList(db.EmbeddedDocumentField(Skills))
    ArmorObjList = FieldList(db.EmbeddedDocumentField(Armor))
    AttacksList = FieldList(db.EmbeddedDocumentField(Attacks))
    AbilityObjsList = FieldList(db.EmbeddedDocumentField(AbilityObjs))
    Owner = db.ReferenceField(User, reverse_delete_rule=2)

# The following forms is what is passed to the Frontend and Jinja to register new Chars.


class CharAttributesForm(Form):
    class Meta:
        csrf = False
    strength = IntegerField('Strength: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    dexterity = IntegerField('Dexterity: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    constitution = IntegerField('Constitution: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    intelligence = IntegerField('Intelligence: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    wisdom = IntegerField('Wisdom: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    charisma = IntegerField('Charisma: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])


class ClassObjForm(Form):
    class Meta:
        csrf = False

    Lvl = IntegerField('Character level: ', [InputRequired(message='Enter a level between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    HitDie = IntegerField('Hit-die: ', [InputRequired(message='This field only takes values between 4 and 12! Enter your class HitDie!'),
                                        NumberRange(min=4, max=12, message="This value can only be between 4 and 12! Enter your class HitDie!")])
    # Abilities is not used currently, but is kept as it is intended to be used for post-submission further work on the app.
    Abilities = HiddenField(db.EmbeddedDocumentField('Abilities: '))
    AttacksPerRound = IntegerField('Attack per round: ', [InputRequired(message='Enter the number of attacks per turn your character can make, unmodified.'), NumberRange(
        min=1, max=10, message="This value can only be between 1 and 10! Consult the Player's Handbook to find your correct attacks-per-round.")])


class SaveForm(Form):
    class Meta:
        csrf = False
    StrSave = BooleanField('Strength saving throw: ')
    DexSave = BooleanField('Dexterity saving throw: ')
    ConSave = BooleanField('Constitution saving throw: ')
    IntSave = BooleanField('Intelligence saving throw: ')
    WisSave = BooleanField('Wisdom saving throw: ')
    ChaSave = BooleanField('Charisma saving throw: ')


class AbilityObjForm(Form):
    class Meta:
        csrf = False
    Name = StringField('Ability name: ')


class AbilitiesForm(Form):
    class Meta:
        csrf = False
    Name = StringField('Name of ability')
    Description = StringField(' Describe the ability, effects, damage, DCs: ')
    DieType = IntegerField('Enter the primary dice for this ability: ')
    Attribute = FormField(CharAttributes, "Your character attributes: ")
    AbilityObjList = FormField(
        AbilityObjForm, 'Add abilities your character knows here: ')


class SkillsForm(Form):
    class Meta:
        csrf = False
    Athletics = BooleanField('Athletics: ')
    Acrobatics = BooleanField('Acrobatics: ')
    Sleight = BooleanField('Sleight of Hand: ')
    Stealth = BooleanField('Stealth: ')
    Arcana = BooleanField('Arcana: ')
    History = BooleanField('History: ')
    Investigation = BooleanField('Investigation: ')
    Nature = BooleanField('Nature: ')
    Religion = BooleanField('Religon: ')
    AnimalHandling = BooleanField('Animal handling: ')
    Insight = BooleanField('Insight: ')
    Medicine = BooleanField('Medicine: ')
    Perception = BooleanField('Perception: ')
    Survival = BooleanField('Survival: ')
    Deception = BooleanField('Deception: ')
    Intimidation = BooleanField('Intimidation: ')
    Performance = BooleanField('Performance: ')
    Persuasion = BooleanField('Persuasion: ')


class CharInput(FlaskForm):
    Name = StringField('Character name: ', [InputRequired(message='You must provide a name for your new character!'), Length(
        min=1, max=30, message="Character name must be between  and 30 characters long!")])
    CharClass = StringField('Character class: ', [InputRequired(message='You must provide a class!'), Length(
        min=1, max=20, message="Class must be between  and 20 characters long!")])
    Subclass = StringField('Subclass: ', [InputRequired(message='You must provide a subclass!'), Length(
        min=1, max=20, message="Subclass must be between  and 20 characters long!")])
    Race = StringField('Race: ', [InputRequired(message='You must provide a race!'), Length(
        min=1, max=20, message="Race must be between 1 and 20 characters long!")])
    Subrace = StringField('Subrace: ', [InputRequired(message='You must provide a subrace!'), Length(
        min=1, max=20, message="Subrace must be between 1 and 20 characters long!")])
    Appearance = TextAreaField('Appearance: ',  [InputRequired(message='You must provide a short appearance description!'), Length(
        min=1, max=1500, message="Appearance must be between 1 and 1500 characters long!")])
    CharDescription = TextAreaField('Backstory: ', [InputRequired(message='You must provide a short backstory!'), Length(
        min=1, max=2000, message="Backstory must be between 1 and 2000 characters long!")])
    ClassObj = FormField(
        ClassObjForm, 'Character class information: ')
    SkillsObjList = FormField(
        SkillsForm, 'Skills: ')
    AttributeList = FormField(
        CharAttributesForm, 'Character attributes: ')
    SavesList = FormField(SaveForm,
                          'Character saves: ')
