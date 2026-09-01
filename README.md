# PK Closet — Social Media App

App interno para criação de artes de **Bom Dia**, **Funcionamento** e **Produto** da PK Closet.

## O que o app faz

- **Bom Dia** (Story 9:16)  
  Frase emocional nova todos os dias + arte no estilo oficial + legenda

- **Funcionamento** (Story 9:16)  
  Comunicado de horário com data, endereço e CTA

- **Produto** (Story ou Post)  
  Foto da peça intacta + opção de modelo real ou virtual + legenda pronta

## Regras importantes

- Logo oficial sempre preservada
- Foto de produto nunca é redesenhada
- Modelo virtual só após aviso e autorização
- Legendadas humanizadas com exatamente **5 hashtags**
- UX com perguntas Sim/Não sempre que possível

## Como rodar

### 1. Instalar dependências

```bash
cd pk_closet_app
pip install -r requirements.txt
```

### 2. Iniciar o app

```bash
streamlit run app.py
```

O app abre no navegador (geralmente http://localhost:8501).

### 3. Usar no celular

- Abra o mesmo endereço na rede local, ou
- Use o download das artes e salve nas Fotos do celular
- Depois publique no Instagram / TikTok

## Estrutura de pastas

```
pk_closet_app/
├── app.py                 ← Interface principal
├── requirements.txt
├── README.md
├── assets/
│   └── logo_oficial.png
├── src/
│   └── composer.py        ← Geração das artes
├── templates/             ← Templates originais (referência)
└── output/                ← Artes geradas
```

## Fluxos resumidos

### Bom Dia
1. App gera frase emocional
2. Você aprova ou pede outra
3. Gera arte + legenda + download

### Funcionamento
1. Informa a data
2. Confirma horário habitual (Sim/Não)
3. Variação sazonal (Sim/Não)
4. Aprova → gera arte + legenda

### Produto
1. Envia foto
2. Já tem modelo real? (Sim/Não)
3. Quer modelo virtual? (com aviso)
4. Nome, cores, grade, preço
5. Story ou Post
6. Aprova → gera arte + legenda pronta para copiar

## Legenda padrão (5 hashtags)

```
#PKCloset #ModaFeminina #LookDoDia #ModaBrasil #EstiloFeminino
```

## Contato da loja

- Instagram / TikTok: @pkclosetrp
- Site: www.pkcloset.com.br
- Endereço: Rua Henrique Dumont, 748 — Jardim Paulista, Ribeirão Preto–SP
- Enviamos para todo o Brasil

---
Versão 1.0 — PK Closet Social Media App
