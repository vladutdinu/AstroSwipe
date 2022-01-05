ASTROSWIPE
=====
Disciplina: ISW
----

Membrii+Roluri:
----

- Dinu Ionut Vladut:PM+DEV

- Purcariu Vladut Ionel:DEV

- Popa Lorena:Tester+Mobile DEV

- Zidaru Marian George:DOC

Tehnologii necesare
====

Docker:
----
* Se acceseaza urmatorul link : https://www.docker.com/get-started si se descarca si instaleaza "Docker".
* Se instaleaza urmatorul pachet: https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package 
* Se porneste aplicatia "Docker Desktop".


Rulare aplicatie:
====

- Se cloneaza repository-ul prin comanda `git clone https://github.com/VladutDinu/AstroSwipe.git`.
- Se intra in directorul "frontend" si se ruleaza comanda `docker build -t isw_frontend .`
- Se intra in directorul "backend" si se ruleaza comanda `docker build -t isw_backend .`
- Se intra in directorul "dev-ops" si se ruleaza comanda `docker-compose up -d`.
- Se asteapta 2 minute si apoi se acceseaza link-ul "localhost:5000".

Diagrame:
====
![Diagrama frontend](_frontend.png)
![Diagrama backend](Backend-flow.drawio.png)