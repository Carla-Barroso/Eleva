# Eleva

Plataforma digital que conecta pessoas em situação de vulnerabilidade social a oportunidades de trabalho autônomo no Distrito Federal, com validação institucional, rastreabilidade e sistema de pagamento em escrow.

🔗 **[Ver projeto no ar](https://elevaprofissinais.vercel.app)**

---

## O problema

No Distrito Federal, programas públicos qualificam e instituições sociais acolhem. Mas nenhuma dessas iniciativas resolve o que acontece depois: a pessoa está pronta para trabalhar e não consegue entrar no mercado porque não tem rede de contatos, histórico verificável ou um canal confiável para ser contratada.

Do outro lado, quem precisa de um eletricista, diarista ou pintor depende de indicação de conhecido, sem nenhuma garantia real de qualidade ou segurança.

O Eleva nasceu para fechar essa lacuna: transformar qualificação institucional em acesso real ao mercado, gerando renda imediata para quem precisa e confiança para quem contrata.

---

## O que foi construído

- Cadastro de profissionais via instituições parceiras (ONGs, CRAS, programas públicos)
- Perfil verificável com certificações, histórico de serviços e avaliações rastreáveis
- Sistema de escrow: pagamento retido até confirmação bilateral de conclusão
- Rastreabilidade em 3 etapas: início, andamento e conclusão do serviço
- Chat de negociação entre cliente e profissional
- Painéis separados para cliente, profissional e instituição
- Repasse automático de 3% à instituição que cadastrou o profissional

---

## Stack

| Camada | Tecnologia | Hospedagem |
|---|---|---|
| Frontend | HTML5, CSS3, JavaScript (Vanilla) | Vercel |
| Backend | Python 3 + Flask | PythonAnywhere |
| Banco de dados | SQLite | PythonAnywhere |
| Integração | REST API + CORS | |

Frontend estático no Vercel para carregamento rápido via CDN. Backend Python no PythonAnywhere para processar as regras críticas de negócio: escrow, tokens de confirmação e repasse financeiro, executadas exclusivamente no servidor.

---

## Arquitetura

```
┌─────────────────────┐         ┌──────────────────────────┐
│   Vercel (Frontend) │  fetch  │ PythonAnywhere (Backend) │
│  HTML / CSS / JS    │ ──────► │   Flask API  +  SQLite   │
└─────────────────────┘ ◄────── └──────────────────────────┘
        CDN global                Regras de negócio + dados
```

---

## Documentação

O desenvolvimento do ELEVA envolveu pesquisa aplicada, modelagem estratégica e documentação técnica.

- 📊 [Benchmark e Análise Estratégica](docs/Benchmark_Estrategico_ELEVA.pdf)
- ⚙️ [Documentação Técnica](docs/Documentacao_Tecnica_ELEVA.pdf)
- 👥 [Personas e Pesquisa de Usuários](docs/Personas_ELEVA.pdf)

## Como rodar localmente

**Backend**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Sobe em `http://localhost:5000`.

**Frontend**
Abra qualquer `.html` no navegador ou use Live Server (VS Code).

> A constante `API_URL` nos arquivos JS aponta para produção. Para rodar local, altere para `http://localhost:5000`.

---

## Sobre o projeto

A ideia nasceu de vivências reais no Distrito Federal. Morando no Areal, região próxima a um albergue, e trabalhando no centro de Taguatinga, observei de perto a realidade de pessoas em situação de vulnerabilidade social e as dificuldades de reinserção no mercado de trabalho, mesmo após processos de acolhimento e qualificação.

Essa experiência despertou uma pergunta que acabou se transformando no ELEVA: como utilizar a tecnologia para ampliar o acesso a oportunidades reais de renda, promovendo inclusão produtiva e contribuindo para uma sociedade mais segura e justa?

O projeto foi concebido, pesquisado, modelado, documentado e desenvolvido integralmente por mim durante a Residência Tecnológica UCB × Porto Digital.

---

## Contato

[LinkedIn](http://www.linkedin.com/in/carla-barrosoo)
