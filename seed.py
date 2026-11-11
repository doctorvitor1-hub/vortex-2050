import os
import re
from app import create_app, db
from app.models import Product

app = create_app()

EBOOKS_CATALOG = [
    # 1. INTELIGÊNCIA ARTIFICIAL & AUTOMAÇÃO (10 E-books)
    ("Agentes Autônomos de IA: Crie Sua Equipe Digital em 2026", "IA & Automação", 49.90, "Domine fluxos de agentes inteligentes que prospectam, atendem e operam negócios 24/7 sem intervenção humana."),
    ("Engenharia de Prompt Avançada: Arquitetura de Raciocínio", "IA & Automação", 39.90, "Saia do básico e aprenda estruturas lógicas usadas por engenheiros de elite para extrair respostas cirúrgicas de LLMs."),
    ("Micro-SaaS com IA: Do Zero ao Primeiro Dólar sem Programar", "IA & Automação", 47.90, "O mapa prático para validar, construir e monetizar ferramentas de nicho usando APIs modernas e ferramentas No-Code."),
    ("Estúdio Criativo IA: Vídeos, Avatares e Vozes Hiper-Realistas", "IA & Automação", 34.90, "Produza campanhas virais e canais inteiros utilizando síntese neural de imagem, vídeo e clonagem de voz."),
    ("IA nos Negócios Locais: Como Vender Automação para Empresas", "IA & Automação", 44.90, "Modelos prontos de atendimento inteligente e agendamento automático para fechar contratos recorrentes."),
    ("Segundo Cérebro Potencializado por Inteligência Artificial", "IA & Automação", 29.90, "Organize livros, reuniões e ideias em uma base de conhecimento pesquisável que conecta insights automaticamente."),
    ("Análise de Dados e Decisão Executiva com Copilotos", "IA & Automação", 37.90, "Transforme planilhas complexas em relatórios estratégicos e previsões de vendas em questão de segundos."),
    ("Ética, Privacidade e Segurança na Era dos Modelos Abertos", "IA & Automação", 32.90, "Aprenda a rodar modelos localmente e blindar dados sensíveis da sua empresa contra vazamentos."),
    ("Copywriting Neural: Textos que Convertem em Qualquer Nicho", "IA & Automação", 36.90, "Combine psicologia do consumidor com geração assistida para criar páginas de vendas de alta conversão."),
    ("O Futuro do Trabalho Híbrido: Habilidades Insubstituíveis", "IA & Automação", 29.90, "Como se posicionar no topo do mercado liderando sistemas inteligentes em vez de competir com eles."),

    # 2. RENDA DIGITAL & ECONOMIA CRIATIVA (10 E-books)
    ("Economia dos Criadores Invisíveis: Monetize Sem Mostrar o Rosto", "Renda Digital", 44.90, "Estratégias de canais dark, curadoria de nicho e perfis temáticos de alto engajamento e receita passiva."),
    ("Produtos Digitais de Ticket Rápido: Funis de Venda Direta", "Renda Digital", 49.90, "Estruture ofertas irresistíveis entre R$ 29 e R$ 97 com tráfego direto e lucro desde o primeiro dia."),
    ("Newsletters Lucrativas: Construa uma Audiência Proprietária", "Renda Digital", 34.90, "Por que o e-mail voltou ao topo e como transformar leitores fiéis em assinantes e patrocinadores."),
    ("Comunidades Pagas: O Novo Modelo de Recorrência Digital", "Renda Digital", 39.90, "Crie ecossistemas fechados onde membros pagam mensalmente por networking, curadoria e acesso."),
    ("Storytelling Magnético para Vídeos Curtos de Alta Retenção", "Renda Digital", 31.90, "Ganchos visuais e narrativos nos primeiros 3 segundos para dominar algoritmos de alcance orgânico."),
    ("Vendas em Dólar Morando no Brasil: Guia de Operação Global", "Renda Digital", 46.90, "Como estruturar produtos, serviços e recebimentos internacionais para multiplicar seu poder de compra."),
    ("Afiliado 3.0: Curadoria de Autoridade e Reviews de Alta Conversão", "Renda Digital", 29.90, "Abandone o spam e construa ativos digitais que geram comissões diárias através de confiança real."),
    ("Design de Ofertas Irresistíveis: Psicologia de Precificação", "Renda Digital", 38.90, "Como empacotar conhecimento comum de um jeito tão claro que o cliente sente que é barato pagar."),
    ("Automação de Tráfego e Escala de Campanhas Digitais", "Renda Digital", 42.90, "Métricas essenciais, leitura de criativos e regras de escala sem queimar orçamento."),
    ("Branding Pessoal Minimalista: Autoridade Sem Ostentação", "Renda Digital", 35.90, "Construa uma marca pessoal respeitada focada em profundidade técnica, estética limpa e resultados."),

    # 3. BIOHACKING, LONGEVIDADE & SAÚDE MENTAL (8 E-books)
    ("Protocolo Sono Profundo: Arquitetura do Descanso Reparador", "Biohacking & Saúde", 34.90, "Ajuste seu ciclo circadiano, temperatura e exposição à luz para acordar com energia máxima."),
    ("Dopamina Limpa: Detox Digital e Recuperação do Foco", "Biohacking & Saúde", 29.90, "Reverta a fadiga mental causada por telas e recupere o prazer em tarefas profundas e desafiadoras."),
    ("Longevidade Aplicada: Biomarcadores e Hábitos Centenários", "Biohacking & Saúde", 47.90, "O que a ciência atual revela sobre metabolismo, massa muscular e prevenção celular para viver mais e melhor."),
    ("Nutrição Cognitiva: Combustível para Clareza Mental", "Biohacking & Saúde", 33.90, "Alimentos, hidratação e suplementação baseada em evidências para eliminar a névoa mental."),
    ("Controle do Estresse e Resiliência do Sistema Nervoso", "Biohacking & Saúde", 31.90, "Técnicas respiratórias e protocolos fisiológicos rápidos para desativar a ansiedade em minutos."),
    ("Treino Híbrido: Força Estética e Condicionamento Cardiovascular", "Biohacking & Saúde", 39.90, "Periodização inteligente de 4 sessões semanais para construir um físico atlético e funcional."),
    ("Saúde Intestinal e o Eixo Cérebro-Intestino na Prática", "Biohacking & Saúde", 36.90, "Como o microbioma influencia diretamente seu humor, imunidade e disposição diária."),
    ("Cronobiologia Produtiva: Trabalhe no Ritmo do Seu DNA", "Biohacking & Saúde", 29.90, "Descubra seu cronotipo e alinhe suas tarefas mais difíceis aos picos naturais de alerta."),

    # 4. FINANÇAS MODERNAS & PATRIMÔNIO (8 E-books)
    ("Arquitetura da Liberdade Financeira: Carteira Blindada", "Finanças Modernas", 44.90, "Alocação inteligente entre renda fixa, ações globais e reservas de valor para atravessar qualquer crise."),
    ("Criptoativos e Web3 Sem Ilusões: Fundamentos e Custódia", "Finanças Modernas", 49.90, "Entenda ciclos de mercado, autocustódia segura e como separar tecnologia real de especulação vazia."),
    ("Psicologia do Dinheiro: Elimine Vieses que Sabotam Seu Caixa", "Finanças Modernas", 32.90, "Identifique gatilhos emocionais de consumo e construa um sistema automático de enriquecimento."),
    ("Renda Passiva com Dividendos e Fundos Imobiliários", "Finanças Modernas", 38.90, "Passo a passo para montar uma máquina de fluxo de caixa mensal previsível e crescente."),
    ("Finanças para Empreendedores Digitais: Separação e Lucro Real", "Finanças Modernas", 36.90, "Como organizar fluxo de caixa, reservas tributárias e pró-labore sem sufocar o crescimento."),
    ("Minimalismo Financeiro: Compre Menos, Viva Melhor", "Finanças Modernas", 29.90, "Corte gastos invisíveis e direcione seu capital apenas para experiências e ativos que importam."),
    ("Investimentos Globais: Dolarizando Seu Patrimônio com Segurança", "Finanças Modernas", 42.90, "Como abrir conta no exterior e investir nas maiores empresas de tecnologia do mundo."),
    ("Negociação de Alto Impacto: Como Fechar Acordos Melhores", "Finanças Modernas", 35.90, "Técnicas práticas para negociar contratos, salários e parcerias ganhando respeito na mesa."),

    # 5. PRODUTIVIDADE EXTREMA & CARREIRA (7 E-books)
    ("Deep Work 2026: O Guia Definitivo do Foco Ininterrupto", "Produtividade Extrema", 34.90, "Bloqueie distrações digitais e produza em 4 horas o que a maioria leva uma semana inteira."),
    ("Sistemas Atômicos: Como Construir Rotinas Inquebráveis", "Produtividade Extrema", 29.90, "Substitua a força de vontade falível por ambientes e gatilhos que tornam a disciplina automática."),
    ("Gestão de Projetos Pessoais com Metodologia Ágil", "Produtividade Extrema", 33.90, "Use sprints semanais e quadros visuais para tirar grandes projetos do papel sem procrastinar."),
    ("Leitura Dinâmica e Síntese: Absorva 1 Livro por Semana", "Produtividade Extrema", 31.90, "Técnicas de leitura ativa e fichamento para transformar informação em aplicação imediata."),
    ("Comunicação Executiva: Clareza, Síntese e Presença", "Produtividade Extrema", 37.90, "Aprenda a apresentar ideias complexas em 2 minutos e conquistar liderança em qualquer reunião."),
    ("Zero Caixa de Entrada: Organização Digital Minimalista", "Produtividade Extrema", 29.90, "Limpe arquivos, e-mails e notificações para manter sua mente leve e seu espaço digital rápido."),
    ("O Poder do Não Estratégico: Protegendo Seu Tempo e Energia", "Produtividade Extrema", 32.90, "Como recusar demandas sem gerar atrito e focar exclusivamente nas poucas ações que trazem 80% de resultado."),

    # 6. ESTÉTICA FUTURISTA, DESIGN & DESENVOLVIMENTO PESSOAL (7 E-books)
    ("Estética Techwear e Minimalismo Urbano: Guia de Estilo 2050", "Estética & Lifestyle", 39.90, "Tecidos tecnológicos, cortes funcionais e paleta monocromática para um visual moderno e atemporal."),
    ("Arquitetura de Ambientes Minimalistas e Produtivos", "Estética & Lifestyle", 34.90, "Iluminação, ergonomia e organização espacial para transformar seu quarto ou escritório em um santuário de foco."),
    ("Estoicismo Moderno: Calma Inabalável no Caos Contemporâneo", "Estética & Lifestyle", 29.90, "Filosofia prática aplicada aos desafios da vida hiperconectada, críticas e tomadas de decisão."),
    ("Inteligência Social e Carisma Silencioso", "Estética & Lifestyle", 36.90, "Como gerar conexão genuína, escuta ativa e presença marcante sem precisar forçar simpatia."),
    ("Design Visual para Não-Designers: Tipografia, Grid e Contraste", "Estética & Lifestyle", 41.90, "Domine os princípios estéticos por trás das marcas mais desejadas do mundo."),
    ("Autodidatismo Acelerado: Aprenda Qualquer Habilidade em 30 Dias", "Estética & Lifestyle", 35.90, "Desconstrução de habilidades, prática deliberada e ciclos rápidos de feedback."),
    ("Manifesto VORTEX: Mentalidade de Construção para a Próxima Década", "Estética & Lifestyle", 45.90, "O manual filosófico e estratégico para criadores, construtores e visionários do novo mundo.")
]

