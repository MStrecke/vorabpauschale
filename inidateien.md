# Werte in den INI-Dateien

Das Programm verwendet die folgenden INI-Dateien:

 * `basis.ini`: enthält die Angaben zum Basiszins und anzuwendendem Kapitalertragssteuersatz
 * `test.ini`: enthält die Testfälle zum Testen des Algorithmus
 * eigene INI-Dateien mit Steuerfällen: der Name ist frei wählbar

## basis.ini

Typischer Inhalt:

```
[basiszins]
2016=1,1%
2018=0,87%
2019=0,52%

[default]
steuersatz=26,375%
```

Im Abschnitt *basiszins* befinden sich die von der Deutschen Bundesbank veröffentlichten Basiszinsen zur Berechnung der Vorabsteuer für die einzelnen Jahre.

Der Wert für 2016 wird nur für Testzwecke verwendet (siehe Testfälle von zendepot).

Unter *default* findet sich der anzuwendende Steuersatz. Maximal sind das im Augenblick 25% + 5,5% Solidaritätszuschlag

25% * (1 + 5,5%) = 26,375%

Falls Ihr persönlicher Steuersatz niedriger ist oder Sie Kirchensteuer bezahlen, kann der Wert angepasst werden.


## test.ini und eigene INI-Dateien

Diese Dateien enthalten die Steuerfälle, die vom Programm verarbeitet werden.

Hier ist ein typischer leerer Eintrag

```
[XXXXXXXXXXXX]
abrechnungsjahr=20XX
freistellungssatz=XX%
kurs_jahresanfang=
kurs_jahresende=
anzahl=
kaufdatum=
kaufkurs=
verkaufsdatum=
verkaufskurs=
ausschuettungen_im_jahr=0
summe_alte_vorabpauschalen=
hinweis=
bemerkung=
warnung=
```

Der Name des Abschnitts (in den eckigen Klammern) muss eindeutig und sollte aussagefähig sein, z.B. Jahr + ISIN. Er wird bei der Ausgabe der Ergebnisse angezeigt.

Welche Felder ausgefüllt sein müssen hängt davon ab, ob Sie den Fonds im Abrechnungsjahr verkauft (V) oder über den 31.12. gehalten (H) haben.


| Schlüssel | benötigt | Inhalt |
| --------- |:--------:| ------ |
| abrechnungsjahr | immer | Jahr für das die Abrechnung erstellt werden soll |
| freistellungssatz | immer | Freistellungssatz, je nach Art des Fonds (30%, 15%, 0%) |
| kurs_jahresanfang | H | Kurs des Fonds zum Jahresanfang |
| kurs_jahresende | H | Kurs des Fonds zum Jahresende |
| anzahl | immer | Anzahl der Anteil -> Wert = Anzahl * Kurs |
| kaufdatum | immer | Datum des Kaufs |
| kaufkurs | V | Kurs zu dem der Anteil gekauft wurde |
| verkaufsdatum | V | Datum an dem der Anteil verkauft wurde |
| verkaufskurs | V | Kurs zu dem der Anteil verkauft wurde |
| ausschuettungen_im_jahr | immer | Höhe der Ausschüttungen im Abrechnungsjahr, kann 0 sein |
| summe_alte_vorabpauschalen | V | Summe der in den letzten Jahren gezahlten Vorabpauschalen für diese Tranche |
| hinweis | - | Klartext ohne weitere Funktion |
| bemerkung | - | Klartext ohne weitere Funktion |
| vorabpauschale | Test | falls gesetzt → Testfall |
| bemessungsgrundlage | Test | falls gesetzt → Testfall |
| Warnung | Test | Hinweis, der *immer* in der Ausgabe angezeigt wird |

Die ausführliche Definition der Parameter finden Sie in [grundlagen.md](grundlagen.md).

## Wann muss ich was eintragen?

### Kauf

Die folgenden Einträge *müssen* gesetzt werden:

 * kaufdatum
 * kaufkurs
 * anzahl
 * freistellungssatz

Bereits jetzt *sollten* Sie eintragen, weil diese Werte verfügbar sind:

 * abrechnungsjahr
 * kurs_jahresanfang

### Verkauf

Die folgenden Einträge *müssen* zusätzlich gesetzt werden:

 * abrechnungsjahr
 * verkaufsdatum
 * verkaufskurs
 * ausschuettungen_im_jahr
 * summe_alte_vorabpauschalen

### falls der Fonds während des Abrechnungsjahr nicht verkauft wurde

 * abrechnungsjahr
 * kurs_jahresanfang
 * kurs_jahresende
 * ausschuettungen_im_jahr

## Allgemein bei jeder Berechnung

Die folgenden Einträge *müssen* gesetzt sein:

 * abrechnungsjahr
 * ausschuettungen_im_jahr

### Schätzung *während* des Abrechnungsjahrs

Während des Abrechnungsjahrs ist der Kurs zum Jahresende natürlich noch nicht bekannt.

Das Programm berechnet dann eine Schätzung auf der Grundlage von

 * abrechnungsjahr
 * kurs_jahresanfang
 * ausschuettungen_im_jahr

Ein Hinweis, dass dies eine Schätzung ist, erscheint in der Info-Spalte

## Tests

Falls beim Schlüssel `vorabpauschale` oder `bemessungsgrundlage` ein Wert eingetragen ist, wird dieser Datensatz als Testfall betrachtet und diese Werte mit den berechneten Werten verglichen. Das Ergebnis des Tests erscheint in der Ausgabe. Ein erfolgreicher Vergleich erlaubt eine Abweichung um 3 Eurocent.

## Warnung

Der Schlüssel `warnung` dient dazu, einen Hinweis in der Liste der Ergebnisse anzuzeigen.

Zum Beispiel den Hinweis, dass die "Berechnung auf der Website wahrscheinlich fehlerhaft" ist.