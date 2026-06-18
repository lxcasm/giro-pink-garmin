import Toybox.Activity;
import Toybox.Application;
import Toybox.Application.Properties;
import Toybox.Graphics;
import Toybox.Lang;
import Toybox.SensorHistory;
import Toybox.System;
import Toybox.UserProfile;
import Toybox.WatchUi;

// ============================================================
//  GIRO PINK - Champ de donnees plein ecran (Edge 1040)
//  Style "Carbone Rosa" : fond prune degrade + accents rose neon.
//  Puissance coloree selon les zones Zwift (% FTP) + barre 6 segments.
//  Zones Zwift : Z1 gris <60% | Z2 bleu 60-75% | Z3 vert 76-89%
//                Z4 jaune 90-104% | Z5 orange 105-118% | Z6 rouge >=119%
// ============================================================

// Palette "Carbone Rosa"
const C_BG      = 0x3A0E26;  // fond uni (prune profond)
const C_BAR     = 0x29091A;  // bandeau superieur (plus sombre)
const C_ACCENT  = 0xFF2E9C;  // rose neon (libelles, lignes)
const C_TOPTXT  = 0xFF8AC6;  // texte du bandeau
const C_VALUE   = 0xFFFFFF;  // valeurs (blanc)
const C_UNIT    = 0xB87A9C;  // unites / texte discret
const C_SEP     = 0x5A2444;  // separateurs de grille
const C_SEG_OFF = 0x4A2A3E;  // segment de zone eteint
const C_WHITE   = 0xFFFFFF;

class GiroPinkDataField extends WatchUi.DataField {

    hidden var mSpeed as Float = 0.0;        // km/h
    hidden var mHasSpeed as Boolean = false;
    hidden var mPower as Number = 0;
    hidden var mHasPower as Boolean = false;
    hidden var mFtp as Number = 200;
    hidden var mZone as Number = 0;          // 0 = pas de donnee
    hidden var mHr as Number = 0;
    hidden var mHasHr as Boolean = false;
    hidden var mCad as Number = 0;
    hidden var mHasCad as Boolean = false;
    hidden var mDist as Float = 0.0;         // km
    hidden var mHasDist as Boolean = false;
    hidden var mAlt as Number = 0;           // m
    hidden var mHasAlt as Boolean = false;
    hidden var mAscent as Number = 0;        // m (D+)
    hidden var mHasAscent as Boolean = false;
    hidden var mTimer as Number = 0;         // ms (temps en roulant)
    hidden var mTemp as Number = 0;          // C
    hidden var mHasTemp as Boolean = false;

    // Calcul de la pente
    hidden var mGrade as Float = 0.0;
    hidden var mHasGrade as Boolean = false;
    hidden var mRefDist as Float = -1.0;     // m
    hidden var mRefAlt as Float = 0.0;       // m

    function initialize() {
        DataField.initialize();
    }

    function compute(info as Activity.Info) as Void {
        // Vitesse (m/s -> km/h)
        if (info.currentSpeed != null) {
            mSpeed = info.currentSpeed * 3.6;
            mHasSpeed = true;
        } else {
            mSpeed = 0.0;
            mHasSpeed = false;
        }

        // Puissance + zone Zwift
        mHasPower = (info.currentPower != null);
        if (mHasPower) {
            mPower = info.currentPower;
        }
        mFtp = resolveFtp();
        mZone = mHasPower ? getZwiftZone(mPower, mFtp) : 0;

        // Frequence cardiaque
        mHasHr = (info.currentHeartRate != null);
        if (mHasHr) { mHr = info.currentHeartRate; }

        // Cadence
        mHasCad = (info.currentCadence != null);
        if (mHasCad) { mCad = info.currentCadence; }

        // Distance (m -> km)
        if (info.elapsedDistance != null) {
            mDist = info.elapsedDistance / 1000.0;
            mHasDist = true;
        } else {
            mHasDist = false;
        }

        // Altitude
        if (info.altitude != null) {
            mAlt = info.altitude.toNumber();
            mHasAlt = true;
        } else {
            mHasAlt = false;
        }

        // Denivele positif (D+)
        if (info.totalAscent != null) {
            mAscent = info.totalAscent.toNumber();
            mHasAscent = true;
        } else {
            mHasAscent = false;
        }

        // Temps en roulant uniquement (timerTime se met en pause a l'arret)
        if (info.timerTime != null) {
            mTimer = info.timerTime;
        }

        // Pente : delta altitude / delta distance, lisse
        computeGrade(info);

        // Temperature (capteur interne)
        computeTemperature();
    }

