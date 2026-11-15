"""Bekannte Blueprints fuer den Gegenstands-Dialog.

Warum eine eigene Liste: `GiveItemToPlayer` braucht den vollstaendigen Blueprint-Pfad, und
der ist je Kategorie unterschiedlich aufgebaut (Weapons/, Items/Consumables/, Resources/,
Items/Armor/<Set>/). Aus einem Namen laesst er sich nicht zuverlaessig raten - deshalb steht
hier pro Eintrag der komplette Pfad, und die Oberflaeche laesst suchen statt tippen.

Alle Eintraege sind auf dem Testserver erprobt oder folgen dem verifizierten Muster der
Kit-Liste. Freie Eingabe bleibt moeglich.
"""

from typing import Iterable

W_A = "/Game/PrimalEarth/CoreBlueprints/Weapons/%s.%s"
C_A = "/Game/PrimalEarth/CoreBlueprints/Items/Consumables/%s.%s"
R_A = "/Game/PrimalEarth/CoreBlueprints/Resources/%s.%s"
I_A = "/Game/PrimalEarth/CoreBlueprints/Items/%s.%s"
M_A = "/Game/PrimalEarth/CoreBlueprints/Weapons/%s.%s"   # Munition liegt unter Weapons/
ARM = "/Game/PrimalEarth/CoreBlueprints/Items/Armor/%s/%s.%s"
SAD = "/Game/PrimalEarth/CoreBlueprints/Items/Armor/Saddles/%s.%s"

