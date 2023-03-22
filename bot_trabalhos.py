from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
import time
import datetime
from datetime import date
import sys
import codecs
import re
import unidecode
import requests

cadastros = [

    "Desafios e estratégias na prevenção à gravidez na adolescência: Educação em saúde",
    "PROPOSTA DE UM MODELO DE GESTÃO DE SEGURANÇA E SAÚDE NO TRABALHO COMO AÇÃO ESTRATÉGICA: UM ESTUDO DE CASO EM UMA EMPRESA DE CONSTRUÇÃO CIVIL",
]

browser = webdriver.Firefox(executable_path="./geckodriver")
browser.get("http://conepe.guarus.iff.edu.br/admins/sign_in")
browser.maximize_window()
time.sleep(2)
password = browser.find_element_by_id("admin_password")
login = browser.find_element_by_id('admin_login')
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
submit = browser.find_element_by_xpath("//input[@value='Entrar']")
login.send_keys("thiago.nunes@iff.edu.br")
password.send_keys("Thi@g0rinu")
submit.click()
poster_titles = [
    "Gêneros textuais e redes sociais: a experiência com a leitura e a escrita nos projetos Literature-se e Jornal IFFolha Itaperuna",
    "A corporeidade se faz lugar: O samba como instrumento de resignificação da identidade negra.",
    "A EVOLUÇÃO DA REGULAMENTAÇÃO SOBRE A LOGÍSTICA REVERSA DE MEDICAMENTOS E A ATUAL SITUAÇÃO DO MUNICÍPIO DE CAMPOS DOS GOYTACAZES-RJ",
    "BOAS PRÁTICAS NO APRAZAMENTO DE ANTIMICROBIANOS EM PÓS-OPERATÓRIO DE CIRURGIA CARDÍACA",
    "Divulgação científica do Programa de Educação Tutorial Ciências da Natureza por meio do Instagram",
    "Estratégias de uma Liga Acadêmica de Trauma e Emergência de Enfermagem no contexto da pandemia por Covid-19: relato de experiência.",
    "Capitalismo Cognitivo: novas roupas, antigas premissas",
    "Comportamentos empreendedores: um estudo com alunas de cursos técnicos integrados ao ensino médio",
    "Estratégias de uma Liga Acadêmica de Trauma e Emergência de Enfermagem no contexto da pandemia por Covid-19: relato de experiência.",
    "TEATRO APLICADO E O CORPO BRINCANTE: UMA EXPERIÊNCIA COM MULHERES ADICTAS EM RECUPERAÇÃO",
    "O Absenteísmo-análise da assiduidade e da saúde mental dos Servidores da Fundação de Atendimento Socioeducativo do Pará-Um estudo no Núcleo de Gestão de Pessoas",
    "Aprendizagem Baseada em Problemas e Canvas de Projeto: ensino híbrido no estudo da eletricidade",
    "Mudanças no Manejo do Solo e a Observação do Clima na Produtividade da Cana-de-Açúcar no Rio de Janeiro.",
    "Reflexões sobre Saúde do trabalhador em tempos de Uberização: Análise do filme Você não estava aqui (2018) de Ken Loach",
    "Ateliê Criativo: Espaço de Transformatividade",
    "Dinâmicas orientadoras sustentáveis de planejamento e gestão dos microempreendimentos em Cajueiro São João da Barra RJ. 2010 2025",
    "NeuroArt: autocuidado e bem estar",
    "JOGOS LÚDICOS: UMA FERRAMENTA PARA ENSINAR CONTEÚDOS DE CIÊNCIAS.",
    "EDUCAÇÃO DO CAMPO: LIMITES E POSSIBILIDADES DA FORMAÇÃO CONTINUADA PARA EDUCADORES NA BAIXADA CAMPISTA",
    "Mineração de dados para o auxílio de identificação de possíveis novos casos de COVID-19",
    "As articulações público-privadas na política para a educação especial: investigações sobre a atuação das instituições filantrópicas no município de Campos dos Goytacazes",
    "Análise de Plataformas Web para Organização de Lições Multimídia Baseadas em Rotação Individual",
    "Utilização de resíduos de granitos como matéria-prima alternativa no preparo de vidros comerciais",
    "Síntese de vidros aluminoborato dopados com térbio visando o melhoramento da eficiência energética de células solares.",
    "Práticas Dialógicas e Processos de Participação: subsídios para a educação ambiental crítica",
    "Políticas públicas e gestão de desastres ambientais: a importância da articulação entre o saber técnico e o saber popular",
    "MST e o Coletivo LGBT Sem Terra: a expressão de gênero e sexualidade na luta pela terra",
    "Identificando ações de vigilância em saúde do trabalhador do Instituto Federal Fluminense sob a perspectiva teórica das Universidades Promotoras da Saúde",
    "Corporações e rede urbana: lógicas espaciais de expansão da Fontes Promotora de Crédito",
    "Prática de Enfermagem Baseada em Evidências como Ferramenta de Prevenção de Infecção Primária de Corrente Sanguínea na Terapia Intensiva",
    "Características Sócio Demográficas de Idosas Portadoras de HIV/AIDS em Campos dos Goytacazes/RJ.",
    "Internacionalización en Casa: una propuesta para desarrollar la competencia intercultural y promover la ciudadanía global",
    "A mudança da rotina escolar e os desafios do ensino remoto",
    "Desenvolvimento de uma solução IoT para o monitoramento de enchentes e inundações",
    "Eixos de desenvolvimento, isenções fiscais e indústria da transformação em Itatiaia-RJ",
    "As Metodologias Ativas de Ensino-Aprendizagem durante o Ensino Remoto Emergencial e perspectivas pós-pandemia",
    "A rede social virtual Facebook como plataforma de apoio ao Ensino Remoto Emergencial durante a pandemia da Covid-19",
    "MODELOS DE MELHORIA PARA PREVENÇÃO DE INFECÇÕES NA UNIDADE DE TERAPIA INTENSIVA: PROTOCOLO DE REVISÃO DE ESCOPO.",
    "IMPLEMENTAÇÃO DE UMA NOVA METODOLOGIA DIDÁTICA INCLUSIVA PARA O ESTUDO E CONHECIMENTO DA ANATOMIA ANIMAL",
    "Educação em saúde via plataforma digital como cuidado: um estudo fenomenológico",
    "O Programa de Educação Tutorial Ciências da Natureza e suas adequações para atividades remotas no contexto da pandemia da COVID-19",
    "Síntese e caracterização do sistema aluminato de cálcio dopado com terras-raras para aplicações tecnológicas",
    "RELAÇÕES ENTRE A NEUROCIÊNCIA, FORMAÇÃO DE PROFESSORES E O ENSINO DE CIÊNCIAS: uma revisão sistemática de literatura",
    "A REDE SOCIAL INSTAGRAM COMO RECURSO PEDAGÓGICO: CURIOSIDADES DAS CIÊNCIAS",
    "A geração de resíduos durante a pandemia por Covid-19: Velhos e novos hábitos insustentáveis",
    "Arrasta para cima: O Instagram como ferramenta de ensino durante as atividades remotas do PIBID Geografia-IFF",
    "Entre desafios e possibilidades: As contribuições do PIBID para a formação inicial de licenciandos em geografia do IFF",
    "Fake News e seus diferentes tipos: por que acreditamos?",
    "Surdos e profissionais de saúde: produzindo cartilha digital bilíngue para comunicação básica.",
    "Participação do PIBID Artes IFF – Música e Teatro - nos projetos pedagógicos do Colégio Estadual José do Patrocínio: Centenário de Paulo Freire e Resgate do Hino da Escola",
    "Espectroscopia fotoacústica a laser de cascata quântica na detecção de etileno",
    "Agendas Ambientais e Atuação do STF no Governo Bolsonaro",
    "Análise do discurso publicitário no mercado imobiliário: elementos da expansão urbana em Campos dos Goytacazes",
    "Avaliação da utilização de espécies medicinais endêmicas à Região dos Lagos: Um levantamento etnobotânico.",
    "Geração de Segundo Harmônico: um protótipo de baixo custo para a demonstração de um efeito óptico não linear",
    "Análise do clima de segurança do paciente em um setor cirúrgico universitário no período pré - pandêmico",
    "Clima de segurança em centro cirúrgico universitário durante os períodos pré-pandêmico e de pandemia da COVID-19",
    "Estudo comparativo de irradiação solar média entre localidades na região Norte Fluminense",
    "A dinâmica do varejo em Campos dos Goytacazes: análise dos supermercados e suas lógicas e estratégias espaciais",
    "Agricultura Urbana e as Políticas Públicas:discutindo as hortas urbanas em Campos dos Goytazes, Rj.",
    "O Projeto de Vida no IFF campus Campos",
    "O Emprego de Pneus Inservíveis na Construção de Cercas Rurais poderia contribuir com a Redução da Poluição Ambiental?",
    "Biossegurança, segurança dos profissionais do centro cirúrgico e segurança do paciente na COVID - 19: um protocolo de revisão de escopo",
    "Desigualdade do acesso à saúde na Região Imediata de Campos dos Goytacazes",
    "Do ensino presencial para o remoto: reflexões sobre a prática docente",
    "PERFIL CLÍNICO E EPIDEMIOLÓGICO DE PACIENTES ACOMETIDOS POR COVID-19 EM UMA UNIDADE DE TERAPIA INTENSIVA DO SISTEMA ÚNICO DE SAÚDE NO RIO DE JANEIRO",
    "Experimentos de Baixo Custo Para o Ensino de Física",
    "Relações Desiguais Capitalistas e Injustiça Ambiental: breve análise do Racismo Ambiental no Brasil",
    "Sequência didática para ensino do gênero textual relatório no Curso Técnico Integrado de Meio Ambiente: uma proposta interdisciplinar",
    "Comunidades Quilombolas do Imbé e seus espaços de educação",
    "O Ensino da Geografia Econômica na Base Nacional Comum Curricular",
    "Avaliação da cultura de segurança pela equipe multidisciplinar de um centro cirúrgico na COVID-19.",
    "A EDUCAÇÃO CIENTÍFICA COMO FERRAMENTA PARA ESTIMULAR A CONSCIENTIZAÇÃO SOCIAL SOBRE A PRESERVAÇÃO AMBIENTAL",
    "Poluição sonora e seus impactos no contexto escolar",
    "As articulações público-privadas na política para a educação especial: investigações sobre a atuação das instituições filantrópicas no município de Campos dos Goytacazes",
    "A desertificação no Nordeste brasileiro após a Grande Aceleração",
    "A INEFICÁCIA DAS CONSULTAS PÚBLICAS COMO INSTRUMENTO LEGAL DE PARTICIPAÇÃO SOCIAL NAS POLITICAS DE TELECOMUNICAÇÃO NO BRASIL.",
    "Coletivo Campos Mais Verde: uma iniciativa de arborização urbana no município de Campos dos Goytacazes - RJ",
    "Política industrial e difusão desigual e seletiva das tendências da Indústria 4.0 no território brasileiro",
    "Análise do Perfil de Egressos do Curso de Bacharelado em Engenharia Ambiental do Instituto Federal Fluminense campus Campos Guarus",
    "Pibid Artes IFF - Música e Teatro no Colégio Estadual Nelson Pereira Rebel: uma vivência pedagógica em meio à pandemia.",
    "Síntese e caracterização óptica de vidros aluminoborato dopados com Ce3+ e Sm3+ para aplicação na geração de luz branca.",
    "Radiação de Corpo Negro: uma proposta de ensino através da sequência didática UEPS",
    "Cartilha Bilíngue Libras/Português com perguntas e respostas sobre doenças crônicas não transmissíveis (DCNT)",
    "Quem somos nós? Conhecendo o perfil da comunidade interna do IFF visando ações para permanência escolar.",
    "A COMUNICAÇÃO COMO INSTRUMENTO BÁSICO DO CUIDADO DE ENFERMAGEM: contribuições para a segurança do paciente",
    "Ergonomia: Os desafios dos discentes durante a pandemia",
    "Estudo sobre consciência ecológica e incidência de hábitos de consumo sustentável na realidade social da Baixada Fluminense, Rio de Janeiro, 2021.",
    "A ELABORAÇÃO DE ANÁLISE DE RISCOS PARA AS ATIVIDADES COM ELETRICIDADE: UM ESTUDO DE CASO NA CONSTRUÇÃO CIVIL",
    "Revivendo a história: Voltando a academia para cursar outra graduação em Engenharia.",
    "Ergonomia: O esgotamento dos profissionais de saúde durante a pandemia",
    "Diagnóstico do monitoramento da qualidade do ar na região sudeste do Brasil",
    "Ergonomia: A percepção de um Engenheiro do Trabalho em um ambiente hospitalar",
    "O aumento da prática de automedicação no Brasil durante o período de pandemia da COVID-19 e os riscos ambientais e sociais associados",
    "Labirinto dos Resíduos: Conscientizando através da ludicidade",
    "Mortalidade da população Negra em tempos de Covid-19 no Município de Campos dos Goytacazes-RJ. Brasil.2020-2021",
    "Perfil de saúde dos caminhoneiros brasileiros de percursos internacionais",
    "Feira de Ciências como instrumento para a alfabetização científica",
    "Ler e escrever: eis a questão!",
    "Mapas Conceituais nas aulas de Língua portuguesa",
    "Avaliação da qualidade da água do rio Paraíba do Sul no município de Campos dos Goytacazes/RJ a partir de dados governamentais",
    "Transporte público coletivo e desigualdade de acesso à cidade nos distritos do extremo norte de Campos dos Goytacazes-RJ",
    "Máquinas Simples em Rotação por Estações de Aprendizagem",
    "Aplicação do Arranjo Halbach em um Gerador Elétrico para Ondas Oceânicas",
    "Vivências e interações nas ações de cidadania dos jovens de São João da Barra/RJ : Um olhar pela prática extensionista",
    "Letramento Científico através de Práticas Experimentais",
    "Aprendizagem Significativa no Ensino Interdisciplinar na Biomecânica utilizando a abordagem STEAM em uma proposta de Ensino Hibrido",
    "Contribuições do Projeto de Residência Pedagógica no Liceu de Humanidades de Campos: Projeto Ciências da Natureza no Contexto de Pandemia do Covid-19",
    "Desenvolvimento de crianças autistas: letramento como instrumento de melhores condições de saúde",
    "Vacinação em gestantes durante a pandemia da COVID-19: uma análise investigativa da literatura.",
    "RADAR REGULATÓRIO: ESTUDO DE VIABILIDADE DO USO INTELIGÊNCIA ARTIFICIAL NA CRIAÇÃO DE UMA AGENDA REGULATÓRIA ESTRUTURADA NO SETOR DE TELECOMUNICAÇÕES.",
    "Projeto Vitalidade em tempos de pandemia",
    "Estratégia de jogos e brincadeiras na pandemia: experiências do projeto de extensão “Movi Mente”",
    "Projeto Vitalidade em tempos de pandemia",
    "Projeto Vitalidade em tempos de pandemia",
    "Dificuldades do ensino remoto: alternativas da RP de Ciências",
    "Estágio curricular da Educação Física em saúde mental. Um relato de experiência",
    "Discriminação étnico-racial: O impacto na vivência de estudantes negros do curso de licenciatura em Educação Física do IFFluminense",
]

