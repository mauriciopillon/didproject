# XRPL

Implementação das roles de Holder, Issuer e Verifier no ledger XRPL.

# Como utilizar?

>[!TIP]
>(Opcional) Ambiente Virtual
><details>
><summary> Windows: </summary>
>
>### Criando o ambiente virtual
>
>```
>python -m venv .venv
>```
>
>### Inicializando o ambiente virtual
>
>```
>source .venv/Scripts/activate
>```
>
></details>

## Instalando dependências
```
pip install -r requirements.txt
```

## Diagrama de fluxo das operações

```mermaid
flowchart LR
  subgraph ISSUER["Universidade (Issuer)"]
    I1["Publicar DID <br/>(set_did)"] --> I2["Emitir Credential<br/>(issue_credential)"]
  end

  subgraph HOLDER["Aluno (Holder)"]
    H1["Publicar DID <br/>(set_did)"] --> H2["Aceitar Credential<br/>(accept_credential)"]
    H2 --> H3["Montar + Assinar VP<br/>(create_verifiable_presentation (JWS Ed25519))"]
  end

  subgraph VERIFIER["Verificador (Verifier)"]
    V1["Receber VP"] --> V2["Validar assinatura (verify_vp_signature) "]
    V2 --> V3["Validar Credential no XRPL<br/>(verify_xrpl_credential)"]
  end

  subgraph XRPL["XRPL Ledger"]
    L1[("DID Issuer")]
    L2[("DID Holder")]
    L3[("Credential")]
  end

  I1 -.-> L1
  I2 -.-> L3
  H1 -.-> L2
  H2 -.-> L3

  H3 --> V1
  V2 -.-> L2
  V3 -.-> L3

```