# (Name, Bezeichnung DE, Kategorie-Vorlage, Zusatz fuer die Vorlage (z.B. Ruestungsset))
ITEMS: list[tuple[str, str, str, str]] = [
    # Werkzeuge und Waffen
    ("PrimalItem_WeaponMetalHatchet", "Metall-Axt", "W", ""),
    ("PrimalItem_WeaponMetalPick", "Metall-Picke", "W", ""),
    ("PrimalItem_WeaponStoneHatchet", "Stein-Axt", "W", ""),
    ("PrimalItem_WeaponStonePick", "Stein-Picke", "W", ""),
    ("PrimalItem_WeaponSickle", "Sichel", "W", ""),
    ("PrimalItem_WeaponPike", "Pike", "W", ""),
    ("PrimalItem_WeaponSword", "Schwert", "W", ""),
    ("PrimalItem_WeaponCrossbow", "Armbrust", "W", ""),
    ("PrimalItem_WeaponBow", "Bogen", "W", ""),
    ("PrimalItem_WeaponLongneckRifle", "Longneck-Gewehr", "W", ""),
    ("PrimalItem_WeaponOneShotRifle", "Gewehr (Longneck)", "W", ""),
    ("PrimalItem_WeaponShotgun", "Schrotflinte", "W", ""),
    ("PrimalItem_WeaponMachinedShotgun", "Pump-Action-Schrotflinte", "W", ""),
    ("PrimalItem_WeaponMachinedPistol", "Pistole", "W", ""),
    ("PrimalItem_WeaponMachinedSniper", "Scharfschuetzengewehr", "W", ""),
    ("PrimalItem_WeaponRocketLauncher", "Raketenwerfer", "W", ""),
    ("PrimalItem_WeaponC4", "C4", "W", ""),
    ("PrimalItem_WeaponGrenade", "Granate", "W", ""),
    ("PrimalItem_WeaponTorch", "Fackel", "W", ""),
    ("PrimalItem_WeaponSpyglass", "Fernglas", "W", ""),
    # Munition
    ("PrimalItemAmmo_ArrowStone", "Steinpfeile", "M", ""),
    ("PrimalItemAmmo_ArrowFlame", "Feuerpfeile", "M", ""),
    ("PrimalItemAmmo_ArrowTranq", "Tranqpfeile", "M", ""),
    ("PrimalItemAmmo_SimpleBullet", "Pistolenmunition", "M", ""),
    ("PrimalItemAmmo_SimpleRifleBullet", "Einfache Gewehrmunition", "M", ""),
    ("PrimalItemAmmo_SimpleShotgunBullet", "Schrotmunition", "M", ""),
    ("PrimalItemAmmo_AdvancedBullet", "Advanced-Munition", "M", ""),
    ("PrimalItemAmmo_AdvancedRifleBullet", "Advanced-Gewehrmunition", "M", ""),
    ("PrimalItemAmmo_AdvancedSniperBullet", "Scharfschuetzen-Munition", "M", ""),
    ("PrimalItemAmmo_Rocket", "Rakete", "M", ""),
    # Verbrauch
    ("PrimalItemConsumable_Narcotic", "Narkotika", "C", ""),
    ("PrimalItemConsumable_Stimulant", "Stimulans", "C", ""),
    ("PrimalItemConsumable_HealSoup", "Medizin-Brew", "C", ""),
    ("PrimalItemConsumable_StaminaSoup", "Energie-Brew", "C", ""),
    ("PrimalItemConsumable_WaterJarRefill", "Wasserkrug", "C", ""),
    ("PrimalItemConsumable_RawMeat", "Rohes Fleisch", "C", ""),
    ("PrimalItemConsumable_CookedMeat", "Gekochtes Fleisch", "C", ""),
    ("PrimalItemConsumable_RawPrimeMeat", "Rohes Primes Fleisch", "C", ""),
    ("PrimalItemConsumable_CookedPrimeMeat", "Gekochtes Primes Fleisch", "C", ""),
    ("PrimalItemConsumable_Berry_Mejoberry", "Mejobeeren", "C", ""),
    ("PrimalItemConsumable_Berry_Amarberry", "Amarbeeren", "C", ""),
    ("PrimalItemConsumable_Berry_Tintoberry", "Tintobeeren", "C", ""),
    ("PrimalItemConsumable_Mindwipe", "Mindwipe-Tonic", "C", ""),
    # Rohstoffe
    ("PrimalItemResource_Stone", "Stein", "R", ""),
    ("PrimalItemResource_Flint", "Feuerstein", "R", ""),
    ("PrimalItemResource_Wood", "Holz", "R", ""),
    ("PrimalItemResource_Thatch", "Stroh", "R", ""),
    ("PrimalItemResource_Fiber", "Fasern", "R", ""),
    ("PrimalItemResource_Hide", "Leder", "R", ""),
    ("PrimalItemResource_Pelt", "Fell", "R", ""),
    ("PrimalItemResource_Chitin", "Chitin", "R", ""),
    ("PrimalItemResource_Keratin", "Keratin", "R", ""),
    ("PrimalItemResource_Metal", "Metallbarren", "R", ""),
    ("PrimalItemResource_MetalIngot", "Metallbarren (Ingot)", "R", ""),
    ("PrimalItemResource_Obsidian", "Obsidian", "R", ""),
    ("PrimalItemResource_Crystal", "Kristall", "R", ""),
    ("PrimalItemResource_Charcoal", "Holzkohle", "R", ""),
    ("PrimalItemResource_Gunpowder", "Schwarzpulver", "R", ""),
    ("PrimalItemResource_Sparkpowder", "Funkenpulver", "R", ""),
    ("PrimalItemResource_CementingPaste", "Zementpaste", "R", ""),
    ("PrimalItemResource_Polymer_Organic", "Organisches Polymer", "R", ""),
    ("PrimalItemResource_Element", "Element", "R", ""),
    ("PrimalItemResource_Silicon", "Silizium", "R", ""),
    ("PrimalItemResource_SilicaPearls", "Siliziumperlen", "R", ""),
    ("PrimalItemResource_BlackPearl", "Schwarze Perlen", "R", ""),
    ("PrimalItemResource_Oil", "Oel", "R", ""),
    ("PrimalItemResource_CactusSap", "Kaktussaft", "R", ""),
    # Ruestung (Riot-Set, im Kit erprobt)
    ("PrimalItemArmor_RiotHelmet", "Riot-Helm", "A", "Riot"),
    ("PrimalItemArmor_RiotShirt", "Riot-Brust", "A", "Riot"),
    ("PrimalItemArmor_RiotPants", "Riot-Hose", "A", "Riot"),
    ("PrimalItemArmor_RiotBoots", "Riot-Stiefel", "A", "Riot"),
    ("PrimalItemArmor_RiotGloves", "Riot-Handschuhe", "A", "Riot"),
    ("PrimalItemArmor_GhillieHelmet", "Ghillie-Kapuze", "A", "Ghillie"),
    ("PrimalItemArmor_GhillieShirt", "Ghillie-Hemd", "A", "Ghillie"),
    ("PrimalItemArmor_GhilliePants", "Ghillie-Hose", "A", "Ghillie"),
    ("PrimalItemArmor_GhillieBoots", "Ghillie-Schuhe", "A", "Ghillie"),
    ("PrimalItemArmor_GhillieGloves", "Ghillie-Handschuhe", "A", "Ghillie"),
    ("PrimalItemArmor_HazardSuitHelmet", "Hazard-Helm", "A", "Hazard"),
    ("PrimalItemArmor_HazardSuitShirt", "Hazard-Anzug", "A", "Hazard"),
    ("PrimalItemArmor_HazardSuitPants", "Hazard-Hose", "A", "Hazard"),
    ("PrimalItemArmor_HazardSuitBoots", "Hazard-Stiefel", "A", "Hazard"),
    ("PrimalItemArmor_HazardSuitGloves", "Hazard-Handschuhe", "A", "Hazard"),

    # Saettel (eigene Vorlage: Items/Armor/Saddles/)
    ("PrimalItemArmor_ArgentavisSaddle", "Argentavis-Sattel", "S", ""),
    ("PrimalItemArmor_PteroSaddle", "Pteranodon-Sattel", "S", ""),
    ("PrimalItemArmor_RexSaddle", "Rex-Sattel", "S", ""),
    ("PrimalItemArmor_RaptorSaddle", "Raptor-Sattel", "S", ""),
    ("PrimalItemArmor_TrikeSaddle", "Triceratops-Sattel", "S", ""),
    ("PrimalItemArmor_StegoSaddle", "Stegosaurus-Sattel", "S", ""),
    ("PrimalItemArmor_SauropodSaddle", "Brontosaurus-Sattel", "S", ""),
    ("PrimalItemArmor_AnkyloSaddle", "Ankylosaurus-Sattel", "S", ""),
    ("PrimalItemArmor_DoedSaddle", "Doedicurus-Sattel", "S", ""),
    ("PrimalItemArmor_MammothSaddle", "Mammut-Sattel", "S", ""),
    ("PrimalItemArmor_SaberSaddle", "Sabertooth-Sattel", "S", ""),
    ("PrimalItemArmor_CarnoSaddle", "Carnotaurus-Sattel", "S", ""),
    ("PrimalItemArmor_SpinoSaddle", "Spinosaurier-Sattel", "S", ""),
    ("PrimalItemArmor_TherizinosaurusSaddle", "Therizinosaurus-Sattel", "S", ""),
    ("PrimalItemArmor_AlloSaddle", "Allosaurus-Sattel", "S", ""),
    ("PrimalItemArmor_YutySaddle", "Yutyrannus-Sattel", "S", ""),
    ("PrimalItemArmor_GigantSaddle", "Giganotosaurus-Sattel", "S", ""),
    ("PrimalItemArmor_MegalodonSaddle", "Megalodon-Sattel", "S", ""),
    ("PrimalItemArmor_MosasaurSaddle", "Mosasaurus-Sattel", "S", ""),
    ("PrimalItemArmor_TusoteuthisSaddle", "Tusoteuthis-Sattel", "S", ""),
    ("PrimalItemArmor_BasilosaurusSaddle", "Basilosaurus-Sattel", "S", ""),
    ("PrimalItemArmor_PlesiosaurSaddle", "Plesiosaurier-Sattel", "S", ""),
    ("PrimalItemArmor_QuetzSaddle", "Quetzal-Sattel", "S", ""),
    ("PrimalItemArmor_TapejaraSaddle", "Tapejara-Sattel", "S", ""),
    ("PrimalItemArmor_ProcoptodonSaddle", "Procoptodon-Sattel", "S", ""),
    ("PrimalItemArmor_BeaverSaddle", "Castoroides-Sattel", "S", ""),
    ("PrimalItemArmor_GallimimusSaddle", "Gallimimus-Sattel", "S", ""),
    ("PrimalItemArmor_BaryonyxSaddle", "Baryonyx-Sattel", "S", ""),
    ("PrimalItemArmor_SarcoSaddle", "Sarcosuchus-Sattel", "S", ""),
    ("PrimalItemArmor_ParacerSaddle", "Paraceratherium-Sattel", "S", ""),
    ("PrimalItemArmor_WoollyRhinoSaddle", "Wollnashorn-Sattel", "S", ""),
    ("PrimalItemArmor_MegatheriumSaddle", "Megatherium-Sattel", "S", ""),
    ("PrimalItemArmor_ThylacoleoSaddle", "Thylacoleo-Sattel", "S", ""),
]

VORLAGEN = {"W": W_A, "C": C_A, "R": R_A, "I": I_A, "M": M_A, "A": ARM, "S": SAD}


def blueprint(name: str, art: str, extra: str) -> str:
    if art == "A":
        return ARM % (extra, name, name)
    return VORLAGEN[art] % (name, name)


def eintraege() -> Iterable[dict]:
    for name, label, art, extra in ITEMS:
        yield {"name": name, "label": label, "bp": blueprint(name, art, extra)}


def suche(q: str, limit: int = 40) -> list[dict]:
    """Filtert nach Bezeichnung, Blueprint-Name oder Kategorie - ohne Gross-/Kleinschreibung."""
    wort = (q or "").strip().lower()
    treffer = []
    for e in eintraege():
        hay = (e["label"] + " " + e["name"]).lower()
        if not wort or wort in hay:
            treffer.append(e)
        if len(treffer) >= limit:
            break
    return treffer
