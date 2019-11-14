#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import sys
import re
import datetime
import argparse

from vorabutil import *


# Dateiname des auszuwertenden Datei
BASISINFO = "basis.ini"

# Datei mit Testdaten
TESTDATEN = "test.ini"

# Abschnitts- und Schlüsselnamen
BASISZINS_SECTION = "basiszins"
PERS_STEUERSATZ_SECTION = "default"
PRES_STEUERSATZ_KEY = "steuersatz"


CONFIGFILE = "daten.ini"



##### Formatierroutinen

def strip(s):
    """ Leerzeichen am Anfang und Ende löschen

    :param s: Eingangswert
    :type s: alle
    :return: bearbeiteter Wert oder None
    :rtype: str/None
    """
    if s is None:
        return None
    return str(s).strip()

def float_conv(s):
    """ Umwandlung String in Float-Zahl

    :param s: Wert mit Dezimalkomma
    :type s: string
    :return: umgewandelter Wert
    :rtype: float
    """

    if s is None:
        return None

    # Dezimalkomma -> Dezimalpunkt
    return float(s.replace(".", "").replace(",", "."))

def prozent_conv(s):
    """ Umwandlung eines Prozentwerts

    :param s: Prozentwert mit Dezimalkomma und "%"
    :type s: string
    :raises ValueError: bei Fehler
    :return: Prozentwert (0.0-100.0)
    :rtype: float
    """

    if s is None:
        return None

    s = s.strip()
    if not s.endswith("%"):
        raise ValueError("Wert endet nicht mit %")

    return float_conv(s[:-1])

DATUM_PATTERN = [
    # TT.MM.JJJJ
    re.compile(r"(?P<tag>\d{1,2})\.(?P<monat>\d{1,2})\.(?P<jahr>\d{4})"),
    # JJJJ-MM-TT
    re.compile(r"(?P<jahr>\d{4})-(?P<monat>\d{1,2})-(?P<tag>\d{1,2})"),
    # JJJJ/MM/TT
    re.compile(r"(?P<jahr>\d{4})/(?P<monat>\d{1,2})/(?P<tag>\d{1,2})")
]


def datum_conv(s):
    """ Umwandlung des Datums

    :param s: Datum als TT.MM.JJJJ oder JJJJ-MM-TT
    :type s: string
    :raises ValueError: bei Fehler
    :return: umgewandeltes Datum
    :rtype: datetime.date
    """

    if s is None:
        return None

    s = s.strip()

    ma = None
    for pattern in DATUM_PATTERN:
        ma = pattern.match(s)
        if ma is not None:
            break

    if ma is not None:
        return datetime.date(year=int(ma.group('jahr')), month=int(ma.group('monat')), day=int(ma.group('tag')))

    raise ValueError("Ungültiges Datumsformat: %s" % s)


# Tabelle der möglichen Schlüsselworte mit zugehöriger Umwandlungsroutine

CONVTABLE = [
    (ABRECHNUNGSJAHR, int),
    (KAUFDATUM, datum_conv),
    (KAUFKURS, float_conv),
    (VERKAUFSDATUM, datum_conv),
    (VERKAUFSKURS, float_conv),
    (ANZAHL, float_conv),
    (FREISTELLUNGSSATZ, prozent_conv),
    (KURS_JAHRESANFANG, float_conv),
    (KURS_JAHRESENDE, float_conv),
    (AUSSCHUETTUNGEN_IM_JAHR, float_conv),
    (SUMME_ALTE_VORABPAUSCHALEN, float_conv),
    (VORABPAUSCHALE, float_conv),
    (BEMESSUNGSGRUNDLAGE, float_conv),
    (WARNUNG, strip)
]

def formatumwandlung(cfg, abschnitt):
    res = {}
    for item in CONVTABLE:
        name, fkt = item

        w = cfg[abschnitt].get(name, raw=True)     # raw: keine Interpolation von "%"
        if w is not None and w.strip() != '':
            # Wert vorhanden (und nicht leer)
            try:
                if fkt is None:
                    res[name] = w
                else:
                    res[name] = fkt(w)
            except Exception as msg:
                print("** Fehler bei der Umwandlung: %s" % msg)
                print("Abschnitt: %s, Position: %s, Wert: %s" % (abschnitt, name, w))
                sys.exit(5)

    return res




