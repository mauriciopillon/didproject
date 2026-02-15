# XRPL

Implementação das roles de Holder, Issuer e Verifier no ledger XRPL.

# Como utilizar?

>[!TIP]
>Ambiente Virtual (Opcional)
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

## Definindo variáveis de ambiente
```
cp .env.example .env
```

## Diagrama de fluxo das operações

```mermaid
flowchart LR
  subgraph ISSUER["Universidade (Issuer)"]
    I1["Publicar DID <br/>(set_did)"] ------> I2["Emitir Credential<br/>(issue_credential)"]
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

## Execução das roles

### Issuer (Universidade)

1. Publicar DID
```
python issuer/set_did.py
```
2. Emitir credencial
```
python issuer/issue_credential.py
```

><details>
><summary>Consultar/Deletar DID (Opcional)</summary>
>   
> 1. Consultar (Retorna objeto DID do ledger) 
>
>```
>python issuer/check_did.py
>```
>
> 2. Deletar (Exclui objeto DID do ledger) 
>
>```
>python issuer/delete_did.py
>```
>
></details>

### Holder (Aluno)

3. Publicar DID
```
python holder/set_did.py
```
4. Aceitar credencial
  >[!Warning]
  > Credencial deve ter sido emitida pelo Issuer antes de poder ser aceita.
```
python holder/accept_credential.py
```
5. Criar Verifiable Presentation (VP)
  >[!Warning]
  > Credencial deve ter sido emitida pelo Issuer antes de poder ser referenciada na VP.
```
python holder/create_verifiable_presentation.py
```
  >[!Note]
  > Por padrão, o caminho da VP criada é `holder/verifiable_presentations/`

><details>
><summary>Consultar/Deletar DID (Opcional)</summary>
>   
> 1. Consultar (Retorna objeto DID do ledger) 
>
>```
>python holder/check_did.py
>```
>
> 2. Deletar (Exclui objeto DID do ledger) 
>
>```
>python holder/delete_did.py
>```
>
></details>

### Verifier

6. Verificar a validade da assinatura EdDSA da VP
  >[!Warning]
  > VP deve ter sido criada pelo Holder (5) para ser verificada.
   ```
   python verifier/verify_vp_signature.py
   ```
7. Verificar a validade da credencial XRPL
  >[!Warning]
  > Credencial deve ter sido emitida pelo Issuer (2) e aceita pelo Holder (4).
   ```
   python verifier/verify_xrpl_credential.py
   ```

