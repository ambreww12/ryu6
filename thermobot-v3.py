# --- !!! ---
#   ███████╗████████╗ ██████╗ ██████╗ ██╗██╗
#   ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██║██║
#   ███████╗   ██║   ██║   ██║██████╔╝██║██║
#   ╚════██║   ██║   ██║   ██║██╔═══╝ ╚═╝╚═╝
#   ███████║   ██║   ╚██████╔╝██║     ██╗██╗
#   ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝
# STOP!!
# JUST BECAUSE THE CODE IS PUBLICLY AVAILABLE DOES NOT MEAN YOU HAVE THE RIGHT TO USE IT.
# NONE OF THIS CODE IS LICENSABLE.
# USING WITHOUT PERMISSION CONSTITUTES COPYRIGHT INFRINGEMENT, PUNISHABLE BY STATUATORY DAMAGES OF $750 TO $30,000 ($150,000 IF WILLFUL).
#   ███████ ███████╗ ██████╗      ████████╗ ██████╗ 
#   ╚════██║██╔════╝██╔═████╗     ╚══██╔══╝██╔═══██╗    
#       ██╔╝███████╗██║██╔██║        ██║   ██╔═══██╗
#      ██╔╝ ╚════██║████╔╝██║        ██║   ██╔═══██╗
#      ██║  ███████║╚██████╔╝        ██║    ██████╔
#      ╚═╝  ╚══════╝ ╚═════╝         ╚═╝    ╚═════╝                                 
#   ██╗███████╗ ██████╗       ██████╗  ██████╗  ██████╗  ██╗
#  ███║██╔════╝██╔═████╗     ██╔═████╗██╔═████╗██╔═████╗ ██║
#  ╚██║███████╗██║██╔██║     ██║██╔██║██║██╔██║██║██╔██║ ██║
#   ██║╚════██║████╔╝██║     ████╔╝██║████╔╝██║████╔╝██║ ╚═╝
#   ██║███████║╚██████╔╝ ██╗ ╚██████╔╝╚██████╔╝╚██████╔╝ ██╗
#   ╚═╝╚══════╝ ╚═════╝  █╔    ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝
# YOU HEAR THAT? YOU WANNA RISK THE PRICE OF A CAR OVER A DISCORD BOT? DOUBLE WHAT THE MEDIAN AMERICAN MAKES IN A YEAR?
# YOU HAVE BEEN WARNED!!!

disable_thermoquestions = True
override_blacklist_userID = {1320177605848203403, 1425965786203164693, 992484516016951336}  # lol


import discord
from discord import app_commands
from discord.ui import Button, View, Select
import random
import os
import json
from pathlib import Path

# ============================================================
# POINTS / LEADERBOARD SYSTEM
# ============================================================
POINTS_FILE = Path("points.json")

def load_points() -> dict:
    if POINTS_FILE.exists():
        try:
            with open(POINTS_FILE, "r") as f:
                data = json.load(f)
                if "thermo" not in data:
                    data["thermo"] = {}
                if "circuit" not in data:
                    data["circuit"] = {}
                return data
        except Exception:
            pass
    return {"thermo": {}, "circuit": {}}

