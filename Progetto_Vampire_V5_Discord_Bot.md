# Vampire: The Masquerade V5 --- Discord Bot

## Documento di progetto e continuità

**Stato:** prototipo funzionante, prima implementazione del motore dadi
avviata\
**Data aggiornamento:** 13 novembre 2026\
**Stack attuale:** Python, `discord.py`, `python-dotenv`\
**Ambiente di sviluppo:** Windows, PowerShell, virtual environment
`.venv`, Python 3.15\
**Ambito:** un singolo server Discord, una cronaca di Vampire: The
Masquerade Quinta Edizione.

------------------------------------------------------------------------

## 1. Scopo del progetto

Realizzare un bot Discord dedicato alla gestione di una cronaca di
**Vampire: The Masquerade V5**.

Il bot dovrà supportare sia il Narratore (Storyteller) sia i giocatori,
riducendo la gestione manuale di dadi, schede, Fame, Volontà, coterie e
sessioni.

Non deve essere soltanto un generatore casuale di dadi: l'obiettivo è un
assistente di cronaca con dati persistenti, permessi e storico.

### Decisioni già prese

  -----------------------------------------------------------------------
  Area                                Decisione
  ----------------------------------- -----------------------------------
  Server                              Un solo server Discord

  Ruoli applicativi                   Narratore e giocatori

  Tiri                                Il giocatore sceglie se rendere il
                                      risultato pubblico o privato

  Schede                              Il Narratore decide quali schede
                                      sono pubbliche

  Creazione personaggi                Modalità guidata e modalità manuale

  Storico                             Completo: tiri, modifiche, sessioni
                                      ed eventi

  Database iniziale                   SQLite

  Libreria Discord                    `discord.py`

  Test                                `pytest`

  Organizzazione                      Moduli separati, motore di gioco
                                      indipendente da Discord
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 2. Funzionalità previste

### 2.1 Motore dadi V5

È il primo componente da completare e verificare.

Comandi previsti: - `/roll`: tiro standard con pool, Fame e difficoltà;
opzione pubblico/privato. - `/rouse`: Rouse Check, da implementare come
procedura distinta. - `/willpower`: gestione e futuri tiri di Volontà. -
`/frenzy`: supporto alle prove di Frenesia, dopo aver definito
esattamente le regole da applicare.

Il motore deve distinguere dadi normali e dadi Fame e restituire i
risultati individuali, non soltanto il totale.

Regole di base già considerate: - Si usano d10. - Ogni risultato da 6 a
10 conta come un successo. - Ogni coppia di 10 produce un critico e
aggiunge due successi bonus. - Un Messy Critical si verifica quando il
tiro è un successo critico e almeno uno dei 10 che forma una coppia
critica proviene da un dado Fame. - Un Bestial Failure si verifica
quando il tiro fallisce e almeno un dado Fame mostra 1. - I dadi Fame
sostituiscono dadi normali: non aumentano il pool. - Il livello di Fame
è compreso tra 0 e 5.

**Nota di accuratezza:** il motore attuale abbina i 10 contando le
coppie (`numero_di_10 // 2`). Per stabilire la presenza di un Messy
Critical è sufficiente verificare che almeno uno dei dadi Fame abbia
ottenuto 10, purché esista almeno una coppia critica: con almeno due 10
e almeno un 10 Fame, è possibile formare una coppia che includa quel
dado Fame. La logica va comunque coperta da test deterministici.

Da verificare e formalizzare prima di considerare il motore completo: -
casi di pool e difficoltà limite; - eventuali tiri automatici o
difficoltà zero, secondo le regole adottate; - tiri contestati; - ritiri
tramite Volontà; - regole specifiche di Frenesia; - Rouse Checks e altre
procedure che non usano il normale pool con dadi Fame.

Non assumere che tutte le procedure di gioco siano un normale `/roll`.

### 2.2 Schede personaggio

Ogni personaggio dovrà essere collegato all'account Discord del
giocatore.

Dati previsti: - identità: nome del personaggio, giocatore, clan,
generazione; - attributi fisici, sociali e mentali; - abilità e
specializzazioni; - discipline e relativi poteri; - Fame; - Salute e
Volontà; - Ambizione, Desiderio e tipo di Predatore; - background,
contatti, equipaggiamento e note.

Comandi previsti: - `/character create` - `/character sheet` -
`/character edit` - `/character list`

La creazione sarà disponibile sia tramite procedura guidata sia tramite
inserimento manuale.

Permessi: - il giocatore crea e modifica il proprio personaggio; - il
Narratore può consultare e modificare tutti i personaggi; - la
visibilità pubblica o privata della scheda è controllata dal Narratore.

