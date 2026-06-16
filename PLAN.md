Você é um desenvolvedor Python sênior, com experiência em ferramentas CLI,
testes de carga, automação web, aplicações assíncronas e
monitoramento de sistemas.

Quero que você implemente um projeto chamado `boca-stress`.

# Objetivo

`boca-stress` é uma ferramenta de linha de comando para realizar testes
controlados de carga em uma instalação do BOCA Online Judge.

A ferramenta deve simular equipes acessando o BOCA, submetendo soluções e
consultando o status das submissões. O objetivo é ajudar administradores de
competições a avaliar se a infraestrutura do BOCA, do banco de dados e do
autojudge suporta a carga esperada durante uma competição. Você deve usar a pasta boca-master como referência ao longo de todo o desenvolvimento. Esta é a pasta literal do site, atualmente deployed em https://boca2.ic.unicamp.br/boca. Todas suas requisicoes devem ser coerentes com a arquitetura e implementacao real do site.

# Stack obrigatória

Use:

- Python 3.12+
- Rich
- Typer para a CLI
- Pydantic para validação de configuração
- pytest para testes
- ruff para lint/format
- mypy para checagem de tipos, se viável

Não implemente tudo em um único arquivo. Crie uma arquitetura modular.

# Arquitetura sugerida

Use uma estrutura semelhante a esta:

```text
boca_stress/
├── __init__.py
├── cli.py
├── config.py
├── models.py
├── simulator.py
├── agents.py
├── backends/
│   ├── __init__.py
│   ├── base.py
│   └── http.py
├── boca/
│   ├── __init__.py
│   ├── admin.py
│   ├── team.py
│   └── parser.py
├── metrics/
│   ├── __init__.py
│   ├── collector.py
│   ├── postgres.py
│   ├── ssh.py
│   └── docker.py
├── report.py
└── tui.py

tests/
├── test_config.py
├── test_solutions_parser.py
├── test_models.py
└── test_simulator.py
```

# Comandos da CLI

Implemente os comandos:

```bash
boca-stress setup
boca-stress run
boca-stress --version
boca-stress --help
```

## Comando `setup`

O comando `setup` deve preparar uma competição de teste.

Parâmetros desejados:

```bash
boca-stress setup \
  --url http://192.168.15.10/boca \
  --admin-user admin \
  --admin-pass boca \
  --problems-dir problems/ \
  --teams 50 
```

os problemas atualmente estão na pasta problems, garanta que estao na pasta e estrutura correta.

Responsabilidades:

- Validar acesso ao BOCA.
- Logar como administrador.
- Cadastrar problemas `.zip` encontrados em `--problems-dir`.
- Criar times de teste, por exemplo `team001`, `team002`, ..., `team050`.


## Comando `run`

O comando `run` executa a simulação.

Exemplo:

```bash
boca-stress run \
  --url http://192.168.15.10/boca \
  --teams 80 \
  --max-think-secs 90 \
  --solutions-dir solutions/ \
  --status-prob 0.25 \
  --simulation-time-mins 120 \
  --seed 123 
```

Parâmetros:

```text
--url
    URL da instalação do BOCA.

--teams
    Número de times simulados.

--max-think-secs
    Tempo máximo entre ações de um time.

--solutions-dir
    Diretório com soluções que serão submetidas.

--status-prob
    Probabilidade de consultar status em vez de submeter uma solução.

--simulation-time-mins
    Duração da simulação em minutos.

--seed
    Semente do gerador aleatório para permitir experimentos reprodutíveis.
```

# Modelo de simulação

Cada time deve ser representado por um agente independente, por exemplo
`TeamAgent`.

Cada agente deve executar em paralelo aos demais. O número de times pode ser
maior que o número de cores da CPU, então use programação assíncrona com
`asyncio`.

Cada time repete o seguinte ciclo até o fim da simulação:

1. Sorteia um delay inteiro entre `1` e `max_think_secs`.
2. Aguarda esse delay.
3. Sorteia uma ação:
   - Com probabilidade `status_prob`, consulta a página de status.
   - Com probabilidade `1 - status_prob`, submete uma solução.
4. Registra o evento em log.
5. Repete.

# Ações dos agentes

## Ação `submit`

Para submeter uma solução:

1. Sortear um problema.
2. Sortear uma linguagem disponível para aquele problema.
3. Sortear uma solução disponível para aquele problema e linguagem.
4. Submeter a solução no BOCA.
5. Medir latência da submissão.
6. Registrar evento.

## Ação `view_status`

Para consultar status:

1. Abrir a página de status/runs.
2. Medir latência.
3. Registrar evento.

# Diretório de soluções

O diretório de soluções deve ter esta estrutura:

```text
solutions/
├── A/
│   ├── accepted.cpp
│   ├── wrong_answer.cpp
│   └── tle.py
├── B/
│   ├── accepted.py
│   └── slow.java
└── solutions.yml
```

