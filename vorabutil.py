#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ABRECHNUNGSJAHR = 'abrechnungsjahr'
KAUFDATUM = 'kaufdatum'
KAUFKURS = 'kaufkurs'
VERKAUFSDATUM = 'verkaufsdatum'
VERKAUFSKURS = 'verkaufskurs'
ANZAHL = 'anzahl'
FREISTELLUNGSSATZ = 'freistellungssatz'
KURS_JAHRESANFANG = 'kurs_jahresanfang'
KURS_JAHRESENDE = 'kurs_jahresende'
AUSSCHUETTUNGEN_IM_JAHR = 'ausschuettungen_im_jahr'
SUMME_ALTE_VORABPAUSCHALEN = 'summe_alte_vorabpauschalen'
WARNUNG = 'warnung'

VORABPAUSCHALE = 'vorabpauschale'
BEMESSUNGSGRUNDLAGE = 'bemessungsgrundlage'
WERTSTEIGERUNG_GESAMT = 'wertsteigerung_gesamt'
WERTSTEIGERUNG_JAHR = 'wertsteigerung_jahr'
UNTERJAHR_FAKTOR = 'unterjahr_faktor'
BASISERTRAG = 'basisertrag'
FEHLERHINWEIS = 'fehler'

ABRECHNUNGSJAHR = 'abrechnungsjahr'
FREISTELLUNGSSATZ = 'freistellungssatz'

def berechne_vorabpauschale_und_bemessungsgrundlage(para, basiszinsen_feld):
    """ Berechnung der Vorabpauschale und der Bemessungsgrundlage

    :param para: Eingangsvariablen
    :type para: dict
    :return: Ausgangsvariablen
    :rtype: dict oder None, falls keine Berechnung stattgefunden hat
    :note: Vorabpauschale VOR Anwendung des Freistellungssatzes
    :note: Bemessungsgrundlage VOR Anwendung des Steuersatzes
    """
    ###### Ist überhaupt etwas zu berechnen?

    # Abrechnungsjahr vor dem Kauf des Papiers
    if para[ABRECHNUNGSJAHR] < para[KAUFDATUM].year:
        return None

    # Abrechnungsjahr nach dem Verkauf des Papiers
    if para.get(VERKAUFSDATUM) is not None and para[ABRECHNUNGSJAHR] > para[VERKAUFSDATUM].year:
        return None

    result = {
        VORABPAUSCHALE: 0.0,
        BEMESSUNGSGRUNDLAGE: 0.0
    }

    # Handelt es sich um einen Verkauf?
    if para.get(VERKAUFSDATUM) is not None and para[ABRECHNUNGSJAHR] == para[VERKAUFSDATUM].year:

        # Keine Vorabpauschale im Verkaufsjahr
        result[VORABPAUSCHALE] = 0.0

        result[WERTSTEIGERUNG_GESAMT] = (
            para[VERKAUFSKURS] - para[KAUFKURS]) * para[ANZAHL]

        result[BEMESSUNGSGRUNDLAGE] = \
            (result[WERTSTEIGERUNG_GESAMT] + para[AUSSCHUETTUNGEN_IM_JAHR])       \
            * (100.0 - para[FREISTELLUNGSSATZ]) / 100.0                    \
            - para[SUMME_ALTE_VORABPAUSCHALEN]

        return result

    # Papier wurde über das Jahresende gehalten

    result[UNTERJAHR_FAKTOR] = 1.0
    if para[ABRECHNUNGSJAHR] == para[KAUFDATUM].year:
        result[UNTERJAHR_FAKTOR] = (13 - para[KAUFDATUM].month) / 12.0

    result[BASISERTRAG] = 0.7 * basiszinsen_feld[para[ABRECHNUNGSJAHR]
                                                 ] / 100.0 * para[KURS_JAHRESANFANG] * para[ANZAHL]

    if para.get(KURS_JAHRESENDE) in [None, ""]:
        # Schätzung auf der Grundlage des Basisertrags und der Ausschüttungen

        result[FEHLERHINWEIS] = "Schätzung, da kein Jahresendkurs vorhanden"
        vorabpauschale_1 = result[BASISERTRAG] - para[AUSSCHUETTUNGEN_IM_JAHR]
        if vorabpauschale_1 < 0:
            vorabpauschale_1 = 0
    else:
        # Normale Berechnung

        result[WERTSTEIGERUNG_JAHR] = (
            para[KURS_JAHRESENDE] - para[KURS_JAHRESANFANG]) * para[ANZAHL]

        # Keine Vorabpauschale, falls
        # keine Wertsteigerung
        #   ODER
        # Ausschüttungen im Jahr > als Basisertrag

        if (result[WERTSTEIGERUNG_JAHR] <= 0) or (para[AUSSCHUETTUNGEN_IM_JAHR] >= result[BASISERTRAG]):
            vorabpauschale_1 = 0.0
        else:
            if result[WERTSTEIGERUNG_JAHR] + para[AUSSCHUETTUNGEN_IM_JAHR] >= result[BASISERTRAG]:
                vorabpauschale_1 = result[BASISERTRAG] - \
                    para[AUSSCHUETTUNGEN_IM_JAHR]
            else:
                vorabpauschale_1 = result[WERTSTEIGERUNG_JAHR]

    # weiter verringert:
    #  * ggf. anteilig fürs Jahr
    #  * abzüglich Freistellungssatz
    result[VORABPAUSCHALE] = vorabpauschale_1                 \
        * result[UNTERJAHR_FAKTOR]

    # Bemessungsgrundlage =
    #   verbleibende Vorabpauschale
    #   + Ausschüttungen im Jahr (anzügliche Freistellung)
    result[BEMESSUNGSGRUNDLAGE] = (result[VORABPAUSCHALE] + para[AUSSCHUETTUNGEN_IM_JAHR]) \
        * (100.0 - para[FREISTELLUNGSSATZ]) / 100.0

    return result
