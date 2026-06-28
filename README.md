# Eleva

Plataforma digital que conecta pessoas em situação de vulnerabilidade social a oportunidades de trabalho autônomo no Distrito Federal, com validação institucional, rastreabilidade e sistema de pagamento em escrow.

🔗 **[Ver projeto no ar](https://elevaprofissinais.vercel.app)**

---

## O problema

No Distrito Federal, o governo qualifica e as ONGs acolhem. Mas nenhuma dessas iniciativas resolve o que acontece depois: a pessoa está pronta para trabalhar e não consegue entrar no mercado porque não tem rede de contatos, histórico verificável ou um canal confiável para ser contratada.

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

Frontend estático no Vercel para carregamento rápido via CDN. Backend Python no PythonAnywhere para processar as regras críticas de negócio: escrow, tokens de confirmação e repasse financeiro, fora do alcance do cliente.

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

Idealizado e desenvolvido por **Carla Barroso**, estudante de Análise e Desenvolvimento de Sistemas na UCB, Residência Tecnológica Porto Digital, 2026.

A ideia nasceu de vivências reais no Distrito Federal. Morando no Areal, região onde havia um albergue, e trabalhando no centro de Taguatinga, observei de perto a realidade de pessoas em situação de vulnerabilidade e a dificuldade de reinserção no mercado de trabalho. Isso gerou uma pergunta que virou projeto: como transformar a vida de alguém através do trabalho, dando acesso a oportunidades reais de renda e contribuindo para uma sociedade mais segura e justa?

Todo o código, arquitetura, identidade visual e pesquisa de contexto foram desenvolvidos por mim.

---

## Contato

[LinkedIn](www.linkedin.com/in/carla-barrosoo) 