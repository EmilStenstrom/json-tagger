rest-tagger
===========

A REST API to tag a Swedish sentence with part of speech tags and named entities.

Documentation
=============

What does the value in the `pos_tag` field mean?
------------------------------------------------

| Code | Swedish category                         | Example | English translation
| ---- | ---------------------------------------- | ------- | -------------------
| AB   | Adverb                                   | inte    | Adverb
| DT   | Determinerare                            | denna   | Determiner
| HA   | Frågande/relativt adverb                 | när     | Interrogative/Relative Adverb
| HD   | Frågande/relativ determinerare           | vilken  | Interrogative/Relative Determiner
| HP   | Frågande/relativt pronomen               | som     | Interrogative/Relative Pronoun
| HS   | Frågande/relativt possessivt pronomen    | vars    | Interrogative/Relative Possessive
| IE   | Infinitivmärke                           | att     | Infinitive Marker
| IN   | Interjektion                             | ja      | Interjection
| JJ   | Adjektiv                                 | glad    | Adjective
| KN   | Konjunktion                              | och     | Conjunction
| NN   | Substantiv                               | pudding | Noun
| PC   | Particip                                 | utsänd  | Participle
| PL   | Partikel                                 | ut      | Particle
| PM   | Egennamn                                 | Mats    | Proper Noun
| PN   | Pronomen                                 | hon     | Pronoun
| PP   | Preposition                              | av      | Preposition
| PS   | Possessivt pronomen                      | hennes  | Possessive
| RG   | Grundtal                                 | tre     | Cardinal number
| RO   | Ordningstal                              | tredje  | Ordinal number
| SN   | Subjunktion                              | att     | Subjunction
| UO   | Utländskt ord                            | the     | Foreign Word
| VB   | Verb                                     | kasta   | Verb

What about the `morph_feat` field?
----------------------------------

| Feature         | Tag | Legend                            | Parts-of-speech where feature applies
| --------------- | --- | --------------------------------- | -------------------------------------
| Gender          | UTR | Uter (common)                     | DT, HD, HP, JJ, NN, PC, PN, PS, (RG, RO)
|                 | NEU | Neuter                            |
|                 | MAS | Masculine                         |
| Number          | SIN | Singular                          | DT, HD, HP, JJ, NN, PC, PN, PS, (RG, RO)
|                 | PLU | Plural                            |
| Definiteness    | IND | Indefinite                        | DT, (HD, HP, HS), JJ, NN, PC, PN, (PS, RG, RO)
|                 | DEF | Definite                          |
| Case            | NOM | Nominative                        | JJ, NN, PC, PM, (RG, RO)
|                 | GEN | Genitive                          |
| Tense           | PRS | Present                           | VB
|                 | PRT | Preterite                         |
|                 | SUP | Supinum                           |
|                 | INF | Infinite                          |
| Voice           | AKT | Active                            |
|                 | SFO | S-form (passive or deponential)   |
| Mood            | KON | Subjunctive (Sw. konjunktiv)      |
| Participle form | PRS | Present                           | PC
|                 | PRF | Perfect                           |
| Degree          | POS | Positive                          | (AB), JJ
|                 | KOM | Comparative                       |
|                 | SUV | Superlative                       |
| Pronoun form    | SUB | Subject form                      | PN
|                 | OBJ | Object form                       |
|                 | SMS | Compound (Sw.sammansättningsform) | All parts-of-speech