def save_points(data: dict):
    with open(POINTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Only this server is allowed to modify leaderboard points
ALLOWED_POINTS_SERVER_ID = 133777777777777777777777777777777777777777777777777777777777777 # effectively zero

# Servers the bot will completely refuse to serve
BLACKLISTED_SERVER_IDS = {
    1530684056931533002,
}

def blacklist_override_text(interaction: discord.Interaction) -> str:
    """Return a short notice if this user is overriding a blacklisted server."""
    if (
        interaction.guild
        and interaction.guild.id in BLACKLISTED_SERVER_IDS
        and interaction.user.id in override_blacklist_userID
    ):
        return "\n\n🔓 Granted: UserID found in 'override_blacklist_userID'"
    return ""


def can_award(interaction: discord.Interaction, leaderboard: str) -> bool:
    """Admins can award on either board.
    Thermo Mods can award only on thermo.
    Circuit Mods can award only on circuit.
    Modifications are ONLY allowed in the designated server.
    """
    if not interaction.guild:
        return False
    # Restrict point modifications to one specific server
    if interaction.guild.id != ALLOWED_POINTS_SERVER_ID:
        return False
    member = interaction.user
    if not isinstance(member, discord.Member):
        return False

    # Discord Administrator permission always allowed
    if member.guild_permissions.administrator:
        return True

    role_names = [r.name.lower() for r in member.roles]

    # Explicit admin-style role names
    if any(rn in ("admin", "admins", "administrator") for rn in role_names):
        return True

    if leaderboard == "thermo":
        return any(("thermo" in rn and "mod" in rn) for rn in role_names)
    if leaderboard == "circuit":
        return any(("circuit" in rn and "mod" in rn) for rn in role_names)
    return False


# THERMODYNAMICS QUESTIONS
QUESTIONS = {
    "Laws of Thermodynamics": {
        "Novice": [
            ("Which law of thermodynamics defines temperature through thermal equilibrium?",
             ["First Law", "Second Law", "Zeroth Law", "Third Law"], 2),
            ("The First Law is a statement of:",
             ["Direction of processes", "Conservation of energy", "Increase of entropy", "Absolute zero"], 1),
            ("Absolute zero corresponds to:",
             ["0 °C", "273 K", "0 K", "−273 °C only"], 2),
            ("Which scientist formulated the Third Law of Thermodynamics?",
             ["James Joule", "Lord Kelvin", "Walther Nernst", "James Clerk Maxwell"], 2),
            ("The Third Law states that the entropy of a perfect crystal approaches zero as:",
             ["Pressure approaches zero", "Temperature approaches absolute zero", "Volume approaches zero", "The system becomes isolated"], 1),
            ("Entropy is a measure of:",
             ["Temperature", "Energy dispersal / disorder", "Pressure", "Volume"], 1),
            ("The SI unit of entropy is:",
             ["J/K", "J", "W/K", "K"], 0),
            ("Which process has Q = 0?",
             ["Isothermal", "Isobaric", "Adiabatic", "Isochoric"], 2),
            ("Cp − Cv for an ideal gas equals:",
             ["0", "R", "γ", "1"], 1),
            ("In the sign convention ΔU = Q − W, positive W means:",
             ["Heat enters the system", "The system does work on the surroundings", "Surroundings do work on the system", "Heat leaves the system"], 1),
        ],
        "Intermediate": [
            ("The Zeroth Law is most closely related to:",
             ["Energy conservation", "Definition of temperature", "Direction of heat flow", "Maximum efficiency"], 1),
            ("In an isolated system, a spontaneous irreversible process always increases:",
             ["Internal energy", "Enthalpy", "Entropy", "Gibbs free energy"], 2),
            ("Which scientist first clearly formulated the Second Law of Thermodynamics?",
             ["James Joule", "Rudolf Clausius", "Lord Kelvin", "James Clerk Maxwell"], 1),
            ("Maxwell's Demon was designed to challenge which law of thermodynamics?",
             ["Zeroth Law", "First Law", "Second Law", "Third Law"], 2),
            ("The Third Law of Thermodynamics is also commonly called:",
             ["Joule's Law", "Nernst Heat Theorem", "Kelvin Principle", "Carnot Principle"], 1),
            ("For a cyclic process, ΔU is:",
             ["Positive", "Negative", "Zero", "Equal to Q"], 2),
            ("The First Law applied to a complete cycle gives:",
             ["ΔU = Q", "Q_net = W_net", "W = 0", "Q = 0"], 1),
            ("An ideal gas expands isothermally. Which quantity is zero?",
             ["Q", "W", "ΔU", "ΔS"], 2),
            ("When ice melts reversibly at 0 °C, ΔS of the system is:",
             ["Zero", "Positive", "Negative", "Undefined"], 1),
            ("For an ideal gas in reversible adiabatic expansion:",
             ["Temperature increases", "Internal energy decreases", "Entropy of system increases", "Heat is absorbed"], 1),
        ],
        "Hard": [
            ("For a reversible process, ∮ dQ/T equals:",
             ["ΔS_system", "0", "ΔS_universe", "Q_net / T"], 1),
            ("In a Carnot cycle the two isothermal processes are accompanied by:",
             ["No entropy change of the universe", "Positive entropy change of the universe", "Negative entropy change of the system", "Zero heat transfer"], 0),
            ("Carnot’s Principle states that no heat engine operating between two temperatures can be more efficient than a:",
             ["Real irreversible engine", "Reversible engine operating between the same temperatures", "Steam engine", "Engine using ideal gas"], 1),
            ("In the derivation of the Clausius inequality, the key statement is that for any real cycle:",
             ["∮ dQ/T ≤ 0", "∮ dQ/T ≥ 0", "∮ dQ/T = 0", "∮ dQ = 0"], 0),
            ("For a cyclic device operating between two reservoirs, the equality ΔS_reservoirs = 0 holds only for:",
             ["Any real engine", "A reversible engine", "A refrigerator", "A heat pump with COP > 1"], 1),
            ("A system has ΔU = −250 J and performs 100 J of work. Heat transferred to the system is:",
             ["−350 J", "−150 J", "+150 J", "+350 J"], 1),
            ("Heat absorbed at constant pressure is equal to the change in:",
             ["Internal energy", "Enthalpy", "Entropy", "Helmholtz free energy"], 1),
            ("For an ideal gas, (∂U/∂V)_T equals:",
             ["R", "Cv", "0", "Cp − R"], 2),
            ("Compared to an isothermal curve, an adiabatic curve on a PV diagram is:",
             ["Less steep", "Steeper", "Identical", "Horizontal"], 1),
            ("An isentropic process is one that occurs at constant:",
             ["Temperature", "Pressure", "Entropy", "Volume"], 2),
        ],
        "Very Hard": [
            ("The resolution to Maxwell’s Demon paradox involves the fact that the demon:",
             ["Must expend energy / increase entropy to observe and sort molecules", "Cannot exist in reality", "Violates the First Law", "Only works at absolute zero"], 0),
            ("When two objects at different temperatures are placed in contact inside an otherwise isolated system, the final common temperature is reached when:",
             ["Their internal energies become equal", "The entropy of the universe is maximized", "Their heat capacities become equal", "No more energy is available"], 1),
            ("A system’s entropy can decrease only if:",
             ["The process is adiabatic", "The surroundings increase in entropy by at least as much", "The process is isothermal", "Absolute zero is approached"], 1),
            ("The change in entropy of the universe for any real (irreversible) process is:",
             ["Zero", "Negative", "Positive", "Equal to ΔS_system"], 2),
            ("In free expansion of an ideal gas, which of the following is true?",
             ["ΔS_system = 0", "ΔS_universe = 0", "ΔS_system > 0 and ΔS_universe > 0", "Q = W ≠ 0"], 2),
            ("The entropy change of the universe for the free expansion of an ideal gas into vacuum is equal to:",
             ["0", "nR ln(V2/V1)", "nCv ln(T2/T1)", "−nR ln(V2/V1)"], 1),
            ("For a heat engine exchanging heat only with two reservoirs, ΔS of the reservoirs is:",
             ["−QH/TH + QC/TC ≥ 0", "QH/TH − QC/TC ≥ 0", "Always zero", "Always negative"], 0),
            ("In a reversible cycle, ∮ (dQ/T) equals:",
             ["ΔS_system", "0", "ΔS_universe", "Q_net / T_avg"], 1),
            ("The change in entropy of the universe when 1 mole of ideal gas expands freely into vacuum to double its volume is:",
             ["0", "R ln 2", "−R ln 2", "Cv ln 2"], 1),
            ("According to the Scioly wiki treatment of the Third Law, two objects at different temperatures can never reach exactly the same temperature because:",
             ["Heat transfer stops completely", "The approach is asymptotic (exponential decay/growth)", "The Second Law forbids it", "Measurement tools are imperfect"], 1),
        ],
        "Impossible": [
            ("In the derivation of Carnot efficiency, the key step that produces η = 1 − TC/TH is the recognition that for the reversible cycle:",
             ["QH/TH = QC/TC", "QH = QC", "W = QH", "ΔS_universe > 0"], 0),
            ("A system absorbs heat Q from a reservoir at T_h and rejects heat to a reservoir at T_c while producing work W. The entropy production of the universe is:",
             ["Q/T_h − (Q − W)/T_c", "(Q − W)/T_c − Q/T_h", "W/T_h", "0"], 1),
            ("The Helmholtz free energy F satisfies the relation (∂F/∂T)_V =:",
             ["−S", "S", "−P", "P"], 0),
            ("For a thermodynamic system, the Helmholtz free energy F = U − TS. The natural variables of F are:",
             ["S, V", "T, V", "T, P", "S, P"], 1),
            ("The natural variables of the Gibbs free energy G are:",
             ["S, V", "T, V", "T, P", "S, P"], 2),
        ]
    },
    "Thermodynamic Processes": {
        "Novice": [
            ("Work done in an isochoric process is:", ["Maximum", "PΔV", "Zero", "Equal to Q"], 2),
            ("An isobaric process on a PV diagram is represented by a:", ["Vertical line", "Horizontal line", "Hyperbola", "Steep curve"], 1),
            ("Which process has Q = 0?", ["Isothermal", "Isobaric", "Adiabatic", "Isochoric"], 2),
            ("The process in which both pressure and volume change but temperature stays constant is called:", ["Isobaric", "Isochoric", "Isothermal", "Adiabatic"], 2),
            ("In free expansion of an ideal gas into vacuum, work is:", ["Maximum", "Zero", "Equal to Q", "Negative"], 1),
            ("For an isochoric process, work done by the system is:", ["PΔV", "nRT ln(V2/V1)", "Zero", "Equal to Q"], 2),
            ("On a P-V diagram the area under a process curve represents:", ["Heat", "Work", "Change in internal energy", "Entropy"], 1),
            ("Which of the following is NOT a state function?", ["Internal energy", "Enthalpy", "Heat", "Entropy"], 2),
            ("In an isothermal process for an ideal gas, ΔU is:", ["Positive", "Negative", "Zero", "Equal to W"], 2),
            ("The slope of an isobar on a P-V diagram is:", ["Infinite", "Zero", "Negative", "Positive and finite"], 1),
        ],
        "Intermediate": [
            ("An ideal gas expands isothermally. Which quantity is zero?", ["Q", "W", "ΔU", "ΔS"], 2),
            ("For a reversible adiabatic process on an ideal gas:", ["PV = constant", "TV^{γ−1} = constant", "T/V = constant", "P/T = constant"], 1),
            ("On a PV diagram, a vertical line represents:", ["Isobaric", "Isothermal", "Isochoric", "Adiabatic"], 2),
            ("In an isobaric process, Q equals:", ["ΔU", "ΔH", "W", "0"], 1),
            ("For a cyclic process, ΔU is:", ["Positive", "Negative", "Zero", "Equal to Q"], 2),
            ("An ideal gas is compressed isothermally. The heat released by the gas is:", ["Zero", "Equal to the work done on the gas", "Equal to ΔU", "Greater than the work done on the gas"], 1),
            ("For a reversible isothermal expansion of an ideal gas, ΔS_system is:", ["Zero", "nR ln(V2/V1)", "Negative", "nCv ln(T2/T1)"], 1),
            ("Which process has the largest magnitude of work done by the system for the same volume change (ideal gas)?", ["Isothermal", "Adiabatic", "Isochoric", "Isobaric"], 3),
            ("A diathermic, rigid, impermeable wall allows:", ["Heat and matter", "Only heat", "Only work", "Nothing"], 1),
            ("During a phase change at constant pressure, temperature:", ["Increases steadily", "Decreases steadily", "Remains approximately constant", "Fluctuates randomly"], 2),
        ],
        "Hard": [
            ("An ideal gas expands reversibly and isothermally from V to 2V. The work done by the gas is:", ["nRT", "nRT ln(2)", "0", "½ nRT"], 1),
            ("In free expansion of an ideal gas into vacuum:", ["W > 0 and Q > 0", "W = 0, Q = 0, ΔU = 0", "Temperature decreases", "ΔU > 0"], 1),
            ("For a reversible adiabatic process:", ["ΔS_system > 0", "ΔS_system = 0", "ΔU = 0", "Q ≠ 0"], 1),
            ("Compared to an isothermal curve, an adiabatic curve on a PV diagram is:", ["Less steep", "Steeper", "Identical", "Horizontal"], 1),
            ("An isentropic process is one that occurs at constant:", ["Temperature", "Pressure", "Entropy", "Volume"], 2),
            ("For a reversible process, an adiabatic process is also:", ["Isobaric", "Isothermal", "Isentropic", "Isochoric"], 2),
            ("An ideal gas expands from V to 3V in a reversible adiabatic process. If γ = 1.4, the final temperature is:", ["T / 3^{0.4}", "T × 3^{0.4}", "T / 3", "T × 3"], 0),
            ("For a polytropic process with n = 0, the process is:", ["Isothermal", "Isobaric", "Isochoric", "Adiabatic"], 1),
            ("The work done in a reversible adiabatic expansion of an ideal gas can also be written as:", ["nR ln(V2/V1)", "nCp(T1 − T2)", "nCv(T1 − T2)", "P1V1 − P2V2"], 2),
            ("In a reversible polytropic process with n = γ, the heat transfer Q is:", ["nCv(T2 − T1)", "nCp(T2 − T1)", "0", "nR(T2 − T1)/(γ − 1)"], 2),
        ],
        "Very Hard": [
            ("An ideal gas undergoes a process in which T ∝ V². The molar heat capacity for this process is:", ["Cv + R/2", "Cv + 2R", "Cp − R", "Cv + R"], 1),
            ("An ideal gas undergoes a process in which PV² = constant. The molar heat capacity for this process is:", ["Cv + R/2", "Cv + 2R", "Cp − R", "Cv + R"], 0),
            ("For an ideal gas undergoing a polytropic process PV^n = constant, the molar heat capacity is:", ["Cv + R/(1−n)", "Cv + R/(n−1)", "Cp − R", "Cv only"], 0),
            ("An ideal gas follows the process TV^{x} = constant. For the molar heat capacity to be 4R, the value of x is: (take γ = 1.4)", ["0.5", "1.0", "1.5", "2.0"], 0),
            ("An ideal gas follows TV^x = constant. If the molar heat capacity for the process is 3R and γ = 5/3, the value of x is:", ["0.5", "1", "1.5", "2"], 0),
            ("In the expression for reversible adiabatic work of an ideal gas, W = (P1V1 − P2V2)/(γ−1) is equivalent to:", ["nR(T1 − T2)", "nCv(T1 − T2)", "nCp(T1 − T2)", "PΔV"], 1),
            ("The work done in a reversible adiabatic process for an ideal gas can be written as:", ["nRT ln(V2/V1)", "nCv(T1 − T2)", "PΔV", "Zero"], 1),
            ("For a reversible adiabatic process on an ideal gas, which is true?", ["PV = constant", "TV^{γ−1} = constant", "T/V = constant", "P/T^γ = constant"], 1),
            ("During a reversible adiabatic process for an ideal gas, which remains constant?", ["TV^{γ−1}", "T/V", "PV", "P/T"], 0),
            ("In free expansion of an ideal gas into vacuum:", ["W > 0 and Q > 0", "W = 0, Q = 0, ΔU = 0", "Temperature decreases", "ΔU > 0"], 1),
        ],
        "Impossible": [
            ("In a reversible polytropic process PV^n = constant, the expression for work done by the gas is:", ["(P1V1 − P2V2)/(n−1)", "nR(T1 − T2)/(n−1)", "Both A and B are equivalent", "R(T1 − T2) ln(V2/V1)"], 2),
            ("A system goes from state A to B via two different paths. The difference in heat absorbed along the two paths equals the difference in:", ["Internal energy", "Work done", "Enthalpy", "Entropy"], 1),
            ("The Joule-Thomson coefficient μ = (∂T/∂P)_H. For an ideal gas μ is:", ["Positive", "Negative", "Zero", "Infinite"], 2),
        ]
    },
    "Heat Transfer": {
        "Novice": [
            ("Heat is best described as:", ["A substance stored in an object", "Energy transferred due to a temperature difference", "The same as temperature", "Internal energy"], 1),
            ("The specific heat of water is approximately:", ["334 J/kg·K", "2256 J/kg·K", "4184 J/kg·K", "1000 J/kg·K"], 2),
            ("Latent heat of fusion of ice is approximately:", ["2256 kJ/kg", "334 kJ/kg", "4184 J/kg", "100 kJ/kg"], 1),
            ("Latent heat of vaporization of water is approximately:", ["334 kJ/kg", "2260 kJ/kg", "4184 J/kg·K", "100 kJ/kg"], 1),
            ("The conversion from Celsius to Kelvin is:", ["T_K = T_C − 273.15", "T_K = T_C + 273.15", "T_K = (9/5)T_C + 32", "T_K = T_C × 273.15"], 1),
            ("Temperature intervals in Celsius and Kelvin are:", ["Different by a factor of 9/5", "Identical in size", "Offset by 32", "Unrelated"], 1),
            ("Extensive properties depend on:", ["The amount of matter", "The type of substance only", "Temperature only", "Pressure only"], 0),
            ("An intensive property is one that:", ["Depends on the size of the system", "Does not depend on the amount of matter", "Is always a state function", "Can only be temperature"], 1),
            ("Which of the following is a state function?", ["Heat", "Work", "Internal energy", "Both heat and work"], 2),
            ("Heat capacity at constant volume is related to:", ["ΔH = nCpΔT", "ΔU = nCvΔT", "W = PΔV", "Q = 0"], 1),
        ],
        "Intermediate": [
            ("Conduction heat transfer through a slab is proportional to:", ["1/thickness", "Thickness squared", "The square of the temperature difference", "Surface roughness only"], 0),
            ("Newton’s law of cooling states that the rate of temperature change is proportional to:", ["The absolute temperature", "The temperature difference with surroundings", "The square of the temperature", "Time only"], 1),
            ("In the expression T(t) = T∞ + (T0 − T∞)e^(−kt), k is the:", ["Thermal conductivity", "Cooling constant", "Specific heat", "Latent heat"], 1),
            ("Thermal resistance for conduction is:", ["kA/L", "L/(kA)", "hA", "1/(hA)"], 1),
            ("In series thermal resistances, total resistance is:", ["The reciprocal of the sum", "The sum of the individual resistances", "The product of the resistances", "The average resistance"], 1),
            ("Newton’s law of cooling is most accurate when the temperature difference is:", ["Very large", "Moderate", "Near absolute zero", "Independent of the difference"], 1),
            ("Coffee-cup calorimetry is approximately a:", ["Constant-volume process", "Constant-pressure process", "Adiabatic process", "Isothermal process"], 1),
            ("Bomb calorimetry is carried out at constant:", ["Pressure", "Volume", "Temperature", "Entropy"], 1),
            ("When calculating final temperature of several objects mixed with no phase change:", ["Tf = Σ (mi ci Ti) / Σ (mi ci)", "Tf = Σ mi Ti / Σ mi", "Tf = average of all Ti", "Tf is always the highest Ti"], 0),
            ("The equation Q = mL is used for:", ["Temperature change with no phase change", "Phase changes", "Adiabatic processes only", "Isothermal compression"], 1),
        ],
        "Hard": [
            ("Wien’s displacement law relates:", ["Pressure and volume", "Wavelength of maximum emission and temperature", "Heat capacity and temperature", "Entropy and volume"], 1),
            ("The Stefan-Boltzmann law gives net radiation heat transfer proportional to:", ["T", "T²", "T³", "T⁴"], 3),
            ("Net radiation heat transfer between a surface and large surroundings is:", ["εσA(Ts − Tsur)", "εσA(Ts⁴ − Tsur⁴)", "σA(Ts⁴ − Tsur⁴) only", "hA(Ts − Tsur)"], 1),
            ("In Newton’s law of cooling, after one time constant τ the remaining temperature difference is approximately:", ["50%", "36.8%", "25%", "10%"], 1),
            ("The time constant τ for a lumped thermal system is:", ["hA / mc", "mc / hA", "kA / L", "L / kA"], 1),
            ("A plot of ln|T − T∞| versus time should be approximately linear with slope:", ["+k", "−k", "k²", "1/k"], 1),
            ("In Newton cooling analysis, a sudden increase in air speed over an object primarily increases:", ["Thermal conductivity k", "The convection coefficient h", "The specific heat c", "The latent heat"], 1),
            ("For radiation, a surface with low emissivity is most effective at reducing heat transfer when it faces:", ["A solid conductor", "An air gap or vacuum", "A high-conductivity metal", "A phase-change material"], 1),
            ("If a calorimeter’s heat capacity is ignored when calculating the specific heat of a hot object, the calculated value is usually:", ["Too high", "Too low", "Unaffected", "Randomly wrong"], 1),
            ("A diathermal boundary allows:", ["Matter to pass", "Heat to pass", "Work only", "Nothing to pass"], 1),
        ],
        "Very Hard": [
            ("A small metal object obeys Newton’s Law of Cooling. In a room held at a constant 25 °C, the object cools from 95 °C to 65 °C in exactly six minutes. The object is then immediately transferred into a second room whose temperature is held constant at 5 °C. Assuming k doesn't change, determine the temperature of the object 8 mins after it was transferred.",
             ["33.5 °C", "38.2 °C", "41.0 °C", "44.9 °C"], 0),
            ("A hot object is cooling in a room held at constant temperature T_a = 25 °C. At time t = 0 its temperature is T_0 = 85 °C. After 8 minutes its temperature has fallen to 65 °C. Estimate the object's temperature after 20 minutes.",
             ["26 °C", "32 °C", "47 °C", "63 °C"], 2),
        ],
        "Impossible": [
            ("""A solid metal sphere of radius 2.5 cm, density 7800 kg m^-3, and specific heat capacity c = 450 J kg^-1 K^-1 is suspended in a large evacuated
        chamber whose walls are held at a constant temperature T_a = 300 K. The sphere’s surface has emissivity ε = 0.80. In addition to thermal radiation,
        a weak convective cooling term is present that follows Newton’s Law of Cooling with heat-transfer coefficient h = 4.5 W m^-2 K^-1. The sphere is initially at 900 K.
        Find the approximate time needed for the sphere's temperature to fall under 450 K.""",
             ["1250 s", "1775 s", "1945 s", "2305 s"], 1),
        ]
    },
    "Ideal Gas & Gas Laws": {
        "Novice": [
            ("For an ideal gas, internal energy depends only on:", ["Pressure", "Volume", "Temperature", "Entropy"], 2),
            ("Cp − Cv for an ideal gas equals:", ["0", "R", "γ", "1"], 1),
            ("Boyle’s Law states that at constant temperature, pressure and volume are:", ["Directly proportional", "Inversely proportional", "Equal", "Independent"], 1),
            ("Charles’ Law states that at constant pressure, volume is directly proportional to:", ["Celsius temperature", "Kelvin temperature", "Pressure", "Number of moles"], 1),
            ("The ideal-gas law is written as:", ["PV = nRT", "P/V = nRT", "PV = nR/T", "P + V = nRT"], 0),
            ("Gay-Lussac’s Law states that at constant volume, pressure is directly proportional to:", ["Celsius temperature", "Kelvin temperature", "Volume", "Number of moles"], 1),
            ("An open thermodynamic system allows which of the following to cross its boundary?", ["Only heat", "Only matter", "Matter, heat, and work", "Nothing"], 2),
            ("A closed system allows heat and work to cross the boundary but does not allow:", ["Energy", "Matter", "Entropy", "Temperature change"], 1),
            ("An isolated thermodynamic system allows which of the following to cross its boundary?", ["Heat only", "Matter only", "Work only", "Nothing"], 3),
            ("According to the kinetic theory, collisions between gas molecules are assumed to be:", ["Inelastic", "Perfectly elastic", "Partially elastic", "Negligible"], 1),
        ],
        "Intermediate": [
            ("Joule’s Second Law states that the internal energy of an ideal gas depends only on:", ["Pressure and volume", "Temperature", "The path taken", "Work done"], 1),
            ("For an ideal gas, ΔU equals:", ["nCpΔT", "nCvΔT", "PΔV", "nR ln(V2/V1)"], 1),
            ("For an ideal gas, ΔH equals:", ["nCvΔT", "nCpΔT", "W", "Q − W"], 1),
            ("The relationship Cp − Cv for an ideal gas is:", ["Zero", "R", "γ", "1"], 1),
            ("γ is defined as:", ["Cv/Cp", "Cp/Cv", "Cp − Cv", "R/Cv"], 1),
            ("The kinetic theory of heat states that the average kinetic energy of gas particles depends only on:", ["Pressure", "Volume", "Temperature", "The number of collisions"], 2),
            ("An open system allows which of the following to cross its boundary?", ["Only energy", "Only matter", "Both matter and energy", "Neither matter nor energy"], 2),
            ("A closed system allows energy but not:", ["Work", "Heat", "Matter", "Temperature change"], 2),
            ("For an ideal gas, the difference Cp − Cv equals:", ["R only for monatomic gases", "R for any ideal gas", "γR", "Zero"], 1),
            ("The change in enthalpy for an ideal gas depends only on:", ["Pressure", "Volume", "Temperature", "The path"], 2),
        ],
        "Hard": [
            ("For an ideal gas, (∂U/∂V)_T equals:", ["R", "Cv", "0", "Cp − R"], 2),
            ("For an ideal gas, (∂H/∂P)_T equals:", ["0", "V", "−V", "T(∂V/∂T)_P − V"], 0),
            ("The ideal-gas entropy change at constant volume is given by:", ["nCv ln(T2/T1)", "nCp ln(T2/T1)", "nR ln(V2/V1)", "Zero"], 0),
            ("The ideal-gas entropy change involving pressure is:", ["nCv ln(T2/T1) + nR ln(V2/V1)", "nCp ln(T2/T1) − nR ln(P2/P1)", "nR ln(T2/T1)", "Cv ln(P2/P1)"], 1),
            ("The Joule-Thomson coefficient for an ideal gas is zero because:", ["Enthalpy depends only on temperature", "Internal energy depends only on temperature", "Both of the above", "Neither"], 2),
            ("van der Waals’ equation corrects the ideal gas law for:", ["Only molecular volume", "Only attractive forces", "Both attractive forces and molecular volume", "Temperature dependence of R"], 2),
            ("For a van der Waals gas, the internal pressure (∂U/∂V)_T is equal to:", ["0", "a/V_m²", "b", "R/V_m"], 1),
            ("One mole of van der Waals gas expands isothermally from V1 to V2. The change in internal energy is:", ["0", "a(1/V1 − 1/V2)", "RT ln((V2−b)/(V1−b))", "−a(1/V1 − 1/V2)"], 1),
            ("The critical compressibility factor Zc for a van der Waals gas is exactly:", ["3/8", "1/4", "1/2", "1/8"], 0),
            ("In a throttling process (Joule-Thomson expansion) for an ideal gas:", ["Temperature always drops", "Enthalpy is constant", "Entropy is constant", "Internal energy increases"], 1),
        ],
        "Very Hard": [
            ("One mole of a van der Waals gas expands isothermally from V1 to V2. The work done is:", ["RT ln((V2−b)/(V1−b))", "RT ln(V2/V1)", "RT ln((V2−b)/(V1−b)) + a(1/V1 − 1/V2)", "None of these"], 2),
            ("For a van der Waals gas, the inversion temperature (where μ_JT = 0) is given by:", ["2a/Rb", "a/Rb", "a/(2Rb)", "2a/(Rb)"], 0),
            ("The critical compressibility factor Zc = PcVc / RTc for a van der Waals gas is:", ["0.375", "0.25", "0.5", "0.125"], 0),
            ("For a photon gas (blackbody radiation), the pressure P is related to energy density u by:", ["P = u/3", "P = u", "P = 3u", "P = u/2"], 0),
            ("For a photon gas, the internal energy U is related to volume and temperature by U ∝:", ["VT", "VT²", "VT³", "VT⁴"], 3),
            ("For blackbody radiation, the entropy S is related to internal energy U and temperature by:", ["S = U/T", "S = (4/3)U/T", "S = (3/4)U/T", "S = U/(3T)"], 1),
        ],
        "Impossible": []
    },
    "Cycles": {
        "Novice": [
            ("Carnot efficiency between 450 K and 300 K is:", ["25%", "33.3%", "50%", "66.7%"], 1),
            ("The efficiency of any real heat engine is always:", ["Equal to Carnot efficiency", "Greater than Carnot efficiency", "Less than Carnot efficiency", "Independent of temperatures"], 2),
            ("On a P-V diagram a clockwise cycle represents:", ["Net work input", "Net work output", "Zero net work", "An isentropic process"], 1),
            ("Carnot efficiency is given by:", ["1 − Qc/Qh", "1 − Tc/Th (temperatures in kelvin)", "W/Qc", "Th/Tc"], 1),
            ("COP of a refrigerator is defined as:", ["W/Qc", "Qc/W", "Qh/W", "W/Qh"], 1),
            ("COP of a heat pump is:", ["Qc/W", "Qh/W", "W/Qh", "The same as refrigerator COP"], 1),
            ("The Otto cycle models:", ["A steam power plant", "A spark-ignition engine with constant-volume heat addition", "A gas turbine", "A refrigerator"], 1),
            ("The Diesel cycle features heat addition at:", ["Constant volume", "Constant pressure", "Constant temperature", "Constant entropy"], 1),
            ("In the Otto cycle, the heat rejection occurs at:", ["Constant pressure", "Constant volume", "Constant temperature", "Constant entropy"], 1),
            ("A refrigerator has a COP of 4. If it removes 800 J from the cold reservoir, the work input required is:", ["160 J", "200 J", "3200 J", "1000 J"], 1),
        ],
        "Intermediate": [
            ("A Carnot refrigerator operates between −10 °C and 25 °C. Its COP is closest to:", ["4.5", "7.5", "10.2", "12.8"], 1),
            ("A Carnot engine has efficiency 1/3. If the sink temperature is 27 °C, the source temperature is:", ["400 K", "450 K", "500 K", "600 K"], 1),
            ("A heat engine absorbs 800 J from a 600 K reservoir and rejects heat to a 300 K reservoir. Maximum possible work output is:", ["200 J", "400 J", "500 J", "600 J"], 1),
            ("The efficiency of an ideal Otto cycle with compression ratio r is:", ["1 − 1/r", "1 − 1/r^{γ−1}", "1 − r^{γ−1}", "1 − (γ−1)/r"], 1),
            ("The efficiency of an ideal Brayton cycle with pressure ratio rp is:", ["1 − 1/rp", "1 − 1/rp^{(γ−1)/γ}", "1 − rp^{(γ−1)/γ}", "1 − (γ−1)/rp"], 1),
            ("A Carnot engine operating between 600 K and 300 K produces 400 J of work. The heat rejected to the cold reservoir is:", ["200 J", "400 J", "600 J", "800 J"], 1),
            ("The efficiency of a Carnot engine is 40%. If the temperature of the sink is 27 °C, the temperature of the source is:", ["227 °C", "327 °C", "500 °C", "77 °C"], 0),
            ("In the Carnot cycle, the process in which the gas is thermally isolated and expands while its temperature decreases is:", ["Isothermal expansion", "Reversible adiabatic expansion", "Isothermal compression", "Adiabatic compression"], 1),
            ("In the Carnot cycle, the net change in entropy of the universe is:", ["Positive", "Negative", "Zero", "Dependent on the temperatures"], 2),
            ("The two adiabatic processes in the Carnot cycle are characterized by:", ["ΔS = 0 (isentropic)", "Q ≠ 0", "ΔU = 0", "Constant pressure"], 0),
        ],
        "Hard": [
            ("A Carnot engine operates between T and T/2. Another identical engine operates between T/2 and T/4. The ratio of their efficiencies is:", ["1 : 1", "1 : 2", "2 : 1", "3 : 1"], 0),
            ("A heat engine operates with two Carnot engines in series. The first operates between T and T/2, the second between T/2 and T/4. The overall efficiency is:", ["1/2", "3/4", "7/8", "15/16"], 1),
            ("The efficiency of a Carnot engine working between temperatures T and T − ΔT (ΔT ≪ T) is approximately:", ["ΔT/T", "2ΔT/T", "ΔT/(2T)", "(ΔT/T)²"], 0),
            ("In the T-S diagram of a Carnot cycle, the heat absorbed during the isothermal expansion is represented by:", ["Area under the upper horizontal line", "Height of the rectangle", "Width of the rectangle", "Diagonal of the rectangle"], 0),
            ("An ideal gas is taken through a cycle consisting of isothermal expansion, isochoric cooling, and adiabatic compression back to the original state. Net work is:", ["Positive (engine)", "Negative (refrigerator)", "Zero", "Cannot be determined without numbers"], 0),
        ],
        "Very Hard": [],
        "Impossible": []
    },
    "History": {
        "Novice": [
            ("The SI unit of energy is named after:", ["James Clerk Maxwell", "James Prescott Joule", "Daniel Fahrenheit", "Walther Nernst"], 1),
            ("Who is often called the 'Father of Thermodynamics'?", ["James Joule", "Rudolf Clausius", "Sadi Carnot", "Lord Kelvin"], 2),
            ("Who introduced the concept of entropy in 1865?", ["Lord Kelvin", "Sadi Carnot", "Rudolf Clausius", "Walther Nernst"], 2),
            ("Who invented the mercury thermometer?", ["Galileo Galilei", "Daniel Gabriel Fahrenheit", "Anders Celsius", "Lord Kelvin"], 1),
            ("The Celsius temperature scale was originally proposed by:", ["Carl Linnaeus", "Anders Celsius", "Daniel Fahrenheit", "Lord Kelvin"], 1),
            ("Absolute temperature is measured using the scale named after:", ["Joule", "Celsius", "Kelvin", "Clausius"], 2),
            ("Which scientist built the first open thermometer?", ["Daniel Fahrenheit", "Galileo Galilei", "Anders Celsius", "James Joule"], 1),
            ("Who coined the word 'thermodynamics'?", ["James Joule", "Lord Kelvin", "Rudolf Clausius", "Walther Nernst"], 1),
            ("Who is credited with determining the value of absolute zero?", ["Lord Kelvin", "James Joule", "Sadi Carnot", "James Clerk Maxwell"], 0),
            ("Which famous physicist proposed the thought experiment known as 'Maxwell's Demon'?", ["Lord Kelvin", "James Clerk Maxwell", "Rudolf Clausius", "Sadi Carnot"], 1),
        ],
        "Intermediate": [
            ("Which scientist is credited with discovering the mechanical equivalent of heat, helping establish the First Law of Thermodynamics?", ["James Prescott Joule", "Sadi Carnot", "Rudolf Clausius", "Lord Kelvin"], 0),
            ("Who developed the Nernst equation, widely used in electrochemistry?", ["Walther Nernst", "Rudolf Clausius", "James Clerk Maxwell", "Lord Kelvin"], 0),
            ("The Fahrenheit temperature scale is named after:", ["A Swedish astronomer", "A Dutch-German physicist", "A Scottish physicist", "A German chemist"], 1),
            ("Which scientist founded the Uppsala Astronomical Observatory?", ["James Clerk Maxwell", "Anders Celsius", "Lord Kelvin", "Galileo Galilei"], 1),
            ("The caloric theory of heat was primarily developed by:", ["James Clerk Maxwell", "Antoine Lavoisier", "Sadi Carnot", "James Joule"], 1),
            ("According to the caloric theory, which of the following assumptions is the only one considered true?", ["Heat is a fluid that flows from hot to cold", "Heat is conserved", "Heat is weightless", "Sensible heat causes temperature increase"], 2),
            ("Which early theory of heat was replaced by Joule's experiments?", ["Atomic theory", "Wave theory", "Caloric theory", "Kinetic theory"], 2),
            ("Before Joule's experiments, Carnot's original analysis of heat engines was based primarily on:", ["The kinetic theory of gases", "The caloric theory of heat", "Statistical mechanics", "Electromagnetism"], 1),
            ("Which pair of scientists are most directly associated with the Second and Third Laws of Thermodynamics, respectively?", ["Joule and Kelvin", "Clausius and Nernst", "Carnot and Maxwell", "Fahrenheit and Celsius"], 1),
            ("Which of the following scientists died before the concept of entropy was introduced?", ["Rudolf Clausius", "Sadi Carnot", "Lord Kelvin", "Walther Nernst"], 1),
        ],
        "Hard": [
            ("The Carnot cycle was first described in which publication?", ["On the Mechanical Theory of Heat", "Reflections on the Motive Power of Fire", "Experimental Researches on Electricity", "The Kinetic Theory of Gases"], 1),
            ("Walther Nernst was awarded the 1920 Nobel Prize in:", ["Physics", "Chemistry", "Medicine", "Mathematics"], 1),
            ("Carnot's work on heat engines was published in:", ["1799", "1824", "1850", "1865"], 1),
            ("Clausius introduced the term 'entropy' in:", ["1824", "1850", "1865", "1905"], 2),
            ("Which scientist's work demonstrated that heat and mechanical work are equivalent?", ["Carnot", "Joule", "Kelvin", "Nernst"], 1),
            ("Which scientist's work on heat engines inspired much of modern thermodynamics despite being based on caloric theory?", ["James Joule", "Sadi Carnot", "Rudolf Clausius", "Lord Kelvin"], 1),
            ("Which scientist proposed a temperature scale that was later modified into the modern Celsius scale after his death?", ["Daniel Fahrenheit", "Anders Celsius", "Lord Kelvin", "Galileo Galilei"], 1),
            ("Which scientist's original heat engine theory remained largely correct even though its underlying assumption—that heat was a conserved fluid—was incorrect?", ["James Joule", "Sadi Carnot", "James Clerk Maxwell", "Walther Nernst"], 1),
            ("Arrange these historical developments from earliest to latest:", ["Kelvin scale → Carnot cycle → Entropy", "Carnot cycle → Joule's mechanical equivalent of heat → Entropy", "Entropy → Carnot cycle → Kelvin scale", "Mechanical equivalent of heat → Carnot cycle → Entropy"], 1),
            ("In the caloric theory, “frigoric” referred to:", ["A type of work", "The absence or lack of caloric (cold)", "Latent heat", "Sensible heat"], 1),
        ],
        "Very Hard": [],
        "Impossible": []
    }
}
# ANATPHY QUESTIONS
QUESTIONS_ANATPHY = {
    "Nervous": {
        "Novice": [
            ("The basic functional unit of the nervous system is the:", ["Nephron", "Neuron", "Osteocyte", "Myofibril"], 1),
            ("Which part of the brain controls balance and coordination?", ["Cerebrum", "Cerebellum", "Medulla oblongata", "Hypothalamus"], 1),
            ("Myelin in the peripheral nervous system is produced by:", ["Oligodendrocytes", "Schwann cells", "Astrocytes", "Microglia"], 1),
            ("The two cerebral hemispheres are connected by the:", ["Corpus callosum", "Thalamus", "Pons", "Medulla"], 0),
            ("Which ion is primarily responsible for the resting membrane potential being negative?", ["Sodium", "Potassium", "Calcium", "Chloride"], 1),
            ("The gap between two neurons is called the:", ["Node of Ranvier", "Synapse", "Axon hillock", "Dendrite"], 1),
            ("Which division of the autonomic nervous system is responsible for 'fight or flight'?", ["Sympathetic", "Parasympathetic", "Somatic", "Enteric"], 0),
            ("Sensory neurons are also called:", ["Afferent neurons", "Efferent neurons", "Interneurons", "Motor neurons"], 0),
            ("The outermost meningeal layer is the:", ["Pia mater", "Arachnoid mater", "Dura mater", "Epidural space"], 2),
            ("Which lobe of the cerebrum is primarily responsible for vision?", ["Frontal", "Parietal", "Temporal", "Occipital"], 3),
        ],
        "Intermediate": [
            ("Which cranial nerve is responsible for the sense of smell?", ["Optic (II)", "Olfactory (I)", "Trigeminal (V)", "Facial (VII)"], 1),
            ("During depolarization of a neuron, the main ion entering the cell is:", ["Potassium", "Sodium", "Calcium", "Chloride"], 1),
            ("Which cranial nerve carries parasympathetic innervation to the heart?", ["Glossopharyngeal (IX)", "Vagus (X)", "Facial (VII)", "Trigeminal (V)"], 1),
            ("Which is NOT a major function of the hypothalamus?", ["Temperature regulation", "Control of the autonomic nervous system", "Production of ADH and oxytocin", "Direct voluntary motor control"], 3),
            ("The sodium-potassium pump moves:", ["3 Na⁺ in and 2 K⁺ out", "3 Na⁺ out and 2 K⁺ in", "2 Na⁺ out and 3 K⁺ in", "Equal numbers of both ions"], 1),
            ("Nodes of Ranvier are important for:", ["Continuous conduction", "Saltatory conduction", "Neurotransmitter release", "Myelin production"], 1),
            ("The primary motor cortex is located in the:", ["Precentral gyrus", "Postcentral gyrus", "Occipital lobe", "Temporal lobe"], 0),
            ("Which glial cell forms the blood-brain barrier?", ["Microglia", "Astrocytes", "Oligodendrocytes", "Ependymal cells"], 1),
            ("The resting membrane potential of a typical neuron is approximately:", ["+30 mV", "0 mV", "−70 mV", "−90 mV"], 2),
            ("Damage to Broca’s area typically results in:", ["Inability to understand language", "Inability to produce speech", "Loss of vision", "Loss of balance"], 1),
        ],
        "Hard": [
            ("During the absolute refractory period:", ["A strong stimulus can still trigger an action potential", "No stimulus can trigger another action potential", "Only potassium channels are open", "The membrane is hyperpolarized"], 1),
            ("At rest the membrane is more permeable to:", ["Sodium than potassium", "Potassium than sodium", "Calcium than either", "Chloride only"], 1),
            ("The blood-brain barrier is formed primarily by:", ["Tight junctions between capillary endothelial cells", "Astrocytes alone", "The meninges", "Absence of capillaries in the brain"], 0),
            ("EPSPs are caused primarily by the opening of:", ["Voltage-gated K⁺ channels", "Ligand-gated Na⁺ or cation channels", "Voltage-gated Ca²⁺ channels", "Cl⁻ channels"], 1),
            ("The reticular activating system is important for:", ["Motor coordination", "Maintaining consciousness and alertness", "Hormone release", "Memory formation"], 1),
            ("Which structure produces cerebrospinal fluid?", ["Arachnoid villi", "Choroid plexus", "Pia mater", "Dura mater"], 1),
            ("Long-term potentiation is most closely associated with:", ["The cerebellum", "The hippocampus", "The medulla", "The thalamus"], 1),
            ("A lesion of the left optic tract produces:", ["Left homonymous hemianopia", "Right homonymous hemianopia", "Bitemporal hemianopia", "Blindness in the left eye only"], 1),
            ("The basal ganglia are primarily involved in:", ["Sensory processing", "Modulation of movement", "Hormone secretion", "Visual processing"], 1),
            ("Which neurotransmitter is most associated with the reward pathway?", ["GABA", "Dopamine", "Serotonin", "Acetylcholine"], 1),
        ],
        "Very Hard": [
            ("The approximate Nernst potential for potassium in a typical neuron is:", ["+60 mV", "0 mV", "−90 mV", "−70 mV"], 2),
            ("The Goldman-Hodgkin-Katz equation takes into account:", ["Only potassium permeability", "Relative permeabilities of Na⁺, K⁺, and Cl⁻", "Only the contribution of the Na⁺/K⁺ pump", "The peak of the action potential"], 1),
            ("Using the Nernst equation at 37 °C, with [K⁺]in = 140 mM and [K⁺]out = 5 mM, the potassium equilibrium potential is closest to:", ["−90 mV", "−70 mV", "−60 mV", "+60 mV"], 0),
            ("Cerebrospinal fluid is produced by the:", ["Arachnoid villi", "Choroid plexus", "Ependymal cells of the central canal only", "Pia mater"], 1),
            ("In multiple sclerosis, the primary pathological process is:", ["Loss of dopamine neurons", "Demyelination of CNS axons", "Accumulation of beta-amyloid", "Death of lower motor neurons"], 1),
            ("The absolute refractory period is caused mainly by:", ["Inactivation of Na⁺ channels", "Opening of K⁺ channels only", "Hyperpolarization", "Depletion of neurotransmitter"], 0),
            ("Which of the following is true of spatial summation?", ["Multiple EPSPs from the same synapse add up over time", "EPSPs from different synapses arrive at the same time and add", "Only IPSPs can summate", "It only occurs in the peripheral nervous system"], 1),
            ("The primary somatosensory cortex is located in the:", ["Precentral gyrus", "Postcentral gyrus", "Occipital lobe", "Insula"], 1),
            ("Which tract carries fine touch and proprioception from the lower body?", ["Lateral spinothalamic", "Anterior spinothalamic", "Fasciculus gracilis", "Fasciculus cuneatus"], 2),
            ("A patient with damage to Wernicke’s area would most likely have difficulty:", ["Producing fluent speech", "Understanding spoken language", "Moving the right arm", "Seeing on the left side"], 1),
        ],
        "Impossible": [
            ("Correct sequence in skeletal muscle excitation-contraction coupling:", ["AP → T-tubule → DHPR conformational change → RyR opens → Ca²⁺ release", "AP → direct Ca²⁺ entry from ECF → troponin binding", "AP → IP₃ production → SR release", "AP → Na⁺ entry → direct myosin activation"], 0),
            ("In the derivation of the Nernst potential, the equilibrium condition is reached when:", ["Chemical and electrical gradients are equal and opposite", "Ion concentrations are equal on both sides", "The membrane is completely impermeable", "The Na⁺/K⁺ pump stops"], 0),
        ]
    },
    "Endocrine": {
        "Novice": [
            ("Which hormone lowers blood glucose levels?", ["Glucagon", "Insulin", "Cortisol", "Epinephrine"], 1),
            ("The hormone TSH is produced by the:", ["Thyroid gland", "Anterior pituitary", "Posterior pituitary", "Hypothalamus only"], 1),
            ("Oxytocin is released from the:", ["Anterior pituitary", "Posterior pituitary", "Thyroid", "Adrenal cortex"], 1),
            ("Thyroid hormones require which element for synthesis?", ["Iron", "Iodine", "Calcium", "Zinc"], 1),
            ("Which gland is often called the 'master gland'?", ["Thyroid", "Adrenal", "Pituitary", "Pineal"], 2),
            ("Melatonin is produced by the:", ["Pituitary", "Pineal gland", "Thyroid", "Adrenal medulla"], 1),
            ("Which hormone is released in response to high blood calcium?", ["PTH", "Calcitonin", "Vitamin D", "Aldosterone"], 1),
            ("The adrenal medulla secretes:", ["Cortisol and aldosterone", "Epinephrine and norepinephrine", "Insulin and glucagon", "T3 and T4"], 1),
            ("Growth hormone is produced by the:", ["Posterior pituitary", "Anterior pituitary", "Hypothalamus", "Thyroid"], 1),
            ("Which hormone stimulates milk production?", ["Oxytocin", "Prolactin", "Estrogen", "Progesterone"], 1),
        ],
        "Intermediate": [
            ("Aldosterone causes the kidneys to:", ["Excrete more sodium", "Reabsorb more sodium", "Reabsorb more potassium", "Decrease blood volume"], 1),
            ("The zona glomerulosa of the adrenal cortex mainly secretes:", ["Cortisol", "Aldosterone", "Androgens", "Epinephrine"], 1),
            ("Testosterone is produced primarily by which cells in the testes?", ["Sertoli cells", "Leydig (interstitial) cells", "Spermatogonia", "Principal cells"], 1),
            ("Atrial natriuretic peptide (ANP) primarily:", ["Increases renin release", "Causes sodium retention", "Promotes natriuresis and lowers blood volume/pressure", "Stimulates ADH release"], 2),
            ("Which hormone increases blood glucose by stimulating gluconeogenesis?", ["Insulin", "Glucagon", "Calcitonin", "ANP"], 1),
            ("The posterior pituitary stores and releases hormones produced by the:", ["Anterior pituitary", "Hypothalamus", "Thyroid", "Adrenal cortex"], 1),
            ("Negative feedback in the thyroid axis involves:", ["High T3/T4 inhibiting TSH and TRH", "Low T3/T4 inhibiting TSH", "TSH stimulating the hypothalamus", "Iodine inhibiting the pituitary"], 0),
            ("Which of the following is a steroid hormone?", ["Insulin", "Glucagon", "Cortisol", "Epinephrine"], 2),
            ("Parathyroid hormone (PTH) acts to:", ["Decrease blood calcium", "Increase blood calcium", "Increase blood glucose", "Decrease blood sodium"], 1),
            ("The renin-angiotensin-aldosterone system is activated by:", ["High blood pressure", "Low blood pressure / low Na⁺", "High blood glucose", "High blood calcium"], 1),
        ],
        "Hard": [
            ("The enzyme responsible for organification and coupling of thyroid hormones is:", ["Thyroid peroxidase", "Deiodinase", "Thyroglobulin synthase", "TSH receptor"], 0),
            ("The final hydroxylation step in the formation of active vitamin D (calcitriol) occurs mainly in the:", ["Liver", "Kidney (proximal tubule)", "Skin", "Intestine"], 1),
            ("Hepcidin regulates iron by:", ["Increasing iron absorption when levels are high", "Decreasing iron absorption and release when iron is high", "Only affecting hemoglobin synthesis", "Stimulating erythropoietin"], 1),
            ("Cortisol has all of the following effects EXCEPT:", ["Increasing blood glucose", "Suppressing the immune system", "Promoting protein synthesis in muscle", "Anti-inflammatory effects"], 2),
            ("Which of the following is true of peptide hormones?", ["They can cross the cell membrane easily", "They typically bind to surface receptors and use second messengers", "They are derived from cholesterol", "They always act slowly"], 1),
            ("Diabetes insipidus is caused by a deficiency of:", ["Insulin", "ADH (vasopressin)", "Aldosterone", "Cortisol"], 1),
            ("The primary stimulus for ADH release is:", ["High blood pressure", "High blood volume", "Increased plasma osmolarity", "Low blood glucose"], 2),
            ("Which cells in the pancreas produce glucagon?", ["Alpha cells", "Beta cells", "Delta cells", "PP cells"], 0),
            ("Graves’ disease is characterized by:", ["Hypothyroidism and low TSH", "Hyperthyroidism and low TSH due to stimulating antibodies", "Hypothyroidism and high TSH", "Normal thyroid function"], 1),
            ("The hypothalamic-pituitary-adrenal axis is primarily regulated by:", ["Positive feedback only", "CRH → ACTH → Cortisol with negative feedback", "Direct neural control only", "Blood glucose levels alone"], 1),
        ],
        "Very Hard": [
            ("In chronic metabolic acidosis the expected respiratory compensation is:", ["Hypoventilation", "Hyperventilation that lowers PCO₂", "Increased renal bicarbonate excretion", "Decreased ammonia production"], 1),
            ("Secondary hyperparathyroidism is most commonly caused by:", ["Parathyroid adenoma", "Chronic kidney disease", "Vitamin D excess", "Thyroid cancer"], 1),
            ("Which of the following hormones uses a nuclear receptor?", ["Insulin", "Glucagon", "Thyroid hormone (T3)", "Epinephrine"], 2),
            ("The somatomedins (IGFs) are produced mainly in the:", ["Pituitary", "Liver", "Muscle", "Adipose tissue"], 1),
            ("A patient with high plasma osmolarity, high ADH, and low urine output most likely has:", ["Diabetes insipidus", "SIADH", "Diabetes mellitus", "Addison’s disease"], 1),
            ("Which of the following is characteristic of Addison’s disease?", ["High cortisol and high aldosterone", "Low cortisol and low aldosterone", "High cortisol only", "High aldosterone only"], 1),
            ("Cushing’s syndrome is characterized by excess:", ["Insulin", "Cortisol", "ADH", "Calcitonin"], 1),
            ("Which hormone is produced by the alpha cells of the pancreas?", ["Insulin", "Glucagon", "Somatostatin", "Pancreatic polypeptide"], 1),
            ("The portal system connecting the hypothalamus to the anterior pituitary carries:", ["Only neural signals", "Releasing and inhibiting hormones", "Only oxytocin", "Only ADH"], 1),
            ("Which of the following is true of steroid hormone action?", ["They bind surface receptors and use cAMP", "They typically enter the cell and bind intracellular receptors that affect transcription", "They cannot cross membranes", "They act only in seconds"], 1),
        ],
        "Impossible": []
    },
    "Special Senses": {
        "Novice": [
            ("Linear acceleration and head position are detected by the:", ["Cochlea", "Semicircular canals", "Utricle and saccule", "Tympanic membrane"], 2),
            ("The structure that equalizes pressure in the middle ear is the:", ["Oval window", "Eustachian tube", "Round window", "Cochlear duct"], 1),
            ("Which cranial nerve carries visual information?", ["Olfactory (I)", "Optic (II)", "Oculomotor (III)", "Trigeminal (V)"], 1),
            ("The sense of smell is detected by receptors in the:", ["Nasal cavity (olfactory epithelium)", "Tongue only", "Pharynx", "Larynx"], 0),
            ("Taste buds are primarily located on the:", ["Soft palate", "Tongue (papillae)", "Epiglottis only", "Esophagus"], 1),
            ("The fluid in the anterior chamber of the eye is:", ["Vitreous humor", "Aqueous humor", "Endolymph", "Perilymph"], 1),
            ("Which part of the eye contains the highest concentration of cones?", ["Optic disc", "Fovea centralis", "Peripheral retina", "Ciliary body"], 1),
            ("The semicircular canals detect:", ["Linear acceleration", "Rotational (angular) acceleration", "Sound frequency", "Taste"], 1),
            ("Sound vibrations are transmitted from the tympanic membrane to the oval window by the:", ["Auditory nerve", "Ossicles (malleus, incus, stapes)", "Cochlea", "Eustachian tube"], 1),
            ("The blind spot in the visual field corresponds to the:", ["Fovea", "Optic disc", "Macula", "Ciliary body"], 1),
        ],
        "Intermediate": [
            ("Which cranial nerve is responsible for the sense of smell?", ["Optic (II)", "Olfactory (I)", "Trigeminal (V)", "Facial (VII)"], 1),
            ("A lesion of the left optic tract produces:", ["Left homonymous hemianopia", "Right homonymous hemianopia", "Bitemporal hemianopia", "Blindness in the left eye only"], 1),
            ("The organ of Corti is located in the:", ["Middle ear", "Cochlear duct (scala media)", "Semicircular canals", "Vestibule"], 1),
            ("Which cells in the retina are responsible for color vision?", ["Rods", "Cones", "Bipolar cells", "Ganglion cells"], 1),
            ("Accommodation (focusing on near objects) involves:", ["Relaxation of the ciliary muscle", "Contraction of the ciliary muscle and rounding of the lens", "Dilation of the pupil only", "Flattening of the lens"], 1),
            ("The malleus, incus, and stapes are collectively called the:", ["Ossicles", "Semicircular canals", "Cochlear hair cells", "Vestibular apparatus"], 0),
            ("Which taste modality is detected by receptors sensitive to H⁺ ions?", ["Sweet", "Salty", "Sour", "Umami"], 2),
            ("The vitreous humor is located in the:", ["Anterior chamber", "Posterior cavity of the eye", "Middle ear", "Cochlea"], 1),
            ("Damage to the vestibular apparatus would most affect:", ["Hearing high frequencies", "Balance and spatial orientation", "Taste", "Smell"], 1),
            ("The optic chiasm is the site where:", ["All optic nerve fibers cross", "Nasal fibers from each eye cross", "Temporal fibers cross", "No fibers cross"], 1),
        ],
        "Hard": [
            ("In the cochlea, high-frequency sounds are detected near the:", ["Apex", "Base (near oval window)", "Middle turn", "Helicotrema"], 1),
            ("Which of the following is true of the dark current in photoreceptors?", ["It is high in the light and low in the dark", "In darkness, cGMP keeps Na⁺ channels open", "Light increases cGMP levels", "Photoreceptors depolarize in response to light"], 1),
            ("The primary auditory cortex is located in the:", ["Occipital lobe", "Temporal lobe (superior temporal gyrus)", "Parietal lobe", "Frontal lobe"], 1),
            ("Motion sickness is primarily caused by conflicting signals between:", ["Vision and vestibular systems", "Taste and smell", "Hearing and vision", "Proprioception and pain"], 0),
            ("Which structure produces aqueous humor?", ["Iris", "Ciliary body", "Lens", "Retina"], 1),
            ("Glaucoma is most commonly associated with:", ["Increased intraocular pressure damaging the optic nerve", "Clouding of the lens", "Detachment of the retina", "Infection of the cornea"], 0),
            ("The otolith organs (utricle and saccule) contain:", ["Cupulae", "Otolithic membrane with calcium carbonate crystals", "Organ of Corti", "Tympanic membrane"], 1),
            ("Which of the following statements about rods is correct?", ["They are concentrated in the fovea", "They are responsible for high-acuity color vision", "They are more sensitive to light than cones and used in dim light", "They respond only to red light"], 2),
            ("Conductive hearing loss can be caused by:", ["Damage to hair cells", "Damage to the auditory nerve", "Otosclerosis or middle ear problems", "Stroke in the temporal lobe"], 2),
            ("The near point of vision increases with age primarily because of:", ["Loss of elasticity of the lens (presbyopia)", "Decreased aqueous humor production", "Retinal degeneration", "Weakening of the extraocular muscles"], 0),
        ],
        "Very Hard": [
            ("In phototransduction, absorption of a photon by rhodopsin leads to:", ["Activation of transducin → activation of PDE → decrease in cGMP → closure of Na⁺ channels", "Increase in cGMP and opening of Na⁺ channels", "Direct opening of Ca²⁺ channels", "Depolarization of the photoreceptor"], 0),
            ("A patient with a pituitary tumor compressing the optic chiasm would most likely have:", ["Homonymous hemianopia", "Bitemporal hemianopia", "Complete blindness in one eye", "Central scotoma only"], 1),
            ("The endolymph has a high concentration of:", ["Sodium", "Potassium", "Calcium", "Chloride only"], 1),
            ("Which of the following is the correct pathway for sound transmission?", ["Tympanic membrane → ossicles → oval window → perilymph → basilar membrane → hair cells", "Tympanic membrane → round window → endolymph → hair cells", "Auricle → cochlea → auditory nerve", "Ossicles → tympanic membrane → cochlea"], 0),
            ("The frequency of a sound is encoded primarily by:", ["The amplitude of the action potentials", "Which region of the basilar membrane vibrates most", "The number of hair cells activated", "The phase of the wave only"], 1),
            ("Which of the following is true of the stapedius and tensor tympani?", ["They amplify sound", "They protect the inner ear from loud sounds by dampening ossicle movement", "They detect linear acceleration", "They produce endolymph"], 1),
            ("Aqueous humor is drained through the:", ["Optic disc", "Canal of Schlemm (trabecular meshwork)", "Vitreous body", "Lacrimal gland"], 1),
            ("Which cells form the optic nerve?", ["Rods and cones", "Bipolar cells", "Ganglion cell axons", "Horizontal cells"], 2),
            ("The macula lutea is important because it:", ["Contains only rods", "Contains the fovea and is responsible for central high-acuity vision", "Is the blind spot", "Produces aqueous humor"], 1),
            ("Nystagmus can be a sign of dysfunction in the:", ["Only the cochlea", "Vestibular system or its central connections", "Only the retina", "Only the olfactory system"], 1),
        ],
        "Impossible": []
    },
    "Respiratory": {
        "Novice": [
            ("Which system is responsible for the exchange of oxygen and carbon dioxide?", ["Circulatory", "Respiratory", "Digestive", "Endocrine"], 1),
            ("The voice box is also known as the:", ["Pharynx", "Larynx", "Trachea", "Epiglottis"], 1),
            ("Which structure prevents food from entering the larynx during swallowing?", ["Uvula", "Epiglottis", "Soft palate", "Glottis"], 1),
            ("The primary muscle of inspiration is the:", ["Internal intercostals", "Diaphragm", "Abdominal muscles", "External oblique"], 1),
            ("Gas exchange in the lungs occurs in the:", ["Bronchi", "Alveoli", "Trachea", "Larynx"], 1),
            ("Which of the following is a function of the nasal cavity?", ["Only olfaction", "Warming, humidifying, and filtering air", "Only producing voice", "Only exchanging gases"], 1),
            ("The trachea is kept open by:", ["Smooth muscle only", "C-shaped rings of hyaline cartilage", "Bone", "Elastic fibers only"], 1),
            ("Which lung has three lobes?", ["Left", "Right", "Both have three", "Neither"], 1),
            ("Surfactant is produced by:", ["Type I alveolar cells", "Type II alveolar cells", "Macrophages", "Goblet cells"], 1),
            ("The amount of air inhaled or exhaled in a normal breath is called:", ["Vital capacity", "Tidal volume", "Residual volume", "Inspiratory reserve"], 1),
        ],
        "Intermediate": [
            ("Surfactant in the lungs functions to:", ["Increase surface tension", "Decrease surface tension in alveoli", "Produce mucus", "Kill pathogens"], 1),
            ("Functional residual capacity equals:", ["Tidal volume + inspiratory reserve", "Expiratory reserve volume + residual volume", "Vital capacity only", "Inspiratory capacity"], 1),
            ("The Bohr effect refers to:", ["Increased O₂ affinity at higher pH", "Decreased O₂ affinity of hemoglobin when pH drops or CO₂ rises", "Increased CO₂ binding only", "A left shift of the dissociation curve"], 1),
            ("Which of the following increases the oxygen-carrying capacity of blood?", ["Decreased hematocrit", "Increased hemoglobin", "Increased temperature only", "Decreased pH only"], 1),
            ("The majority of CO₂ is transported in blood as:", ["Dissolved CO₂", "Carbaminohemoglobin", "Bicarbonate ions", "Carbonic acid only"], 2),
            ("Which chemoreceptors respond primarily to changes in blood PCO₂ and pH?", ["Only peripheral", "Central chemoreceptors (and peripheral)", "Only stretch receptors", "Only irritant receptors"], 1),
            ("Vital capacity is:", ["Tidal volume only", "IRV + TV + ERV", "Residual volume + ERV", "Total lung capacity"], 1),
            ("Which of the following is true of quiet expiration?", ["It is an active process requiring muscle contraction", "It is largely passive due to elastic recoil", "It requires the diaphragm to contract", "It only occurs during exercise"], 1),
            ("The chloride shift involves:", ["Cl⁻ leaving RBCs as HCO₃⁻ enters", "Cl⁻ entering RBCs as HCO₃⁻ leaves", "Na⁺ and Cl⁻ exchanging", "Only K⁺ movement"], 1),
            ("Which of the following shifts the oxyhemoglobin dissociation curve to the right?", ["Decreased temperature", "Increased pH", "Increased 2,3-BPG, increased CO₂, increased temperature", "Decreased 2,3-BPG"], 2),
        ],
        "Hard": [
            ("In severe emphysema one would expect:", ["Increased elastic recoil", "Decreased residual volume", "Air trapping and increased residual volume", "Increased FEV1/FVC ratio"], 2),
            ("The Hering-Breuer reflex is mediated by:", ["Carotid body chemoreceptors", "Pulmonary stretch receptors via the vagus nerve", "Central chemoreceptors", "Joint proprioceptors"], 1),
            ("The pre-Bötzinger complex is best described as:", ["The primary rhythm generator for respiration", "A peripheral chemoreceptor", "Located in the cerebral cortex", "Active only during exercise"], 0),
            ("During exercise the oxygen-hemoglobin dissociation curve shifts right mainly because of:", ["Decreased temperature and 2,3-BPG", "Increased CO₂, H⁺, temperature, and 2,3-BPG", "Increased pH only", "Decreased PCO₂"], 1),
            ("The chloride shift in red blood cells involves:", ["Cl⁻ entering in exchange for HCO₃⁻ leaving", "Cl⁻ leaving in exchange for HCO₃⁻ entering", "Active pumping of chloride out", "No role for band 3 protein"], 0),
            ("A left shift of the oxygen-hemoglobin dissociation curve is caused by:", ["Increased 2,3-BPG", "Decreased pH", "Increased temperature", "Fetal hemoglobin or decreased 2,3-BPG"], 3),
            ("FEV1/FVC ratio is typically reduced in:", ["Restrictive lung disease", "Obstructive lung disease", "Both equally", "Neither"], 1),
            ("Which of the following is true of central chemoreceptors?", ["They respond directly to blood PO₂", "They respond to changes in CSF pH caused by CO₂", "They are located in the carotid bodies", "They only respond to lactic acid"], 1),
            ("Anatomical dead space is approximately:", ["50 mL", "150 mL", "500 mL", "1500 mL"], 1),
            ("Which of the following increases respiratory rate?", ["Decreased arterial PCO₂", "Increased arterial PCO₂", "Increased arterial pH", "Decreased temperature"], 1),
        ],
        "Very Hard": [
            ("The respiratory quotient for pure carbohydrate oxidation is:", ["0.7", "0.8", "1.0", "1.2"], 2),
            ("In healthy individuals during maximal exercise, the main limit to oxygen delivery is usually:", ["Pulmonary diffusion", "Cardiac output", "Mitochondrial capacity", "Hemoglobin concentration"], 1),
            ("Which of the following best describes hypoxic hypoxia?", ["Low arterial PO₂", "Anemia or low hemoglobin", "Circulatory failure", "Cyanide poisoning"], 0),
            ("The alveolar gas equation approximates PAO₂ as:", ["PIO₂ − (PACO₂ / R)", "PIO₂ + PACO₂", "Only PIO₂", "PVO₂ − PACO₂"], 0),
            ("In the zone 1 condition of the lung (West zones):", ["Blood flow is continuous", "Alveolar pressure exceeds arterial pressure and flow may be reduced or absent", "Venous pressure is highest", "It is the base of the lung in upright posture"], 1),
        ],
        "Impossible": []
    },
    "Digestive": {
        "Novice": [
            ("Bile is produced by the:", ["Gallbladder", "Pancreas", "Liver", "Stomach"], 2),
            ("Most nutrient absorption occurs in the:", ["Stomach", "Duodenum", "Jejunum", "Large intestine"], 2),
            ("Pepsin is an enzyme that digests:", ["Carbohydrates", "Lipids", "Proteins", "Nucleic acids"], 2),
            ("Which organ stores and concentrates bile?", ["Liver", "Gallbladder", "Pancreas", "Stomach"], 1),
            ("The primary function of the large intestine is:", ["Protein digestion", "Water absorption and feces formation", "Fat digestion", "Production of bile"], 1),
            ("Amylase begins the digestion of:", ["Proteins", "Starches / carbohydrates", "Lipids", "Nucleic acids"], 1),
            ("Which structure prevents food from entering the trachea?", ["Uvula", "Epiglottis", "Soft palate only", "Glottis"], 1),
            ("Intrinsic factor is required for absorption of:", ["Vitamin C", "Vitamin B12", "Vitamin D", "Iron only"], 1),
            ("The pancreas secretes digestive enzymes into the:", ["Stomach", "Duodenum", "Ileum", "Colon"], 1),
            ("Which of the following is a function of the liver?", ["Only storage of bile", "Production of bile, detoxification, and metabolism of nutrients", "Only production of insulin", "Only mechanical digestion"], 1),
        ],
        "Intermediate": [
            ("The portal triad of the liver contains branches of the:", ["Hepatic artery, hepatic vein, and bile duct", "Hepatic artery, portal vein, and bile duct", "Portal vein, hepatic vein, and lymph vessel", "Hepatic artery, portal vein, and hepatic vein"], 1),
            ("Which enzyme activates trypsinogen to trypsin?", ["Pepsin", "Enterokinase (enteropeptidase)", "Amylase", "Lipase"], 1),
            ("Cholecystokinin (CCK) stimulates:", ["Gastric acid secretion", "Gallbladder contraction and pancreatic enzyme secretion", "Only insulin release", "Only saliva production"], 1),
            ("Secretin primarily stimulates the pancreas to release:", ["Enzymes", "Bicarbonate-rich fluid", "Insulin", "Glucagon"], 1),
            ("The majority of water absorption in the GI tract occurs in the:", ["Stomach", "Small intestine", "Large intestine only", "Esophagus"], 1),
            ("Which of the following is true of bile salts?", ["They digest proteins", "They emulsify fats and aid in their absorption", "They digest carbohydrates", "They are enzymes"], 1),
            ("Parietal cells in the stomach secrete:", ["Pepsinogen", "HCl and intrinsic factor", "Mucus", "Gastrin"], 1),
            ("Chief cells secrete:", ["HCl", "Pepsinogen", "Intrinsic factor", "Mucus"], 1),
            ("The hormone gastrin is produced by:", ["Parietal cells", "G cells in the stomach", "Chief cells", "Pancreatic alpha cells"], 1),
            ("Which of the following is absorbed primarily in the ileum?", ["Glucose", "Amino acids", "Bile salts and vitamin B12", "Alcohol"], 2),
        ],
        "Hard": [
            ("The enterogastric reflex:", ["Increases gastric motility when the duodenum is empty", "Inhibits gastric emptying when the duodenum is distended or acidic", "Only involves the large intestine", "Stimulates acid secretion"], 1),
            ("Which of the following is true of the migrating myoelectric complex (MMC)?", ["It occurs only during feeding", "It is the 'housekeeping' motility that clears residual content during fasting", "It is only in the large intestine", "It is controlled only by the CNS"], 1),
            ("Fat absorption requires:", ["Only amylase", "Bile salts, pancreatic lipase, and formation of micelles", "Only pepsin", "Only HCl"], 1),
            ("Which vitamin is most dependent on intrinsic factor for absorption?", ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin K"], 1),
            ("The cephalic phase of gastric secretion is triggered by:", ["Food in the stomach", "Sight, smell, or thought of food", "Food in the intestine", "Only hormones"], 1),
            ("Which of the following increases surface area for absorption in the small intestine?", ["Only the length", "Plicae circulares, villi, and microvilli", "Only the diameter", "Only mucus"], 1),
            ("Hepatic portal blood comes primarily from the:", ["Hepatic artery", "GI tract, spleen, and pancreas", "Hepatic vein", "Aorta only"], 1),
            ("Which of the following is a function of the enteric nervous system?", ["Only controlling skeletal muscle", "Regulating motility and secretion relatively independently of the CNS", "Only sensing pain", "Only controlling the heart"], 1),
            ("Zollinger-Ellison syndrome involves:", ["Low gastrin", "Gastrin-secreting tumor leading to excess acid", "Low acid production", "Only pancreatic enzyme deficiency"], 1),
            ("Which of the following is true of lacteals?", ["They absorb amino acids", "They absorb chylomicrons / dietary fats into the lymphatic system", "They absorb glucose", "They are part of the large intestine"], 1),
        ],
        "Very Hard": [
            ("The alkaline tide refers to:", ["Increased blood acidity after a meal", "Temporary increase in blood bicarbonate (and pH) after a large meal due to gastric acid secretion", "Only changes in urine pH", "Decreased blood pH"], 1),
            ("Which of the following best describes the role of the sphincter of Oddi?", ["Controls entry of food into the stomach", "Controls flow of bile and pancreatic juice into the duodenum", "Prevents reflux into the esophagus", "Controls defecation"], 1),
            ("In the absence of bile salts, absorption of which of the following would be most impaired?", ["Glucose", "Amino acids", "Long-chain fatty acids and fat-soluble vitamins", "Water"], 2),
        ],
        "Impossible": []
    },
    "Immune & Lymphatic": {
        "Novice": [
            ("White blood cells are also called:", ["Erythrocytes", "Leukocytes", "Thrombocytes", "Platelets"], 1),
            ("Which leukocyte is most involved in allergic reactions?", ["Neutrophil", "Eosinophil", "Monocyte", "Lymphocyte"], 1),
            ("The spleen’s primary functions include:", ["Producing digestive enzymes", "Filtering blood and immune surveillance", "Storing bile", "Producing urine"], 1),
            ("Which of the following is a primary lymphoid organ?", ["Lymph node", "Spleen", "Thymus", "Tonsil"], 2),
            ("Antibodies are produced by:", ["T cells", "B cells / plasma cells", "Neutrophils", "Macrophages"], 1),
            ("Which cells are primarily responsible for cell-mediated immunity?", ["B cells", "T cells", "Neutrophils", "Eosinophils"], 1),
            ("Lymph nodes function to:", ["Only produce red blood cells", "Filter lymph and house immune cells", "Only store fat", "Produce digestive enzymes"], 1),
            ("Which of the following is part of innate immunity?", ["Antibodies from a previous infection", "Skin, mucus, and phagocytes", "Memory B cells", "Only vaccination"], 1),
            ("The thoracic duct drains lymph into the:", ["Right atrium", "Left subclavian vein", "Aorta", "Portal vein"], 1),
            ("Which leukocyte is typically the most abundant in circulating blood?", ["Eosinophil", "Basophil", "Neutrophil", "Monocyte"], 2),
        ],
        "Intermediate": [
            ("Which type of tissue covers body surfaces and lines internal cavities?", ["Connective tissue", "Muscle tissue", "Nervous tissue", "Epithelial tissue"], 3),
            ("MHC class I molecules present antigen to:", ["CD4+ T cells", "CD8+ T cells (cytotoxic T cells)", "B cells only", "Neutrophils"], 1),
            ("MHC class II molecules present antigen to:", ["CD8+ T cells", "CD4+ T cells (helper T cells)", "Only NK cells", "Only macrophages"], 1),
            ("Which of the following is a secondary lymphoid organ?", ["Bone marrow", "Thymus", "Lymph node", "None of these"], 2),
            ("Opsonization refers to:", ["Killing of cells by perforin", "Coating of pathogens to enhance phagocytosis", "Only antibody production", "Fever"], 1),
            ("Which antibody is the most abundant in serum and can cross the placenta?", ["IgA", "IgM", "IgG", "IgE"], 2),
            ("IgE is most associated with:", ["Mucosal immunity", "Allergic reactions and parasitic defense", "Primary response only", "Only complement activation"], 1),
            ("The complement system can:", ["Only produce antibodies", "Enhance inflammation, opsonize, and form the membrane attack complex", "Only activate T cells", "Only produce fever"], 1),
            ("Natural killer (NK) cells are part of:", ["Adaptive immunity only", "Innate immunity and can kill virus-infected or tumor cells", "Only antibody production", "Only phagocytosis"], 1),
            ("Which of the following is true of passive immunity?", ["It requires the person’s own immune system to respond", "It involves transfer of antibodies (e.g., maternal or antiserum) and is temporary", "It always lasts a lifetime", "It only comes from vaccines"], 1),
        ],
        "Hard": [
            ("Clonal selection refers to:", ["Random killing of lymphocytes", "Activation and proliferation of lymphocytes specific for a particular antigen", "Only innate responses", "Only macrophage activation"], 1),
            ("Which of the following is required for full activation of a naïve T cell?", ["Only antigen recognition", "Antigen recognition plus costimulation (e.g., B7-CD28)", "Only cytokines from B cells", "Only antibody binding"], 1),
            ("Affinity maturation occurs in:", ["The thymus", "Germinal centers of secondary lymphoid organs", "Bone marrow only", "The spleen red pulp only"], 1),
            ("Which cytokine is particularly important for activating macrophages?", ["IL-4", "IFN-γ", "IL-10", "TGF-β"], 1),
            ("DiGeorge syndrome is characterized by:", ["Absence of B cells", "Thymic hypoplasia / absence leading to T cell deficiency", "Only neutrophil deficiency", "Only complement deficiency"], 1),
            ("Which of the following is true of immunological memory?", ["It only exists for innate immunity", "Secondary responses are faster and of greater magnitude due to memory cells", "It disappears after one year", "It only applies to T cells"], 1),
            ("The alternative pathway of complement activation is triggered by:", ["Antibody-antigen complexes", "Pathogen surfaces in the absence of antibody", "Only mannose-binding lectin", "Only C1q"], 1),
            ("Which of the following cells can act as professional antigen-presenting cells?", ["Only neutrophils", "Dendritic cells, macrophages, and B cells", "Only erythrocytes", "Only plasma cells"], 1),
            ("Tolerance to self antigens is maintained in part by:", ["Only positive selection", "Negative selection (deletion) of strongly self-reactive clones and regulatory T cells", "Only antibodies", "Only complement"], 1),
            ("Which of the following is characteristic of a secondary (anamnestic) immune response?", ["Long lag period and mostly IgM", "Short lag period, higher titer, and mostly IgG", "No antibodies produced", "Only innate mechanisms"], 1),
        ],
        "Very Hard": [
            ("In the context of MHC restriction, CD8+ T cells recognize antigen presented on:", ["MHC II", "MHC I", "Only self MHC II", "Only foreign MHC"], 1),
            ("Which of the following best describes the role of AIRE in the thymus?", ["It promotes positive selection only", "It allows expression of tissue-specific antigens for negative selection", "It only produces antibodies", "It activates complement"], 1),
            ("Somatic hypermutation of immunoglobulin genes occurs primarily in:", ["Developing B cells in bone marrow", "Activated B cells in germinal centers", "T cells in the thymus", "All lymphocytes equally"], 1),
        ],
        "Impossible": []
    },
    "Excretory": {
        "Novice": [
            ("The functional unit of the kidney is the:", ["Neuron", "Alveolus", "Nephron", "Hepatocyte"], 2),
            ("The renal corpuscle is made of the glomerulus and:", ["Loop of Henle", "Bowman’s capsule", "Collecting duct", "Proximal tubule only"], 1),
            ("Which of the following is a function of the kidneys?", ["Only produce bile", "Filter blood, regulate fluid/electrolyte balance, and produce urine", "Only produce insulin", "Only store urine"], 1),
            ("Urine is carried from the kidney to the bladder by the:", ["Urethra", "Ureter", "Renal artery", "Collecting duct only"], 1),
            ("The glomerulus is a:", ["Tube", "Capillary tuft", "Hormone-producing cell", "Muscle"], 1),
            ("Which hormone increases water reabsorption in the collecting duct?", ["ANP", "ADH (vasopressin)", "Aldosterone only", "Insulin"], 1),
            ("The proximal convoluted tubule reabsorbs the majority of:", ["Only water", "Filtered glucose, amino acids, and a large fraction of Na⁺ and water", "Only urea", "Only creatinine"], 1),
            ("Which of the following is normally completely reabsorbed in the proximal tubule?", ["Urea", "Glucose (under normal conditions)", "Creatinine", "Inulin"], 1),
            ("The loop of Henle is important for:", ["Only filtering blood", "Creating the medullary osmotic gradient", "Only secreting hormones", "Only producing renin"], 1),
            ("Micturition refers to:", ["Filtration", "The act of urination", "Reabsorption", "Secretion of renin"], 1),
        ],
        "Intermediate": [
            ("Aldosterone causes the kidneys to:", ["Excrete more sodium", "Reabsorb more sodium", "Reabsorb more potassium", "Decrease blood volume"], 1),
            ("The juxtaglomerular apparatus helps regulate:", ["Blood glucose", "Blood pressure through renin release", "Body temperature", "Blood pH directly"], 1),
            ("Macula densa cells sense changes in:", ["Blood pressure in the afferent arteriole", "NaCl concentration in the distal tubule", "Oxygen levels", "Hormone levels"], 1),
            ("Which of the following increases glomerular filtration rate (GFR)?", ["Constriction of the afferent arteriole", "Dilation of the afferent arteriole", "Increased plasma oncotic pressure", "Severe volume depletion"], 1),
            ("The countercurrent multiplier is located in the:", ["Proximal convoluted tubule", "Loop of Henle", "Distal convoluted tubule", "Collecting duct"], 1),
            ("Water reabsorption in the proximal tubule is driven mainly by:", ["Active transport of water", "The osmotic gradient created by solute reabsorption", "Hydrostatic pressure", "ADH"], 1),
            ("Which of the following is true of the descending limb of the loop of Henle?", ["It actively transports NaCl", "It is highly permeable to water", "It is impermeable to water", "It secretes hydrogen ions primarily"], 1),
            ("The ascending limb of the loop of Henle:", ["Is highly permeable to water", "Actively transports NaCl and is impermeable to water", "Only reabsorbs glucose", "Is the main site of ADH action"], 1),
            ("Renin is released in response to:", ["High blood pressure", "Low blood pressure, low NaCl at macula densa, or sympathetic stimulation", "High blood glucose", "High ADH"], 1),
            ("Atrial natriuretic peptide (ANP) acts on the kidney to:", ["Increase Na⁺ reabsorption", "Increase Na⁺ excretion and decrease blood volume", "Increase water reabsorption only", "Stimulate renin release"], 1),
        ],
        "Hard": [
            ("Most bicarbonate reabsorption in the kidney occurs in the:", ["Proximal convoluted tubule", "Thick ascending limb", "Distal convoluted tubule", "Collecting duct"], 0),
            ("The key active transport step of the countercurrent multiplier is:", ["Na⁺-K⁺-2Cl⁻ cotransport in the thick ascending limb", "Water reabsorption in the descending limb", "Urea recycling alone", "Active Na⁺ transport in the collecting duct"], 0),
            ("Glucose reabsorption in the proximal tubule occurs primarily via:", ["SGLT cotransporters driven by the sodium gradient", "GLUT transporters only", "Paracellular diffusion", "Primary active transport independent of sodium"], 0),
            ("Hypoproteinemia would be expected to:", ["Decrease GFR", "Increase GFR because of lower glomerular capillary oncotic pressure", "Have no effect on GFR", "Increase afferent arteriolar resistance"], 1),
            ("In the collecting duct, principal cells are primarily involved in:", ["H⁺ secretion", "Na⁺ reabsorption and K⁺ secretion (under aldosterone influence)", "Only water reabsorption independent of ADH", "Bicarbonate synthesis only"], 1),
            ("Intercalated cells in the collecting duct are important for:", ["Only Na⁺ reabsorption", "Acid-base regulation (H⁺ secretion or HCO₃⁻ secretion)", "Only glucose reabsorption", "Only urea handling"], 1),
            ("The clearance of which substance is commonly used to estimate GFR?", ["Glucose", "Inulin or creatinine", "Urea only", "Sodium"], 1),
            ("PAH clearance is used to estimate:", ["GFR", "Renal plasma flow", "Only tubular secretion of H⁺", "Only aldosterone activity"], 1),
            ("Which of the following would increase renin release?", ["High NaCl delivery to the macula densa", "Increased blood pressure in the afferent arteriole", "Decreased blood pressure or decreased NaCl at the macula densa", "High ANP"], 2),
            ("In the presence of ADH, the collecting duct becomes:", ["Impermeable to water", "Permeable to water via aquaporins", "Impermeable to urea", "Unable to reabsorb Na⁺"], 1),
        ],
        "Very Hard": [
            ("The fractional excretion of sodium (FENa) is useful in distinguishing:", ["Only glomerular disease", "Prerenal azotemia from acute tubular necrosis (among other uses)", "Only acid-base disorders", "Only diabetes insipidus"], 1),
            ("In the countercurrent system, urea recycling contributes to:", ["Only cortical osmolality", "The high osmolality of the inner medulla", "Only GFR regulation", "Only bicarbonate reabsorption"], 1),
            ("Which of the following is true of the tubuloglomerular feedback mechanism?", ["Increased NaCl at the macula densa causes afferent arteriole dilation", "Increased NaCl at the macula densa causes afferent arteriole constriction, reducing GFR", "It only involves the efferent arteriole", "It is independent of the juxtaglomerular apparatus"], 1),
        ],
        "Impossible": []
    },
    "Cardiovascular": {
        "Novice": [
            ("The pacemaker of the heart is the:", ["AV node", "SA node", "Bundle of His", "Purkinje fibers"], 1),
            ("Which blood vessels carry blood away from the heart?", ["Veins", "Arteries", "Capillaries", "Venules"], 1),
            ("The primary function of red blood cells is to:", ["Fight infection", "Clot blood", "Transport oxygen", "Produce antibodies"], 2),
            ("The smallest blood vessels are:", ["Arteries", "Veins", "Capillaries", "Arterioles"], 2),
            ("Oxygenated blood returns to the heart from the lungs via the:", ["Pulmonary arteries", "Pulmonary veins", "Aorta", "Superior vena cava"], 1),
            ("Which chamber of the heart receives deoxygenated blood from the body?", ["Left atrium", "Right atrium", "Left ventricle", "Right ventricle"], 1),
            ("The valve between the left atrium and left ventricle is the:", ["Tricuspid", "Pulmonary", "Mitral (bicuspid)", "Aortic"], 2),
            ("Which of the following is true of veins?", ["They always carry oxygenated blood", "They carry blood toward the heart and often have valves", "They have the thickest walls", "They are the site of gas exchange"], 1),
            ("Systole refers to:", ["Relaxation of the heart", "Contraction of the heart", "Only atrial filling", "Only ventricular filling"], 1),
            ("The first heart sound (S1) is caused by:", ["Closure of the semilunar valves", "Closure of the AV valves", "Opening of the AV valves", "Atrial contraction only"], 1),
        ],
        "Intermediate": [
            ("Starling’s law of the heart states that:", ["Heart rate is controlled only by the SA node", "Stroke volume increases with increased end-diastolic volume (within physiological limits)", "Cardiac output is independent of venous return", "Blood pressure depends only on resistance"], 1),
            ("The second heart sound (S2) is caused by:", ["Closure of the atrioventricular valves", "Closure of the semilunar valves", "Opening of the AV valves", "Rapid ventricular filling"], 1),
            ("In fetal circulation, the foramen ovale allows blood to flow from:", ["Right atrium to left atrium", "Right ventricle to left ventricle", "Pulmonary artery to aorta", "Superior to inferior vena cava"], 0),
            ("Cardiac output equals:", ["Stroke volume × heart rate", "Stroke volume / heart rate", "Only stroke volume", "Only heart rate"], 0),
            ("Which of the following increases heart rate?", ["Parasympathetic stimulation", "Sympathetic stimulation", "Only ADH", "Only decreased temperature"], 1),
            ("Mean arterial pressure is approximately:", ["Systolic pressure", "Diastolic + 1/3 (systolic − diastolic)", "Only diastolic pressure", "Systolic − diastolic"], 1),
            ("Which vessels are the primary site of resistance regulation?", ["Elastic arteries", "Arterioles", "Capillaries", "Veins"], 1),
            ("Baroreceptors that help regulate blood pressure are located in the:", ["Only the heart", "Carotid sinus and aortic arch", "Only the kidney", "Only the vena cava"], 1),
            ("Which of the following is true of the Frank-Starling mechanism?", ["It requires sympathetic stimulation", "Increased venous return increases end-diastolic volume and stroke volume", "It only works in failure", "It decreases stroke volume with increased preload"], 1),
            ("The QRS complex on an ECG represents:", ["Atrial depolarization", "Ventricular depolarization", "Ventricular repolarization", "Atrial repolarization"], 1),
        ],
        "Hard": [
            ("The plateau phase of the cardiac action potential is mainly due to:", ["Rapid opening of delayed rectifier K⁺ channels", "Inward Ca²⁺ current balancing outward K⁺ current", "Prolonged opening of Na⁺ channels", "Inactivity of the Na⁺/K⁺ pump"], 1),
            ("Calcium-induced calcium release in cardiac muscle involves:", ["L-type Ca²⁺ channels triggering ryanodine receptors", "Only T-type calcium channels", "Voltage-gated sodium channels releasing Ca²⁺", "No involvement of the sarcoplasmic reticulum"], 0),
            ("The common pathway of the clotting cascade begins with activation of:", ["Factor XII", "Factor VII", "Factor X", "Factor VIII"], 2),
            ("Factor VIII acts as a cofactor for:", ["Activation of Factor X by Factor IXa", "Conversion of prothrombin to thrombin", "Activation of Factor VII", "Cross-linking of fibrin"], 0),
            ("The Frank-Starling mechanism is best explained by:", ["Increased sympathetic drive", "Optimal sarcomere length improving actin-myosin overlap and calcium sensitivity", "It only works in heart failure", "Decreased stroke volume with increased preload"], 1),
            ("Blocking the Na⁺/Ca²⁺ exchanger (NCX) in cardiac myocytes would tend to:", ["Decrease intracellular calcium and weaken contraction", "Increase intracellular calcium and strengthen contraction", "Have no effect on contractility", "Affect only pacemaker cells"], 1),
            ("The tenase complex consists of:", ["Factors VIIIa and IXa (with Ca²⁺ and phospholipid)", "Factors Va and Xa", "Tissue factor and Factor VIIa", "Factors XIa and XIIa"], 0),
            ("Which of the following is true of the ductus arteriosus in the fetus?", ["It connects the pulmonary artery to the aorta, bypassing the lungs", "It connects the two atria", "It is in the liver", "It closes immediately at birth in all cases"], 0),
            ("Pulse pressure is:", ["Diastolic pressure", "Systolic − diastolic pressure", "Mean arterial pressure", "Only systolic pressure"], 1),
            ("Which of the following would increase stroke volume?", ["Decreased preload", "Increased contractility or increased preload (within limits)", "Increased afterload only", "Only decreased heart rate"], 1),
        ],
        "Very Hard": [
            ("In the cardiac cycle, the period of isovolumetric contraction occurs when:", ["AV valves are open and semilunar valves are open", "AV valves are closed and semilunar valves are still closed", "Only the atria are contracting", "Blood is being ejected"], 1),
            ("Which of the following is the correct sequence of the conduction system?", ["AV node → SA node → Bundle of His → Purkinje", "SA node → AV node → Bundle of His → Purkinje fibers", "Purkinje → SA node → AV node", "Bundle of His → SA node → AV node"], 1),
            ("The dicrotic notch on an arterial pressure tracing is associated with:", ["AV valve closure", "Aortic valve closure", "Mitral valve opening", "Atrial contraction"], 1),
            ("Which of the following best describes afterload?", ["The end-diastolic volume", "The pressure the ventricle must overcome to eject blood", "Only the heart rate", "Only the preload"], 1),
            ("In the presence of increased afterload (e.g., hypertension), the ventricle initially:", ["Always increases stroke volume", "May show reduced stroke volume until compensation (e.g., hypertrophy) occurs", "Only decreases heart rate", "Has no change"], 1),
        ],
        "Impossible": []
    },
    "Integumentary": {
        "Novice": [
            ("The largest organ of the human body is the:", ["Liver", "Brain", "Skin", "Small intestine"], 2),
            ("Keratohyalin granules are found in which epidermal layer?", ["Stratum basale", "Stratum spinosum", "Stratum granulosum", "Stratum corneum"], 2),
            ("Which layer of the epidermis is the deepest and contains stem cells?", ["Stratum corneum", "Stratum lucidum", "Stratum basale (germinativum)", "Stratum granulosum"], 2),
            ("Melanin is produced by:", ["Keratinocytes", "Melanocytes", "Langerhans cells", "Merkel cells"], 1),
            ("Which of the following is a function of the skin?", ["Only protection", "Protection, temperature regulation, sensation, vitamin D synthesis", "Only vitamin D synthesis", "Only sensation"], 1),
            ("Sebaceous glands secrete:", ["Sweat", "Sebum (oil)", "Only mucus", "Only hormones"], 1),
            ("Which type of sweat gland is involved in thermoregulation?", ["Apocrine", "Eccrine (merocrine)", "Sebaceous", "Ceruminous only"], 1),
            ("The dermis is primarily composed of:", ["Epithelium", "Connective tissue", "Muscle only", "Nervous tissue only"], 1),
            ("Which layer is present only in thick skin (palms and soles)?", ["Stratum basale", "Stratum spinosum", "Stratum lucidum", "Stratum granulosum"], 2),
            ("Hair follicles are associated with:", ["Only eccrine glands", "Sebaceous glands", "Only apocrine glands in all cases", "No glands"], 1),
        ],
        "Intermediate": [
            ("Langerhans cells in the epidermis function as:", ["Melanin producers", "Antigen-presenting cells", "Touch receptors", "Keratin producers"], 1),
            ("Merkel cells are associated with:", ["Pain sensation", "Light touch / tactile sensation", "Temperature only", "Only pressure"], 1),
            ("The arrector pili muscle is responsible for:", ["Sweat secretion", "Goosebumps (piloerection)", "Only hair growth", "Only sebum secretion"], 1),
            ("Which of the following is true of apocrine sweat glands?", ["They are the primary thermoregulatory glands", "They become active at puberty and are found in axillary and genital regions", "They are found all over the body", "They produce only watery sweat"], 1),
            ("Vitamin D synthesis in the skin requires:", ["Only heat", "UV light acting on a cholesterol derivative", "Only melanin", "Only keratin"], 1),
            ("The hypodermis (subcutaneous layer) is primarily:", ["Dense irregular connective tissue", "Adipose tissue and loose connective tissue", "Stratified squamous epithelium", "Only muscle"], 1),
            ("Which of the following contributes to skin color?", ["Only hemoglobin", "Melanin, carotene, and hemoglobin", "Only carotene", "Only keratin"], 1),
            ("First-degree burns involve:", ["Only the epidermis", "Epidermis and part of the dermis", "Full thickness of skin", "Underlying muscle"], 0),
            ("Which of the following is a function of keratin?", ["Only pigment production", "Providing toughness and water resistance to the epidermis", "Only sensation", "Only temperature regulation"], 1),
            ("The papillary layer of the dermis contains:", ["Only dense irregular connective tissue", "Areolar connective tissue and dermal papillae", "Only adipose tissue", "Only hair follicles"], 1),
        ],
        "Hard": [
            ("Which of the following is true of the stratum corneum?", ["It is actively mitotic", "It consists of dead, keratin-filled cells that are continuously shed", "It contains melanocytes primarily", "It is the deepest layer"], 1),
            ("In wound healing, the process of restoring the epidermis is primarily accomplished by:", ["Only fibroblasts", "Migration and proliferation of keratinocytes", "Only melanocytes", "Only immune cells"], 1),
            ("Which of the following sensory receptors is most sensitive to deep pressure and vibration?", ["Meissner’s corpuscles", "Pacinian (lamellar) corpuscles", "Merkel cells", "Free nerve endings only"], 1),
            ("Meissner’s corpuscles are primarily involved in:", ["Deep pressure", "Light touch and low-frequency vibration", "Pain only", "Temperature only"], 1),
            ("Which of the following is true of eccrine sweat?", ["It is always viscous and odoriferous", "It is mostly water with salts and waste products and helps cool the body", "It is only produced in the axilla", "It contains only sebum"], 1),
            ("The rule of nines is used to:", ["Diagnose skin cancer", "Estimate the percentage of body surface area burned", "Measure skin thickness", "Only classify burns by depth"], 1),
            ("Which of the following is a characteristic of third-degree burns?", ["Only redness and pain", "Full-thickness destruction; may be painless due to nerve damage", "Only blistering", "Only epidermal involvement"], 1),
            ("Langerhans cells are derived from:", ["Keratinocytes", "Bone marrow (immune lineage)", "Melanocytes", "Fibroblasts"], 1),
            ("Which of the following best describes the role of the skin in innate immunity?", ["Only producing antibodies", "Physical barrier, acidic secretions, and presence of immune cells", "Only fever production", "Only complement activation"], 1),
            ("Fingerprints are formed by:", ["Only the epidermis", "Dermal papillae underlying the epidermis", "Only sweat glands", "Only hair follicles"], 1),
        ],
        "Very Hard": [
            ("In the process of keratinization, cells in the stratum granulosum:", ["Begin to fill with keratin and keratohyalin; nuclei and organelles disintegrate", "Are actively dividing", "Produce melanin", "Are completely dead and shed immediately"], 0),
            ("Which of the following is true of the dermal vascular plexus?", ["It has no role in temperature regulation", "It participates in thermoregulation by dilating or constricting", "It only supplies the epidermis", "It is absent in thick skin"], 1),
            ("A key difference between thin and thick skin is:", ["Thin skin has no hair follicles or sebaceous glands", "Thick skin lacks hair follicles and sebaceous glands and has a stratum lucidum", "Thick skin is found on the face", "Thin skin has a stratum lucidum"], 1),
        ],
        "Impossible": []
    },
    "Skeletal": {
        "Novice": [
            ("Bones are connected to other bones by:", ["Tendons", "Ligaments", "Cartilage only", "Fascia"], 1),
            ("The process of bone formation is called:", ["Ossification", "Hematopoiesis", "Calcification only", "Resorption"], 0),
            ("The shoulder joint is an example of a:", ["Hinge joint", "Pivot joint", "Ball-and-socket joint", "Saddle joint"], 2),
            ("Elastic cartilage is found in the:", ["Nose", "Intervertebral discs", "External ear", "Tracheal rings"], 2),
            ("Which type of bone cell breaks down bone matrix?", ["Osteoblast", "Osteocyte", "Osteoclast", "Chondrocyte"], 2),
            ("Which type of bone cell builds bone matrix?", ["Osteoclast", "Osteoblast", "Osteocyte", "Chondrocyte"], 1),
            ("The shaft of a long bone is called the:", ["Epiphysis", "Diaphysis", "Metaphysis", "Periosteum"], 1),
            ("Red bone marrow is primarily responsible for:", ["Fat storage", "Hematopoiesis (blood cell production)", "Only mineral storage", "Only leverage"], 1),
            ("Which of the following is a function of the skeletal system?", ["Only support", "Support, protection, movement, mineral storage, blood cell production", "Only blood cell production", "Only protection"], 1),
            ("The axial skeleton includes:", ["Limbs and girdles", "Skull, vertebral column, and thoracic cage", "Only the skull", "Only the limbs"], 1),
        ],
        "Intermediate": [
            ("Hyaline cartilage is found in:", ["Intervertebral discs", "Articular surfaces of bones, nose, trachea", "External ear", "Pubic symphysis only"], 1),
            ("Fibrocartilage is found in:", ["The external ear", "Intervertebral discs and menisci", "The nose", "Costal cartilages only"], 1),
            ("The epiphyseal plate is responsible for:", ["Appositional growth only", "Lengthwise growth of long bones", "Only thickness growth", "Only remodeling"], 1),
            ("Which of the following is true of compact bone?", ["It contains many large spaces", "It is dense and organized into osteons (Haversian systems)", "It is only found in the epiphysis", "It has no blood supply"], 1),
            ("Spongy (cancellous) bone contains:", ["Osteons primarily", "Trabeculae and often red marrow", "Only yellow marrow", "No bone cells"], 1),
            ("Parathyroid hormone (PTH) acts to:", ["Decrease blood calcium by stimulating osteoblasts", "Increase blood calcium by stimulating osteoclasts (among other actions)", "Only increase bone density", "Only decrease phosphate"], 1),
            ("Calcitonin acts to:", ["Increase blood calcium", "Decrease blood calcium by inhibiting osteoclasts", "Only increase osteoclast activity", "Only affect the kidneys"], 1),
            ("A synarthrosis is a:", ["Freely movable joint", "Immovable joint", "Slightly movable joint", "Only a synovial joint"], 1),
            ("A diarthrosis is a:", ["Immovable joint", "Freely movable (synovial) joint", "Slightly movable joint", "Only a fibrous joint"], 1),
            ("Which of the following is an example of a hinge joint?", ["Shoulder", "Elbow or knee", "Hip", "Atlas-axis"], 1),
        ],
        "Hard": [
            ("In endochondral ossification, bone replaces:", ["Only fibrous membranes", "A hyaline cartilage model", "Only existing bone", "Only dense connective tissue"], 1),
            ("Intramembranous ossification forms:", ["Most long bones", "Flat bones of the skull and clavicle (among others)", "Only the vertebrae", "Only the limbs"], 1),
            ("Wolff’s law states that:", ["Bone density is independent of stress", "Bone remodels in response to mechanical stress", "Only hormones control bone", "Cartilage never remodels"], 1),
            ("Osteoporosis is characterized by:", ["Increased bone density", "Decreased bone mass and increased fracture risk", "Only excess osteoblast activity", "Only excess cartilage"], 1),
            ("Which of the following is true of the periosteum?", ["It lines the medullary cavity", "It is a connective tissue membrane covering the outer surface of bone (except articular surfaces)", "It is only found in spongy bone", "It produces synovial fluid"], 1),
            ("The endosteum lines:", ["The outer surface of bone", "The medullary cavity and trabeculae", "Only joints", "Only the periosteum"], 1),
            ("Which of the following is a pivot joint?", ["Shoulder", "Atlantoaxial joint (atlas-axis)", "Hip", "Knee"], 1),
            ("A saddle joint is found at the:", ["Elbow", "Carpometacarpal joint of the thumb", "Knee", "Shoulder"], 1),
            ("Which of the following is true of synovial joints?", ["They lack a joint cavity", "They have a joint cavity filled with synovial fluid and are freely movable", "They are always immovable", "They are only fibrous"], 1),
            ("The primary curves of the vertebral column are the:", ["Cervical and lumbar", "Thoracic and sacral", "Only cervical", "Only lumbar"], 1),
        ],
        "Very Hard": [
            ("In the process of bone remodeling, which cells are responsible for resorption of bone?", ["Osteoblasts", "Osteoclasts", "Osteocytes only", "Chondrocytes"], 1),
            ("Which of the following is true of the epiphyseal line?", ["It is the site of ongoing lengthwise growth in adults", "It is the remnant of the epiphyseal plate after growth has ceased", "It is only found in flat bones", "It produces red marrow"], 1),
            ("A greenstick fracture is most common in:", ["Elderly adults", "Children (because bones are more flexible)", "Only the skull", "Only the femur of athletes"], 1),
            ("Which of the following hormones is most important for closing the epiphyseal plates?", ["PTH", "Estrogen / testosterone (sex hormones)", "Calcitonin only", "Insulin only"], 1),
            ("The hardness of bone is primarily due to:", ["Collagen only", "Hydroxyapatite (calcium phosphate) crystals", "Only water", "Only osteocytes"], 1),
        ],
        "Impossible": []
    },
    "Muscular": {
        "Novice": [
            ("Which type of muscle is voluntary?", ["Cardiac", "Smooth", "Skeletal", "All of the above"], 2),
            ("Bones are connected to muscles by:", ["Ligaments", "Tendons", "Cartilage", "Fascia"], 1),
            ("In the sliding filament theory, calcium binds to which protein?", ["Myosin", "Actin", "Troponin", "Tropomyosin"], 2),
            ("The contractile unit of a muscle fiber is the:", ["Myofibril", "Sarcomere", "Sarcolemma", "Fascicle"], 1),
            ("Which of the following is true of skeletal muscle?", ["It is nonstriated and involuntary", "It is striated and voluntary", "It is striated and involuntary", "It is nonstriated and voluntary"], 1),
            ("Cardiac muscle is:", ["Voluntary and nonstriated", "Involuntary and striated", "Voluntary and striated", "Involuntary and nonstriated"], 1),
            ("Smooth muscle is found in:", ["The heart", "Walls of hollow organs (e.g., gut, blood vessels)", "Attached to bones", "Only the diaphragm"], 1),
            ("The sarcoplasmic reticulum stores:", ["Sodium", "Calcium", "Potassium", "ATP only"], 1),
            ("A motor unit consists of:", ["One muscle fiber and all its motor neurons", "One motor neuron and all the muscle fibers it innervates", "Only the neuromuscular junction", "Only the tendon"], 1),
            ("Which of the following is required for muscle contraction?", ["Only sodium", "ATP and calcium", "Only potassium", "Only oxygen"], 1),
        ],
        "Intermediate": [
            ("Type I muscle fibers are characterized as:", ["Fast-twitch glycolytic", "Slow-twitch oxidative and fatigue-resistant", "Fast oxidative-glycolytic", "Primarily anaerobic"], 1),
            ("In a sarcomere, the H zone contains:", ["Only thin filaments", "Only thick filaments", "Both overlapping filaments", "No filaments"], 1),
            ("The sarcoplasmic reticulum’s main role in skeletal muscle is to:", ["Store and release calcium ions", "Generate ATP", "Synthesize contractile proteins", "Conduct action potentials"], 0),
            ("The neuromuscular junction is the site where:", ["Two muscle fibers join", "A motor neuron communicates with a muscle fiber", "Tendons attach to bone", "Only blood vessels enter"], 1),
            ("Acetylcholine at the neuromuscular junction causes:", ["Hyperpolarization only", "Depolarization of the muscle cell membrane (end-plate potential)", "Only calcium release from SR without depolarization", "Inhibition of contraction"], 1),
            ("The latent period of a muscle twitch is the time:", ["Of peak tension", "Between stimulus and the beginning of tension development", "Of relaxation only", "Of fatigue"], 1),
            ("Wave summation occurs when:", ["Stimuli are so far apart that the muscle fully relaxes", "A second stimulus arrives before the muscle has fully relaxed", "Only one stimulus is given", "The muscle is stretched"], 1),
            ("Tetanus (fused) is:", ["A single twitch", "A sustained contraction with no relaxation between stimuli", "Only relaxation", "Only fatigue"], 1),
            ("Isometric contraction is when:", ["The muscle shortens and moves a load", "The muscle generates tension but does not change length", "The muscle lengthens", "Only the load moves"], 1),
            ("Isotonic contraction is when:", ["Tension changes but length stays constant", "The muscle changes length while tension stays relatively constant", "Only isometric", "Only passive stretch"], 1),
        ],
        "Hard": [
            ("The length-tension relationship in skeletal muscle is largely due to:", ["Optimal overlap of actin and myosin filaments", "Availability of ATP only", "Frequency of stimulation only", "Elasticity of titin alone"], 0),
            ("A key feature of smooth muscle is:", ["It always requires an action potential to contract", "It can maintain contraction with low ATP use (latch state)", "It uses troponin as its main regulatory protein", "It has an extensive T-tubule system"], 1),
            ("According to the size principle of motor unit recruitment:", ["Large motor units are recruited first", "Small, fatigue-resistant motor units are recruited first", "Recruitment is random", "Fast-twitch fibers are always first"], 1),
            ("Correct sequence in skeletal muscle excitation-contraction coupling:", ["AP → T-tubule → DHPR conformational change → RyR opens → Ca²⁺ release", "AP → direct Ca²⁺ entry from ECF → troponin binding", "AP → IP₃ production → SR release", "AP → Na⁺ entry → direct myosin activation"], 0),
            ("In smooth muscle, calcium binds primarily to:", ["Troponin", "Calmodulin", "Tropomyosin only", "Myosin directly without any intermediary"], 1),
            ("Which of the following is true of fast glycolytic (Type IIx) fibers?", ["They have many mitochondria and high myoglobin", "They rely on anaerobic glycolysis, fatigue quickly, and generate high force", "They are the most fatigue-resistant", "They are only found in the heart"], 1),
            ("The end-plate potential is:", ["An action potential in the muscle", "A local depolarization at the neuromuscular junction caused by ACh", "Only hyperpolarization", "Generated in the T-tubule"], 1),
            ("Which of the following terminates the action of acetylcholine at the neuromuscular junction?", ["Reuptake only", "Acetylcholinesterase", "Only diffusion", "Only calcium"], 1),
            ("In the sliding filament mechanism, the power stroke occurs when:", ["ATP binds to myosin", "Myosin head pulls actin after Pi release (and ADP release continues the cycle)", "Calcium binds to tropomyosin", "Only when ATP is hydrolyzed without attachment"], 1),
            ("Rigor mortis occurs because:", ["Calcium is pumped back into the SR", "ATP is depleted so myosin cannot detach from actin", "Only sodium channels close", "Only potassium is high"], 1),
        ],
        "Very Hard": [
            ("In cardiac muscle, the long refractory period is important because it:", ["Allows summation and tetanus", "Prevents tetanus and allows time for filling", "Only increases force", "Only decreases heart rate"], 1),
            ("Which of the following is true of multiunit smooth muscle?", ["It contracts as a single unit via gap junctions", "It is more similar to skeletal muscle in that fibers are separately innervated", "It is only found in the gut", "It never requires calcium"], 1),
            ("Single-unit (visceral) smooth muscle is characterized by:", ["Independent innervation of each fiber", "Gap junctions allowing coordinated contraction of many cells", "Only voluntary control", "Presence of T-tubules"], 1),
            ("The role of titin in muscle is primarily:", ["To bind calcium", "To provide elasticity and stabilize myosin", "To hydrolyze ATP", "To form cross-bridges"], 1),
            ("Which of the following best describes the relationship between load and velocity of shortening in muscle?", ["Velocity increases as load increases", "Velocity decreases as load increases (inverse relationship)", "Velocity is independent of load", "Only isometric contractions have velocity"], 1),
        ],
        "Impossible": []
    }
}

# WQ QUESTIONS (2026 Freshwater)
QUESTIONS_WATER = {
    "Freshwater Ecology": {
        "Novice": [
            ("The primary source of energy for most freshwater ecosystems is:", ["Chemosynthesis", "Sunlight (photosynthesis)", "Geothermal heat", "Detritus only"], 1),
            ("A watershed is best defined as:", ["A single lake", "The land area that drains into a particular body of water", "Only the river channel", "An underground aquifer"], 1),
            ("Which of the following is an abiotic factor in a stream?", ["Mayfly larvae", "Dissolved oxygen", "Algae", "Fish"], 1),
            ("Lentic ecosystems refer to:", ["Flowing water (rivers, streams)", "Standing water (lakes, ponds)", "Oceans only", "Groundwater"], 1),
            ("Lotic ecosystems refer to:", ["Standing water", "Flowing water", "Wetlands only", "Estuaries"], 1),
            ("The process by which water vapor becomes liquid is called:", ["Evaporation", "Condensation", "Transpiration", "Infiltration"], 1),
            ("Which zone of a lake receives the most sunlight?", ["Profundal", "Littoral", "Benthic", "Profoundal"], 1),
            ("Carrying capacity is the:", ["Maximum population an environment can sustain", "Minimum population needed to survive", "Rate of population growth", "Number of predators"], 0),
            ("A keystone species is one that:", ["Is the most abundant", "Has a disproportionately large effect on its ecosystem", "Is always a top predator", "Is invasive"], 1),
            ("The water cycle is also known as the:", ["Carbon cycle", "Hydrologic cycle", "Nitrogen cycle", "Phosphorus cycle"], 1),
        ],
        "Intermediate": [
            ("Eutrophication is primarily caused by excess:", ["Oxygen", "Nutrients (especially nitrogen and phosphorus)", "Salt", "Sediment only"], 1),
            ("Which of the following is a density-dependent limiting factor?", ["Temperature", "Competition for food", "Natural disaster", "Sunlight"], 1),
            ("In a lake, the thermocline is:", ["The surface layer", "The zone of rapid temperature change with depth", "The bottom sediments", "The shoreline"], 1),
            ("Primary productivity in freshwater systems is often limited by:", ["Carbon dioxide", "Nitrogen or phosphorus", "Oxygen", "Sunlight only"], 1),
            ("Which organism is typically a producer in a freshwater food web?", ["Mayfly", "Algae / phytoplankton", "Trout", "Caddisfly larva"], 1),
            ("The littoral zone of a lake is characterized by:", ["Deep open water", "Shallow water near shore with rooted plants", "The deepest, coldest water", "Only plankton"], 1),
            ("A population that grows without limits shows:", ["Logistic growth", "Exponential growth", "Linear growth", "Declining growth"], 1),
            ("Which of the following is an example of mutualism in a freshwater system?", ["Fish cleaning parasites from another fish", "A parasite living on a fish", "A predator eating prey", "Two species competing for the same food"], 0),
            ("Stratification in lakes is most pronounced in:", ["Winter", "Summer (in temperate lakes)", "Spring turnover", "Always the same"], 1),
            ("The benthic zone refers to:", ["Open water", "The bottom sediments and organisms living there", "The surface film", "Only floating plants"], 1),
        ],
        "Hard": [
            ("The Redfield ratio for healthy phytoplankton is approximately:", ["16 N : 1 P", "1 N : 16 P", "106 C : 16 N : 1 P", "1 C : 1 N : 1 P"], 2),
            ("Oligotrophic lakes are characterized by:", ["High nutrients and high productivity", "Low nutrients, clear water, and low productivity", "High sediment and low oxygen", "Only warm water"], 1),
            ("Cultural eutrophication differs from natural eutrophication in that it is:", ["Slower", "Caused primarily by human activities", "Beneficial to all species", "Limited to oceans"], 1),
            ("In a stratified lake in summer, the hypolimnion typically has:", ["High oxygen and warm temperatures", "Low oxygen and cold temperatures", "High light and high nutrients", "The same conditions as the epilimnion"], 1),
            ("Which of the following would most likely increase the biochemical oxygen demand (BOD) of a stream?", ["Adding cold water", "Input of organic sewage or decaying plant matter", "Increasing water flow", "Adding oxygen"], 1),
            ("The edge effect in freshwater habitats often leads to:", ["Lower biodiversity", "Higher biodiversity at the interface of two habitats", "Only invasive species", "Complete isolation"], 1),
            ("A riffle in a stream is best described as:", ["A deep, slow pool", "A shallow, fast-flowing section with turbulent water", "A stagnant backwater", "The mouth of the river"], 1),
            ("Which of the following is a correct sequence of lake succession?", ["Oligotrophic → mesotrophic → eutrophic", "Eutrophic → oligotrophic → mesotrophic", "Mesotrophic → oligotrophic → eutrophic", "No succession occurs in lakes"], 0),
            ("The compensation depth is the depth at which:", ["Photosynthesis equals respiration", "No light penetrates", "Temperature is constant", "Nutrients are zero"], 0),
            ("In freshwater ecology, allochthonous input refers to:", ["Nutrients produced within the system", "Organic matter or nutrients coming from outside the aquatic system", "Only dissolved oxygen", "Sediment from the bottom"], 1),
        ],
        "Very Hard": [
            ("During fall turnover in a temperate lake, the primary driving force is:", ["Wind mixing after surface cooling reduces density differences", "Increased solar radiation", "Ice formation", "Inflow of warm water"], 0),
            ("The River Continuum Concept predicts that headwater streams are dominated by:", ["Phytoplankton and zooplankton", "Shredders and collectors relying on allochthonous leaf litter", "Large predatory fish only", "Rooted macrophytes"], 1),
            ("A high Shannon diversity index in a macroinvertebrate sample generally indicates:", ["Poor water quality", "Good water quality and habitat diversity", "Only pollution-tolerant species", "No ecological value"], 1),
            ("Which of the following best describes a fen?", ["A nutrient-poor peatland fed mainly by precipitation", "A peatland fed by groundwater, often more nutrient-rich than a bog", "A deep lake", "A fast-flowing river"], 1),
            ("In the context of freshwater food webs, a trophic cascade occurs when:", ["A change in one trophic level affects multiple other levels", "Only producers are affected", "Nutrients are recycled", "Temperature changes"], 0),
        ],
        "Impossible": []
    },
    "Macroinvertebrates": {
        "Novice": [
            ("Which of the following is generally considered pollution-sensitive (Group 1)?", ["Bloodworm (chironomid)", "Mayfly nymph", "Leech", "Aquatic worm"], 1),
            ("Stonefly nymphs are typically indicators of:", ["Poor water quality", "Good water quality (high dissolved oxygen)", "Only warm water", "High nutrient pollution"], 1),
            ("Caddisfly larvae often build:", ["Cases from sticks, leaves, or stones", "Nets only in the water column", "Burrows in mud only", "Nothing"], 0),
            ("Which macroinvertebrate group is most tolerant of low oxygen?", ["Mayflies", "Stoneflies", "Bloodworms / chironomids", "Riffle beetles"], 2),
            ("Gilled snails are generally:", ["Pollution tolerant", "Pollution sensitive", "Only found in oceans", "Predators of fish"], 1),
            ("The presence of many different pollution-sensitive taxa usually indicates:", ["Poor water quality", "Good water quality", "Only temporary pollution", "High salinity"], 1),
            ("Dobsonfly larvae (hellgrammites) are:", ["Pollution tolerant", "Pollution sensitive and predatory", "Herbivores only", "Only found in lakes"], 1),
            ("Water pennies are the larval form of:", ["A beetle", "A mayfly", "A dragonfly", "A true fly"], 0),
            ("Which of the following is a complete metamorphosis insect?", ["Mayfly", "Stonefly", "Caddisfly", "Dragonfly (incomplete)"], 2),
            ("Riffle beetles are typically found in:", ["Slow, stagnant water", "Fast-flowing, well-oxygenated water", "Only deep lakes", "Brackish water"], 1),
        ],
        "Intermediate": [
            ("A biotic index that gives higher scores to pollution-sensitive taxa is used to:", ["Measure only chemical pollution", "Assess overall stream health based on the community present", "Count only fish", "Measure temperature"], 1),
            ("Which functional feeding group scrapes algae from surfaces?", ["Shredders", "Scrapers / grazers", "Collectors", "Predators"], 1),
            ("Shredders in a stream primarily feed on:", ["Fine particulate organic matter", "Coarse particulate organic matter (leaf litter)", "Other animals", "Dissolved nutrients"], 1),
            ("The EPT index refers to the richness of:", ["Ephemeroptera, Plecoptera, Trichoptera", "Earthworms, Planarians, Turbellarians", "Only beetles", "Fish families"], 0),
            ("Dragonfly and damselfly nymphs are:", ["Herbivores", "Predators with extendable labium", "Filter feeders", "Parasites"], 1),
            ("Which of the following is true of blackfly larvae?", ["They are scrapers", "They are filter feeders that attach to substrates in flowing water", "They are only found in lakes", "They are pollution intolerant"], 1),
            ("A high percentage of oligochaetes (aquatic worms) in a sample often indicates:", ["Excellent water quality", "Organic pollution or low oxygen conditions", "High dissolved oxygen", "Only pristine conditions"], 1),
            ("Hellgrammites are the larvae of:", ["Dobsonflies", "Caddisflies", "Mayflies", "Stoneflies"], 0),
            ("Which macroinvertebrate is known for building a case and is often used in biotic indices?", ["Leech", "Caddisfly larva", "Aquatic worm", "Midge larva"], 1),
            ("The presence of planarians (flatworms) in moderate numbers usually indicates:", ["Severe pollution", "Fair to good water quality", "Only toxic conditions", "No ecological information"], 1),
        ],
        "Hard": [
            ("In the Hilsenhoff Biotic Index, a lower score indicates:", ["Worse water quality", "Better water quality", "No relationship to quality", "Only temperature stress"], 1),
            ("Which of the following taxa belongs to the order Plecoptera?", ["Mayflies", "Stoneflies", "Caddisflies", "Dragonflies"], 1),
            ("Net-spinning caddisflies are primarily:", ["Shredders", "Collectors-filterers", "Scrapers", "Predators only"], 1),
            ("A stream sample dominated by chironomids and oligochaetes with very few EPT taxa most likely indicates:", ["Excellent conditions", "Significant organic pollution or habitat degradation", "Only cold water", "High altitude"], 1),
            ("The larval stage of which insect is called a naiad?", ["Beetle", "Mayfly, dragonfly, or damselfly", "True fly", "Caddisfly"], 1),
            ("Which of the following is a correct pairing of pollution tolerance?", ["Mayfly – tolerant; Bloodworm – sensitive", "Stonefly – sensitive; Leech – tolerant", "Caddisfly – highly tolerant; Midge – sensitive", "Riffle beetle – tolerant; Snail – sensitive"], 1),
            ("Functional feeding groups are useful because they:", ["Only identify species", "Reflect the energy pathways and habitat conditions in the stream", "Measure only chemical parameters", "Are independent of water quality"], 1),
            ("In a healthy headwater stream, you would expect a high proportion of:", ["Shredders", "Phytoplankton grazers only", "Large predatory fish", "Only filter feeders"], 0),
            ("The presence of water scorpions or water boatmen in high numbers can indicate:", ["Pristine conditions only", "Possible nutrient enrichment or still-water habitats", "Only high oxygen", "Toxic pollution exclusively"], 1),
            ("Which of the following best describes the life cycle of most mayflies?", ["Complete metamorphosis with a long adult life", "Incomplete metamorphosis; adults live only a short time to reproduce", "No larval stage", "Larvae live in the ocean"], 1),
        ],
        "Very Hard": [
            ("When calculating a simple biotic index, organisms are often weighted by tolerance values. A community with many low-tolerance (sensitive) taxa will produce a:", ["High index value (poor quality)", "Low index value (good quality)", "Value unrelated to quality", "Value only reflecting temperature"], 1),
            ("The ratio of scrapers to shredders can help indicate:", ["Whether the stream is more autochthonous or allochthonous driven", "Only the temperature", "The number of fish species", "Salinity"], 0),
            ("In biomonitoring, a 'reference site' is used to:", ["Compare against potentially impacted sites", "Only measure chemicals", "Grow laboratory cultures", "Ignore natural variation"], 0),
        ],
        "Impossible": []
    },
    "Water Chemistry & Monitoring": {
        "Novice": [
            ("Dissolved oxygen is typically highest in water that is:", ["Warm and stagnant", "Cold and turbulent", "High in organic matter", "Very deep and still"], 1),
            ("pH is a measure of:", ["Temperature", "Hydrogen ion concentration (acidity/basicity)", "Dissolved solids only", "Oxygen content"], 1),
            ("Turbidity refers to:", ["The amount of dissolved oxygen", "The cloudiness or clarity of water caused by suspended particles", "The temperature of the water", "The pH"], 1),
            ("A Secchi disk is used to measure:", ["Temperature", "Water clarity / transparency", "pH", "Dissolved oxygen"], 1),
            ("Which gas is most critical for aquatic animal survival?", ["Nitrogen", "Oxygen", "Carbon dioxide only", "Methane"], 1),
            ("Hardness of water is primarily caused by dissolved:", ["Sodium and potassium", "Calcium and magnesium", "Iron only", "Chloride"], 1),
            ("Alkalinity is a measure of the water’s ability to:", ["Conduct electricity", "Resist changes in pH (buffering capacity)", "Hold oxygen", "Support algae only"], 1),
            ("Which of the following typically decreases dissolved oxygen?", ["Photosynthesis", "Respiration and decomposition of organic matter", "Cold temperatures", "Turbulence"], 1),
            ("Conductivity of water increases with:", ["Decreasing dissolved ions", "Increasing dissolved ions / salinity", "Only temperature decrease", "Only pure water"], 1),
            ("The unit commonly used for dissolved oxygen concentration is:", ["ppt", "mg/L or ppm", "pH units", "NTU only"], 1),
        ],
        "Intermediate": [
            ("Biochemical Oxygen Demand (BOD) measures:", ["The amount of oxygen currently in the water", "The amount of oxygen required by microorganisms to decompose organic matter", "Only chemical oxygen demand", "The oxygen produced by plants"], 1),
            ("A sudden drop in dissolved oxygen after a rainstorm in an agricultural area is often due to:", ["Increased photosynthesis", "Runoff carrying organic matter or nutrients leading to higher respiration", "Colder water", "Increased turbulence only"], 1),
            ("Which of the following is a point source of pollution?", ["Agricultural runoff", "A pipe discharging factory wastewater", "Urban stormwater", "Atmospheric deposition"], 1),
            ("Nonpoint source pollution is best described as:", ["Pollution from a single identifiable source", "Pollution from diffuse sources across the landscape", "Only industrial discharge", "Only sewage treatment plant output"], 1),
            ("The saturation concentration of dissolved oxygen decreases as:", ["Temperature decreases", "Temperature increases", "Pressure increases", "Salinity decreases"], 1),
            ("Which parameter is most directly related to the buffering capacity of water?", ["Dissolved oxygen", "Alkalinity", "Turbidity", "Temperature"], 1),
            ("A high concentration of fecal coliform bacteria indicates:", ["Good water quality for drinking", "Possible contamination by sewage or animal waste", "High dissolved oxygen", "Low nutrients"], 1),
            ("Orthophosphate is a form of phosphorus that is:", ["Readily available for uptake by plants and algae", "Only found in rocks", "Toxic to all aquatic life", "Never measured"], 0),
            ("Which of the following would most increase turbidity?", ["Clear spring water", "Soil erosion and sediment runoff", "High dissolved oxygen", "Cold temperatures"], 1),
            ("The relationship between temperature and dissolved oxygen is:", ["Directly proportional", "Inversely proportional (warmer water holds less oxygen)", "Unrelated", "Only dependent on pH"], 1),
        ],
        "Hard": [
            ("A stream with high BOD, low dissolved oxygen, and high nutrient levels is most likely suffering from:", ["Thermal pollution only", "Organic and nutrient pollution (eutrophication process)", "Only heavy metal contamination", "Low alkalinity"], 1),
            ("The percentage of saturation of dissolved oxygen is useful because it:", ["Ignores temperature effects", "Accounts for the effect of temperature (and salinity) on oxygen solubility", "Only measures absolute mg/L", "Is the same as BOD"], 1),
            ("Which of the following is true of ammonia in water?", ["It is always harmless", "In its unionized form (NH₃) it is toxic to aquatic life, especially at higher pH and temperature", "It only comes from the atmosphere", "It decreases BOD"], 1),
            ("A sudden fish kill after a hot night in a eutrophic pond is often caused by:", ["Too much oxygen", "Depletion of dissolved oxygen due to high respiration and low photosynthesis at night", "Low temperature", "High alkalinity"], 1),
            ("Total Suspended Solids (TSS) differ from turbidity in that TSS:", ["Is a quantitative mass measurement of particles, while turbidity is an optical measure", "Is only measured in oceans", "Is always lower than turbidity", "Measures only dissolved substances"], 0),
            ("Which of the following best describes the purpose of a multiparameter water quality sonde?", ["To measure only one parameter at a time", "To simultaneously measure several parameters (e.g., DO, pH, conductivity, temperature, turbidity)", "Only for laboratory use", "Only for salinity"], 1),
            ("In the context of water quality standards, the 'criteria continuous concentration' is related to:", ["Acute toxicity", "Chronic toxicity (longer-term exposure)", "Only taste", "Only color"], 1),
            ("Which of the following ions contributes most to water hardness?", ["Na⁺", "Ca²⁺ and Mg²⁺", "Cl⁻", "K⁺"], 1),
            ("A positive correlation between conductivity and chloride in a stream near a road often indicates:", ["Natural geology only", "Possible road salt runoff influence", "High dissolved oxygen", "Only algal blooms"], 1),
            ("The process of nitrification in aquatic systems converts:", ["Nitrate to nitrogen gas", "Ammonia → nitrite → nitrate", "Nitrogen gas to ammonia", "Organic nitrogen directly to N₂"], 1),
        ],
        "Very Hard": [
            ("In calculating the oxygen saturation deficit, the most important environmental factors to correct for are:", ["Only pH", "Temperature and barometric pressure (and salinity if applicable)", "Only turbidity", "Only time of day"], 1),
            ("A stream that shows diel (daily) fluctuations in dissolved oxygen with peaks in late afternoon and lows just before dawn is most likely:", ["Oligotrophic with low productivity", "Eutrophic or highly productive with significant algal/plant photosynthesis and respiration", "Completely abiotic", "Affected only by groundwater"], 1),
            ("The Redfield ratio is most useful for interpreting:", ["Whether nitrogen or phosphorus is more likely to be limiting primary production", "Only dissolved oxygen levels", "Temperature profiles", "Macroinvertebrate diversity alone"], 0),
        ],
        "Impossible": []
    },
    "Water Treatment": {
        "Novice": [
            ("The main purpose of primary wastewater treatment is to:", ["Remove dissolved nutrients", "Remove large solids and settleable material by physical processes", "Kill all pathogens with chlorine", "Add oxygen"], 1),
            ("Chlorination in drinking water treatment is primarily used to:", ["Remove sediment", "Disinfect / kill pathogens", "Adjust pH", "Remove hardness"], 1),
            ("Coagulation and flocculation in water treatment help to:", ["Kill bacteria", "Clump small particles together so they can settle or be filtered", "Add oxygen", "Remove dissolved salts only"], 1),
            ("Activated sludge is part of:", ["Primary treatment", "Secondary (biological) treatment", "Tertiary treatment only", "Disinfection only"], 1),
            ("Which of the following is a common method of disinfection for drinking water?", ["Sedimentation only", "Chlorination, UV, or ozonation", "Only filtration", "Only coagulation"], 1),
            ("Screening in wastewater treatment removes:", ["Dissolved chemicals", "Large debris (rags, sticks, plastics)", "All pathogens", "Nutrients"], 1),
            ("The purpose of a septic system is to:", ["Treat wastewater from individual homes in areas without sewer systems", "Only store water", "Produce drinking water", "Cool industrial water"], 0),
            ("Fluoridation of drinking water is done primarily to:", ["Kill bacteria", "Prevent tooth decay", "Remove hardness", "Increase pH"], 1),
            ("Sedimentation tanks allow:", ["Particles to settle by gravity", "Bacteria to grow rapidly", "Only chemical reactions", "Water to evaporate"], 0),
            ("Which treatment stage typically removes the most suspended solids?", ["Preliminary", "Primary settling", "Disinfection", "Fluoridation"], 1),
        ],
        "Intermediate": [
            ("Secondary wastewater treatment primarily uses:", ["Physical settling only", "Biological processes (microorganisms) to break down organic matter", "Only chemical precipitation", "Reverse osmosis"], 1),
            ("Tertiary (advanced) treatment is often used to remove:", ["Only large solids", "Nutrients (nitrogen and phosphorus) and remaining contaminants", "Nothing additional", "Only temperature"], 1),
            ("The purpose of aeration in the activated sludge process is to:", ["Cool the water", "Provide oxygen for aerobic microorganisms", "Kill all bacteria", "Remove solids by flotation only"], 1),
            ("Which of the following is a common method for removing hardness?", ["Chlorination", "Ion exchange or lime softening", "UV disinfection", "Screening"], 1),
            ("In drinking water treatment, the typical sequence after coagulation/flocculation is:", ["Disinfection then sedimentation", "Sedimentation → filtration → disinfection", "Only filtration", "Aeration only"], 1),
            ("Biosolids from wastewater treatment are:", ["Always hazardous waste", "The settled organic solids that can sometimes be beneficially reused after treatment", "Only used for drinking water", "Pure chemicals"], 1),
            ("Which process is most effective at removing dissolved salts?", ["Conventional sedimentation", "Reverse osmosis or distillation", "Chlorination", "Screening"], 1),
            ("The main goal of wastewater treatment overall is to:", ["Make water drinkable immediately", "Reduce pollutants so the effluent can be safely discharged or reused", "Only remove temperature", "Increase nutrient levels"], 1),
            ("UV disinfection works by:", ["Adding chemicals", "Damaging the DNA of microorganisms", "Settling particles", "Changing pH"], 1),
            ("Which of the following is typically part of preliminary treatment?", ["Activated sludge", "Bar screens and grit removal", "Chlorination", "Nutrient removal"], 1),
        ],
        "Hard": [
            ("In the activated sludge process, the mixed liquor is:", ["Only clean water", "The combination of wastewater and activated microorganisms", "Only settled solids", "Chemical coagulants"], 1),
            ("Nitrification in wastewater treatment converts ammonia to:", ["Nitrogen gas directly", "Nitrite then nitrate", "Organic nitrogen", "Phosphate"], 1),
            ("Denitrification requires:", ["Aerobic conditions", "Anoxic conditions and a carbon source to convert nitrate to nitrogen gas", "Only high oxygen", "Only chlorine"], 1),
            ("Chemical precipitation of phosphorus often uses:", ["Chlorine", "Iron or aluminum salts", "Only UV", "Sodium chloride"], 1),
            ("A major advantage of membrane bioreactors (MBRs) is:", ["They require no energy", "They can produce high-quality effluent with a small footprint", "They eliminate the need for any disinfection"], 1),
            ("The purpose of a grit chamber is to:", ["Grow bacteria", "Remove heavy inorganic particles (sand, gravel) by settling", "Disinfect the water", "Remove dissolved nutrients"], 1),
            ("Which of the following is true of combined sewer overflows (CSOs)?", ["They only occur in modern separate systems", "They can discharge untreated or partially treated sewage during heavy rain", "They improve water quality", "They are only used for drinking water"], 1),
            ("In potable water treatment, the CT value refers to:", ["Concentration × time for disinfection effectiveness", "Only temperature", "Conductivity × turbidity", "Only chemical dose"], 0),
            ("Which process is most commonly used for desalination of seawater?", ["Conventional activated sludge", "Reverse osmosis", "Only chlorination", "Screening"], 1),
            ("The main difference between primary and secondary treatment is:", ["Primary is biological; secondary is physical", "Primary is mainly physical; secondary is mainly biological", "There is no difference", "Primary removes nutrients; secondary removes solids"], 1),
        ],
        "Very Hard": [
            ("In a conventional activated sludge system, the sludge age (mean cell residence time) is important because it affects:", ["Only the temperature", "The types of microorganisms that can be maintained and the degree of treatment", "Only the pH", "The color of the water"], 1),
            ("Biological phosphorus removal relies on:", ["Chemical addition only", "Alternating anaerobic and aerobic conditions to select for phosphorus-accumulating organisms", "Only high oxygen at all times", "UV light"], 1),
            ("A common problem in chlorination is the formation of:", ["Only oxygen", "Disinfection byproducts such as trihalomethanes", "Only nitrogen gas", "Beneficial nutrients"], 1),
        ],
        "Impossible": []
    },
    "Pollution & Human Impacts": {
        "Novice": [
            ("Point source pollution comes from:", ["Many diffuse sources", "A single identifiable source (e.g., a pipe)", "Only the atmosphere", "Only agriculture"], 1),
            ("Nonpoint source pollution is often associated with:", ["A factory discharge pipe", "Runoff from farms, streets, and construction sites", "Only sewage treatment plants", "Only power plants"], 1),
            ("Sedimentation in streams is harmful because it can:", ["Increase dissolved oxygen", "Smother habitat, reduce light, and clog gills", "Only benefit fish", "Decrease temperature"], 1),
            ("Thermal pollution typically comes from:", ["Cooling water discharge from power plants or industry", "Only agricultural runoff", "Only sewage", "Rainwater"], 0),
            ("Which of the following is a common result of excess nutrient pollution?", ["Clearer water", "Algal blooms and potential oxygen depletion", "Higher dissolved oxygen permanently", "Fewer insects"], 1),
            ("Plastic pollution in freshwater systems can harm organisms by:", ["Providing food", "Ingestion, entanglement, and habitat alteration", "Increasing oxygen", "Only changing pH"], 1),
            ("Acid rain is primarily caused by:", ["Emissions of sulfur dioxide and nitrogen oxides", "Only carbon dioxide", "Only methane", "Natural lake processes"], 0),
            ("Which human activity is a major source of sediment pollution?", ["Construction and poor land management", "Only fishing", "Only swimming", "Only boating"], 0),
            ("Eutrophication can lead to:", ["Increased biodiversity in all cases", "Hypoxia (low oxygen) and dead zones", "Always better fishing", "Higher pH only"], 1),
            ("Which of the following is an example of a best management practice (BMP) for reducing runoff pollution?", ["Removing all vegetation near streams", "Riparian buffers / buffer strips", "Increasing impervious surfaces", "Dumping waste directly into streams"], 1),
        ],
        "Intermediate": [
            ("A major difference between point and nonpoint source pollution is that nonpoint sources are:", ["Easier to regulate and control", "Harder to identify and control because they are diffuse", "Only from factories", "Always more toxic"], 1),
            ("Hypoxia in aquatic systems is often linked to:", ["High dissolved oxygen", "Decomposition of algal blooms following nutrient enrichment", "Only cold water", "High pH"], 1),
            ("Which of the following is a common heavy metal pollutant of concern in water?", ["Sodium", "Mercury or lead", "Calcium", "Potassium"], 1),
            ("Impervious surfaces (roads, parking lots) increase pollution by:", ["Allowing more infiltration", "Increasing the volume and speed of runoff that carries pollutants", "Decreasing runoff", "Only cooling the water"], 1),
            ("Which of the following is true of pharmaceutical pollution in water?", ["It is not a concern", "Trace amounts of drugs can affect aquatic organisms even at low concentrations", "It only comes from factories", "It is completely removed by all treatment plants"], 1),
            ("Channelization of streams typically leads to:", ["Increased habitat diversity", "Reduced habitat complexity and higher flow velocity", "More wetlands", "Better water quality automatically"], 1),
            ("Which of the following is an example of remediation of a polluted site?", ["Ignoring the problem", "Constructed wetlands or phytoremediation", "Increasing the pollution", "Removing all vegetation"], 1),
            ("The Clean Water Act in the United States primarily regulates:", ["Only air pollution", "Discharges of pollutants into waters of the United States", "Only drinking water in homes", "Only ocean pollution"], 1),
            ("Which of the following is a common indicator of sewage contamination?", ["High dissolved oxygen", "Elevated fecal coliform or E. coli levels", "Low turbidity", "High pH only"], 1),
            ("Agricultural best management practices to reduce nutrient runoff include:", ["Applying fertilizer right before heavy rain", "Cover crops, buffer strips, and precise fertilizer application", "Removing all streamside vegetation", "Increasing tillage on slopes"], 1),
        ],
        "Hard": [
            ("The concept of 'total maximum daily load' (TMDL) is used to:", ["Set the maximum amount of a pollutant that a water body can receive and still meet standards", "Only measure temperature", "Count fish", "Only regulate air emissions"], 0),
            ("Bioaccumulation differs from biomagnification in that bioaccumulation is:", ["The increase in concentration up the food chain", "The buildup of a substance in an individual organism over time", "Only related to temperature", "Only for nutrients"], 1),
            ("Which of the following is most likely to biomagnify?", ["Nitrate", "Mercury or PCBs", "Phosphate", "Dissolved oxygen"], 1),
            ("A stream restoration project that re-meanders a channelized stream is primarily aiming to:", ["Increase flow speed", "Restore habitat complexity, reduce erosion, and improve ecological function", "Make the stream straighter", "Only increase temperature"], 1),
            ("Which of the following is a common effect of acid mine drainage?", ["Increased pH and high oxygen", "Low pH, high metals, and stressed aquatic communities", "Only warmer water", "Increased biodiversity"], 1),
            ("Endocrine-disrupting compounds in water are of concern because they can:", ["Only change temperature", "Interfere with hormone systems of aquatic organisms at very low concentrations", "Increase dissolved oxygen", "Only affect plants"], 1),
            ("Which of the following is true of microplastics in freshwater?", ["They are completely harmless", "They can be ingested by organisms and may carry adsorbed pollutants", "They only exist in oceans", "They increase oxygen levels"], 1),
            ("The 'urban stream syndrome' typically includes:", ["Higher biodiversity and stable flows", "Flashier hydrographs, elevated pollutants, and simplified channels", "Only colder water", "No human impact"], 1),
            ("Which of the following is a passive treatment method for acid mine drainage?", ["Continuous chemical dosing only", "Constructed wetlands or anoxic limestone drains", "Only dilution", "Removing all water"], 1),
            ("A key principle of low-impact development (LID) is to:", ["Maximize impervious surfaces", "Mimic natural hydrology by promoting infiltration and reducing runoff", "Pipe all water directly to streams", "Remove all vegetation"], 1),
        ],
        "Very Hard": [
            ("In the context of the Clean Water Act, a '303(d) list' refers to:", ["A list of waters that are impaired and need TMDLs", "Only pristine waters", "Only oceans", "A list of treatment plants"], 0),
            ("Which of the following best describes the process of natural attenuation?", ["Active human cleanup only", "Reliance on natural processes (dilution, degradation, sorption, etc.) to reduce contaminant concentrations", "Only chemical treatment", "Ignoring the contamination"], 1),
            ("The concept of 'assimilative capacity' of a water body refers to:", ["How much pollution it can receive without exceeding water quality standards", "Only its volume", "Only its temperature", "The number of fish it can hold"], 0),
        ],
        "Impossible": []
    },
    "Invasive / Nuisance Species": {
        "Novice": [
            ("Zebra mussels are problematic because they:", ["Improve water clarity only beneficially", "Filter large amounts of plankton, clog pipes, and outcompete native species", "Only live in oceans", "Are native to North America"], 1),
            ("Which of the following is an invasive aquatic plant?", ["Native water lily", "Eurasian watermilfoil or water hyacinth", "Only algae", "Cattails in all cases"], 1),
            ("Asian carp are a concern in North American waters because they:", ["Are excellent sport fish only", "Can outcompete native fish and disrupt food webs", "Only live in saltwater", "Improve water quality"], 1),
            ("Purple loosestrife is invasive in wetlands because it:", ["Provides excellent habitat for all species", "Forms dense stands that displace native vegetation", "Is easily controlled by all animals", "Only grows in deserts"], 1),
            ("An invasive species is best defined as:", ["Any non-native species", "A non-native species that causes ecological or economic harm", "Only plants", "Only animals that are large"], 1),
            ("Which of the following is a common way invasive aquatic species are introduced?", ["Ballast water of ships, aquarium releases, and recreational boats", "Only natural migration", "Only wind", "Only birds"], 0),
            ("The spiny water flea is problematic because it:", ["Is a native species", "Can clog fishing gear and alter plankton communities", "Only lives in saltwater", "Improves fish growth"], 1),
            ("Water hyacinth is invasive because it:", ["Grows slowly", "Forms dense mats that block light and oxygen exchange", "Is easily eaten by all fish", "Only grows in cold water"], 1),
            ("Which of the following is true of many invasive species?", ["They always have many natural predators in the new environment", "They often lack natural predators and can reproduce rapidly", "They never affect native species", "They only live for one year"], 1),
            ("A common method to prevent the spread of aquatic invasives is:", ["Moving boats between water bodies without cleaning", "Cleaning, draining, and drying boats and equipment", "Releasing aquarium pets into lakes", "Using live bait from other regions freely"], 1),
        ],
        "Intermediate": [
            ("Zebra mussels can dramatically increase water clarity by:", ["Producing oxygen", "Filtering large quantities of phytoplankton", "Eating fish", "Increasing nutrients"], 1),
            ("Which of the following is a potential consequence of high zebra mussel densities?", ["Increased native mussel populations", "Biofouling of water intake pipes and altered food webs", "Only benefits to all species", "Decreased water clarity"], 1),
            ("Asian carp (e.g., silver carp) are known for:", ["Jumping out of the water when startled, creating hazards for boaters", "Only living in the ocean", "Improving native fisheries", "Being easy to eradicate completely"], 0),
            ("The best long-term strategy for managing invasive species is usually:", ["Complete eradication after they are widespread", "Prevention of introduction and early detection/rapid response", "Ignoring them", "Only chemical control forever"], 1),
            ("Which of the following is an example of a biological control attempt for an invasive aquatic plant?", ["Introducing a host-specific insect or pathogen", "Using only herbicides everywhere", "Removing all water", "Adding more nutrients"], 0),
            ("Rusty crayfish are invasive in some regions because they:", ["Only eat algae", "Can reduce aquatic plant abundance and outcompete native crayfish", "Improve habitat for fish", "Are native everywhere"], 1),
            ("Which of the following statements about invasive species management is correct?", ["Once established, they are always easy and cheap to remove", "Prevention is far more cost-effective than control after establishment", "They never spread to new areas", "Only plants can be invasive"], 1),
            ("The 'invasional meltdown' hypothesis suggests that:", ["Invasive species always decline over time", "The presence of one invasive species can facilitate the invasion of others", "Native species always win", "Only one invasive can exist in a system"], 1),
            ("Which of the following is a common vector for the spread of invasive aquatic plants?", ["Fragments stuck to boats, trailers, and fishing gear", "Only natural seed dispersal by wind", "Only fish", "Only groundwater"], 0),
            ("In the Great Lakes, the sea lamprey is controlled primarily by:", ["Complete removal of all water", "Larvicides (TFM) and barriers", "Only fishing", "Adding more nutrients"], 1),
        ],
        "Hard": [
            ("A major ecological impact of zebra mussels in the Great Lakes has been:", ["Increased populations of native unionid mussels", "Decline of native mussels due to competition and fouling, and shifts in energy flow", "No measurable impact", "Only benefits to fish"], 1),
            ("Which of the following best describes the reproductive strategy that helps many aquatic invasives succeed?", ["Slow reproduction and high parental care", "High reproductive output, rapid growth, and broad environmental tolerance", "Only sexual reproduction once per decade", "Dependence on a single host"], 1),
            ("The use of environmental DNA (eDNA) in invasive species management is valuable because it can:", ["Only identify large fish visually", "Detect the presence of a species from water samples even when individuals are rare", "Only measure chemicals", "Replace all other monitoring"], 1),
            ("Which of the following is a potential risk of biological control?", ["It always works perfectly", "The control agent may attack non-target native species", "It is always more expensive than chemicals", "It only works on plants"], 1),
            ("In the context of aquatic invasive species, 'ballast water exchange' is intended to:", ["Increase the number of invasives", "Reduce the transfer of organisms between different ports/ecosystems", "Only clean the ship", "Add nutrients"], 1),
            ("Which of the following statements about the economic impact of aquatic invasive species is most accurate?", ["They have no economic cost", "They can cause significant costs through infrastructure damage, fishery losses, and control efforts", "They only benefit the economy", "Costs are limited to one year"], 1),
            ("A 'dead zone' related to invasive species could theoretically form if:", ["An invasive filter feeder removes so much plankton that the food web collapses in some areas", "Only native species are present", "Oxygen levels rise", "Nutrients decrease permanently"], 0),
            ("Which of the following is true of many successful aquatic plant invaders?", ["They reproduce only by seed", "They can reproduce vegetatively from fragments, allowing rapid spread", "They require very specific conditions", "They never form dense stands"], 1),
            ("The 'enemy release hypothesis' suggests that invasive species succeed partly because:", ["They face more predators in the new range", "They leave behind natural enemies (predators, parasites, pathogens) from their native range", "They are always larger", "They only invade poor habitats"], 1),
            ("Which management approach is generally considered most effective for widespread aquatic invasive plants?", ["A single method used once", "Integrated approaches combining mechanical, chemical, and biological methods as appropriate", "Only doing nothing", "Only removing water"], 1),
        ],
        "Very Hard": [
            ("In invasion ecology, the 'propagule pressure' concept emphasizes that:", ["Only the traits of the species matter", "The number and frequency of individuals introduced strongly influence establishment success", "Habitat is irrelevant", "Only climate matters"], 1),
            ("Which of the following best explains why some lakes are more susceptible to zebra mussel invasion than others?", ["Only the presence of fish", "Calcium concentration (needed for shell formation), pH, and connectivity to invaded waters", "Only depth", "Only temperature in winter"], 1),
            ("A quantitative risk assessment for a potential aquatic invasive species would typically evaluate:", ["Only its appearance", "Its likelihood of arrival, establishment, spread, and the magnitude of potential impacts", "Only its scientific name", "Only whether it is edible"], 1),
        ],
        "Impossible": []
    }
}

if disable_thermoquestions:
    QUESTIONS = {
        "Service Disabled": {
            "Novice": [
                ("Service is currently disabled.", ["Okay", "Understood", "Got it", "Alright"], 0),
            ]
        }
    }
    

# ============================================================
# UI CLASSES
# ============================================================
class AnswerButton(Button):
    def __init__(self, label: str, index: int, correct_index: int, options: list):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.index = index
        self.correct_index = correct_index
        self.options = options

    async def callback(self, interaction: discord.Interaction):
        view: QuestionView = self.view
        if view.answered:
            await interaction.response.send_message("This question has already been answered.", ephemeral=True)
            return
        view.answered = True
        selected = chr(65 + self.index)
        correct = chr(65 + self.correct_index)

        for item in view.children:
            item.disabled = True
            if isinstance(item, AnswerButton):
                if item.index == self.correct_index:
                    item.style = discord.ButtonStyle.success
                elif item.index == self.index:
                    item.style = discord.ButtonStyle.danger

        if self.index == self.correct_index:
            msg = f"✅ **Correct!**\nYou selected **{selected}) {self.options[self.index]}**"
        else:
            msg = (f"❌ **Wrong.**\n"
                   f"You selected **{selected}) {self.options[self.index]}**\n"
                   f"Correct answer: **{correct}) {self.options[self.correct_index]}**")
        await interaction.response.send_message(msg, ephemeral=True)

        embed = interaction.message.embeds[0]
        embed.set_footer(text=f"Answered by {interaction.user.display_name}")
        await interaction.message.edit(view=view)


class QuestionView(View):
    def __init__(self, correct_index: int, options: list, owner_id: int):
        super().__init__(timeout=120)
        self.correct_index = correct_index
        self.options = options
        self.owner_id = owner_id
        self.answered = False
        for i, letter in enumerate(["A", "B", "C", "D"]):
            self.add_item(AnswerButton(letter, i, correct_index, options))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Only the person who requested this question can answer it.", ephemeral=True
            )
            return False
        return True


class DifficultySelect(Select):
    def __init__(self, owner_id: int, category: str, questions_dict: dict, color: int, title_prefix: str):
        self.owner_id = owner_id
        self.category = category
        self.questions_dict = questions_dict
        self.color = color
        self.title_prefix = title_prefix

        available = []
        diffs = ["Novice", "Intermediate", "Hard", "Very Hard", "Impossible"]
        for diff in diffs:
            has_questions = False
            if category == "Any":
                for cat in questions_dict.values():
                    if cat.get(diff):
                        has_questions = True
                        break
            else:
                if questions_dict.get(category, {}).get(diff):
                    has_questions = True
            if has_questions:
                emoji = {"Novice": "🟢", "Intermediate": "🟡", "Hard": "🟠", "Very Hard": "🔴", "Impossible": "🟣"}[diff]
                available.append(discord.SelectOption(label=diff, emoji=emoji))

        if not available:
            available = [discord.SelectOption(label="No questions available", value="none")]

        super().__init__(placeholder="Choose difficulty...", min_values=1, max_values=1, options=available)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Only the person who ran the command can choose the difficulty.", ephemeral=True
            )
            return

        difficulty = self.values[0]
        if difficulty == "none":
            await interaction.response.send_message("No questions available for this selection.", ephemeral=True)
            return

        pool = []
        if self.category == "Any":
            for cat_name, cat_data in self.questions_dict.items():
                if cat_data.get(difficulty):
                    for q in cat_data[difficulty]:
                        pool.append((cat_name, q))
        else:
            for q in self.questions_dict[self.category][difficulty]:
                pool.append((self.category, q))

        if not pool:
            await interaction.response.send_message("No questions found for this combination.", ephemeral=True)
            return

        cat_name, (q_text, options, correct) = random.choice(pool)

        title = f"{self.title_prefix} — {cat_name} ({difficulty})" if self.category == "Any" else f"{self.title_prefix} — {self.category} ({difficulty})"

        embed = discord.Embed(
            title=title,
            description=q_text,
            color=self.color
        )
        option_text = "\n".join(f"**{chr(65+i)})** {opt}" for i, opt in enumerate(options))
        embed.add_field(name="Options", value=option_text, inline=False)
        embed.set_footer(text="(Only the user who requested the question can answer this question)")

        view = QuestionView(correct, options, interaction.user.id)
        await interaction.response.edit_message(embed=embed, view=view)


