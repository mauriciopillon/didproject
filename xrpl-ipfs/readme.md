# XRPL

Implementação das roles de Holder, Issuer e Verifier no ledger XRPL.

# Como utilizar?

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

## Inicialização do container IPFS
```
docker compose -f ipfs/docker-compose.yaml up -d
```

><details>
><summary>Testando o container (Opcional)</summary>
>
>```
>curl -X POST http://127.0.0.1:5001/api/v0/version
>```
>
></details>

## Diagrama de fluxo das operações

```mermaid
flowchart LR
  subgraph ISSUER["Universidade (Issuer)"]
    I1["Create DID Document <br/>"] --> I2["Create Verifiable Credential<br/>"]
    
  end

  subgraph HOLDER["Aluno (Holder)"]
    H1["Create DID Document <br/>"] --> H2["Accept XRPL Credential<br/>"]
    H2 --> H3["Create Verifiable Presentation<br/>"]
  end

  subgraph VERIFIER["Verificador (Verifier)"]
    V1["Load Verifiable Presentation"] --> V2["Verify EdDSA Signature<br/>"]
    V2 --> V3["Verify XRPL Credential<br/>"]
    V4["Load Verifiable Credential<br/>(OPTIONAL)"] --> V2["Verify EdDSA Signature<br/>"]
  end

  subgraph XRPL["XRPL Ledger"]
    L1[("DID Issuer")]
    L2[("DID Holder")]
    L3[("Credential")]
  end

  subgraph IPFS["IPFS"]
    P1[("issuer_did.json")]
    P2[("diploma_vc.json")]
    P3[("holder_did.json")]
  end

  I1 -->|Set DID to XRPL| L1
  H1 -.-> L2
  H2 -.-> L3
  I2 -.-> V4

  I1 -->|upload issuer DID to IPFS| P1
  I2 -->|upload Verifiable Credential to IPFS| P2
  H1 -->|upload holder DID to IPFS| P3

  P1 -->|"download issuer_did <br/> (optional)"| V2
  P3 -->|download holder_did| V2

  H3 --> V1
  V2 -.-> L2
  V3 -.-> L3

```

## Diagrama de Sequência das operações
```mermaid
sequenceDiagram
  participant Issuer as Universidade (Issuer)
  participant Holder as Aluno (Holder)
  participant Verifier as Verificador (Verifier)
  participant XRPL as XRPL Ledger
  participant IPFS as IPFS

  Issuer->>Issuer: Create DID Document
  Issuer->>IPFS: Upload issuer_did.json
  Issuer->>XRPL: Set DID to XRPL

  Issuer->>Issuer: Create Verifiable Credential
  Issuer->>IPFS: Upload diploma_vc.json

  Holder->>Holder: Create DID Document
  Holder->>IPFS: Upload holder_did.json
  Holder->>XRPL: Set DID to XRPL

  Holder->>XRPL: Accept XRPL Credential
  XRPL-->>Holder: Credential accepted

  Holder->>Holder: Create Verifiable Presentation
  Holder->>Verifier: Load Verifiable Presentation

  Verifier->>XRPL: check holder XRPL DID for IPFS CID
  XRPL-->>Verifier: IPFS CID for holder DID 
  Verifier->>IPFS: Download holder_did.json
  IPFS-->>Verifier: holder DID

  Verifier->>Verifier: Verify EdDSA Signature

  Verifier->>XRPL: Verify XRPL Credential
  XRPL-->>Verifier: Credential validation result

  opt Optional Verification
      Issuer->>Verifier: Load Verifiable Credential
      Verifier->>XRPL: check issuer XRPL DID for IPFS CID
      XRPL-->>Verifier: IPFS CID for issuer DID
      Verifier->>IPFS: Download issuer_did.json
      IPFS-->>Verifier: issuer DID
      Verifier->>Verifier: Verify EdDSA Signature

  end


```

## Execução das roles

### Issuer (Universidade)

#### 1. Criar documento DID
```
python issuer/create_did_document.py
```
Retorna CID do documento, por exemplo:  ```CID: QmU6ua7J66nUqvLyCN2iERLyNCs9M2C8hZwS9AhFo3fQuW```
#### 2. Criar objeto DID no XRPL ledger 
No arquivo `issuer/xrpl_did/set_did.py`
```

```
#### 3. Criar verifiable credential
```
python issuer/create_verifiable_credential.py
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

