# Parameter der Hauptroutine zur Berechnung der Vorabpauschale und der Bemessungsgrundlage

Die Routine `berechne_vorabpauschale_und_bemessungsgrundlage` befindet sich in `vorabutil.py`.

## Einganswerte

Die Routine wird mit zwei Parametern aufgerufen:

 * `para`: ein Dictionary mit den Werten des Steuerfalls
 * `basiszinsen_feld`: ein Dictionary mit den Basiszinsen für die einzelnen Jahre

### basiszinsen_feld

Dictionary

 * Schlüssel: Integer, Jahreszahl (z,B. 2019)
 * Wert: Float, Prozentwert (z.B. 0,52 - entsprechend 0,52%)

### Steuerfall Eingabewerte

Die Schlüsselnamen in diesem Dictionary sind (in `vorabutil.py`) als Konstanten definiert (durchgehend in Großbuchstaben).

Sie entsprechen den Schlüsselnamen in den INI-Dateien (dort sind sie jedoch durchgehend klein geschrieben).


| Konstante                  | wann
| -------------------------- | ---------------
| ABRECHNUNGSJAHR            | immer
| KAUFDATUM                  | ab dem Kauf
| KAUFKURS                   | ab dem Kauf
| ANZAHL                     | ab dem Kauf
| FREISTELLUNGSSATZ          | ab dem Kauf
| KURS_JAHRESANFANG          | beim Halten
| KURS_JAHRESENDE            | beim Halten
| AUSSCHUETTUNGEN_IM_JAHR    | beim Halten, beim Verkauf
| VERKAUFSDATUM              | beim Verkauf
| VERKAUFSKURS               | beim Verkauf
| SUMME_ALTE_VORABPAUSCHALEN | beim Verkauf

### Ergebnisse

Auch diese Schlüssel sind als Konstanten definiert.

| Konstante                  | wann
| -------------------------- | ---------------
| VORABPAUSCHALE             | immer
| BEMESSUNGSGRUNDLAGE        | immer
| BASISERTRAG                | beim Halten
| WERTSTEIGERUNG_JAHR        | beim Halten
| WERTSTEIGERUNG_GESAMT      | beim Verkauf
| UNTERJAHR_FAKTOR           | im Jahr des Kaufs
| FEHLERHINWEIS              | bei besonderen Situationen

#### FEHLERHINWEIS

Eine der erwähnten besonderen Situationen auf der mit diesem Eintrag hingewiesen wird, ist die Schätzung der Vorabsteuer *während* des Abrechnungsjahrs (siehe auch [inidateien.md](inidateien.md)).

Im Normalfall hat das Ergebnis der Routine keinen Eintrag FEHLERHINWEIS.