class CategorySelect(Select):
    def __init__(self, owner_id: int, questions_dict: dict, color: int, title_prefix: str):
        self.owner_id = owner_id
        self.questions_dict = questions_dict
        self.color = color
        self.title_prefix = title_prefix

        options = [discord.SelectOption(label="Any", description="Random from all categories", emoji="🎲")]
        for cat in questions_dict.keys():
            options.append(discord.SelectOption(label=cat))

        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Only the person who ran the command can choose the category.", ephemeral=True
            )
            return

        category = self.values[0]

        embed = discord.Embed(
            title=f"{self.title_prefix}",
            description=f"**Category:** {category}\n\nNow select a difficulty:",
            color=self.color
        )

        view = View(timeout=60)
        view.add_item(DifficultySelect(
            self.owner_id,
            category,
            self.questions_dict,
            self.color,
            self.title_prefix
        ))
        await interaction.response.edit_message(embed=embed, view=view)


class CategoryView(View):
    def __init__(self, owner_id: int, questions_dict: dict, color: int, title_prefix: str):
        super().__init__(timeout=60)
        self.owner_id = owner_id
        self.add_item(CategorySelect(owner_id, questions_dict, color, title_prefix))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Only the person who used the command can select a category.", ephemeral=True
            )
            return False
        return True