O arquivo `solutions.yml` descreve problemas, linguagens e pesos.

Exemplo:

```yaml
problems:
  A:
    weight: 3
    solutions:
      - file: A/accepted.cpp
        language: C++
        weight: 5
      - file: A/wrong_answer.cpp
        language: C++
        weight: 2
      - file: A/tle.py
        language: Python
        weight: 1

  B:
    weight: 1
    solutions:
      - file: B/accepted.py
        language: Python
        weight: 4
      - file: B/slow.java
        language: Java
        weight: 1
```

Implemente um parser validado com Pydantic.

O parser deve:

- Verificar se `solutions.yml` existe.
- Verificar se todos os arquivos listados existem.
- Verificar se cada problema tem pelo menos uma solução.
- Verificar se pesos são positivos.
- Permitir sorteio ponderado de problemas e soluções.
- Permitir filtrar soluções por problema e linguagem.


# Métricas

Colete pelo menos:

- Número total de submissões.
- Número total de consultas de status.
- Número total de erros.
- Submissões por minuto.
- Consultas de status por minuto.
- Latência média de submissão.
- Latência média de status.
- Tamanho da fila do autojudge
- CPU, memória e carga do sistema

Para o MVP, implemente métricas internas e deixe a coleta remota modular.

# Monitoramento

Prepare a arquitetura para coletar métricas dos Servidores via:

- SSH.
- Docker.
- PostgreSQL.


```bash
--ssh-host boca-server
--ssh-user toca-admin
--ssh-pass password 
--docker-container boca
--db-host 
--db-user
--db-pass
```

Note que pode haver mais de um container e mais de um servidor para monitoramento.
Então é possível opções como

--docker-container boca-web --docker-container boca-judge

O mesmo vale para o ssh

# TUI com Rich

Durante a simulação, exiba uma interface ao vivo com Rich.

Ela deve mostrar:

- Barra de progresso da simulação.
- Tempo decorrido.
- Tempo total.
- Número de times.
- Total de submissões.
- Total de consultas de status.
- Total de erros.
- Submissões por minuto.
- Tamanho da fila do auto judge
- CPU, memória e carga, se disponível.
- Últimas ações dos agentes.

Exemplo visual:

```text
BOCA Stress Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tempo: 00:42:15 / 02:00:00    Times: 80    Backend: browser

Submissões: 1240    Status views: 320    Erros: 3
Throughput: 28.4 sub/min    p95 submit: 912 ms    p95 status: 420 ms

CPU:  ███████████████░░░░  76%
Mem:  █████████░░░░░░░░░░  45%
Load: 8.2  7.9  6.4

Fila autojudge:
████████████░░░░░░░░░░░░ 62

Últimas ações:
16:15:30 Time 5 submeteu A em Python (tle.py)
16:15:35 Time 3 visualizou status
16:15:45 Time 1 submeteu B em C++ (accepted.cpp)
16:16:03 Time 5 visualizou status
```

Mas eu quero que vc use "bubble", tipo bubble tea. Ou seja, frames com cantos
arredondados.


# Reprodutibilidade

A opção `--seed` deve controlar as decisões aleatórias:

- Ordem dos delays.
- Escolha de ações.
- Escolha de problemas.
- Escolha de soluções.

Com a mesma seed e mesma configuração, a sequência lógica de ações deve ser
reprodutível, dentro do possível.


# README

Crie um `README.md` completo contendo:

- O que é o projeto.
- Instalação.
- Uso básico.
- Exemplos de comandos.
- Estrutura esperada de `problems/`.
- Estrutura esperada de `solutions/`.
- Exemplo de `solutions.yml`.
- Como executar testes.

# Qualidade do código

Exigências:

- Use type hints.
- Use dataclasses ou Pydantic models para entidades centrais.
- Evite funções gigantes.
- Separe regra de negócio, CLI, backend e TUI.
- Escreva testes unitários para parser de configuração e parser de soluções.
- Não quebre a execução inteira quando um time falhar.
- Use logging estruturado sempre que possível.
- Documente pontos em que o BOCA pode variar conforme a versão/configuração.

# Implementação incremental

Implemente em etapas.

## Etapa 1: esqueleto

- Criar pacote Python.
- Criar CLI com Typer.

## Etapa 2: 

- Implementar funcionalidade de `setup`.

## Etapa 3: simulação mínima

- Criar `TeamAgent`.
- Fazer login de time.
- Consultar página de status.

## Etapa 4: submissão

- Implementar submissão de arquivo.

## Etapa 4: TUI

- Criar painel ao vivo com Rich.

## Etapa 5:

- Criar README

Antes de escrever código, apresente um breve plano de implementação e depois
comece criando os arquivos do projeto.
