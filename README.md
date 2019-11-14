# Programm zur Berechnung der Vorabpauschale und der Bemessungsgrenze

> This program calculates a specific German tax. It may only be of interest to private German tax payers. Due to this the  documentation is in German only.

## Wichtiger Hinweis

> Ich bin kein Steuerberater. Alle Ergebnisse dieser Routine sind unverbindlich und ohne Gewähr. Sie können von den tatsächlichen Werten abweichen.

## Aufruf

Beispiel:
```
./vorabpauschale.py depot1_2018.ini depot2_2018.ini ...
```

## Beschreibung

Das Programm beruht auf Recherchen im Internet zu diesem Thema. Dabei haben sich aber auch Unterschiede in der Interpretation des Gesetzestexts gezeigt.

Dieses Programm implementiert einen Algorithmus entsprechend der Mehrzahl dieser Quellen. Eine Garantie für die Richtigkeit ist das jedoch nicht und ich bin für Hinweise auf Fehler dankbar.

Die Hauptroutine `berechne_vorabpauschale_und_bemessungsgrundlage` befindet sich in der Datei `vorabutil.py`. Sie erhält die Daten der einzelnen Steuerfälle als Dictionary und gibt die Ergebnisse auch als Dictionary aus. Sie enthält keine weiteren Abhängigkeiten und kann daher auch von anderen Programmen aufgerufen werden. Die Beschreibung der Parameter finden Sie in [parameter.md](parameter.md)

Das restliche Programm dient zum Einlesen der Daten und zur Ausgabe der Ergebnisse.

Die genaue Beschreibung der Parameter und des Algorithmus finden Sie in [grundlagen.md](grundlagen.md).

[inidateien.md](inidateien.md) beschreibt die Parameter, die in den (eigenen) INI-Dateien gespeichert sind. Dort erfahren Sie auch, welche Einträge wann gesetzt werden müssen.

Die Ein- und Ausgaben des Algorithmus verwendet die normalen Python Datenformte (string, float usw.).

Die Werte in den INI-Dateien und die Ausgabe der Ergebnisse verwendet hingegen das Dezimalkomma.

Die Datei `basis.ini` enthält die Angaben zu Basiszins und anzuwendendem Kapitalertragssteuersatz.

Die Datei `test.ini` enthält die Steuer-Testfälle zum Testen des Algorithmus.

INI-Dateien mit eigenen Testfällen können einen beliebigen Namen haben.