# ============================================================
# BOT
# ============================================================
class ThermoBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # needed to resolve members for leaderboard names
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Global sync — works on every server the bot is in
        # (can take up to ~1 hour to fully propagate the first time)
        synced = await self.tree.sync()
        print(f"✅ Globally synced {len(synced)} commands:")
        for cmd in synced:
            print(f"   /{cmd.name}")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

client = ThermoBot()


async def global_interaction_check(interaction: discord.Interaction) -> bool:
    """Deny all slash-command service in blacklisted servers (unless user is in override list)."""
    try:
        guild = interaction.guild
        if guild is None:
            return True
        if guild.id not in BLACKLISTED_SERVER_IDS:
            return True
        # Blacklisted server
        if interaction.user.id in override_blacklist_userID:
            return True
        # Deny
        msg = (
            "🚫 **Server Blacklisted.** If you want to use Ryu6, you can download the Discord app "
            "to use it anywhere (besides a blacklisted server) or use it through a non-blacklisted "
            "server such as ZeroQuality or Steroid."
        )
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(msg)
            else:
                await interaction.followup.send(msg)
        except Exception:
            pass
        return False
    except Exception as e:
        print(f"interaction_check error: {e}")
        return True  # fail open so commands still work

# Bind directly (more reliable than decorator)
client.tree.interaction_check = global_interaction_check