def identisch(a, b):
    """ Teste ob Werte identisch sind, berücksichtige Rundungsfehler

    :param a: Wert 1
    :type a: float
    :param b: Wert 2
    :type b: fload
    :return: ist identisch
    :rtype: bool
    """
    return abs(a-b) < 0.003

def myformat(data, formatstring, defaultlaenge, faktor=None, komma_punkt=True):
    """ formatiere Daten

    :param data: zu formatierender Wert
    :type data: Any
    :param formatstring: Formatstring für den Wert
    :type formatstring: str
    :param defaultlaenge: Länge, falls Wert is None
    :type defaultlaenge: int
    :param faktor: Faktor mit dem der Wert zuvor multipliziert wird, defaults to None
    :type faktor: float, optional
    :param komma_punkt: Austausch Punk/Komma, defaults to True
    :type komma_punkt: bool, optional
    :return: formatierter Wert
    :rtype: str
    """

    if data is None:
        return " " * defaultlaenge

    if faktor is not None:
        data *= faktor                # z.B. 100.0 für Prozentzahlen

    s = formatstring % data
    if komma_punkt:
        s.translate({'.': ',', ',': '.'})
    return s


def lese_abschnitt_basiszinsen(abschnitt):
    """ Hole die Basiszinsen aus dem Abschnitt der INI-Datei

    :param abschnitt: eingelesener Basiszins-Abschnitt aus der INI-Datei
    :type abschnitt: Section
    :return: dict mit key=Jahr und value=Basiszinsprozentsatz
    :rtype: dict
    """
    result = {}

    for item in abschnitt:
        try:
            jahr = int(item)
        except ValueError:
            print("Fehler: Jahr im Abschnitt %s keine Zahl: %s" (
                BASISZINS_SECTION, item))
            sys.exit(2)

        # Beispiel: 0,87%
        # raw: keine Interpolation des "%"
        prozwert = abschnitt.get(item, raw=True)
        try:
            result[jahr] = prozent_conv(prozwert)
        except:
            print("* Fehler beim Einlesen der Basiszinsen für Jahr %s: %s" %
                  (jahr, prozwert))
            sys.exit(3)

    return result


def lese_basiszinzsatz_und_persoenlichen_steuersatz(configname):
    """ Lese Basiszinzsatz und persönlichen Steuersatz aus INI-Datei

    :param configname: Name der INI-Datei
    :type configname: str
    :return: Werte
    :rtype: dict, float
    """
    basis_config = configparser.ConfigParser()
    basis_config.read([configname, ])

    # Basiszinssätze einlesen
    basiszinsen = None

    secs = basis_config.sections()
    if not BASISZINS_SECTION in secs:
        print("Fehler: Keine Basiszinsen in der Konfigurationsdatei", configname)
        sys.exit(1)
    else:
        basiszinsen = lese_abschnitt_basiszinsen(
            basis_config[BASISZINS_SECTION])

    # Persönlicher Steuersatz

    pers_satz = 26.375          # Standardwert

    if PERS_STEUERSATZ_SECTION in secs:
        s = basis_config[PERS_STEUERSATZ_SECTION].get(PRES_STEUERSATZ_KEY, raw=True)
        pers_satz = prozent_conv(s)

    return basiszinsen, pers_satz