    hidden function resolveFtp() as Number {
        var ftp = Properties.getValue("ftpOverride");
        if (ftp != null && (ftp as Number) > 0) {
            return ftp as Number;
        }
        if (UserProfile has :getFunctionalThresholdPower) {
            var p = UserProfile.getFunctionalThresholdPower(Activity.SPORT_CYCLING);
            if (p != null && p > 0) {
                return p;
            }
        }
        return 200;
    }

    hidden function computeGrade(info as Activity.Info) as Void {
        if (info.altitude == null || info.elapsedDistance == null) {
            return;
        }
        var dist = info.elapsedDistance;
        var alt = info.altitude;
        if (mRefDist < 0.0) {
            mRefDist = dist;
            mRefAlt = alt;
            return;
        }
        var dDist = dist - mRefDist;
        if (dDist >= 10.0) {
            var g = (alt - mRefAlt) / dDist * 100.0;
            if (g > 45.0) { g = 45.0; }
            if (g < -45.0) { g = -45.0; }
            if (mHasGrade) {
                mGrade = mGrade * 0.6 + g * 0.4;
            } else {
                mGrade = g;
                mHasGrade = true;
            }
            mRefDist = dist;
            mRefAlt = alt;
        }
    }

    hidden function computeTemperature() as Void {
        if (Toybox has :SensorHistory && SensorHistory has :getTemperatureHistory) {
            var iter = SensorHistory.getTemperatureHistory({:period => 1});
            if (iter != null) {
                var sample = iter.next();
                if (sample != null && sample.data != null) {
                    mTemp = sample.data.toNumber();
                    mHasTemp = true;
                }
            }
        }
    }

    function onUpdate(dc as Dc) as Void {
        var w = dc.getWidth();
        var h = dc.getHeight();

        drawBackground(dc, w, h);

        var barH = (h * 0.064).toNumber();
        drawTopBar(dc, w, barH);

        var heroH = (h * 0.29).toNumber();
        drawHero(dc, w, barH, heroH);

        var gridY = barH + heroH;
        drawGrid(dc, w, gridY, h);
    }

    // ---------- Fond : couleur unie ----------
    hidden function drawBackground(dc as Dc, w as Number, h as Number) as Void {
        dc.setColor(C_BG, C_BG);
        dc.clear();
    }