@client.tree.command(name="thermo", description="Get a thermodynamics question")
async def thermo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 HeatSO Thermodynamics",
        description="Select a category (or Any):" + blacklist_override_text(interaction),
        color=0xE85D04
    )
    await interaction.response.send_message(
        embed=embed,
        view=CategoryView(interaction.user.id, QUESTIONS, 0xE85D04, "🔥 HeatSO Thermodynamics")
    )


@client.tree.command(name="random", description="Alias for /thermo")
async def random_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 HeatSO Thermodynamics",
        description="Select a category (or Any):" + blacklist_override_text(interaction),
        color=0xE85D04
    )
    await interaction.response.send_message(
        embed=embed,
        view=CategoryView(interaction.user.id, QUESTIONS, 0xE85D04, "🔥 HeatSO Thermodynamics")
    )


@client.tree.command(name="anatphy", description="Get an Anatomy & Physiology question (SciOly style)")
async def anatphy(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🧬 Anatomy & Physiology",
        description="Select a category (or Any):" + blacklist_override_text(interaction),
        color=0x0D9488
    )
    await interaction.response.send_message(
        embed=embed,
        view=CategoryView(interaction.user.id, QUESTIONS_ANATPHY, 0x0D9488, "🧬 Anatomy & Physiology")
    )


