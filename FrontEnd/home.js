document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');

    if (searchInput && searchBtn) {
        
        // DICIONÁRIO SEMÂNTICO DE CONTEXTO DO ELEVA
        const dicionarioEleva = {
            // Mapeamentos diretos para a categoria "Serviços de Limpeza"
            'limpeza': { tipo: 'cat', valor: 'Serviços de Limpeza' },
            'faxina': { tipo: 'cat', valor: 'Serviços de Limpeza' },
            'diarista': { tipo: 'cat', valor: 'Serviços de Limpeza' },
            'faxineira': { tipo: 'cat', valor: 'Serviços de Limpeza' },
            'passadeira': { tipo: 'cat', valor: 'Serviços de Limpeza' },
            
            // Mapeamentos para "Pintura"
            'pintor': { tipo: 'cat', valor: 'Pintura' },
            'pintura': { tipo: 'cat', valor: 'Pintura' },
            'grafiato': { tipo: 'cat', valor: 'Pintura' },
            'textura': { tipo: 'cat', valor: 'Pintura' },
            
            // Mapeamentos para "Serviços Elétricos"
            'eletrica': { tipo: 'cat', valor: 'Serviços Elétricos' },
            'eletricista': { tipo: 'cat', valor: 'Serviços Elétricos' },
            'fiacao': { tipo: 'cat', valor: 'Serviços Elétricos' },
            'curto': { tipo: 'cat', valor: 'Serviços Elétricos' },
            'tomada': { tipo: 'cat', valor: 'Serviços Elétricos' },
            'luz': { tipo: 'cat', valor: 'Serviços Elétricos' },
            
            // Mapeamentos para "Serviços Hidráulicos"
            'encanador': { tipo: 'cat', valor: 'Serviços Hidráulicos' },
            'hidraulica': { tipo: 'cat', valor: 'Serviços Hidráulicos' },
            'vazamento': { tipo: 'cat', valor: 'Serviços Hidráulicos' },
            'bombeiro': { tipo: 'cat', valor: 'Serviços Hidráulicos' },
            'chuveiro': { tipo: 'cat', valor: 'Serviços Hidráulicos' },
            'torneira': { tipo: 'cat', valor: 'Serviços Hidráulicos' },
            'agua': { tipo: 'cat', valor: 'Serviços Hidráulicos' },
            
            // Mapeamentos para "Serviços de Ar-condicionado"
            'ar': { tipo: 'cat', valor: 'Serviços de Ar-condicionado' },
            'condicionado': { tipo: 'cat', valor: 'Serviços de Ar-condicionado' },
            'split': { tipo: 'cat', valor: 'Serviços de Ar-condicionado' },
            'refrigeracao': { tipo: 'cat', valor: 'Serviços de Ar-condicionado' },

            // Mapeamentos para "Pequenos Reparos"
            'reparo': { tipo: 'cat', valor: 'Pequenos Reparos' },
            'marcenaria': { tipo: 'cat', valor: 'Pequenos Reparos' },
            'marceneiro': { tipo: 'cat', valor: 'Pequenos Reparos' },
            'conserto': { tipo: 'cat', valor: 'Pequenos Reparos' },
            'ajuste': { tipo: 'cat', valor: 'Pequenos Reparos' },

            // Mapeamentos para "Fretes"
            'mudanca': { tipo: 'cat', valor: 'Fretes' },
            'frete': { tipo: 'cat', valor: 'Fretes' },
            'transporte': { tipo: 'cat', valor: 'Fretes' },

            // Mapeamentos para "Montagem de Móveis"
            'montagem': { tipo: 'cat', valor: 'Montagem de Móveis' },
            'montador': { tipo: 'cat', valor: 'Montagem de Móveis' },
            'armario': { tipo: 'cat', valor: 'Montagem de Móveis' },
            'moveis': { tipo: 'cat', valor: 'Montagem de Móveis' },

            // Mapeamentos para "Serviços de Piso"
            'piso': { tipo: 'cat', valor: 'Serviços de Piso' },
            'porcelanato': { tipo: 'cat', valor: 'Serviços de Piso' },
            'ceramica': { tipo: 'cat', valor: 'Serviços de Piso' },
            'revestimento': { tipo: 'cat', valor: 'Serviços de Piso' },

            // Mapeamentos para "Instalações"
            'instalacao': { tipo: 'cat', valor: 'Instalações' },
            'instalador': { tipo: 'cat', valor: 'Instalações' },
            'suporte': { tipo: 'cat', valor: 'Instalações' },

            // Mapeamentos para "Decoração"
            'decoracao': { tipo: 'cat', valor: 'Decoração' },
            'organizer': { tipo: 'cat', valor: 'Decoração' },
            
            // PALAVRAS GENÉRICAS ACEITÁVEIS (Tratamento especial)
            'casa': { tipo: 'geral', valor: '' },
            'apartamento': { tipo: 'geral', valor: '' },
            'condominio': { tipo: 'geral', valor: '' },
            'reforma': { tipo: 'geral', valor: '' },
            'servico': { tipo: 'geral', valor: '' },
            'geral': { tipo: 'geral', valor: '' },
            
            // Regiões geográficas cadastradas do Distrito Federal
            'ceilandia': { tipo: 'texto', valor: 'Ceilândia' },
            'samambaia': { tipo: 'texto', valor: 'Samambaia' },
            'taguatinga': { tipo: 'texto', valor: 'Taguatinga' },
            'guara': { tipo: 'texto', valor: 'Guará' },
            'planaltina': { tipo: 'texto', valor: 'Planaltina' },
            'sol': { tipo: 'texto', valor: 'Sol Nascente' },
            'estrutural': { tipo: 'texto', valor: 'Estrutural' }
        };

        const executarBuscaInteligente = () => {
            const termoOriginal = searchInput.value.trim();
            
            if (!termoOriginal) {
                alert("Por favor, digite o que você precisa resolver hoje antes de pesquisar!");
                return;
            }

            // NORMALIZAÇÃO: Caixa baixa, remove acentos e caracteres especiais para evitar falhas de digitação
            const termoNormalizado = termoOriginal
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "")
                .replace(/[^a-z0-9\s]/g, "");

            // Separa a frase digitada em palavras
            const palavras = termoNormalizado.split(/\s+/);
            
            let urlDestino = null;
            let encontrouFiltro = false;

            // Percorre cada palavra digitada pelo cliente procurando no dicionário
            for (const palavra of palavras) {
                if (dicionarioEleva[palavra]) {
                    encontrouFiltro = true;
                    const correspondencia = dicionarioEleva[palavra];

                    if (correspondencia.tipo === 'cat') {
                        // Se digitou sinônimos (ex: "faxina"), redireciona para a categoria exata da API
                        urlDestino = `pesquisa.html?cat=${encodeURIComponent(correspondencia.valor)}`;
                        break; // Prioridade total para categorias
                    } else if (correspondencia.tipo === 'texto') {
                        // Se digitou região (ex: "Ceilândia"), busca por texto na API
                        urlDestino = `pesquisa.html?q=${encodeURIComponent(correspondencia.valor)}`;
                    } else if (correspondencia.tipo === 'geral') {
                        // Se for um termo genérico aceitável (ex: "casa" ou "limpeza"), abre a listagem expandida completa
                        urlDestino = `pesquisa.html`;
                    }
                }
            }

            // Tomada de Decisão do Mecanismo
            if (encontrouFiltro && urlDestino) {
                window.location.href = urlDestino;
            } else {
                // Se digitar coisas fora do escopo (ex: "pizza", "advogado", "sapato", "abracadabra")
                alert(`O Eleva é focado em infraestrutura de manutenção residencial, comercial e serviços urbanos do dia a dia.\n\nNão encontramos correspondência técnica para "${termoOriginal}".\n\nTente pesquisar por termos como: Faxina, Pintor, Eletricista, Vazamento ou digite sua região (ex: Ceilândia).`);
            }
        };

        // Vincula as ações do usuário sem código inline no HTML
        searchBtn.addEventListener('click', executarBuscaInteligente);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') executarBuscaInteligente();
        });
    }
});