def slugify(text):
    text = text.lower()
    text = re.sub(r'[áàãâä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[íìîï]', 'i', text)
    text = re.sub(r'[óòõôö]', 'o', text)
    text = re.sub(r'[úùûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

def run_seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        assets_dir = os.path.join(os.path.dirname(__file__), 'digital_assets')
        os.makedirs(assets_dir, exist_ok=True)

        badges = ["EM ALTA", "BEST-SELLER", "NOVO 2050", "EXCLUSIVO", "TOP TENDÊNCIA"]

        for idx, (title, category, price, description) in enumerate(EBOOKS_CATALOG, start=1):
            slug = f"{idx:02d}-{slugify(title)}"
            file_name = f"{slug}.html"
            badge = badges[idx % len(badges)]

            product = Product(
                title=title,
                slug=slug,
                category=category,
                description=description,
                price=price,
                product_type='digital',
                file_name=file_name,
                cover_badge=badge
            )
            db.session.add(product)

            file_path = os.path.join(assets_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title} | VORTEX 2050</title>
<style>
  body {{ background: #090A0F; color: #E2E8F0; font-family: system-ui, sans-serif; line-height: 1.8; max-width: 780px; margin: 40px auto; padding: 30px; }}
  .brand {{ color: #00F0FF; font-weight: bold; letter-spacing: 3px; font-size: 12px; }}
  h1 {{ color: #FFFFFF; border-bottom: 1px solid #1E293B; padding-bottom: 15px; }}
  .meta {{ color: #94A3B8; font-size: 14px; margin-bottom: 30px; }}
  .chapter {{ background: #11131C; padding: 25px; border-radius: 10px; border-left: 3px solid #00F0FF; margin-bottom: 25px; }}
</style>
</head>
<body>
  <div class="brand">VORTEX 2050 // EDIÇÃO DIGITAL LICENCIADA</div>
  <h1>{title}</h1>
  <div class="meta">Categoria: {category} • Edição #{idx:02d} • Acesso Vitalício Liberado</div>
  <div class="chapter">
    <h2>Visão Geral e Premissa Central</h2>
    <p>{description}</p>
    <p>Este material faz parte da curadoria oficial VORTEX 2050, desenvolvido para aplicação prática imediata nos cenários tecnológicos, econômicos e comportamentais mais relevantes da atualidade.</p>
  </div>
  <div class="chapter">
    <h2>Capítulo 1: Fundamentos e Arquitetura de Execução</h2>
    <p>1. Diagnóstico do cenário atual e eliminação de ruído operacional.<br>
    2. Implementação dos protocolos centrais descritos nesta edição.<br>
    3. Métricas de acompanhamento semanal e ajuste de rota.</p>
  </div>
  <div class="chapter">
    <h2>Capítulo 2: Plano de Ação de 7 Dias</h2>
    <p>Aplique os conceitos deste guia em blocos focados de 45 minutos diários para consolidar os resultados apresentados.</p>
  </div>
</body>
</html>""")

        db.session.commit()
        print(f"Sucesso! {len(EBOOKS_CATALOG)} e-books cadastrados no banco e gerados em digital_assets/.")

if __name__ == '__main__':
    run_seed()