@client.tree.command(name="waterquality", description="Get a Water Quality question (SciOly 2026 Freshwater)")
async def waterquality(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💧 Water Quality (Freshwater)",
        description="Select a category (or Any):" + blacklist_override_text(interaction),
        color=0x0284C7
    )
    await interaction.response.send_message(
        embed=embed,
        view=CategoryView(interaction.user.id, QUESTIONS_WATER, 0x0284C7, "💧 Water Quality")
    )


@client.tree.command(name="wq", description="Alias for /waterquality")
async def wq(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💧 Water Quality (Freshwater)",
        description="Select a category (or Any):" + blacklist_override_text(interaction),
        color=0x0284C7
    )
    await interaction.response.send_message(
        embed=embed,
        view=CategoryView(interaction.user.id, QUESTIONS_WATER, 0x0284C7, "💧 Water Quality")
    )


@client.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    if False:
        pass
    else:
        # was gonna be an easter egg lol
        result = "Heads" if random.random() < 0.5 else "Tails"
    
    await interaction.response.send_message(f"🪙 The coin landed on **{result}**!" + blacklist_override_text(interaction))
    
@client.tree.command(name="simvault", description="Simulate Scio.ly Vault Openings (1–10)")
@app_commands.describe(amount="How many cases to open (1-10)")
async def simvault(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 10]):
    results = {
        "Solid Gold": 0,
        "Vault Door": 0,
        "Gazillionaire": 0,
        "Bullion": 0,
        "Nothing": 0
    }

    for _ in range(amount):
        roll = random.random()  # 0.0 to 1.0

        if roll < 0.01:
            results["Solid Gold"] += 1
        elif roll < 0.02:
            results["Vault Door"] += 1
        elif roll < 0.03:
            results["Gazillionaire"] += 1
        elif roll < 0.04:
            results["Bullion"] += 1
        else:
            results["Nothing"] += 1

    # Build the response
    lines = [f"**Opened {amount} Vault {'s' if amount > 1 else ''}:**\n"]

    if results["Solid Gold"]:
        lines.append(f"🟡 **Solid Gold** × {results['Solid Gold']}")
    if results["Vault Door"]:
        lines.append(f"🚪 **Vault Door** × {results['Vault Door']}")
    if results["Gazillionaire"]:
        lines.append(f"💰 **Gazillionaire** × {results['Gazillionaire']}")
    if results["Bullion"]:
        lines.append(f"🪙 **Bullion** × {results['Bullion']}")
    if results["Nothing"]:
        lines.append(f"📦 Nothing × {results['Nothing']}")

    # Extra flavour if they hit smth rare
    rares = results["Solid Gold"] + results["Vault Door"] + results["Gazillionaire"] + results["Bullion"]
    if rares == 0:
        lines.append("\n*Better luck next time...*")
    elif rares >= 2:
        lines.append(f"\n🔥 **{rares} rares in one pull!**")

    embed = discord.Embed(
        title="🏦 Simulated Vault Opening",
        description="\n".join(lines),
        color=0xF59E0B  # gold-ish color
    )
    embed.set_footer(text=f"Requested by {interaction.user.display_name}")
    embed.description = (embed.description or "") + blacklist_override_text(interaction)

    await interaction.response.send_message(embed=embed)


