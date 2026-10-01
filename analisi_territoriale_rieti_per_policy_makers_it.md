# Rieti: specializzazioni produttive, divergenze demografiche e resilienza territoriale

**Base informativa per una presentazione ai decisori pubblici · revisione 30 settembre 2026**

## La tesi in un minuto

Rieti combina una popolazione contenuta, dispersa e anziana con attività manifatturiere collegate ai mercati internazionali e una componente logistica rilevante. La sfida non è soltanto attirare nuovi investimenti: è trasformare queste risorse in più opportunità di lavoro, competenze e servizi accessibili nei diversi contesti locali.

Quattro messaggi possono guidare la presentazione:

1. **Il calo demografico è molto disomogeneo.** I comuni più vicini a Roma crescono nel complesso, mentre il capoluogo e le aree più lontane perdono residenti. Il pendolarismo spiega in parte il fenomeno: in Sabina il 45% dei lavoratori residenti lavora in provincia di Roma. Servono insieme politiche di attrazione e adattamento dei servizi.
2. **La crescita dell’export non equivale automaticamente a sviluppo diffuso.** Le evidenze ufficiali rafforzano il ruolo della manifattura specializzata, ma mostrano anche una forte concentrazione. Competenze, fornitori e accesso al lavoro devono essere verificati con risultati locali.
3. **Rieti forma i suoi giovani ma non trattiene i laureati.** La perdita netta di giovani laureati è la peggiore del Centro-Nord. I profili tecnici e scientifici sono difficili da reperire, ma in provincia non esiste un corso post-diploma in farmaceutica, meccatronica o chimica. Una formazione tecnica mirata è giustificata, su scala contenuta.
4. **L’energia è un tema abilitante.** Rieti produce già molta elettricità rinnovabile, soprattutto idroelettrica. Il fotovoltaico può crescere su edifici e siti produttivi idonei, ma il potenziale effettivo richiede verifiche di rete, domanda, vincoli e proprietà.

La strategia consigliata è quindi un portafoglio differenziato: rafforzare manifattura e servizi produttivi; costruire con le imprese una piccola offerta di formazione tecnica legata alle specializzazioni esistenti; rendere il lavoro raggiungibile; adeguare mobilità, cura e abitazioni alla geografia demografica; sviluppare progetti energetici a partire da siti e consumi verificati. Agricoltura, trasformazione alimentare e turismo sono opportunità da testare con domanda e operatori identificati, non risultati già dimostrati dal modello.

## 1. Il territorio

Il dataset comunale comprende tutti i **73 comuni reatini**, **149.766 residenti**, circa **2.750 km²** e **54,5 abitanti/km²**. Il comune di Rieti conta **45.083 residenti**, il 30,1% del totale provinciale. **39 comuni hanno meno di 1.000 abitanti**; insieme rappresentano 17.163 persone (11,5%). La rete dei servizi deve quindi coprire molti piccoli insediamenti oltre al capoluogo.