### 2.3 Coterie

Dati previsti: - nome e tipologia; - rifugio; - risorse e contatti; -
relazioni; - obiettivi comuni; - background condiviso; - membri
associati.

Comandi previsti: - `/coterie create` - `/coterie sheet` -
`/coterie edit` - `/coterie members`

La gestione sarà riservata al Narratore, con consultazione per i
giocatori secondo i permessi della cronaca.

### 2.4 Sessioni e cronaca

Il Narratore dovrà poter: - aprire e chiudere una sessione; - assegnare
titolo e descrizione; - registrare note ed eventi; - assegnare
esperienza; - consultare lo storico delle sessioni.

Comandi previsti: - `/session start` - `/session end` -
`/session note` - `/session history` - `/session xp`

Lo storico completo dovrà includere, con una politica di accesso
definita: - tiri effettuati; - autore e personaggio coinvolto; - data e
ora; - pool, Fame, difficoltà e risultati dei singoli dadi; - esito; -
modifiche alle schede; - eventi e note delle sessioni; - assegnazioni di
esperienza.

------------------------------------------------------------------------

## 3. Architettura tecnica prevista

Separare la logica di gioco dall'integrazione Discord.

Il motore dadi deve poter essere testato senza avviare il bot. I comandi
Discord ricevono i parametri, invocano il motore e presentano il
risultato.

Struttura obiettivo:

``` text
discord-bot/
│
├── bot.py
├── config.py
├── .env
├── requirements.txt
│
├── commands/
│   ├── __init__.py
│   ├── dice.py
│   ├── characters.py
│   ├── coterie.py
│   └── sessions.py
│
├── core/
│   ├── __init__.py
│   ├── dice_engine.py
│   ├── permissions.py
│   └── character_manager.py
│
├── database/
│   ├── database.py
│   ├── models.py
│   └── repositories/
│       ├── characters.py
│       ├── sessions.py
│       └── coterie.py
│
└── tests/
    ├── test_dice.py
    └── test_characters.py
```

La struttura può essere introdotta gradualmente: non è necessario creare
subito file vuoti per tutti i moduli.

### Tecnologie

-   `discord.py`: bot e slash commands.
-   `python-dotenv`: lettura delle variabili d'ambiente.
-   `SQLite`: persistenza locale nella prima versione.
-   `SQLAlchemy`: accesso e modellazione del database, da introdurre
    quando inizierà il modulo persistente.
-   `pytest`: test automatici.

Non è necessario introdurre Docker o un database remoto nella prima
fase.

------------------------------------------------------------------------

## 4. Stato effettivo dell'implementazione

### 4.1 Bot Discord

Il bot iniziale utilizzava una classe derivata da `discord.Client` e un
`CommandTree`.

Quando è stato introdotto il caricamento delle estensioni, è comparso:

``` text
AttributeError: 'Bot' object has no attribute 'load_extension'
```

**Causa:** `load_extension()` è disponibile nella classe `commands.Bot`,
non nel `discord.Client` di base.

**Correzione applicata:** usare `commands.Bot`.

Versione attuale di `bot.py`:

``` python
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
GUILD = discord.Object(id=int(os.environ["GUILD_ID"]))


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default()
        )

    async def setup_hook(self):
        await self.load_extension("commands.dice")

        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

        print("Comandi sincronizzati!")


client = Bot()


@client.tree.command(
    name="ping",
    description="Test di connessione"
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")


client.run(TOKEN)
```

**Stato:** l'utente ha confermato che, dopo questa modifica, il bot
funziona.

### 4.2 Configurazione `.env`

Il file contiene almeno:

``` env
DISCORD_TOKEN=il_token_del_bot
GUILD_ID=id_numerico_del_server
```

Non inserire token reali nel documento, nel repository o nei messaggi.
Il file `.env` deve essere escluso da Git tramite `.gitignore`.

### 4.3 Estensione Discord per i dadi

File `commands/dice.py`:

``` python
import discord
from discord.ext import commands
from discord import app_commands

from core.dice_engine import roll_v5


class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="roll",
        description="Esegue un tiro di dado V5"
    )
    @app_commands.describe(
        pool="Numero totale di dadi",
        hunger="Livello di Fame del personaggio",
        difficulty="Successi richiesti",
        private="Rendere privato il risultato?"
    )
    async def roll(
        self,
        interaction: discord.Interaction,
        pool: int,
        hunger: int,
        difficulty: int,
        private: bool = False
    ):
        try:
            result = roll_v5(
                pool=pool,
                hunger=hunger,
                difficulty=difficulty
            )
        except ValueError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True
            )
            return

        dice_display = []

        for die in result["dice"]:
            prefix = "F" if die["is_hunger"] else "N"
            dice_display.append(
                f"`{prefix}:{die['value']}`"
            )

        outcomes = {
            "success": "SUCCESSO",
            "critical": "CRITICAL SUCCESS",
            "messy_critical": "MESSY CRITICAL",
            "failure": "FALLIMENTO",
            "bestial_failure": "BESTIAL FAILURE"
        }

        colors = {
            "success": discord.Color.green(),
            "critical": discord.Color.gold(),
            "messy_critical": discord.Color.dark_red(),
            "failure": discord.Color.light_grey(),
            "bestial_failure": discord.Color.red()
        }

        outcome = result["outcome"]

        embed = discord.Embed(
            title=f"Tiro V5 - {outcomes[outcome]}",
            color=colors[outcome]
        )

        embed.add_field(
            name="Pool",
            value=f"{pool} dadi",
            inline=True
        )
        embed.add_field(
            name="Fame",
            value=str(hunger),
            inline=True
        )
        embed.add_field(
            name="Difficoltà",
            value=str(difficulty),
            inline=True
        )
        embed.add_field(
            name="Risultati",
            value=" ".join(dice_display),
            inline=False
        )
        embed.add_field(
            name="Successi",
            value=f"{result['successes']} / {difficulty}",
            inline=True
        )
        embed.add_field(
            name="Critici",
            value=str(result["critical_pairs"]),
            inline=True
        )
        embed.set_footer(
            text="N = Dado normale | F = Dado Fame"
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=private
        )


async def setup(bot):
    await bot.add_cog(Dice(bot))
```

### 4.4 Motore dadi iniziale

File `core/dice_engine.py`:

``` python
from secrets import randbelow


def roll_v5(
    pool: int,
    hunger: int,
    difficulty: int,
    rng=None
) -> dict:

    if not 1 <= pool <= 30:
        raise ValueError("Il pool deve essere compreso tra 1 e 30.")

    if not 0 <= hunger <= 5:
        raise ValueError("La Fame deve essere compresa tra 0 e 5.")

    if not 1 <= difficulty <= 30:
        raise ValueError("La difficoltà deve essere compresa tra 1 e 30.")

    if rng is None:
        rng = randbelow

    hunger_dice = min(pool, hunger)
    normal_dice = pool - hunger_dice

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

    base_successes = sum(
        die["value"] >= 6 for die in dice
    )

    tens = [die for die in dice if die["value"] == 10]

    critical_pairs = len(tens) // 2
    critical_bonus = critical_pairs * 2

    total_successes = base_successes + critical_bonus

    hunger_ones = sum(
        die["is_hunger"] and die["value"] == 1
        for die in dice
    )

    hunger_tens = sum(
        die["is_hunger"] and die["value"] == 10
        for die in dice
    )

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
```

**Nota tecnica:** il parametro `rng` riceve una funzione compatibile con
`secrets.randbelow`, cioè una funzione che restituisce un intero tra
zero incluso e il limite escluso. È stato previsto per rendere i test
deterministici.

### 4.5 Test proposti

È stato preparato un primo file `tests/test_dice.py` con cinque test: 1.
successo normale; 2. Messy Critical; 3. Critical Success pulito; 4.
Bestial Failure; 5. Fame superiore al pool, con verifica che i dadi Fame
non superino i dadi totali.

Installazione ed esecuzione:

``` powershell
pip install pytest
python -m pytest -v
```

**Stato dei test:** non è ancora stato riportato in chat un risultato di
esecuzione di `pytest`. Non considerare quindi i test già superati. Il
bot è stato confermato funzionante dopo la correzione a `commands.Bot`;
il funzionamento completo del comando `/roll` e del motore va ancora
verificato.

------------------------------------------------------------------------

## 5. Correzioni e miglioramenti tecnici da fare

Prima di aggiungere schede e database, completare la verifica del motore
dadi.

1.  Verificare tutti i casi critici con test deterministici.
2.  Verificare che i dadi Fame siano effettivamente sostituzioni dei
    dadi normali.
3.  Verificare i casi con più coppie di 10.
4.  Verificare che un 10 su dado Fame senza coppia critica non produca
    Messy Critical.
5.  Verificare che un 1 su dado Fame produca Bestial Failure solo quando
    il tiro complessivo fallisce.
6.  Decidere e documentare il comportamento dei pool e delle difficoltà
    limite in conformità alle regole V5.