# ============================================================
# LEADERBOARD / POINTS COMMANDS
# ============================================================

@client.tree.command(name="awardpoint", description="Award (or deduct) points — only in the designated server, by admins / thermo mods / circuit mods")
@app_commands.describe(
    leaderboard="Which leaderboard to modify",
    user="The member to give points to",
    pts="Points to add (use negative number to deduct)"
)
@app_commands.choices(leaderboard=[
    app_commands.Choice(name="thermo", value="thermo"),
    app_commands.Choice(name="circuit", value="circuit"),
])
async def awardpoint(
    interaction: discord.Interaction,
    leaderboard: app_commands.Choice[str],
    user: discord.Member,
    pts: int
):
    board = leaderboard.value

    if not can_award(interaction, board):
        await interaction.response.send_message(
            "❌ You do not have permission to award points on this leaderboard.\n"
            "• Point modifications are **only allowed** in the designated server.\n"
            "• Required roles (in that server): **Administrator**, **Thermo Mod**, or **Circuit Mod** (matching the board).",
            ephemeral=True
        )
        return

    data = load_points()
    uid = str(user.id)

    if uid not in data[board]:
        data[board][uid] = 0

    data[board][uid] += pts
    save_points(data)

    new_total = data[board][uid]
    sign = "+" if pts >= 0 else ""
    await interaction.response.send_message(
        f"✅ Awarded **{sign}{pts}** points to {user.mention} on the **{board}** leaderboard.\n"
        f"New total: **{new_total}** pts"
        + blacklist_override_text(interaction)
    )


