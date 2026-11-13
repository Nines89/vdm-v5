
from secrets import randbelow


def roll_v5(
    pool: int,
    hunger: int,
    difficulty: int,
    rng=None
) -> dict:

    # Validazione
    if not 1 <= pool <= 30:
        raise ValueError("Il pool deve essere compreso tra 1 e 30.")

    if not 0 <= hunger <= 5:
        raise ValueError("La Fame deve essere compresa tra 0 e 5.")

    if not 1 <= difficulty <= 30:
        raise ValueError("La difficoltà deve essere compresa tra 1 e 30.")

    # Permette di utilizzare un generatore deterministico nei test
    if rng is None:
        rng = randbelow

    # La Fame sostituisce i dadi normali
    hunger_dice = min(pool, hunger)
    normal_dice = pool - hunger_dice

    # Lancio dei dadi
    dice = []

    for _ in range(normal_dice):
        dice.append({
            "value": rng(10) + 1,
            "is_hunger": False
        })

    for _ in range(hunger_dice):
        dice.append({
            "value": rng(10) + 1,
            "is_hunger": True
        })

    # Conteggio dei successi
    base_successes = sum(
        die["value"] >= 6 for die in dice
    )

    # Coppie di 10
    tens = [die for die in dice if die["value"] == 10]

    critical_pairs = len(tens) // 2
    critical_bonus = critical_pairs * 2

    total_successes = base_successes + critical_bonus

    # Risultati sui dadi Fame
    hunger_ones = sum(
        die["is_hunger"] and die["value"] == 1
        for die in dice
    )

    hunger_tens = sum(
        die["is_hunger"] and die["value"] == 10
        for die in dice
    )

    # Determinazione dell'esito
    success = total_successes >= difficulty

    if success:
        if critical_pairs > 0 and hunger_tens > 0:
            outcome = "messy_critical"
        elif critical_pairs > 0:
            outcome = "critical"
        else:
            outcome = "success"

    else:
        if hunger_ones > 0:
            outcome = "bestial_failure"
        else:
            outcome = "failure"

    return {
        "pool": pool,
        "hunger": hunger,
        "hunger_dice": hunger_dice,
        "difficulty": difficulty,
        "dice": dice,
        "base_successes": base_successes,
        "critical_pairs": critical_pairs,
        "critical_bonus": critical_bonus,
        "successes": total_successes,
        "margin": total_successes - difficulty,
        "hunger_ones": hunger_ones,
        "hunger_tens": hunger_tens,
        "outcome": outcome
    }
