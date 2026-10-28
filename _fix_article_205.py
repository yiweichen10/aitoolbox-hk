import io
p='_append_article_205.py'
s=open(p,encoding='utf-8').read()
pairs=[
("Postman's 2025 State of the API survey put a hard number on a fear most teams had not budgeted for: 51% of developers worry about AI agents making unauthorized or excessive calls to their APIs \u2014 on top of endpoint counts that keep growing faster than the teams maintaining them. The client you use to poke at those endpoints has quietly become infrastructure, and in 2026 four API testing tools divide almost the entire desktop market between them: Postman, Insomnia, Bruno, and Hoppscotch.",
 "Postman's 2025 State of the API survey put a hard number on a fear most teams had not budgeted for: 51% of developers worry about AI agents making unauthorized or excessive calls to their APIs \u2014 on top of endpoint counts growing faster than headcount. The client you poke those endpoints with has quietly become infrastructure, and in 2026 four API testing tools divide almost the entire desktop market: Postman, Insomnia, Bruno, and Hoppscotch."),
("The pattern that holds across all of it: the tool matters less",
 "The pattern that holds: the tool matters less"),
("zero install, more than 80,000 GitHub stars",
 "zero install, 80,000+ GitHub stars"),
("That is why the pricing sections below read so differently",
 "That is why the pricing sections read so differently"),
("the old Basic and Professional team plans are gone, replaced by Free, Solo, Team, and Enterprise, with annual billing saving up to 25% and monthly rates no longer published on the pricing page.",
 "the old Basic and Professional plans are gone, replaced by Free, Solo, Team, and Enterprise, with annual billing saving up to 25% and monthly rates no longer published."),
("(the page shows 50 to 100 depending on where you look)",
 "(the page shows 50 to 100 depending where you look)"),
("None of this is unreasonable, but model it: a six-developer team on Postman Team pays $114 a month before any add-on, and that number is the honest baseline for the comparisons below.",
 "None of this is unreasonable, but model it: six developers on Postman Team pay $114 a month before add-ons \u2014 the honest baseline for the comparisons below."),
("Teams that don't want collections reviewed like code will find Bruno's workflow odd; teams that already live in Git wonder",
 "Teams that don't want collections reviewed like code will find the workflow odd; teams that live in Git wonder"),
("for up to 3 users \u2014 that is the free collaboration ceiling",
 "for up to 3 users \u2014 the free collaboration ceiling"),
("unlimited users, unlimited organizations, RBAC, and 10,000 mock requests",
 "unlimited users and organizations, RBAC, and 10,000 mock requests"),
("and HashiCorp \u2014 genuinely useful when your test secrets already live in one.",
 "and HashiCorp \u2014 useful when your test secrets already live in one."),
("and a collection runner \u2014 no account required for the core web app.",
 "and a collection runner \u2014 no account required."),
("adds SSO, audit logs, and admin controls for organizations that must keep the tooling inside their own perimeter",
 "adds SSO, audit logs, and admin controls for organizations that must keep tooling inside their own perimeter"),
("the ecosystem, mock servers, monitors, and documentation generators are years ahead, and the free tier covers a solo developer indefinitely.",
 "the ecosystem, mock servers, monitors, and documentation generators are years ahead."),
("Three integration notes from experience. First, testing authenticated endpoints is half the job, and token lifecycles, SSO flows, and service credentials deserve the same rigor as the requests themselves",
 "Three integration notes. First, testing authenticated endpoints is half the job, and token lifecycles, SSO flows, and service credentials deserve the same rigor as the requests"),
("covers the tools built for that job",
 "covers tools built for that job"),
("there is no seat meter and no cloud service to pay for, because collaboration happens through your own Git infrastructure",
 "there is no seat meter and no cloud service to pay for, since collaboration happens through your own Git infrastructure"),
("the largest integration catalog \u2014 if any of those matter, pay for it.",
 "the largest integration catalog \u2014 pay for it if any of those matter."),
]
ok=0
for old,new in pairs:
    if old not in s:
        print('NOT FOUND:',old[:70]); continue
    s=s.replace(old,new,1); ok+=1
open(p,'w',encoding='utf-8').write(s)
print('applied',ok,'of',len(pairs))