@client.tree.command(name="leaderboard", description="Show the current top 5 on a leaderboard")
@app_commands.describe(leaderboard="Which leaderboard to display")
@app_commands.choices(leaderboard=[
    app_commands.Choice(name="thermo", value="thermo"),
    app_commands.Choice(name="circuit", value="circuit"),
])
async def leaderboard_cmd(
    interaction: discord.Interaction,
    leaderboard: app_commands.Choice[str]
):
    board = leaderboard.value
    data = load_points()
    scores = data.get(board, {})

    if not scores:
        await interaction.response.send_message(
            f"📭 No points have been recorded on the **{board}** leaderboard yet."
            + blacklist_override_text(interaction)
        )
        return

    # Sort descending and take top 5
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

    embed = discord.Embed(
        title=f"🏆 {board.capitalize()} Leaderboard — Top 5",
        color=0xE85D04 if board == "thermo" else 0x6366F1
    )

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    lines = []
    for i, (uid, pts) in enumerate(sorted_scores):
        member = interaction.guild.get_member(int(uid)) if interaction.guild else None
        name = member.display_name if member else f"User {uid}"
        lines.append(f"{medals[i]} **{name}** — {pts} pts")

    embed.description = "\n".join(lines)
    embed.set_footer(text=f"Requested by {interaction.user.display_name}")
    embed.description = (embed.description or "") + blacklist_override_text(interaction)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="self", description="Show your own points on both leaderboards")
async def self_cmd(interaction: discord.Interaction):
    data = load_points()
    uid = str(interaction.user.id)

    thermo_pts = data["thermo"].get(uid, 0)
    circuit_pts = data["circuit"].get(uid, 0)

    embed = discord.Embed(
        title=f"📊 Your Points — {interaction.user.display_name}",
        color=0x10B981
    )
    embed.add_field(name="🔥 Thermo", value=f"**{thermo_pts}** pts", inline=True)
    embed.add_field(name="⚡ Circuit", value=f"**{circuit_pts}** pts", inline=True)
    embed.set_footer(text="Use /leaderboard to see the top 5")
    embed.description = (embed.description or "") + blacklist_override_text(interaction)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="fullleaderstats", description="Show every person with a nonzero score on all leaderboards")
async def fullleaderstats(interaction: discord.Interaction):
    data = load_points()

    def build_lines(board: str) -> list[str]:
        scores = {uid: pts for uid, pts in data.get(board, {}).items() if pts != 0}
        if not scores:
            return ["*No one has nonzero points yet.*"]
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        lines = []
        for rank, (uid, pts) in enumerate(sorted_scores, start=1):
            member = interaction.guild.get_member(int(uid)) if interaction.guild else None
            name = member.display_name if member else f"User {uid}"
            lines.append(f"**{rank}.** {name} — **{pts}** pts")
        return lines

    thermo_lines = build_lines("thermo")
    circuit_lines = build_lines("circuit")

    embed_thermo = discord.Embed(
        title="🔥 Thermo — Full Leaderboard (nonzero scores)",
        description="\n".join(thermo_lines),
        color=0xE85D04
    )
    embed_thermo.set_footer(text=f"Requested by {interaction.user.display_name}")

    embed_circuit = discord.Embed(
        title="⚡ Circuit — Full Leaderboard (nonzero scores)",
        description="\n".join(circuit_lines),
        color=0x6366F1
    )
    embed_circuit.set_footer(text=f"Requested by {interaction.user.display_name}")

    embed_thermo.description = (embed_thermo.description or "") + blacklist_override_text(interaction)
    await interaction.response.send_message(embeds=[embed_thermo, embed_circuit])

@client.tree.command(name="ryu6help", description="Show all commands and an overview of the bot")
async def ryu6help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📚 Ryu6 Bot — Help & Overview",
        description=(
            "Practice **Science Olympiad** questions and more!\n"
            "Questions support category + difficulty selection (Novice → Impossible).\n"
            "Only the person who requested a question can answer it with the buttons. What the user answered becomes public, and the correct answer gets revealed."
        ),
        color=0x5865F2
    )

    embed.add_field(
        name="🔥 Thermodynamics",
        value=(
            "`/thermo` — Get a thermodynamics question\n"
            "`/random` — Alias for `/thermo`"
        ),
        inline=False
    )

    embed.add_field(
        name="🧬 Anatomy & Physiology",
        value="`/anatphy` — Get an A&P question (SciOly style)",
        inline=False
    )

    embed.add_field(
        name="💧 Water Quality (2026 Freshwater)",
        value=(
            "`/waterquality` — Get a Water Quality question\n"
            "`/wq` — Alias for `/waterquality`\n"
            "*Categories: Freshwater Ecology, Macroinvertebrates, Chemistry & Monitoring, "
            "Water Treatment, Pollution & Human Impacts, Invasive / Nuisance Species*"
        ),
        inline=False
    )

    embed.add_field(
        name="🎲 Fun / Utility",
        value=(
            "`/coinflip` — Flip a coin\n"
            "`/checkprofanity` — Check the profanity usage of a user\n"
            "`/simvault [1-10]` — Simulate scio.ly vault openings (try your luck!)"
        ),
        inline=False
    )

    embed.add_field(
        name="🏆 Points & Leaderboards",
        value=(
            "`/leaderboard` — Top 5 on thermo or circuit board\n"
            "`/self` — Check your own points on both boards\n"
            "`/fullleaderstats` — Full list of everyone with nonzero scores\n"
            "`/awardpoint` — Award or deduct points *(Admins / Thermo Mod / Circuit Mod only, "
            "and only in the designated server)*"
        ),
        inline=False
    )

    embed.add_field(
        name="ℹ️ Notes",
        value=(
            "• Difficulties: 🟢 Novice · 🟡 Intermediate · 🟠 Hard · 🔴 Very Hard · 🟣 Impossible\n"
            "• Point awards are restricted to one specific server and require the proper roles.\n"
            "• Use this command anytime with `/ryu6help`"
        ),
        inline=False
    )

    embed.set_footer(text=f"Requested by {interaction.user.display_name}")
    embed.description = (embed.description or "") + blacklist_override_text(interaction)
    await interaction.response.send_message(embed=embed)
# ============================================================
# PROFANITY SCANNER
# ============================================================
# Normal swear words — shown fully
BAD_WORDS = {
    # Fuck family
    "fuck", "fucks", "fucking", "fucked", "fucker", "fuckers",
    "motherfucker", "motherfuckers", "motherfucking",
    "motherfuckingly",
    "fahh", "fahhh", "fahhhh", "fahhhhh", "fahhhhhh",
    "fuckass","titfuck","thighfuck","titfucker","thighfucker","titfucking","thighfucking",
    "fuckface", "fuckfaces",
    "fuckhead", "fuckheads",
    "fuckwit", "fuckwits",
    "fuckstick",
    "fuckboy", "fuckboys",
    "fuckgirl", "fuckgirls",
    "fuckup", "fuckups",
    "fuckoff",
    "clusterfuck",
    "dumbfuck",
    "fuckhole",
    "fucknut",
    "fucktard",
    "absofuckinglutely",
    "unfuckingbelievable",
    "fubar",
    "stfu", "gtfo", "wtf", "omfg", "sybau", "syfm",
    "mf", "mfer", "mfs",

    # Shit family
    "shit", "shits", "shitty", "shittier", "shittiest",
    "bullshit",
    "shithead", "shitheads",
    "shitface",
    "shitbag", "shitbags",
    "shitshow",
    "shitstorm",
    "shitpost", "shitposting", "shitposter",
    "shitload", "shitloads",
    "shithole", "shitholes",
    "shitstain",
    "shitfaced",
    "apeshit",
    "batshit",
    "horseshit",
    "dogshit",
    "jackshit",
    "dipshit",
    "dumbshit",
    "shite",
    "ts",

    # Bitch family
    "bitch", "bitches",
    "bitching",
    "bitchy",
    "bitchass",
    "bitchface",
    "bitchboy",
    "bitchmade",
    "sonofabitch",
    "sob",

    # Ass family
    "ass", "asses",
    "asshole", "assholes",
    "asshat",
    "asswipe", "asswipes",
    "assclown",
    "assbag",
    "asslicker",
    "asslick",
    "assmunch",
    "assmonkey",
    "assfuck",
    "assfucker","assfucking",
    "assface",
    "asshead",
    "dumbass",
    "smartass",
    "jackass",
    "badass",
    "hardass",
    "arse", "arses",
    "arsehole", "arseholes",
    "lmao","anal",

    # Dick family
    "dick", "dicks",
    "dickhead", "dickheads",
    "dickwad",
    "dickweed",
    "dickface",
    "dickhole",
    "dickbag",
    "dipstick",

    # Cock family
    "cock", "cocks",
    "cockhead",
    "cockface",
    "cocksucker", "cocksuckers",
    "cockbite",
    "cockblock",
    "cockblocked",
    "cockblocking",

    # Pussy / Cunt
    "pussy", "pussies",
    "pussyfuck", "pussyfucker","pussysucker","pussysucking",
    "twat", "twats",
    "twatwaffle",
    "twatface",
    "cunt", "cunts",
    "cuntface",
    "cunty","cuntfucker","cuntfucking","cuntsucker","cuntsucking",

    # Bastard
    "bastard", "bastards",

    # Insults
    "whore", "whores", "whoring",
    "slut", "sluts", "slutty",
    "skank", "skanks",
    "tramp", "tramps",
    "hoe", "hoes",
    "thot","thots",
    
    # Religious
    "damn", "damned",
    "dayum",
    "dammit",
    "goddamn",
    "goddammit",
    "goddamned",
    "hell",
    "hellish",

    # Piss
    "piss", "pissed",
    "pissing",
    "pisser",
    "pisshead",
    "pmo",

    # British
    "prick", "pricks",
    "bollock", "bollocks",
    "bugger", "buggery",
    "git",
    "tosser", "tossers",
    "wanker", "wankers",
    "wank", "wanking",
    "knob", "knobhead", "knobheads",

    # Sexual slang
    "tit", "tits", "titty", "titties",
    "cum", "cums", "cumming",
    "jizz",
    "spunk",
    "cuck", "cucks", "cuckold",
    "goon", "gooner", "gooning",
    "crack", "cracked", "cracking", 
    "clap","clapping","clapped",
    # toys and stuff
    "dildo", "vibrator", "fleshlight","strap-on",

    # Porn family
    "porn",
    "porno",
    "pornography",
    "pornographical",
    "xxx", "nsfw", "hentai", "onlyfans", "pornhub", "hub", "phub",
    "smut",

    # General insults
    "douche", "douches",
    "douchebag", "douchebags",
    "douchecanoe",
    "jerkoff", "jerkoffs",
    "nutjob", "nutjobs",

    # No-space versions
    "engineeringcad", "engicad", "engiecad", "engcad","cornso",
}

# Multi-word phrases (these need special handling)
MULTI_WORD_BAD = {
    "engineering cad",
    "engi cad",
    "engie cad",
    "eng cad",
}

# Actual slurs — these get censored harder / treated more strictly
SLURS = {
    # Racial
    "nigger", "niggers", "nigga", "niggas", "niggah",
    "coon", "coons",
    "spic", "spics", "wetback", "wetbacks", "beaner", "beaners",
    "chink", "chinks", "gook", "gooks",
    "kike", "kikes",
    "towelhead", "towelheads", "raghead", "ragheads",
    "cracker",

    # Sexual orientation / gender
    "fag", "fags", "faggot", "faggots", "faggy",
    "dyke", "dykes",
    "tranny", "trannies", "shemale", "shemales",

    # Disability / mental
    "retard", "retards", "retarded", "tard", "tards",
    "spaz", "spazz", "spastic",
    "mong", "mongoloid",
}

def censor_slur(word: str) -> str:
    """Censor only slurs (keep first + last letter)."""
    w = word.lower()
    if len(w) <= 2:
        return w[0] + "*"
    return w[0] + "*" * (len(w) - 2) + w[-1]


@client.tree.command(name="checkprofanity", description="Scan a user's recent public messages for profanity counts")
@app_commands.describe(user="The user whose messages to scan")
async def checkprofanity(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(thinking=True)

    if not interaction.guild:
        await interaction.followup.send("This command only works in a server." + blacklist_override_text(interaction))
        return

    # Combine everything we want to count
    all_targets = BAD_WORDS | SLURS | MULTI_WORD_BAD
    counts = {word: 0 for word in all_targets}

    messages_scanned = 0
    channels_scanned = 0

    for channel in interaction.guild.text_channels:
        perms = channel.permissions_for(interaction.guild.me)
        if not (perms.read_messages and perms.read_message_history):
            continue

        channels_scanned += 1

        try:
            async for msg in channel.history(limit=800):
                if msg.author.id != user.id or not msg.content:
                    continue

                messages_scanned += 1
                content = msg.content.lower().replace("\n", " ")

                # 1. Single-word check
                for w in content.split():
                    cleaned = w.strip(".,!?;:\"'()[]{}<>")
                    if cleaned in counts:
                        counts[cleaned] += 1

                # 2. Multi-word phrase check
                for phrase in MULTI_WORD_BAD:
                    counts[phrase] += content.count(phrase)

        except (discord.Forbidden, discord.HTTPException):
            continue

    results = [(word, count) for word, count in counts.items() if count > 0]
    results.sort(key=lambda x: x[1], reverse=True)

    if not results:
        await interaction.followup.send(
            f"No matching profanity found for {user.mention} "
            f"in the last ~800 messages of {channels_scanned} public channels "
            f"({messages_scanned} of their messages scanned)."
            + blacklist_override_text(interaction)
        )
        return

    lines = ["**Word** **# of times**"]
    lines.append("─" * 34)

    for word, count in results:
        display = censor_slur(word) if word in SLURS else word
        lines.append(f"{display:<22} {count}")

    table = "```\n" + "\n".join(lines) + "\n```"

    embed = discord.Embed(
        title=f"🤬 Profanity Report — {user.display_name}",
        description=table,
        color=0xDC2626
    )
    embed.set_footer(
        text=f"Scanned {messages_scanned} messages across {channels_scanned} public channels (last ~800 msgs each) • Requested by {interaction.user.display_name}"
    )

    embed.description = (embed.description or "") + blacklist_override_text(interaction)
    await interaction.followup.send(embed=embed)
client.run(os.getenv("DISCORD_TOKEN"))