7.  Aggiungere gestione degli errori e test per input non validi.
8.  Considerare un limite Discord alla lunghezza del campo contenente i
    dadi, per evitare embed troppo lunghi.

Non implementare procedure di Rouse Check, Volontà o Frenesia
riutilizzando automaticamente la logica del tiro standard: devono avere
funzioni e regole specifiche.

------------------------------------------------------------------------

## 6. Roadmap

### Versione 0.1 --- Motore dadi

-   [x] Bot Discord funzionante.
-   [x] Caricamento estensione con `commands.Bot`.
-   [ ] Verifica effettiva del comando `/roll`.
-   [ ] Esecuzione e superamento dei test.
-   [ ] Rifinitura delle regole e dei casi limite.
-   [ ] Storico dei tiri (inizialmente non persistente).

### Versione 0.2 --- Personaggi

-   [ ] Modello dati del personaggio.
-   [ ] Collegamento al proprietario Discord.
-   [ ] Creazione guidata.
-   [ ] Creazione manuale.
-   [ ] Consultazione e modifica della scheda.
-   [ ] Permessi Narratore/giocatore.
-   [ ] Visibilità controllata dal Narratore.
-   [ ] Persistenza SQLite.

### Versione 0.3 --- Coterie

-   [ ] Creazione e modifica.
-   [ ] Membri.
-   [ ] Rifugio, risorse, contatti e obiettivi.
-   [ ] Collegamento dei personaggi alla coterie.

### Versione 0.4 --- Sessioni e cronaca

-   [ ] Apertura e chiusura sessioni.
-   [ ] Note ed eventi.
-   [ ] Storico.
-   [ ] Assegnazione esperienza.
-   [ ] Registro modifiche alle schede.
-   [ ] Registro dei tiri.

### Versione successiva --- Funzionalità avanzate

-   [ ] Rouse Checks.
-   [ ] Volontà e relativi tiri.
-   [ ] Frenesia.
-   [ ] Gestione Salute e danni.
-   [ ] Umanità e altre risorse.
-   [ ] Iniziativa e supporto al combattimento.

------------------------------------------------------------------------

## 7. Prossima sessione di sviluppo: istruzioni operative

Riprendere il progetto da questi passaggi, in ordine:

1.  Verificare che la struttura delle cartelle sia corretta e che
    esistano `commands/__init__.py` e `core/__init__.py`.
2.  Creare o verificare `core/dice_engine.py` e `commands/dice.py`
    usando le versioni riportate.
3.  Avviare `python -m pytest -v` e correggere eventuali errori.
4.  Avviare `python bot.py`.
5.  Provare `/roll` su Discord con pool, Fame e difficoltà differenti.
6.  Verificare sia la risposta pubblica sia quella privata.
7.  Solo dopo la validazione, iniziare il modello dati delle schede
    personaggio.

### Comandi PowerShell utili

``` powershell
# Attivazione ambiente virtuale
.\.venv\Scripts\Activate.ps1

# Installazione test
pip install pytest

# Test
python -m pytest -v

# Avvio bot
python bot.py
```

### Regole di lavoro per le prossime iterazioni

-   Procedere un modulo alla volta.
-   Non riscrivere file funzionanti senza una ragione tecnica.
-   Separare sempre logica di gioco, integrazione Discord e persistenza.
-   Aggiungere test prima di estendere il motore.
-   Non dichiarare una funzionalità completata finché non è stata
    provata.
-   Quando una regola V5 è ambigua, segnalarla e verificarla prima di
    codificarla.
-   Conservare questo documento aggiornato a ogni decisione
    architetturale significativa.

------------------------------------------------------------------------

## 8. Registro decisioni

  Data         Decisione
  ------------ ------------------------------------------------
  13/11/2026   Progetto dedicato a Vampire: The Masquerade V5
  13/11/2026   Un solo server Discord
  13/11/2026   Gestione Narratore e giocatori
  13/11/2026   Tiri pubblici o privati a scelta
  13/11/2026   Visibilità schede controllata dal Narratore
  13/11/2026   Creazione personaggi guidata e manuale
  13/11/2026   Storico completo
  13/11/2026   SQLite come database iniziale
  13/11/2026   `commands.Bot` per supportare le estensioni
  13/11/2026   Primo modulo: motore dadi V5

------------------------------------------------------------------------

**Questo documento è la fonte di continuità del progetto.** Quando si
riprenderà il lavoro, allegarlo o incollarne il contenuto nella nuova
conversazione e aggiornare la sezione "Stato effettivo
dell'implementazione" dopo ogni modifica verificata.