    // ---------- Bandeau : heure | GIRO | temperature ----------
    hidden function drawTopBar(dc as Dc, w as Number, barH as Number) as Void {
        dc.setColor(C_BAR, C_BAR);
        dc.fillRectangle(0, 0, w, barH);

        var clock = System.getClockTime();
        var hour = clock.hour;
        if (!System.getDeviceSettings().is24Hour) {
            hour = hour % 12;
            if (hour == 0) { hour = 12; }
        }
        var timeStr = hour.format("%d") + ":" + clock.min.format("%02d");
        var cy = (barH / 2).toNumber();

        dc.setColor(C_TOPTXT, Graphics.COLOR_TRANSPARENT);
        dc.drawText((w * 0.05).toNumber(), cy, Graphics.FONT_TINY, timeStr,
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER);
        dc.drawText(w / 2, cy, Graphics.FONT_TINY, "GIRO",
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        var tempStr = mHasTemp ? mTemp.format("%d") + "\u00B0" : "--\u00B0";
        dc.drawText((w * 0.95).toNumber(), cy, Graphics.FONT_TINY, tempStr,
            Graphics.TEXT_JUSTIFY_RIGHT | Graphics.TEXT_JUSTIFY_VCENTER);

        dc.setColor(C_ACCENT, Graphics.COLOR_TRANSPARENT);
        dc.fillRectangle(0, barH - 2, w, 2);
    }

    // ---------- Heros : vitesse en grand ----------
    hidden function drawHero(dc as Dc, w as Number, y as Number, hH as Number) as Void {
        var cx = w / 2;

        dc.setColor(C_ACCENT, Graphics.COLOR_TRANSPARENT);
        dc.drawText(cx, y + (hH * 0.16).toNumber(), Graphics.FONT_XTINY, "VITESSE",
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        var speedStr = mHasSpeed ? mSpeed.format("%.1f") : "--";
        var speedFont = (speedStr.length() > 4)
            ? Graphics.FONT_NUMBER_HOT
            : Graphics.FONT_NUMBER_THAI_HOT;
        dc.setColor(C_VALUE, Graphics.COLOR_TRANSPARENT);
        dc.drawText(cx, y + (hH * 0.52).toNumber(), speedFont, speedStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        dc.setColor(C_UNIT, Graphics.COLOR_TRANSPARENT);
        dc.drawText(cx, y + (hH * 0.86).toNumber(), Graphics.FONT_TINY, "km/h",
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // ligne accent sous le heros
        var m = (w * 0.085).toNumber();
        dc.setColor(C_ACCENT, Graphics.COLOR_TRANSPARENT);
        dc.fillRectangle(m, y + hH - 2, w - m * 2, 3);
    }

    // ---------- Grille : 4 lignes x 2 colonnes ----------
    hidden function drawGrid(dc as Dc, w as Number, gridY as Number, h as Number) as Void {
        var midX = w / 2;
        var rowH = ((h - gridY) / 4).toNumber();
        var pad = (w * 0.02).toNumber();

        // separateurs
        dc.setColor(C_SEP, Graphics.COLOR_TRANSPARENT);
        dc.fillRectangle(midX - 1, gridY + pad, 2, rowH * 4 - pad * 2);
        for (var i = 1; i < 4; i += 1) {
            dc.fillRectangle(pad, gridY + rowH * i - 1, w - pad * 2, 2);
        }

        var cxL = (w * 0.25).toNumber();
        var cxR = (w * 0.75).toNumber();

        var big = Graphics.FONT_NUMBER_MEDIUM;
        var mid = Graphics.FONT_NUMBER_MILD;

        // Ligne 1 : Puissance (zone Zwift) | Coeur
        drawPower(dc, cxL, gridY, rowH, w);
        drawMetric(dc, cxR, gridY, rowH, "COEUR",
            mHasHr ? mHr.toString() : "--", "bpm", big, C_VALUE);

        // Ligne 2 : Cadence | Pente
        var y1 = gridY + rowH;
        drawMetric(dc, cxL, y1, rowH, "CADENCE",
            mHasCad ? mCad.toString() : "--", "rpm", mid, C_VALUE);
        drawMetric(dc, cxR, y1, rowH, "PENTE",
            mHasGrade ? mGrade.format("%.1f") : "--", "%", mid, C_VALUE);

        // Ligne 3 : Distance | Altitude
        var y2 = gridY + rowH * 2;
        drawMetric(dc, cxL, y2, rowH, "DISTANCE",
            mHasDist ? formatDistance(mDist) : "--", "km", mid, C_VALUE);
        drawMetric(dc, cxR, y2, rowH, "ALTITUDE",
            mHasAlt ? mAlt.toString() : "--", "m", mid, C_VALUE);

        // Ligne 4 : Temps roulant | Denivele +
        var y3 = gridY + rowH * 3;
        drawMetric(dc, cxL, y3, rowH, "TEMPS ROULANT", formatTimer(mTimer), "", mid, C_VALUE);
        drawMetric(dc, cxR, y3, rowH, "DENIVELE +",
            mHasAscent ? mAscent.toString() : "--", "m", mid, C_VALUE);
    }

    // Metrique standard : libelle accent, valeur, unite
    hidden function drawMetric(dc as Dc, cx as Number, top as Number, rowH as Number,
                               label as String, value as String, unit as String,
                               font as Graphics.FontDefinition, valColor as Number) as Void {
        dc.setColor(C_ACCENT, Graphics.COLOR_TRANSPARENT);
        dc.drawText(cx, top + (rowH * 0.24).toNumber(), Graphics.FONT_XTINY, label,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        dc.setColor(valColor, Graphics.COLOR_TRANSPARENT);
        dc.drawText(cx, top + (rowH * 0.57).toNumber(), font, value,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        if (!unit.equals("")) {
            dc.setColor(C_UNIT, Graphics.COLOR_TRANSPARENT);
            dc.drawText(cx, top + (rowH * 0.85).toNumber(), Graphics.FONT_XTINY, unit,
                Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
        }
    }

    // Cellule Puissance : valeur en couleur de zone + barre 6 segments
    hidden function drawPower(dc as Dc, cx as Number, top as Number, rowH as Number, w as Number) as Void {
        var zoneColor = (mZone >= 1) ? getZoneColor(mZone) : C_UNIT;

        dc.setColor(C_ACCENT, Graphics.COLOR_TRANSPARENT);
        dc.drawText(cx, top + (rowH * 0.22).toNumber(), Graphics.FONT_XTINY, "PUISSANCE W",
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        var pwr = mHasPower ? mPower.toString() : "--";
        dc.setColor(zoneColor, Graphics.COLOR_TRANSPARENT);
        dc.drawText(cx, top + (rowH * 0.53).toNumber(), Graphics.FONT_NUMBER_MEDIUM, pwr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // barre de zones
        var barW = (w * 0.40).toNumber();
        var seg = (barW / 6).toNumber();
        var bx = cx - (seg * 6) / 2;
        var by = top + (rowH * 0.84).toNumber();
        var bh = (rowH * 0.11).toNumber();
        if (bh < 5) { bh = 5; }
        for (var z = 1; z <= 6; z += 1) {
            var col = (z <= mZone) ? getZoneColor(z) : C_SEG_OFF;
            dc.setColor(col, Graphics.COLOR_TRANSPARENT);
            dc.fillRectangle(bx + (z - 1) * seg, by, seg - 2, bh);
        }
    }
}

// Distance : 2 decimales sous 100 km, sinon 1 decimale
function formatDistance(km as Float) as String {
    if (km < 100.0) {
        return km.format("%.2f");
    }
    return km.format("%.1f");
}

// Temps : H:MM:SS ou M:SS
function formatTimer(ms as Number) as String {
    var totalSec = (ms / 1000).toNumber();
    var hrs = totalSec / 3600;
    var mins = (totalSec % 3600) / 60;
    var secs = totalSec % 60;
    if (hrs > 0) {
        return hrs.format("%d") + ":" + mins.format("%02d") + ":" + secs.format("%02d");
    }
    return mins.format("%d") + ":" + secs.format("%02d");
}

// Zone Zwift (1..6) selon % FTP
function getZwiftZone(power as Number, ftp as Number) as Number {
    if (ftp <= 0) { return 1; }
    var pct = power.toFloat() / ftp.toFloat() * 100.0;
    if (pct < 60)  { return 1; }
    if (pct < 76)  { return 2; }
    if (pct < 90)  { return 3; }
    if (pct < 105) { return 4; }
    if (pct < 119) { return 5; }
    return 6;
}

// Couleurs des zones Zwift
function getZoneColor(zone as Number) as Number {
    switch (zone) {
        case 1: return 0x9AA0A6; // gris clair - recup
        case 2: return 0x2D9CDB; // bleu - endurance
        case 3: return 0x39B54A; // vert - tempo
        case 4: return 0xF5E617; // jaune - seuil
        case 5: return 0xFC6719; // orange - VO2
        case 6: return 0xE31937; // rouge - anaerobie
        default: return 0x9AA0A6;
    }
}

class GiroPinkApp extends Application.AppBase {

    function initialize() {
        AppBase.initialize();
    }

    function getInitialView() {
        return [new GiroPinkDataField()];
    }
}

function getApp() as GiroPinkApp {
    return Application.getApp() as GiroPinkApp;
}
