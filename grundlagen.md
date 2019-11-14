# Wichtiger Hinweis

> Ich bin kein Steuerberater. Alle Ergebnisse dieser Routine sind unverbindlich und ohne Gewähr. Eine Haftung ist ausgeschlossen. Trotzdem bin ich für Hinweise auf Fehler dankbar.

Diese Dokument beschreibt die Grundlagen des Programms und die einzelnen Parameter der Routine `berechne_vorabpauschale_und_bemessungsgrundlage` in `vorabutil.py`.

Es berechnet die Vorabpauschale und die Bemessungsgrundlage für Privatanleger für Fonds und ETF nach dem Investionssteuergesetz 2018.

# Definitionen

## Grunddaten

### Abrechnungsjahr

Jahr für das die Abrechnung erfolgt.

Zusammen mit dem `Kaufdatum` und dem `Verkaufsdatum` wird bestimmt:

* ob die Anteile im Abrechnungsjahr gekauft wurden
* ob die Anteile im Abrechnungsjahr verkauft wurden
* ob die Anteile über das Abrechnungsjahr hinaus gehalten wurden
* ob der Anleger die Anteile im Abrechnungsjahr überhaupt besessen hat

### Anzahl

Anzahl der Anteile an einem Fonds/ETF. Der Wert berechnet sich aus der Multiplikation
der Anzahl mit dem jeweiligen Kurs.

### Kaufdatum

Datum zu dem die Anteile gekauft wurden.

### Kaufkurs

Kurs zu dem die Anteile gekauft wurden

### Verkaufsdatum

Datum zu dem die Anteile vergekauft wurden.

### Verkaufskurs

Kurs zu dem die Anteile verkauft wurden

### Kurs am Jahresanfang

Kurs eines Anteils zu Beginn des Jahres = letzter Kurs des Vorjahres

### Kurs zum Jahresende

Kurs eines Anteils am Ende des Jahres = letzter Kurs im Jahr

### Ausschüttungen im Jahr

Im Abrechnungsjahr erhaltene Ausschüttungen des Fonds

### Basiszins

Wird am Beginn des Jahres vom Bundesfinanzministerium festgelegt.
Angegeben wird der Zinssatz in Prozent.
(Hinterlegt in `basis.ini`)

### Anzuwendender Steuersatz

Dieser Wert in `basis.ini` bezieht sich auf die anwendbare Abgeltungssteuer.
Zurzeit (2019) sind das maximal 25% + 5,5% Solidaritätszuschlag:

25% * (1 + 5,5%) = 26,375%

Falls Sie zusätzlich Kirchensteuer bezahlen oder der eigene Einkommenssteuersatz
unter 25% beträgt, können Sie hier auch angepasste Werte eintragen.

### Teilfreistellung

Die Teilfreistellung ist ein Prozentsatz und hängt von der Art des Fonds ab.
Für Privatanlager sind das:

| Fondstyp    | Aktienquote | Teilfreistellung |
| ----------- |:-----------:|:----------------:|
| Aktienfonds |    ≥ 51%    | 30%              |
| Mischfonds  |    ≥ 25%    | 15%              |
| Sonstige    |    < 25%    | 0%               |

### Summe alte Vorabpauschalen

Summe der Vorabpauschalen aus früheren Jahren, die bereits versteuert wurden.

## Abgeleitete Werte

### Basisertrag

`Basisertrag = Kurs zum Jahresanfang x Anzahl x Basiszins x 0,7`


### Wertentwicklung

`(Kurs zum Jahresende - Kurs am Jahresanfang) * Anzahl`


### Vorabbauschale

* Null im Jahr des Verkaufs
* Anteilig im Jahr des Kaufs: n/12
  * n = Anzahl der angefangenen Monate in dem das Papier gehalten wurde
    * Kauf am 31.01. => n = 12
    * Kauf am  1.02. => n = 11
    * Kauf am 28.02. => n = 11
    * Kauf am  1.03. => n = 10
    * usw.
* Null bei negativer Wertentwicklung im Abrechnungsjahr
* Null, wenn Ausschüttungen im Jahr >= Basisertrag

#### Falls Wertentwicklung + Ausschüttungen im Jahr >= Basisertrag

`Vorabpauschale = Basisertrag - Ausschüttungen`

* falls negativ, dann 0

## Falls Wertentwicklung + Ausschüttungen im Jahr < Basisertrag

`Vorabpauschale = Wertentwicklung`

* eine negative Wertentwicklung wurde schon vorab aussortiert

## Bemessungsgrundlage

Der Wert, der zur Berechnung der Steuer herangezogen wird.

### wenn der Fonds im Abrechnungsjahr *nicht* verkauft wurde

`Bemessungsgrundlage = (Vorabpauschale + Ausschüttungen im Jahr) * (100% - Teilfreistellung)`

### falls der Fonds im Abrechnungsjahr verkauft wurde


`Bemessungsgrundlage = ((Verkaufskurs - Kaufkurs) * Anzahl_Anteile + Ausschüttungen im Jahr - Summe alter Vorabpauschalen) * (100% - Teilfreistellung)`

## zu zahlende Steuer

`(Summe aller Bemessungsgrundlagen ggf. abzüglich des Sparerfreibetrags) * anzuwendender Steuersatz`


# Offene Fragen

* Was ist mit der Summe alter Vorabpauschalen, wenn für eine frühere Vorabpauschale wegen des Freibetrags keine Steuer gezahlt wurde?

# Links

* https://www.justetf.com/de/news/etf/etf-und-steuern-das-neue-investmentsteuergesetz-ab-2018.html
* https://www.justetf.com/de/etf-steuerrechner.html
* https://www.justetf.com/de/news/geldanlage/der-sparerpauschbetrag.html
* https://www.vlh.de/wissen-service/steuer-abc/wie-funktioniert-die-abgeltungssteuer.html
* https://www.dasinvestment.com/fondsverband-bvi-die-wichtigsten-fragen-und-antworten-zur-investmentsteuerreform/?page=16
  - Beispiel für Summe alte Vorabpauschalen
* https://www.onvista-bank.de/vorabpauschale.html
  - Vorabpauschale bezieht sich immer auf das Vorjahr
  - Grundlage ist das Portefolio am 31.12
* https://zendepot.de/etf-fonds-steuern/#Die_neuen_Regelungen
* https://www.ffb.de/public/wissen/investmentsteuerreform.html#tabcontent01https://www.ffb.de/public/wissen/investmentsteuerreform.html#tabcontent01
* https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&ved=2ahUKEwi2x-_m-NDlAhXIGuwKHWkPC_wQFjADegQIAhAC&url=https%3A%2F%2Fwww.hypovereinsbank.de%2Fcontent%2Fdam%2Fhypovereinsbank%2Ffooter%2FHVB-Investmentsteuerreform-Infoblatt.pdf&usg=AOvVaw2lHk0yC6zyzGJPW0hGOmZ8