if __name__ == "__main__":
    basis_zinsen, pers_satz = lese_basiszinzsatz_und_persoenlichen_steuersatz(
            BASISINFO)

    parser = argparse.ArgumentParser(description='Berechnung von Vorabpauschale und Bemessungsgrundlage')

    parser.add_argument('Fallliste',
        nargs="+",
        help='ein oder mehrere Dateien mit Steuerfällen' )

    args = parser.parse_args()

    total_vor = total_bemess = 0.0

    for fallliste in args.Fallliste:
        daten_config = configparser.ConfigParser()
        daten_config.read([fallliste])
        secs = daten_config.sections()

        print("Abschnitt             Vorab- Bemessungs-  Steuer | Kauf                            Verkauf               Wertst. Auschütt.| Kurssteigerung         Wertst.|  Basis- Unterjahr- Info")
        print("                   pauschale   grundlage %6.3f%% | Datum         Anzahl     Preis  Datum          Preis  gesamt   im Jahr | Jahrsanf.  Jahresende    Jahr |  ertrag faktor" % pers_satz)

        summe_vor = summe_bemess = 0.0
        for abschnitt in secs:

            daten = formatumwandlung(daten_config, abschnitt)
            ergebnisse = berechne_vorabpauschale_und_bemessungsgrundlage(daten, basis_zinsen)

            if ergebnisse is None:
                print(myformat(abschnitt, "%-20s", 20) + " ******* Nicht anwendbar ********")
                continue

            summe_vor += ergebnisse[VORABPAUSCHALE]
            summe_bemess += ergebnisse[BEMESSUNGSGRUNDLAGE]

            info = ""
            if daten.get(VORABPAUSCHALE) is not None or daten.get(BEMESSUNGSGRUNDLAGE) is not None:
                vorab_ok = identisch(ergebnisse[VORABPAUSCHALE], daten.get(VORABPAUSCHALE))
                bemessung_ok = identisch(ergebnisse[BEMESSUNGSGRUNDLAGE], daten.get(BEMESSUNGSGRUNDLAGE))
                if vorab_ok and bemessung_ok:
                    info = "* Test ok"
                else:
                    info = "* Test Fehler - Vorab: %.2f, Bemessung: %.2f" % (
                        daten[VORABPAUSCHALE], daten[BEMESSUNGSGRUNDLAGE])

            if ergebnisse.get(FEHLERHINWEIS) is not None:
                info = '* ' + ergebnisse.get(FEHLERHINWEIS)

            steuer = 26.375 / 100.0 * ergebnisse[BEMESSUNGSGRUNDLAGE]

            print(
                myformat(abschnitt, "%-20s", 20) +
                myformat(ergebnisse.get(VORABPAUSCHALE), "%8.2f", 8) +
                myformat(ergebnisse.get(BEMESSUNGSGRUNDLAGE), "%12.2f", 12) +
                myformat(steuer, "%8.2f", 12) +
                " | " + myformat(daten.get(KAUFDATUM), "%10s", 10, komma_punkt=False) +
                myformat(daten.get(ANZAHL), "%10.4f", 10) +
                myformat(daten.get(KAUFKURS), "%10.2f", 10) +
                '  ' + myformat(daten.get(VERKAUFSDATUM), "%10s", 10, komma_punkt=False) +
                myformat(daten.get(VERKAUFSKURS), "%10.2f", 10) +
                myformat(ergebnisse.get(WERTSTEIGERUNG_GESAMT), "%9.2f", 9) +
                myformat(daten.get(AUSSCHUETTUNGEN_IM_JAHR), "%9.2f", 9) +
                ' | ' + myformat(daten.get(KURS_JAHRESANFANG), "%10.2f", 10) +
                myformat(daten.get(KURS_JAHRESENDE), "%10.2f", 10) +
                myformat(ergebnisse.get(WERTSTEIGERUNG_JAHR), "%9.2f", 9) +
                ' | ' + myformat(ergebnisse.get(BASISERTRAG), "%7.2f", 7) +
                ' ' + myformat(ergebnisse.get(UNTERJAHR_FAKTOR), "%5.1f", 5, faktor=100.0) +
                "      " + info
            )

            warnung = daten.get(WARNUNG)
            if warnung is not None:
                print("***", warnung)

        print(
            "            Summe   " +
                myformat(summe_vor, "%8.2f", 8) +
                myformat(summe_bemess, "%12.2f", 12) +
                "\n")

        total_vor += summe_vor
        total_bemess += summe_bemess

    if len(args.Fallliste) > 1:
        print(
            "Total               " +
                myformat(total_vor, "%8.2f", 8) +
                myformat(total_bemess, "%12.2f", 12))

