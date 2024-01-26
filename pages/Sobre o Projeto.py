import streamlit as st

#st.markdown('<head><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"></head>', unsafe_allow_html = True)

st.set_page_config(page_title= 'Sobre o Projeto', layout='wide', page_icon= ':fuelpump:')
st.title('Desenvolvimento do Projeto 🛠️')

st.markdown('<p style="text-align: justify;">Este projeto foi um Tech Challenge proposto na quarta fase do curso de Pós-graduação em Data Analytics da faculdade Fiap em que nós alunos fomos convidados a analisar o preço histórico do barril de petróleo e a partir dessa análise cumprir alguns desafios:</p>', unsafe_allow_html = True)
st.markdown('- Criar um dashboard interativo')
st.markdown('- Apresentar insights')
st.markdown('- Criar um modelo preditivo com Série Temporal')
st.markdown('- Fazer deploy do modelo em produção')

st.markdown('## Pipeline')
miro_url = 'https://miro.com/app/live-embed/uXjVN1YW9H4=/?moveToViewport=-1291,-645,2580,1288&embedId=482323719511'
st.markdown(f'<iframe width="80%" height="600" src="{miro_url}" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>', unsafe_allow_html=True)


st.markdown('## Links Úteis')
st.markdown('##### Repositório do projeto')
st.markdown('[Repositório do projeto no Github](https://github.com/kfpetruz/Dash-e-Modelo-Preditivo-Combustiveis)')
st.markdown('##### Fontes de dados')
st.markdown('[Preço do Petróleo](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view)')
st.markdown('[Taxa de Câmbio Dólar-Real](http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M)')
st.markdown('##### Fontes informacionais')
st.markdown('[Site BBC News Brasil - publicado em maio/2015](https://www.bbc.com/portuguese/noticias/2015/05/150508_china_desaceleracao_lgb)') 
st.markdown('[Site Exame - publicado em novembro/2015](https://exame.com/economia/precos-do-petroleo-se-aproximam-do-fundo-do-poco-de-2008/)')
st.markdown('[Site Veja - publicado em abril/2020](https://veja.abril.com.br/economia/petroleo-tem-menor-preco-em-18-anos-por-queda-na-demanda-devido-covid-19)')
st.markdown('[Jornal Nexo - março/2022](https://www.nexojornal.com.br/expresso/2022/03/17/5-gr%C3%A1ficos-para-entender-20-anos-de-pre%C3%A7os-da-gasolina)')  

st.markdown('## Equipe')
st.markdown('#####  Keila Ferreira Petruz - Analista de BI </span>  <a href="https://www.linkedin.com/in/keila-ferreira-petruz/" target="_blank"  style="margin: 0px 5px 0px 10px;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="30" height="30"></a> <a href="https://github.com/kfpetruz" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="30" height="30"></a>', unsafe_allow_html = True)
st.markdown('##### Tainá Maria Dias de Paula - Analista de BI </span>  <a href="https://www.linkedin.com/in/tainamdpaula/" target="_blank"  style="margin: 0px 5px 0px 10px;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="30" height="30"></a> <a href="https://github.com/tainamaria" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="30" height="30"></a>', unsafe_allow_html = True)


#Verificar se é possível inerir um frame com o Miro interativo - OK
#Melhorar o visual da página - OK
#Desenhar o modelo no Miro
#PUBLICAR O GITHUB QUANDO ENTREGAR O PROJETO
#testar todos os links
# Pegar uma referência da subida do preço após a pandemia