orais = [
    "A conservação dos mangues na APA de Guapimirim e da ESEC da Guanabara — ecossistema aliado contra as mudanças climáticas",
    "Impressão 3D de um sensor fotoacústico para a detecção de metano em baixas concentrações",
    "Modelagem numérica, construção e caracterização de sensores fotoacústicos para detecção de metano em níveis de traços",
    '''Representações e Vozes Indígenas nos Documentários “Amazônia Sociedade Anônima” e “A Última Floresta”''',
    "O USO DA ELASTO-CONTENÇÃO E DA LASERTERAPIA COMO TRATAMENTO ADJUVANTE NAS LESÕES DE MEMBROS INFERIORES",
    "Possíveis influências da obesidade em tarefas cognitivas e motoras de escolares numa perspectiva neuropsicopedagógica",
    "Prevalência de eventos adversos em uma unidade de terapia intensiva especializada em trauma",
    "Caracterização de Sensor Fotoacústico para Detecção de Biomarcadores Oriundos da Respiração Humana",
    "Composição, Segurança e Atividades de Valeriana officinalis L. no Sistema Nervoso Central",
    "Segurança e Atividades Farmacológicas de Bidens pilosa L.",
    "Cálculo de eficiência em módulos fotovoltaicos por meio de curva I-V",
    "Controle Inteligente de Temperatura e Umidade em Data Center",
    "Estudo de Variações de Geometria de um Gerador Linear",
    "Simulador Bidimensional de Condução Transiente de Calor em Meios Porosos – CCMP-2D",
    "The Wizard and The Book: Um Serious Game para Auxiliar o Ensino da Geometria",
    "Experiências do ARQiFF Tube – Canal no YouTube dos Cursos de Graduação e Pós-graduação em Arquitetura e Urbanismo do IFF",
    "Igualdade de gênero e empoderamento de meninas na escola: um estudo no ensino médio",
    "Aprendizagem Baseada em Problemas e Canvas de Projeto: ensino híbrido no estudo da eletricidade",
    "Eixos de desenvolvimento, isenções fiscais e indústria da transformação em Itatiaia-RJ",
    "Cine Darcy: o cinema Universitário da Universidade Estadual do Norte Fluminense Darcy Ribeiro (UENF)",
    "Fazendo Cultura: Receitas tradicionais de famílias da região da estrada de ferro"
]

errors = []
cadastros = []
for i in range(1, 320):
    url = "http://conepe.guarus.iff.edu.br/admin/work/%d/edit/"%i
    browser.get(url)
    time.sleep(1)  
    try:
        
        title = browser.find_element_by_id("work_title").get_attribute('value')
        print("Tentando: ", title)
        # import pdb;pdb.set_trace()
        if title in poster_titles or title in orais:
            check_apresentado = browser.find_element_by_id("work_apresentado")
            
            if not check_apresentado.get_attribute("checked"):
                print("Cadastrando presença: ", title)                
                check_apresentado.click()
                save = browser.find_element_by_name("_save")
                save.click()
            cadastros.append(title)
    except:
        errors.append(url)
cadastrados_str = "CADASTROS,,\n"
for title in cadastros:
    cadastrados_str += '"%s"\n'%title
# import pdb;pdb.set_trace()
open("cadastros.csv", 'w').write(cadastrados_str)
print("Não foi possível cadastrar")
diff = [t for t in poster_titles if t not in cadastros]
[print(t) for t in diff]
print("-------------ERROS-------------")
[print(e) for e in errors]



































