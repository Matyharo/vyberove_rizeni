"""One-time, explicit transcription of facts inspected in public web sources.

This is NOT a scraper or an LLM extraction benchmark. It builds the reviewable
input JSON from the research notes below. No network or external dependencies.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AS_OF = "2026-10-22"
sources, investors, claims, transactions, decisions, funds = [], [], [], [], [], []


def source(sid, url, publisher, title, summary, published=None, kind="investor"):
    sources.append(dict(id=sid, url=url, publisher=publisher, title=title,
                        published_on=published, accessed_on=AS_OF, kind=kind,
                        access_method="web_tool_open", evidence_summary=summary))
    return sid


def claim(iid, field, value, sid, note="", status="supported", scope="organization", as_of=None):
    cid = f"{iid}.{field}.{sum(c['investor_id'] == iid and c['field'] == field for c in claims) + 1}"
    claims.append(dict(id=cid, investor_id=iid, field=field, value=value,
                       source_id=sid, scope=scope, valid_as_of=as_of,
                       status=status, note=note))


def investor(iid, name, website, sid, office, sectors, stage, geography, ticket, note=""):
    investors.append(dict(id=iid, name=name, website=website, entity_level="investment_organization",
                          human_verified=False))
    claim(iid, "name", name, sid)
    claim(iid, "website", website, sid)
    claim(iid, "investor_type", "venture_capital", sid,
          "Klasifikace AI podle mandátu a doložené investice; nikoli právní licence.")
    claim(iid, "czech_office", office, sid)
    claim(iid, "sectors", sectors, sid)
    claim(iid, "stage", stage, sid)
    claim(iid, "geography", geography, sid)
    claim(iid, "ticket", ticket, sid, note,
          status="supported" if ticket else "not_found")
    claim(iid, "total_investment_capital", None, sid,
          "Srovnatelný aktuální celkový kapitál organizace není v použitých zdrojích doložen. Viz oddělené capital_reference.",
          status="not_found")


def capital(iid, metric, amount, currency, sid, scope, note, status="supported", as_of=None, bound="exact"):
    claim(iid, "capital_reference", dict(metric=metric, amount=amount, currency=currency, bound=bound),
          sid, note, status=status, scope=scope, as_of=as_of)


def transaction(iid, company, sid, date=None, precision="unknown", date_kind="announcement", round_amount=None,
                note="", corroborating=None):
    transactions.append(dict(id=f"tx-{iid}-{len(transactions)+1}", investor_id=iid, company=company,
                             source_id=sid, corroborating_source_ids=corroborating or [], date=date,
                             date_precision=precision, date_kind=date_kind, round_amount=round_amount,
                             investor_contribution=None, evidence_kind="named_investment",
                             note=note or "Výše kola není příspěvkem investora; oznámení není dokladem data vypořádání."))


def decision(iid, label, reason, sids):
    decisions.append(dict(candidate_id=iid, prediction=label, reason=reason, source_ids=sids,
                          predicted_on=AS_OF, author="Codex", review_status="pending_human"))


source("credo-home", "https://www.credoventures.com/", "Credo Ventures", "Investment approach and Prague contact",
       "Pre-seed zakladatelé z CEE a diaspory; ticket 1–5 mil. USD; pražská kancelář; pojmenované investice ElevenLabs a UiPath.")
source("credo-cvca", "https://cvca.cz/en/credo-ventures-2/", "CVCA", "Credo Ventures member profile",
       "Asociační profil uvádí spravované fondy 170 mil. EUR, ticket 50 tis.–10 mil. EUR a IT/internet. Referenční datum částek chybí.", kind="association")
source("axoflow", "https://axoflow.com/blog/7m-to-improve-security-data-quality", "Axoflow", "$7M to improve security data quality",
       "Příjemce investice jmenuje Credo Ventures mezi investory seed kola 7 mil. USD.", "2025-01-21", "portfolio_company")
investor("credo", "Credo Ventures", "https://www.credoventures.com/", "credo-home", "Karlovo náměstí 10, Praha",
         "Bez pevné sektorové teze; technologičtí zakladatelé", "pre-seed", "CEE a globální diaspora",
         dict(min=1000000, max=5000000, currency="USD", basis="check"))
capital("credo", "manager_aum", 170000000, "EUR", "credo-cvca", "manager", "Nedatovaný asociační profil; nepovažovat za aktuální AUM.", "historical_unconfirmed")
claim("credo", "ticket", dict(min=50000, max=10000000, currency="EUR", basis="preferred_investment"), "credo-cvca",
      "Alternativní nedatovaný asociační údaj. Pro přehled má přednost vlastní web s aktuálně publikovaným mandátem.", "historical_unconfirmed")
transaction("credo", "Axoflow", "axoflow", "2025-01-21", "day", round_amount=dict(amount=7000000, currency="USD", composition="seed_round"))

source("depo-home", "https://depoventures.com/", "DEPO Ventures", "Investment strategy",
       "Inception/pre-seed, defence, space, fintech, Industry 4.0 a energie; ticket 250–500 tis. EUR; 9 mil. EUR proinvestováno.")
source("depo-tapaya", "https://depoventures.com/latest/turning-any-smartphone-into-a-payment-terminal-czech-fintech-tapaya-has-raised-eur-1-million", "DEPO Ventures", "Tapaya raises EUR 1 million",
       "DEPO a Passion Capital vedly pre-seed kolo Tapaya ve výši 1 mil. EUR. Stránka obsahuje pražskou kontaktní adresu. Datum oznámení není v otevřeném textu.")
source("depo-cvca", "https://cvca.cz/en/depo-ventures-2/", "CVCA", "DEPO Ventures profile",
       "VC se sídlem/kontaktem v Praze, nedatovaný ticket 50–300 tis. EUR a spravované fondy 5,5 mil. EUR.", kind="association")
investor("depo", "DEPO Ventures", "https://depoventures.com/", "depo-home", None,
         "Defence; space; fintech; Industry 4.0; energie", "inception; pre-seed", "Evropa, CEE a diaspora",
         dict(min=250000, max=500000, currency="EUR", basis="check"))
next(c for c in claims if c['id'] == 'depo.czech_office.1').update(value="Plynární 10, Praha 7", source_id="depo-tapaya")
capital("depo", "invested_to_date", 9000000, "EUR", "depo-home", "organization", "Proinvestováno; není to AUM ani dostupný kapitál.")
capital("depo", "manager_aum", 5500000, "EUR", "depo-cvca", "manager", "Nedatovaný asociační údaj.", "historical_unconfirmed")
claim("depo", "ticket", dict(min=50000, max=300000, currency="EUR", basis="preferred_investment"), "depo-cvca", "Asociační profil se liší od vlastního webu; referenční datum neznámé.", "historical_unconfirmed")
transaction("depo", "Tapaya", "depo-tapaya", round_amount=dict(amount=1000000, currency="EUR", composition="pre_seed_round"), note="Účast doložena investorem; datum oznámení nenalezeno. Nedatovat podle copyrightu ani stáří crawl indexu.")

source("inibio-home", "https://www.inibio.eu/", "i&i Bio", "Strategy and dated portfolio",
       "Life sciences, léky, medtech, diagnostika a AI; early-stage; běžně 0,5–2 mil. EUR, business creation od 150 tis. EUR. KyDo Therapeutics v portfoliu s rokem 2025.")
source("inibio-cvca", "https://cvca.cz/en/biotech-investments/", "CVCA", "i&i Biotech Investments profile",
       "Pražská adresa Pobřežní 394/12; popis i&i Biotech Fund jako investora do biotechnologických spin-offů.", kind="association")
source("inibio-capital", "https://www.inibio.eu/news/experienced-businessmen-join-forces-with-excellent-science%2C-invest-%E2%82%AC2m-in-the-fund-at-the-iocb", "i&i Bio", "Experienced businessmen join forces with excellent science",
       "Text datovaný 30. 11. 2022 uvádí tehdejší kapitál přibližně 47 mil. EUR. Aktualizovaný boilerplate na téže stránce uvádí přes 53 mil. EUR bez vlastního data.", "2022-11-30")
investor("inibio", "i&i Biotech Fund", "https://www.inibio.eu/", "inibio-home", None,
         "Life sciences; drug discovery; medtech; diagnostika; AI ve zdravotnictví", "early-stage", "Evropa, zejména CEE",
         dict(min=500000, max=2000000, currency="EUR", basis="sweet_spot"), "Business creation od 150 000 EUR; není to dolní mez běžného sweet spot.")
next(c for c in claims if c['id'] == 'inibio.czech_office.1').update(value="Pobřežní 394/12, Praha 8", source_id="inibio-cvca")
capital("inibio", "fund_closed_size", 47000000, "EUR", "inibio-capital", "i&i Biotech Fund", "Historická částka z hlavního textu; přibližná, ne současný celkový kapitál.", "historical_unconfirmed", "2022-11-30", "approximate")
capital("inibio", "fund_reported_managed_capital", 53000000, "EUR", "inibio-capital", "i&i Biotech Fund", "Spodní hranice z nedatovaného boilerplate stejné stránky; nemá automaticky datum článku.", "undated_reference", bound="greater_than")
transaction("inibio", "KyDo Therapeutics", "inibio-home", "2025", "year", "portfolio_investment_year", note="Oficiální portfolio přiřazuje rok 2025; přesný den a výše příspěvku nezjištěny.")

source("inven-home", "https://www.invencapital.cz/", "INVEN Capital", "Investment focus and office",
       "Climate tech, Evropa a Izrael, ticket 2–30 mil. EUR; kontakt Praha 4; na webu propojené portfolio a zpráva o Andercore.")
source("inven-eib", "https://www.eib.org/en/press/all/2023-047-expanding-strategic-partnership-eib-supports-investments-in-climate-friendly-startups-providing-a-further-eur50-million-to-the-czech-fund-inven-capital", "European Investment Bank", "Expanding strategic partnership with Inven Capital",
       "EIB uvádí celkové AUM přes 500 mil. EUR a přes 260 mil. EUR pro nové investice v období 2022–2027; neaktuální historický údaj.", kind="institution")
source("inven-cvca", "https://cvca.cz/en/inven-capital-2/", "CVCA", "INVEN Capital member profile",
       "Cleantech investice v pozdějším růstu, ticket 2–30 mil. EUR, pražská adresa a pojmenované portfolio.", kind="association")
source("andercore", "https://www.andercore.com/press/andercore-secures-40m-series-b-for-ai-driven-industrial-trade-platform", "Andercore", "Andercore secures $40m Series B",
       "Příjemce potvrzuje účast Inven Capital v kole 40 mil. USD složeném z equity a debt.", "2026-02-11", "portfolio_company")
investor("inven", "INVEN Capital", "https://www.invencapital.cz/", "inven-home", "Pod Křížkem 1773/2, Praha 4",
         "Climate tech", "growth", "Evropa a Izrael", dict(min=2000000, max=30000000, currency="EUR", basis="ticket"))
next(c for c in claims if c['id'] == 'inven.stage.1').update(source_id="inven-cvca")
capital("inven", "manager_aum", 500000000, "EUR", "inven-eib", "manager", "Historické AUM z tiskové zprávy označené 2023 v URL; dnešní AUM neověřeno.", "historical_unconfirmed", bound="greater_than")
transaction("inven", "Andercore", "andercore", "2026-02-11", "day", round_amount=dict(amount=40000000, currency="USD", composition="equity_and_debt"), corroborating=["inven-home"])

source("kaya-home", "https://www.kaya.vc/", "KAYA", "Fund, ticket and offices",
       "Pre-seed/seed zakladatelé z CEE; ticket 1–3 mil. USD; AUM 500 mil. USD; současný fond 85 mil. USD; kancelář Thámova, Praha.")
source("kaya-news", "https://newsletter.kaya.vc/", "KAYA", "CEEfarers September 2025",
       "Vlastní newsletter potvrzuje investici do E2B a další nové investice; zveřejněn 30. 9. 2025.", "2025-09-30")
source("e2b", "https://www.insightpartners.com/ideas/e2b-raises-a-21m-series-a-to-offer-cloud-for-ai-agents-to-fortune-100/?ref=newsletter.kaya.vc", "Insight Partners", "E2B Raises a $21M Series A",
       "Vedoucí investor kola jmenuje KAYA mezi účastníky Series A E2B ve výši 21 mil. USD.", "2025-07-28", "coinvestor")
investor("kaya", "KAYA VC", "https://www.kaya.vc/", "kaya-home", "Thámova 183/11, Praha 8",
         "Digitální, fyzická a spotřebitelská ekonomika; široké technologické zaměření", "pre-seed; seed", "CEE zakladatelé",
         dict(min=1000000, max=3000000, currency="USD", basis="ticket"))
capital("kaya", "manager_aum", 500000000, "USD", "kaya-home", "manager", "Vlastní aktuálně dostupný web, bez referenčního data ocenění; self-reported, nikoli auditované.")
next(c for c in claims if c['id'] == 'kaya.total_investment_capital.1').update(value=dict(metric="manager_aum", amount=500000000, currency="USD", bound="exact"), status="supported", note="Self-reported AUM na webu; datum ocenění není uvedeno.")
funds.append(dict(id="kaya-current", investor_id="kaya", name="Current Fund (web neuvádí právní název)", source_id="kaya-home"))
capital("kaya", "fund_reported_size", 85000000, "USD", "kaya-home", "fund:kaya-current", "Web říká Current Fund; bez důkazu typu closing neoznačovat final close.")
transaction("kaya", "E2B", "e2b", "2025-07-28", "day", round_amount=dict(amount=21000000, currency="USD", composition="series_a"), corroborating=["kaya-news"])

source("nation1-home", "https://n1.rocks/", "N1 / Nation 1", "Investment approach and offices",
       "Spravuje 60 mil. USD ve dvou fondech pro AI a zdravotnictví; první investice 100 tis.–1 mil. USD; Praha Národní 135/14; testimonial Snuggs uvádí vstup N1 v pre-seed v roce 2019.")
source("nation1-legal", "https://n1.rocks/disclosure", "Nation 1", "SFDR disclosure",
       "Právní názvy Nation 1 GP a Nation 1 GP II propojují značku N1 s původním názvem. Fondy domicilované v Lucembursku.")
investor("nation1", "Nation 1 / N1", "https://n1.rocks/", "nation1-home", "Národní 135/14, Praha 1",
         "AI; healthtech; frontier tech", "early-stage; od založení", "Evropa a USA",
         dict(min=100000, max=1000000, currency="USD", basis="typical_first_investment"))
capital("nation1", "manager_aum", 60000000, "USD", "nation1-home", "manager", "Self-reported spravovaný kapitál přes dva fondy; bez data ocenění.")
next(c for c in claims if c['id'] == 'nation1.total_investment_capital.1').update(value=dict(metric="manager_aum", amount=60000000, currency="USD", bound="exact"), status="supported", note="Self-reported across two funds; referenční datum neuvedeno.")
transaction("nation1", "Snuggs", "nation1-home", "2019", "year", "portfolio_investment_year", note="Testimonial zakladatelky na webu N1 popisuje pre-seed vstup v roce 2019; nejde o ověření současné aktivity.")

source("tensor-home", "https://tensor.ventures/", "Tensor Ventures", "Thesis and Czech contact",
       "Seed a Series A, AI, quantum, computational biotech a sustainable tech; globální síť; český kontakt v Karlíně, právní sídlo v Lucembursku.")
source("tensor-cvca", "https://cvca.cz/en/tensor-ventures/", "CVCA", "Tensor Ventures profile",
       "Ticket 250 tis.–1 mil. EUR, spravovaný kapitál 20 mil. EUR, geografie EU/USA; referenční datum hodnot chybí.", kind="association")
source("tensor-news", "https://blog.tensor.ventures/p/tensor-ventures-decoded-newsletter-fb6", "Tensor Ventures", "Decoded December 2025",
       "Tensor vedl závěrečnou tranši 1,1 mil. EUR v seed kole Repsense o celkových 2 mil. EUR. Vložená zpráva datovaná 16. 12. 2025.", "2025-12-23")
investor("tensor", "Tensor Ventures", "https://tensor.ventures/", "tensor-home", "Pernerova 697/35, Praha 8",
         "Deep tech; AI; quantum; computational biotech; sustainable tech", "seed; Series A", None, None)
next(c for c in claims if c['id'] == 'tensor.geography.1').update(value="EU a USA", source_id="tensor-cvca")
next(c for c in claims if c['id'] == 'tensor.ticket.1').update(value=dict(min=250000, max=1000000, currency="EUR", basis="preferred_investment"), source_id="tensor-cvca", status="historical_unconfirmed", note="Nedatovaný asociační profil; současné rozpětí neověřeno.")
capital("tensor", "manager_aum", 20000000, "EUR", "tensor-cvca", "manager", "Nedatovaný údaj; nevydávat za současný celkový kapitál.", "historical_unconfirmed")
transaction("tensor", "Repsense", "tensor-news", "2025-12-16", "day", "embedded_announcement", round_amount=dict(amount=2000000, currency="EUR", composition="total_seed_round"), note="1,1 mil. EUR je velikost závěrečné tranše s více investory, nikoli osobní ticket Tensoru.")

source("tilia-home", "https://tilia.vc/", "Tilia Impact Ventures", "Mandate, ticket, portfolio and contact",
       "Early-stage impact VC z CEE; equity/convertible debt; první ticket 0,3–1,2 mil. EUR; Praha. Hodnota unlocked for impact není doložené AUM.")
source("tilia-sfdr", "https://tilia.vc/sfdr/", "Tilia Impact Ventures", "Sustainability disclosures Fund II",
       "Fond II spravuje Tilia Impact Ventures II GP; venture kapitál pro seed/startup/Series A a environmentální a sociální dopad.")
source("letsdata", "https://letsdata.net/resources/newsroom/letsdata-1-6m-investment", "LetsData", "LetsData Secures $1.6M",
       "Příjemce investice jmenuje Tilia Impact Ventures mezi účastníky kola 1,6 mil. USD.", "2025-01-15", "portfolio_company")
investor("tilia", "Tilia Impact Ventures", "https://tilia.vc/", "tilia-home", "Drtinova 557/10, Praha 5",
         "Sektorově agnostický impact; environmentální a sociální dopad", "early-stage", "CEE+",
         dict(min=300000, max=1200000, currency="EUR", basis="initial_ticket"))
funds.append(dict(id="tilia-ii", investor_id="tilia", name="Tilia Impact Ventures Fund II", source_id="tilia-sfdr"))
transaction("tilia", "LetsData", "letsdata", "2025-01-15", "day", round_amount=dict(amount=1600000, currency="USD", composition="funding_round"), corroborating=["tilia-home"])

source("purple-home", "https://www.purple-ventures.com/", "Purple Ventures", "Investment strategy, portfolio and media digest",
       "Pre-seed/seed technologické firmy s prvními tržbami, CEE+; první ticket 250–400 tis. EUR. Portfolio Fether Labs: investováno 2026. Mediální souhrn uvádí přes 700 mil. Kč získaných ve fondu II.")
source("purple-linkedin", "https://cz.linkedin.com/company/purple-ventures", "Purple Ventures (company profile)", "Purple Ventures LinkedIn company profile",
       "Firemní profil propojuje vlastní doménu, ústředí Brno a primární lokalitu Masarykova 26. Uvádí první ticket 250–500 tis. EUR, což se liší od 250–400 tis. EUR na vlastním webu. Oba mandáty jsou bez referenčního data.", kind="investor_social_profile")
investor("purple", "Purple Ventures", "https://www.purple-ventures.com/", "purple-home", "Masarykova 26, Brno; firemní kontaktní adresa v patičce webu",
         "Purpose-driven technologické inovace", "pre-seed; seed", "CEE+",
         dict(min=250000, max=400000, currency="EUR", basis="initial_ticket"))
next(c for c in claims if c['id'] == 'purple.czech_office.1').update(source_id="purple-linkedin", note="Primární lokalita a ústředí na firemním profilu odpovídají adrese na webu; není nezávislou návštěvou kanceláře.")
next(c for c in claims if c['id'] == 'purple.ticket.1').update(status="partial", note="Vlastní web uvádí 250–400 tis. EUR, firemní LinkedIn 250–500 tis. EUR. Data mandátů neznámá; spor neřešíme odhadem. Přehled ukazuje web, nikoli sjednocené současné rozpětí.")
claim("purple", "ticket", dict(min=250000, max=500000, currency="EUR", basis="initial_ticket"), "purple-linkedin", "Alternativní self-reported rozsah; rozpor s webem zůstává otevřený.", "undated_reference")
transaction("purple", "Fether Labs", "purple-home", "2026", "year", "portfolio_investment_year", note="Portfolio výslovně uvádí PV 2 | Invested in 2026; přesný den není z tohoto zdroje znám.")
funds.append(dict(id="purple-ii", investor_id="purple", name="Purple Ventures Fund II", source_id="purple-home"))
capital("purple", "fund_reported_raised_capital", 700000000, "CZK", "purple-home", "fund:purple-ii", "Spodní hranice v souhrnu výsledků 2025 na vlastním webu; bez vlastního data zprávy a bez doložení final close.", "undated_reference", bound="greater_than")

source("jt-home", "https://www.jtventures.cz/", "J&T Ventures", "Investment criteria and contact",
       "Praha Karlín; CEE, SEE, Baltics; pre-seed až Series A; 300 tis.–3 mil. EUR; sektorově agnostické.")
source("jt-approach", "https://www.jtventures.cz/pristup", "J&T Ventures", "Approach and FAQ",
       "Equity a konvertibilní půjčky; fond se výslovně neoznačuje za corporate VC J&T banky, která je institucionálním investorem.")
source("grid", "https://www.jtventures.cz/blog/grid-online-prinasi-lepe-zaplacene-kuryry-levnejsi-dopravu-i-mene-aut-ve-mestech-rika-ondrej-kratky", "J&T Ventures", "Interview with grid.online founder",
       "Investice 1,5 mil. EUR od Reflex Capital, J&T Ventures a Grid Invest. Datum přímého článku v otevřeném textu chybí.")
source("jt-blog", "https://www.jtventures.cz/blog", "J&T Ventures", "Blog index",
       "Index uvádí u rozhovoru grid.online datum 20. 4. 2025; neověřené datum transakce samotné.")
investor("jt", "J&T Ventures", "https://www.jtventures.cz/", "jt-home", "Sokolovská 700/113a, Praha 8",
         "Sektorově agnostické; B2B, B2C, marketplaces", "pre-seed až Series A", "CEE; SEE; Baltics",
         dict(min=300000, max=3000000, currency="EUR", basis="investment"))
transaction("jt", "grid.online", "grid", "2025-04-20", "day", "article_index_date", round_amount=dict(amount=1500000, currency="EUR", composition="round"), corroborating=["jt-blog"], note="Datum převzato z indexu J&T blogu, nikoli z transakce. Investor i příjemce popsáni v rozhovoru.")

source("reflex-home", "https://www.reflexcapital.com/", "Reflex Capital", "Investments and Prague office",
       "Vlastní web ukazuje investice do technologických firem, pražskou adresu a 150 mil. EUR historicky investováno; nejde o AUM.")
source("reflex-portfolio", "https://www.reflexcapital.com/portfolio/", "Reflex Capital", "Current investments",
       "Vlastní portfolio dokládá konkrétní firmy; samotný seznam nedokládá dnešní běžný ticket ani celkové AUM.")
investor("reflex", "Reflex Capital", "https://www.reflexcapital.com/", "reflex-home", "Rašínovo nábřeží 2000/78, Praha 2",
         "Technologické firmy; mandát sektorů není na použité stránce formalizován", None, None, None,
         "Běžný ticket v použitých primárních zdrojích nenalezen; neodvozovat z velikosti kol.")
next(c for c in claims if c['id'] == 'reflex.sectors.1').update(status="partial", note="Portfolio ukazuje technologické firmy, ale explicitní sektorový mandát na použité stránce nenalezen.")
next(c for c in claims if c['id'] == 'reflex.stage.1').update(value="startup / venture; přesné fáze nezjištěny", source_id="grid", status="partial", note="Venture klasifikace z charakteru portfolia a investice do startupu grid.online; nejde o explicitní mandát fondu.")
next(c for c in claims if c['id'] == 'reflex.geography.1').update(value=None, status="not_found", note="Pražská a americká kancelář samy o sobě nedokládají cílovou investiční geografii.")
next(c for c in claims if c['id'] == 'reflex.investor_type.1').update(source_id="grid", status="inferred", note="Klasifikace podle startupového portfolia a doložené investice grid.online, bez právního ověření.")
capital("reflex", "invested_to_date", 150000000, "EUR", "reflex-home", "organization", "Web uvádí invested; nesmí být prezentováno jako celkový investiční kapitál.")
transaction("reflex", "grid.online", "grid", "2025-04-20", "day", "article_index_date", round_amount=dict(amount=1500000, currency="EUR", composition="round"), corroborating=["jt-blog"], note="Účast potvrzena rozhovorem na webu spoluinvestora J&T. Datum je datum indexu článku, nikoli vypořádání.")

source("lighthouse-discovery", "https://czechstartups.gov.cz/investori_en/lighthouse-venture/", "CzechStartups / CzechInvest", "Lighthouse venture discovery profile",
       "More information směřuje na lighthouseventuresllc.com, nikoli na české lhv.vc. Automatické spojení podle jména by bylo chybné.", kind="discovery")
source("lighthouse-home", "https://lhv.vc/about-us/", "Lighthouse Ventures GP s.r.o.", "About Lighthouse Ventures",
       "Česká GP s IČO 07500912, Praha 6; early-stage venture, B2B software, fintech, AI; ticket 200 tis.–1 mil. EUR. Není prokázáno, že jde o entitu z discovery odkazu.")
decision("lighthouse", "needs_review", "Discovery profil odkazuje na jinou entitu. Český fond na lhv.vc existuje, ale nelze tiše zaměnit subjekt ze zmrazeného výběru. Vyžaduje lidské vyřešení identity nebo samostatný nový kandidát mimo metriky tohoto vzorku.", ["lighthouse-discovery", "lighthouse-home"])

source("genesis", "https://cvca.cz/en/genesis-capital-equity-s-r-o-2/", "CVCA", "Genesis Capital Equity",
       "Buyout, akvizice, růstový kapitál a konsolidace firem; nedokládá VC mandát pro tento úzký pilot.", kind="association")
source("arx", "https://cvca.cz/en/arx-equity-partners-2/", "CVCA", "ARX Equity Partners",
       "Akvizice, management buyout, expansion a sektorová konsolidace; částka 5–50 mil. EUR je velikost transakce, ne automaticky ticket.", kind="association")
source("akat", "https://cvca.cz/en/akat-cze/", "CVCA", "AKAT",
       "Asociace správců majetku a kolektivního investování, která zastupuje zájmy sektoru.", kind="association")
source("bdo", "https://cvca.cz/en/bdo-czech-republic-s-r-o-2/", "CVCA", "BDO Czech Republic",
       "Audit, daně, účetnictví a transakční poradenství; účast na obchodech jako poradce nedokládá investování.", kind="association")
source("fundlift", "https://czechstartups.gov.cz/investori_en/fundlift/", "CzechStartups / CzechInvest", "Fundlift",
       "Investiční crowdfunding propojující firmy a investory; samotná platforma není doloženým přímým VC.", kind="discovery")
source("startovac", "https://czechstartups.gov.cz/investori_en/startovac/", "CzechStartups / CzechInvest", "Startovač",
       "Platforma pro veřejné financování kreativních projektů, nikoli doklad přímého venture investora.", kind="discovery")
source("cvca-about", "https://cvca.cz/en/membership/", "CVCA", "Membership categories",
       "Asociace rozlišuje investující plné členy a přidružené poskytovatele služeb; členství není samo o sobě důkazem transakce.", kind="association")
source("startupstart", "https://czechstartups.gov.cz/investori_en/startupstart-cz/", "CzechStartups / CzechInvest", "Startupstart.cz",
       "Platforma propojuje startupy s investory; přímé investování platformy nedoloženo.", kind="discovery")
for iid, reason, sid in [
    ("genesis", "Skutečný PE investor, ale buyout/growth mandát je mimo VC pilot. Není odmítnut pro globální PE databázi.", "genesis"),
    ("arx", "Skutečný PE investor mimo VC pilot; akvizice a buyout nejsou důkazem VC mandátu.", "arx"),
    ("akat", "Asociace, nikoli přímý investor.", "akat"),
    ("bdo", "Poradenská společnost; transakce klientů nejsou její vlastní investice.", "bdo"),
    ("fundlift", "Crowdfundingová platforma; chybí důkaz přímého VC mandátu.", "fundlift"),
    ("startovac", "Crowdfunding kreativních projektů; není přímý VC investor.", "startovac"),
    ("cvca", "Oborová asociace zastupující investory; není sama fondem.", "cvca-about"),
    ("startupstart", "Zprostředkovatelská platforma; vlastní venture investice nedoložena.", "startupstart"),
]:
    decision(iid, "exclude", reason, [sid])

# Initial predictions remain frozen separately. Purple's address was found during
# the subsequent AI check in the footer of the same primary source.
for inv in investors:
    iid = inv["id"]
    sids = list(dict.fromkeys([c["source_id"] for c in claims if c["investor_id"] == iid] +
                             [t["source_id"] for t in transactions if t["investor_id"] == iid]))
    reason = "Investiční mandát, česká kancelář a pojmenovaná přímá investice doloženy; rozhodnutí AI čeká na lidskou kontrolu."
    if iid == "purple":
        reason += " Po první predikci nalezena adresa na webu a potvrzena firemním profilem s ústředím a primární lokalitou Brno; původní needs_review zachováno. Ticket má nevyřešený rozpor."
    decision(iid, "include", reason, sids)

dataset = dict(schema_version=1, as_of=AS_OF,
               provenance="Curated by Codex using opened public web pages; not human verified; no automated extraction accuracy claimed.",
               sources=sources, investors=investors, claims=claims, transactions=transactions, funds=funds, decisions=decisions)
(ROOT / "data" / "pilot.json").write_text(json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote pilot: {len(investors)} organizations, {len(sources)} sources, {len(claims)} claims")