Le colonne demografiche denominate `2021` e `2025` vanno interpretate come stock di inizio anno: per Rieti corrispondono ai totali ISTAT al 31 dicembre 2020 e al 31 dicembre 2024. Non descrivono quattro anni completi fino a dicembre 2025. Nel 2011 la popolazione era 155.164; il calo fino a fine 2024 è circa il 3,5%. [ISTAT 2021](https://www.istat.it/wp-content/uploads/2023/09/Lazio-Focus2021-Censimantopermanente.pdf), [ISTAT 2024](https://www.istat.it/wp-content/uploads/2026/04/12_Focus_Censimento_Popolazione_Lazio_2024.pdf).

I confronti più utili sono L’Aquila (densità simile), Viterbo (provincia vicina e stesso sistema camerale), Terni (territorio vicino e anziano) e Frosinone (comparatore manifatturiero regionale). Nessuno è un gemello perfetto: densità, struttura industriale e accessibilità sono diverse. Il dataset contiene otto gruppi provinciali (AQ, FR, IS, LT, RI, TE, TR, VT) e non include Roma; ogni media del Lazio deve quindi indicare chiaramente la copertura.

## 2. Demografia e geografia interna

| Provincia | Residenti inizio 2025 | Densità | Variazione inizio 2021–inizio 2025 | 65+ (%) | Indice di vecchiaia |
|---|---:|---:|---:|---:|---:|
| **Rieti** | **149.766** | **54,5** | **−1,04%** | **27,5** | **268,4** |
| L’Aquila | 286.706 | 56,8 | −1,41% | 26,9 | 243,1 |
| Viterbo | 307.405 | 85,0 | −0,46% | 26,3 | 243,4 |
| Terni | 215.285 | 101,2 | −2,12% | 29,1 | 283,6 |
| Frosinone | 462.661 | 142,5 | −2,09% | 26,0 | 224,6 |

L’indice di vecchiaia è calcolato come 65+ diviso 0–14, dopo aver sommato i residenti dei comuni; non è la media ponderata degli indici comunali. Il valore corretto per Rieti è 268,4, coerente con ISTAT. Rieti non è la provincia che si spopola più rapidamente: il problema è la combinazione di bassa densità, quota anziana elevata e forti differenze interne. [Tabella riproducibile](analysis/output/demographic_peers.csv).

![Confronto demografico](analysis/figures/01_demographic_peers.png)

Nel 2024 il bilancio ISTAT è: saldo naturale −1.153, migrazione interna +53, migrazione estera +1.109, aggiustamento statistico −231, variazione complessiva −222. La migrazione quasi compensa il saldo naturale. Il campo comunale `saldo_migratorio_2025` non è riconciliabile con questo bilancio e non viene utilizzato per spiegare la dinamica.

La distanza corretta da Roma presente nel dataset è una proxy che include una penalità altimetrica: non è tempo di viaggio, accessibilità ferroviaria o classificazione ufficiale delle aree interne. Le fasce sono quindi esplorative:

| Distanza corretta da Roma | Comuni | Residenti | Variazione | Indice di vecchiaia | Densità |
|---|---:|---:|---:|---:|---:|
| **<55 km** | 27 | 57.585 | **+1,10%** | 234,4 | 99,5 |
| **55–85 km** | 39 | 85.840 | **−2,07%** | 283,1 | 57,4 |
| **>85 km** | 7 | 6.341 | **−5,68%** | 445,2 | 9,4 |

Il gradiente resta simile usando soglie di 50 o 60 km, ma non dimostra un effetto causale della vicinanza a Roma. Il capoluogo perde 824 residenti (−1,8%) e spiega il 52,5% della perdita provinciale. L’area oltre 85 km contiene solo il 4,2% degli abitanti ma circa un quarto del territorio. [Fasce](analysis/output/distance_bands.csv), [sensibilità](analysis/output/distance_threshold_sensitivity.csv).

![Punti comunali e fasce esplorative](analysis/figures/02_internal_geography.png)

### Pendolarismo: Roma è un mercato del lavoro quotidiano per la Sabina, non per tutta la provincia

La matrice ISTAT 2021 del pendolarismo per lavoro conta **48.401 residenti reatini** che si spostano per lavoro almeno tre giorni a settimana. **14.449 (30%) lavorano fuori provincia**: 11.934 nella provincia di Roma, di cui 9.176 nel comune di Roma. Solo 5.090 persone entrano in provincia per lavorare: il saldo quotidiano è di circa **9.400 lavoratori in uscita**.

| Distanza corretta da Roma | Pendolari residenti 2021 | Nel proprio comune | Nel comune di Rieti | In provincia di Roma | Posti di lavoro per lavoratore residente |
|---|---:|---:|---:|---:|---:|
| **<55 km** | 18.289 | 27% | 5% | **45%** | 0,65 |
| **55–85 km** | 28.165 | 54% | 14% | 12% | 0,90 |
| **>85 km** | 1.947 | 61% | 11% | 11% | 0,92 |

I comuni in crescita vicini a Roma sono in larga parte luoghi di residenza per chi lavora a Roma: Fara in Sabina vi invia il 63% dei lavoratori residenti, Scandriglia il 53%, Forano il 49%. La matrice ISTAT dei tempi di percorrenza stradali conferma la proxy di distanza usata nel documento (correlazione 0,92); nessun comune reatino è a meno di 72 minuti d’auto dal centro di Roma. Il legame tra pendolarismo verso Roma e variazione della popolazione è moderato (correlazione 0,29): un’associazione, non un nesso causale. Il capoluogo è il principale polo interno (18.267 posti di lavoro coperti da pendolari, 5.065 lavoratori da altri comuni reatini); Fara in Sabina è un nodo a doppio senso, con il 45% dei suoi posti occupati da residenti fuori provincia. Il polo industriale Rieti–Cittaducale recluta localmente: il 93% dei suoi lavoratori risiede in provincia. [Tabella comunale](analysis/output/commuting_municipal_2021.csv), [fasce](analysis/output/commuting_bands_2021.csv).

![Pendolarismo verso Roma e destinazioni](analysis/figures/05_commuting.png)

**Il confronto 2011–2021** va letto con cautela, perché le definizioni sono diverse (2011: spostamenti quotidiani dichiarati al censimento; 2021: stima da archivi amministrativi, almeno tre giorni a settimana). La direzione è comunque chiara: la quota di chi lavora nel proprio comune scende dal 50% al 44%; chi lavora in provincia di Roma passa da 10.079 (21%) a 11.934 (25%); i posti di lavoro del polo Rieti–Cittaducale restano fermi (20.657 e 20.661), mentre i suoi residenti che lavorano a Roma salgono da 1.120 a 1.653. Nei comuni montani lontani (Amatrice, Leonessa, Borgorose) la quota verso Roma circa raddoppia: poiché il metodo 2021 attribuisce il luogo di lavoro da archivi previdenziali e fiscali, il dato indica più residenti legati a datori di lavoro con sede a Roma, non necessariamente più spostamenti quotidiani. [Flussi 2011–2021](analysis/output/commuting_flows_2011_2021.csv), [confronto comunale](analysis/output/work_commuting_municipal_2011_2021.csv).

Nel 2011, ultimo anno con questo dettaglio, chi lavorava a Roma usava per il 55% l’auto, per il 26% il treno e per l’11% la corriera; il 56% impiegava oltre un’ora e il 70% usciva di casa prima delle 7:15. Le donne lavoravano meno spesso in provincia di Roma (17% contro il 24% degli uomini). Il pendolarismo per studio era soprattutto locale: il 65% dei 23.400 studenti pendolari studiava nel proprio comune e il 23% in un altro comune reatino. La matrice 2021 per studio è stata pubblicata dall’ISTAT e sostituirà questi dati quando il portale ISTAT tornerà raggiungibile. [Mezzo e tempi 2011](analysis/output/commuting_mode_time_2011.csv), [studio](analysis/output/study_commuting_municipal_2011_2021.csv).

## 3. Economia, lavoro e prosperità

Le tavole camerali più recenti riportano per il 2024 un valore aggiunto pro capite di **24.245 euro** per Rieti, contro 33.348 euro in Italia e 39.120 nel Lazio. Rieti è quindi circa il 27,3% sotto la media italiana. Il valore aggiunto complessivo passa da 3,507 miliardi nel 2023 a 3,636 miliardi nel 2024 (+3,7% a prezzi correnti); questo non misura la crescita reale al netto dell’inflazione. Le stime di pubblicazioni precedenti sono diverse e non vengono concatenate. [Tavole camerali](https://www.chpe.camcom.it/pagina182570_statistiche-su-valore-aggiunto.html/).

| Tasso di occupazione 15–64 anni | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|
| **Rieti** | **58,4** | **61,8** | **62,7** | **60,8** |
| Viterbo | 58,4 | 58,0 | 63,9 | 62,3 |
| Frosinone | 56,2 | 55,5 | 57,8 | 59,5 |
| Lazio | 61,8 | 63,2 | 64,0 | 64,2 |
| Italia | 60,1 | 61,5 | 62,2 | 62,5 |

Nel 2025 gli occupati reatini diminuiscono del 2,1%, mentre in Italia aumentano dello 0,8%. Nel 2024 il tasso è 70,9% per gli uomini e 54,1% per le donne: un divario di 16,8 punti. Il dato suggerisce di collegare formazione e imprese a trasporti, cura e conciliazione, senza attribuire automaticamente una causa alla sola differenza statistica. [Rapporto camerale 2025](https://www.rivt.camcom.it/files/quintorapportoeconomiaaltolazio-_11821.pdf).

La disoccupazione è moderatamente superiore ai benchmark, non eccezionale: **7,3% nel 2025**, contro 6,1% in Italia e 5,5% nel Lazio. Le debolezze più marcate sono partecipazione e retribuzioni: il tasso di inattività è **34,3%** ed è in aumento, e la retribuzione media annua lorda dei dipendenti è **18.480 euro** (2023), contro 23.630 in Italia. I NEET 15–29 anni sono il 12,0%, meno della media italiana (15,2%). Poiché circa 9.400 residenti in più escono dalla provincia per lavoro rispetto a quanti vi entrano, una parte dei redditi dei residenti è prodotta a Roma, mentre il valore aggiunto pro capite misura la produzione localizzata a Rieti. [BES dei territori 2025](https://www.istat.it/notizia/bes-dei-territori-edizione-2025/).

## 4. Export e struttura produttiva

Le esportazioni ufficiali di beni crescono da **591,7 milioni nel 2024 a 878,4 milioni nel 2025 (+48,5%)**. I prodotti farmaceutici rappresentano l’80,1% dell’export 2025; escludendoli, le esportazioni diminuiscono di circa il 6%. La crescita è quindi forte ma concentrata. La Camera di Commercio documenta inoltre la specializzazione della “Pump Valley” Rieti–Cittaducale, con competenze meccaniche ed elettroniche e forte orientamento estero. [Export 2025](https://www.rivt.camcom.it/files/quintorapportoeconomiaaltolazio-_11821.pdf), [Pump Valley](https://www.rivt.camcom.it/it/news/rieti-boom-export-manifatturiero-e-spiragli-di-luce-da-costruzioniturismo-e-attivita-professionali_1951.htm).

Il SAM 2022 stima **6,50 miliardi di euro di output lordo** e **2,97 miliardi di valore aggiunto lavoro+capitale**. L’output lordo non è PIL. Le principali attività sono:

| Attività SAM | Output (€m) | Valore aggiunto (€m) | LQ vs Lazio | Lettura |
|---|---:|---:|---:|---|
| Costruzioni | 766,5 | 231,1 | 1,85 | Retrofit, sicurezza e resilienza. |
| Logistica e supporto ai trasporti | 608,3 | 235,2 | 3,02 | Piattaforma per manifattura e servizi. |
| Sanità | 442,8 | 214,6 | 1,32 | Servizio essenziale in un territorio anziano. |
| Agricoltura e allevamento | 332,5 | 191,4 | 6,05 | Specializzazione da collegare a domanda e trasformazione. |
| Farmaceutica | 249,5 | 87,6 | 3,56 | Specializzazione esportatrice da consolidare. |
| Meccanica | 139,2 | 38,3 | 5,17 | Competenze e filiera fornitori. |
| Elettronica/ottica | 130,2 | 46,4 | 5,76 | Nicchia tecnica da validare con le imprese. |

Il controllo con le esportazioni camerali 2022 mostra differenze rilevanti per farmaceutica, elettronica, alimentare e agricoltura; la meccanica è invece numericamente vicina. Le categorie doganali e quelle del SAM non coincidono: i valori modellati non vanno quindi presentati come export osservato. L’agroalimentare resta una pista, da sottoporre a verifica di volumi, compratori, margini e capacità degli impianti.

Gli acquisti intermedi modellati dentro Rieti sono 5,9 milioni (0,17% del totale), contro 456,2 milioni dal resto del Lazio, 2.401,1 milioni dal resto d’Italia e 555,4 milioni dall’estero. È un risultato di allocazione del modello, non una misura osservata degli acquisti locali. Non va trasformato in prova che l’economia locale sia priva di filiere.

I moltiplicatori nazionali sono scenari di tecnologia media: logistica 2,05 di output e 0,83 di valore aggiunto per euro di domanda; meccanica 2,00 e 0,65; costruzioni 2,35 e 0,81. Non sono rendimenti di progetto, effetti occupazionali o benefici trattenuti a Rieti.

![Occupazione ed export](analysis/figures/03_exports_and_employment.png)

## 5. Competenze e laureati: un divario reale, su scala contenuta

Una lettura diffusa è che Rieti abbia una farmaceutica e una “Pump Valley” forti, ma soffra comunque di alta disoccupazione e fuga dei cervelli. I dati confermano una parte di questa lettura, ne correggono un’altra e indicano un ruolo preciso, ma limitato, per la formazione tecnica.

**Le specializzazioni sono reali ma piccole in termini di occupazione.**

- **Farmaceutica.** Farmindustria colloca Rieti **al 2° posto in Italia per peso della farmaceutica sull’occupazione manifatturiera**, ma fuori dalle prime 25 province per numero di addetti. [Farmindustria, Indicatori Farmaceutici 2025, Tav. 105](https://www.farmindustria.it/app/uploads/2022/03/IndicatoriFarmaceutici2025_Def_05082025.pdf#page=87). È concentrata in poche aziende; la principale è Takeda a Cittaducale (plasmaderivati), con oltre 750 addetti e il 64% dell’export provinciale nel 2024 secondo l’azienda, pari a circa l’1,3% degli occupati. [Takeda, ottobre 2024](https://www.takeda.com/it-it/comunicati-stampa/2024/centro-innovazione/). Nel 2026 il gruppo è in riorganizzazione e le rappresentanze sindacali riferiscono una cassa integrazione ordinaria (CIGO) temporanea legata a una fermata per manutenzione e investimenti. [RSU e sindacati, luglio 2026](https://www.formatrieti.it/2026/07/25/takeda-rieti-la-posizione-di-rsu-e-sindacati-facciamo-chiarezza/), [accordo, agosto 2026](https://www.formatrieti.it/2026/08/31/takeda-rieti-positivo-lesito-del-confronto-sindacale-si-apre-una-nuova-fase-sul-piano-industriale-e-sulle-prospettive-occupazionali/).
- **Pump Valley.** SEKO (circa 410 addetti a Rieti) ed EMEC (oltre 200) occupano da sole quanto lo stabilimento farmaceutico; Microdos appartiene al gruppo olandese Verder. Non esistono un’organizzazione di distretto né un’istituzione formativa dedicata. Sono dati aziendali e di stampa, non statistiche ufficiali. [SEKO](https://www.formatrieti.it/2025/10/17/federlazio-si-congratula-con-seko-s-p-a-e-con-il-dott-stefano-folio-per-lalta-onorificenza-per-la-sostenibilita/), [EMEC](https://www.emecpumps.com/chi-siamo/).

**La fuga dei laureati è confermata.**

| Indicatore | Rieti | Viterbo | L’Aquila | Terni | Frosinone | Lazio | Italia |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Mobilità dei laureati italiani 25–39 anni, per 1.000 (2023)** | **−32,8** | −12,9 | −18,1 | −23,5 | −29,6 | +5,0 | −6,2* |
| Laureati 25–39 anni, % (2024) | **23,9** | 25,5 | 30,9 | 30,7 | 27,3 | 35,3 | 30,9 |
| Almeno il diploma, 25–64 anni, % (2024) | 73,9 | 70,6 | 71,8 | 76,6 | 74,7 | 75,1 | 66,7 |
| Passaggio all’università, % (2022) | 55,6 | 55,4 | 62,6 | 59,3 | 50,8 | 57,4 | 51,7 |
| NEET 15–29 anni, % (2024) | 12,0 | 14,3 | 18,5 | 10,7 | 15,9 | 15,2 | 15,2 |
| Retribuzione media annua lorda dei dipendenti, € (2023) | 18.480 | 17.740 | 19.574 | 20.923 | 20.333 | 24.169 | 23.630 |

\*Per l’Italia sono conteggiati solo i movimenti con l’estero. Fonte: [ISTAT, BES dei territori 2025](https://www.istat.it/notizia/bes-dei-territori-edizione-2025/); [tabella](analysis/output/bes_human_capital_peers.csv).

Rieti è **22ª su 107 province** per perdita di laureati: le 21 che fanno peggio sono tutte nel Mezzogiorno, quindi è il valore peggiore del Centro-Nord. Il saldo è negativo ogni anno dal 2019. Il problema non è la scuola: il livello di istruzione degli adulti è sopra la media, il passaggio all’università è superiore alla media italiana e i NEET sono pochi. I giovani studiano fuori e non tornano: dei 3.846 residenti iscritti ad atenei tradizionali nel 2024/25, **solo il 12% studia in provincia e il 49% a Roma**. [MUR-USTAT](https://dati-ustat.mur.gov.it/dataset/iscritti). I residenti di 20–34 anni calano del 5,7% tra il 2019 e il 2026, il doppio della popolazione totale. L’offerta universitaria a Rieti cresce (1.331 iscritti nel 2024/25, 767 nel 2019/20) ma riguarda ingegneria edile e professioni sanitarie: non ci sono corsi di chimica, farmacia o ingegneria industriale. Gli indicatori campionari provinciali sono volatili: nella tabella di supporto sono riportate medie triennali.

![Mobilità dei laureati e profili tecnici difficili da reperire](analysis/figures/06_skills_and_graduates.png)

**La domanda delle imprese riguarda profili tecnici scarsi, ma in numeri piccoli.** Excelsior (Unioncamere–Ministero del Lavoro) prevede per il 2025 **8.870 entrate a Rieti, il 45,6% di difficile reperimento** (Lazio 42,1%, Italia 47,0%); solo il **9,5% richiede la laurea** (Lazio 15,5%). I profili più scarsi sono quelli legati a farmaceutica e meccanica: specialisti in scienze chimiche e fisiche (110 entrate, 98% difficili), laureati chimico-farmaceutici (60, 84%), operai della meccanica di precisione (60, 85%), meccanici e manutentori (190, 76%), diplomati in meccanica, meccatronica ed energia (220, 68%). La domanda più ampia resta quella di personale non qualificato della logistica (1.460 entrate). Sono intenzioni di assunzione, non assunzioni effettive. [Tabella profili](analysis/output/excelsior_2025_rieti_profiles.csv).

**Manca il gradino dopo il diploma.** Gli istituti tecnici formano già la base: l’IIS Rosatelli ha 179 studenti negli indirizzi chimica-materiali-biotecnologie e 306 in meccanica, meccatronica, elettronica e automazione; l’IIS Aldo Moro di Fara in Sabina 377 in elettronica e telecomunicazioni. [Dati MIM](analysis/output/secondary_school_supply_rieti_2024_25.csv). Ma in provincia gli unici corsi ITS Academy sono di logistica (Fara in Sabina) e agroalimentare (Rieti); gli ITS laziali di farmaceutica e meccatronica operano a Roma, Pomezia, Frosinone e Latina. L’avviso regionale ITS 2026 finanzia 80 corsi da circa 330.000 euro ciascuno, ma è scaduto il 22 settembre 2026: l’obiettivo realistico è la programmazione 2027. [Avviso ITS Lazio 2026](https://www.regione.lazio.it/sites/default/files/documentazione/2026/DD-G11637-19-08-2026-allegato1-avviso.pdf).

**Cosa ne deriva.** La formazione specialistica è giustificata nella misura di uno o due corsi ITS (circa 25 studenti ciascuno): qualità e produzione farmaceutica, erogato a Rieti dall’ITS farmaceutico esistente, e meccatronica e manutenzione, progettato con i produttori di pompe. Da sola non basta a invertire la fuga dei laureati: servono anche tirocini retribuiti, percorsi di rientro e ruoli per laureati nelle imprese. Ogni corso va costruito con più imprese, per non dipendere dalle decisioni di poche aziende.

## 6. Energia e rinnovabili

Nel 2024 Rieti produce **297,9 GWh** di elettricità lorda, di cui **290,5 GWh rinnovabili**: 220,7 idroelettrici, 49,2 fotovoltaici e 20,6 da bioenergie. Le rinnovabili sono il 97,5% della produzione provinciale, ma questo non equivale alla quota dei consumi coperta localmente. [Terna 2024](https://download.terna.it/terna/Statistiche%20Regionali_2024_8de8598cb39d81e.pdf).

La potenza fotovoltaica passa da circa 44 MW nel 2023 a 53 MW nel 2024. Il confronto pro capite resta molto diverso: Rieti 0,35 kW/abitante, Terni 0,81, Frosinone 0,61, Viterbo 5,14. Il divario segnala una diversa diffusione, non un potenziale tecnicamente disponibile.

L’indice energetico copre 73 comuni e 30.214 addetti localizzati in luoghi di lavoro nel 2022. I comuni ad alto o molto alto rischio concentrano 7.900 addetti (26,1%). Fara in Sabina, Cittaducale e Montopoli di Sabina sono i principali casi da sottoporre ad audit. L’indice è un modello di esposizione, non una bolletta aziendale o una stima di capacità rinnovabile; inoltre tutti i comuni reatini hanno gli stessi input di copertura solare/eolica.

La proposta è partire da coperture industriali e logistiche, edifici pubblici, fabbricati agricoli e siti già urbanizzati. Per ogni sito servono superficie utile, domanda oraria, connessione, ombreggiamento, proprietà e vincoli. Gli scenari 5, 10 e 20 MW riportati nei dati di supporto sono semplici esercizi di dimensionamento, non stime di potenziale realizzabile.

![Generazione rinnovabile e fotovoltaico](analysis/figures/04_energy_context.png)

## 7. SWOT orientata alle decisioni

| Punti di forza | Debolezze |
|---|---|
| Manifattura specializzata: farmaceutica (2ª provincia per peso sull’occupazione manifatturiera) e Pump Valley. | Bassa densità e forte frammentazione insediativa. |
| Crescita aggregata della fascia vicina a Roma, sostenuta dall’accesso al mercato del lavoro romano. | Divergenza tra Sabina, capoluogo e aree montane. |
| Base rinnovabile idroelettrica e crescita del fotovoltaico. | Valore aggiunto pro capite e partecipazione al lavoro inferiori ai benchmark. |
| Logistica, costruzioni e sanità come attività rilevanti nel SAM. | Export molto concentrato: la farmaceutica è concentrata in poche aziende. |
| Buona base scolastica: istruzione degli adulti, passaggio all’università e NEET migliori della media; istituti tecnici già attivi in chimica, meccatronica ed elettronica. | Perdita di laureati (la peggiore del Centro-Nord), poca domanda di laureati e retribuzioni basse. |

| Opportunità | Minacce |
|---|---|
| Sviluppare fornitori, manutenzione, ingegneria e competenze intorno agli anchor industriali. | Shock su un grande comparto o impresa esportatrice. |
| Integrare lavoro, trasporti, abitazioni, cura e servizi per trattenere famiglie. | Spirale tra perdita di popolazione attiva e riduzione dei servizi. |
| Audit energetici e fotovoltaico su siti produttivi verificati. | Investimenti basati su potenziali territoriali o moltiplicatori non validati. |
| Progetti agroalimentari e turistici guidati da compratori e operatori reali. | Pressioni energetiche, climatiche e idriche. |
| Completare la filiera formativa tecnica con uno o due corsi ITS a Rieti (farmaceutica; meccatronica e manutenzione). | Dipendenza crescente da Roma e da poche aziende farmaceutiche, con la principale in riorganizzazione. |

## 8. Agenda operativa

1. **Competenze e fornitori industriali:** intervistare imprese anchor, mappare profili difficili da reperire e organizzare i produttori di pompe in una rete comune per competenze e fornitori.
2. **Filiera formativa tecnica:** chiedere alle fondazioni ITS laziali di farmaceutica e meccatronica di attivare corsi a Rieti nella programmazione 2027, con programmi e tirocini concordati con più imprese e collegati agli istituti Rosatelli e Aldo Moro tramite formazione duale.
3. **Trattenere e far rientrare i laureati:** sperimentare tirocini retribuiti e percorsi di rientro per i residenti che studiano a Roma e L’Aquila, chiedendo alle imprese di individuare ruoli per laureati.
4. **Lavoro e residenzialità:** verificare collegamenti tra turni, trasporto pubblico, abitazioni e servizi di cura nei principali bacini occupazionali.
5. **Servizi nei piccoli comuni:** misurare tempi reali di accesso a salute, scuola e mobilità e definire standard intercomunali.
6. **Energia sui siti ad alto carico:** realizzare audit su Fara in Sabina, Cittaducale e altri siti produttivi, includendo calore e trasporti.
7. **Agroalimentare guidato dal mercato:** investire in lavorazione o catena del freddo soltanto dopo aver verificato volumi, compratori, margini e gestione.

Nei primi tre mesi servono baseline, domanda degli anchor, bacini di servizio e siti energetici; nei successivi tre mesi si seleziona un portafoglio con operatori, costi e utenti identificati; entro dodici mesi si implementano i piloti fattibili e si misurano gli esiti.

## 9. Struttura suggerita per 14 slide

1. La sfida: specializzazione produttiva e divergenza demografica.
2. Il territorio: popolazione, densità, capoluogo e piccoli comuni.
3. Il confronto con i peer.
4. Perché la popolazione diminuisce: saldo naturale e migrazioni.
5. Le differenze interne e i limiti delle fasce di distanza.
6. Dove lavorano i residenti: pendolarismo verso Roma e interno, 2011–2021.
7. Valore aggiunto, occupazione, partecipazione, retribuzioni e divario di genere.
8. Export: crescita e concentrazione farmaceutica in poche aziende.
9. Cosa aggiunge il SAM e quali sono i suoi limiti.
10. Fuga dei laureati e formazione tecnica: domanda, offerta e gradino mancante.
11. Filiere da testare: manifattura, logistica, agroalimentare e servizi.
12. Energia: idroelettrico, fotovoltaico e audit sui carichi.
13. SWOT.
14. Priorità, primi 90 giorni e indicatori di risultato.

## Fonti e limiti

La versione italiana utilizza il dataset comunale, il SAM 2022, l’indice energetico, ISTAT, Terna, GSE, Regione Lazio e i rapporti della Camera di Commercio Rieti–Viterbo. Le verifiche e le definizioni sono raccolte nell’[appendice di validazione](analysis/validation_and_sources.md); gli output riproducibili sono in [analysis/output](analysis/output), le figure in [analysis/figures](analysis/figures), e il documento tecnico SAM aggiornato è [qui](SAM/analisi_sam_rieti_2022.md).

Questa revisione aggiunge le matrici ISTAT del pendolarismo (lavoro 2021; lavoro e studio 2011), i tempi di percorrenza stradali ISTAT, il BES dei territori, gli iscritti MUR-USTAT, i dati scolastici MIM, Excelsior e Farmindustria. Gli addetti delle imprese provengono da fonti aziendali e di stampa. Restano da misurare con fonti dedicate: tempi del trasporto pubblico, disponibilità abitativa, domanda turistica, occupazione ufficiale per settore (ISTAT ASIA), pendolarismo per studio 2021, rischio sismico, vincoli di rete e fattibilità economica dei progetti. Gli script sono `analysis/scripts/build_commuting_evidence.py`, `build_skills_evidence.py` e, quando il portale ISTAT sarà raggiungibile, `fetch_istat_study_matrix.py`. Questi elementi devono precedere la selezione degli investimenti.
